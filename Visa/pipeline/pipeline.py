import sys,os
from Visa import *
from Visa.logger import logging
from Visa.exception import CustomException
from Visa.entity.config_entity import *
from Visa.utils.utils import read_yaml_file
from Visa.constant import *
from Visa.components.data_ingestion import DataIngestion
from Visa.entity.config_entity import DataIngestionConfig
from Visa.entity.artifact_entity import DataIngestionArtifact
from Visa.config.configuration import Configuration



class Pipeline():
    def __init__(self, config: Configuration = Configuration()) -> None:
        try:
            self.config = config
        except Exception as e:
            raise CustomException(e,sys)
        
    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(data_ingestion_config = self.config.get_data_ingestion_config()
                                           )
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise CustomException(e,sys)
        
        
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
    
        except Exception as e:
            raise CustomException(e,sys)