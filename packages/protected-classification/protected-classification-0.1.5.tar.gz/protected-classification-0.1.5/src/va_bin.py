from typing import List, Tuple, NewType, TypeVar
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
import pandas as pd

from sklearn.calibration import CalibrationDisplay
from sklearn.naive_bayes import GaussianNB

from sklearn.metrics import log_loss, accuracy_score, brier_score_loss

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

from sklearn.calibration import CalibratedClassifierCV

np.random.seed(seed=1)

X, y = make_classification(
    n_samples=100000, n_features=20, n_informative=2, n_redundant=2, random_state=1
)

train_samples = 1000  # Samples used for training the models
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    shuffle=False,
    test_size=100000 - train_samples,
)

# Define data types.

clf = GaussianNB()
clf.fit(X_train, y_train)
clf_prob = clf.predict_proba(X_test)



Data = List[Tuple[float, float]]  # List of (predicted_probability, true_label).
Bins = List[float]  # List of bin boundaries, excluding 0.0, but including 1.0.
BinnedData = List[Data]  # binned_data[i] contains the data in bin i.
T = TypeVar('T')

eps = 1e-6


def split(sequence: List[T], parts: int) -> List[List[T]]:
    assert parts <= len(sequence)
    array_splits = np.array_split(sequence, parts)
    splits = [list(l) for l in array_splits]
    assert len(splits) == parts
    return splits


def get_equal_bins(probs: List[float], num_bins: int=10) -> Bins:
    """Get bins that contain approximately an equal number of data points."""
    sorted_probs = sorted(probs)
    if num_bins > len(sorted_probs):
        num_bins = len(sorted_probs)
    binned_data = split(sorted_probs, num_bins)
    bins: Bins = []
    for i in range(len(binned_data) - 1):
        last_prob = binned_data[i][-1]
        next_first_prob = binned_data[i + 1][0]
        bins.append((last_prob + next_first_prob) / 2.0)
    bins.append(1.0)
    bins = sorted(list(set(bins)))
    return bins


def get_equal_prob_bins(probs: List[float], num_bins: int=10) -> Bins:
    return [i * 1.0 / num_bins for i in range(1, num_bins + 1)]


def get_discrete_bins(data: List[float]) -> Bins:
    sorted_values = sorted(np.unique(data))
    bins = []
    for i in range(len(sorted_values) - 1):
        mid = (sorted_values[i] + sorted_values[i+1]) / 2.0
        bins.append(mid)
    bins.append(1.0)
    return bins



