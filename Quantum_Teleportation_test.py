from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, execute
from qiskit.visualization import plot_histogram
import numpy as np

def arbitrary_state(theta, phi):
    return [np.cos(theta/2), np.exp(1j*phi)*np.sin(theta/2)]

def quantum_teleportation(psi):
    # Create quantum registers
    qr = QuantumRegister(3, 'q')  # 3 qubits: psi (message), Alice's qubit, Bob's qubit
    crz = ClassicalRegister(1, 'crz')  # Classical register for Z basis measurement
    crx = ClassicalRegister(1, 'crx')  # Classical register for X basis measurement
    cr_result = ClassicalRegister(1, 'cr_result')  # Classical register for the final result
    qc = QuantumCircuit(qr, crz, crx, cr_result)
    
    # Prepare the message qubit (psi)
    qc.initialize(psi, 0)
    
    # Create entangled Bell pair between Alice and Bob
    qc.h(1)
    qc.cx(1, 2)
    
    # Perform Bell measurement on psi and Alice's qubit
    qc.cx(0, 1)
    qc.h(0)
    qc.measure(0, crz)
    qc.measure(1, crx)
    
    # Apply correction operations on Bob's qubit based on measurement outcome
    qc.x(2).c_if(crx, 1)
    qc.z(2).c_if(crz, 1)

    # Measure Bob's qubit
    qc.measure(2, cr_result)
    
    return qc

# Define the message qubit state, for example, a superposition state (|0> + |1>)/sqrt(2)
theta = np.pi / 2
phi = 0
psi = arbitrary_state(theta, phi)

# Perform quantum teleportation
qc = quantum_teleportation(psi)

# Visualize the quantum circuit
print(qc.draw())

# Simulate the circuit
simulator = Aer.get_backend('qasm_simulator')
result = execute(qc, backend=simulator, shots=1024).result()
counts = result.get_counts(qc)

# Print the result
print(counts)

# Plot the histogram
plot_histogram(counts)

# Calculate the success rate
success_count = 0
for key, value in counts.items():
    if (key[-1] == '0' and np.isclose(np.abs(psi[0])**2, 1)) or (key[-1] == '1' and np.isclose(np.abs(psi[1])**2, 1)):
        success_count += value

success_count = 0
for key, value in counts.items():
    if (key[-1] == '0' and np.isclose(np.abs(psi[0])**2, 1)) or (key[-1] == '1' and np.isclose(np.abs(psi[1])**2, 1)):
        success_count += value
    if (key[-1] == '0' and np.isclose(np.abs(psi[0])**2, 0.5)) or (key[-1] == '1' and np.isclose(np.abs(psi[1])**2, 0.5)):
        success_count += value / 2

success_rate = success_count / 1024
print(f"Success rate: {success_rate * 100}%")