import os
import pickle

from RFSwitch import *

class Device:
    # List of available device for operation
    DEVICES_LIST = [
        "rpitx-expansion-board-SP3T",
        "rpitx-expansion-board-SP4T",
        "rpitx-expansion-board-SP6T",
        "rpitx-expansion-board-SP3T-LNA",
        "rpitx-expansion-board-SP4T-LNA",
        "rpitx-expansion-board-SP6T-LNA"
    ]
    
    # Matching a specific device with its configuration
    # <DEVICE> : (<NUMBER OF AVAILABLE FILTERS>, <FILTER SWITCH TRUTH TABLE>, <LNA SWITCH THRUTH TABLE>)
    DEVICE_TYPE_MAPPING = {
        # Boards without LNA
        DEVICES_LIST[0]: (3, RFSwitch.SP3T_SWITCH_TRUTH_TABLE, None),
        DEVICES_LIST[1]: (4, RFSwitch.SP4T_SWITCH_TRUTH_TABLE, None),
        DEVICES_LIST[2]: (6, RFSwitch.SP6T_SWITCH_TRUTH_TABLE, None),
        # Boards with LNA
        DEVICES_LIST[3]: (3, RFSwitch.SP3T_SWITCH_TRUTH_TABLE, RFSwitch.SPDT_SWITCH_TRUTH_TABLE),
        DEVICES_LIST[4]: (4, RFSwitch.SP4T_SWITCH_TRUTH_TABLE, RFSwitch.SPDT_SWITCH_TRUTH_TABLE),
        DEVICES_LIST[5]: (6, RFSwitch.SP6T_SWITCH_TRUTH_TABLE, RFSwitch.SPDT_SWITCH_TRUTH_TABLE)
    }

    def __init__(self, model_name):
        self.model_name = model_name
        self.filters = []
        self.filter_switch = None
        self.lna = []
        self.lna_switch = None

    def initFilterRFSwitches(self, input_switch_pinout, output_switch_pinout, switch_truth_table):
        if (self.filter_switch == None):
            self.filter_switch = FilterSwitch(input_switch_pinout, output_switch_pinout, switch_truth_table)

    def initLNA(self, input_switch_pinout, output_switch_pinout, switch_truth_table):
        if (switch_truth_table != None):
            if (self.lna_switch == None):
                self.lna_switch = LNASwitch(input_switch_pinout, output_switch_pinout, switch_truth_table)

    def enableFilter(self, filter_index):
        if (self.filter_switch != None):
            # We activate two switches at the same time because we need to create a 
            # path for the signal to pass through a particular filter. This is 
            # achieved by sending the output signal to the input switch, passing 
            # it through a filter and then exiting through the output switch
            return self.filter_switch.activateRFPath(filter_index) 
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

        if self.lna:
            configuration_info += f"\nAmplifier:\n"
            configuration_info += f"Model Number: {self.lna[0].model_number}\n"
            configuration_info += f"Case Style: {self.lna[0].case_style}\n"
            configuration_info += f"Description: {self.lna[0].description}\n"
            configuration_info += f"F Low: {self.lna[0].f_low}\n"
            configuration_info += f"F High: {self.lna[0].f_high} MHz\n"
            configuration_info += f"Gain Typ: {self.lna[0].gain} dB\n"
            configuration_info += delimiter
        return configuration_info