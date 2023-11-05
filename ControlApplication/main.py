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
# Informational message about using GPIO port simulation
MOCK_GPIO_USED_INFO = (
    "Simulation of GPIO ports is used!\n\n"
    "The state of the real GPIO ports will not change! "
    "Disable this mode if you want to control the expansion board!"
) if IS_MOCK_GPIO_USED else None

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

def main():

    user_interface = UserInterface(LOG_FILENAME)

    # Displays an information message indicating that GPIO port simulation is being used
    if IS_MOCK_GPIO_USED:
        user_interface.displayInfo(MOCK_GPIO_USED_INFO)

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