import os
from box.exceptions import BoxValueError
import yaml
from PubMed import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
import yaml
import pandas as pd


def load_config(path="config/config.yaml"):
    """Load configuration from YAML file."""
    try:
        with open(path, "r") as file:
            return yaml.safe_load(file)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e

# def filter_affiliations(authors):
#     """Check if at least one author is affiliated with a pharma or biotech company."""
#     pharma_keywords = ["pharma", "biotech", "med", "therapeutics"]
#     try:
#         for author in authors:
#             affiliation = author.get("affiliation", "").lower()
#         if any(keyword in affiliation for keyword in pharma_keywords):
#             return True
#         return False
#     except BoxValueError:
#         raise ValueError("yaml file is empty")
#     except Exception as e:
#         raise e


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e
    


# @ensure_annotations
# def create_directories(path_to_directories: list, verbose=True):
#     for path in path_to_directories:
#         os.makedirs(path, exist_ok=True)
#         if verbose:
#             logger.info(f"created directory at: {path}")


@ensure_annotations
def save_json(path: Path, data: dict):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    logger.info(f"json file saved at: {path}")

@ensure_annotations
def save_to_csv(papers):
    try:
        filename="data/filtered_papers.csv"
        df = pd.DataFrame(papers)
        df.to_csv(filename, index=False)
        print(f"Saved {len(papers)} papers to {filename}")
        logger.info(f"json file saved at: {filename}")
    except Exception as e:
        logger.exception(e)
        
        raise e


# @ensure_annotations
# def load_json(path: Path) -> ConfigBox:
#     """load json files data

#     Args:
#         path (Path): path to json file

#     Returns:
#         ConfigBox: data as class attributes instead of dict
#     """
#     with open(path) as f:
#         content = json.load(f)

#     logger.info(f"json file loaded succesfully from: {path}")
#     return ConfigBox(content)


# @ensure_annotations
# def save_bin(data: Any, path: Path):
#     """save binary file

#     Args:
#         data (Any): data to be saved as binary
#         path (Path): path to binary file
#     """
#     joblib.dump(value=data, filename=path)
#     logger.info(f"binary file saved at: {path}")


# @ensure_annotations
# def load_bin(path: Path) -> Any:
#     """load binary data

#     Args:
#         path (Path): path to binary file

#     Returns:
#         Any: object stored in the file
#     """
#     data = joblib.load(path)
#     logger.info(f"binary file loaded from: {path}")
#     return data



# @ensure_annotations
# def get_size(path: Path) -> str:
#     """get size in KB

#     Args:
#         path (Path): path of the file

#     Returns:
#         str: size in KB
#     """
#     size_in_kb = round(os.path.getsize(path)/1024)
#     return f"~ {size_in_kb} KB"



