from cnnClassifier.constants import *
from cnnClassifier.utils.common import read_yaml, create_directories
from cnnClassifier.entity.config_entity import DataIngestionConfig
from cnnClassifier.entity.config_entity import TrainingConfig
from cnnClassifier.entity.config_entity import PrepareBaseModelConfig
from cnnClassifier.entity.config_entity import EvaluationConfig
from cnnClassifier.entity.config_entity import SplitConfig

import os
class ConfigurationManager:
    def __init__(
            self,
            config_filepath= CONFIG_FILE_PATH,
            params_filepath = PARAMS_FILE_PATH
    ):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)

        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config= DataIngestionConfig(
            root_dir= config.root_dir,
            source_URL= config.source_URL,
            local_data_file= config.local_data_file,
            unzip_dir= config.unzip_dir
        )

        return data_ingestion_config

    def get_prepare_base_model_config(self) -> PrepareBaseModelConfig:
        config = self.config.prepare_base_model
        
        create_directories([config.root_dir])

        prepare_base_model_config = PrepareBaseModelConfig(
            root_dir=Path(config.root_dir),
            base_model_path=Path(config.base_model_path),
            params_image_size=self.params.IMAGE_SIZE,
            params_learning_rate=self.params.LEARNING_RATE,
        )

        return prepare_base_model_config

    def get_training_config(self) -> TrainingConfig:
        training = self.config.training
        prepare_base_model = self.config.prepare_base_model
        params = self.params
        Med_train = training.Med_train
        Cover_train= training.Cover_train
        Med_val=training.Med_val
        Cover_val=training.Cover_val
        create_directories([
            Path(training.root_dir)
        ])

        training_config = TrainingConfig(
            root_dir=Path(training.root_dir),
            trained_model_path=Path(training.trained_model_path),
            base_model_path=Path(prepare_base_model.base_model_path),
            Med_train=Path(Med_train),
            Cover_train= Path(Cover_train),
            Med_val= Path(Med_val),
            Cover_val= Path(Cover_val),
            params_epochs=params.EPOCHS,
            params_batch_size=params.BATCH_SIZE,
            params_is_augmentation=params.AUGMENTATION,
            params_image_size=params.IMAGE_SIZE
        )

        return training_config
    def get_evaluation_config(self) -> EvaluationConfig:
        eval_config = EvaluationConfig(
            path_of_model= r"artifacts\training\model.h5",
            Med_test= r"artifacts\data_ingestion\Data-CS-DVC\test_data\Med_test",
            Cover_test= r"artifacts\data_ingestion\Data-CS-DVC\test_data\Cover_test",
            all_params= self.params,
            mlflow_uri= r"https://dagshub.com/08Youssef08/Securing-Medical-Data-Transfer-Using-Deep-Steganography-and-Cryptography-MLflow-DVC.mlflow",
            params_image_size= self.params.IMAGE_SIZE,
            params_batch_size= self.params.BATCH_SIZE
        )
        return eval_config
    def get_split_config(self) -> SplitConfig:
        model_split = self.config.model_split
        create_directories([
            Path(model_split.root_dir)
        ])

        split_config = SplitConfig(
            root_dir=Path(model_split.root_dir),
            trained_model_path=Path(model_split.trained_model_path),
            hiding_model_path = Path(model_split.hiding_model_path),
            reveal_model_path = Path(model_split.reveal_model_path)
        )

        return split_config