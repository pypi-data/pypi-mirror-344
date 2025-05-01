"""
Quantum Circuit Core Module

This module provides core functionality for quantum circuit operations.
It serves as a foundational component for more specialized circuit implementations.
"""

import logging
from typing import Dict, Any, List, Optional, Union, Tuple
import numpy as np

# Configure logging
logger = logging.getLogger(__name__)

class Gate:
    """
    Base class for quantum gates.
    """
    def __init__(self, name: str, num_qubits: int = 1, params: Optional[List[float]] = None):
        """
        Initialize a quantum gate.
        
        Args:
            name: Name of the gate
            num_qubits: Number of qubits the gate acts on
            params: Optional parameters for parameterized gates
        """
        self.name = name
        self.num_qubits = num_qubits
        self.params = params or []
        
    def __str__(self) -> str:
        """String representation of the gate."""
        param_str = ""
        if self.params:
            param_str = f"({', '.join(str(p) for p in self.params)})"
        return f"{self.name}{param_str}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the gate to a dictionary representation."""
        return {
            "name": self.name,
            "num_qubits": self.num_qubits,
            "params": self.params
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Gate':
        """Create a gate from a dictionary representation."""
        return cls(
            name=data["name"],
            num_qubits=data["num_qubits"],
            params=data.get("params", [])
        )


class CircuitBase:
    """
    Base class for quantum circuits in the core module.
    """
    def __init__(self, n_qubits: Optional[int] = None, num_qubits: Optional[int] = None, name: str = "base_circuit") -> None:
        """
        Initialize a base circuit.
        
        Args:
            n_qubits: Legacy parameter for number of qubits
            num_qubits: Preferred parameter for number of qubits
            name: Name of the circuit
        """
        # Determine qubit count, supporting both legacy and new alias
        qubit_count = num_qubits if num_qubits is not None else (n_qubits if n_qubits is not None else 3)
        self.n_qubits = qubit_count
        self.num_qubits = qubit_count  # alias for backward compatibility in tests
        self.name = name
        self.gates = []
        logger.debug(f"Created CircuitBase with {self.num_qubits} qubits, name: {name}")
    
    def add_gate(self, gate_type: str, target: Union[int, List[int]], **params) -> None:
        """
        Add a gate to the circuit.
        
        Args:
            gate_type: Type of gate to add
            target: Target qubit(s)
            params: Additional parameters for the gate
        """
        self.gates.append({
            "type": gate_type,
            "target": target,
            "params": params
        })
        logger.debug(f"Added {gate_type} gate to circuit {self.name}")
    
    def simulate(self) -> Dict[str, Any]:
        """
        Simulate the circuit.
        
        Returns:
            Dictionary containing simulation results
        """
        logger.info(f"Simulating circuit {self.name} with {self.n_qubits} qubits and {len(self.gates)} gates")
        # This is just a placeholder implementation
        return {
            "success": True,
            "circuit_name": self.name,
            "n_qubits": self.n_qubits,
            "n_gates": len(self.gates),
            "results": {"00": 0.5, "11": 0.5}  # Placeholder results
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the circuit to a dictionary.
        
        Returns:
            Dictionary representation of the circuit
        """
        return {
            "name": self.name,
            "n_qubits": self.n_qubits,
            "gates": self.gates
        }


class QuantumCircuit(CircuitBase):
    """
    Quantum circuit implementation compatible with the framework.
    This is a simplified version of a quantum circuit for testing purposes.
    """
    def __init__(self, n_qubits: Optional[int] = None, num_qubits: Optional[int] = None, name: str = "quantum_circuit") -> None:
        """
        Initialize a quantum circuit.
        
        Args:
            n_qubits: Legacy parameter for number of qubits
            num_qubits: Preferred parameter for number of qubits
            name: Name of the circuit
        """
        super().__init__(n_qubits=n_qubits, num_qubits=num_qubits, name=name)
        self.measurements = {}
        # Track classical bits count for simulation tasks
        self.num_clbits = 0
        logger.debug(f"Created QuantumCircuit with {self.num_qubits} qubits, name: {name}")
    
    def h(self, qubit: int) -> 'QuantumCircuit':
        """
        Add a Hadamard gate to the circuit.
        
        Args:
            qubit: Target qubit
            
        Returns:
            Self for method chaining
        """
        self.add_gate("h", qubit)
        return self
    
    def x(self, qubit: int) -> 'QuantumCircuit':
        """
        Add an X gate to the circuit.
        
        Args:
            qubit: Target qubit
            
        Returns:
            Self for method chaining
        """
        self.add_gate("x", qubit)
        return self
    
    def cx(self, control: int, target: int) -> 'QuantumCircuit':
        """
        Add a CNOT gate to the circuit.
        
        Args:
            control: Control qubit
            target: Target qubit
            
        Returns:
            Self for method chaining
        """
        self.add_gate("cx", [control, target])
        return self
    
    def measure(self, qubit: int, cbit: int = -1) -> 'QuantumCircuit':
        """
        Add a measurement operation to the circuit.
        
        Args:
            qubit: Qubit to measure
            cbit: Classical bit to store the result (defaults to same as qubit if -1)
            
        Returns:
            Self for method chaining
        """
        if cbit == -1:
            cbit = qubit
        self.add_gate("measure", qubit, cbit=cbit)
        # Update classical bits count
        self.num_clbits = max(self.num_clbits, cbit + 1)
        return self
    
    def measure_all(self) -> 'QuantumCircuit':
        """
        Add measurement operations for all qubits.
        
        Returns:
            Self for method chaining
        """
        # Measure all qubits by index
        for i in range(self.num_qubits):
            self.measure(i, i)
        return self

    # Add T gate for phase operations
    def t(self, qubit: int) -> 'QuantumCircuit':
        """
        Add a T gate to the circuit.
        """
        self.add_gate("t", qubit)
        return self

    # Add S gate for phase operations
    def s(self, qubit: int) -> 'QuantumCircuit':
        """
        Add an S gate to the circuit.
        """
        self.add_gate("s", qubit)
        return self

    # Add Z gate for phase flip operations
    def z(self, qubit: int) -> 'QuantumCircuit':
        """
        Add a Z gate to the circuit.
        """
        self.add_gate("z", qubit)
        return self

    def to_qiskit(self):
        """
        Convert this custom circuit representation to a standard qiskit.QuantumCircuit.

        Returns:
            qiskit.QuantumCircuit: The equivalent Qiskit circuit object, or None if Qiskit is not available.
        """
        try:
            from qiskit import QuantumCircuit as _QiskitQuantumCircuit
        except ImportError:
            logger.warning("Qiskit not installed. Cannot convert to Qiskit QuantumCircuit.")
            return None

        # Create a Qiskit circuit. Use num_clbits if measurements are defined, else just qubits.
        qiskit_circ = _QiskitQuantumCircuit(self.num_qubits, self.num_clbits if self.num_clbits > 0 else self.num_qubits, name=self.name)

        # Apply gates from the custom circuit's gate list
        for gate in self.gates:
            typ = gate.get('type')
            tgt = gate.get('target')
            params = gate.get('params', {}) # Get gate parameters

            if typ == 'h':
                qiskit_circ.h(tgt)
            elif typ == 'x':
                qiskit_circ.x(tgt)
            elif typ == 'cx':
                # Ensure target is a list/tuple for CX
                if isinstance(tgt, list) and len(tgt) == 2:
                    qiskit_circ.cx(tgt[0], tgt[1])
                else:
                    logger.warning(f"Skipping CX gate with invalid target format: {tgt}")
            elif typ == 't':
                qiskit_circ.t(tgt)
            elif typ == 's':
                qiskit_circ.s(tgt)
            elif typ == 'z':
                qiskit_circ.z(tgt)
            elif typ == 'measure':
                # Apply measurement if specified
                cbit = params.get('cbit')
                if cbit is not None:
                    qiskit_circ.measure(tgt, cbit)
                else:
                    # Default measure qubit to its corresponding classical bit index if not specified
                    qiskit_circ.measure(tgt, tgt)
            else:
                # Attempt to apply any other gate by name dynamically
                # This requires the gate name in our list to match a method in qiskit.QuantumCircuit
                fn = getattr(qiskit_circ, typ, None)
                if callable(fn):
                    if isinstance(tgt, list):
                        fn(*tgt) # Unpack target list as arguments
                    else:
                        fn(tgt)  # Single target qubit
                else:
                    logger.warning(f"Unsupported or unknown gate type '{typ}' encountered during Qiskit conversion.")
                    # Optionally raise an error or skip

        return qiskit_circ


def create_circuit(circuit_type: str, n_qubits: int = 3, **params) -> CircuitBase:
    """
    Factory function to create a circuit of the specified type.
    
    Args:
        circuit_type: Type of circuit to create
        n_qubits: Number of qubits in the circuit
        params: Additional parameters for the circuit
        
    Returns:
        A CircuitBase instance (or subclass)
    """
    logger.info(f"Creating circuit of type {circuit_type} with {n_qubits} qubits")
    circuit = CircuitBase(n_qubits=n_qubits, name=f"{circuit_type}_circuit")
    
    # Add some basic gates based on the circuit type
    if circuit_type == "bell_state":
        circuit.add_gate("h", 0)
        circuit.add_gate("cx", [0, 1])
    elif circuit_type == "ghz_state":
        circuit.add_gate("h", 0)
        for i in range(1, n_qubits):
            circuit.add_gate("cx", [0, i])
    
    return circuit 