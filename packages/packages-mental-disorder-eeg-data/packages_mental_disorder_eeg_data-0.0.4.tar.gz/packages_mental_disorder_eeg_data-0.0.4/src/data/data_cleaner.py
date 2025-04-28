import pandas as pd

class DataCleaner:
    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe.copy()
        self.__remove_missing_columns()
    
    def __remove_missing_columns(self, threshold=0.5):
        limit = int(threshold * len(self.df))
        self.df = self.df.dropna(thresh=limit, axis=1)
        
    def find_most_null_column(self, threshold=0.5):
        null_ratios = self.df.isnull().mean()
        for col, ration in null_ratios.items():
            if ration > threshold:
                return col
        return None