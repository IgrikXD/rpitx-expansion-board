from concurrent.futures import ThreadPoolExecutor
from gpiozero.pins.mock import MockFactory
from gpiozero import OutputDevice
from gpiozero import BadPinFactory
from ControlApplication.Logger import *
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

    def __init__(self, switch_pinout, switch_truth_table, use_mock_gpio = False, log_filename = None):

        if log_filename:
            self.logger = Logger(log_filename)
        else:
            self.logger = None

        # Used BCM port numbering by default
        if use_mock_gpio:
            used_pin_factory = MockFactory()

            if self.logger:
                self.logger.logMessage("gpiozero used MockFactory for GPIO operation!", Logger.LogLevel.INFO)
        else:
            used_pin_factory = None
        
        self.switch_pinout = switch_pinout
        self.switch_truth_table = switch_truth_table
        self.active_rf_output = None

        try:
            self.switch_control = [
                OutputDevice(pin=gpio_number, initial_value=HIGH, pin_factory=used_pin_factory)
                for gpio_number in self.switch_pinout
            ]
            
            if self.logger:
                self.logger.logMessage(f"RFSwitch initialized on GPIO: {switch_pinout}", Logger.LogLevel.INFO)

        except BadPinFactory:
            self.switch_control = None

            if self.logger:
                self.logger.logMessage(f"RFSwitch not initialized on GPIO: {switch_pinout}", Logger.LogLevel.ERROR)
            
    def activateRFOutput(self, rf_output):
        if (self.switch_control and (self.active_rf_output != rf_output or self.active_rf_output == None)):
            try:
                self.active_rf_output = rf_output

                if self.logger:
                    self.logger.logMessage(f"RF path {rf_output} activated!", Logger.LogLevel.INFO, True)
                    self.logger.logMessage("START OF CNANGING GPIO STATE PROCESS", Logger.LogLevel.INFO)

                for output_gpio_obj, gpio_state in zip(self.switch_control, self.switch_truth_table[rf_output]):
                    output_gpio_obj.value = gpio_state
                    
                    if self.logger:
                        self.logger.logMessage(f"{output_gpio_obj.pin}: {gpio_state}")
                
            except Exception:
                if self.logger:
                    self.logger.logMessage(f"Unable to set state {gpio_state} for {output_gpio_obj.pin}!", 
                                           Logger.LogLevel.ERROR)
                    self.logger.logMessage("END OF CHANGING GPIO STATE PROCESS", Logger.LogLevel.INFO, True)
                
                return False
            
            if self.logger:
                self.logger.logMessage("END OF CHANGING GPIO STATE PROCESS", Logger.LogLevel.INFO, True)

            return True
        
        elif (not self.switch_control):
            if self.logger:
                self.logger.logMessage(f"RFSwitch not initialized! GPIO {self.switch_pinout} state not changed!", 
                                       Logger.LogLevel.ERROR)
            return False

        elif (self.active_rf_output == rf_output):
            if self.logger:
                self.logger.logMessage(f"Trying to activate already active RF path {rf_output}!", Logger.LogLevel.INFO)
            return True

class RFSwitchWrapper():
    def __init__(self, input_switch_pinout, output_switch_pinout, switch_truth_table, use_mock_gpio = False, log_filename = None):
        self.input_switch = RFSwitch(input_switch_pinout, switch_truth_table, use_mock_gpio, log_filename)
        self.output_switch = RFSwitch(output_switch_pinout, switch_truth_table, use_mock_gpio, log_filename)
        
        if log_filename:
            self.logger = Logger(log_filename)
        else:
            self.logger = None
    
    def activateRFPath(self, rf_path_index):
        # We activate two switches at the same time because we need to create a 
        # path for the signal to pass through a particular filter. This is 
        # achieved by sending the output signal to the input switch, passing 
        # it through a filter and then exiting through the output switch
        if self.logger:
            self.logger.logMessage("RFSwitchWrapper.activateRFPath() function called!", Logger.LogLevel.INFO)
            self.logger.logMessage("Changing the state of the GPIO ports for each of the "
                           "RFSwitch is performed in a separate thread!", Logger.LogLevel.INFO)
    
        with ThreadPoolExecutor(max_workers=2) as executor:
            input_switch_state_change_thread = executor.submit(self.input_switch.activateRFOutput, rf_path_index)
            output_switch_state_change_thread = executor.submit(self.output_switch.activateRFOutput, rf_path_index)

        return (input_switch_state_change_thread.result() and output_switch_state_change_thread.result())

class FilterSwitch(RFSwitchWrapper):

    def enableFilter(self, filter_index):
        return self.activateRFPath(filter_index) 
    
class LNASwitch(RFSwitchWrapper):

    def __init__(self, input_switch_pinout, output_switch_pinout, switch_truth_table, use_mock_gpio = False, log_filename = None):
        super().__init__(input_switch_pinout, output_switch_pinout, switch_truth_table, use_mock_gpio, log_filename)
        self.is_active = False

    def toggleLNA(self):
        # Toggle is_active value
        self.is_active = not self.is_active  
        activation_status = self.activateRFPath(2 if self.is_active else 1)
        
        if not activation_status:
            self.is_active = False
        
        return self.is_active