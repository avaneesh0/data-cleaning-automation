import os
import pandas as pd
import numpy as np
import logging
logger = logging.getLogger(__name__)

def loadCsv(path) -> pd.DataFrame:
    df = pd.read_csv(path)
    logging.info(f"Reading file at [{path}]")
    return df

def loadExcell(path) -> pd.DataFrame:
    df = pd.read_excel(path , engine="openpyxl")
    logging.info(f"Reading file at [{path}]")
    return df

def loadDataFrame(file) -> pd.DataFrame:
    if file["fileExt"] == ".csv":
        data = loadCsv(os.path.join("./", file["filePath"]))
        return data
    else: 
        supportedExt = [".xlsx", ".xlsm", ".xltx", ".xltm"]
        for ext in supportedExt:
            if file["fileExt"] == ext:
                data = loadExcell(os.path.join("./", file["filePath"]))
                return data  
        
def saveOutput(data: pd.DataFrame, file: dict):
    if file["fileExt"] == ".csv":
        data.to_csv(f"data/processed/{file['fileName']}", index=False)
        logging.info(f"Saving cleaned file at [data/processed/{file['fileName']}]")
    else:
        extention = [".xlsx", ".xlsm", ".xltx", ".xltm"]
        for ext in extention:
            if file["fileExt"] == ext:
                data.to_excel(f"data/processed/{file['fileName']}", index=False)
                logging.info(f"Saving cleaned file at [data/processed/{file['fileName']}]")
                
def removeDublicate(data: pd.DataFrame) -> pd.DataFrame:
    data = data.drop_duplicates()
    logging.info("Dublicates removed")
    return data

def cleanData(data: pd.DataFrame) -> pd.DataFrame:

    date_col = detect_datetime_columns(data)
    for col in date_col:
        data[col] = pd.to_datetime(data[col])
        
    for col in data.columns:
        
        if data[col].dtype == object: 
            data[col].str.strip()
            data[col].str.lower()
            
        total_Null = data[col].isnull().sum()
        if total_Null > 0:
            if data[col].dtype == object:
                data[col] = data[col].fillna("Missing")
                logging.info(f"Fill {total_Null} null value in {col} with Missing")
                
            if np.issubdtype(data[col].dtype, np.number ):
                data[col] = data[col].fillna(np.mean(data[col]))
                logging.info(f"Filled {total_Null} null value in {col} with mean")
            
    
    logging.info("Data cleaned")
    return data

def detect_datetime_columns(df: pd.DataFrame, threshold=0.8) -> list:
    datetime_cols = []
    
    for col in df.select_dtypes(include=["object"]).columns:
        converted = pd.to_datetime(df[col], errors='coerce', format="mixed", dayfirst=True)
        
        success_rate = converted.notna().sum() / len(df)
        
        if success_rate >= threshold:
            datetime_cols.append(col)
            
    return datetime_cols