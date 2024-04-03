from src.loan.logger import logging
from src.loan.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
from src.loan.pipeline.training_pipeline import TrainPipeline
import os
if __name__ == '__main__':
    trainig = TrainPipeline()
    trainig.run_pipeline()
    logging.info("All is ok")

    