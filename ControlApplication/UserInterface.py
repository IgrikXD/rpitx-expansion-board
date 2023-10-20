from Device import *
from Filter import *
from whiptail import Whiptail

OK_BUTTON = 0
CANCEL_BUTTON = 1

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

    def chooseBoard(self):
        selected_board = self.whiptail_interface.menu("Choose your board:", self.devices_list)
        # <Cancel> button has been pressed
        if(selected_board[1] == CANCEL_BUTTON):
            self.whiptail_interface.msgbox(FAREWELL_MESSAGE)
            exit(0)
        return selected_board[0]
    
    def chooseMenuItem(self):
        return self.whiptail_interface.menu("Choose an action:", self.configuration_actions)
        
    def displayInfo(self, info):
        self.whiptail_interface.msgbox(info)

    def loadConfiguration(self, selected_board):
        while True:
            configuration_path = self.whiptail_interface.inputbox("Enter the path of the configuration file:", f"{CONFIGS_DIR}{selected_board}.pkl")
            # <Cancel> button has been pressed
            if(configuration_path[1] == CANCEL_BUTTON):
                self.whiptail_interface.msgbox("Configuration not loaded! Please choose another board.")
                return None
            else:
                try:
                    with open(configuration_path[0], 'rb') as device_configuration_file:
                        device = pickle.load(device_configuration_file)
                    self.whiptail_interface.msgbox("Configuration loaded succesfully!")
                    return device
                except FileNotFoundError:
                    # You will be prompted to enter the new file path
                    self.whiptail_interface.msgbox("Configuration file not found!")

    def saveConfiguration(self, device):
        os.makedirs(CONFIGS_DIR, exist_ok=True)

        file_path = f"{CONFIGS_DIR}{device.model_name}.pkl"
        
        with open(file_path, 'wb') as device_configuration_file:
            pickle.dump(device, device_configuration_file)
        
        self.whiptail_interface.msgbox(f"Configuration saved!\nFile: {file_path}")

    def createActionsList(self, device):
        actions_list = [] 
        for i, filter_obj in enumerate(device.filters):
            actions_list.append(f"Activate filter {i + 1}: {filter_obj.model_number}, {filter_obj.description}")
        if (device.lna != None):
                actions_list.append(f"Toogle LNA state: {device.lna.model_number}, {device.lna.description}")
        
        return actions_list

    def updateBoardInfo(self, active_filter, is_lna_activated, device):
        board_status = f"Active filter: {active_filter}\n"
        if (device.lna != None):
            board_status += f"Is LNA active: {is_lna_activated}\n"
        board_status += "Select an available action:"

        return board_status

    def chooseBoardAction(self, device):

        actions_list = self.createActionsList(device)
        
        active_filter = "Not selected!"
        is_lna_activated = False

        while True:
            
            board_status = self.updateBoardInfo(active_filter, is_lna_activated, device)

            action_choice = self.whiptail_interface.radiolist(board_status, actions_list)

            if (action_choice[1] == OK_BUTTON) and (len(action_choice[0]) == 0):
                # <OK> has been pressed but no any action choosed
                self.whiptail_interface.msgbox("You have not selected an action!")
            elif (action_choice[1] == CANCEL_BUTTON):
                # <Cancel> button has been pressed
                self.whiptail_interface.msgbox(FAREWELL_MESSAGE)
                exit(0)
            else:
                active_filter = ' '.join(action_choice[0])
                if (action_choice[0][1] == "filter"):
                    device.enableFilter(actions_list.index(active_filter) + 1)
                    self.whiptail_interface.msgbox(f"{active_filter} enabled!")
                elif (action_choice[0][1] == "LNA"):
                    is_lna_activated = device.toogleLNA()
                    if (is_lna_activated):
                        self.whiptail_interface.msgbox(f"LNA enabled!")
                    else:
                        self.whiptail_interface.msgbox(f"LNA disabled!")
                else:
                    self.whiptail_interface.msgbox("Error in device configuration!")

    def createConfiguration(self, selected_board, filter_objects):
        device = Device(selected_board)

        for i in range(device.filters_amount):
            
            unique_case_styles = sorted(set(filter.case_style for filter in filter_objects))
            filter_case = self.whiptail_interface.menu(f"Choose case for filter {i + 1} from {device.filters_amount}:", unique_case_styles)

            # <Cancel> button has been pressed
            if(filter_case[1] == CANCEL_BUTTON):
                self.whiptail_interface.msgbox(CONFIGURATION_CREATED_ABORTED)
                return None
            
            case_style_choice = unique_case_styles.index(filter_case[0])
            selected_case_style = unique_case_styles[case_style_choice]

            available_model_numbers = [filter.model_number for filter in filter_objects if filter.case_style == selected_case_style]
            filter_model = self.whiptail_interface.menu(f"Avaliable filter models for '{selected_case_style}' case:", available_model_numbers)

            # <Cancel> button has been pressed
            if(filter_model[1] == CANCEL_BUTTON):
                self.whiptail_interface.msgbox(CONFIGURATION_CREATED_ABORTED)
                return None

            model_number_choice = available_model_numbers.index(filter_model[0])
            selected_model_number = available_model_numbers[model_number_choice]

            # We find a filter that matches the parameters in the list of all available filters, 
            # and add it to the list of filters for a specific device
            for filter in filter_objects:
                if (filter.model_number == selected_model_number) and (filter.case_style == selected_case_style):
                    device.filters.append(filter)
                    break

        return device
