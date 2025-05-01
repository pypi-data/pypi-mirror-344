"""
Standard quantum circuits library.

This module provides implementations of standard quantum circuits
that are commonly used in quantum algorithms and experiments.
"""

import logging
import numpy as np
from typing import Optional, List, Tuple, Dict

# Import the custom QuantumCircuit class
from quantum_finance.quantum_toolkit.core.circuit import QuantumCircuit
# Qiskit circuit import might not be needed here if only using custom class
# from qiskit import QuantumCircuit as QiskitCircuit, ClassicalRegister, QuantumRegister
# from qiskit.circuit.library import QFT # QFT needs specific handling

# Configure logging
logger = logging.getLogger(__name__)


def create_bell_state() -> QuantumCircuit:
    """
    Creates a Bell state (|Φ+⟩ = |00⟩ + |11⟩) / √2 circuit
    using the custom QuantumCircuit class.

    Returns:
        QuantumCircuit: Custom circuit object for the Bell state.
    """
    n_qubits = 2
    circuit = QuantumCircuit(num_qubits=n_qubits, name="bell_state")
    circuit.h(0)  # Apply Hadamard to the first qubit
    circuit.cx(0, 1)  # Apply CNOT with control q0 and target q1
    # Measurements removed - handle downstream if needed
    logger.debug("Created Bell state circuit")
    return circuit


def create_ghz_state(n_qubits: int) -> QuantumCircuit:
    """
    Creates a GHZ (Greenberger–Horne–Zeilinger) state circuit
    using the custom QuantumCircuit class.
    (|00...0⟩ + |11...1⟩) / √2

    Args:
        n_qubits (int): Number of qubits (must be >= 2).

    Returns:
        QuantumCircuit: Custom circuit object for the GHZ state.

    Raises:
        ValueError: If n_qubits < 2.
    """
    if n_qubits < 2:
        raise ValueError("GHZ state requires at least 2 qubits")

    circuit = QuantumCircuit(num_qubits=n_qubits, name=f"ghz_state_{n_qubits}")
    circuit.h(0) # Apply Hadamard to the first qubit
    # Apply CNOT gates from the first qubit to all others
    for i in range(1, n_qubits):
        circuit.cx(0, i)
    # Measurements removed
    logger.debug(f"Created GHZ state circuit with {n_qubits} qubits")
    return circuit


def create_quantum_fourier_transform(
    n_qubits: int,
    approximation_degree: int = 0,
    do_swaps: bool = True,
    inverse: bool = False,
    insert_barriers: bool = False # Barrier functionality might not exist in custom class
) -> QuantumCircuit:
    """
    Creates a Quantum Fourier Transform (QFT) circuit
    using the custom QuantumCircuit class.

    Note: This is a basic implementation mapping QFT concepts to the custom
          circuit's available gates (H, controlled rotations represented by CX/single qubit gates).
          Advanced Qiskit QFT features like approximation_degree might not be
          fully representable without adding corresponding gates (e.g., controlled phase)
          to the custom class or its to_qiskit converter.
          Barriers are likely not supported.

    Args:
        n_qubits (int): Number of qubits.
        approximation_degree (int): Degree of approximation (currently ignored).
        do_swaps (bool): Whether to include final swaps (currently ignored, requires SWAP gate).
        inverse (bool): If True, creates the Inverse QFT (currently ignored).
        insert_barriers (bool): If True, inserts barriers (currently ignored).

    Returns:
        QuantumCircuit: Custom circuit object approximating the QFT.
    """
    circuit = QuantumCircuit(num_qubits=n_qubits, name="qft")

    if approximation_degree != 0:
        logger.warning("QFT approximation_degree is currently ignored in custom circuit implementation.")
    if inverse:
         logger.warning("Inverse QFT is currently ignored in custom circuit implementation.")
    if insert_barriers:
         logger.warning("Barrier insertion is currently ignored in custom circuit implementation.")

    # QFT Algorithm adapted for basic gates (H, CX, phase gates like S, T, Z)
    # This is a simplified implementation. Accurate QFT needs controlled phase gates.
    # We will use H and CX as placeholders for the structure.
    for i in range(n_qubits):
        circuit.h(i)
        # Apply controlled rotations (approximated/placeholder)
        for j in range(i + 1, n_qubits):
            # A real QFT uses controlled phase gates here (e.g., CP(pi/2**(j-i)))           
            # We don't have CP in the custom class, add placeholder CX for structure
            logger.warning(f"Using placeholder CX({j}, {i}) for QFT controlled phase gate.")
            circuit.cx(j, i)

    # Swaps are typically needed at the end, but SWAP gate is not standard in custom class
    if do_swaps:
        logger.warning("QFT swaps are currently ignored as SWAP gate is not implemented in custom class.")
        # for i in range(n_qubits // 2):
        #     circuit.add_gate('swap', [i, n_qubits - 1 - i]) # If SWAP were added

    logger.debug(f"Created placeholder QFT circuit with {n_qubits} qubits")
    return circuit


def create_inverse_quantum_fourier_transform(
    n_qubits: int,
    approximation_degree: int = 0,
    do_swaps: bool = True,
    insert_barriers: bool = False
) -> QuantumCircuit:
    """
    Creates an Inverse Quantum Fourier Transform (IQFT) circuit
    using the custom QuantumCircuit class.

    Note: This currently just calls the placeholder QFT implementation.
          A proper IQFT would require reversing the QFT operations and using
          inverse controlled phase gates.
          See QFT notes regarding limitations.

    Args:
        n_qubits (int): Number of qubits.
        approximation_degree (int): Degree of approximation (currently ignored).
        do_swaps (bool): Whether to include initial swaps (currently ignored).
        insert_barriers (bool): If True, inserts barriers (currently ignored).

    Returns:
        QuantumCircuit: Custom circuit object approximating the IQFT.
    """
    logger.warning("IQFT implementation currently returns the same placeholder as QFT.")
    # A true IQFT would involve reversed operations and inverse gates.
    # For now, just return the forward QFT placeholder.
    return create_quantum_fourier_transform(
        n_qubits=n_qubits,
        approximation_degree=approximation_degree,
        do_swaps=do_swaps,
        inverse=True, # Mark as inverse, though implementation ignores it
        insert_barriers=insert_barriers
    )