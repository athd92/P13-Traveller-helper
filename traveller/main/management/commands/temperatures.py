import pandas as pd
import pycountry
import os


class TempClass:
    def __init__(self):
        self.res = {}

    def get_datas(self):
        print(os.getcwd())
        temperatures = pd.read_csv("media/temperatures.csv")
        for ind, row in temperatures.iterrows():
            self.res[row.get("ISO_3DIGIT")] = {
                "jan": row.get("Jan_Temp"),
                "feb": row.get("Feb_temp"),
                "mar": row.get("Mar_temp"),
                "apr": row.get("Apr_Temp"),
                "may": row.get("May_temp"),
                "jun": row.get("Jun_Temp"),
                "july": row.get("July_Temp"),
                "aug": row.get("Aug_Temp"),
                "sept": row.get("Sept_temp"),
                "oct": row.get("Oct_temp"),
                "nov": row.get("Nov_Temp"),
                "dec": row.get("Dec_temp"),
            }
        return self.res
