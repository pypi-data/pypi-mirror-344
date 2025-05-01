import timeit
import numpy as np
import pandas as pd
from qiskit import QuantumCircuit
from qiskit.circuit.library import CXGate
from src.quantum_finance.quantum_toolkit.circuits.w_state_consolidated import create_w_state

def benchmark_w_state_creation(min_qubits: int = 1, max_qubits: int = 10, repeats: int = 5, number: int = 10):
    """
    Benchmarks the create_w_state function for various qubit counts.

    Measures execution time, circuit depth, and CNOT count.

    Args:
        min_qubits (int): Minimum number of qubits to test.
        max_qubits (int): Maximum number of qubits to test.
        repeats (int): Number of times to repeat the timing measurement.
        number (int): Number of times to execute the function within each repeat.

    Returns:
        pd.DataFrame: DataFrame containing benchmark results.
                     Columns: ['Num Qubits', 'Avg Time (s)', 'Std Dev Time (s)', 
                               'Depth', 'CNOT Count']
    """
    results = []
    print(f"Benchmarking W-state creation from {min_qubits} to {max_qubits} qubits...")
    print(f"Timing parameters: repeats={repeats}, number={number}")

    for n_qubits in range(min_qubits, max_qubits + 1):
        # --- Time the circuit creation ---
        # Using timeit for more stable timing measurements
        timer = timeit.Timer(lambda: create_w_state(n_qubits), 
                             setup=f"from src.quantum_finance.quantum_toolkit.circuits.w_state_consolidated import create_w_state")
        
        try:
            # The repeat function returns a list of times for each repeat
            times = timer.repeat(repeat=repeats, number=number)
            # Calculate average and standard deviation, dividing by 'number' to get time per single execution
            avg_time = np.mean(times) / number
            std_dev_time = np.std(times) / number
        except Exception as e:
            print(f"Error timing {n_qubits} qubits: {e}")
            avg_time = np.nan
            std_dev_time = np.nan

        # --- Analyze the circuit structure (depth, CNOTs) ---
        # Create one instance to analyze
        circuit_depth = np.nan
        cnot_count = np.nan
        try:
            qc = create_w_state(n_qubits)
            circuit_depth = qc.depth()
            # Count CNOT gates by iterating through circuit data
            cnot_count = 0
            for instruction in qc.data:
                if isinstance(instruction.operation, CXGate):
                    cnot_count += 1
        except Exception as e:
            print(f"Error analyzing circuit for {n_qubits} qubits: {e}")
            
        # --- Store results ---
        results.append({
            'Num Qubits': n_qubits,
            'Avg Time (s)': avg_time,
            'Std Dev Time (s)': std_dev_time,
            'Depth': circuit_depth,
            'CNOT Count': cnot_count
        })
        print(f"  {n_qubits} qubits: Avg Time={avg_time:.6f}s (+/- {std_dev_time:.6f}s), Depth={circuit_depth}, CNOTs={cnot_count}")

    print("Benchmarking complete.")
    return pd.DataFrame(results)

if __name__ == "__main__":
    # --- Configuration ---
    MIN_QUBITS = 1
    MAX_QUBITS = 12  # Adjust as needed based on performance
    REPEATS = 5      # Number of timing repetitions
    NUMBER = 10      # Executions per repetition

    # --- Run Benchmark ---
    benchmark_results_df = benchmark_w_state_creation(
        min_qubits=MIN_QUBITS, 
        max_qubits=MAX_QUBITS, 
        repeats=REPEATS, 
        number=NUMBER
    )

    # --- Display Results ---
    print("\\n--- Benchmark Results ---")
    # Optional: Nicer formatting if pandas is available
    try:
        # Set display options for better readability
        pd.set_option('display.float_format', '{:.6f}'.format) 
        pd.set_option('display.max_rows', None) # Show all rows
        print(benchmark_results_df.to_string(index=False))
    except ImportError:
        print("Pandas not found. Printing basic results:")
        for record in benchmark_results_df.to_dict('records'):
             print(record)

    # --- Optional: Save Results ---
    # output_file = "w_state_benchmark_results.csv"
    # benchmark_results_df.to_csv(output_file, index=False)
    # print(f"\nResults saved to {output_file}") 