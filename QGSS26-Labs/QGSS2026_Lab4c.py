import marimo

__generated_with = "0.23.13"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Lab 4: Towards quantum advantage

    # Chapter 4: Variational problems: Sample-based quantum diagonalization

    ### *Note: Lab4c is a bonus lab non-required for the badge*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *Usage estimate of QPU time for the notebook excluding the bonus part: 10 seconds on Nighthawk r1 or 2 seconds on Heron r2. (NOTE: This is an estimate only. Your runtime might vary.)*

    *The QPU usage estimate reflects only backend execution time. Queueing, calibration, and runtime session delays can extend total execution to several minutes, even for workloads using only seconds of QPU time.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Table of Contents

    - Exercise 1: Map LUCJ circuit to the Nighthawk device
    - Exercise 2: Examine the resulting bitstring
    - Exercise 3: Recover the bitstring
    - Exercise 4: Augment SQD with a classical reference subspace
    - Scored Exercise: Find your best subspace!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In Lab 4a, we explored what quantum advantage means and how the [Quantum Advantage Tracker](https://quantum-advantage-tracker.github.io/) classifies demonstrations into three categories: classically verifiable problems, variational problems, and observable estimation. We saw examples like the $ \mathrm{Fe}_4\mathrm{S}_4$ molecule computation (variational) and the Loschmidt Echo calculation (observable estimation).

    Now we look into the second category: **variational problems**. These are chemistry and material science problems where we are focused on obtaining ground-state for advanced simulation. Materials are governed directly by quantum mechanics and this obviously makes them an ideal domain for applying quantum computataion.

    In this lab, you will estimate the **ground-state energy** of the nitrogen molecule (N₂) on a real quantum computer using **Sample-based Quantum Diagonalization (SQD)**.

    SQD is a hybrid quantum–classical method: the quantum computer runs a parameterized circuit and *proposes* which electron arrangements are most important, while the classical computer does the linear algebra — diagonalizing the molecular Hamiltonian in that small, smartly chosen set of configurations.

    By the end of this chapter you will have mapped a chemistry circuit to two different IBM device topologies, cleaned up noisy hardware bitstrings, and beaten the classical brute-force method using real quantum hardware.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Install the necessary libraries

    > **Note for Windows users:**
    > One of the required library (pyscf) does not officially support Windows OS. For this lab, please consider using [qBraid](https://qbraid.com/) and [Google Colab](https://colab.research.google.com/). If you are comfortable with extra environmental setup, [Windows Subsystem for Linux](https://learn.microsoft.com/en-us/windows/wsl/install) may be ideal enabling you to utilize your local environment in a full functionality.
    """)
    return


@app.cell
def _():
    # '%pip install qiskit-addon-sqd' command supported automatically in marimo
    # '%pip install ffsim' command supported automatically in marimo
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Imports
    """)
    return


@app.cell
def _():
    # Import necessary packages
    import warnings
    warnings.filterwarnings('ignore')
    import copy
    import numpy as np
    import matplotlib.pyplot as plt
    from collections import defaultdict
    from typing import cast
    from itertools import combinations
    from functools import partial
    import pyscf
    import pyscf.cc
    import pyscf.mcscf
    import ffsim
    from qiskit.circuit import QuantumCircuit, QuantumRegister, CircuitInstruction, Barrier
    from qiskit.transpiler import generate_preset_pass_manager
    from qiskit.visualization import plot_error_map
    from qiskit_ibm_runtime import QiskitRuntimeService, Sampler
    from qiskit_ibm_runtime.fake_provider import FakeMiami
    from qiskit_addon_sqd.fermion import SCIResult, solve_sci_batch
    from qiskit_addon_sqd.subsampling import subsample
    from qiskit_addon_sqd.counts import bit_array_to_arrays, bitstring_matrix_to_integers

    return (
        Barrier,
        CircuitInstruction,
        QiskitRuntimeService,
        QuantumCircuit,
        QuantumRegister,
        SCIResult,
        bit_array_to_arrays,
        bitstring_matrix_to_integers,
        cast,
        combinations,
        copy,
        ffsim,
        generate_preset_pass_manager,
        np,
        partial,
        plot_error_map,
        plt,
        pyscf,
        solve_sci_batch,
        subsample,
    )


@app.cell
def _():
    from qc_grader.challenges.qgss_2026 import (
        check_progress,
        grade_lab4c_ex1a,
        grade_lab4c_ex1b,
        grade_lab4c_ex2a,
        grade_lab4c_ex2b,
        grade_lab4c_ex3a,
        grade_lab4c_ex3b,
        grade_lab4c_ex4,
        grade_lab4c_exbonus,
    )

    return (
        check_progress,
        grade_lab4c_ex1a,
        grade_lab4c_ex1b,
        grade_lab4c_ex2a,
        grade_lab4c_ex2b,
        grade_lab4c_ex3a,
        grade_lab4c_ex3b,
        grade_lab4c_ex4,
        grade_lab4c_exbonus,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Throughout the Lab you can use the `check_progress` function to see how many exercises you have completed:
    """)
    return


@app.cell
def _(check_progress):
    check_progress()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Background: Molecular quantum chemistry in 5 minutes

    You do **not** need a chemistry background to complete this lab. This section gives you just enough vocabulary.

    ### Molecules, orbitals, and electrons

    Think of a molecule as a small concert hall.
    The **molecular orbitals** are the seats in that hall.
    The **electrons** are the guests who must be seated according to one strict rule: each seat (orbital) can hold *at most one guest of a given spin* — this is the Pauli exclusion principle.

    Each spatial orbital can host two electrons, one with **spin-α (↑)** and one with **spin-β (↓)**.
    We always track the two spin flavours separately, which is exactly why the bitstrings you will measure later are split into an α half and a β half.

    ### The ground state and why it matters

    The **ground state** is the lowest-total-energy seating arrangement.
    It tells chemists whether a molecule is stable, how strong its bonds are, and whether it will react.
    Computing the ground-state energy accurately is one of the most compelling near-term applications of quantum computers because the number of possible seatings grows *exponentially* — for $n$ orbitals and $N_e$ electrons there are $\binom{n}{N_e}$ arrangements per spin species, which quickly exceeds any classical computer's reach.
    For N₂ in this lab, with 26 active orbitals and 5 electrons per spin, that is already $\binom{26}{5} = 65{,}780$ configurations per spin sector — and the full Hilbert space dimension is the product of both spin sectors: over four billion states.

    Finding the ground state is formally an **eigenvalue problem**:

    $$\hat{H} |\psi_0\rangle = E_0 |\psi_0\rangle$$

    where $|\psi_0\rangle$ is the ground-state wavefunction and $E_0$ is the lowest energy eigenvalue.
    Equivalently, the **variational principle** frames it as a minimization:

    $$E_0 = \min_{\|\psi\|=1} \langle \psi | \hat{H} | \psi \rangle$$

    Any trial state $|\psi\rangle$ you construct gives an **upper bound** on $E_0$: $\langle\psi|\hat{H}|\psi\rangle \geq E_0$.
    This inequality underlies every variational quantum algorithm, including SQD.

    In second quantization the Hamiltonian separates into one- and two-body terms:

    $$\hat{H} = \sum_{pq} h_{pq}\,\hat{a}^\dagger_p \hat{a}_q + \frac{1}{2}\sum_{pqrs} g_{pqrs}\,\hat{a}^\dagger_p \hat{a}^\dagger_q \hat{a}_s \hat{a}_r + E_\text{nuc}$$

    - $h_{pq}$: **one-electron integrals** — kinetic energy and electron–nucleus attraction (`hcore` in the code).
    - $g_{pqrs}$: **two-electron repulsion integrals** — electron–electron Coulomb repulsion (`eri` in the code).
    - $E_\text{nuc}$: constant nuclear repulsion energy.

    SQD solves this problem by projecting $\hat{H}$ onto a small **subspace** — a carefully chosen set of Slater determinants — and diagonalizing it exactly within that subspace.
    The quantum computer's job is to propose which determinants belong there.

    ### Classical reference methods

    Three classical benchmarks frame our plots:

    | Method | What it does | Accuracy |
    |---|---|---|
    | **Hartree–Fock (HF)** | Each electron ignores every other and picks the cheapest seat independently. Fast, but ignores electron *correlation* — the tendency of electrons to dodge each other. | Upper bound on $E_0$; rough estimation. |
    | **CCSD** (Coupled Cluster Singles & Doubles) | Starts from HF, then adds 1- and 2-electron "jumps" out of the HF arrangement using algebraic amplitudes $t_1$ (singles) and $t_2$ (doubles). Captures most correlation. | Provides efficient and reasonable classical estimation of $E_0$. |
    | **Classical selected-CI** (Reference subspace in this lab) | Builds and diagonalizes the Hamiltonian in a small, hand-picked set of Slater determinants. When high-quality determinants are provided, it can approach near-exact accuracy. The reference subspace in this lab is a brute-force proxy: configurations are enumerated by excitation rank with no selection criterion, then diagonalized exactly. If your SQD result beats this baseline, you have demonstrated *quantum utility*: the quantum sampler has found configurations that no brute-force enumeration could reach. | Scales with configuration quality. The lab's brute-force version is typically better than HF but short of CCSD. |

    > **Key point:** We will also *use* CCSD to seed our quantum circuit — its amplitudes describe how electrons want to jump between orbitals, and we transplant that chemical intuition directly into the parameters of the quantum ansatz.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Building the N₂ molecule and its Hamiltonian

    ### The nitrogen molecule

    We study **molecular nitrogen (N₂)**: two nitrogen atoms separated by 2.0 Å.
    This is roughly double N₂'s equilibrium bond length (~1.1 Å) — a stretched geometry where electron correlation effects are more pronounced, making the gap between HF and the exact ground state larger and the quantum computing application more compelling.
    We describe the molecule using the **`cc-pvdz` basis set** — a standard vocabulary of orbital shapes that balances accuracy with computational cost.
    Running Hartree–Fock in this basis gives us 28 spatial orbitals in total.

    ### Active space and frozen orbitals

    Not all orbitals matter equally.
    The innermost **core** orbitals (the 1s electrons of each nitrogen atom) sit deep in energy and essentially never change — they are perfectly happy where they are no matter what the molecule does.
    Computing those orbitals quantum-mechanically would waste precious qubits.

    We therefore **freeze** them:
    - `n_frozen = 2` removes the 2 lowest-energy core orbitals from the quantum treatment.
    - `active_space = range(n_frozen, mol.nao_nr())` is the set of orbitals where the chemically interesting action — bond formation, electron correlation — actually happens.

    This is the **active-space approximation**: solve the full HF over everything, then only treat the active-space electrons on the quantum computer.
    After freezing, we are left with:
    - `num_orbitals` active spatial orbitals → this will equal the number of qubits per spin sector.
    - `(num_elec_a, num_elec_b)` active electrons of spin-α and spin-β.  N₂ is a closed-shell singlet, so `num_elec_a == num_elec_b`.

    The code cell below also extracts the **one-electron integrals** (`hcore`), **two-electron repulsion integrals** (`eri`), and the constant **nuclear repulsion energy** — together these are the numerical representation of $\hat{H}$ restricted to the active space, which the classical eigensolver will diagonalize later.
    """)
    return


@app.cell
def _(pyscf):
    # Build N2 molecule
    mol = pyscf.gto.Mole()
    mol.build(
        atom=[["N", (0, 0, 0)], ["N", (2.0, 0, 0)]],
        basis="cc-pvdz",
    )

    # Define active space
    n_frozen = 2
    active_space = range(n_frozen, mol.nao_nr())

    # Get molecular integrals
    scf = pyscf.scf.RHF(mol).run()
    num_orbitals = len(active_space)
    n_electrons = int(sum(scf.mo_occ[active_space]))
    num_elec_a = (n_electrons + mol.spin) // 2
    num_elec_b = (n_electrons - mol.spin) // 2
    cas = pyscf.mcscf.CASCI(scf, num_orbitals, (num_elec_a, num_elec_b))
    mo = cas.sort_mo(active_space, base=0)
    hcore, nuclear_repulsion_energy = cas.get_h1cas(mo)
    eri = pyscf.ao2mo.restore(1, cas.get_h2cas(mo), num_orbitals)

    # Print molecular information
    print(f"Number of molecular orbitals: {num_orbitals}")
    print(f"Number of electrons (a, b): {(num_elec_a, num_elec_b)}")
    return (
        active_space,
        eri,
        hcore,
        mo,
        mol,
        nuclear_repulsion_energy,
        num_elec_a,
        num_elec_b,
        num_orbitals,
        scf,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Running CCSD to seed the quantum ansatz

    Before we build the quantum circuit, we run **CCSD** classically.
    We are *not* using CCSD as the final answer — that would defeat the purpose.
    We are **mining it for its amplitudes**:

    - `t1[i, a]` — the amplitude for a single electron to "jump" from occupied orbital $i$ to virtual orbital $a$.
    - `t2[i, j, a, b]` — the amplitude for an electron *pair* to scatter from $(i, j)$ to $(a, b)$.

    These amplitudes encode CCSD's chemical intuition about how electrons correlate.
    In the next section, the `ffsim` library will read them and compile them into the rotation angles of the quantum circuit, effectively transplanting classical chemistry knowledge into the quantum device as a high-quality starting guess.
    """)
    return


@app.cell
def _(active_space, mol, pyscf, scf):
    # Get CCSD t2 amplitudes for initializing the ansatz
    ccsd = pyscf.cc.CCSD(scf, frozen=[i for i in range(mol.nao_nr()) if i not in active_space]).run(max_cycle=1000)
    t1 = ccsd.t1
    t2 = ccsd.t2
    return ccsd, t1, t2


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Quantum state preparation: the LUCJ ansatz

    ### What is the LUCJ ansatz?

    The goal of state preparation is to build a quantum circuit that approximates the N₂ ground state well enough that sampling it yields electron configurations close to the true ground state.
    We use the **LUCJ ansatz** — **Local Unitary Cluster Jastrow** — a hardware-efficient parameterized circuit that captures electron correlation through two ingredients:

    1. **Orbital rotations** $e^{i\hat{K}}$: one-body unitaries that mix the molecular orbitals (think of them as rearranging the seats).
    2. **Jastrow factor** $e^{i\sum_{pq} J_{pq}\,\hat{n}_p \hat{n}_q}$: a diagonal interaction that penalizes or rewards pairs of electrons simultaneously occupying orbitals $p$ and $q$ (electrons react to each other's presence).

    One UCJ layer has the form:

    $$U_\mu = e^{i\hat{K}_\mu}\; e^{i\sum_{p<q} J^{(\mu)}_{pq}\,\hat{n}_p \hat{n}_q}\; e^{-i\hat{K}_\mu}$$

    where $\hat{n}_p = a^\dagger_p a_p$ is the occupation-number operator for orbital $p$.
    Here $a^\dagger_p$ **creates** an electron in orbital $p$ and $a_p$ **removes** one — this is the standard **second-quantization** language for many-body quantum systems.
    $\hat{n}_p$ is simply the projector onto the occupied state: it equals 1 if orbital $p$ is occupied and 0 if empty.
    The full ansatz stacks `n_reps` such layers: $U = U_{n_\text{reps}} \cdots U_1$.
    Here we use `n_reps = 1`.

    ### From CCSD amplitudes to circuit parameters

    `ffsim.UCJOpSpinBalanced.from_t_amplitudes(t1, t2, n_reps, interaction_pairs)` reads the CCSD single- and double-excitation amplitudes and compiles them into the rotation angles $K_\mu$ and Jastrow couplings $J_{pq}^{(\mu)}$.
    Intuitively: if CCSD says "orbitals $i$ and $a$ swap strongly", the corresponding orbital rotation in $e^{i\hat{K}}$ gets a large angle.

    **Spin-balanced** means the α (spin-up) and β (spin-down) sectors share the same orbital-rotation parameters — appropriate for a closed-shell singlet like N₂ (same α and β occupations), and it halves the number of free parameters.

    ### Interaction pairs — the hardware constraint

    The Jastrow factor requires two qubits to interact directly.
    The `interaction_pairs` argument tells `ffsim` which pairs of orbitals can interact:

    - `alpha_alpha_indices = [(p, p+1) ...]` — same-spin *nearest-neighbor* interactions along the qubit chain (one line per spin sector on the chip).
    - `alpha_beta_indices` — **cross-spin** interactions: an α qubit at position $p$ couples to a β qubit at position $q$.
      These are **constrained by the device wiring**: the coupling is only hardware-native if the two physical qubits are neighbors on the chip.

    This is the key point of Exercise 1: different IBM devices have different topologies, so the allowed `alpha_beta_indices` differ between a Heron chip and a Nighthawk chip.
    """)
    return


@app.cell
def _(QiskitRuntimeService, plot_error_map):
    service = QiskitRuntimeService()
    backend_hr = service.backend("ibm_kingston")
    plot_error_map(backend_hr)
    return backend_hr, service


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Jordan–Wigner encoding: from orbitals to qubits

    The **Jordan–Wigner (JW) transformation** is the dictionary that maps fermionic orbital states onto qubit states:

    $$\text{orbital } p \text{ occupied} \;\Longleftrightarrow\; \text{qubit } p = |1\rangle, \qquad
      \text{orbital } p \text{ empty} \;\Longleftrightarrow\; \text{qubit } p = |0\rangle$$

    We use $2 \times \texttt{num\_orbitals}$ qubits in total:
    - Qubits $0, \ldots, \texttt{num\_orbitals}-1$ → spin-α occupations
    - Qubits $\texttt{num\_orbitals}, \ldots, 2\cdot\texttt{num\_orbitals}-1$ → spin-β occupations

    This is exactly why, much later in Exercise 2a, a measured bitstring of length `2*num_orbitals` splits cleanly into an α half and a β half.

    Two `ffsim` circuit instructions handle the encoding:
    - `PrepareHartreeFockJW` — sets the initial qubit state to the Hartree–Fock occupation pattern (the first `num_elec_a` α-qubits and `num_elec_b` β-qubits are $|1\rangle$, the rest $|0\rangle$).
    - `UCJOpSpinBalancedJW` — applies the UCJ correlator in the JW qubit basis.

    ### PRE_INIT passes and gate counts

    The `ffsim.qiskit.PRE_INIT` transpiler pass decomposes the high-level `ffsim` gate objects into native hardware gates *before* the main transpilation pass runs.
    Running `count_ops()` with and without `PRE_INIT` shows how many native 2-qubit gates the circuit requires — fewer gates means less accumulated noise.

    The code below shows the complete setup for the **Heron (`ibm_kingston`)** device as a worked example.
    Exercise 1 asks you to redo this mapping for the **Nighthawk (`ibm_miami`)** device.

    ### The SQD workflow: a brief map

    Once the circuit is ready, the rest of this chapter follows a four-step loop:

    1. **Sample** — run the LUCJ circuit on hardware and collect bitstrings.
    2. **Recover configurations** — fix bitstrings that noise has pushed to the wrong electron count.
    3. **Build a subspace** — collect the most frequent (most probable) electron configurations as a basis.
    4. **Diagonalize** $\hat{H}$ in that subspace — get an energy estimate; feed the resulting orbital occupancies back to step 2.

    Each iteration the subspace gets a little smarter.
    """)
    return


@app.cell
def _(num_orbitals):
    # For the Heron device, the alpha-beta interaction happens per every four indicies
    alpha_alpha_indices = [(p, p + 1) for p in range(num_orbitals - 1)]
    alpha_beta_indices_hr = [(p, p) for p in range(0, num_orbitals, 4)]
    alpha_beta_indices_hr = alpha_beta_indices_hr[:5]  # truncate at fifth pair

    print(alpha_beta_indices_hr)
    return alpha_alpha_indices, alpha_beta_indices_hr


@app.cell
def _(
    Barrier,
    CircuitInstruction,
    QuantumCircuit,
    QuantumRegister,
    alpha_alpha_indices,
    alpha_beta_indices_hr,
    display,
    ffsim,
    num_elec_a,
    num_elec_b,
    num_orbitals,
    t1,
    t2,
):
    n_reps = 1
    ucj_op_hr = ffsim.UCJOpSpinBalanced.from_t_amplitudes(
        t1=t1,
        t2=t2,
        n_reps=n_reps,
        interaction_pairs=(alpha_alpha_indices, alpha_beta_indices_hr),
        optimize=True,
        options=dict(maxiter=20),
    )
    nelec = (num_elec_a, num_elec_b)

    # create an empty quantum circuit
    qubits = QuantumRegister(2 * num_orbitals, name="q")
    circuit_hr = QuantumCircuit(qubits)

    # prepare Hartree-Fock state as the reference state and append it to the quantum circuit
    circuit_hr.append(ffsim.qiskit.PrepareHartreeFockJW(num_orbitals, nelec), qubits)

    # apply the UCJ operator to the reference state
    circuit_hr.append(ffsim.qiskit.UCJOpSpinBalancedJW(ucj_op_hr), qubits)

    # investigate into the circuit for execution
    inner_circuit_hr = ffsim.qiskit.PRE_INIT.run(circuit_hr)
    for i in range(2, 0, -1):
        inner_circuit_hr.data.insert(i, CircuitInstruction(Barrier(num_qubits=2*num_orbitals), qubits))
    display(inner_circuit_hr.decompose().draw("mpl", fold=-1))

    # insert final measurement
    circuit_hr.measure_all()
    return circuit_hr, n_reps


@app.cell
def _(backend_hr, circuit_hr, ffsim, generate_preset_pass_manager):
    # select spin a and b layout according to the device topology
    spin_a_layout = [
         21,  36,  41,  42,  43,     56,  63,  64,  65,  77,
         85,  86,  87,  97, 107,    108, 109, 118, 129, 128,
        127, 126, 125, 117, 105,    104
    ]
    spin_b_layout = [
         23,  24,  25,  37,  45,     46,  47,  57,  67,  68,
         69,  78,  89,  90,  91,     98, 111, 112, 113, 114,
        115,  99,  95,  94,  93,     79
    ]

    initial_layout = spin_a_layout + spin_b_layout

    pass_manager = generate_preset_pass_manager(
        optimization_level=3, backend=backend_hr, initial_layout=initial_layout
    )

    # without PRE_INIT passes
    isa_circuit_hr = pass_manager.run(circuit_hr)
    print(f"Gate counts (w/o pre-init passes): {isa_circuit_hr.count_ops()}")

    # with PRE_INIT passes
    # We will use the circuit generated by this pass manager for hardware execution
    pass_manager.pre_init = ffsim.qiskit.PRE_INIT
    isa_circuit_hr = pass_manager.run(circuit_hr)
    print(f"Gate counts (w/ pre-init passes): {isa_circuit_hr.count_ops()}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise 1: Map LUCJ circuit for the Nighthawk device

    Now let's port the same circuit to the **Nighthawk (`ibm_miami`)** device.
    Run the error-map cell below and compare the connectivity diagram to Heron's.
    Notice how the α and β qubit rails are wired differently — that changes which cross-spin interaction pairs are hardware-native.

    > **No access to `ibm_miami`?** Use `FakeMiami` instead — uncomment the second line in the cell below. `FakeMiami` reproduces the Nighthawk device topology (same qubit graph and basis gates) so the circuit mapping and layout exercises work identically; the only difference is that it simulates noise rather than running on real hardware.
    """)
    return


@app.cell
def _(plot_error_map, service):
    backend_nh = service.backend("ibm_miami")
    # # Use this command to use FakeMiami if you don't have access to ibm_miami
    # backend_nh = FakeMiami()

    plot_error_map(backend_nh)
    return (backend_nh,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="exercise_1a"></a>
    <div class="alert alert-block alert-success">

    <b>Exercise 1a: Select the alpha–beta interaction pairs for the Nighthawk device</b>

    **Your Goal:** Fill `alpha_beta_indices_nh` with the cross-spin interaction pairs appropriate for the Nighthawk device topology.

    **Background:** Recall from Section 2 that each `(p, q)` tuple in `alpha_beta_indices` means "the Jastrow factor couples α-orbital $p$ to β-orbital $q$, and those two qubits must be physically adjacent on the chip."

    - On **Heron (`ibm_kingston`)**, the α and β qubit chains only touch at every 4th site, so we used `[(p, p) for p in range(0, num_orbitals, 4)]` truncated to 5 pairs (there are only 5 hardware-adjacent α–β crossings).
    - On **Nighthawk (`ibm_miami`)**, the α and β rails can be laid next to each other so that $p$-th qubit on the α chain can interact with the $p$-th qubit on the β chain for *every* $p$. There is no need to skip indices.

    **Hint:**
    - **(Recommended)** You can make 24 qubit pairs (truncate at 24) rather than pairing all qubits. This makes it easier to map the circuit to the Nighthawk topology.
    - You may notice that you cannot arrange every α and β pair side-by-side, but don't worry about that at this stage.

    </div>
    """)
    return


@app.cell
def _():
    # Select alpha-beta interaction pairs according to the Nighthawk device topology
    # ---- TODO : Task 1a ----
    alpha_beta_indices_nh = []
    # ---- End of TODO : Task 1a ----

    print(alpha_beta_indices_nh)
    return (alpha_beta_indices_nh,)


@app.cell
def _(alpha_beta_indices_nh, grade_lab4c_ex1a):
    grade_lab4c_ex1a(alpha_beta_indices_nh)
    return


@app.cell
def _(
    Barrier,
    CircuitInstruction,
    QuantumCircuit,
    QuantumRegister,
    alpha_alpha_indices,
    alpha_beta_indices_nh,
    display,
    ffsim,
    n_reps,
    num_elec_a,
    num_elec_b,
    num_orbitals,
    t1,
    t2,
):
    ucj_op_nh = ffsim.UCJOpSpinBalanced.from_t_amplitudes(t1=t1, t2=t2, n_reps=n_reps, interaction_pairs=(alpha_alpha_indices, alpha_beta_indices_nh), optimize=True, options=dict(maxiter=20))
    nelec_1 = (num_elec_a, num_elec_b)
    qubits_1 = QuantumRegister(2 * num_orbitals, name='q')
    circuit_nh = QuantumCircuit(qubits_1)
    circuit_nh.append(ffsim.qiskit.PrepareHartreeFockJW(num_orbitals, nelec_1), qubits_1)
    circuit_nh.append(ffsim.qiskit.UCJOpSpinBalancedJW(ucj_op_nh), qubits_1)
    inner_circuit_nh = ffsim.qiskit.PRE_INIT.run(circuit_nh)
    for i_1 in range(2, 0, -1):
        inner_circuit_nh.data.insert(i_1, CircuitInstruction(Barrier(num_qubits=2 * num_orbitals), qubits_1))
    display(inner_circuit_nh.decompose().draw('mpl', fold=-1))
    # create an empty quantum circuit
    # prepare Hartree-Fock state as the reference state and append it to the quantum circuit
    # apply the UCJ operator to the reference state
    # investigate the circuit for execution
    # insert final measurement
    circuit_nh.measure_all()
    return circuit_nh, nelec_1


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="exercise_1b"></a>
    <div class="alert alert-block alert-success">

    <b>Exercise 1b: Define the qubit layout for the Nighthawk device</b>

    **Your Goal:** Provide `spin_a_layout` and `spin_b_layout` — lists of exactly `num_orbitals` (= 26) physical qubit indices each — that correctly map the α and β spin-orbital chains onto Nighthawk's hardware.

    **Background:** `initial_layout` instructs the transpiler to place logical qubit $p$ on physical qubit `initial_layout[p]`. A good layout must satisfy two requirements simultaneously:

    1. **Connectivity within each spin sector:** the same-spin nearest-neighbor interactions `alpha_alpha_indices = [(p, p+1) ...]` require physical qubits $p$ and $p+1$ within each list to be hardware-adjacent (connected by a two-qubit gate line on the chip). Each list should therefore trace a *connected path* through the device graph.

    2. **α–β adjacency:** according to the pairs provided in exercise 1a, place the pairs as close to each other as possible. It is perfectly fine to use a few swaps if needed.

    **Hint:**
    - Not every α and β pair will sit side-by-side. Applying a few swap operations is fine, as long as the swaps can operate in parallel, keeping the circuit depth minimal.
    - **(Optional)** If you want to tackle a more advanced challenge, try pairing all 26 qubits in the previous exercise and mapping them to the Nighthawk. The passing criteria is quite challenging and the grader result may fluctuate with the transpiler seed. Try a few different seeds to get a better transpilation result.
    </div>
    """)
    return


@app.cell
def _(backend_nh, circuit_nh, ffsim, generate_preset_pass_manager):
    # select spin a and b layout according to the device topology
    # ---- TODO : Task 1b ----
    spin_a_layout_1 = []
    spin_b_layout_1 = []
    initial_layout_1 = spin_a_layout_1 + spin_b_layout_1
    pass_manager_1 = generate_preset_pass_manager(optimization_level=3, backend=backend_nh, initial_layout=initial_layout_1)
    isa_circuit_nh = pass_manager_1.run(circuit_nh)
    print(f'Gate counts (w/o pre-init passes): {isa_circuit_nh.count_ops()}')
    pass_manager_1.pre_init = ffsim.qiskit.PRE_INIT
    # ---- End of TODO : Task 1b ----
    isa_circuit_nh = pass_manager_1.run(circuit_nh)
    # without PRE_INIT passes
    # with PRE_INIT passes
    # We will use the circuit generated by this pass manager for hardware execution
    print(f'Gate counts (w/ pre-init passes): {isa_circuit_nh.count_ops()}')
    return (initial_layout_1,)


@app.cell
def _(alpha_beta_indices_nh, grade_lab4c_ex1b, initial_layout_1):
    grade_lab4c_ex1b(initial_layout_1, alpha_beta_indices_nh, seed=None)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Quantum Sampling

    With the circuit mapped to Nighthawk's topology, we submit 2,000 shots to the device.
    Each **shot** measures all `2*num_orbitals` qubits and returns one **bitstring** — a binary snapshot of which orbitals are occupied at that moment.
    Physically, each bitstring is *one proposed electron configuration*: a candidate for a basis state of the ground state.

    The collection of all 2,000 bitstrings, together with how often each distinct configuration appears, is the raw material that SQD will process.

    > **Note on runtime:** Running a real hardware job takes 10 seconds on `ibm_miami` or 2 seconds on `ibm_kingston`.
    > To keep this notebook self-contained, the cell below submits the job and saves the `job_id`.
    > The *following* cell retrieves the pre-computed results from that saved ID — you do not need to resubmit.
    """)
    return


@app.cell
def _(job):
    # # Option 1: if you have an access to the Nighthawk device, try running the square-lattice circuit.
    # sampler = Sampler(mode=backend_nh)
    # job = sampler.run([isa_circuit_nh], shots=2_000)

    # # Option 2: if you don't have an access to the Nighthawk device, you can run Heron fitted circuit.
    # sampler = Sampler(mode=backend_hr)
    # job = sampler.run([isa_circuit_hr], shots=2_000)

    job_id = job.job_id()
    print(f"Submitted job {job_id}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The cell below retrieves the completed job and converts the raw measurement outcomes into two arrays:

    - `raw_bitstrings` — integer array of shape `(n_unique, 2*num_orbitals)` where each row is a distinct bitstring (each element is 0 or 1).
    - `raw_probs` — float array of length `n_unique` giving the empirical probability of each bitstring; `raw_probs[k]` is the fraction of shots that produced `raw_bitstrings[k]`.
    """)
    return


@app.cell
def _(bit_array_to_arrays, service):
    # Retrieve job using the job id
    job_id_1 = 'd8oks6e8aqlc73egmkl0'
    job = service.job(job_id_1)
    primitive_result = job.result()
    pub_result = primitive_result[0]
    bit_array = pub_result.data.meas
    # Convert BitArray into bitstring and probability arrays
    raw_bitstrings, raw_probs = bit_array_to_arrays(bit_array)
    return bit_array, job, raw_bitstrings, raw_probs


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise 2: Examine the resulting bitstrings

    Once the sampling is done, it's time to understand what we have.
    The two code cells below let you inspect the shape and contents of `raw_bitstrings` before you begin processing.
    Run them first, then complete the two exercises.
    """)
    return


@app.cell
def _(raw_bitstrings):
    print(raw_bitstrings.shape)
    return


@app.cell
def _(raw_bitstrings):
    print(raw_bitstrings[0])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="exercise_2a"></a>
    <div class="alert alert-block alert-success">

    <b>Exercise 2a: Reshape the raw bitstrings into spin sectors</b>

    **Your Goal:** Implement `reshape_bitstring` to divide the **spin-α** and **spin-β** bitstrings from the experiment results.

    **Background:** The Jordan–Wigner encoding places the spin-α qubits in the *first* block of each bitstring and the spin-β qubits in the *second* block.
    A `1` at position $p$ in the α block means "α-orbital $p$ is occupied"; `0` means empty.
    Separating the two spin sectors lets us:
    - Check the electron count per spin independently (Exercise 2b).
    - Apply spin-specific corrections during configuration recovery (Exercise 3).

    **Hint:**
    - The shape of the `raw_bitstrings` is **(2000, 52)**. You should get an array of shape **(2000, 2, 26)**.
    - **Bit-ordering caution:** Qiskit returns measurement results in *little-endian* (last qubit measured = first bit in string). After reshaping, verify which block is α by printing `reshaped_bitstrings[0, :]` and checking whether the block matches with the α bitstring. You may need to flip the spin-block ordering so that index 0 is always α.
    - Cross-check with the raw `raw_bitstrings[0]` printed above.

    </div>
    """)
    return


@app.cell
def _(np, num_orbitals, raw_bitstrings):
    def reshape_bitstring(
        bitstrings: np.ndarray,
        num_orbitals: int
    ) -> np.ndarray:

        # ---- TODO : Task 2a ----

        # ---- End of TODO : Task 2a ----

        return reshaped_bitstrings

    reshaped_bitstrings = reshape_bitstring(raw_bitstrings, num_orbitals)
    print(reshaped_bitstrings[0, :])
    return reshape_bitstring, reshaped_bitstrings


@app.cell
def _(grade_lab4c_ex2a, raw_bitstrings, reshape_bitstring):
    grade_lab4c_ex2a(reshape_bitstring, raw_bitstrings)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="exercise_2b"></a>
    <div class="alert alert-block alert-success">

    <b>Exercise 2b: Count electrons per sample (Hamming weight)</b>

    **Your Goal:** Implement `hamming_weight` that takes the reshaped bitstring array and returns an integer array giving the number of occupied orbitals for each spin sector in each sample.

    **Background:** The **Hamming weight** of a binary string is simply its number of 1s.
    In our context, Hamming weight = number of electrons of that spin in that sample.

    A *valid* sample must have exactly 5 spin-α electrons **and** 5 spin-β electrons (particle number conservation).
    In a noiseless world, every shot would be valid. On real hardware, bit-flip errors and other noise mechanisms push some bitstrings outside the correct particle-number sector — those samples are physically meaningless and would corrupt the diagonalization if used directly.

    Counting the Hamming weight is the first step to detecting these bad samples.

    **Hint:** Sum over the last axis (the orbital axis).

    </div>
    """)
    return


@app.cell
def _(np, reshaped_bitstrings, weight):
    def hamming_weight(bitstrings: np.ndarray) -> np.ndarray:

        # ---- TODO : Task 2b ----

        # ---- End of TODO : Task 2b ----

        return weight

    print(hamming_weight(reshaped_bitstrings)[0])
    return (hamming_weight,)


@app.cell
def _(grade_lab4c_ex2b, hamming_weight):
    grade_lab4c_ex2b(hamming_weight)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The cell below checks how many samples already have the correct electron counts — i.e., how many shots are "valid" before any repair. Don't be surprised if this count is zero — bit-flip errors on real hardware easily push samples outside the correct particle-number sector.
    """)
    return


@app.cell
def _(hamming_weight, nelec_1, np, raw_probs, reshaped_bitstrings):
    print(int(2000.0 * np.sum(raw_probs[np.all(hamming_weight(reshaped_bitstrings) == nelec_1)])))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise 3: Recover the bitstring

    ### Why configuration recovery is necessary

    The true molecular ground state lives entirely within the **fixed-particle-number sector**: configurations with exactly `(num_elec_a, num_elec_b)` electrons.
    Quantum mechanics conserves particle number — the physical molecule cannot spontaneously gain or lose electrons.

    However, a real quantum device introduces **bit-flip errors** (and other noise) that change some `0`s to `1`s and vice versa.
    A single bit-flip moves a bitstring *out* of the physical sector; suddenly, the sample reports the wrong number of electrons.
    That sample is physically meaningless and, if fed directly to the diagonalizer, would contaminate the subspace with non-physical configurations.

    **Configuration recovery** repairs each broken sample by flipping the minimum number of bits needed to restore the correct electron count, choosing *which* bits to flip based on our current best estimate of each orbital's average occupancy.

    ### Initializing occupancy from Hartree–Fock

    The recovery algorithm needs a prior estimate of "how occupied is each orbital, on average?"
    We bootstrap this with the **Hartree–Fock occupancy**: the `num_elec_a` highest-index orbitals are fully occupied (occupancy = 1), the rest are empty (occupancy = 0).
    As the SQD loop progresses, this is replaced by the actual orbital occupancies measured from the diagonalized quantum state — so the recovery improves with each iteration.
    """)
    return


@app.cell
def _(np, num_elec_a, num_orbitals):
    initial_occupancy = np.zeros((2, num_orbitals), dtype=float)
    initial_occupancy[:, -num_elec_a:] = 1.
    print(initial_occupancy)
    return (initial_occupancy,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="exercise_3a"></a>
    <div class="alert alert-block alert-success">

    <b>Exercise 3a: Define the bit-flip probability function</b>

    **Your Goal:** Implement `weight_flip_0_to_1(occupancy)` which, given an array of orbital occupancies in $[0, 1]$, returns the probability weight for flipping each orbital from empty (0) to occupied (1).

    **Background:** When a sample is *missing* an electron (too few 1s), we must flip some empty orbital to occupied.
    We want to preferentially fill orbitals that are *usually* occupied — because the true ground state probably has those orbitals filled.
    Conversely, we should almost never fill an orbital that is usually empty.

    The function:

    $$W_{0\to1}(\text{occ}) = e^{\text{occ}} - 1, \qquad 0 \le \text{occ} \le 1$$

    captures exactly this behavior:
    - $W_{0\to1}(0) = 0$ — never fill a never-occupied orbital.
    - $W_{0\to1}(1) = e - 1 \approx 1.718$ — strongly prefer filling an always-occupied orbital.
    - Monotonically increasing in between.

    The companion function `weight_flip_1_to_0(occ) = weight_flip_0_to_1(1 - occ)` is already provided; removing an electron favors orbitals that are usually empty (high probability of being 0).

    </div>
    """)
    return


@app.cell
def _(np, prob):
    def weight_flip_0_to_1(occupancy: np.ndarray) -> np.ndarray:

        # ---- TODO : Task 3a ----

        # ---- End of TODO : Task 3a ----

        return prob

    def weight_flip_1_to_0(occupancy):
        return weight_flip_0_to_1(1-occupancy)

    return (weight_flip_0_to_1,)


@app.cell
def _(grade_lab4c_ex3a, weight_flip_0_to_1):
    grade_lab4c_ex3a(weight_flip_0_to_1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="exercise_3b"></a>
    <div class="alert alert-block alert-success">

    <b>Exercise 3b: Recover bitstring configurations to the correct electron count</b>

    **Your Goal:** Complete the `recover_configurations` function by filling in the three-branch correction logic inside the per-spin loop.

    **Background — the algorithm, step by step:**

    The outer loop iterates over every bitstring sample. For each sample and each spin sector `i` (0 = α, 1 = β):

    1. Compute `weight[i]` = Hamming weight = number of electrons in sector `i` (you wrote this in Exercise 2b).
    2. Compare `weight[i]` to `num_elec[i]`:

       - **Too few electrons** (`weight[i] < num_elec[i]`): we must flip `num_elec[i] - weight[i]` empty bits to 1.
         - Find empty orbitals
         - Get flip weights for those candidates
         - Normalize the weights to make a probability distribution
         - Randomly select which to flip
         - Set the chosen bits to `True`

       - **Too many electrons** (`weight[i] > num_elec[i]`): we must flip `weight[i] - num_elec[i]` occupied bits to 0.
         - Mirror the procedure above, but make sure that you are choosing occupied bits to flip.

       - **Exactly right** (`weight[i] == num_elec[i]`): leave the spin sector unchanged.

    **Hint:** Each branch needs four lines: find candidates with `np.where`, compute and normalize probabilities, call `rand_seed.choice` to choose which bit to flip, and flip the bits.

    **Note:** The output format: each corrected bitstring is converted to a string and accumulated into `corrected_dict` (a `defaultdict` that merges any bitstrings that end up identical after correction).

    </div>
    """)
    return


app._unparsable_cell(
    r"""
    def recover_configurations(
        bitstrings: np.ndarray,
        probs: np.ndarray,
        occupancy: np.ndarray,
        num_orbitals: int,
        num_elec: tuple[int, int],
        rand_seed: np.random.Generator,
    ) -> tuple[np.ndarray, np.ndarray]:
        corrected_dict: defaultdict[str, float] = defaultdict(float)
        for bitstring, freq, weight in zip(bitstrings, probs, hamming_weight(bitstrings)):
            bs_corrected = bitstring.copy()
            for i in range(2):
                # ---- TODO : Task 3b ----



                # ---- End of TODO : Task 3b ----
            bs_str = "".join("1" if bit else "0" for bit in bs_corrected.flatten())
            corrected_dict[bs_str] += freq

        bs_mat_out = np.array([[bit == "1" for bit in bs] for bs in corrected_dict]).reshape(-1, 2, num_orbitals)
        freqs_out = np.array([f for f in corrected_dict.values()])
        freqs_out = np.abs(freqs_out) / np.sum(np.abs(freqs_out))

        return bs_mat_out, freqs_out

    recovered_bitstrings, recovered_probs = recover_configurations(
        reshaped_bitstrings, raw_probs, initial_occupancy, num_orbitals, nelec, np.random.default_rng())
    """,
    name="_"
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The cell below shows how many samples are valid (correct electron count) **after** configuration recovery — compare to the pre-recovery number from Exercise 2b.
    """)
    return


@app.cell
def _(hamming_weight, nelec_1, np, recovered_bitstrings, recovered_probs):
    print(np.rint(2000.0 * np.sum(recovered_probs[np.all(hamming_weight(recovered_bitstrings) == nelec_1, axis=1)])).astype(int))
    return


@app.cell
def _(grade_lab4c_ex3b, recover_configurations):
    grade_lab4c_ex3b(recover_configurations)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### From recovered bitstrings to the diagonalization subspace

    With all samples now in the correct particle-number sector, we prepare them for diagonalization:

    1. **`subsample`** splits the recovered configurations into `num_batches` independent batches of `samples_per_batch` samples each. Running the eigensolver on multiple independent batches gives us variance estimates (the box plot later shows the spread) and reduces the chance of getting stuck in an unlucky set of configurations.

    2. **`bitstring_matrix_to_integers`** packs each binary bitstring into a single Python integer — the standard "determinant label" format that the selected-CI eigensolver `solve_sci_batch` expects.
       These integer labels are called **CI strings** (Configuration Interaction strings): each integer encodes which orbitals are occupied, uniquely identifying one **Slater determinant** — a properly antisymmetrized product of single-electron orbital states that satisfies the Pauli exclusion principle and represents one valid electron configuration.

    3. **`build_subspace`** takes the CI strings, deduplicates within each batch, sorts by marginal probability (most-sampled first), optionally prepends a user-specified `include` set, and truncates to `max_dim` configurations per spin. The result is the **subspace basis**: the set of Slater determinants the Hamiltonian will be projected onto.
    """)
    return


@app.cell
def _(np, num_orbitals, recovered_bitstrings, recovered_probs, subsample):
    subsamples = np.array(subsample(recovered_bitstrings.reshape(-1, 2*num_orbitals), recovered_probs, samples_per_batch=20, num_batches=5))
    subsamples = subsamples.reshape(*subsamples.shape[:-1], 2, -1)
    print(subsamples.shape)
    print(subsamples[4, 19])
    return (subsamples,)


@app.cell
def _(bitstring_matrix_to_integers, np, subsamples):
    ci_strs = np.array([bitstring_matrix_to_integers(samples[:, i]) for samples in subsamples for i in range(2)])
    ci_strs = ci_strs.reshape(-1, 2, ci_strs.shape[-1])
    print(ci_strs.shape)
    print(ci_strs[0])
    return (ci_strs,)


@app.cell
def _(ci_strs, np):
    def build_subspace(subsamples, include=np.empty((2, 0), dtype=int), max_dim=(None, None)):

        subspaces = []
        for samples in subsamples:
            subspace_list = []
            for i in range(2):

                # Get the single-spin bitstrings and counts.
                bitstrings, counts = np.unique(samples[i], return_counts=True)

                # Sort the single-spin bitstrings in descending order by marginal probability.
                bitstrings = bitstrings[np.argsort(counts)[::-1]]
            
                # Prioritize explicitly requested bitstrings, then sampled bitstrings
                subspace = np.concatenate((include[i], bitstrings))

                # Get unique values while preserving the original order
                _, indices = np.unique(subspace, return_index=True)
                indices.sort()
                subspace = subspace[indices]

                # Truncate bitstrings to the maximum dimension.
                subspace = subspace[:max_dim[i]]
                subspace.sort()

                subspace_list.append(subspace)
            subspaces.append(subspace_list)

        return subspaces

    subspace = build_subspace(ci_strs, max_dim=(15, 15))
    print(np.array(subspace).shape)
    return (build_subspace,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQD loop parameters

    Before running the self-consistent loop, here is what each parameter controls:

    | Parameter | Meaning |
    |---|---|
    | `max_iterations` | How many recover → subsample → diagonalize cycles to run. More iterations let the occupancy estimate converge. |
    | `num_batches` | Number of independent subspace batches per iteration. More batches → better statistics (wider box plot range). |
    | `samples_per_batch` | Configurations per batch. Larger → richer subspace but more classical eigensolver work. |
    | `max_dim` | Maximum number of Slater determinants per spin sector in the subspace. Controls the dimension of the Hamiltonian matrix. |
    """)
    return


@app.cell
def _(SCIResult, np, nuclear_repulsion_energy, partial, solve_sci_batch):
    # Seed
    seed=142

    # SQD options
    max_iterations = 5

    # Eigenstate solver options
    num_batches = 5
    samples_per_batch = 500
    max_dim = (300, 300)
    max_cycle = 200

    # Pass options to the built-in eigensolver. If you just want to use the defaults,
    # you can omit this step, in which case you would not specify the sci_solver argument
    # in the call to diagonalize_fermionic_hamiltonian below.
    sci_solver = partial(solve_sci_batch, spin_sq=0.0, max_cycle=max_cycle)

    # List to capture intermediate results
    result_history = []

    def callback(results: list[SCIResult]):
        result_history.append(results)
        iteration = len(result_history)
        print(f"Iteration {iteration}")
        for i, result in enumerate(results):
            print(f"\tSubsample {i+1}")
            print(f"\t\tEnergy: {result.energy + nuclear_repulsion_energy}")
            print(f"\t\tSubspace dimension: {np.prod(result.sci_state.amplitudes.shape)}")

    return (
        callback,
        max_dim,
        max_iterations,
        num_batches,
        samples_per_batch,
        seed,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### The self-consistent SQD loop

    The loop below implements the four-step SQD cycle end-to-end:

    1. **Recover** — call `recover_configurations` using the *current* `current_occupancies` as the flip-probability prior.
    2. **Subsample** — draw `num_batches` independent batches of `samples_per_batch` configurations.
    3. **Build subspace** — convert to CI strings and call `build_subspace` to get the Slater determinant basis.
    4. **Diagonalize** — call `sci_solver` to project and diagonalize $\hat{H}$ in that subspace.

    After diagonalization, the key feedback step is:
    ```python
    current_occupancies = current_result.orbital_occupancies
    ```
    The eigenvector produced by the solver tells us how occupied each orbital is on average in the approximate ground state.
    This updated occupancy prior feeds back into step 1 in the *next* iteration, making the configuration recovery progressively more accurate.
    The loop runs for `max_iterations` cycles and tracks the best (lowest-energy) result seen across all batches and iterations.
    """)
    return


@app.cell
def _(
    SCIResult,
    bit_array,
    bit_array_to_arrays,
    bitstring_matrix_to_integers,
    build_subspace,
    callback,
    cast,
    copy,
    eri,
    hcore,
    initial_occupancy,
    max_dim,
    max_iterations,
    nelec_1,
    np,
    num_batches,
    num_orbitals,
    recover_configurations,
    reshape_bitstring,
    samples_per_batch,
    seed,
    solve_sci_batch,
    subsample,
):
    result_history_1 = []
    rng = np.random.default_rng(seed)
    current_occupancies = initial_occupancy
    best_result = None
    sci_solver_1 = solve_sci_batch
    raw_bitstrings_1, raw_probs_1 = bit_array_to_arrays(bit_array)
    for _ in range(max_iterations):
    # Convert BitArray into bitstring and probability arrays
        reshaped_bitstrings_1 = reshape_bitstring(raw_bitstrings_1, num_orbitals)
        bitstrings, probs = recover_configurations(reshaped_bitstrings_1, raw_probs_1, current_occupancies, num_orbitals, nelec_1, rand_seed=rng)
    # Run configuration recovery loop
        subsamples_1 = np.array(subsample(bitstrings.reshape(-1, 2 * num_orbitals), probs, samples_per_batch=samples_per_batch, num_batches=num_batches, rand_seed=rng))
        subsamples_1 = subsamples_1.reshape(*subsamples_1.shape[:-1], 2, -1)
        ci_strs_1 = np.array([bitstring_matrix_to_integers(samples[:, i]) for samples in subsamples_1 for i in range(2)])
        ci_strs_1 = ci_strs_1.reshape(-1, 2, ci_strs_1.shape[-1])  # If we do have average orbital occupancy information, use it to refine the
        subspace_1 = build_subspace(ci_strs_1, max_dim=max_dim)  # full set of noisy configurations
        results = sci_solver_1(subspace_1, hcore, eri, num_orbitals, nelec_1)
        callback(results)
        best_result_in_batch = min(results, key=lambda result: result.energy)
        if best_result is None or best_result_in_batch.energy < best_result.energy:
            best_result = copy.deepcopy(best_result_in_batch)  # Subsample batches of bitstrings
        current_result = copy.deepcopy(best_result_in_batch)
        current_occupancies = current_result.orbital_occupancies
    # best_result is not None because there must have been at least one iteration
    best_result = cast(SCIResult, best_result)  # Convert bitstrings to CI strings and include requested and carryover strings  # Run diagonalization  # Call callback function  # Get best result from batch  # Check if the energy is the lowest seen so far  # Save the current result and occupancies
    return best_result, result_history_1, sci_solver_1


@app.cell
def _(best_result, ccsd, nuclear_repulsion_energy, plt, result_history_1, scf):
    print(f'Best energy = {best_result.energy + nuclear_repulsion_energy}')
    plt.axhline(scf.e_tot, color='C0', label='HF')
    plt.axhline(ccsd.e_tot, color='C1', label='CCSD')
    plt.boxplot([x.energy + nuclear_repulsion_energy for results in result_history_1 for x in results], tick_labels=['Original SQD'])
    plt.legend(loc='upper right')
    plt.show()
    # Will submit the best subspace basis
    best_subspace = (best_result.sci_state.ci_strs_a, best_result.sci_state.ci_strs_b)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You may see that the original SQD method finds a better energy estimate than the HF state — this is already a non-trivial result, as it shows the quantum samples are steering the diagonalization into a physically meaningful region of Hilbert space.
    However, the result is not yet as good as the classical CCSD benchmark.

    The gap between SQD and CCSD can have many causes. The most direct lever is the **size of the subspace**: a larger subspace captures more of the ground-state wavefunction, but diagonalizing it demands significantly more classical compute — scaling up can require anything from a high-performance workstation to a full HPC cluster.

    Here we focus instead on another major contributor to this gap: the limitations of pure sampling. Hardware noise and finite shot counts mean the sampler misses some chemically important electron configurations — particularly configurations that differ from the HF reference by only one or two orbital occupancies. These near-HF configurations contribute strongly to the ground state but may be suppressed in the measured distribution by hardware noise.

    **Exercise 4 directly addresses this gap** by augmenting the sampled subspace with a set of classically enumerated reference determinants.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise 4: Augment SQD with a classical reference subspace

    ### Reference subspace

    Before combining classical and quantum subspaces, let's first see what happens if we diagonalize in a *purely classical, physically motivated* subspace — no quantum samples at all.

    As introduced in the Background, **classical selected-CI** is a family of methods where chemists use perturbation theory or physical intuition to iteratively identify and include the most influential Slater determinants. The accuracy of the result depends directly on the quality of that selection.

    The **reference subspace in this lab** is a simpler, brute-force proxy for this method. Rather than applying any selection criterion, we enumerate all low-excitation-rank configurations by filling orbitals from the lowest energy up and keep the first 300. These **reference determinants** require no chemical insight to construct — just systematic enumeration — making them a reproducible and computationally cheap classical baseline.

    As noted in the Background, this brute-force approach typically achieves an energy better than HF but short of CCSD. It serves as our **classical baseline for quantum utility**: if your SQD result beats it, the quantum samples have contributed configurations that classical enumeration alone would miss.

    We enumerate these determinants systematically using `itertools.combinations`:
    """)
    return


@app.cell
def _(combinations):
    print(list(combinations(range(5), 3)))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="exercise_4"></a>
    <div class="alert alert-block alert-success">

    <b>Exercise 4: Build a classical reference subspace</b>

    **Your Goal:** Construct `ref_bitstrings` — up to 300 Slater determinants representing the lowest-excitation-rank configurations around the HF reference — and convert them to `ref_ci_strings` suitable for the eigensolver.

    **Background:** Returning to our concert-hall analogy: instead of hoping the quantum sampler stumbles upon the most important seating arrangements, we systematically enumerate all *front-row* configurations — those where electrons fill the lowest available orbitals first — and hand them directly to the eigensolver. Unlike true classical selected-CI, where chemists use perturbation theory to identify the most influential determinants, this is a brute-force enumeration: no selection criterion is applied, just the first 300 lowest-excitation-rank configurations. As noted in the Background, this typically yields an energy between HF and CCSD and serves as the classical baseline to beat.

    **Hint:**
    - Consider starting from a fully occupied bitstring and unoccupying orbitals from the highest-energy ones first.
    - Apply `bitstring_matrix_to_integers` to convert to CI string format.
    - Remember to provide both α and β strings for the diagonalizer.

    </div>
    """)
    return


@app.cell
def _():
    # ---- TODO : Task 4 ----



    # ---- End of TODO : Task 4 ----
    return


@app.cell
def _(grade_lab4c_ex4, ref_ci_strings):
    grade_lab4c_ex4(ref_ci_strings)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now try diagonalizing the Hamiltonian in this purely classical reference subspace:
    """)
    return


@app.cell
def _(
    eri,
    hcore,
    nelec_1,
    np,
    nuclear_repulsion_energy,
    num_orbitals,
    ref_ci_strings,
    sci_solver_1,
):
    ref_result = sci_solver_1([ref_ci_strings], hcore, eri, num_orbitals, nelec_1)[0]
    print(f'Reference Subspace Energy: {ref_result.energy + nuclear_repulsion_energy}')
    print(f'Subspace dimension: {np.prod(ref_result.sci_state.amplitudes.shape)}')
    return (ref_result,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You may find that the reference subspace energy is **lower** than the original (pure quantum sampling) SQD result.
    This confirms that the hand-picked low-energy configurations are genuinely important for the ground state, and that the quantum sampler alone may drop some of them due to hardware noise.

    ### Combining quantum samples with a classical reference subspace

    The most powerful approach combines the two sources:
    - **Pin** a set of reference determinants as a guaranteed anchor (`include = ref_ci_strings[:, :100]` — first 100 configurations).
    - Let the quantum sampler supply the remaining `max_dim - 100` configurations per batch as usual.

    Every diagonalization then starts from a solid classical foundation while the quantum device explores the complementary part of the space.
    How do you expect the result to compare to the pure-sampling and pure-reference cases?
    """)
    return


@app.cell
def _(
    SCIResult,
    bit_array,
    bit_array_to_arrays,
    bitstring_matrix_to_integers,
    build_subspace,
    cast,
    copy,
    eri,
    hcore,
    initial_occupancy,
    max_dim,
    max_iterations,
    nelec_1,
    np,
    nuclear_repulsion_energy,
    num_batches,
    num_orbitals,
    recover_configurations,
    ref_ci_strings,
    reshape_bitstring,
    samples_per_batch,
    seed,
    solve_sci_batch,
    subsample,
):
    # List to capture intermediate results
    pm_result_history = []

    def callback_1(results: list[SCIResult]):
        pm_result_history.append(results)
        iteration = len(pm_result_history)
        print(f'Iteration {iteration}')
        for i, result in enumerate(results):
            print(f'\tSubsample {i}')
            print(f'\t\tEnergy: {result.energy + nuclear_repulsion_energy}')
            print(f'\t\tSubspace dimension: {np.prod(result.sci_state.amplitudes.shape)}')
    include = ref_ci_strings[:, :100]
    # We are pinning the 100 lowest-excitation-rank reference determinants during the SQD loop.
    # The remaining entries are filled from quantum samples as usual.
    rng_1 = np.random.default_rng(seed)  # Pin 100 reference determinants
    current_occupancies_1 = initial_occupancy
    best_result_1 = None
    sci_solver_2 = solve_sci_batch
    raw_bitstrings_2, raw_probs_2 = bit_array_to_arrays(bit_array)
    for _ in range(max_iterations):
        reshaped_bitstrings_2 = reshape_bitstring(raw_bitstrings_2, num_orbitals)
    # Convert BitArray into bitstring and probability arrays
        bitstrings_1, probs_1 = recover_configurations(reshaped_bitstrings_2, raw_probs_2, current_occupancies_1, num_orbitals, nelec_1, rand_seed=rng_1)
        subsamples_2 = np.array(subsample(bitstrings_1.reshape(-1, 2 * num_orbitals), probs_1, samples_per_batch=samples_per_batch, num_batches=num_batches, rand_seed=rng_1))
    # Run configuration recovery loop
        subsamples_2 = subsamples_2.reshape(*subsamples_2.shape[:-1], 2, -1)
        ci_strs_2 = np.array([bitstring_matrix_to_integers(samples[:, i]) for samples in subsamples_2 for i in range(2)])
        ci_strs_2 = ci_strs_2.reshape(-1, 2, ci_strs_2.shape[-1])
        subspace_2 = build_subspace(ci_strs_2, include, max_dim=max_dim)  # If we do have average orbital occupancy information, use it to refine the
        results_1 = sci_solver_2(subspace_2, hcore, eri, num_orbitals, nelec_1)  # full set of noisy configurations
        callback_1(results_1)
        best_result_in_batch_1 = min(results_1, key=lambda result: result.energy)
        if best_result_1 is None or best_result_in_batch_1.energy < best_result_1.energy:
            best_result_1 = copy.deepcopy(best_result_in_batch_1)
        current_result_1 = copy.deepcopy(best_result_in_batch_1)  # Subsample batches of bitstrings
        current_occupancies_1 = current_result_1.orbital_occupancies
    # best_result is not None because there must have been at least one iteration
    best_result_1 = cast(SCIResult, best_result_1)  # Convert bitstrings to CI strings and include requested and carryover strings  # Run diagonalization  # Call callback function  # Get best result from batch  # Check if the energy is the lowest seen so far  # Save the current result and occupancies
    return best_result_1, pm_result_history


@app.cell
def _(
    best_result_1,
    ccsd,
    nuclear_repulsion_energy,
    plt,
    pm_result_history,
    ref_result,
    result_history_1,
    scf,
):
    print(f'Best energy (reference-augmented SQD) = {best_result_1.energy + nuclear_repulsion_energy}')
    plt.axhline(scf.e_tot, color='C0', label='HF')
    plt.axhline(ccsd.e_tot, color='C1', label='CCSD')
    plt.axhline(ref_result.energy + nuclear_repulsion_energy, color='C2', label='Reference Subspace')
    plt.boxplot([[x.energy + nuclear_repulsion_energy for results in result_history_1 for x in results], [x.energy + nuclear_repulsion_energy for results in pm_result_history for x in results]], tick_labels=['Original SQD', 'Reference-Augmented SQD'])
    plt.legend(loc='upper right')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Observe two improvements in the **Reference-Augmented SQD** box plot:

    1. **Lower energy** — the best estimate is closer to the CCSD reference, because the 100 pinned reference determinants guarantee that the most important near-HF configurations are always in the subspace, regardless of sampling noise.
    2. **Tighter spread** — the box plot is narrower, meaning the result is more *stable* across different batches. Anchoring the subspace with reference determinants reduces variance from unlucky sampling.

    **If the Reference-Augmented SQD energy is lower than the pure classical reference subspace energy — congratulations. You have just demonstrated quantum utility on real quantum hardware.** The quantum samples contributed configurations that no brute-force enumeration could find on its own, and those configurations produced a measurably better ground-state energy estimate. This is exactly what quantum utility looks like in practice: the quantum device has added something that classical enumeration alone cannot replicate. Well done.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Bonus Challenge: Further improve the energy estimation

    Now it's your turn to further push the energy estimate towards **quantum advantage!**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="exercise_bonus"></a>
    <div class="alert alert-block alert-success">

    <b>Bonus exercise: Find your best subspace!</b>

    **Your Goal:** Push the SQD energy estimate for N₂ as low as possible.

    **Constraint:** Your subspace dimension must not exceed **90,000** (i.e., keep `max_dim` at most `(300, 300)`). This limit applies to all participants to ensure a fair comparison.

    **Hints:**

    - **Strategic subspace refinement:** You might have noticed that current SQD loop is not improving the result over iteration. Consider refining subspace more strategically, possibly keeping some quality determinants and carrying them over SQD iteration.

    - **Different configuration recovery scheme:** The function used to recover configurations basically governs the quality of your sample space. Experiment with different functional forms for `prob_flip_0_to_1` to steer the recovered configurations toward higher-quality samples.

    - **Better ansatz:** Using more LUCJ layers or further optimized parameters can improve the quality of quantum samples. As you have seen from the augmented method above, the sample quality matters a lot in overall SQD performance and convergence rate.

    - **More iterations:** When you feel like you are ready, increase `max_iterations` or `num_batches` to let the SQD loop recover the configuration further.

    **Expectation:** Unfortunately, in the given size of subspace size, you may not be able to beat the CCSD result. However, you can still exercise some important techniques to improve the SQD algorithm before scaling it up to larger subspace dimension. For this bonus challenge, refer to the score which will range from 0 to 100, where 100 is the best outcome. Your score reflects how well you minimize the energy. Try to achieve the score 100 if you can!

    You can submit your best result with the cell below.

    </div>
    """)
    return


@app.cell
def _(best_result_1, grade_lab4c_exbonus, nuclear_repulsion_energy):
    best_energy = best_result_1.energy + nuclear_repulsion_energy
    best_subspace_1 = (best_result_1.sci_state.ci_strs_a, best_result_1.sci_state.ci_strs_b)
    grade_lab4c_exbonus(best_energy, best_subspace_1)  # Submit the best energy and subspace
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Well done — you have completed the Bonus Challenge!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Additional information

    **Created by:** Boseong Kim

    **Version:** 1.0.0
    """)
    return


if __name__ == "__main__":
    app.run()

