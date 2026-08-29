import marimo

__generated_with = "0.23.14"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Import Dependencies
    """)
    return


@app.cell
def _():
    import os
    import numpy as np
    import marimo as mo
    import matplotlib.pyplot as plt

    from dotenv import load_dotenv
    from IPython.display import display

    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Statevector
    from qiskit.visualization import plot_histogram, plot_bloch_multivector

    load_dotenv()
    token = os.getenv("IBM_QUANTUM_API_KEY")
    instance = os.getenv("IBM_QUANTUM_INSTANCE")
    return QuantumCircuit, Statevector, display, mo, plot_bloch_multivector


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Lab 1 Review: Building Quantum Circuits for Real Hardware
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Basic Gates and Quantum Concepts

    - Quantum computation works by manipulating **qubits** with the use of gates, these qubits initially start with a value of $\ket{0}$.
    - We are introduced to three basic gates: $X$, $H$, and $CX$.
    - We can show a state in *two* ways:
        1. **State Vector** - The LaTeX form, where each term is an amplitude multiplying a basis state like $\ket{0}$.
        2. **Bloch Sphere** - A geometrical representation of the pure state space of a two-level quantum mechanical system (qubit).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1.1. The $X$ Gate
    The $X$ gate is a *single-qubit* gate that flips the state of a qubit. It is the quantum version of the classical NOT gate. Geometrically, $X$ is a rotation by $\pi$ (180°) around the X-axis of the Bloch sphere. Its matrix is:

    $$
    X = \begin{pmatrix}0 & 1 \\ 1 & 0 \end{pmatrix}
    $$

    ---

    $$
    X\ket{0} =
    \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}
    \begin{pmatrix}1 \\ 0 \end{pmatrix} =
    \begin{pmatrix} 0 \\ 1 \end{pmatrix} =
    \ket{1}
    $$
    """)
    return


@app.cell
def _(QuantumCircuit, Statevector, display, plot_bloch_multivector):
    x_qc = QuantumCircuit(1)
    x_qc.x(0)
    x_sv = Statevector(x_qc)

    display(x_qc.draw("mpl"))
    display(x_sv.draw("latex"))
    display(plot_bloch_multivector(x_sv))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1.2. The $H$ Gate

    This gate places a qubit in a state of **superposition**, where it can partly be in $\ket{0}$ and $\ket{1}$ states. Upon measuring a qubit in this state, will yield a $\ket{0}$ or $\ket{1}$ each with a probability of 50%. It is also a *single-qubit* gate. Its matrix is:

    $$
    \frac{1}{\sqrt2}
    \begin{pmatrix}
    1 & 1 \\ 1 & -1
    \end{pmatrix}
    $$
    ---
    $$
    H\ket{0} =
    \frac{1}{\sqrt2}\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}
    \begin{pmatrix} 1 \\ 0 \end{pmatrix} =
    \begin{pmatrix}
    \frac{1}{\sqrt2} & \frac{1}{\sqrt2} \\
    \frac{1}{\sqrt2} & -\frac{1}{\sqrt2}
    \end{pmatrix}
    \begin{pmatrix} 1 \\ 0 \end{pmatrix} =
    \begin{pmatrix} \frac{1}{2} \\ \frac{1}{2} \end{pmatrix}
    $$
    """)
    return


@app.cell
def _(QuantumCircuit, Statevector, display, plot_bloch_multivector):
    h_qc = QuantumCircuit(1)
    h_qc.h(0)
    h_sv = Statevector(h_qc)

    display(h_qc.draw("mpl"))
    display(h_sv.draw("latex"))
    display(plot_bloch_multivector(h_sv))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1.3. The $CX$ Gate

    The $CX$ gate is a two-qubit gate. It functions in the same as $X$ that it flips the state of a **target** qubit except that it will only do so when the **control** qubit is $\ket{1}$. When the control qubit is in superposition, the two qubits become **entangled**.

    Typically the permutation matrix for this gate is:

    $$
    CX =
    \begin{pmatrix}
    1 & 0 & 0 & 0 \\
    0 & 1 & 0 & 0 \\
    0 & 0 & 0 & 1 \\
    0 & 0 & 1 & 0
    \end{pmatrix}
    $$

    where each colum corresponds to the four basis states: $\ket{00}$, $\ket{01}$, $\ket{11}$, and $\ket{10}$ respectively.

    However, the Qiskit ordering for two qubits is $\ket{q_1q_0}$. So the permutation matrix that takes into account this ordering has to be built from the truth table directly:

    $q_0 \rightarrow \text{control},\hspace{0.5em} q_1 \rightarrow \text{target}$

    |Basis|After $CX$|
    |-|-|
    |$\ket{00}$|$\ket{00}$|
    |$\ket{01}$|$\ket{11}$|
    |$\ket{10}$|$\ket{10}$|
    |$\ket{11}$|$\ket{01}$|

    $$
    CX =
    \begin{pmatrix}
    1 & 0 & 0 & 0 \\
    0 & 0 & 0 & 1 \\
    0 & 0 & 1 & 0 \\
    0 & 1 & 0 & 0
    \end{pmatrix}
    $$
    ---
    $$
    q_0 = \ket{0}, \hspace{0.5em} q_1 = \ket{0}
    $$

    $$
    Hq_0 = H\ket{0} = \frac{1}{\sqrt2}(\ket{0} + \ket{1})
    $$

    $$
    \ket{q_1q_0} = \frac{1}{\sqrt2}(\ket{00} + \ket{01})
    $$

    $$
    CX\ket{q_1q_0} = \frac{1}{\sqrt2}(CX\ket{00} + CX\ket{01})
    $$

    $$
    \ket{q_1q_0}= \frac{1}{\sqrt2}(\ket{00} + \ket{11})
    $$
    """)
    return


@app.cell
def _(QuantumCircuit, Statevector, display):
    cx_qc = QuantumCircuit(2)
    cx_qc.h(0)
    cx_qc.cx(0, 1)

    cx_sv = Statevector(cx_qc)

    display(cx_qc.draw("mpl"))
    display(cx_sv.draw("latex"))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### The Bell State

    The state we just created is $\frac{1}{\sqrt2}(\ket{00} + \ket{11}$. What does this mean?

    - If we measure both qubits, we get either $\ket{00}$ or $\ket{11}$ each with 50% probability.
    - We never get $\ket{01}$ or $\ket{10}$. The qubits are perfectly correlated.
    - This correlation persists no matter how far apart the qubits are. This is **entanglement**, and it's the key resource that makes quantum computing powerful.
    """)
    return


@app.cell
def _(QuantumCircuit, Statevector, display):
    # Creating all 4 Bell States

    b1_qc = QuantumCircuit(2)
    b1_qc.h(0)
    b1_qc.cx(0, 1)

    b2_qc = QuantumCircuit(2)
    b2_qc.x(1)
    b2_qc.h(0)
    b2_qc.cx(0, 1)

    b3_qc = QuantumCircuit(2)
    b3_qc.x(0)
    b3_qc.h(0)
    b3_qc.cx(0, 1)

    b4_qc = QuantumCircuit(2)
    b4_qc.x(0)
    b4_qc.x(1)
    b4_qc.h(0)
    b4_qc.cx(0, 1)

    b1_sv = Statevector(b1_qc)
    b2_sv = Statevector(b2_qc)
    b3_sv = Statevector(b3_qc)
    b4_sv = Statevector(b4_qc)

    display(b1_sv.draw("latex"))
    display(b2_sv.draw("latex"))
    display(b3_sv.draw("latex"))
    display(b4_sv.draw("latex"))
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
