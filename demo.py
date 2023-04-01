from Visa.entity.config_entity import DataIngestionConfig
from Visa.entity.artifact_entity import DataIngestionArtifact
from Visa.config.configuration import Configuration
import os,sys
from Visa.logger import logging
from Visa.pipeline.pipeline import Pipeline
from Visa.exception import CustomException

def main():
    try:
        pipeline = Pipeline()
        pipeline.run_pipeline()

    except Exception as e:
        logging.error(f"{e}")
        print(e)

if __name__ == "__main__":
    main()