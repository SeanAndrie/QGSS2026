import marimo

__generated_with = "0.23.14"
app = marimo.App(width="full")


@app.cell
def _():
    import os
    import marimo as mo
    from dotenv import load_dotenv

    load_dotenv()
    token = os.getenv("IBM_QUANTUM_API_KEY")
    instance = os.getenv("IBM_QUANTUM_INSTANCE")
    return instance, mo, token


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Lab 1: Building Quantum Circuits for Real Hardware

    ## Qiskit Global Summer School 2026

    Welcome to Lab 1! In this notebook you will learn how to build quantum circuits from the ground up and prepare them for execution on real quantum hardware.

    **What you'll learn:**

    1. [**Part 1: Basic Gates & Quantum Concepts**](#part1): How X, H, and CX gates create superposition and entanglement
    2. [**Part 2: Circuit Depth**](#part2): Why depth matters, GHZ states, and how to reduce depth using symmetry
    3. [**Part 3: Transpilation**](#part3): Adapting circuits to the constraints of a real processor (the 133-qubit IBM Heron chip)
    4. [**Part 4: Running on a Noisy Simulator**](#part4): Executing circuits on a noisy simulator and comparing results

    Each part builds on the last, and by the end you'll be constructing efficient 64-qubit entangled states for real hardware, skills that carry directly into Lab 2.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Before you begin

    > **This lab runs entirely on a local *simulator* (`FakeTorino`).** You will **not** consume any IBM Quantum runtime minutes here — every circuit is transpiled and executed locally. (We show how to point at a real backend at the very end of Part 4.) Submitting your answers to the grader *does* require a configured IBM Quantum account; see the account-setup cell just below the imports if a grade cell reports an authentication error.

    <details>
    <summary><b>Common setup issues (click to expand)</b></summary>

    - **Figures not showing up?** If you're in **VS Code** and a plot prints as text instead of rendering, re-run the cell — this notebook calls `display(...)` explicitly so figures show across Jupyter, JupyterLab, VS Code, Colab, and qBraid.
    - **`jupyter notebook` not found?** You may have **JupyterLab** installed instead of the classic Notebook — launch with `jupyter lab`.
    - **Graphviz error on a topology/gate-map plot?** Install Graphviz (`conda install -c conda-forge python-graphviz`, or your OS package manager). The topology plots in this lab use `networkx` + `matplotlib`, so most users won't need it.
    - **`pip` installing into the wrong environment?** Use the `%pip` magic (as in the install cell below) rather than `!pip` — `%pip` always targets the kernel you're running.

    </details>

    **Helpful Qiskit documentation:** [Circuits & gates](https://quantum.cloud.ibm.com/docs/api/qiskit/circuit) · [`QuantumCircuit`](https://quantum.cloud.ibm.com/docs/api/qiskit/qiskit.circuit.QuantumCircuit) · [Transpilation](https://docs.quantum.ibm.com/guides/transpile) · [`Statevector`](https://quantum.cloud.ibm.com/docs/api/qiskit/qiskit.quantum_info.Statevector)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Imports
    """)
    return


@app.cell
def _():
    # Run this cell if these packages aren't already installed in your environment.
    # (Uses the %pip magic so packages always install into the *running* kernel —
    # important on qBraid/Colab, where a plain !pip can target the wrong environment.)
    # "%pip install 'qiskit[visualization]' qiskit-ibm-runtime qiskit-aer numpy networkx" command supported automatically in marimo
    # %pip install --upgrade git+https://github.com/qiskit-community/Quantum-Challenge-Grader.git' command supported automatically in marimo
    return


@app.cell
def _():
    from IPython.display import display
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Statevector
    from qiskit.visualization import plot_histogram, plot_bloch_multivector
    import matplotlib.pyplot as plt
    import numpy as np

    print("Imports loaded successfully — you're ready to go.")
    return (
        QuantumCircuit,
        Statevector,
        display,
        np,
        plot_bloch_multivector,
        plot_histogram,
        plt,
    )


@app.cell
def _():
    from qc_grader.challenges.qgss_2026 import (
        grade_lab1_ex1,
        grade_lab1_ex2,
        grade_lab1_ex3,
        grade_lab1_ex4,
        grade_lab1_ex5,
        grade_lab1_ex6,
        grade_lab1_ex7,
    )

    return (
        grade_lab1_ex1,
        grade_lab1_ex2,
        grade_lab1_ex3,
        grade_lab1_ex4,
        grade_lab1_ex5,
        grade_lab1_ex6,
        grade_lab1_ex7,
    )


@app.cell
def _(instance, token):
    # ── (Optional) IBM Quantum account setup ──────────────────────────────────────
    # The grader checks your answers locally, but *submitting* them requires a
    # configured IBM Quantum account. A fresh Colab/qBraid session does NOT inherit
    # the account you saved in Lab 0, so if a grade cell below fails with an
    # authentication error, run the SAME save_account(...) call you used in Lab 0 —
    # for example:

    from qiskit_ibm_runtime import QiskitRuntimeService
    QiskitRuntimeService.save_account(
        channel="ibm_quantum_platform",
        token=token,
        instance=instance,
        overwrite=True,
    )

    # You only need to do this once per environment.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Part 1: Basic Gates and Quantum Concepts <a id="part1"></a>

    Quantum computation works by manipulating **qubits**, the quantum analog of classical bits. A qubit starts in the state $|0\rangle$ and we transform it using **quantum gates**. Let's meet the three most important single- and two-qubit gates.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### The X Gate (bit-flip)

    The X gate flips a qubit's state: $|0\rangle \to |1\rangle$ and $|1\rangle \to |0\rangle$. It's the quantum version of a classical NOT gate.

    Geometrically, X is a rotation by $\pi$ (180°) around the X-axis of the Bloch sphere. Its matrix is:

    $$X = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$$

    > **Reading the output below:** we show each state two ways — as a state *vector* (the LaTeX form, where each term is an amplitude multiplying a basis state like $|0\rangle$) and on the **Bloch sphere** (a geometric picture of a single qubit). A basis state's measurement probability is the squared magnitude of its amplitude.
    """)
    return


@app.cell
def _(QuantumCircuit, Statevector, display, plot_bloch_multivector):
    # Build a circuit that applies an X gate to a single qubit
    qc = QuantumCircuit(1)
    qc.x(0)
    display(qc.draw('mpl'))
    _sv = Statevector(qc)
    # Inspect the resulting state: as a vector (LaTeX) and on the Bloch sphere
    display(_sv.draw('latex'))
    display(plot_bloch_multivector(_sv))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### The H Gate (superposition)

    The Hadamard gate puts a qubit into **superposition**, a state that is partly $|0\rangle$ and partly $|1\rangle$ at the same time:

    $$H|0\rangle = \frac{1}{\sqrt{2}}\bigl(|0\rangle + |1\rangle\bigr)$$

    If we measure a qubit in this state, we get $|0\rangle$ or $|1\rangle$ each with 50% probability. Like X, the H gate is a rotation, this time by $\pi$ around an axis halfway between X and Z on the Bloch sphere. Its matrix is:

    $$H = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}$$
    """)
    return


@app.cell
def _(QuantumCircuit, Statevector, display, plot_bloch_multivector):
    qc_1 = QuantumCircuit(1)
    qc_1.h(0)
    display(qc_1.draw('mpl'))
    _sv = Statevector(qc_1)
    display(_sv.draw('latex'))
    display(plot_bloch_multivector(_sv))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### The CX (CNOT) Gate and Entanglement

    The CX gate is a **two-qubit** gate. It flips the **target** qubit if and only if the **control** qubit is $|1\rangle$. When the control is in superposition, something remarkable happens: the two qubits become **entangled**. Their measurement outcomes become perfectly correlated in a way that has no classical explanation.

    Let's see this in action by creating our first **Bell state**.
    """)
    return


@app.cell
def _(QuantumCircuit, Statevector, display):
    qc_2 = QuantumCircuit(2)
    qc_2.h(0)
    qc_2.cx(0, 1)
    display(qc_2.draw('mpl'))
    _sv = Statevector(qc_2)
    display(_sv.draw('latex'))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Understanding the Bell state

    The state we just created is $\frac{1}{\sqrt{2}}\bigl(|00\rangle + |11\rangle\bigr)$. What does this mean?

    - If we measure both qubits, we get either $|00\rangle$ or $|11\rangle$, each with 50% probability.
    - We **never** get $|01\rangle$ or $|10\rangle$. The qubits are perfectly correlated.
    - This correlation persists no matter how far apart the qubits are. This is **entanglement**, and it's the key resource that makes quantum computing powerful.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 1: Build the $|01\rangle + |10\rangle$ Bell state

    We just built $\frac{1}{\sqrt{2}}\bigl(|00\rangle + |11\rangle\bigr)$. Now it's your turn!

    **Task:** Build a circuit that prepares the Bell state $\frac{1}{\sqrt{2}}\bigl(|01\rangle + |10\rangle\bigr)$.

    <details>
    <summary><b>Hint</b></summary>

    You already know how to make $|00\rangle + |11\rangle$. What single gate can you add to flip one of the qubits?
    </details>

    Docs: [`QuantumCircuit` gates](https://docs.quantum.ibm.com/api/qiskit/qiskit.circuit.QuantumCircuit) (see `.x()`, `.h()`, `.cx()`)
    """)
    return


@app.cell
def _(QuantumCircuit, Statevector, display):
    qc_3 = QuantumCircuit(2)
    qc_3.h(0)
    qc_3.cx(0, 1)
    qc_3.x(0)
    display(qc_3.draw('mpl'))
    _sv = Statevector(qc_3)
    display(_sv.draw('latex'))
    return (qc_3,)


@app.cell
def _(grade_lab1_ex1, qc_3):
    grade_lab1_ex1(qc_3)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Multiple paths to the same state

    One beautiful thing about quantum circuits is that the same state can often be prepared in different ways. There are (at least) three ways to build $|01\rangle + |10\rangle$:

    <details>
    <summary><b>Click to reveal all three solutions</b></summary>

    **Method 1:** Apply X *before* the Bell circuit:

    ```python
    qc = QuantumCircuit(2)
    qc.x(1)        # Flip qubit 1 to |1⟩ first
    qc.h(0)
    qc.cx(0, 1)
    ```

    **Method 2:** Apply X to qubit 1 *after* the Bell circuit:

    ```python
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.x(1)        # Flip qubit 1 after entangling
    ```

    **Method 3:** Apply X to qubit 0 *after* the Bell circuit:

    ```python
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.x(0)        # Flip qubit 0 after entangling
    ```

    All three produce the same state! This might seem surprising, especially Method 3, where we flip qubit 0 instead of qubit 1. But because the qubits are entangled, flipping *either* one swaps $|00\rangle \leftrightarrow |01\rangle$ and $|11\rangle \leftrightarrow |10\rangle$, giving us $|01\rangle + |10\rangle$ either way.

    This idea (that the same quantum state can be reached by different circuits) will be important when we start optimizing for real hardware.
    </details>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Optional: Relative Phase

    So far we've seen $|00\rangle + |11\rangle$ and $|01\rangle + |10\rangle$. But there are actually **four** Bell states. The other two involve a **minus sign** (a relative phase):

    $$\frac{1}{\sqrt{2}}\bigl(|00\rangle - |11\rangle\bigr) \qquad \text{and} \qquad \frac{1}{\sqrt{2}}\bigl(|01\rangle - |10\rangle\bigr)$$

    The **Z gate** introduces this phase: it leaves $|0\rangle$ unchanged but maps $|1\rangle \to -|1\rangle$.

    $$Z = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}$$

    The minus sign doesn't change measurement probabilities in the standard basis (you'd still get 50/50), but it is physically real and affects how the state interferes in further computation.
    """)
    return


@app.cell
def _(QuantumCircuit, Statevector, display):
    qc_4 = QuantumCircuit(2)
    qc_4.h(0)
    qc_4.cx(0, 1)
    qc_4.z(0)
    display(qc_4.draw('mpl'))
    _sv = Statevector(qc_4)
    display(_sv.draw('latex'))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Optional stretch exercise:** Can you build $\frac{1}{\sqrt{2}}\bigl(|01\rangle - |10\rangle\bigr)$? Combine what you learned about X and Z gates. (No solution provided. Experiment!)
    """)
    return


@app.cell
def _(QuantumCircuit, Statevector, display):
    qc_5 = QuantumCircuit(2)
    qc_5.x(1)
    qc_5.h(0)
    qc_5.cx(0, 1)
    qc_5.z(0)
    display(qc_5.draw('mpl'))
    _sv = Statevector(qc_5)
    display(_sv.draw('latex'))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Part 1 Summary

    **Learning goals achieved:**
    - **X gate**: flips $|0\rangle \leftrightarrow |1\rangle$ (bit-flip / $\pi$ rotation around X)
    - **H gate**: creates superposition $|0\rangle \to \frac{1}{\sqrt{2}}(|0\rangle + |1\rangle)$
    - **CX gate**: entangles two qubits, the key to quantum advantage
    - The same quantum state can be prepared by **multiple different circuits**
    - *Optional*: relative phase ($\pm$ signs) is physically meaningful
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Part 2: Circuit Depth <a id="part2"></a>

    On real quantum hardware, every gate introduces a small amount of error. Circuits with more layers of gates accumulate more noise and produce worse results. The number of layers is called the **circuit depth**, and reducing it is one of the most important practical skills in quantum computing.

    In this part, we'll learn what depth is, build larger entangled states, and discover how **symmetry** lets us dramatically reduce circuit depth.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### GHZ States: Entanglement at Scale

    The Bell state entangles 2 qubits. The **GHZ state** (Greenberger–Horne–Zeilinger) generalizes this to $N$ qubits:

    $$|\text{GHZ}_N\rangle = \frac{1}{\sqrt{2}}\bigl(|00\ldots0\rangle + |11\ldots1\rangle\bigr)$$

    For 3 qubits: $\frac{1}{\sqrt{2}}\bigl(|000\rangle + |111\rangle\bigr)$. When measured, all qubits agree: either all 0 or all 1.
    """)
    return


@app.cell
def _(QuantumCircuit, Statevector, display):
    qc_6 = QuantumCircuit(3)
    qc_6.h(0)
    qc_6.cx(0, 1)
    qc_6.cx(1, 2)
    display(qc_6.draw('mpl'))
    _sv = Statevector(qc_6)
    display(_sv.draw('latex'))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Two ways to build an N-qubit GHZ state

    There are (at least) two natural approaches for building a GHZ state:

    1. **Fan-out from qubit 0**: Apply H to qubit 0, then CX from qubit 0 to every other qubit: CX(0,1), CX(0,2), …, CX(0,N−1).
    2. **Chain along neighbors**: Apply H to qubit 0, then pass the entanglement along a chain: CX(0,1), CX(1,2), …, CX(N−2,N−1).

    Both produce the exact same GHZ state. Let's implement them as reusable functions.
    """)
    return


@app.cell
def _(QuantumCircuit, display):
    def ghz_fan(n):
        """GHZ via fan-out: all CX gates use qubit 0 as control."""
        qc = QuantumCircuit(n)
        qc.h(0)
        for i in range(1, n):
            qc.cx(0, i)
        return qc


    def ghz_chain(n):
        """GHZ via chain: each CX passes entanglement to the next qubit."""
        qc = QuantumCircuit(n)
        qc.h(0)
        for i in range(n - 1):
            qc.cx(i, i + 1)
        return qc


    print("Fan-out (5 qubits):")
    display(ghz_fan(5).draw("mpl"))
    print("\nChain (5 qubits):")
    display(ghz_chain(5).draw("mpl"))
    return ghz_chain, ghz_fan


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### What is Circuit Depth?

    The **depth** of a quantum circuit is the number of time steps (layers) needed to execute it, assuming we run as many gates **in parallel** as possible.

    **Rules for parallelism:**
    - Two gates can run in the **same layer** only if they act on **completely different qubits**.
    - If two gates share any qubit, they must run in **different layers**.

    > **Caution:** The visual drawing of a circuit can be misleading! Gates may appear side-by-side in the diagram but still be sequential because they share a qubit. Always verify depth with code when it matters.
    """)
    return


@app.cell
def _(QuantumCircuit, display):
    # Example 1: Two independent X gates → depth 1 (they run in parallel)
    qc1 = QuantumCircuit(2)
    qc1.x(0)
    qc1.x(1)
    print("Two independent X gates -- depth:", qc1.depth())
    display(qc1.draw("mpl"))

    # Example 2: Two CX gates sharing qubit 0 → depth 2 (must be sequential)
    qc2 = QuantumCircuit(3)
    qc2.cx(0, 1)
    qc2.cx(0, 2)
    print("\nCX(0,1) then CX(0,2) -- depth:", qc2.depth())
    display(qc2.draw("mpl"))

    # Example 3: Two CX gates on disjoint qubits → depth 1 (parallel)
    qc3 = QuantumCircuit(4)
    qc3.cx(0, 1)
    qc3.cx(2, 3)
    print("\nCX(0,1) and CX(2,3) in parallel -- depth:", qc3.depth())
    display(qc3.draw("mpl"))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 2: Predict the Circuit Depth

    Look at the circuits below and **predict their depth** before running the check cell. Think about which gates can run in parallel.

    In the next cell, set `your_answer_a` and `your_answer_b` to your predicted integers at the two marked lines, then run the check cell and the grader.

    <details>
    <summary><b>Hint</b></summary>

    Draw out which qubits each gate touches and figure out the layers — two gates can share a layer only if they act on completely different qubits.
    </details>
    """)
    return


@app.cell
def _(QuantumCircuit, display):
    # Circuit A
    qc_a = QuantumCircuit(4)
    qc_a.h(0)
    qc_a.h(1)
    qc_a.cx(0, 2)
    qc_a.cx(1, 3)
    qc_a.cx(2, 3)
    display(qc_a.draw("mpl"))

    # Set your_answer_a to your predicted depth for Circuit A (an integer):
    ## TODO ADD YOUR CODE HERE ##

    your_answer_a = 3


    # Circuit B
    qc_b = QuantumCircuit(3)
    qc_b.h(0)
    qc_b.cx(0, 1)
    qc_b.h(2)
    qc_b.cx(2, 1)
    display(qc_b.draw("mpl"))

    # Set your_answer_b to your predicted depth for Circuit B (an integer):
    ## TODO ADD YOUR CODE HERE ##

    your_answer_b = 3

    # After setting both predictions above, run the next cell to check them, then the grader.
    return qc_a, qc_b, your_answer_a, your_answer_b


@app.cell
def _(qc_a, qc_b):
    # Check your answers!
    print("Circuit A depth:", qc_a.depth())
    print("Circuit B depth:", qc_b.depth())
    return


@app.cell
def _(grade_lab1_ex2, your_answer_a, your_answer_b):
    grade_lab1_ex2({"a": your_answer_a, "b": your_answer_b})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <details>
    <summary><b>Click to reveal explanation</b></summary>

    **Circuit A (depth 3):**
    - Layer 1: H(0) and H(1) (different qubits, parallel)
    - Layer 2: CX(0,2) and CX(1,3) (different qubits, parallel)
    - Layer 3: CX(2,3)

    **Circuit B (depth 3):**
    - Layer 1: H(0) and H(2) (different qubits, parallel)
    - Layer 2: CX(0,1) (must wait for H(0))
    - Layer 3: CX(2,1) (shares qubit 1 with previous CX, must be sequential)

    Note how Circuit B's drawing might make it look like CX(0,1) and CX(2,1) could be parallel, but they both use qubit 1!
    </details>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Depth of Our GHZ Circuits

    Let's check the depth of both GHZ constructions we built earlier. You might expect one to be better than the other, but...
    """)
    return


@app.cell
def _(ghz_chain, ghz_fan):
    for n in [5, 10, 20]:
        fan_depth = ghz_fan(n).depth()
        chain_depth = ghz_chain(n).depth()
        print(f"n = {n:2d}:  fan depth = {fan_depth},  chain depth = {chain_depth}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    They have the **same depth**. Both are $N$ (1 for the H gate + $N-1$ for the CX gates). Why?

    - **Fan-out**: Every CX gate shares qubit 0 as the control, so none can run in parallel.
    - **Chain**: Each CX depends on the result of the previous one (qubit $i$ must be entangled before it can entangle qubit $i+1$).

    Both constructions are *linear* in the number of qubits. For 100 qubits, that's 100 layers of gates, far too many for noisy hardware. Can we do better?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Reducing Depth: Start from the Middle

    Here's the key insight: the GHZ state is **symmetric**: all qubits end up in the same superposition. We don't have to build it starting from one end!

    If we place the H gate on the **middle** qubit and grow the entanglement outward in *both* directions at once (two chains running in parallel, one heading left and one heading right), the two halves proceed simultaneously. This approximately **halves** the CX depth.
    """)
    return


@app.cell
def _(QuantumCircuit, display, ghz_chain):
    def ghz_half_depth(n, add_barriers=False):
        """GHZ starting from the middle, growing outward in both directions.

        Pass add_barriers=True to insert a barrier after each outward step; this
        makes the parallel layers visible in the circuit drawing. Barriers count
        as a layer, so always measure depth on a barrier-free circuit.
        """
        qc = QuantumCircuit(n)
        mid = n // 2
        qc.h(mid)

        # Spread left and right simultaneously
        for step in range(1, n):
            left = mid - step
            right = mid + step
            if left >= 0:
                qc.cx(left + 1, left)  # Spread left
            if right < n:
                qc.cx(right - 1, right)  # Spread right
            if add_barriers:
                qc.barrier()
            if left <= 0 and right >= n - 1:
                break
        return qc


    # Draw WITH barriers so the parallel layers are easy to see...
    display(ghz_half_depth(20, add_barriers=True).draw("mpl"))

    # ...but measure depth on the barrier-free circuit:
    qc_half = ghz_half_depth(20)
    print(f"Half-depth GHZ (20 qubits): depth {qc_half.depth()}")
    print(f"Linear GHZ (20 qubits):     depth {ghz_chain(20).depth()}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Going Further: Recursive Fan-Out

    The halving trick only applied the idea once. We split the work into two branches. But we can apply it **recursively**: once the middle qubit entangles a qubit to its left and right, those newly entangled qubits can *each* serve as new starting points to spread entanglement further.

    In each layer, every already-entangled qubit that has an unentangled neighbor performs one CX. This **doubles** the number of entangled qubits per layer:

    | Layer | Action | Entangled qubits |
    |-------|--------|-----------------|
    | 0 | H on qubit 0 | 1 |
    | 1 | CX(0,1) | 2 |
    | 2 | CX(0,2) + CX(1,3) | 4 |
    | 3 | CX(0,4) + CX(1,5) + CX(2,6) + CX(3,7) | 8 |
    | 4 | CX(0,8) + CX(1,9) + … + CX(7,15) | 16 |

    The depth grows as $\lceil\log_2(N)\rceil + 1$ instead of $N$, an **exponential improvement**!

    For $N = 16$: depth = $\log_2(16) + 1 = 5$.

    > **Note:** For simplicity the table above indexes the recursive fan-out starting from **qubit 0** rather than the middle. Where you start doesn't change the $O(\log N)$ depth scaling — the doubling of entangled qubits per layer is what matters. Exercise 3 below uses this qubit-0 indexing.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 3: Build a Depth-5 GHZ State for 16 Qubits

    **Task:** Build a 16-qubit GHZ circuit with depth exactly 5 using recursive fan-out.

    **Strategy:** In each CX layer, every already-entangled qubit should entangle one new qubit. After $k$ CX layers, you should have $2^k$ entangled qubits.

    **Note:** In this abstract (non-hardware) setting, any qubit can connect to any other qubit. We'll deal with hardware constraints in Part 3.
    """)
    return


@app.cell
def _(QuantumCircuit):
    def ghz_fan_recursive(qc:QuantumCircuit, entangled:list[int], remain:list[int]):
        """
        Creates a GHZ State of N qubits by doubling the entangled set each round: every qubit that's already entangled becomes a control for one brand-new target. 

        Params:
        qc        - A Quantum Circuit
        entangled - qubits that already hold the correct GHZ-correlated state
        remain    - qubits that haven't been entangled yet
        """

        if not remain:
            return

        # Caps how many new qubits can entangle *this* round
        batch_size = min(len(entangled), len(remain))

        # Grabs that many qubits off the front of remain
        batch = remain[:batch_size]

        # Pair each entangled qubit with one fresh target and applies a CNOT
        for control, target in zip(entangled, batch):
            qc.cx(control, target)

        ghz_fan_recursive(qc, entangled + batch, remain[batch_size:])

    return (ghz_fan_recursive,)


@app.cell
def _(QuantumCircuit, Statevector, display, ghz_fan_recursive, np):
    qc_7 = QuantumCircuit(16)
    qc_7.h(0)
    ghz_fan_recursive(qc_7, [0], list(range(1, 16)))
    display(qc_7.draw('mpl'))
    print('Depth:', qc_7.depth())
    assert qc_7.depth() == 5, f'Expected depth 5, got {qc_7.depth()}'
    _sv = Statevector(qc_7)
    _probs = np.abs(_sv.data) ** 2
    assert np.isclose(_probs[0], 0.5) and np.isclose(_probs[-1], 0.5), 'Not a valid GHZ state!'
    print('Success — valid 16-qubit GHZ state with depth 5.')
    return (qc_7,)


@app.cell
def _(grade_lab1_ex3, qc_7):
    grade_lab1_ex3(qc_7)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Part 2 Summary

    **Learning goals achieved:**
    - **Circuit depth**: the number of sequential gate layers (lower = less noise)
    - **GHZ states**: $N$-qubit entanglement $\frac{1}{\sqrt{2}}(|00\ldots0\rangle + |11\ldots1\rangle)$
    - Linear GHZ circuits (fan-out or chain) have depth $N$
    - **Starting from the middle** halves the depth
    - **Recursive fan-out** achieves depth $\lceil\log_2(N)\rceil + 1$, exponentially better
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Part 3: Transpilation <a id="part3"></a>

    So far we've built circuits using abstract qubits and familiar gates like H and CX. But real quantum hardware has specific constraints:

    1. **Limited native gates**: The processor only supports a fixed set of gates. The IBM Heron processors use $\{R_Z, \sqrt{X}, X, CZ\}$. No H gate, no CX gate!
    2. **Limited connectivity**: Not every pair of qubits is physically connected. If you need a two-qubit gate between unconnected qubits, extra SWAP gates must be inserted (each costing 3 CZ gates).
    3. **Physical qubit assignment**: Your abstract qubit 0 must be mapped to a specific physical qubit on the chip.

    **Transpilation** is the process of transforming an abstract circuit into one that respects all these constraints. Let's see it in action.
    """)
    return


@app.cell
def _():
    from qiskit import generate_preset_pass_manager
    from qiskit_ibm_runtime.fake_provider import FakeTorino

    # FakeTorino simulates the 133-qubit IBM Heron processor
    backend = FakeTorino()
    print(f"Backend: {backend.name}")
    print(f"Qubits: {backend.num_qubits}")
    print(
        f"Native gates: {sorted(g for g in backend.operation_names if g not in ['reset', 'delay', 'measure', 'id', 'if_else', 'for_loop', 'switch_case'])}"
    )
    return FakeTorino, backend, generate_preset_pass_manager


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We'll start small: transpile a **5-qubit** chain GHZ so the before/after is easy to read. (Don't be thrown by the size change — Part 2 went up to 20 qubits; we scale back up to a 64-qubit GHZ in Exercise 7.)
    """)
    return


@app.cell
def _(backend, display, generate_preset_pass_manager, ghz_chain):
    qc_8 = ghz_chain(5)
    print('Original circuit:')
    display(qc_8.draw('mpl'))
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    qc_with_meas = qc_8.copy()
    qc_with_meas.measure_all()
    _isa_qc = pm.run(qc_with_meas)
    print('\nTranspiled circuit:')
    display(_isa_qc.draw('mpl', idle_wires=False))
    print(f'\nBefore: depth {qc_8.depth()}, gates {dict(qc_8.count_ops())}')
    print(f'After:  depth {_isa_qc.depth()}, gates {dict(_isa_qc.count_ops())}')
    return (pm,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### What changed?

    Look at the transpiled circuit:

    - **H is gone**, replaced by combinations of $R_Z$ and $\sqrt{X}$ gates (the native single-qubit gates)
    - **CX is gone**, replaced by CZ gates surrounded by single-qubit gates
    - **Physical qubit numbers** appear: your abstract qubits are now mapped to specific hardware qubits
    - **The depth increased**: each abstract gate expands into multiple native gates

    The good news: the transpiler found a layout where all 5 qubits are physically connected in a chain, so **no SWAP gates were needed**. That won't always be the case!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Detour: What if we ignore topology?

    Our chain GHZ transpiled cleanly because qubits 0-1-2-3-4 are physically connected on Heron. But what if we use the **fan-out** pattern instead, with the **same** physical layout? Qubit 0 is connected to qubit 1, but **not** to qubits 2, 3, or 4. The transpiler has to do something to make `CX(0, 2)`, `CX(0, 3)`, and `CX(0, 4)` happen.

    Its solution: **insert SWAP gates** to physically shuffle the state of qubit 0 along the chain until it's adjacent to its target. Each SWAP decomposes into **3 CZ gates** on the real hardware. This is transpilation *visibly* rewriting your circuit — watch the gate counts and depth jump. Let's see it in action.

    > **Note on the measurements:** when SWAPs move logical qubits onto different physical wires, the transpiler also **re-routes the measurements** so each classical bit still records the qubit you intended. That bookkeeping is handled for you, but it's why the measurement section of the transpiled drawing may not line up one-to-one with the original circuit.
    """)
    return


@app.cell
def _(backend, display, ghz_fan, pm):
    from qiskit import transpile

    # Same fan-out GHZ, same physical layout (chain 0-1-2-3-4 on Heron)
    qc_fan = ghz_fan(5)
    qc_fan.measure_all()

    # Transpile while keeping SWAPs visible (don't decompose them to native gates yet)
    isa_fan_swaps = transpile(
        qc_fan,
        coupling_map=backend.coupling_map,
        basis_gates=["h", "cx", "swap"],
        initial_layout=[0, 1, 2, 3, 4],
        optimization_level=1,
    )

    print("Fan-out GHZ on the line 0-1-2-3-4 (SWAPs kept visible):")
    display(isa_fan_swaps.draw("mpl", idle_wires=False))
    print(f"SWAPs inserted: {isa_fan_swaps.count_ops().get('swap', 0)}")
    print(f"CX gates:       {isa_fan_swaps.count_ops().get('cx', 0)}")
    print("(Each SWAP becomes 3 CZ gates in the final native circuit.)")

    # Now fully decomposed to native gates -- this is what actually runs on hardware:
    isa_fan_native = pm.run(qc_fan)
    print(
        f"\nFully transpiled to native gates: depth {isa_fan_native.depth()}, "
        f"CZ gates {isa_fan_native.count_ops().get('cz', 0)}"
    )
    display(isa_fan_native.draw("mpl", idle_wires=False, fold=-1))
    return (transpile,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### The Bridge Gate Identity

    SWAPs aren't the only way to handle a non-local CX. There's a clever circuit identity called the **bridge gate** that implements `CX(0, 2)` using only nearest-neighbor gates on the chain `0 — 1 — 2`, **without** ever moving state:

    $$\text{CX}(0, 2) \;=\; \text{CX}(0, 1)\,\cdot\,\text{CX}(1, 2)\,\cdot\,\text{CX}(0, 1)\,\cdot\,\text{CX}(1, 2)$$

    Four nearest-neighbor CX gates in that order produce the **exact same** transformation as one long-distance `CX(0, 2)`. The middle qubit acts as a "bridge": its state is temporarily flipped and then flipped back, leaving it unchanged, while the entangling action propagates from qubit 0 to qubit 2.

    Bridges are useful when you need *one* non-local CX through *one* intermediate. For more complex routing, the transpiler usually still prefers SWAPs. But the identity makes the cost of a non-local gate concrete: even with this trick, a "free" non-local CX costs **4×** as many CX gates as a local one.
    """)
    return


@app.cell
def _(QuantumCircuit, Statevector, display):
    # Verify the bridge identity: CX(0, 2) == CX(0,1) CX(1,2) CX(0,1) CX(1,2)

    # Direct: one long-distance CX (with H on qubit 0 so the entangling action is visible)
    qc_direct = QuantumCircuit(3)
    qc_direct.h(0)
    qc_direct.cx(0, 2)
    display(qc_direct.draw("mpl"))

    # Bridge: four nearest-neighbor CX gates
    qc_bridge = QuantumCircuit(3)
    qc_bridge.h(0)
    qc_bridge.cx(0, 1)
    qc_bridge.cx(1, 2)
    qc_bridge.cx(0, 1)
    qc_bridge.cx(1, 2)
    display(qc_bridge.draw("mpl"))

    sv_direct = Statevector(qc_direct)
    sv_bridge = Statevector(qc_bridge)

    print("Direct  CX(0, 2):", sv_direct)
    print("Bridge form:    ", sv_bridge)
    print("States equal?   ", sv_direct.equiv(sv_bridge))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 4: Build a Nearest-Neighbor GHZ Using the Bridge Identity

    Here's a 3-qubit GHZ built with the fan-out pattern:

    ```python
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(0, 2)   # <-- This CX is non-local on a 0-1-2 chain!
    ```

    That last gate, `CX(0, 2)`, can't run directly on hardware where only neighbors are connected.

    **Task:** Build the same 3-qubit GHZ state, but use the **bridge identity** to replace `CX(0, 2)` with four nearest-neighbor CX gates. The final circuit should use only `CX(0, 1)` and `CX(1, 2)` — never `CX(0, 2)`.

    After you're done, look at how many CX gates you used compared to the chain form (`H(0); CX(0, 1); CX(1, 2)`). That difference is the real cost of insisting on a fan-out shape when the hardware wants a chain.
    """)
    return


@app.cell
def _(QuantumCircuit, Statevector, display, np):
    qc_9 = QuantumCircuit(3)
    qc_9.h(0)
    qc_9.cx(0, 1)
    qc_9.cx(1, 2)
    display(qc_9.draw('mpl'))
    _sv = Statevector(qc_9)
    print('Your state:', _sv)
    _probs = np.abs(_sv.data) ** 2
    assert np.isclose(_probs[0], 0.5) and np.isclose(_probs[-1], 0.5), 'Not a valid 3-qubit GHZ state!'
    non_local = []
    for instr in qc_9.data:
        if instr.operation.name == 'cx':
            q_indices = [qc_9.find_bit(_q).index for _q in instr.qubits]
            if abs(q_indices[0] - q_indices[1]) != 1:
                non_local.append(tuple(q_indices))
    assert not non_local, f'Non-nearest-neighbor CX found: {non_local}'
    print(f"Valid GHZ using only nearest-neighbor CX gates ({qc_9.count_ops().get('cx', 0)} CX total).")
    return (qc_9,)


@app.cell
def _(grade_lab1_ex4, qc_9):
    grade_lab1_ex4(qc_9)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <details>
    <summary><b>Click to reveal solution</b></summary>

    ```python
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.cx(0, 1)
    # Bridge identity replacing CX(0, 2): four nearest-neighbor CX gates
    qc.cx(0, 1)
    qc.cx(1, 2)
    qc.cx(0, 1)
    qc.cx(1, 2)
    ```

    This works, but note that the original `CX(0, 1)` and the first `CX(0, 1)` from the bridge are adjacent — and `CX(0, 1) · CX(0, 1) = I` (any CX is its own inverse). So we can cancel them, leaving:

    ```python
    qc.h(0)
    qc.cx(1, 2)
    qc.cx(0, 1)
    qc.cx(1, 2)
    ```

    **3 CX gates.** Compare to the chain form `H(0); CX(0,1); CX(1,2)` which uses **2**. Even with simplification, insisting on the fan-out shape on a nearest-neighbor chip costs us an extra CX per non-local hop. For longer chains and higher-distance CXs, this overhead grows quickly — which is why designing topology-aware circuits from the start (the rest of Part 3) is the real win.
    </details>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 5: Efficient 5-Qubit GHZ on a Line

    Physical qubits 0–4 on FakeTorino form a chain: 0-1-2-3-4. Let's build a GHZ circuit that respects this connectivity and minimizes depth.

    **Task:** Build a 5-qubit GHZ circuit with abstract depth **4** by starting from the middle qubit.

    <details>
    <summary><b>Hint</b></summary>

    Remember the "start from the middle" trick from Part 2! Put H on the middle qubit, then grow outward toward both ends.
    </details>
    """)
    return


@app.cell
def _(QuantumCircuit):
    def ghz_half(qc:QuantumCircuit, qubits:list[int], end:str): 
        n = len(qubits)

        if n <= 1:
            return

        mid = n // 2
        if end == "left":
            qc.cx(qubits[mid - 1], qubits[mid])
        elif end == "right":
            qc.cx(qubits[mid], qubits[mid - 1])

        ghz_half(qc, qubits[mid:], "left")
        ghz_half(qc, qubits[:mid], "right")

    return (ghz_half,)


@app.cell
def _(
    QuantumCircuit,
    backend,
    display,
    generate_preset_pass_manager,
    ghz_half,
):
    qc_10 = QuantumCircuit(5)
    qc_10.h(5 // 2)
    ghz_half(qc_10, list(range(5)), end="right")
    display(qc_10.draw('mpl'))
    print('Abstract depth:', qc_10.depth())
    assert qc_10.depth() == 4, f'Expected depth 4, got {qc_10.depth()}'
    _qc_m = qc_10.copy()
    _qc_m.measure_all()
    pm_1 = generate_preset_pass_manager(optimization_level=1, backend=backend, initial_layout=[0, 1, 2, 3, 4])
    _isa_qc = pm_1.run(_qc_m)
    print(f'Transpiled depth: {_isa_qc.depth()}')
    print(f"CZ gates: {_isa_qc.count_ops().get('cz', 0)}")
    return (qc_10,)


@app.cell
def _(grade_lab1_ex5, qc_10):
    grade_lab1_ex5(qc_10)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Hardware Topology: Heavy-Hex

    FakeTorino models a **Heron processor** with **heavy-hex** connectivity. The 133 qubits are arranged in a distinctive pattern:

    - **Horizontal chains** of qubits run across each row
    - **Vertical bridge qubits** connect rows at staggered positions
    - Most qubits have **degree 2** (two neighbors)
    - **Junction qubits** have **degree 3** (three neighbors). These are the branching points

    This topology is *not* all-to-all. A two-qubit gate between non-neighboring qubits requires SWAP gates, which dramatically increase depth. Building efficient circuits for heavy-hex means working *with* the connectivity, not against it.

    Let's visualize a portion of the FakeTorino coupling map to see the structure.
    """)
    return


@app.cell
def _(backend, display, plt):
    # Visualize the heavy-hex connectivity for a portion of FakeTorino
    import networkx as nx
    cm = backend.coupling_map
    sub_qubits = set(range(46))

    # Include enough qubits to show the Exercise 6 T-junction: qubit 25's third
    # neighbor is qubit 35 (with 35-44 forming the vertical leg), which lie beyond
    # the first two rows -- so we draw qubits 0-45 rather than stopping at 33.
    G = nx.Graph()

    for _q in sub_qubits:
        G.add_node(_q)
    for _q in sub_qubits:
        for _nb in cm.neighbors(_q):
            if _nb in sub_qubits:
                G.add_edge(_q, _nb)

    junctions = [_q for _q in sub_qubits if G.degree(_q) == 3]
    _colors = ['#ff6b6b' if _q in junctions else '#4ecdc4' for _q in G.nodes()]
    _fig, _ax = plt.subplots(figsize=(15, 6))

    # Identify degree-3 junctions
    pos = nx.kamada_kawai_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=400, font_size=9, node_color=_colors, edge_color='#888', width=2, ax=_ax)
    _ax.set_title('FakeTorino: Qubits 0–45 (red = degree-3 junctions)')

    plt.tight_layout()
    display(_fig)
    plt.close(_fig)

    print('Degree-3 junctions (qubits 0-45):', sorted(junctions))
    return (cm,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 6: 7-Qubit GHZ on a Heavy-Hex Subgraph

    Consider this T-shaped subgraph of FakeTorino:

    ```
    23 -- 24 -- 25 -- 26 -- 27
                |
               35
                |
               44
    ```

    Qubit 25 is a **degree-3 junction**: it connects to qubits 24, 26, and 35. You can spot exactly this T-shape — qubit 25 with its three neighbors, and the 25–35–44 leg — in the heavy-hex topology graph plotted above.

    **Task:** Build a 7-qubit GHZ circuit on this subgraph with the **minimum possible depth**.

    <details>
    <summary><b>Hints</b></summary>

    - Which qubit should you start from? (Think about where the branching point is!)
    - Remember: a qubit can only participate in one CX gate per layer.
    - Map your abstract qubits as: 0→q23, 1→q24, 2→q25, 3→q26, 4→q27, 5→q35, 6→q44.
    </details>
    """)
    return


@app.cell
def _(QuantumCircuit, backend, display, generate_preset_pass_manager):
    qc_11 = QuantumCircuit(7)

    qc_11.h(2)
    qc_11.cx(2, 1)
    qc_11.cx(1, 0)
    qc_11.cx(2, 3)
    qc_11.cx(3, 4)
    qc_11.cx(2, 5)
    qc_11.cx(5, 6)

    display(qc_11.draw('mpl'))
    print('Abstract depth:', qc_11.depth())
    _qc_m = qc_11.copy()
    _qc_m.measure_all()
    pm_2 = generate_preset_pass_manager(optimization_level=1, backend=backend, initial_layout=[23, 24, 25, 26, 27, 35, 44])
    _isa_qc = pm_2.run(_qc_m)
    print(f'Transpiled depth: {_isa_qc.depth()}')
    print(f"CZ gates: {_isa_qc.count_ops().get('cz', 0)}")
    return (qc_11,)


@app.cell
def _(grade_lab1_ex6, qc_11):
    grade_lab1_ex6(qc_11)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 7: The Final Challenge — 64-Qubit GHZ

    Now let's put everything together. Your task is to build an efficient GHZ state for **64 qubits** (qubits 0–63 of FakeTorino) and transpile it.

    <details>
    <summary><b>New here? What's a "BFS spanning tree" and why use one?</b></summary>

    A **spanning tree** is a set of edges that connects every qubit in the subgraph with no loops. **Breadth-first search (BFS)** builds one by starting at a chosen *center* qubit and exploring outward in rings: first all of its neighbors (distance 1), then *their* unvisited neighbors (distance 2), and so on.

    Why this matters for circuit depth: if we entangle each qubit with its BFS *parent*, the GHZ circuit's depth is essentially the **longest root-to-leaf distance** in the tree. Starting from a well-centered qubit keeps that distance — and therefore the depth — as small as the hardware graph allows. (It's the "start from the middle" idea from Part 2, generalized from a line to an arbitrary graph.)

    Background: [breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search) · [`CouplingMap`](https://docs.quantum.ibm.com/api/qiskit/qiskit.transpiler.CouplingMap).
    </details>

    **Strategy:**
    1. Use the backend's coupling map to find the connectivity of qubits 0–63
    2. Build a **spanning tree** via BFS (breadth-first search) from a well-chosen center qubit
    3. Construct the GHZ circuit by entangling along the tree, layer by layer
    4. Transpile and compare depth against a naive linear GHZ

    **Helpful information:**
    - The best center qubit in the 0–63 subgraph is **qubit 25** (minimizes the maximum distance to any other qubit)
    - `backend.coupling_map.neighbors(q)` gives you the neighbors of qubit $q$
    - The BFS tree is built for you in the next cell — your job is the single line that adds the entangling CX from each qubit to its parent.
    """)
    return


@app.cell
def _(cm):
    # Helper: show degree-3 junctions in the 64-qubit subgraph
    _sub = set(range(64))
    print('Degree-3 junctions in qubits 0-63:')
    for _q in sorted(_sub):
        nbs = [_nb for _nb in cm.neighbors(_q) if _nb in _sub]
        if len(nbs) >= 3:
            print(f'  Qubit {_q}: neighbors {sorted(nbs)}')
    return


@app.cell
def _(QuantumCircuit, backend, cm, generate_preset_pass_manager, ghz_chain):
    from collections import deque

    n_1 = 64
    _sub = set(range(n_1))
    center = 25
    parent = {center: None}
    bfs_depth = {center: 0}
    queue = deque([center])

    while queue:
        node = queue.popleft()
        for _nb in sorted(cm.neighbors(node)):
            if _nb in _sub and _nb not in parent:
                parent[_nb] = node
                bfs_depth[_nb] = bfs_depth[node] + 1
                queue.append(_nb)

    print(f'BFS from qubit {center}: reached {len(parent)} qubits')
    print(f'Max BFS depth: {max(bfs_depth.values())}')

    qc_12 = QuantumCircuit(n_1)
    qc_12.h(center)
    max_d = max(bfs_depth.values())

    for _d in range(1, max_d + 1):
        for _q in range(n_1):
            if _q in bfs_depth and bfs_depth[_q] == _d:
                # vv ANSWER HERE vv
                qc_12.cx(parent[_q], _q)

    qc_12.measure_all()

    print(f'\nYour GHZ abstract depth: {qc_12.depth() - 1}')

    pm_3 = generate_preset_pass_manager(optimization_level=1, backend=backend)
    _isa_qc = pm_3.run(qc_12)

    print(f'Your GHZ transpiled depth: {_isa_qc.depth()}')
    print(f"Your GHZ CZ gates: {_isa_qc.count_ops().get('cz', 0)}")

    _qc_naive = ghz_chain(n_1)
    _qc_naive.measure_all()
    isa_naive = pm_3.run(_qc_naive)

    print(f'\nNaive chain transpiled depth: {isa_naive.depth()}')
    print(f"Naive chain CZ gates: {isa_naive.count_ops().get('cz', 0)}")
    return (qc_12,)


@app.cell
def _(grade_lab1_ex7, qc_12):
    grade_lab1_ex7(qc_12)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Part 3 Summary

    **Learning goals achieved:**
    - **Transpilation** transforms abstract circuits into hardware-native ones (gate decomposition + qubit routing + layout)
    - Heron processors use $\{R_Z, \sqrt{X}, X, CZ\}$ (no H or CX)
    - **Heavy-hex topology**: degree-2 chain qubits and degree-3 junction qubits
    - SWAP gates (needed for non-neighboring qubits) cost 3 CZ each, so avoid them by designing topology-aware circuits
    - **BFS spanning tree**: a systematic way to build efficient GHZ circuits on arbitrary hardware graphs
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Part 4: Running on a Noisy Simulator <a id="part4"></a>

    Now let's see how circuit depth actually affects results on a noisy processor. We'll use **FakeTorino** — a *local* noisy simulator that reproduces the real Torino chip's error rates and connectivity — to compare an efficient GHZ circuit against a naive one. Everything in this section runs **locally**, so it consumes **no IBM Quantum runtime minutes**; the last code cell shows how you would switch to a real backend.

    This follows the **Qiskit Patterns** workflow:
    1. **Map**: Design the abstract circuit for the problem
    2. **Optimize**: Transpile for the target backend
    3. **Execute**: Run using `SamplerV2`
    4. **Post-process**: Analyze measurement results
    """)
    return


@app.cell
def _(FakeTorino):
    from qiskit_aer import AerSimulator
    from qiskit_ibm_runtime import SamplerV2

    # Build a noisy simulator using FakeTorino's noise model and connectivity
    aer_backend = AerSimulator.from_backend(FakeTorino())
    sampler = SamplerV2(aer_backend)
    print(
        f"Ready to run on: {aer_backend.name} ({aer_backend.num_qubits} qubits, noisy simulation)"
    )

    # To run on REAL hardware instead of this local noisy simulator, you would swap in a
    # real backend (this DOES consume IBM Quantum runtime minutes and needs a saved account):
    #
    # from qiskit_ibm_runtime import QiskitRuntimeService
    # service = QiskitRuntimeService()
    # real_backend = service.least_busy(operational=True, simulator=False)
    # sampler = SamplerV2(real_backend)
    return (sampler,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### The Experiment

    We'll compare two 15-qubit GHZ circuits (using row 0 of FakeTorino, qubits 0–14):

    1. **Naive (fan-out)**: H on qubit 0, then CX(0,1), CX(0,2), …, CX(0,14). This does *not* match the hardware connectivity: qubit 0 isn't connected to most other qubits, so the transpiler must insert many SWAP gates.

    2. **Efficient (topology-aware)**: Start from the middle (qubit 7), fan out in both directions along the physical chain. This *matches* the hardware, so no SWAPs are needed.

    If our optimization theory is correct, the efficient circuit should have significantly higher fidelity.
    """)
    return


@app.cell
def _(QuantumCircuit, backend, generate_preset_pass_manager, transpile):
    n_2 = 15

    _qc_naive = QuantumCircuit(n_2)
    _qc_naive.h(0)
    for i in range(1, n_2):
        _qc_naive.cx(0, i)
    _qc_naive.measure_all()

    qc_eff = QuantumCircuit(n_2)
    mid = n_2 // 2
    qc_eff.h(mid)
    for step in range(1, n_2):
        left = mid - step
        right = mid + step
        if left >= 0:
            qc_eff.cx(left + 1, left)
        if right < n_2:
            qc_eff.cx(right - 1, right)
        if left <= 0 and right >= n_2 - 1:
            break
    qc_eff.measure_all()

    pm_4 = generate_preset_pass_manager(optimization_level=1, backend=backend, initial_layout=list(range(n_2)))

    isa_naive_1 = pm_4.run(_qc_naive)
    isa_eff = pm_4.run(qc_eff)

    isa_naive_swaps = transpile(_qc_naive, coupling_map=backend.coupling_map, basis_gates=['h', 'cx', 'swap'], initial_layout=list(range(n_2)), optimization_level=1)

    isa_eff_swaps = transpile(qc_eff, coupling_map=backend.coupling_map, basis_gates=['h', 'cx', 'swap'], initial_layout=list(range(n_2)), optimization_level=1)

    naive_swaps = isa_naive_swaps.count_ops().get('swap', 0)
    eff_swaps = isa_eff_swaps.count_ops().get('swap', 0)

    print('=== Circuit Comparison ===')
    print(f"Naive:     SWAPs inserted = {naive_swaps:>2},  transpiled depth = {isa_naive_1.depth():>4},  CZ gates = {isa_naive_1.count_ops().get('cz', 0)}")
    print(f"Efficient: SWAPs inserted = {eff_swaps:>2},  transpiled depth = {isa_eff.depth():>4},  CZ gates = {isa_eff.count_ops().get('cz', 0)}")
    print('\n(Each SWAP becomes ~3 CZ gates, which is why the naive CZ count grows so quickly.)')
    return isa_eff, isa_naive_1, n_2


@app.cell
def _(isa_eff, isa_naive_1, sampler):
    # Execute both circuits on the noisy simulator.
    # SHOTS controls how many times we sample. 8192 is ideal but can time out on
    # free Colab/qBraid sessions -- lower it (1024-2048 is plenty here) if needed.
    SHOTS = 2048
    job = sampler.run([isa_naive_1, isa_eff], shots=SHOTS)
    result = job.result()
    counts_naive = result[0].data.meas.get_counts()
    counts_eff = result[1].data.meas.get_counts()
    print('Execution complete!')
    print(f'Naive:     {sum(counts_naive.values())} shots')
    print(f'Efficient: {sum(counts_eff.values())} shots')
    return counts_eff, counts_naive


@app.cell
def _(counts_eff, counts_naive, n_2):
    # Calculate GHZ fidelity: fraction of shots in |00...0⟩ or |11...1⟩
    def ghz_fidelity(counts, n):
        total = sum(counts.values())
        correct = counts.get('0' * n, 0) + counts.get('1' * n, 0)
        return correct / total
    fid_naive = ghz_fidelity(counts_naive, n_2)
    fid_eff = ghz_fidelity(counts_eff, n_2)
    print(f'Naive GHZ fidelity:     {fid_naive:.4f}')
    print(f'Efficient GHZ fidelity: {fid_eff:.4f}')
    if fid_eff > fid_naive:
        improvement = (fid_eff - fid_naive) / fid_naive * 100
        print(f'Improvement: {improvement:.1f}%')
    return fid_eff, fid_naive


@app.cell
def _(counts_eff, counts_naive, display, n_2, plot_histogram):
    # Visualize: side-by-side histogram of measurement outcomes
    display(plot_histogram([counts_naive, counts_eff], legend=['Naive (fan-out)', 'Efficient (topology-aware)'], number_to_keep=8, sort='desc', title=f'{n_2}-Qubit GHZ: Naive vs Efficient on FakeTorino', figsize=(14, 5)))
    return


@app.cell
def _(display, fid_eff, fid_naive, isa_eff, isa_naive_1, n_2, plt):
    _fig, _ax = plt.subplots(figsize=(8, 5))
    labels = ['Naive\n(fan-out)', 'Efficient\n(topology-aware)']
    fidelities = [fid_naive, fid_eff]
    depths = [isa_naive_1.depth(), isa_eff.depth()]
    _colors = ['#ff6b6b', '#4ecdc4']
    bars = _ax.bar(range(len(labels)), fidelities, color=_colors, width=0.5, edgecolor='white')
    _ax.set_ylabel('GHZ Fidelity', fontsize=13)
    _ax.set_title(f'{n_2}-Qubit GHZ on FakeTorino: Depth vs Fidelity', fontsize=14)
    _ax.set_xticks(range(len(labels)))
    _ax.set_xticklabels(labels, fontsize=12)
    for bar, _d, f in zip(bars, depths, fidelities):
        _ax.text(bar.get_x() + bar.get_width() / 2.0, bar.get_height() + 0.02, f'depth = {_d}', ha='center', va='bottom', fontsize=11, fontweight='bold')
    _ax.set_ylim(0, 1.0)
    _ax.spines['top'].set_visible(False)
    _ax.spines['right'].set_visible(False)
    plt.tight_layout()
    display(_fig)
    plt.close(_fig)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### What do we see?

    The efficient circuit, with its lower transpiled depth and fewer two-qubit gates, achieves significantly higher fidelity on the noisy simulator. The pattern is clear:

    - **Fewer CZ gates** → fewer sources of two-qubit error
    - **Lower depth** → less time for qubits to decohere
    - **No SWAP gates** → no unnecessary overhead from routing

    > **Don't be alarmed by the absolute numbers.** A 15-qubit GHZ state on noisy hardware is genuinely hard, so the raw fidelities here are often in the **0.4–0.6** range — not the ~0.99 you might expect from a textbook. Every two-qubit gate adds a little error, and there are many of them. What matters in this experiment is the **relative** improvement of the efficient circuit over the naive one; that gap is the whole point.

    On real hardware, the difference would be even more dramatic. This demonstrates that **circuit optimization is not just an academic exercise**: it directly impacts the quality of your quantum computation.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Looking Ahead: Lab 2

    In Lab 2, we will compare the new IBM **Nighthawk** processor against the **Heron** processor (the architecture we've been working with in this lab). The two have different connectivity patterns: Heron uses heavy-hex, while Nighthawk has a denser graph with more neighbors per qubit. These architectural differences directly affect circuit performance.

    The skills you've built here (constructing efficient GHZ states, understanding depth, working with heavy-hex topology) will carry directly into Lab 2, where GHZ circuits are used to benchmark and compare the two processors.

    See you in Lab 2! 🚀
    """)
    return


@app.cell
def _():
    from qc_grader.challenges.qgss_2026 import check_progress 

    check_progress("lab1")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Lab 1 Complete: Final Summary

    **What you've learned:**

    | Concept | Key Takeaway |
    |---------|-------------|
    | **X, H, CX gates** | The building blocks of quantum circuits |
    | **Superposition** | H gate creates $\frac{1}{\sqrt{2}}(\lvert 0\rangle + \lvert 1\rangle)$ |
    | **Entanglement** | CX + superposition creates correlated qubit pairs |
    | **Bell & GHZ states** | Entanglement for 2 and N qubits |
    | **Circuit depth** | Number of sequential gate layers; lower = less noise |
    | **Recursive fan-out** | GHZ in $O(\log N)$ depth instead of $O(N)$ |
    | **Transpilation** | Abstract → hardware-native circuits |
    | **Heavy-hex topology** | Degree-2 chains + degree-3 junctions |
    | **Topology-aware design** | Work with hardware connectivity to avoid SWAPs |
    | **Noisy execution** | Lower depth → higher fidelity on real devices |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Additional information

    **Created by:** James Weaver

    **Version:** 1.0.0
    """)
    return


if __name__ == "__main__":
    app.run()
