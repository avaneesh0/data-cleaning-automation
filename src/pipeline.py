from src.cleaning import  loadDataFrame, removeDublicate, cleanData, saveOutput
from src.utils import dataframe_report, write_report, summary
import logging


logger = logging.getLogger(__name__)


def process_all_file(files: list):
    for file in files:
        
        if not file["loadDataFrame"]:
            continue
        
        data = loadDataFrame(file)
        dfReport_before = dataframe_report(data)

        processed_data = data.copy()

        processed_data = removeDublicate(processed_data)
        processed_data = cleanData(processed_data)                
        saveOutput(processed_data, file)
        
        dfReport_after = dataframe_report(processed_data, dfReport_before)
        write_report(dfReport_before , dfReport_after)
        
        logger.info(f"Processed {len(files)} files successfully")
