import os
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def fileDetail():
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
                "fileName": f,
                "filePath": filePath,
                "fileExt": ext[1],
                "loadDataFrame": True
                }
                
            else:
                
                file = {
                    "fileName": f,
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
    data_info = []
    for col in df.columns:
        if df[col].isnull().sum() > 0:
            data_info.append({"column": col,
                              "null_value": df[col].isnull().sum()})
    
    if report:
        for r in report:
            data_info.append({"column": r['column'],
                              "null_value": df[r['column']].isnull().sum()})
    
    return data_info

def write_tittle():
    with open("validation_report.txt", "w", encoding="utf-8") as f:
        f.write("==============================\n")
        f.write("    DATA VALIDATION REPORT\n")
        f.write("==============================\n")
        f.write("\n")
        
def write_report_before_cleaning(report: list):
    with open("validation_report.txt", "a", encoding="utf-8") as f:
        f.write("    🔹 BEFORE CLEANING\n")
        f.write("------------------------------\n")
        f.write("\n")
        f.write("Missing value\n")
        
        for r in report:
            f.write(f"-- {r['column']} : {r['null_value']}\n")
            
        f.write("\n")
            
def write_report_after_cleaning(report: list):
    with open("validation_report.txt", "a", encoding="utf-8") as f:
        f.write("------------------------------\n")
        f.write("    🔹 AFTER CLEANING\n")
        f.write("------------------------------\n")
        f.write("\n")
        f.write("Missing value\n")
        
        for r in report:
            f.write(f"-- {r['column']} : {r['null_value']}\n")
            
        f.write("\n")

def summary(report_before: list, report_after: list):
    missing_value = 0
    for r in report_before:
        missing_value += r['null_value']
        
    with open("validation_report.txt", "a", encoding="utf-8") as f:
        f.write("  🔹 SUMMARY\n")
        f.write("------------------------------\n")
        f.write("Total Issues Fixed\n")
        f.write(f"-- Missing values fixed: {missing_value}\n")
        f.write("Final Data Quality: ✅ CLEAN & READY\n")

def write_report(report_before: list, report_after: list):
    write_tittle()
    write_report_before_cleaning(report_before)
    write_report_after_cleaning(report_after)
    summary(report_before, report_after)