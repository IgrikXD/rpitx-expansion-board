
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor
from Device import *
from RFSwitch import *
from UserInterface import *
from Components import *

AMPLIFIER_MODELS_DIR = f"{APPLICATION_DIR}/AmplifiersList"
FILTER_MODELS_DIR = f"{APPLICATION_DIR}/FiltersList"
FILTER_DUMP_FILE = "FiltersListDump.pkl"
AMPLIFIER_DUMP_FILE = "AmplifierDump.pkl"

LOG_FILENAME = f"{APPLICATION_DIR}/DebugInfo.log"

APP_VERISON = 0.3
# -----------------------------------------------------------
# Changelog:
# -----------------------------------------------------------
# Version 0.3: 
# -----------------------------------------------------------
# The FiltersList and AmplifiersList directories have been 
# moved to the ControlApplication directory. Now, dumps of 
# components and configurations of expansion boards are saved 
# taking into account the parent directory in which the 
# application source files are located.
# The application execution order has been changed. Now, when 
# you start the program, you are asked to choose one of two 
# possible actions: creating a new device configuration or 
# loading an existing one.
# When creating a new configuration, you are prompted to 
# select the type of device for which the configuration is 
# being created.
# When loading an existing configuration, you are prompted to 
# select a configuration file from the list (the board type is 
# determined automatically). If the application does not find 
# information about saved configurations, an information message 
# is displayed, after which you will be returned to the main menu.
# Code refactoring.
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
# whiptail_interface.msgbox() is now called with an additional 
# --scrolltext parameter
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

    user_interface = UserInterface(LOG_FILENAME)

    # Initializing available filter and amplifier models
    with ThreadPoolExecutor(max_workers=2) as executor:
        filters_future = executor.submit(ComponentsList, ComponentsList.FILTER, FILTER_MODELS_DIR, FILTER_DUMP_FILE, LOG_FILENAME)
        amplifiers_future = executor.submit(ComponentsList, ComponentsList.AMPLIFIER, AMPLIFIER_MODELS_DIR, AMPLIFIER_DUMP_FILE, LOG_FILENAME)

        filters_list = filters_future.result()
        amplifiers_list = amplifiers_future.result()

    while True:
        user_action = user_interface.chooseItem("Choose an action:", UserInterface.APPLICATION_ACTIONS, True)

        # "Create a new device configuration" has been choosen
        if (user_action == UserInterface.APPLICATION_ACTIONS[0]):
            board = user_interface.chooseItem("Choose your board:", Device.SUPPORTED_DEVICES)
            if board == None:
                continue
            device = user_interface.createDeviceConfiguration(board, filters_list.data, amplifiers_list.data)
            if device == None:
                continue
            user_interface.saveDeviceConfiguration(device)

        # "Load device configuration" has been choosen
        elif (user_action == UserInterface.APPLICATION_ACTIONS[1]):
            device = user_interface.loadDeviceConfiguration()
            if device == None:
                continue

        device.initFilterRFSwitches(FilterSwitch.FILTER_INPUT_SWITCH_GPIO_PINS, 
                                    FilterSwitch.FILTER_OUTPUT_SWITCH_GPIO_PINS)

        # The LNA will only be initialized if the DEVICE_TYPE_MAPPING structure 
        # contains switch information to control the LNA
        device.initLNA(LNASwitch.LNA_INPUT_SWITCH_GPIO_PINS, 
                       LNASwitch.LNA_OUTPUT_SWITCH_GPIO_PINS)
        
        # Displaying text information about the active device configuration
        user_interface.displayInfo(device.getConfigurationInfo())
        # The main application menu, allowing you to select and enable a specific filter or toogle LNA state
        user_interface.chooseBoardAction(device)
    # End of while loop

if __name__ == "__main__":
    main()