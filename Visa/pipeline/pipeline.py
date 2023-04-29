import sys,os
from Visa import *
from Visa.logger import logging
from Visa.exception import CustomException
from Visa.entity.config_entity import *
from Visa.utils.utils import read_yaml_file
from Visa.constant import *
from Visa.components.data_ingestion import DataIngestion
from Visa.components.data_validation import DataValidation
from Visa.components.data_transformation import DataTransformation
from Visa.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig
from Visa.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact,ModelTrainerArtifact
from Visa.config.configuration import Configuration
from Visa.components.model_trainer import ModelTrainer


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
        
    def start_data_validation(self, data_ingestion_artifact:DataIngestionArtifact)-> DataValidationArtifact:
        try:
            data_validation = DataValidation(data_validation_config=self.config.get_data_validation_config(),
                                             data_ingestion_artifact=data_ingestion_artifact)
            return data_validation.initiate_data_validation()
        except Exception as e:
            raise CustomException(e, sys) from e

    def start_data_transformation(self,
                                  data_ingestion_artifact: DataIngestionArtifact,
                                  data_validation_artifact: DataValidationArtifact) -> DataTransformationArtifact:
        try:
            data_transfromation = DataTransformation(
                data_transformation_config=self.config.get_data_transformation_config(),
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_artifact=data_validation_artifact
            )

            return data_transfromation.initiate_data_transformation()
        except Exception as e:
            raise CustomException(e, sys) from e
    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            model_trainer = ModelTrainer(model_trainer_config=self.config.get_model_trainer_config(),
                                         data_transformation_artifact=data_transformation_artifact
                                         )
            return model_trainer.initiate_model_trainer()
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transfromation_artifact = self.start_data_transformation(data_ingestion_artifact=data_ingestion_artifact,
                                                                          data_validation_artifact=data_validation_artifact)
            
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_transfromation_artifact)
    
        except Exception as e:
            raise CustomException(e,sys)