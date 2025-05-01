"""
Backend module for the quantum-AI platform.
"""

# This package contains backend functionality for the quantum-AI platform.
# No module-level application factory here; create_app is provided in the top-level backend facade.

# Backward compatibility shims: re-export core classes
from .quantum_algorithms import GroversAlgorithm, ShorWrapper
from .ml_framework import BayesianNN, TransformerModel
