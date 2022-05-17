import json
import logging
import os
import sys
from io import BytesIO

import pandas as pd
from sagemaker_inference import encoder

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Load filters folders
filters_dir = os.path.join(os.path.dirname(__file__))
sys.path.append(filters_dir)

from src.Ensemble.Ensemble_filter import EnsembleModel


def input_fn(input_data, content_type):
    """Parse input data payload

    We currently take json input. Since we need to process both labelled
    and unlabelled data we first determine whether the label column is present
    by looking at how many columns were provided.
    """
    logger.info("Processing input with content-type {}".format(content_type))
    if content_type == 'application/json':
        input_data = json.loads(input_data)
        return input_data

    elif content_type == "application/jsonlines":
        dataframe = pd.read_json(BytesIO(input_data), lines=True)
        logger.info(f"Infering {dataframe.shape} dataframe.")
        return dataframe

    else:
        raise ValueError("{} not supported by script!".format(content_type))


def model_fn(model_dir):
    """
    Deserialize and return fitted model.
    """
    model = None

    return model


def predict_fn(input_data, model):
    """Preprocess input data
    The output is returned in the following order:
        rest of features either one hot encoded or standardized
    """

    logger.info("Starting prediction")

    filter_object = EnsembleModel()
    prediction = filter_object.predict(input_data['review'])

    return prediction


def output_fn(prediction, accept):
    """Format prediction output

    The default accept/content-type between containers for serial inference is JSON.
    We also want to set the ContentType or mimetype as the same value as accept so the next
    container can read the response payload correctly.
    """
    if accept == 'text/csv':
        return encoder.encode(prediction, accept), accept

    elif accept == 'application/json':
        return prediction

    else:
        raise ValueError(f"{accept} accept type is not supported by this script.")
