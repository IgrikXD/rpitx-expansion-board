
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor
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

APP_VERISON = 0.2
# -----------------------------------------------------------
# Changelog:
# -----------------------------------------------------------
# Version 0.2: 
# -----------------------------------------------------------
# When the activateRFPath() function is called, 
# the activateRFOutput() function is called on a separate 
# thread for each of the RFSwitch objects. This eliminates 
# the problem of sequential switching of GPIO states for each 
# of the RFSwitch objects - first the input switch was switched, 
# then the output switch. Now, we switch the states of two 
# switches simultaneously.
# The ComponentsList constructors are now called in separate 
# threads, which allows reading data about filters and 
# amplifiers in parallel rather than sequentially.
# When creating a ComponentsList object, each of the .csv files 
# is now processed in a separate thread.
# Added highlighting of application start and stop timestamp 
# using '-' signs.
# -----------------------------------------------------------


def showHelpInfo(app_version, log_filename):
    help_info = (
        f"rpitx-control {app_version} - 2023 Ihar Yatsevich\n"
        f"{Fore.YELLOW}Avaliable application arguments:{Style.RESET_ALL}\n"
        f"{Fore.GREEN}--use-mock-gpio{Style.RESET_ALL}         Using MockFactory to simulate real GPIO ports.This allows the application " 
        f"to run on devices other than RaspberryPi without causing a GPIO initialization error. Used for "
        f"debugging and testing GPIO port states.\n"
        f"{Fore.GREEN}--show-debug-info{Style.RESET_ALL}       Output debugging information to a file: {log_filename}"
    )
    print(help_info)

def main():

    # The program was launched with the --help argument. We display the help information and finish the work.
    if ("--help" in sys.argv):
        showHelpInfo(APP_VERISON, LOG_FILENAME)
        exit(0)

    user_interface = UserInterface(Device.DEVICES_LIST, UserInterface.CONFIGURATION_ACTIONS, LOG_FILENAME)

    # Initializing available filter and amplifier models
    with ThreadPoolExecutor(max_workers=2) as executor:
        filters_future = executor.submit(ComponentsList, ComponentsList.FILTER, FILTER_MODELS_DIR, FILTER_DUMP_FILE, LOG_FILENAME)
        amplifiers_future = executor.submit(ComponentsList, ComponentsList.AMPLIFIER, AMPLIFIER_MODELS_DIR, AMPLIFIER_DUMP_FILE, LOG_FILENAME)

        filters_list = filters_future.result()
        amplifiers_list = amplifiers_future.result()

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