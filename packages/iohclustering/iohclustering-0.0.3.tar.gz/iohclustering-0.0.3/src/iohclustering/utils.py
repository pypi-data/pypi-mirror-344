from importlib.resources import files
from .cluster_baseline_problems import CLUSTER_BASELINE_DATASETS
import numpy as np


def get_dataset(dataset: int | str) -> np.ndarray:
    """
    Load a dataset from the static resources.
    Parameters:

    ----------  
    dataset : int or str
        The dataset to load. If an integer is provided, it is used to index into the
        CLUSTER_BASELINE_DATASETS dictionary. If a string is provided, it is used as the
        dataset name directly.
    Returns:
    -------
        np.ndarray
            The loaded dataset as a NumPy array.
    Raises:
    -------
        ValueError: If the dataset name is not found in `CLUSTER_BASELINE_DATASETS`.
        FileNotFoundError : If the dataset file does not exist in the specified path.
    """

    if(type(dataset) == int):
        dataset = CLUSTER_BASELINE_DATASETS[dataset]
    dataset_path = files("iohclustering.static").joinpath(f"{dataset}.txt")
    data = np.loadtxt(dataset_path, delimiter=',')

    return data