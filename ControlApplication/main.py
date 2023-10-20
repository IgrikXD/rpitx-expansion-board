from Device import *
from Filter import *
from RFSwitch import *
from UserInterface import *

def main():

    filters_list = FiltersList(Filter.FILTER_MODELS_DIR)
    user_interface = UserInterface(Device.DEVICES_LIST, UserInterface.CONFIGURATION_ACTIONS)

    while True:
        board = user_interface.chooseBoard()
        action = user_interface.chooseAction()

        # <Cancel> button has been pressed
        # You will be prompted to select your device again
        if (action[1] == CANCEL_BUTTON):
            continue
        
        # "Create a new device configuration" has been choosen
        elif (action[0] == UserInterface.CONFIGURATION_ACTIONS[0]):
            device = user_interface.createConfiguration(board, filters_list.data)
            if device == None:
                continue
            user_interface.saveConfiguration(device)

        # "Load device configuration" has been choosen
        if (action[0] == UserInterface.CONFIGURATION_ACTIONS[1]):
            device = user_interface.loadConfiguration(board)
            if device == None:
                continue
        
        device.initFilterRFSwitches(RFSwitch.RF_INPUT_SWITCH_GPIO_PINS, RFSwitch.RF_OUTPUT_SWITCH_GPIO_PINS, Device.DEVICE_TYPE_MAPPING[board][1])
        # Displaying text information about the active device configuration
        user_interface.displayInfo(device.getConfigurationInfo())
        # The main application menu, allowing you to select and enable a specific filter
        user_interface.chooseActiveFilter(device)
    # End of while loop

if __name__ == "__main__":
    main()