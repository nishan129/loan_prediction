from src.loan.entity.artifact_entity import ClassificationMetricArtifact
from src.loan.exception import ModelException
import sys,os
import numpy as np
from sklearn.metrics import f1_score,precision_score, recall_score, accuracy_score

def get_classification_score(y_true,y_pred)->ClassificationMetricArtifact :
    try:
        pred = np.where(y_pred >= 0.5,1,0)
        accuracy = accuracy_score(y_true=y_true,y_pred=pred)
        f1_scor = f1_score(y_true=y_true,y_pred=pred)
        precision = precision_score(y_pred=pred,y_true=y_true)
        recall = recall_score(y_true=y_true,y_pred=pred)
        
        classification_metric_artifact =  ClassificationMetricArtifact(
            accuracy_score=accuracy,
            f1_score=f1_scor,
            precision_score=precision,
            recall_score=recall
        )
        return classification_metric_artifact
    except Exception as e:
        raise ModelException(e,sys)