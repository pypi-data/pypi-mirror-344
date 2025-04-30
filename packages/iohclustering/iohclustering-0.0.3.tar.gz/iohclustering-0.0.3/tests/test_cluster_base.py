import unittest
from unittest.mock import patch, MagicMock
import numpy as np
import ioh
from iohclustering.cluster_base import create_cluster_problem, get_problem_id, get_problem, load_problems, get_kmeans_pp_baseline
from iohclustering.cluster_baseline_problems import BASELINE_K_DIMENTIONS


class TestClusterBase(unittest.TestCase):

    def test_load_problems(self):
        # Test loading problems
        problems = load_problems()
        self.assertIsInstance(problems, dict)
        self.assertGreater(len(problems), 0)
        self.assertEqual(len(problems), 40)
        
        from iohclustering.cluster_baseline_problems import CLUSTER_BASELINE_DATASETS, BASELINE_K_DIMENTIONS
        # Check if the problems loaded match the expected datasets and dimensions
        for dataset, k_values in BASELINE_K_DIMENTIONS.items():
            for k in k_values:
                problem_name = f"Cluster_{dataset}_k{k}"
                self.assertIn(problem_name, problems.keys())

    def test_get_problem_id_valid(self):
        # Test valid dataset names
        self.assertEqual(get_problem_id("breast_pca"), 1)
        self.assertEqual(get_problem_id("bReAsT_PcA"), 1)  # Test case-insensitivity

    def test_get_problem_id_invalid(self):
        # Test invalid dataset name
        with self.assertRaises(ValueError) as context:
            get_problem_id("unknown_dataset")
        self.assertEqual(str(context.exception), "Unknown dataset name unknown_dataset")

    def test_create_cluster_problem(self):

        # Test creating a clustering problem
        k = 2
        f, retransform = create_cluster_problem("breast_pca", k= k, instance=1, error_metric="mse_euclidean")
        self.assertEqual(f.meta_data.name, "Cluster_breast_pca_k2")
        self.assertEqual(f.meta_data.problem_id, 1)
        self.assertEqual(f.meta_data.instance, 1)
        self.assertEqual(f.meta_data.n_variables, k*2)
        self.assertEqual(f.meta_data.optimization_type, ioh.OptimizationType.MIN)

    def test_create_cluster_problem_custom_data(self):

        # Test creating a clustering problem
        data = np.array([[0,0], [1,1], [3,3], [4,4]])
        k = 2
        f, retransform = create_cluster_problem(data, k= k, instance=1, error_metric="mse_euclidean")
        self.assertEqual(f.meta_data.name, "Cluster_custom_k2")
        self.assertEqual(f.meta_data.instance, 1)
        self.assertEqual(f.meta_data.n_variables, k*2)
        self.assertEqual(f.meta_data.optimization_type, ioh.OptimizationType.MIN)

        input_vec = np.array([[1.0, 2.0],[3.0, 4.0]])
        transformed_input_vec = np.array([0.25, 0.5, 0.75, 1.0])
        self.assertTrue(np.allclose(retransform(transformed_input_vec), input_vec))

    def test_get_problem(self):
        k = 2
        f, retransform = get_problem(1, instance=1, k=k)
        self.assertEqual(f.meta_data.name, "Cluster_breast_pca_k2")
        self.assertEqual(f.meta_data.problem_id, 1)
        self.assertEqual(f.meta_data.instance, 1)
        self.assertEqual(f.meta_data.n_variables, k*2)
        self.assertEqual(f.meta_data.optimization_type, ioh.OptimizationType.MIN)

        # Test retrieving a problem by dataset name
        f, retransform = get_problem("breast_pca", instance=1, k=2)
        self.assertEqual(f.meta_data.name, "Cluster_breast_pca_k2")
        self.assertEqual(f.meta_data.problem_id, 1)
        self.assertEqual(f.meta_data.instance, 1)
        self.assertEqual(f.meta_data.n_variables, k*2)
        self.assertEqual(f.meta_data.optimization_type, ioh.OptimizationType.MIN)

        # Test invalid dataset ID
        with self.assertRaises(ValueError) as context:
            get_problem(99, instance=1, k=2)
        self.assertEqual(str(context.exception), "Unknown dataset id 99")

    

    def test_get_kmeans_pp_baseline(self):
        # Test loading the k-means++ baseline problems
        baseline_kmeans_pp_mse = get_kmeans_pp_baseline()

        self.assertEqual(len(baseline_kmeans_pp_mse), 40)

        

if __name__ == "__main__":
    unittest.main()