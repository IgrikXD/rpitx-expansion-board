import os
import pandas
import pickle
import sys
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor
from ControlApplication.Logger import *

class BaseModel:
    def __init__(self, model_number, case_style, description):
        self.model_number = model_number
        self.case_style = case_style
        self.description = description

class Filter(BaseModel):
    def __init__(self, model_number, case_style, description, filter_type, passband_f1, passband_f2, stopband_f3, stopband_f4):
        super().__init__(model_number, case_style, description)
        self.filter_type = filter_type
        self.passband_f1 = passband_f1
        self.passband_f2 = passband_f2
        self.stopband_f3 = stopband_f3
        self.stopband_f4 = stopband_f4

class Amplifier(BaseModel):
    def __init__(self, model_number, case_style, description, f_low, f_high, gain):
        super().__init__(model_number, case_style, description)
        self.f_low = f_low
        self.f_high = f_high
        self.gain = gain

class ComponentsList:

    FILTER = "Filter"
    AMPLIFIER = "Amplifier"

    def __init__(self, model_type, models_dir, dump_filename, log_filename = None):
        self.model_type = model_type
        if ("--show-debug-info" in sys.argv) and log_filename:
            self.logger = Logger(log_filename)
        else:
            self.logger = None
        
        dump_file_path = os.path.join(models_dir, dump_filename)
        
        if os.path.exists(dump_file_path):
            self.data = self.__loadDump(dump_file_path)
        else:
            self.data = self.__getModelsList(models_dir)
            if self.data is not None:
                self.__saveDump(dump_file_path)
            else:
                init_error_info = (
                    f"{Fore.RED}{model_type} components initialization error!{Style.RESET_ALL}\n"
                    f"Make sure that the {Fore.YELLOW}{models_dir}{Style.RESET_ALL} directory contains .csv files describing the available components!" 
                )
                print(init_error_info)
                exit(1)

    def __getModelsList(self, models_dir):
        models = []

        file_list = [filename for filename in os.listdir(models_dir) if filename.endswith('.csv')]

        if not file_list:
            if self.logger:
                self.logger.logMessage(f"{self.model_type} model .csv files are missing!", Logger.LogLevel.ERROR)
            return None 

        with ThreadPoolExecutor() as executor:
            for model_list in executor.map(self.__processCsvFile, [os.path.join(models_dir, filename) for filename in file_list]):
                models.extend(model_list)

        return models

    def __loadDump(self, dump_file_path):
        with open(dump_file_path, 'rb') as model_list_dump_file:
            if self.logger:
                self.logger.logMessage(f"Dump loaded: {dump_file_path}", Logger.LogLevel.INFO)
            return pickle.load(model_list_dump_file)

    def __processCsvFile(self, csv_file_path):
        models_list = []

        df = pandas.read_csv(csv_file_path)
        for _, row in df.iterrows():
            if (self.model_type == self.FILTER):
                model = Filter(
                    row['Model Number'],
                    row['Case Style'],
                    row['Description'],
                    row['Filter Type'],
                    row['Passband F1 (MHz)'],
                    row['Passband F2 (MHz)'],
                    row['Stopband F3 (MHz)'],
                    row['Stopband F4 (MHz)']
                )
            elif (self.model_type == self.AMPLIFIER):
                model = Amplifier(
                    row['Model Number'],
                    row['Case Style'],
                    row['Subcategories'],
                    row['F Low (MHz)'],
                    row['F High (MHz)'],
                    row['Gain (dB) Typ.']
                )

            models_list.append(model)
        
        return models_list

    def __saveDump(self, dump_file_path):
        with open(dump_file_path, 'wb') as model_list_dump_file:
            pickle.dump(self.data, model_list_dump_file)
            if self.logger:
                self.logger.logMessage(f"Dump saved: {dump_file_path}", Logger.LogLevel.INFO)
