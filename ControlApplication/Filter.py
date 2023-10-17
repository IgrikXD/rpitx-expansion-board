import os
import pandas

class Filter:
    def __init__(self, model_number, case_style, description, filter_type, passband_f1, passband_f2, stopband_f3, stopband_f4):
        self.model_number = model_number
        self.case_style = case_style
        self.description = description
        self.filter_type = filter_type
        self.passband_f1 = passband_f1
        self.passband_f2 = passband_f2
        self.stopband_f3 = stopband_f3
        self.stopband_f4 = stopband_f4

class FiltersList:
    def __init__(self, filter_models_dir):
        self.filters = self.getFiltersList(filter_models_dir)

    def getFiltersList(self, filter_models_dir):
        filters = []

        for filters_info_filename in os.listdir(filter_models_dir):
            if filters_info_filename.endswith('.csv'):
                filters_info_path = os.path.join(filter_models_dir, filters_info_filename)
                df = pandas.read_csv(filters_info_path)
                for _, row in df.iterrows():
                    filter_obj = Filter(
                        row['Model Number'],
                        row['Case Style'],
                        row['Description'],
                        row['Filter Type'],
                        row['Passband F1 (MHz)'],
                        row['Passband F2 (MHz)'],
                        row['Stopband F3 (MHz)'],
                        row['Stopband F4 (MHz)'])
                    filters.append(filter_obj)
        
        return filters
