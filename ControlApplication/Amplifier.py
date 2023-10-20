import os
import pandas
import pickle

class Amplifier:
    # Directory with .csv files containing models of all amplifiers available for use
    AMPLIFIER_MODELS_DIR = "./AmplifiersList"

    def __init__(self, model_number, case_style, description, f_low, f_high, gain):
        self.model_number = model_number
        self.case_style = case_style
        self.description = description
        self.f_low = f_low
        self.f_high = f_high
        self.gain = gain

class AmplifiersList:

    DUMP_FILENAME = "AmplifierDump.pkl"

    def __init__(self, amplifier_models_dir):
        dump_file_path = os.path.join(amplifier_models_dir, self.DUMP_FILENAME)
        # We save the state of the object after its first initialization, 
        # this saves time on re-reading .csv files. When we try to initialize 
        # the list of available amplifiers, we try to restore its state - 
        # if restoration fails, we form the list again
        if os.path.exists(dump_file_path):
            self.data = self.loadDump(dump_file_path)
        else:
            self.data = self.getAmplifiersList(amplifier_models_dir)
            self.saveSump(dump_file_path)

    def getAmplifiersList(self, amplifier_models_dir):
        amplifiers = []

        for amplifiers_info_filename in os.listdir(amplifier_models_dir):
            
            if amplifiers_info_filename.endswith('.csv'):
                amplifiers_info_path = os.path.join(amplifier_models_dir, amplifiers_info_filename)
                df = pandas.read_csv(amplifiers_info_path)
             
                for _, row in df.iterrows():
                    amplifier_obj = Amplifier(
                        row['Model Number'],
                        row['Case Style'],
                        row['Subcategories'],
                        row['F Low (MHz)'],
                        row['F High (MHz)'],
                        row['Gain (dB) Typ.'])
                    amplifiers.append(amplifier_obj)
        
        return amplifiers

    def loadDump(self, dump_file_path):
        
        with open(dump_file_path, 'rb') as amplifiers_list_dump_file:
            return pickle.load(amplifiers_list_dump_file)
        
    def saveSump(self, dump_fle_path):

        with open(dump_fle_path, 'wb') as amplifiers_list_dump_file:
                pickle.dump(self.data, amplifiers_list_dump_file)