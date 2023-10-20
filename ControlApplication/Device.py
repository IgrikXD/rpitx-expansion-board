import os
import pickle
from gpiozero.pins.mock import MockFactory
from gpiozero import OutputDevice

# Aliases for high and low logic levels
HIGH = True
LOW = False

class RFSwitch():

    RF_INPUT_SWITCH_PINOUT = [17, 27, 22]
    RF_OUTPUT_SWITCH_PINOUT = [0, 5, 6]

    SP3T_SWITCH_TRUTH_TABLE = {
            1: (LOW, LOW, LOW),     #RF common to RF1
            2: (LOW, LOW, HIGH),    #RF common to RF2
            3: (HIGH, LOW, LOW)     #RF common to RF3
    }

    SP4T_SWITCH_TRUTH_TABLE = {
            1: (LOW, LOW, LOW),     #RF common to RF1
            2: (LOW, LOW, HIGH),    #RF common to RF2
            3: (HIGH, LOW, LOW),    #RF common to RF3
            4: (HIGH, LOW, HIGH)    #RF common to RF4
    }

    SP6T_SWITCH_TRUTH_TABLE = {
            1: (LOW, LOW, LOW),     #RF common to RF1
            2: (LOW, LOW, HIGH),    #RF common to RF2
            3: (LOW, HIGH, LOW),    #RF common to RF3
            4: (LOW, HIGH, HIGH),   #RF common to RF4
            5: (HIGH, LOW, LOW),    #RF common to RF5
            6: (HIGH, LOW, HIGH),   #RF common to RF6
    }

    def __init__(self, switch_pinout, switch_truth_table):
        # Used BCM port numbering by default
        used_pin_factory = MockFactory()
        self.switch_pinout = switch_pinout
        self.switch_truth_table = switch_truth_table
        # used_pin_factory = None
        self.switch_control = [
            OutputDevice(pin=gpio_number, initial_value=HIGH, pin_factory=used_pin_factory)
            for gpio_number in self.switch_pinout
        ]

    def activateRFOutput(self, rf_output):
        try:
            for output_gpio_obj, gpio_state in zip(self.switch_control, self.switch_truth_table[rf_output]):
                output_gpio_obj.value = gpio_state
        except Exception:
            return False
        return True

class Device:
    # List of available device for operation
    DEVICES_LIST = [
        "rpitx-expansion-board-SP3T",
        "rpitx-expansion-board-SP4T",
        "rpitx-expansion-board-SP6T"
    ]
    
    # Matching a specific device with its configuration
    # <DEVICE> : (<NUMBER OF AVAILABLE FILTERS>, <RF SWITCH TRUTH TABLE>)
    DEVICE_TYPE_MAPPING = {
        DEVICES_LIST[0]: (3, RFSwitch.SP3T_SWITCH_TRUTH_TABLE),
        DEVICES_LIST[1]: (4, RFSwitch.SP4T_SWITCH_TRUTH_TABLE),
        DEVICES_LIST[2]: (6, RFSwitch.SP6T_SWITCH_TRUTH_TABLE)
    }

    def __init__(self, model_name):
        self.model_name = model_name
        self.filters = []
        self.filers_input_switch = None
        self.filers_output_switch = None
        self.filters_amount = self.DEVICE_TYPE_MAPPING[model_name][0]

    def initFilterRFSwitches(self, input_switch_pinout, output_switch_pinout, switch_truth_table):
        if (self.filers_input_switch == None and self.filers_output_switch == None):
            self.filers_input_switch = RFSwitch(input_switch_pinout, switch_truth_table)
            self.filers_output_switch = RFSwitch(output_switch_pinout, switch_truth_table)

    def enableFilter(self, filter_index):
        if (self.filers_input_switch != None and self.filers_input_switch != None):
            return (self.filers_input_switch.activateRFOutput(filter_index) and self.filers_output_switch.activateRFOutput(filter_index))
        return False
    
    def getConfigurationInfo(self):
        delimiter = "=" * 60
        configuration_info = f"{delimiter}\nActive board configuration:\n"
        configuration_info += f"{delimiter}\nChoosed board: {self.model_name}\n"
        configuration_info += f"{delimiter}\nChoosed filters:\n"
        configuration_info += delimiter
        for i, filter_obj in enumerate(self.filters, start=1):
            configuration_info += f"\nFilter {i}:\n"
            configuration_info += f"Model Number: {filter_obj.model_number}\n"
            configuration_info += f"Case Style: {filter_obj.case_style}\n"
            configuration_info += f"Description: {filter_obj.description}\n"
            configuration_info += f"Filter Type: {filter_obj.filter_type}\n"
            configuration_info += f"Passband F1: {filter_obj.passband_f1} MHz\n"
            configuration_info += f"Passband F2: {filter_obj.passband_f2} MHz\n"
            configuration_info += f"Stopband F3: {filter_obj.stopband_f3} MHz\n"
            configuration_info += f"Stopband F4: {filter_obj.stopband_f4} MHz\n"
            configuration_info += delimiter

        return configuration_info