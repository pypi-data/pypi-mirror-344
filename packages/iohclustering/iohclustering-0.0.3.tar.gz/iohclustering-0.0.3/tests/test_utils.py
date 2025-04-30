import unittest
from unittest.mock import patch, MagicMock
import numpy as np
from iohclustering.utils import get_dataset
from iohclustering.cluster_baseline_problems import CLUSTER_BASELINE_DATASETS



class TestUtils(unittest.TestCase):

    @patch("iohclustering.utils.files")
    @patch("iohclustering.utils.np.loadtxt")
    def test_get_dataset_with_valid_int(self, mock_loadtxt, mock_files):
        # Mock the dataset path and data
        mock_files.return_value.joinpath.return_value = "mocked_path.txt"
        mock_loadtxt.return_value = np.array([[1, 2], [3, 4]])

        # Test with a valid integer index
        dataset_index = 0
        CLUSTER_BASELINE_DATASETS[dataset_index] = "mock_dataset"
        result = get_dataset(dataset_index)

        # Assertions
        mock_files.assert_called_once_with("iohclustering.static")
        mock_loadtxt.assert_called_once_with("mocked_path.txt", delimiter=",")
        np.testing.assert_array_equal(result, np.array([[1, 2], [3, 4]]))

    @patch("iohclustering.utils.files")
    @patch("iohclustering.utils.np.loadtxt")
    def test_get_dataset_with_valid_str(self, mock_loadtxt, mock_files):
        # Mock the dataset path and data
        mock_files.return_value.joinpath.return_value = "mocked_path.txt"
        mock_loadtxt.return_value = np.array([[5, 6], [7, 8]])

        # Test with a valid string
        dataset_name = "mock_dataset"
        result = get_dataset(dataset_name)

        # Assertions
        mock_files.assert_called_once_with("iohclustering.static")
        mock_loadtxt.assert_called_once_with("mocked_path.txt", delimiter=",")
        np.testing.assert_array_equal(result, np.array([[5, 6], [7, 8]]))

    def test_get_dataset_with_invalid_int(self):
        # Test with an invalid integer index
        invalid_index = 99
        with self.assertRaises(KeyError):
            get_dataset(invalid_index)

    def test_get_dataset_with_invalid_str(self):
        # Test with an invalid string
        invalid_name = "non_existent_dataset"
        with self.assertRaises(FileNotFoundError):
            get_dataset(invalid_name)


if __name__ == "__main__":
    unittest.main()