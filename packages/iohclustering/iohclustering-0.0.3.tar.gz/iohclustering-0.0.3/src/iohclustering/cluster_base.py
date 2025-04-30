import tarfile
import warnings

import urllib
import ioh 
import numpy as np
import os
from .cluster_metrics import *
from .cluster_baseline_problems import *
from importlib.resources import files
import pandas as pd

def create_cluster_problem(dataset: str | np.ndarray, k: int, instance=1, error_metric="mse_euclidean") -> tuple[ioh.problem.RealSingleObjective, callable]:
    """
    Creates a clustering problem wrapped as an IOH problem for optimization.
    
    Parameters:
    ---------
        dataset : str or np.ndarray
            The dataset to be used for clustering. If a string is provided, it is assumed
            to be the name of a banchmark dataset. If an np.ndarray is provided, it is used directly
            as the dataset.
        k : int
            The number of clusters to create.
        instance : int, optional (default=1)
            The instance number for the problem. Useful for generating different problem
            instances with the same structure.
        error_metric : str or callable, optional (default="mse_euclidean")
            The error metric to evaluate the clustering. If a string is provided, it must
            match one of the predefined metrics in `CLUSTER_METRICS`. If a callable is provided,
            it should accept two arguments: the normalized dataset and the cluster centers.
    
    Returns:
    ---------
        f : ioh.problem.RealSingleObjective
            The IOH-wrapped clustering problem, ready for optimization.
        retransform : callable
                        A function that retransforms the optimized solution back to the original scale
                        of the dataset. It accepts a 1D array of cluster centers and returns a 2D array
                        of shape (k, number_of_features).

    Raises:
    ---------
        ValueError : If the provided `error_metric` is a string and does not match any predefined
                     metric in `CLUSTER_METRICS`.

    Notes:
        - The dataset is normalized to the range [0, 1] to ensure consistent scaling.
        - The `retransform` function can be used to map the normalized cluster centers
            back to their original scale.
        - The problem is set up for minimization, as clustering typically aims to minimize
            the error metric.
    """
    id = None
    if isinstance(dataset, str):
        id = get_problem_id(dataset)
        dataset_path = files("iohclustering.static").joinpath(f"{dataset}.txt")
        data = np.loadtxt(dataset_path, delimiter=',')

    else:
        data = dataset
        dataset = 'custom'

    if isinstance(error_metric, str):
        if error_metric in CLUSTER_METRICS.keys():
            error_metric = CLUSTER_METRICS[error_metric]
        else:
            raise ValueError(f"Unknown metric {error_metric}")
    

    data_np = np.array(data)
    # Normalize the data to the range [0, 1]
    data_min = np.tile(np.min(data_np, axis=0), k)
    data_max = np.tile(np.max(data_np, axis=0), k)
    data_normalized = (data_np - np.min(data_np, axis=0)) / (np.max(data_np, axis=0) - np.min(data_np, axis=0))
    
    # Define the objective function to be minimized
    def obj_func(x: np.ndarray) -> float:
        return error_metric(data_normalized, x.reshape(k, np.size(data_np, axis=1)))

    # Wrap the function as an IOH problem
    f = ioh.wrap_problem(
        obj_func,                                   # Handle to the function
        name=f"Cluster_{dataset}_k{k}",             # Name to be used when instantiating
        optimization_type=ioh.OptimizationType.MIN, # Specify that we want to minimize
        problem_class=ioh.ProblemClass.REAL,        # Problem class
        lb=0,                                       # Lower bound of the search space
        ub=1,                                       # Upper bound of the search space
        instance=instance,                          # Instance number
        dimension=int(k * np.size(data_np, axis=1)) # Dimension of the problem (k * number of features)
    )
    
    # Set the meta data for the problem
    if(id is not None):
        f.set_id(id)

    def retransform(X):
        X2 = ((X * (data_max - data_min)) + data_min)
        return X2.reshape(k, -1)

    return f, retransform


def get_problem_id(dataset_name: str) -> int:
    """
    Retrieve the problem ID associated with a given dataset name.
    This function takes a dataset name as input, converts it to lowercase, 
    and checks if it exists in the `CLUSTER_BASELINE_DATASETS` dictionary. 
    If the dataset name is found, it returns the corresponding problem ID. 
    Otherwise, it raises a `ValueError`.

    Parameters:
    ---------
        dataset_name (str): The name of the dataset to look up.
    
    Returns:
    ---------
        int: The problem ID associated with the given dataset name.
    
    Raises:
    ---------
        ValueError: If the dataset name is not found in `CLUSTER_BASELINE_DATASETS`.
    
    """
    dataset_name = dataset_name.lower()
    if dataset_name in CLUSTER_BASELINE_DATASETS.values():
        for k, v in CLUSTER_BASELINE_DATASETS.items():
            if v == dataset_name:
                return k
    else:
        raise ValueError(f"Unknown dataset name {dataset_name}")


def get_problem(fid: int | str, instance: int = 1, k: int = 2) -> ioh.problem.RealSingleObjective:
    """
    Retrieve a clustering problem based on the given dataset identifier.

    Parameters:
    ---------
        fid (int | str): The dataset identifier, either as an integer or a string.
                         If a string is provided, it will be converted to an integer
                         using the `get_problem_id` function.
        instance (int, optional): The instance of the dataset to use. Defaults to 1.
        k (int, optional): The number of clusters for the clustering problem. Defaults to 2.

    Returns:
    ---------
        f : ioh.problem.RealSingleObjective
              The IOH-wrapped clustering problem, ready for optimization.
        retransform : callable
                        A function that retransforms the optimized solution back to the original scale
                        of the dataset. It accepts a 1D array of cluster centers and returns a 2D array
                        of shape (k, number_of_features).

    Raises:
    ---------
        ValueError: If the provided dataset identifier is not found in the
                    `CLUSTER_BASELINE_DATASETS` dictionary.
    """
    if(type(fid) == str):
        fid = get_problem_id(fid)
    
    if fid not in CLUSTER_BASELINE_DATASETS.keys():
        raise ValueError(f"Unknown dataset id {fid}")

    return create_cluster_problem(
        dataset=CLUSTER_BASELINE_DATASETS[fid],
        k=k,
        instance=instance,
        error_metric=CLUSTER_METRICS["mse_euclidean"]
    )




def load_problems():
    """
    Loads clustering problems from the specified datasets path.

    This function iterates through a predefined set of baseline datasets and 
    checks if corresponding dataset files (with a `.txt` extension) exist in 
    the given directory. For each dataset, it generates clustering problems 
    for a set of predefined dimensions (k-values) and stores them in a dictionary.

    Parameters:
    ---------
        datasets_path (str): The path to the directory containing dataset files. 
                             Defaults to "banchmark_datasets".

    Returns:
    ---------
        dict: A dictionary where the keys are problem names (from metadata) 
              and the values are the corresponding clustering problem objects.

    """
    
    folder = files("iohclustering.static")
    datasets_names = [f.name for f in folder.iterdir() if f.suffix == ".txt"]

    problems = {}
    for dataset in CLUSTER_BASELINE_DATASETS.values():
        if f"{dataset}.txt" in datasets_names:
            for k in BASELINE_K_DIMENTIONS[dataset]:
                problem, retransform = create_cluster_problem(dataset, k)
                problems[problem.meta_data.name] = problem, retransform
    return problems


def get_kmeans_pp_baseline():
    """
    Load the KMeans++ baseline data from a CSV file.

    This function reads the KMeans++ baseline data from a CSV file and returns
    it as a Pandas DataFrame. The CSV file is expected to be located in the
    "iohclustering.static" directory.

    Returns:
    ---------
        pd.DataFrame: The KMeans++ baseline data as a Pandas DataFrame.
    
    Raises:
    ---------
        FileNotFoundError: If the KMeans++ baseline file does not exist.
    """
    
    kmeanspp_baseline_path = files("iohclustering.static").joinpath(KMEANSPP_BASELINE_FILE)
    if not os.path.exists(kmeanspp_baseline_path):
        raise FileNotFoundError(f"KMeans++ baseline file {KMEANSPP_BASELINE_FILE} does not exist.")
    
    return pd.read_csv(kmeanspp_baseline_path)
