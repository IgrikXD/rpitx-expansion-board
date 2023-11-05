from ControlApplication.RFSwitch import * 

class Device:
    # List of available device for operation
    SUPPORTED_DEVICES = [
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
        SUPPORTED_DEVICES[0]: (3, RFSwitch.SP3T_SWITCH_TRUTH_TABLE, None),
        SUPPORTED_DEVICES[1]: (4, RFSwitch.SP4T_SWITCH_TRUTH_TABLE, None),
        SUPPORTED_DEVICES[2]: (6, RFSwitch.SP6T_SWITCH_TRUTH_TABLE, None),
        # Boards with LNA
        SUPPORTED_DEVICES[3]: (3, RFSwitch.SP3T_SWITCH_TRUTH_TABLE, RFSwitch.SPDT_SWITCH_TRUTH_TABLE),
        SUPPORTED_DEVICES[4]: (4, RFSwitch.SP4T_SWITCH_TRUTH_TABLE, RFSwitch.SPDT_SWITCH_TRUTH_TABLE),
        SUPPORTED_DEVICES[5]: (6, RFSwitch.SP6T_SWITCH_TRUTH_TABLE, RFSwitch.SPDT_SWITCH_TRUTH_TABLE)
    }

    FILTERS_SWITCH_TRUTH_TABLE = 1
    LNA_SWITCH_TRUTH_TABLE = 2

    def __init__(self, model_name, log_filename = None):
        self.model_name = model_name
        self.filters = []
        self.filter_switch = None
        self.lna = []
        self.lna_switch = None
        self.log_filename = log_filename

    def initFilterRFSwitches(self, input_switch_pinout, output_switch_pinout, use_mock_gpio = False):
        if self.filter_switch is None:
            self.filter_switch = FilterSwitch(input_switch_pinout, output_switch_pinout, 
                                              Device.DEVICE_TYPE_MAPPING[self.model_name][self.FILTERS_SWITCH_TRUTH_TABLE], 
                                              use_mock_gpio, self.log_filename)

    def initLNA(self, input_switch_pinout, output_switch_pinout, use_mock_gpio = False):
        switch_truth_table = Device.DEVICE_TYPE_MAPPING[self.model_name][self.LNA_SWITCH_TRUTH_TABLE]
        if switch_truth_table and self.lna_switch is None:
            self.lna_switch = LNASwitch(input_switch_pinout, output_switch_pinout, 
                                        switch_truth_table, use_mock_gpio,
                                        self.log_filename)

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
            if filter_obj.model_number == None:
                filter_info = (
                    f"\nFilter {i}: Not installed!\n"
                )
            else:
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
                )
            configuration_info += f"{filter_info}{delimiter}"

        return configuration_info
