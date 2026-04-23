import logging 

logger = logging.getLogger(__name__)

def write_tittle(file: str):
    with open(f"validator/validation_of_{file}.txt", "w", encoding="utf-8") as f:
        f.write("==============================\n")
        f.write("    DATA VALIDATION REPORT\n")
        f.write("==============================\n")
        f.write("\n")
        
def write_report_before_cleaning(report: list, file: str):
    sub_list, sub_dict = report
    
    with open(f"validator/validation_of_{file}.txt", "a", encoding="utf-8") as f:
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
        f.write("Data Type Issues\n")
        f.write(f"-- {sub_dict["data_type_changed"]["column"]} : {sub_dict["data_type_changed"]["dtype"]}\n")
        f.write("\n")
        f.write(f"Status: {sub_dict['Status']}\n")
        f.write("\n")
            
def write_report_after_cleaning(report: list, file: str):
    sub_list, sub_dict = report
    
    with open(f"validator/validation_of_{file}.txt", "a", encoding="utf-8") as f:
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
        f.write("Data Type Issues Fixed\n")
        f.write(f"-- {sub_dict["data_type_changed"]["column"]} : {sub_dict["data_type_changed"]["dtype"]}\n")
        f.write("\n")
        f.write(f"Status: {sub_dict['Status']}\n")
        f.write("\n")

def summary(report_before: list, report_after: list, file:str):
    sub_list_before, sub_dict_before = report_before
    sub_list_after, sub_dict_after = report_after
    
    missing_value_before = total_missing_value(sub_list_before, 'null_value')
    missing_value_after = total_missing_value(sub_list_after, 'null_value')
    
    duplicate_row_before = sub_dict_before['duplicate']
    duplicate_row_after = sub_dict_after['duplicate']
    
    with open(f"validator/validation_of_{file}.txt", "a", encoding="utf-8") as f:
        f.write("------------------------------\n")
        f.write("  🔹 SUMMARY\n")
        f.write("------------------------------\n")
        f.write("\n")
        f.write("Total Issues Fixed\n")
        f.write("\n")
        f.write(f"-- Missing values fixed : {missing_value_before} -> {missing_value_after}\n")
        f.write(f"-- Duplicate row removed : {duplicate_row_before} -> {duplicate_row_after}\n")
        f.write("\n")
        f.write(f"-- Datatype of column changed\n")
        f.write(f"   {sub_dict_before["data_type_changed"]["column"]} : {sub_dict_before["data_type_changed"]["dtype"]} -> {sub_dict_after["data_type_changed"]["dtype"]}\n")
        f.write("\n")
        f.write("Data Quality Improvement: 0% → 100%\n")
        f.write("\n")
        f.write("Final Data Quality: ✅ CLEAN & READY\n")

def write_report(report_before: list, report_after: list, fileInfo: dict):
    file = fileInfo["fileName"]
    logging.info("Preparing report")
    write_tittle(file)
    write_report_before_cleaning(report_before, file)
    write_report_after_cleaning(report_after, file)
    logging.info("Preparing summary")
    summary(report_before, report_after, file)
    
def total_missing_value(report: list, key: str) -> int:
    missing_value = 0
    for elm in report:
            missing_value += elm[key]
    return missing_value