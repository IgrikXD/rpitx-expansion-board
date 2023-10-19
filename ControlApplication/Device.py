from abc import ABC, abstractmethod
import os
import pickle
from gpiozero.pins.mock import MockFactory
from gpiozero import OutputDevice

# Aliases for high and low logic levels
HIGH = True
LOW = False

class RFSwitch(ABC):

    RF_INPUT_SWITCH_PINOUT = [17, 27, 22]
    RF_OUTPUT_SWITCH_PINOUT = [0, 5, 6]

    def __init__(self):
        # Used BCM port numbering by default
        used_pin_factory = MockFactory()
        # used_pin_factory = None
        self.input_switch = [
            OutputDevice(pin=gpio_number, initial_value=HIGH, pin_factory=used_pin_factory)
            for gpio_number in self.RF_INPUT_SWITCH_PINOUT
        ]
        self.output_switch = [
            OutputDevice(pin=gpio_number, initial_value=HIGH, pin_factory=used_pin_factory)
            for gpio_number in self.RF_OUTPUT_SWITCH_PINOUT
        ]

    @abstractmethod
    def enableFilter(self, filter_index):
        pass

    def changeControlSignals(self, gpio_values):
        for gpio_number, gpio_state in zip(self.input_switch, gpio_values):
            gpio_number.value = gpio_state
            print(gpio_state)

        for gpio_number, gpio_state in zip(self.output_switch, gpio_values):
            gpio_number.value = gpio_state

class SPDTSwitch(RFSwitch):

    RF_SWITCH_OUTPUTS_TO_GPIO = {
            1: (LOW, LOW, LOW),     #RF common to RF1
            2: (LOW, LOW, HIGH)     #RF common to RF2
    }

    def enableFilter(self, filter_index):
        print(f"Enabling filter {filter_index} on SPDT switch")

        try:
            self.changeControlSignals(self.RF_SWITCH_OUTPUTS_TO_GPIO[filter_index])
        except Exception:
            return False
        return True

class SP3TSwitch(RFSwitch):

    RF_SWITCH_OUTPUTS_TO_GPIO = {
            1: (LOW, LOW, LOW),     #RF common to RF1
            2: (LOW, LOW, HIGH),    #RF common to RF2
            3: (HIGH, LOW, LOW)     #RF common to RF3
    }

    def enableFilter(self, filter_index):
        print(f"Enabling filter {filter_index} on SP3T switch")

        try:
            self.changeControlSignals(self.RF_SWITCH_OUTPUTS_TO_GPIO[filter_index])
        except Exception:
            return False
        return True

class SP4TSwitch(RFSwitch):

    RF_SWITCH_OUTPUTS_TO_GPIO = {
            1: (LOW, LOW, LOW),     #RF common to RF1
            2: (LOW, LOW, HIGH),    #RF common to RF2
            3: (HIGH, LOW, LOW),    #RF common to RF3
            4: (HIGH, LOW, HIGH)    #RF common to RF4
    }

    def enableFilter(self, filter_index):
        print(f"Enabling filter {filter_index} on SP4T switch")
        
        try:
            self.changeControlSignals(self.RF_SWITCH_OUTPUTS_TO_GPIO[filter_index])
        except Exception:
            return False
        return True

class SP6TSwitch(RFSwitch):

    RF_SWITCH_OUTPUTS_TO_GPIO = {
            1: (LOW, LOW, LOW),     #RF common to RF1
            2: (LOW, LOW, HIGH),    #RF common to RF2
            3: (LOW, HIGH, LOW),    #RF common to RF3
            4: (LOW, HIGH, HIGH),   #RF common to RF4
            5: (HIGH, LOW, LOW),    #RF common to RF5
            6: (HIGH, LOW, HIGH),   #RF common to RF6
    }

    def enableFilter(self, filter_index):
        print(f"Enabling filter {filter_index} on SP6T switch")

        try:
            self.changeControlSignals(self.RF_SWITCH_OUTPUTS_TO_GPIO[filter_index])
        except Exception:
            return False
        return True

class Device:
    # List of available device for operation
    DEVICES_LIST = [
        "rpitx-expansion-board-SPDT", 
        "rpitx-expansion-board-SP3T", 
        "rpitx-expansion-board-SP4T", 
        "rpitx-expansion-board-SP6T"
    ]
    
    # Matching a specific device with its configuration
    # <DEVICE> : (<NUMBER OF AVAILABLE FILTERS>)
    DEVICE_TYPE_MAPPING = {
        DEVICES_LIST[0]: (2),
        DEVICES_LIST[1]: (3),
        DEVICES_LIST[2]: (4),
        DEVICES_LIST[3]: (6)
    }

    CONFIGURATION_INFO_DELIMITER = "=" * 60

    def __init__(self, model_name):
        self.model_name = model_name
        self.filters = []
        self.switch_strategy = None
        self.filters_amount = self.DEVICE_TYPE_MAPPING[model_name]

    def enableFilter(self, filter_index):
        # The operating strategy is selected when the enableFilter function 
        # is launched for the first time.
        if (self.switch_strategy == None):
            if (self.model_name == self.DEVICES_LIST[0]):
                self.switch_strategy = SPDTSwitch()
            elif (self.model_name == self.DEVICES_LIST[1]):
                self.switch_strategy = SP3TSwitch()
            elif (self.model_name == self.DEVICES_LIST[2]):
                self.switch_strategy = SP4TSwitch()
            elif (self.model_name == self.DEVICES_LIST[3]):
                self.switch_strategy = SP6TSwitch()
        
        return self.switch_strategy.enableFilter(filter_index)
    
    def getConfigurationInfo(self):
        configuration_info = f"{self.CONFIGURATION_INFO_DELIMITER}\nActive board configuration:\n"
        configuration_info += f"{self.CONFIGURATION_INFO_DELIMITER}\nChoosed board: {self.model_name}\n"
        configuration_info += f"{self.CONFIGURATION_INFO_DELIMITER}\nChoosed filters:\n"
        configuration_info += self.CONFIGURATION_INFO_DELIMITER
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
            configuration_info += self.CONFIGURATION_INFO_DELIMITER

        return configuration_info