from Filter import *
from UserInterface import *

# Directory with .csv files containing models of all filters available for use
FILTER_MODELS_DIR = "./FiltersList"

# List of available device for operation
DEVICES_LIST = [
    "rpitx-expansion-board-SPDT", 
    "rpitx-expansion-board-SP3T", 
    "rpitx-expansion-board-SP4T", 
    "rpitx-expansion-board-SP6T"
]

# Matching a specific device with its configuration
# <DEVICE> : <SWITCH TYPE>, <NUMBER OF AVAILABLE FILTERS>
DEVICE_TYPE_MAPPING = {
    DEVICES_LIST[0]: ("SPDT", 2),
    DEVICES_LIST[1]: ("SP3T", 3),
    DEVICES_LIST[2]: ("SP4T", 4),
    DEVICES_LIST[3]: ("SP6T", 6)
}

# List of actions available to perform for a specific device
CONFIGURATION_ACTIONS = [
    "Create a new device configuration",
    "Load device configuration"
]

def main():

    filters_list = FiltersList(FILTER_MODELS_DIR)
    user_interface = UserInterface(DEVICES_LIST, CONFIGURATION_ACTIONS)

    while True:
        board = user_interface.chooseBoard()
        action = user_interface.chooseAction()

        # <Cancel> button has been pressed
        # You will be prompted to select your device again
        if (action[1] == CANCEL_BUTTON):
            continue
        
        # "Create a new device configuration" has been choosen
        elif (action[0] == CONFIGURATION_ACTIONS[0]):
            device = user_interface.createConfiguration(board, DEVICE_TYPE_MAPPING, filters_list.filters)
            if device == None:
                continue
            user_interface.saveConfiguration(device)

        # "Load device configuration" has been choosen
        if (action[0] == CONFIGURATION_ACTIONS[1]):
            device = user_interface.loadConfiguration(board)
            if device == None:
                continue
        
        # Displaying text information about the active device configuration
        user_interface.displayInfo(device.getConfigurationInfo())
        # The main application menu, allowing you to select and enable a specific filter
        user_interface.chooseActiveFilter(device)
    # End of while loop

if __name__ == "__main__":
    main()