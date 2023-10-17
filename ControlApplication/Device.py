from abc import ABC, abstractmethod
import os
import pickle

CONFIGS_DIR = "./SavedConfiguration/"

class SwitchStrategy(ABC):
    @abstractmethod
    def enableFilter(self, filter_index):
        pass

class SPDTSwitchStrategy(SwitchStrategy):
    def enableFilter(self, filter_index):
        # TODO
        print(f"Enabling filter {filter_index} on SPDT switch")

class SP3TSwitchStrategy(SwitchStrategy):
    def enableFilter(self, filter_index):
        # TODO
        print(f"Enabling filter {filter_index} on SP3T switch")

class SP4TSwitchStrategy(SwitchStrategy):
    def enableFilter(self, filter_index):
        # TODO
        print(f"Enabling filter {filter_index} on SP4T switch")

class SP6TSwitchStrategy(SwitchStrategy):
    def enableFilter(self, filter_index):
        # TODO
        print(f"Enabling filter {filter_index} on SP6T switch")

class Device:
    def __init__(self, switch_type, model_name):
        self.switch_type = switch_type
        self.model_name = model_name
        self.filters = []
        if (switch_type == "SPDT"):
            self.switch_strategy = SPDTSwitchStrategy()
        elif (switch_type == "SP3T"):
            self.switch_strategy = SP3TSwitchStrategy()
        elif (switch_type == "SP4T"):
            self.switch_strategy = SP4TSwitchStrategy()
        elif (switch_type == "SP6T"):
            self.switch_strategy = SP6TSwitchStrategy()

    def setSwitchStrategy(self, switch_strategy):
        self.switch_strategy = switch_strategy

    def enableFilter(self, filter_index):
        if self.switch_strategy:
            self.switch_strategy.enableFilter(filter_index)
        else:
            print("Switch strategy not set!")

    def saveConfiguration(self):
        os.makedirs(CONFIGS_DIR, exist_ok=True)

        with open(f"{CONFIGS_DIR}{self.model_name}.pkl", 'wb') as device_configuration_file:
            pickle.dump(self, device_configuration_file)

        return f"{CONFIGS_DIR}{self.model_name}.pkl"
    
    def getConfigurationInfo(self):
        configuration_info = "=" * 60
        configuration_info += "\nActive board configuration:\n"
        configuration_info += "=" * 60
        configuration_info += f"\nChoosed board: {self.model_name}\n"
        configuration_info += "=" * 60
        configuration_info += f"\nChoosed filters:\n"
        configuration_info += "=" * 60
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
            configuration_info += "=" * 60

        return configuration_info