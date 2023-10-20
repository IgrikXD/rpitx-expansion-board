from RFSwitch import *

class LNA:

    LNA_INPUT_SWITCH_GPIO_PINS = [23, 24]
    LNA_OUTPUT_SWITCH_GPIO_PINS = [16, 26]

    def __init__(self, model_number, description):
        self.input_switch = None
        self.output_switch = None
        self.lna = None
        self.is_active = False
        self.model_number = model_number
        self.description = description
