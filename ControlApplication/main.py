from concurrent.futures import ThreadPoolExecutor
from ControlApplication.Device import *
from ControlApplication.UserInterface import *
from ControlApplication.Components import *

# Output debugging information to a file
SHOW_DEBUG_INFO = True
# Log file save location
LOG_FILENAME = f"{APPLICATION_DIR}/DebugInfo.log" if SHOW_DEBUG_INFO else None

# Using MockFactory to simulate real GPIO ports.This allows the 
# application to run on devices other than RaspberryPi without 
# causing a GPIO initialization error. Used for debugging and 
# testing GPIO port states.
IS_MOCK_GPIO_USED = True

# Information related to the configuration of RF filter switches
FILTER_MODELS_DIR = f"{APPLICATION_DIR}/FiltersList"
FILTER_DUMP_FILE = "FiltersListDump.pkl"
FILTER_INPUT_SWITCH_GPIO_PINS = [17, 27, 22]
FILTER_OUTPUT_SWITCH_GPIO_PINS = [0, 5, 6]

# Information related to the configuration of LNA switches
AMPLIFIER_MODELS_DIR = f"{APPLICATION_DIR}/AmplifiersList"
AMPLIFIER_DUMP_FILE = "AmplifierDump.pkl"
LNA_INPUT_SWITCH_GPIO_PINS = [23, 24]
LNA_OUTPUT_SWITCH_GPIO_PINS = [16, 26]

# List of actions available to perform for a specific device
APPLICATION_ACTIONS = ["Create a new device configuration", "Load device configuration"]

# -----------------------------------------------------------
# Changelog:
# -----------------------------------------------------------
# Version 0.4: 
# -----------------------------------------------------------
# 
# -----------------------------------------------------------
# Version 0.3: 
# -----------------------------------------------------------
# The FiltersList and AmplifiersList directories have been 
# moved to the ControlApplication directory. Now, dumps of 
# components and configurations of expansion boards are saved 
# taking into account the parent directory in which the 
# application source files are located.
# 
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
# 
# Checking for the presence of .csv files of component models
# When the program starts, it checks whether .csv files exist in 
# the FiltersList and AmplifiersList directories. These files are
# used to build a list of available components when creating a 
# device configuration. If it is not possible to load the 
# previously created .pkl dump of the list of components and the 
# necessary .csv files to build the list of components are 
# missing, an error message is displayed in the console and the 
# program ends.
# 
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
# 
# The ComponentsList constructors are now called in separate 
# threads, which allows reading data about filters and 
# amplifiers in parallel rather than sequentially.
# When creating a ComponentsList object, each of the .csv files 
# is now processed in a separate thread.
# 
# Added highlighting of application start and stop timestamp 
# using '-' signs.
# 
# whiptail_interface.msgbox() is now called with an additional 
# --scrolltext parameter
# -----------------------------------------------------------

def main():

    user_interface = UserInterface(LOG_FILENAME)

    # Initializing available filter and amplifier models
    with ThreadPoolExecutor(max_workers=2) as executor:
        filters_future = executor.submit(ComponentsList, ComponentsList.FILTER, FILTER_MODELS_DIR, FILTER_DUMP_FILE, LOG_FILENAME)
        amplifiers_future = executor.submit(ComponentsList, ComponentsList.AMPLIFIER, AMPLIFIER_MODELS_DIR, AMPLIFIER_DUMP_FILE, LOG_FILENAME)

        filters_list = filters_future.result()
        amplifiers_list = amplifiers_future.result()

    while True:
        user_action = user_interface.chooseItem("Choose an action:", APPLICATION_ACTIONS, 
                                                exit_if_cancel_pressed = True)

        # "Create a new device configuration" has been choosen
        if (user_action == APPLICATION_ACTIONS[0]):
            board = user_interface.chooseItem("Choose your board:", Device.SUPPORTED_DEVICES)
            # <Cancel> button has been pressed
            if board is None:
                continue
            device = user_interface.createDeviceConfiguration(board, filters_list.data, amplifiers_list.data)
            if device is None:
                continue
            user_interface.saveDeviceConfiguration(device)

        # "Load device configuration" has been choosen
        elif (user_action == APPLICATION_ACTIONS[1]):
            device = user_interface.loadDeviceConfiguration()
            # <Cancel> button has been pressed or configuration files are missing
            if device is None:
                continue
        
        # RF switches are initialized for all types of expansion boards
        device.initFilterRFSwitches(FILTER_INPUT_SWITCH_GPIO_PINS, FILTER_OUTPUT_SWITCH_GPIO_PINS, IS_MOCK_GPIO_USED)

        # The LNA will only be initialized if the currently selected expansion board supports it
        device.initLNA(LNA_INPUT_SWITCH_GPIO_PINS, LNA_OUTPUT_SWITCH_GPIO_PINS, IS_MOCK_GPIO_USED)
        
        # Displaying text information about the active device configuration
        user_interface.displayInfo(device.getConfigurationInfo())
        # The main application menu, allowing you to select and enable a specific filter or toogle LNA state
        user_interface.chooseBoardAction(device)

if __name__ == "__main__":
    main()