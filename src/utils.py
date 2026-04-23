import os
import pandas as pd
from src.cleaning import detect_datetime_columns
import logging

logger = logging.getLogger(__name__)

def fileDetail() -> list:
    directory = "data/raw/"
    logging.info(f"Checking file in {directory}")
    files = [f for f in os.listdir(directory) if f != ".gitkeep"]
    
    if len(files) == 0:
        logging.info("Add file to clean data")
        
    if files:
        fileInfo = []
        for f in files:
            
            ext = os.path.splitext(f)
            filePath = directory + f
            
            if ext[1] in [".csv",".xlsx", ".xlsm", ".xltx", ".xltm"]:
                
                file = {
                "fileName": ext[0],
                "filePath": filePath,
                "fileExt": ext[1],
                "loadDataFrame": True
                }
                
            else:
                
                file = {
                    "fileName": ext[0],
                    "filePath": filePath,
                    "fileExt": ext[1],
                    "loadDataFrame": False
                }
                
            fileInfo.append(file)
            
        logging.info("File info obtained")
        return fileInfo
    else:
        raise FileNotFoundError("No file")


def dataframe_report(df: pd.DataFrame , report = []) -> dict :
    data_info = [[], {}]
    data_list, data_dict = data_info
    
    data_dict["Status"] = "✅ Passed"
    
    date_col = detect_datetime_columns(df)
    for d_col in date_col:
            print("was there")
            data_dict["data_type_changed"] = {"column": d_col,
                                              "dtype": df[d_col].dtype
                                              }
            data_dict["Status"] = "❌ Failed"
            
    for col in df.columns:
        
        if df.duplicated().sum():
            data_dict["duplicate"] = df.duplicated().sum()
            data_dict["Status"] = "❌ Failed"
        else:
            data_dict["duplicate"] = df.duplicated().sum()
        
        if df[col].isnull().sum() > 0:
            data_list.append({"column": col,
                              "null_value": df[col].isnull().sum()})
            
            data_dict["Status"] = "❌ Failed"
    
    if report:
        logging.info("Preparing file report after cleaning")
        for r in report[0]:
            data_list.append({"column": r['column'],
                              "null_value": df[r['column']].isnull().sum()})
            
        dt_changed_col = report[1]["data_type_changed"]["column"]
        
        data_dict["data_type_changed"] = {"column": dt_changed_col,
                                        "dtype": df[dt_changed_col].dtype
                                        }
        
    else:
        logging.info("Preparing file report before cleaning")
    
    return data_info
