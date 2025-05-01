from qiskit.circuit import QuantumCircuit  # Core circuit class
from qiskit import transpile  # Qiskit transpiler for circuit optimization
from qiskit.circuit.library import QFT  # Quantum Fourier Transform library circuit
from qiskit_aer import AerSimulator  # Aer simulator backend
# Import standard primitive interface
from qiskit_aer.primitives import Sampler as LocalSampler  # Local sampler primitive
from qiskit_ibm_runtime import QiskitRuntimeService, Session, Options, Sampler  # IBM Quantum runtime primitives
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_bell_state():
    """
    Creates a Bell state quantum circuit.
    
    Returns:
        QuantumCircuit: Quantum circuit representing the Bell state.
    """
    # Create a quantum circuit with 2 qubits and 2 classical bits for measurement
    qc = QuantumCircuit(2, 2)
    
    # Apply Hadamard gate to the first qubit to create superposition
    qc.h(0)
    
    # Apply CNOT gate with control qubit 0 and target qubit 1 to entangle qubits
    qc.cx(0, 1)
    
    # Measure both qubits to collapse the state
    qc.measure([0, 1], [0, 1])
    
    return qc

def quantum_fourier_transform(n_qubits):
    """
    Creates a Quantum Fourier Transform circuit.
    
    Args:
        n_qubits (int): Number of qubits for the QFT
        
    Returns:
        QuantumCircuit: QFT circuit
    """
    qc = QFT(n_qubits)
    # Add measurement to all qubits
    cr = QuantumCircuit(n_qubits, n_qubits)
    cr.measure_all()
    return qc.compose(cr)

def run_qft_simulation(n_qubits, shots=1000):
    """
    Executes a Quantum Fourier Transform (QFT) simulation.
    
    Args:
        n_qubits (int): Number of qubits in the QFT circuit.
        shots (int): Number of simulation runs.
    
    Returns:
        dict: Measurement counts from the QFT simulation.
    """
    qft_circuit = quantum_fourier_transform(n_qubits)
    
    if qft_circuit is None:
        logger.error("Failed to create QFT circuit")
        return {}
    
    # Use Aer's simulator backend
    simulator = AerSimulator()
    
    # Transpile the circuit for the simulator
    transpiled_circuit = transpile(qft_circuit, simulator)
    
    # Execute the QFT circuit - using updated API pattern
    job = simulator.run(transpiled_circuit, shots=shots)
    result = job.result()
    
    # Return the measurement counts - in Qiskit 1.0+ we don't need to pass the circuit
    return result.get_counts()

if __name__ == "__main__":
    # Create and run a Bell state circuit
    bell_state_circuit = create_bell_state()
    
    # Use Aer's simulator backend for simulation
    simulator = AerSimulator()
    
    # Transpile the circuit for the simulator - recommended in Qiskit 1.0+
    transpiled_circuit = transpile(bell_state_circuit, simulator)
    
    # Execute the circuit on the simulator
    job = simulator.run(transpiled_circuit, shots=1000)
    
    # Retrieve the results of the simulation
    result = job.result()
    
    # Get the counts of measurement outcomes - in Qiskit 1.0+ we don't need to pass the circuit
    counts = result.get_counts()
    print("Measurement counts:", counts)
    
    # Note: For Qiskit 1.0+ compatibility, please refer to the Qiskit migration guide 
    # for using the newer V2 primitives like SamplerV2 and EstimatorV2