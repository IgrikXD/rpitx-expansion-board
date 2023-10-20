from Amplifier import *
from Device import *
from Filter import *
from RFSwitch import *
from UserInterface import *

FILTERS_SWITCH_TRUTH_TABLE = 1
LNA_SWITCH_TRUTH_TABLE = 2

def main():

    filters_list = FiltersList(Filter.FILTER_MODELS_DIR)
    amplifiers_list = AmplifiersList(Amplifier.AMPLIFIER_MODELS_DIR)
    user_interface = UserInterface(Device.DEVICES_LIST, UserInterface.CONFIGURATION_ACTIONS)

    while True:
        board = user_interface.chooseBoard()
        action = user_interface.chooseAction()

        # <Cancel> button has been pressed
        # You will be prompted to select your device again
        if (action[BUTTONS_STATE] == CANCEL_BUTTON):
            continue
        
        # "Create a new device configuration" has been choosen
        elif (action[USER_CHOICE] == UserInterface.CONFIGURATION_ACTIONS[0]):
            device = user_interface.createConfiguration(board, filters_list.data, amplifiers_list.data)
            if device == None:
                continue
            user_interface.saveConfiguration(device)

        # "Load device configuration" has been choosen
        if (action[USER_CHOICE] == UserInterface.CONFIGURATION_ACTIONS[1]):
            device = user_interface.loadConfiguration(board)
            if device == None:
                continue
        
        device.initFilterRFSwitches(FilterSwitch.FILTER_INPUT_SWITCH_GPIO_PINS, 
                                    FilterSwitch.FILTER_OUTPUT_SWITCH_GPIO_PINS, 
                                    Device.DEVICE_TYPE_MAPPING[board][FILTERS_SWITCH_TRUTH_TABLE])
        
        # The LNA will only be initialized if the DEVICE_TYPE_MAPPING structure 
        # contains switch information to control the LNA
        device.initLNA(LNASwitch.LNA_INPUT_SWITCH_GPIO_PINS, 
                       LNASwitch.LNA_OUTPUT_SWITCH_GPIO_PINS, 
                       Device.DEVICE_TYPE_MAPPING[board][LNA_SWITCH_TRUTH_TABLE])
        
        # Displaying text information about the active device configuration
        user_interface.displayInfo(device.getConfigurationInfo())
        # The main application menu, allowing you to select and enable a specific filter or toogle LNA state
        user_interface.chooseBoardAction(device)
    # End of while loop

if __name__ == "__main__":
    main()