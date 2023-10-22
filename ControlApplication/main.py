import datetime
from Device import *
from RFSwitch import *
from UserInterface import *
from Components import *

FILTERS_SWITCH_TRUTH_TABLE = 1
LNA_SWITCH_TRUTH_TABLE = 2

AMPLIFIER_MODELS_DIR = "./AmplifiersList"
FILTER_MODELS_DIR = "./FiltersList"
FILTER_DUMP_FILE = "FiltersListDump.pkl"
AMPLIFIER_DUMP_FILE = "AmplifierDump.pkl"

LOG_FILENAME = "./ControlApplication/DebugInfo.log"

def appRunningTimestamp(log_filename):
    if ("--show-debug-info" in sys.argv) and (log_filename != None):
        with open(log_filename, "a") as file:
            file.write(f"[INFO]: Application running at: {datetime.datetime.now()}!\n")

def main():

    appRunningTimestamp(LOG_FILENAME)
    filters_list = ComponentsList(ComponentsList.FILTER, FILTER_MODELS_DIR, FILTER_DUMP_FILE, LOG_FILENAME)
    amplifiers_list = ComponentsList(ComponentsList.AMPLIFIER, AMPLIFIER_MODELS_DIR, AMPLIFIER_DUMP_FILE, LOG_FILENAME)
    user_interface = UserInterface(Device.DEVICES_LIST, UserInterface.CONFIGURATION_ACTIONS, LOG_FILENAME)

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
            user_interface.saveDeviceConfiguration(device)

        # "Load device configuration" has been choosen
        if (action[USER_CHOICE] == UserInterface.CONFIGURATION_ACTIONS[1]):
            device = user_interface.loadDeviceConfiguration(board)
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