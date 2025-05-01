#!/usr/bin/env python3
"""
Script to run a simple Estimator primitive workflow and analyze results.
This demonstrates using the quantum_results_analysis module.
"""
from qiskit_ibm_runtime import Session, Estimator  # type: ignore
from qiskit_ibm_runtime.fake_provider import FakeAlmadenV2  # type: ignore
from qiskit import QuantumCircuit  # type: ignore
from qiskit.quantum_info import SparsePauliOp  # type: ignore
from qiskit.transpiler import generate_preset_pass_manager  # type: ignore
# Use absolute import without 'src' prefix - this is the proper Python package structure
# This assumes PYTHONPATH is set to include the parent directory of 'quantum_finance'
from quantum_finance.quantum_results_analysis import analyze_primitive  # type: ignore


def main():
    # Use fake provider for demonstration (no real device queue)
    backend = FakeAlmadenV2()
    
    # Build a simple Bell circuit
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    
    # Transpile circuit to hardware ISA for primitives
    pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
    isa_qc = pm.run(qc)
    
    # Map observables to the transpiled circuit layout
    orig_patterns = ["ZI", "IZ"]
    labels = ["Z0", "Z1"]
    # Get mapping from virtual to physical qubits
    mapping = isa_qc.layout.input_qubit_mapping
    n_q = isa_qc.num_qubits
    observables = []
    for pattern in orig_patterns:
        phys_lab = ["I"] * n_q
        for virt_index, op_char in enumerate(pattern):
            virt_qubit = qc.qubits[virt_index]
            phys_index = mapping[virt_qubit]
            phys_lab[phys_index] = op_char
        phys_label_str = "".join(phys_lab)
        observables.append(SparsePauliOp.from_list([(phys_label_str, 1.0)]))
    
    # Run Estimator primitive within a runtime session and analyze
    with Session(backend=backend) as session:
        estimator = Estimator(session)  # type: ignore
        job = estimator.run([(isa_qc, observables)])
        result = job.result()
        pub_result = result[0]
    
    analysis = analyze_primitive(pub_result, labels)
    fig = analysis["figure"]
    preds = analysis["predictions"]
    
    # Save plot and print predictions
    fig.savefig("quantum_analysis_plot.png")
    print("Binary predictions:", preds)
    print("Plot saved to quantum_analysis_plot.png")


if __name__ == "__main__":
    main() 