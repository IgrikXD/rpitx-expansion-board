from abc import ABC, abstractmethod
import os
import pickle
from gpiozero.pins.mock import MockFactory
from gpiozero import DigitalOutputDevice, OutputDevice

class SwitchStrategy(ABC):
    @abstractmethod
    def enableFilter(self, filter_index):
        pass

class SPDTSwitchStrategy(SwitchStrategy):
    def enableFilter(self, filter_index):
        # TODO
        print(f"Enabling filter {filter_index} on SPDT switch")
        return True

class SP3TSwitchStrategy(SwitchStrategy):
    def enableFilter(self, filter_index):
        # TODO
        print(f"Enabling filter {filter_index} on SP3T switch")
        return True

class SP4TSwitchStrategy(SwitchStrategy):

    RF_INPUT_SWITCH_PINOUT = [17, 22, 27]
    RF_INPUT_SWITCH_OUTPUTS_GPIO_STATE_MAPPING = {
            1: (False, False, False), #RF common to RF1
            2: (False, False, True),  #RF common to RF2
            3: (True, False, False),  #RF common to RF3
            4: (True, False, True)    #RF common to RF4
    }
    
    def __init__(self):
        # Used BCM port numbering by default
        # used_pin_factory = MockFactory()
        used_pin_factory = None
        self.input_switch = [
            OutputDevice(pin=pin_number, initial_value=True, pin_factory=used_pin_factory)
            for pin_number in self.RF_INPUT_SWITCH_PINOUT
        ]
        for i, switch in enumerate(self.input_switch):
            print(f"Initial value PIN{self.RF_INPUT_SWITCH_PINOUT[i]}: {switch.value}")

    def enableFilter(self, filter_index):
        print(f"Enabling filter {filter_index} on SP4T switch")
        
        for switch in self.input_switch:
            switch.value = SP4TSwitchStrategy.RF_INPUT_SWITCH_OUTPUTS_GPIO_STATE_MAPPING[filter_index][self.input_switch.index(switch)]

        for i, switch in enumerate(self.input_switch):
            print(f"Actual value PIN{self.RF_INPUT_SWITCH_PINOUT[i]}: {switch.value}")

        return True

class SP6TSwitchStrategy(SwitchStrategy):
    def enableFilter(self, filter_index):
        # TODO
        print(f"Enabling filter {filter_index} on SP6T switch")
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
    # <DEVICE> : (<SWITCH TYPE>, <NUMBER OF AVAILABLE FILTERS>)
    DEVICE_TYPE_MAPPING = {
        DEVICES_LIST[0]: (SPDTSwitchStrategy(), 2),
        DEVICES_LIST[1]: (SP3TSwitchStrategy(), 3),
        DEVICES_LIST[2]: (SP4TSwitchStrategy(), 4),
        DEVICES_LIST[3]: (SP6TSwitchStrategy(), 6),
    }

    CONFIGURATION_INFO_DELIMITER = "=" * 60

    def __init__(self, model_name):
        self.model_name = model_name
        self.filters = []
        if model_name in Device.DEVICE_TYPE_MAPPING:
            self.switch_strategy, self.filters_amount = Device.DEVICE_TYPE_MAPPING[model_name]

    def enableFilter(self, filter_index):
        if self.switch_strategy:
            return self.switch_strategy.enableFilter(filter_index)
    
    def getConfigurationInfo(self):
        configuration_info = f"{Device.CONFIGURATION_INFO_DELIMITER}\nActive board configuration:\n"
        configuration_info += f"{Device.CONFIGURATION_INFO_DELIMITER}\nChoosed board: {self.model_name}\n"
        configuration_info += f"{Device.CONFIGURATION_INFO_DELIMITER}\nChoosed filters:\n"
        configuration_info += Device.CONFIGURATION_INFO_DELIMITER
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
            configuration_info += Device.CONFIGURATION_INFO_DELIMITER

        return configuration_info