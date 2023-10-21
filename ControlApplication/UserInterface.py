from Device import *
import os
import pickle
from whiptail import Whiptail

OK_BUTTON = 0
CANCEL_BUTTON = 1
BUTTONS_STATE = 1
USER_CHOICE = 0

CONFIGS_DIR = "./SavedConfiguration/"

APPLICATION_TITLE = "rpitx-expansion-board control application"
FAREWELL_MESSAGE = "Thanks for using rpitx-expansion-board project!"
CONFIGURATION_CREATED_ABORTED = "Configuration creation aborted!"

class UserInterface:

    # List of actions available to perform for a specific device
    CONFIGURATION_ACTIONS = [
        "Create a new device configuration",
        "Load device configuration"
    ]

    def __init__(self, devices_list, configuration_actions):
        self.whiptail_interface = Whiptail(title=APPLICATION_TITLE)
        self.devices_list = devices_list
        self.configuration_actions = configuration_actions

    def chooseAction(self):
        return self.whiptail_interface.menu("Choose an action:", self.configuration_actions)

    def displayInfo(self, info):
        self.whiptail_interface.msgbox(info)

    def chooseBoard(self):
        selected_board = self.whiptail_interface.menu("Choose your board:", self.devices_list)
        # <Cancel> button has been pressed
        if (selected_board[BUTTONS_STATE] == CANCEL_BUTTON):
            self.displayInfo(FAREWELL_MESSAGE)
            exit(0)
        return selected_board[USER_CHOICE]

    def loadDeviceConfiguration(self, selected_board):
        while True:
            configuration_path = self.whiptail_interface.inputbox("Enter the path of the configuration file:", 
                                                                  os.path.join(CONFIGS_DIR, f"{selected_board}.pkl"))
            
            # <Cancel> button has been pressed
            if(configuration_path[BUTTONS_STATE] == CANCEL_BUTTON):
                self.displayInfo("Configuration not loaded! Please choose another board.")
                return None
            
            try:
                with open(configuration_path[USER_CHOICE], 'rb') as device_configuration_file:
                    device = pickle.load(device_configuration_file)

                if "--show-debug-info" in sys.argv:
                    print(f"{Fore.YELLOW}[INFO]: Device configuration loaded: {configuration_path[USER_CHOICE]}{Style.RESET_ALL}")

                self.displayInfo("Configuration loaded succesfully!")
                return device
            
            except FileNotFoundError:
                # You will be prompted to enter the new file path
                self.displayInfo("Configuration file not found!")

    def saveDeviceConfiguration(self, device):
        os.makedirs(CONFIGS_DIR, exist_ok=True)

        file_path = os.path.join(CONFIGS_DIR, f"{device.model_name}.pkl")
        
        with open(file_path, 'wb') as device_configuration_file:
            pickle.dump(device, device_configuration_file)
        
        if "--show-debug-info" in sys.argv:
            print(f"{Fore.YELLOW}[INFO]: Device configuration info saved: {file_path}{Style.RESET_ALL}")
        
        self.displayInfo(f"Configuration saved!\nFile: {file_path}")

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
            action_choice = self.whiptail_interface.menu(board_status, ACTIONS_LIST)

            if (action_choice[BUTTONS_STATE] == CANCEL_BUTTON):
                # <Cancel> button has been pressed
                self.displayInfo(FAREWELL_MESSAGE)
                exit(0)
            else:
                user_choice = action_choice[USER_CHOICE]

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

    def createConfiguration(self, selected_board, filter_objects, amplifier_objects):
        device = Device(selected_board)

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

