from src.loan.entity.artifact_entity import ClassificationMetricArtifact
from src.loan.exception import ModelException
import sys,os
from sklearn.metrics import f1_score,precision_score, recall_score

def get_classification_score(y_true,y_pred) -> ClassificationMetricArtifact:
    try:
        f1_scor = f1_score(y_true=y_true,y_pred=y_pred)
        precision = precision_score(y_pred=y_pred,y_true=y_true)
        recall = recall_score(y_true=y_true,y_pred=y_pred)
        
        classification_metric_artifact =  ClassificationMetricArtifact(
            f1_score=f1_scor,
            precision_score=precision,
            recall_score=recall
        )
        return classification_metric_artifact
    except Exception as e:
        raise ModelException(e,sys)