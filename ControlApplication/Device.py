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
    
    def getConfigurationInfo(self):
        delimiter = "=" * 60
        configuration_info = f"{delimiter}\nActive board configuration:\n"
        configuration_info += f"{delimiter}\nChoosed board: {self.model_name}\n"

        if self.lna:
            lna_info = self.lna[0]
            amplifier_info = (
                f"{delimiter}\nAmplifier:\n"
                f"Model Number: {lna_info.model_number}\n"
                f"Case Style: {lna_info.case_style}\n"
                f"Description: {lna_info.description}\n"
                f"F Low: {lna_info.f_low}\n"
                f"F High: {lna_info.f_high} MHz\n"
                f"Gain Typ: {lna_info.gain} dB\n"
            )
            configuration_info += amplifier_info

        configuration_info += f"{delimiter}\nChoosed filters:\n"
        configuration_info += delimiter

        for i, filter_obj in enumerate(self.filters, start=1):
            filter_info = (
                f"\nFilter {i}:\n"
                f"Model Number: {filter_obj.model_number}\n"
                f"Case Style: {filter_obj.case_style}\n"
                f"Description: {filter_obj.description}\n"
                f"Filter Type: {filter_obj.filter_type}\n"
                f"Passband F1: {filter_obj.passband_f1} MHz\n"
                f"Passband F2: {filter_obj.passband_f2} MHz\n"
                f"Stopband F3: {filter_obj.stopband_f3} MHz\n"
                f"Stopband F4: {filter_obj.stopband_f4} MHz\n"
                f"{delimiter}"
            )
            configuration_info += filter_info

        return configuration_info
