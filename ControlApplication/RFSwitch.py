from gpiozero.pins.mock import MockFactory
from gpiozero import OutputDevice

# Aliases for high and low logic levels
HIGH = True
LOW = False

class RFSwitch():

    RF_INPUT_SWITCH_GPIO_PINS = [17, 27, 22]
    RF_OUTPUT_SWITCH_GPIO_PINS = [0, 5, 6]

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
