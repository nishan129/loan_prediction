from dataclasses import dataclass

@dataclass(frozen=True)
class DataIngestionArtifact:
    trained_file_path: str
    test_file_path: str