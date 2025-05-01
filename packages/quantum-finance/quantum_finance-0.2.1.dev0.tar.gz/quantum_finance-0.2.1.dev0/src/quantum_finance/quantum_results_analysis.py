"""
Module for analyzing Qiskit Runtime primitive results:
- plotting expectation values with error bars
- mapping expectation values to binary predictions
"""

from typing import List, Any, Dict
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.figure import Figure


def plot_expectation_values(evs: np.ndarray, stds: np.ndarray, labels: List[str]) -> Figure:
    """
    Plot expectation values with error bars.
    evs: array of floats shape (n_observables,)
    stds: array of uncertainties shape (n_observables,)
    labels: list of observable names
    """
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.errorbar(labels, evs, yerr=stds, fmt='-o', capsize=4)
    ax.set_xlabel("Observables")
    ax.set_ylabel("Expectation values")
    ax.set_title("Quantum Measurement Results")
    ax.grid(True)
    plt.tight_layout()
    return fig


def map_expectations_to_binary(evs: np.ndarray, threshold: float = 0.0) -> np.ndarray:
    """
    Convert an array of expectation values into binary predictions (0 or 1).
    threshold: cutoff for predicting 1 (default: 0.0)
    """
    return (evs > threshold).astype(int)


def analyze_primitive(pub_result: Any, observables_labels: List[str], threshold: float = 0.0) -> Dict[str, Any]:
    """
    Full analysis pipeline for a single PubResult:
    - Extract expectation values and standard deviations
    - Generate a plot figure of the measurements
    - Map expectations to binary predictions
    Returns a dict with 'figure' and 'predictions'.
    """
    evs = pub_result.data.evs
    stds = pub_result.data.stds
    fig = plot_expectation_values(evs, stds, observables_labels)
    preds = map_expectations_to_binary(evs, threshold)
    return {"figure": fig, "predictions": preds} 