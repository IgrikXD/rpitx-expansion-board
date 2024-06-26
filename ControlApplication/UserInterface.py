import os
import pickle
from ControlApplication.Components import *
from ControlApplication.Device import *
from ControlApplication.Logger import *
from whiptail import Whiptail

# Which button was pressed?
OK_BUTTON = 0
CANCEL_BUTTON = 1
# Are we reading the state of the button or the result of the execution?
BUTTONS_STATE = 1
USER_CHOICE = 0

# Absolute path to the directory with the program source files
APPLICATION_DIR = os.path.dirname(os.path.abspath(__file__))
# Path to the directory where expansion board configuration files are saved
CONFIGS_DIR = f"{APPLICATION_DIR}/SavedConfiguration/"

APPLICATION_TITLE = "rpitx-expansion-board control application"
FAREWELL_MESSAGE = "Thanks for using rpitx-expansion-board project!"
CONFIGURATION_CREATED_ABORTED = "Configuration creation aborted!"

class UserInterface:

    def __init__(self, log_filename = None):
        self.whiptail_interface = Whiptail(title=APPLICATION_TITLE)
        self.log_filename = log_filename
        
        if log_filename:
            self.logger = Logger(log_filename)
            self.displayInfo(f"Debug mode enabled!\n\nLogs will be writed to: {log_filename}")
            self.logger.logMessage(f"Application running!", Logger.LogLevel.INFO, True, True)
        else:
            self.logger = None

    def chooseItem(self, prompt, items, exit_if_cancel_pressed = False):
        user_action = self.whiptail_interface.menu(prompt, items)
        # <Cancel> button has been pressed
        if (user_action[BUTTONS_STATE] == CANCEL_BUTTON):
            if exit_if_cancel_pressed:
                self.displayFarewellMessageAndExit()
            return None
    
        return user_action[USER_CHOICE]

    def displayInfo(self, info):
        self.whiptail_interface.msgbox(info, extra_args=["--scrolltext"])

    def displayFarewellMessageAndExit(self):
        self.displayInfo(FAREWELL_MESSAGE)
        
        if self.logger:
            self.logger.logMessage(f"Application stopped!", Logger.LogLevel.INFO, True, True)
        exit(0)

    def loadDeviceConfiguration(self):
        if not os.path.exists(CONFIGS_DIR) or not any(file.endswith('.pkl') for file in os.listdir(CONFIGS_DIR)):
            self.displayInfo(f"No configuration files found in the directory: {CONFIGS_DIR}"
                                "\n\nPlease create a new device configuration!")
            return None

        configuration_files_list = [file for file in os.listdir(CONFIGS_DIR) if file.endswith(".pkl")]

        configuration_path = self.chooseItem(
            "Select a configuration file:", configuration_files_list)

        if not configuration_path:
            return None
        
        with open(f"{CONFIGS_DIR}/{configuration_path}", 'rb') as device_configuration_file:
            device = pickle.load(device_configuration_file)

        if self.logger:
            self.logger.logMessage(f"Device configuration loaded: {CONFIGS_DIR}/{configuration_path}", Logger.LogLevel.INFO)

        self.displayInfo("Configuration loaded succesfully!")
        
        return device

    def saveDeviceConfiguration(self, device):
        os.makedirs(CONFIGS_DIR, exist_ok=True)

        file_path = os.path.join(CONFIGS_DIR, f"{device.model_name}.pkl")
        
        with open(file_path, 'wb') as device_configuration_file:
            pickle.dump(device, device_configuration_file)
        
        if self.logger:
            self.logger.logMessage(f"Device configuration info saved: {file_path}", Logger.LogLevel.INFO)
        
        self.displayInfo(f"Configuration saved!\n\nFile: {file_path}")

    def __createActionsList(self, device):
        actions_list = [(f"Activate filter {i + 1}", f"{filter_obj.model_number}, {filter_obj.description}") 
                        for i, filter_obj in enumerate(device.filters) 
                        if filter_obj.model_number != None]

        if device.lna_switch is not None:
            lna = device.lna[0]
            actions_list.append((f"Toggle LNA state", f"{lna.model_number}, {lna.description}, {lna.f_low} - {lna.f_high} MHz"))
        
        return actions_list

    def __updateBoardInfo(self, active_filter, is_lna_activated, device):
        board_status = f"Device type: {device.model_name}\n"
        board_status += f"Active filter: {active_filter}\n"
        
        if device.lna_switch is not None:
            board_status += f"Is LNA active: {is_lna_activated}!\n"
        board_status += "Select an available action:"

        return board_status

    def chooseBoardAction(self, device):

        ACTIONS_LIST = self.__createActionsList(device)
        
        active_filter = "Not selected!"
        is_lna_activated = False

        while True:
            
            board_status = self.__updateBoardInfo(active_filter, is_lna_activated, device)
            user_choice = self.chooseItem(board_status, ACTIONS_LIST, True)

            if "Activate filter" in user_choice:
                filter_id = int(user_choice[-1])
                device_filter = device.filters[filter_id - 1]
                active_filter = f"{filter_id} - {device_filter.model_number}, {device_filter.description}"

                if device.filter_switch.enableFilter(filter_id):
                    self.displayInfo(f"Filter {active_filter} enabled!")
                else:
                    self.displayInfo("Error in device configuration!")
            
            elif "Toggle LNA" in user_choice:
                is_lna_activated = device.lna_switch.toggleLNA()
                self.displayInfo("LNA enabled!" if is_lna_activated else "LNA disabled!")

    def selectComponent(self, components_list, prompt, may_be_not_installed = False):
        while True:
            unique_case_styles = sorted(set(component.case_style for component in components_list))
            
            NOT_INSTALLED_ITEM = "<Not installed>"
            if may_be_not_installed:
                unique_case_styles.insert(0, NOT_INSTALLED_ITEM)
            
            selected_case_style = self.chooseItem(prompt, unique_case_styles, False)
            
            if not selected_case_style:
                # The user pressed <Cancel>, we display info message and return to the initial menu
                self.displayInfo(CONFIGURATION_CREATED_ABORTED)
                return None

            if selected_case_style == NOT_INSTALLED_ITEM:
                # The user pressed <Not installed>
                # We note that the component is not installed on the expansion board
                return BaseModel(None, None, None)

            available_model_numbers = [component.model_number for component in components_list if component.case_style == selected_case_style]
            selected_model_number = self.chooseItem(f"Available models for '{selected_case_style}' case:", available_model_numbers, False)
            
            if not selected_model_number:
                # The user clicked <Cancel>, we suggest selecting the case type again
                continue

            for component in components_list:
                if (component.model_number == selected_model_number) and (component.case_style == selected_case_style):
                    return component

    def __noValidComponents(self, device_filters):
        for filter in device_filters:
            # If there is information on at least one component - return False
            if filter.model_number is not None:
                return False
        
        return True

    def createDeviceConfiguration(self, selected_board, filter_objects, amplifier_objects):
        device = Device(selected_board, self.log_filename)

        # Fill in information about the filters used
        for i in range(device.DEVICE_TYPE_MAPPING[selected_board][0]):
            selected_filter = self.selectComponent(filter_objects, f"Choose filter case for filter {i + 1} from {device.DEVICE_TYPE_MAPPING[selected_board][0]}:", True)
            if selected_filter is None:
                return None
            device.filters.append(selected_filter)

        # We check that there is information about at least one filter installed on the board
        if self.__noValidComponents(device.filters):
            # The user has not selected any filters and returns to the start menu, we have nothing to switch
            self.displayInfo("No information about the filters used! "
                             "Create a new configuration or load an existing one!")
            return None

        # If the expansion board supports built-in LNA, select the LNA used
        if "LNA" in selected_board:
            selected_amplifier = self.selectComponent(amplifier_objects, "Choose amplifier case:")
            if selected_amplifier is None:
                return None
            device.lna.append(selected_amplifier)

        return device