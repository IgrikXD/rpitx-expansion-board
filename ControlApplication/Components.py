import os
import pandas
import pickle

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

    def __init__(self, model_type, models_dir, dump_filename):
        self.model_type = model_type
        self.dump_file_path = os.path.join(models_dir, dump_filename)
        
        if os.path.exists(self.dump_file_path):
            self.data = self.loadDump(self.dump_file_path)
        else:
            self.data = self.getModelsList(models_dir)
            self.saveDump(self.dump_file_path)

    def getModelsList(self, models_dir):
        models = []

        for model_info_filename in os.listdir(models_dir):
            
            if model_info_filename.endswith('.csv'):
                model_info_path = os.path.join(models_dir, model_info_filename)
                df = pandas.read_csv(model_info_path)

                for _, row in df.iterrows():
                    if self.model_type == self.FILTER:
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
                    elif self.model_type == self.AMPLIFIER:
                        model = Amplifier(
                            row['Model Number'],
                            row['Case Style'],
                            row['Subcategories'],
                            row['F Low (MHz)'],
                            row['F High (MHz)'],
                            row['Gain (dB) Typ.']
                        )
                    models.append(model)

        return models

    def loadDump(self, dump_file_path):
        with open(dump_file_path, 'rb') as model_list_dump_file:
            return pickle.load(model_list_dump_file)

    def saveDump(self, dump_file_path):
        with open(dump_file_path, 'wb') as model_list_dump_file:
            pickle.dump(self.data, model_list_dump_file)
