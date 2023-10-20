from gpiozero.pins.mock import MockFactory
from gpiozero import OutputDevice

# Aliases for high and low logic levels
HIGH = True
LOW = False

class RFSwitch():

    SPDT_SWITCH_TRUTH_TABLE = {
            1: (LOW, LOW),     #RF common to RF1
            2: (LOW, HIGH)     #RF common to RF2
    }

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
                print(f"{output_gpio_obj} {gpio_state}")
        except Exception:
            return False
        print("------------------------------------------")
        return True

class RFSwitchContainer(RFSwitch):
    def __init__(self, input_switch_pinout, output_switch_pinout, switch_truth_table):
        self.input_switch = RFSwitch(input_switch_pinout, switch_truth_table)
        self.output_switch = RFSwitch(output_switch_pinout, switch_truth_table)

    def activateRFPath(self, rf_path_index):
        return (self.input_switch.activateRFOutput(rf_path_index) and self.output_switch.activateRFOutput(rf_path_index))

class FilterSwitch(RFSwitchContainer):

    FILTER_INPUT_SWITCH_GPIO_PINS = [17, 27, 22]
    FILTER_OUTPUT_SWITCH_GPIO_PINS = [0, 5, 6]

    
class LNASwitch(RFSwitchContainer):

    LNA_INPUT_SWITCH_GPIO_PINS = [23, 24]
    LNA_OUTPUT_SWITCH_GPIO_PINS = [16, 26]

    def __init__(self, input_switch_pinout, output_switch_pinout, switch_truth_table):
        super().__init__(input_switch_pinout, output_switch_pinout, switch_truth_table)
        self.is_active = False

    def toogleLNA(self):
        # Toogle is_active value
        self.is_active = not self.is_active  
        if self.is_active:
            activation_status = self.activateRFPath(2)
        else:
            activation_status = self.activateRFPath(1)

        if activation_status == False:
            self.is_active = False

        return self.is_active