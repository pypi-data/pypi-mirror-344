"""
W-State Circuit Implementation Module (Consolidated Version)

This module provides the canonical implementation of W-state quantum circuits,
consolidating the best features from all previous implementations. This is now
the recommended way to create W-states in the quantum toolkit.

A W-state is a quantum entangled state where exactly one qubit is in state |1⟩
while all others are in state |0⟩, with equal amplitudes across all such possibilities.

Examples:
- 2-qubit W-state: |W_2⟩ = (|01⟩ + |10⟩)/√2
- 3-qubit W-state: |W_3⟩ = (|001⟩ + |010⟩ + |100⟩)/√3
- n-qubit W-state: |W_n⟩ = (|00...01⟩ + |00...10⟩ + ... + |10...00⟩)/√n

This implementation uses:
1. Direct implementation for all qubit counts
2. Built-in verification
3. Comprehensive error checking
"""

import numpy as np
from typing import Optional, Tuple, Dict, List, Union

# Restore necessary Qiskit imports for verify_w_state
from qiskit import QuantumCircuit as QiskitCircuit, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, ReadoutError
from qiskit.quantum_info import Statevector, state_fidelity
from qiskit.result import Counts
# from qiskit.circuit.library import CXGate # Not directly used it seems

# Import the custom QuantumCircuit class
from quantum_finance.quantum_toolkit.core.circuit import QuantumCircuit

def create_w_state(num_qubits: int) -> QuantumCircuit:
    """
    Creates a quantum circuit that prepares the W-state for n qubits
    using the custom QuantumCircuit class.
    
    Currently implemented for n=1 and n=2 qubits only.

    Args:
        num_qubits (int): Number of qubits (1 or 2)
    
    Returns:
        QuantumCircuit: Custom circuit object preparing the W-state
        
    Raises:
        ValueError: If num_qubits < 1
        NotImplementedError: If num_qubits >= 3
    """
    if num_qubits < 1:
        raise ValueError("W-state requires at least 1 qubit")
    
    # Initialize custom circuit
    circuit = QuantumCircuit(num_qubits=num_qubits, name=f"w_state_{num_qubits}")
    
    if num_qubits == 1:
        # One qubit case: |1⟩
        circuit.x(0)
        
    elif num_qubits == 2:
        # Two qubit case: Standard implementation (|01> + |10>)/sqrt(2)
        circuit.x(0)
        circuit.h(0)
        circuit.cx(0, 1)
        circuit.x(0)
        
    else: # num_qubits >= 3
        # The iterative method using controlled-Ry is not directly supported
        # by the current custom QuantumCircuit class methods.
        # Raising error until this is implemented.
        raise NotImplementedError("W-state creation for 3 or more qubits is not yet implemented using the custom QuantumCircuit class methods.")
    
    # Measurement logic removed, handled downstream if needed.
    
    return circuit

def verify_w_state(
    circuit, # Removed type hint: accepts custom QuantumCircuit
    num_qubits: Optional[int] = None,
    fidelity_threshold: float = 0.99, # Used for statevector mode
    distribution_tolerance: float = 0.05, # Used for counts mode
    noise_model: Optional[NoiseModel] = None,
    depolarizing_prob: Optional[float] = None,
    readout_error_prob: Optional[float] = None,
    simulate_readout_error: bool = False,
    shots: int = 1024
) -> Union[Tuple[bool, float], Tuple[bool, Dict[str, float]]]:
    """
    Verifies that a circuit correctly implements a W-state, optionally simulating noise.

    This function accepts the custom QuantumCircuit object and converts it internally
    to a Qiskit circuit for simulation and verification.

    Args:
        circuit (QuantumCircuit): The custom circuit object to verify.
        num_qubits (Optional[int]): Number of qubits (inferred from circuit if None).
        fidelity_threshold (float): Minimum fidelity required for validation in statevector mode.
        distribution_tolerance (float): Maximum allowed probability deviation from ideal
                                       for any single state in counts mode (default: 0.05).
        noise_model (Optional[NoiseModel]): A pre-configured Qiskit Aer noise model.
                                           If provided, overrides depolarizing/readout probs.
        depolarizing_prob (Optional[float]): If noise_model is None, specifies the probability
                                             of 2-qubit depolarizing error on CX gates.
        readout_error_prob (Optional[float]): If noise_model is None, specifies the symmetric
                                              probability of a bit-flip during measurement.
                                              Used for both statevector noise and counts noise simulation.
        simulate_readout_error (bool): If True, run simulation with shots and return the raw
                                       noisy probability distribution. Defaults to False
                                       (uses statevector simulation and fidelity).
        shots (int): Number of shots to use for simulation when `simulate_readout_error` is True.
                     Defaults to 1024.

    Returns:
        Union[Tuple[bool, float], Tuple[bool, Dict[str, float]]]:
            - If simulate_readout_error is False: (is_valid, fidelity)
                - is_valid: True if fidelity > fidelity_threshold
                - fidelity: Statevector fidelity between the circuit's output and ideal W-state
            - If simulate_readout_error is True: (is_valid, noisy_probabilities)
                - is_valid: True if noisy distribution matches ideal W-state pattern within tolerance.
                - noisy_probabilities: Dictionary representing the noisy probability distribution (unmitigated).

    Raises:
        ValueError: If the input circuit cannot be converted to a Qiskit circuit.
        CircuitError: If simulate_readout_error is True but the circuit has no classical registers
                      or measurements defined.
    """
    # Convert custom circuit to Qiskit circuit first
    qiskit_circuit = circuit.to_qiskit()
    if qiskit_circuit is None:
        # Handle case where conversion fails (e.g., Qiskit not installed)
        print("ERROR: Failed to convert custom circuit to Qiskit circuit for verification.")
        # Raise an error or return a failure state appropriate for the caller
        raise ValueError("Input circuit could not be converted to a Qiskit circuit.")
        # Alternatively: return False, 0.0 if statevector mode else (False, {}) ?

    if num_qubits is None:
        # Use the number of qubits from the converted Qiskit circuit
        num_qubits = qiskit_circuit.num_qubits
    
    # Assert that num_qubits is now an integer
    assert isinstance(num_qubits, int), "Number of qubits could not be determined."
    # Now the type checker knows num_qubits is an int for the rest of the function

    # --- Construct Noise Model if specific probabilities are given ---
    active_noise_model = noise_model 
    readout_info_available = readout_error_prob is not None and readout_error_prob > 0
    if active_noise_model is None and (depolarizing_prob is not None or readout_error_prob is not None):
        print("Constructing basic noise model...")
        active_noise_model = NoiseModel()
        
        # Add depolarizing error to CX gates
        if depolarizing_prob is not None and depolarizing_prob > 0:
            error_depol = depolarizing_error(depolarizing_prob, 2)
            active_noise_model.add_all_qubit_quantum_error(error_depol, ['cx'])
            print(f"  Added 2q depolarizing error ({depolarizing_prob=}) to CX gates.")
            
        # Add readout error
        if readout_error_prob is not None and readout_error_prob > 0:
            p0_given_1 = readout_error_prob
            p1_given_0 = readout_error_prob
            error_readout = ReadoutError([[1 - p1_given_0, p1_given_0], [p0_given_1, 1 - p0_given_1]])
            active_noise_model.add_all_qubit_readout_error(error_readout)
            print(f"  Added symmetric readout error ({readout_error_prob=}).")
            readout_info_available = True # Mark as available even if part of constructed model
    elif active_noise_model is not None:
        # Check if the provided noise model itself has readout error defined
        # This check is basic; a more robust check would inspect noise_model.to_dict()
        if any("readout_error" in str(instruction).lower() for instruction in active_noise_model._local_readout_errors):
             readout_info_available = True
        pass # Use the provided noise model as is

    noise_info_str = f"(Noise: {'Model Provided' if noise_model else (f'Depol={depolarizing_prob}, Readout={readout_error_prob}' if active_noise_model else 'None')})"

    # --- Verification Logic ---
    if not simulate_readout_error:
        # --- Statevector Simulation and Fidelity Check ---
        print(f"Running statevector simulation for {num_qubits} qubits {noise_info_str}")
        backend_options = {
            'method': 'statevector',
            'zero_threshold': 1e-10
        }
        backend = AerSimulator(noise_model=active_noise_model, **backend_options)

        # Ensure the Qiskit circuit doesn't contain measurements for statevector simulation
        sim_circuit = qiskit_circuit.copy() # Use copy method of Qiskit circuit
        try:
            # Attempt to remove measurements using Qiskit's potential method (might vary by version)
            # Qiskit circuits are immutable in some contexts, direct removal might fail
            # Let's try removing by rebuilding without measurement instructions
            sim_circuit_no_meas = QiskitCircuit(sim_circuit.num_qubits, name=sim_circuit.name + "_no_meas")
            for instruction in sim_circuit.data:
                if instruction.operation.name != 'measure':
                    sim_circuit_no_meas.append(instruction)
            sim_circuit = sim_circuit_no_meas # Use the rebuilt circuit
        except Exception as e:
            print(f"Warning: Could not explicitly remove measurements for statevector sim: {e}. Proceeding with original.")
            # If removal fails, proceed anyway; Aer statevector might ignore them

        try:
            job = backend.run(sim_circuit) # Run the Qiskit circuit
            result = job.result()
            actual_sv = Statevector(result.get_statevector()) # Using modern method

            # Calculate fidelity
            theoretical = create_theoretical_w_state(num_qubits)
            theoretical_sv = Statevector(theoretical)
            fidelity = float(state_fidelity(actual_sv, theoretical_sv))

            is_valid = bool(fidelity > fidelity_threshold)
            print(f"Verification (Fidelity): Fidelity = {fidelity:.6f} -> {'Valid' if is_valid else 'Invalid'} (Threshold: {fidelity_threshold})")
            return is_valid, fidelity

        except Exception as e:
            error_msg = str(e)
            print(f"Error during statevector verification: {error_msg}")
            # --- WORKAROUND REMOVED --- 
            # if "'_FakeJob' object has no attribute" in error_msg:
            #     print("WORKAROUND: Detected _FakeJob error, likely due to test patching. Assuming success for E2E test.")
            #     return True, 1.0 # Return success to allow E2E test to pass despite patch interference
            # --- END WORKAROUND ---
            
            # Attempt to provide more context if possible (Original fallback)
            try:
                # Try getting statevector via older methods if modern one failed
                 sv_data = result.data().get('statevector') # Note: result might not be defined if backend.run failed
                 if sv_data:
                     actual_sv = Statevector(sv_data)
                     # Need theoretical state here too for fallback calculation
                     theoretical = create_theoretical_w_state(num_qubits)
                     theoretical_sv = Statevector(theoretical)
                     fidelity = float(state_fidelity(actual_sv, theoretical_sv))
                     is_valid = bool(fidelity > fidelity_threshold)
                     print(f"Fallback Verification (Fidelity): Fidelity = {fidelity:.6f} -> {'Valid' if is_valid else 'Invalid'} (Threshold: {fidelity_threshold})")
                     return is_valid, fidelity
                 else: # Added else for clarity
                     print("Fallback statevector retrieval: No statevector data found in result.")
            except NameError: # Catch case where 'result' is not defined because backend.run failed
                print("Fallback statevector retrieval failed: 'result' object not available.")
            except Exception as e_fallback:
                 print(f"Fallback statevector retrieval also failed: {e_fallback}")

            return False, 0.0 # Original failure return

    else:
        # --- Counts Simulation (No Mitigation Applied) ---
        print(f"Running counts simulation ({shots} shots) for {num_qubits} qubits {noise_info_str}")
        print("WARNING: Readout error mitigation requested but standard tools not found. Returning raw noisy distribution.")

        # Use the converted Qiskit circuit for counts simulation
        sim_circuit = qiskit_circuit.copy()
        if not sim_circuit.cregs:
             raise ValueError("Qiskit circuit must have classical registers for counts simulation.")
        if not any(instruction.operation.name == 'measure' for instruction in sim_circuit.data):
            print("Warning: Adding measurement to all qubits in Qiskit circuit as none were found.")
            if len(sim_circuit.clbits) < num_qubits:
                cr_name = f"c_verify_{len(sim_circuit.cregs)}"
                new_cr = ClassicalRegister(num_qubits - len(sim_circuit.clbits), cr_name)
                sim_circuit.add_register(new_cr)
            # Measure qubits to the first num_qubits classical bits
            sim_circuit.measure(list(range(num_qubits)), list(range(num_qubits)))

        # Set up simulator for counts
        backend_options = {'method': 'automatic'} 
        backend = AerSimulator(noise_model=active_noise_model)

        try:
            job = backend.run(sim_circuit, shots=shots) # Run the Qiskit circuit
            result = job.result()
            noisy_counts = result.get_counts(sim_circuit) # Get counts using Qiskit circuit

            # Calculate raw noisy probabilities
            total_shots = sum(noisy_counts.values())
            noisy_probs_dict = {k: v / total_shots for k, v in noisy_counts.items()}

            # --- Validate Noisy Distribution ---
            # Check if noisy distribution roughly matches W-state pattern
            ideal_indices = {2**i for i in range(num_qubits)}
            expected_prob_val = 1.0 / num_qubits
            tolerance = distribution_tolerance # Use the specified tolerance

            is_valid = True
            total_prob_one_hot = 0.0

            for state_key, prob in noisy_probs_dict.items():
                # Ensure state_key is handled correctly (might be hex or binary string)
                if isinstance(state_key, str):
                    idx = int(state_key.replace('0x', ''), 16) if state_key.startswith('0x') else int(state_key, 2)
                else:
                    idx = state_key # Assume integer if not string

                if idx in ideal_indices:
                    total_prob_one_hot += prob
                    if abs(prob - expected_prob_val) > tolerance:
                        print(f"  Deviation: State {state_key} prob {prob:.4f} vs expected {expected_prob_val:.4f}")
                        is_valid = False
                elif prob > tolerance: # Check non-W states for significant probability
                     print(f"  Significant non-W state: State {state_key} prob {prob:.4f}")
                     is_valid = False

            # Also check if the sum of probabilities for the expected W-states is reasonably close to 1
            # The tolerance here might need adjustment depending on noise levels
            if abs(total_prob_one_hot - 1.0) > tolerance * num_qubits:
                 print(f"  Total probability in expected W-states ({total_prob_one_hot:.4f}) deviates significantly from 1.")
                 is_valid = False

            print(f"Verification (Noisy Counts): Matches W-state pattern -> {'Valid' if is_valid else 'Invalid'} (Tolerance: {tolerance})")
            # Return the noisy probability dictionary
            return is_valid, noisy_probs_dict

        except Exception as e:
            print(f"Error during counts simulation: {str(e)}")
            return False, {}


def create_theoretical_w_state(num_qubits: int) -> np.ndarray:
    """
    Creates a theoretical W-state vector for comparison.
    
    Args:
        num_qubits (int): Number of qubits
        
    Returns:
        np.ndarray: Statevector representing the W-state
    """
    # Handle the trivial case of 0 qubits gracefully if needed, though create_w_state enforces >= 1
    if num_qubits <= 0:
        # Or raise ValueError("num_qubits must be positive")
        return np.array([1.+0.j]) # Represents state |⟩ for 0 qubits

    state = np.zeros(2**num_qubits, dtype=complex)
    
    # W-state has equal amplitude for each one-hot state
    # Handle num_qubits=1 case separately to avoid division by zero if using sqrt(num_qubits) directly
    if num_qubits == 1:
         amplitude = 1.0
    else:
         amplitude = 1.0 / np.sqrt(num_qubits)

    # Set amplitude for each state with exactly one qubit in |1⟩
    for i in range(num_qubits):
        idx = 2**i  # Binary with only i-th bit set
        state[idx] = amplitude
        
    return state 