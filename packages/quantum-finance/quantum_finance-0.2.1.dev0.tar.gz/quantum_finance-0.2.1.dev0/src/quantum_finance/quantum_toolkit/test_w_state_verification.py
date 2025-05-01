#!/usr/bin/env python3
"""
W-State Verification Test Script (Updated for Consolidated Implementation)

This script tests and verifies the correctness of the consolidated W-state 
implementation, including optional noise simulation.
"""

import os
import sys
import numpy as np
import unittest  # Use unittest framework for better structure
from typing import Tuple

# --- Path Setup --- #
# Add project root to path to allow imports from src
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
if project_root not in sys.path:
    sys.path.append(project_root)
print(f"Added {project_root} to sys.path")

# --- Imports --- #
try:
    # Import the consolidated W-state functions
    from src.quantum_finance.quantum_toolkit.circuits.w_state_consolidated import (
        create_w_state, 
        verify_w_state,
        create_theoretical_w_state
    )
    # Import Qiskit components needed for testing
    from qiskit import QuantumCircuit
    from qiskit_aer.noise import NoiseModel, depolarizing_error, ReadoutError # For creating test noise model
    HAS_DEPENDENCIES = True
    print("✅ Successfully imported W-state module and Qiskit/Aer components.")
except ImportError as e:
    HAS_DEPENDENCIES = False
    print(f"❌ Error importing dependencies: {e}")
    print("   Please ensure qiskit, qiskit-aer are installed and the project structure is correct.")
    # Optionally, re-raise or exit if dependencies are critical
    # raise e 
    sys.exit(1) # Exit if core dependencies are missing

# --- Test Class --- #
@unittest.skipIf(not HAS_DEPENDENCIES, "Skipping tests due to missing dependencies (Qiskit/Aer or W-state module)")
class TestWStateVerification(unittest.TestCase):
    """Test suite for the consolidated W-state implementation and verification."""

    def test_w_state_creation_and_verification_basic(self):
        """Tests basic W-state creation and verification without noise."""
        print("\n--- Testing Basic W-State Verification (No Noise) ---")
        for n_qubits in [1, 2, 3, 4, 5]: # Test a range of qubit counts
            with self.subTest(n_qubits=n_qubits):
                print(f"Testing {n_qubits}-qubit W-state...")
                try:
                    # Create the circuit
                    circuit = create_w_state(n_qubits)
                    self.assertIsInstance(circuit, QuantumCircuit)
                    
                    # Verify (noise-free)
                    is_valid, fidelity = verify_w_state(circuit, num_qubits=n_qubits)
                    
                    self.assertTrue(is_valid, f"{n_qubits}-qubit state failed ideal verification (Fidelity: {fidelity:.4f})")
                    self.assertAlmostEqual(fidelity, 1.0, delta=0.01, msg=f"{n_qubits}-qubit state fidelity deviates significantly from 1.0")
                    print(f"  {n_qubits}-qubit PASSED (Fidelity: {fidelity:.6f})")

                except Exception as e:
                    self.fail(f"Error during {n_qubits}-qubit basic test: {e}")

    def test_w_state_verification_with_noise(self):
        """Tests W-state verification with a basic noise model."""
        print("\n--- Testing W-State Verification with Noise --- ")
        n_qubits = 3 # Use a small example for noise simulation
        depol_prob = 0.01 # 1% depolarizing error on CX
        readout_prob = 0.02 # 2% readout error 
        fidelity_floor = 0.90 # Expect fidelity drop, but should still be high
        fidelity_ceiling = 0.995 # Expect fidelity to be noticeably less than 1.0
        
        print(f"Testing {n_qubits}-qubit W-state with depolarizing={depol_prob}, readout={readout_prob}...")

        try:
            # Create the circuit
            circuit = create_w_state(n_qubits)
            
            # Verify with noise probabilities
            is_valid, fidelity = verify_w_state(
                circuit, 
                num_qubits=n_qubits, 
                depolarizing_prob=depol_prob,
                readout_error_prob=readout_prob, # Pass readout error for completeness
                fidelity_threshold=fidelity_floor # Use lower threshold for noisy case
            )
            
            self.assertTrue(is_valid, f"{n_qubits}-qubit state failed noisy verification (Fidelity: {fidelity:.4f} < Threshold: {fidelity_floor})")
            self.assertLess(fidelity, fidelity_ceiling, f"{n_qubits}-qubit noisy fidelity ({fidelity:.4f}) was unexpectedly high, expected < {fidelity_ceiling}")
            self.assertGreater(fidelity, fidelity_floor, f"{n_qubits}-qubit noisy fidelity ({fidelity:.4f}) was unexpectedly low, expected > {fidelity_floor}")
            print(f"  {n_qubits}-qubit PASSED noisy test (Fidelity: {fidelity:.6f})")
            
            # --- Test with pre-built noise model --- # 
            print(f"\nTesting {n_qubits}-qubit W-state with pre-built noise model...")
            noise_model_prebuilt = NoiseModel()
            error_depol = depolarizing_error(depol_prob, 2)
            noise_model_prebuilt.add_all_qubit_quantum_error(error_depol, ['cx']) # Target by name here is okay for NoiseModel construction
            error_readout = ReadoutError([[1 - readout_prob, readout_prob], [readout_prob, 1 - readout_prob]])
            noise_model_prebuilt.add_all_qubit_readout_error(error_readout)
            
            is_valid_nm, fidelity_nm = verify_w_state(
                circuit, 
                num_qubits=n_qubits, 
                noise_model=noise_model_prebuilt,
                fidelity_threshold=fidelity_floor 
            )
            self.assertTrue(is_valid_nm, f"{n_qubits}-qubit state failed pre-built noise model verification (Fidelity: {fidelity_nm:.4f} < Threshold: {fidelity_floor})")
            self.assertLess(fidelity_nm, fidelity_ceiling, f"{n_qubits}-qubit pre-built noisy fidelity ({fidelity_nm:.4f}) was unexpectedly high, expected < {fidelity_ceiling}")
            self.assertGreater(fidelity_nm, fidelity_floor, f"{n_qubits}-qubit pre-built noisy fidelity ({fidelity_nm:.4f}) was unexpectedly low, expected > {fidelity_floor}")
            print(f"  {n_qubits}-qubit PASSED pre-built noise model test (Fidelity: {fidelity_nm:.6f})")


        except Exception as e:
            self.fail(f"Error during {n_qubits}-qubit noise test: {e}")

    def test_invalid_qubit_count(self):
        """Tests that create_w_state raises ValueError for n_qubits < 1."""
        print("\n--- Testing Invalid Qubit Count --- ")
        with self.assertRaises(ValueError):
            create_w_state(0)
        with self.assertRaises(ValueError):
            create_w_state(-1)
        print("  PASSED invalid qubit count tests.")

# --- Main Execution --- #
if __name__ == "__main__":
    print("Running W-State Verification Tests...")
    # Add setup/teardown if needed later
    unittest.main()
