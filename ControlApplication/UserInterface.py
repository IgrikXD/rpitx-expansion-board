import datetime
from Device import *
import os
import pickle
from whiptail import Whiptail

OK_BUTTON = 0
CANCEL_BUTTON = 1
BUTTONS_STATE = 1
USER_CHOICE = 0

APPLICATION_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIGS_DIR = f"{APPLICATION_DIR}/SavedConfiguration/"

APPLICATION_TITLE = "rpitx-expansion-board control application"
FAREWELL_MESSAGE = "Thanks for using rpitx-expansion-board project!"
CONFIGURATION_CREATED_ABORTED = "Configuration creation aborted!"

class UserInterface:

    # List of actions available to perform for a specific device
    APPLICATION_ACTIONS = [
        "Create a new device configuration",
        "Load device configuration"
    ]

    def __init__(self, log_filename = None):
        self.whiptail_interface = Whiptail(title=APPLICATION_TITLE)
        self.log_filename = log_filename
        
        if ("--show-debug-info" in sys.argv) and (log_filename != None):
            self.displayInfo(f"Debug mode enabled!\nLogs will be writed to: {log_filename}")
            with open(log_filename, "a") as file:
                file.write(f"-------------------------------------------------\n")
                file.write(f"[INFO]: Application running at: {datetime.datetime.now()}!\n")
                file.write(f"-------------------------------------------------\n")

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
        
        if ("--show-debug-info" in sys.argv) and (self.log_filename != None):
            with open(self.log_filename, "a") as file:
                file.write(f"-------------------------------------------------\n")
                file.write(f"[INFO]: Application stopped at: {datetime.datetime.now()}!\n")
                file.write(f"-------------------------------------------------\n")
        exit(0)

    def loadDeviceConfiguration(self):
        while True:
            configuration_files_list = [file for file in os.listdir(CONFIGS_DIR) if file.endswith(".pkl")]

            if not configuration_files_list:
                self.displayInfo(f"No configuration files found in the directory: {CONFIGS_DIR} "
                                 "\n\nPlease create a new device configuration!")
                return None

            configuration_path = self.whiptail_interface.menu(
                "Select a configuration file:", configuration_files_list)
            
            # <Cancel> button has been pressed
            if(configuration_path[BUTTONS_STATE] == CANCEL_BUTTON):
                self.displayInfo("Configuration not loaded! "
                                 "Please choose another configuration file or create a new configuration.")
                return None
            
            with open(f"{CONFIGS_DIR}/{configuration_path[USER_CHOICE]}", 'rb') as device_configuration_file:
                device = pickle.load(device_configuration_file)

            if ("--show-debug-info" in sys.argv) and (self.log_filename != None):
                with open(self.log_filename, "a") as file:
                    file.write(f"[INFO]: Device configuration loaded: {configuration_path[USER_CHOICE]}\n")

            self.displayInfo("Configuration loaded succesfully!")
            
            return device

    def saveDeviceConfiguration(self, device):
        os.makedirs(CONFIGS_DIR, exist_ok=True)

        file_path = os.path.join(CONFIGS_DIR, f"{device.model_name}.pkl")
        
        with open(file_path, 'wb') as device_configuration_file:
            pickle.dump(device, device_configuration_file)
        
        if ("--show-debug-info" in sys.argv) and (self.log_filename != None):
            with open(self.log_filename, "a") as file:
                file.write(f"[INFO]: Device configuration info saved: {file_path}\n")
        
        self.displayInfo(f"Configuration saved!\n\nFile: {file_path}")

    def createActionsList(self, device):
        actions_list = [(f"Activate filter {i + 1}", f"{filter_obj.model_number}, {filter_obj.description}") 
                    for i, filter_obj in enumerate(device.filters)]
        
        if device.lna_switch is not None:
            lna = device.lna[0]
            actions_list.append((f"Toggle LNA state", f"{lna.model_number}, {lna.description}, {lna.f_low} - {lna.f_high} MHz"))
        
        return actions_list

    def updateBoardInfo(self, active_filter, is_lna_activated, device):
        board_status = f"Active filter: {active_filter}\n"
        
        if device.lna_switch is not None:
            board_status += f"Is LNA active: {is_lna_activated}!\n"
        board_status += "Select an available action:"

        return board_status

    def chooseBoardAction(self, device):

        ACTIONS_LIST = self.createActionsList(device)
        
        active_filter = "Not selected!"
        is_lna_activated = False

        while True:
            
            board_status = self.updateBoardInfo(active_filter, is_lna_activated, device)
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

    def selectComponent(self, components_list, prompt):
        unique_case_styles = sorted(set(component.case_style for component in components_list))
        case_style_choice = self.whiptail_interface.menu(prompt, unique_case_styles)

        if case_style_choice[BUTTONS_STATE] == CANCEL_BUTTON:
            self.displayInfo(CONFIGURATION_CREATED_ABORTED)
            return None

        selected_case_style = case_style_choice[USER_CHOICE]

        available_model_numbers = [component.model_number for component in components_list if component.case_style == selected_case_style]
        model_choice = self.whiptail_interface.menu(f"Available models for '{selected_case_style}' case:", available_model_numbers)

        if model_choice[BUTTONS_STATE] == CANCEL_BUTTON:
            self.displayInfo(CONFIGURATION_CREATED_ABORTED)
            return None

        selected_model_number = model_choice[USER_CHOICE]

        for component in components_list:
            if (component.model_number == selected_model_number) and (component.case_style == selected_case_style):
                return component

    def createDeviceConfiguration(self, selected_board, filter_objects, amplifier_objects):
        device = Device(selected_board, self.log_filename)

        for i in range(device.DEVICE_TYPE_MAPPING[selected_board][0]):
            selected_filter = self.selectComponent(filter_objects, f"Choose filter case for filter {i + 1} from {device.DEVICE_TYPE_MAPPING[selected_board][0]}:")
            if selected_filter is None:
                return None
            device.filters.append(selected_filter)

        if "LNA" in selected_board:
            selected_amplifier = self.selectComponent(amplifier_objects, "Choose amplifier case:")
            if selected_amplifier is None:
                return None
            device.lna.append(selected_amplifier)

        return device