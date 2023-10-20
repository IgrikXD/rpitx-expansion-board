import os
import pickle

from RFSwitch import *

class Device:
    # List of available device for operation
    DEVICES_LIST = [
        "rpitx-expansion-board-SP3T",
        "rpitx-expansion-board-SP4T",
        "rpitx-expansion-board-SP6T"
    ]
    
    # Matching a specific device with its configuration
    # <DEVICE> : (<NUMBER OF AVAILABLE FILTERS>, <RF SWITCH TRUTH TABLE>, <IS LNA SUPPORTED>)
    DEVICE_TYPE_MAPPING = {
        DEVICES_LIST[0]: (3, RFSwitch.SP3T_SWITCH_TRUTH_TABLE, False),
        DEVICES_LIST[1]: (4, RFSwitch.SP4T_SWITCH_TRUTH_TABLE, False),
        DEVICES_LIST[2]: (6, RFSwitch.SP6T_SWITCH_TRUTH_TABLE, False)
    }

    def __init__(self, model_name):
        self.model_name = model_name
        self.filters = []
        self.filters_amount = self.DEVICE_TYPE_MAPPING[model_name][0]
        self.filers_input_switch = None
        self.filers_output_switch = None

    def initFilterRFSwitches(self, input_switch_pinout, output_switch_pinout, switch_truth_table):
        if (self.filers_input_switch == None and self.filers_output_switch == None):
            self.filers_input_switch = RFSwitch(input_switch_pinout, switch_truth_table)
            self.filers_output_switch = RFSwitch(output_switch_pinout, switch_truth_table)

    def enableFilter(self, filter_index):
        if (self.filers_input_switch != None and self.filers_input_switch != None):
            # We activate two switches at the same time because we need to create a 
            # path for the signal to pass through a particular filter. This is 
            # achieved by sending the output signal to the input switch, passing 
            # it through a filter and then exiting through the output switch
            return (self.filers_input_switch.activateRFOutput(filter_index) 
                    and self.filers_output_switch.activateRFOutput(filter_index))
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