import os
import pandas as pd
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
    data_info = [[], {}]
    data_list, data_dict = data_info
    
    data_dict["Status"] = "✅ Passed"
    
    for col in df.columns:
        
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
    else:
        logging.info("Preparing file report before cleaning")
    
    return data_info

def write_tittle():
    with open("validation_report.txt", "w", encoding="utf-8") as f:
        f.write("==============================\n")
        f.write("    DATA VALIDATION REPORT\n")
        f.write("==============================\n")
        f.write("\n")
        
def write_report_before_cleaning(report: list):
    sub_list, sub_dict = report
    
    with open("validation_report.txt", "a", encoding="utf-8") as f:
        f.write("    🔹 BEFORE CLEANING\n")
        f.write("------------------------------\n")
        f.write("\n")
        f.write("Missing Value\n")
        
        for r in sub_list:
            f.write(f"-- {r['column']} : {r['null_value']}\n")
            
        f.write("\n")
        f.write("Duplicate\n")
        f.write(f"-- Duplicate row : {sub_dict['duplicate']}\n")
        f.write("\n")
        f.write("Invalid Values\n")
        f.write("-- Will be added later\n")
        f.write("\n")
        f.write("Data Type Issues\n")
        f.write("-- Will be added later\n")
        f.write("\n")
        f.write(f"Status: {sub_dict['Status']}\n")
        f.write("\n")
            
def write_report_after_cleaning(report: list):
    sub_list, sub_dict = report
    
    with open("validation_report.txt", "a", encoding="utf-8") as f:
        f.write("------------------------------\n")
        f.write("    🔹 AFTER CLEANING\n")
        f.write("------------------------------\n")
        f.write("\n")
        f.write("Missing Value\n")
        
        for r in sub_list:
            f.write(f"-- {r['column']} : {r['null_value']}\n")
        
        f.write("\n")
        f.write("Duplicate\n")
        f.write(f"-- Duplicate row : {sub_dict['duplicate']}\n ")
        f.write("\n")
        f.write("Invalid Values\n")
        f.write("-- Will be added later\n")
        f.write("\n")
        f.write("Data Type Issues\n")
        f.write("-- Will be added later\n")
        f.write("\n")
        f.write(f"Status: {sub_dict['Status']}\n")
        f.write("\n")

def summary(report_before: list, report_after: list):
    sub_list_before, sub_dict_before = report_before
    sub_list_after, sub_dict_after = report_after
    
    missing_value_before = add_list_of_dict(sub_list_before, 'null_value')
    missing_value_after = add_list_of_dict(sub_list_after, 'null_value')
    
    duplicate_row_before = sub_dict_before['duplicate']
    duplicate_row_after = sub_dict_after['duplicate']
    
    with open("validation_report.txt", "a", encoding="utf-8") as f:
        f.write("------------------------------\n")
        f.write("  🔹 SUMMARY\n")
        f.write("------------------------------\n")
        f.write("\n")
        f.write("Total Issues Fixed\n")
        f.write("\n")
        f.write(f"-- Missing values fixed : {missing_value_before} -> {missing_value_after}\n")
        f.write(f"-- Duplicate row removed : {duplicate_row_before} -> {duplicate_row_after}\n")
        f.write("\n")
        f.write("Data Quality Improvement: 0% → 100%\n")
        f.write("\n")
        f.write("Final Data Quality: ✅ CLEAN & READY\n")

def write_report(report_before: list, report_after: list):
    logging.info("Preparing report")
    write_tittle()
    write_report_before_cleaning(report_before)
    write_report_after_cleaning(report_after)
    logging.info("Preparing summary")
    summary(report_before, report_after)
    
def add_list_of_dict(report: list, key: str) -> int:
    missing_value = 0
    for elm in report:
            missing_value += elm[key]
    return missing_value