from gpiozero.pins.mock import MockFactory
from gpiozero import OutputDevice
import sys

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

    def __init__(self, switch_pinout, switch_truth_table, log_filename = None):
        self.log_filename = log_filename
        # Used BCM port numbering by default
        if "--use-mock-gpio" in sys.argv:
            used_pin_factory = MockFactory()
            if ("--show-debug-info" in sys.argv) and (self.log_filename != None):
                with open(self.log_filename, "a") as file:
                    file.write(f"[INFO]: gpiozero used MockFactory for GPIO operation!\n")
        else:
            used_pin_factory = None
        
        self.switch_pinout = switch_pinout
        self.switch_truth_table = switch_truth_table
        self.switch_control = [
            OutputDevice(pin=gpio_number, initial_value=HIGH, pin_factory=used_pin_factory)
            for gpio_number in self.switch_pinout
        ]
        self.active_rf_output = None

        if ("--show-debug-info" in sys.argv) and (self.log_filename != None):
            with open(self.log_filename, "a") as file:
                file.write(f"[INFO]: RFSwitch initialized on GPIO: {switch_pinout}\n")

    def activateRFOutput(self, rf_output):
        if (self.active_rf_output != rf_output or self.active_rf_output == None):
            try:
                self.active_rf_output = rf_output

                if ("--show-debug-info" in sys.argv) and (self.log_filename != None):
                    with open(self.log_filename, "a") as file:
                        file.write(f"-------------------------------------------------\n")
                        file.write(f"[INFO]: RF path {rf_output} activated!\n")
                        file.write(f"-------------------------------------------------\n")
                        file.write(f"[INFO]: START OF CNANGING GPIO STATE\n")
                
                for output_gpio_obj, gpio_state in zip(self.switch_control, self.switch_truth_table[rf_output]):
                    output_gpio_obj.value = gpio_state
                    
                    if ("--show-debug-info" in sys.argv) and (self.log_filename != None):
                        with open(self.log_filename, "a") as file:
                            if gpio_state:
                                file.write(f"{output_gpio_obj.pin}: {gpio_state}\n")
                            else:
                                file.write(f"{output_gpio_obj.pin}: {gpio_state}\n")
            
            except Exception:
                if ("--show-debug-info" in sys.argv) and (self.log_filename != None):
                    with open(self.log_filename, "a") as file:
                        file.write(f"[ERROR]: Unable to set state {gpio_state} for {output_gpio_obj.pin}!")
                        file.write(f"[INFO]: END OF CHANGING GPIO STATE\n")
                        file.write(f"-------------------------------------------------\n\n")
                
                return False
            
            if ("--show-debug-info" in sys.argv) and (self.log_filename != None):
                with open(self.log_filename, "a") as file:
                    file.write(f"[INFO]: END OF CHANGING GPIO STATE\n")
                    file.write(f"-------------------------------------------------\n\n")
            
            return True
        
        if ("--show-debug-info" in sys.argv) and (self.log_filename != None):
            with open(self.log_filename, "a") as file:
                file.write(f"[INFO]: Trying to activate already active RF path {rf_output}!\n")

        return True

class RFSwitchWrapper(RFSwitch):
    def __init__(self, input_switch_pinout, output_switch_pinout, switch_truth_table, log_filename = None):
        self.input_switch = RFSwitch(input_switch_pinout, switch_truth_table, log_filename)
        self.output_switch = RFSwitch(output_switch_pinout, switch_truth_table, log_filename)

    def activateRFPath(self, rf_path_index):
        # We activate two switches at the same time because we need to create a 
        # path for the signal to pass through a particular filter. This is 
        # achieved by sending the output signal to the input switch, passing 
        # it through a filter and then exiting through the output switch
        return (self.input_switch.activateRFOutput(rf_path_index) and self.output_switch.activateRFOutput(rf_path_index))

class FilterSwitch(RFSwitchWrapper):

    FILTER_INPUT_SWITCH_GPIO_PINS = [17, 27, 22]
    FILTER_OUTPUT_SWITCH_GPIO_PINS = [0, 5, 6]

    def enableFilter(self, filter_index):
            return self.activateRFPath(filter_index) 
    
class LNASwitch(RFSwitchWrapper):

    LNA_INPUT_SWITCH_GPIO_PINS = [23, 24]
    LNA_OUTPUT_SWITCH_GPIO_PINS = [16, 26]

    def __init__(self, input_switch_pinout, output_switch_pinout, switch_truth_table, log_filename):
        super().__init__(input_switch_pinout, output_switch_pinout, switch_truth_table, log_filename)
        self.is_active = False

    def toggleLNA(self):
        # Toggle is_active value
        self.is_active = not self.is_active  
        activation_status = self.activateRFPath(2 if self.is_active else 1)
        
        if not activation_status:
            self.is_active = False
        
        return self.is_active