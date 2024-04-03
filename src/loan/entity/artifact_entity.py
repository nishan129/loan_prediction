from dataclasses import dataclass

@dataclass(frozen=True)
class DataIngestionArtifact:
    trained_file_path: str
    test_file_path: str
    
@dataclass(frozen=True)
class DataValidationArtifact:
    validation_status: bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_report_file_path: str
    
@dataclass(frozen=True)
class DataTransformationArtifact:
    transformed_object_filepath: str
    transformed_train_filepath: str
    transformed_test_filepath: str
    