import marimo

__generated_with = "0.23.14"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import os
    from dotenv import load_dotenv

    load_dotenv()
    API_KEY = os.getenv("IBM_QUANTUM_API_KEY")
    INSTANCE = os.getenv("IBM_QUANTUM_INSTANCE")

    print(f"API KEY: {API_KEY}")
    print(f"INSTANCE: {INSTANCE}")
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Lab 3: Your New Tool For Quantum Advantage

    Welcome to Lab 3 of the Qiskit Global Summer School 2026!

    In this lab, you will learn how to use __[Samplomatic](https://github.com/Qiskit/samplomatic)__, a framework introduced to enable advanced control over the error mitigation process. This is an important step in our journey towards Quantum Advantage.

    - In __Chapter 1__, we will cover the error mitigation processes that are possible in Qiskit Runtime _without_ Samplomatic. You will learn what it means to _dress a layer_ and how a Pauli propagates through a Clifford gate! These are essential concepts for Chapter 2.

    - In __Chapter 2__, you will learn everything you need to know to use Samplomatic: how to box up circuits, learn noise in layers and execute jobs with the _Executor_ primitive.

    - Finally, in __Chapter 3__, we introduce two Qiskit add-ons that use Samplomatic: [Propagated Noise Absorption](https://qiskit.github.io/qiskit-addon-pna/) (PNA) and [Shaded Lightcones](https://qiskit.github.io/qiskit-addon-slc/) (SLC).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    __Usage information:__ _Total estimated QPU usage on a Heron device is 1 minute 30 seconds. This usage estimate reflects backend execution time only. Queue time, calibration, and runtime session delays may be longer._

    This lab requires execution on QPU hardware. We will be learning the noise in the device in order to perform advanced error mitigation and execution on real hardware is required for all the noise Learner jobs. It is not possible to execute these jobs with a simulator!

    __Note for Windows Users:__
    The shaded lightcone add-on used in Chapter 3 uses the `pyscf` package, a Python-based chemistry simulation library, which is not natively supported on Windows. We recommend Windows users use a cloud based service like qBraid or create a Python environment using the Windows Subsystem for Linux.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup & Imports
    Uncomment the `pip install`'s below and execute the cell to install the required libraries. Remember to restart your kernel afterwards!
    """)
    return


@app.cell
def _():
    # Install required packages
    #!pip install -q -U qiskit qiskit-ibm-runtime
    #!pip install -q matplotlib numpy ipython
    #!pip install -q samplomatic
    #!pip install -q qiskit-addon-utils qiskit-addon-pna qiskit-addon-slc
    #!pip install --upgrade qc-grader
    #!pip install plotly
    #!pip install pylatexenc
    #!pip install nbformat
    return


@app.cell
def _():
    ### Scientific Computing
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch

    ### IPython
    from IPython.display import display

    ### Qiskit 
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Pauli, SparsePauliOp
    from qiskit.transpiler import generate_preset_pass_manager

    ### Qiskit IBM Runtime
    from qiskit_ibm_runtime import QiskitRuntimeService, Executor, QuantumProgram
    from qiskit_ibm_runtime.options import EstimatorOptions
    from qiskit_ibm_runtime.options_models.noise_learner_v3_options import NoiseLearnerV3Options
    from qiskit_ibm_runtime.noise_learner_v3 import NoiseLearnerV3

    ### Samplomatic
    import samplomatic
    from samplomatic import Twirl, InjectNoise, ChangeBasis, build
    from samplomatic.transpiler import generate_boxing_pass_manager
    from samplomatic.utils import find_unique_box_instructions, get_annotation

    ### Qiskit Addons
    from qiskit_addon_utils.exp_vals.measurement_bases import get_measurement_bases
    from qiskit_addon_utils.exp_vals.expectation_values import executor_expectation_values
    from qiskit_addon_utils.noise_management import trex_factors, gamma_from_noisy_boxes
    from qiskit_addon_pna import generate_noise_mitigating_observable
    from qiskit_addon_slc.bounds import compute_backward_bounds, compute_forward_bounds, compute_local_scales, merge_bounds
    from qiskit_addon_slc.utils import generate_noise_model_paulis, map_modifier_ref_to_ref
    from qiskit_addon_slc.visualization import draw_shaded_lightcone


    # Grader imports
    from qc_grader.challenges.qgss_2026 import (
        grade_lab3_ex1,
        grade_lab3_ex2,
        grade_lab3_ex3,
        grade_lab3_ex4,
        grade_lab3_ex5,
    )

    # grader function to check your progress
    from qc_grader.challenges.qgss_2026 import check_progress

    return (
        ChangeBasis,
        EstimatorOptions,
        Executor,
        InjectNoise,
        NoiseLearnerV3,
        NoiseLearnerV3Options,
        Patch,
        Pauli,
        QiskitRuntimeService,
        QuantumCircuit,
        QuantumProgram,
        SparsePauliOp,
        Twirl,
        build,
        check_progress,
        compute_backward_bounds,
        compute_forward_bounds,
        compute_local_scales,
        display,
        draw_shaded_lightcone,
        executor_expectation_values,
        find_unique_box_instructions,
        gamma_from_noisy_boxes,
        generate_boxing_pass_manager,
        generate_noise_mitigating_observable,
        generate_noise_model_paulis,
        generate_preset_pass_manager,
        get_annotation,
        get_measurement_bases,
        grade_lab3_ex1,
        grade_lab3_ex2,
        grade_lab3_ex3,
        grade_lab3_ex4,
        grade_lab3_ex5,
        map_modifier_ref_to_ref,
        merge_bounds,
        np,
        plt,
        samplomatic,
        trex_factors,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Define the backend:

    In this lab we will work with a __Heron device__. As stated above, noise learning jobs executed on the backend cannot be executed with a simulator. By focusing on a Heron device, participants working with an Open Plan account can participate in this lab.

    It is a good idea to you use the _same backend_ throughout this tutorial. We will be learning the noise in the backend and using that noise model to implement advanced error mitigation techniques. Therefore, if you change backend halfway through, the learned noise model will not be applicable to the new backend.

    Note: If you are having trouble connecting to a backend, return to Lab 0 and make sure you have set up your IBM Quantum Platform Account correctly.
    """)
    return


@app.cell
def _(QiskitRuntimeService, generate_preset_pass_manager):
    service = QiskitRuntimeService()

    # Define the backend: 
    service = QiskitRuntimeService()
    backend = service.least_busy(
        operational=True,
        filters=lambda b: b.processor_type.get('family') == 'Heron'
    )

    print(f"Backend     : {backend.name}")
    print(f"# qubits    : {backend.num_qubits}")
    print(f"Basis gates : {backend.basis_gates}")

    # Create ISA pass manager for transpilation with optimization_level=0
    isa_pm = generate_preset_pass_manager(backend=backend, optimization_level=0)
    return backend, isa_pm, service


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Chapter 0 — Errors on today's quantum hardware

    Today's quantum hardware is noisy. Every gate, every idle moment, every measurement introduces small errors, and at utility scale (circuits on 100+ qubits) those errors accumulate to a degree that can no longer be ignored. Until full fault tolerance arrives, the only way to get *useful* answers out of these devices is to manage that noise, to suppress it where we can, to characterize it where we can't, and to mitigate its bias when we read out a result. Dealing with noise is therefore a central part of getting useful results from today's devices, and the techniques for doing it are an active area of development.

    The techniques for handling noise fall into roughly four categories. They differ in *when* they act, in *what* they cost, and in whether they fix errors, flag them, or merely correct the statistics after the fact — so it is worth seeing all four before we introduce the new tools this lab is built around.

    - **Error correction (EC)** encodes logical information redundantly, repeatedly extracts syndromes, and when implemented fault-tolerantly, can suppress logical errors below physical error rates. Full QEC is prohibitive on near-term devices because of its qubit and time overheads.

    - **Error detection (ED)** flags runs that are likely corrupted and discards them via post-selection, keeping a smaller but cleaner sample. The flag can come from a detection-only QEC code, one whose distance heralds an error without giving enough information to identify and reverse it. In that case, making ED a limiting case of error correction. ED lets a higher-level code in a hierarchical scheme treat the flagged error as an *erasure* (a known location is far easier to correct than an unknown one). It can equally come from cheaper, code-free checks, such as verifying a symmetry the ideal circuit should preserve, e.g. a conserved parity or particle number, and rejecting shots that violate it. Either way, ED trades a reduced usable sample against an implementation overhead well below that of fault-tolerant EC.

    - **Error mitigation (EM)** does not fix individual shots at all. It biases or re-weights the statistics across many noisy runs so that the *estimate* of an expectation value (or distribution) is closer to the ideal one ([Cai et al., *Quantum error mitigation*, Rev. Mod. Phys. 95, 2023](https://journals.aps.org/rmp/abstract/10.1103/RevModPhys.95.045005)). This is the regime where today's utility-scale experiments operate, and it is the focus of this lab.

    - **Error suppression (ES)** acts during execution to reshape the noise itself. Examples include dynamical decoupling (DD), which inserts pulses on idle qubits to cancel coherent error, and Pauli twirling (PT), which randomizes gate dressings so that the residual error becomes a stochastic Pauli channel ([Wallman & Emerson, PRA 94, 2016](https://journals.aps.org/pra/abstract/10.1103/PhysRevA.94.052325)).

    Two of these four you have already used, whether you noticed or not, if you have run the Qiskit Runtime primitives. Error suppression and error mitigation are what `Estimator` implements (error correction and detection are not something the primitive applies for you). At its default option, `Estimator` already corrects for systematic readout bias (Twirled Readout Error eXtinction, TREX). You can also go further and enable additional error suppression and error mitigation methods yourself using `EstimatorOptions` as we shall see in section 1.1.2. What all of these options have in common is that they act on your circuit as a single _circuit-wide_ policy, which adds a fixed kind of overhead to every run.

    This lab introduces the tools (_Samplomatic_) that you can use alongside Qiskit Runtime to go beyond that _circuit-wide_ setting, allowing you to manage noise layer by layer and observable by observable. In Chapter 1, we begin by giving an overview of what the familiar `EstimatorOptions` do and what they cost.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Chapter 1 — Error mitigation as a Runtime product, and the theory behind its cost

    This chapter takes the familiar Runtime options and opens them up:
    - Section 1.1 walks through the error suppression and error mitigation methods `Estimator` offers and has you configure each one by hand.

    - Section 1.2 then steps one level *below* the switches to the small piece of algebra — *dressing* and *commutation* — that is the most basic principle these techniques rest on.

    - Section 1.3 closes the chapter by asking what these whole-circuit switches *cannot* do, and what they cost in terms of resource overhead. This motivates the finer, box-by-box tools the rest of the lab is built around.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1.1  Error mitigation as a cloud service

    The introduction noted that Qiskit Runtime exposes error mitigation as a product: a set of options you turn on, applied to your circuit as a single circuit-wide policy. This section catalogs those options on the `EstimatorV2` primitive — what each one does, and which `resilience_level` preset turns it on (section 1.1.1) — and then looks at each method's settings and behavior in detail (section 1.1.2). It closes with Exercise 1, in which you configure each of the five methods on its own `EstimatorOptions` so the effect of each one stays separable. The algebra these methods rest on comes in section 1.2.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1.1.1  The options on the Runtime primitives

    The `EstimatorV2` primitive bundles these error suppression and error mitigation techniques behind a single `EstimatorOptions` object. The official catalogue is [Error mitigation and suppression techniques](https://quantum.cloud.ibm.com/docs/en/guides/error-mitigation-and-suppression-techniques). The `resilience_level` option is a convenience preset that turns a fixed set of them on at once. The table below shows each technique, its role, and which preset level enables it. We will introduce the exact attribute paths in section 1.1.2.

    | Technique | Role | One-line description | Enabled by |
    |---|---|---|---|
    | **DD** (Dynamical decoupling) | Suppression | Insert pulse sequences on idle qubits to cancel coherent errors that build up while qubits sit idle | Enable explicitly |
    | **PT** (Pauli twirling, gates) | Suppression | Tailor the coherent part of 2Q-gate noise into an effectively stochastic Pauli channel, which also lets downstream methods (PEA, PEC) assume Pauli-channel noise | Level 2 |
    | **TREX** (Twirled readout error extinction) | Mitigation | Twirl measurements with random X gates so the readout-error transfer matrix becomes diagonal and can be inverted by rescaling | Level 1 (default) |
    | **ZNE** (Zero-noise extrapolation) | Mitigation | Amplify noise at several controlled factors (e.g. by gate folding) and extrapolate the expectation value back to the zero-noise limit (not guaranteed unbiased) | Level 2 |
    | **PEA** (Probabilistic error amplification) | Mitigation | Replace ZNE's gate-folding amplification with one driven by a *learned* Pauli-Lindblad noise model, for more accurate noise scaling (still using ZNE's extrapolation step) | Set explicitly (with ZNE) |
    | **PEC** (Probabilistic error cancellation) | Mitigation | Sample anti-noise circuits whose ensemble average inverts the learned noise channel, giving an unbiased estimate at the cost of a sampling overhead $\gamma^2$ | Set explicitly |

    By default Runtime runs at **resilience level=1**, which enables TREX only; see the [Configure error mitigation](https://docs.quantum.ibm.com/guides/configure-error-mitigation) guide for what each level turns on. The next section looks at each technique's options and behavior in detail.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1.1.2  The methods in detail

    This section expands each technique from the table in section 1.1.1: what it does, the options that control it, and when it helps. Figures and full explanations are from the official [Error mitigation and suppression techniques](https://docs.quantum.ibm.com/guides/error-mitigation-and-suppression-techniques) guide.

    #### Dynamical decoupling (DD) — *suppression*
    Idle qubits pick up coherent errors while they wait for other qubits to finish. DD inserts a sequence of pulses on those idle qubits that multiplies out to the identity, so the intended computation is unchanged, while the pulses average away the slow coherent drift. It helps most when a circuit has idle gaps; on a densely packed circuit it can do little, or even hurt, because the pulses are themselves imperfect.

    ![Dynamical decoupling: an XX pulse sequence inserted during a qubit's idle period (IBM Quantum docs).](https://quantum.cloud.ibm.com/docs/images/guides/error-mitigation-explanation/dd.avif)

    - `dynamical_decoupling.enable` — turn DD on (off by default).
    - `dynamical_decoupling.sequence_type` — which pulse sequence; default `"XX"`, others include `"XpXm"`, `"XY4"`.

    #### Pauli twirling (PT) — *suppression*
    Twirling (randomized compiling) sandwiches a chosen gate between random single-qubit Paulis picked so the ideal operation is unchanged. Averaged over many random instances, an arbitrary noise channel becomes a stochastic *Pauli* channel: coherent error, which otherwise accumulates quadratically with depth, is reshaped into Pauli noise that grows only linearly. Since most hardware error comes from two-qubit gates, twirling is usually applied to the native 2Q gates, and it is a prerequisite for PEA and PEC, which assume Pauli-channel noise.

    ![Pauli twirling replaces one circuit with a random ensemble of equivalent twirled circuits (IBM Quantum docs).](https://quantum.cloud.ibm.com/docs/images/guides/error-mitigation-explanation/pauli_twirling.svg)

    - `twirling.enable_gates` — twirl the 2Q gate layers.
    - `twirling.num_randomizations` — number of random twirled instances.
    - `twirling.shots_per_randomization` — shots per instance.

    #### Twirled readout error extinction (TREX) — *mitigation*
    TREX targets *measurement* error. It twirls the readout by randomly inserting an X before a measurement and flipping the classical bit back afterward. This, with readout error present, diagonalizes the readout-error transfer matrix so it can be inverted by a simple rescaling. The rescaling factor is learned by benchmarking random circuits prepared in the zero state, at the cost of a few calibration circuits. This is the one method on by default (_resilience level 1_).

    ![Measurement twirling: an X gate before the measurement and a classical bit-flip after are equivalent to a plain measurement when noiseless (IBM Quantum docs).](https://quantum.cloud.ibm.com/docs/images/guides/error-mitigation-explanation/measurement_twirling.svg)

    - `resilience.measure_mitigation` — turn TREX on.
    - `resilience.measure_noise_learning.num_randomizations`, `...shots_per_randomization` — control measurement-noise learning.

    #### Zero-noise extrapolation (ZNE) — *mitigation*
    ZNE runs the circuit at several *amplified* noise levels and extrapolates the expectation value back to zero noise. Runtime amplifies noise by digital gate folding. This replaces a unitary $U$ with $U U^\dagger U$ (and longer foldings) to multiply its noise by a known factor and then fits the results with a chosen functional form. It often improves accuracy but is *not* guaranteed unbiased. The default samples three noise factors, for roughly a 3× overhead.

    ![Zero-noise extrapolation: digital gate folding amplifies noise; results are extrapolated to the zero-noise limit (IBM Quantum docs).](https://quantum.cloud.ibm.com/docs/images/guides/error-mitigation-explanation/zne.avif)

    - `resilience.zne_mitigation` — turn ZNE on.
    - `resilience.zne.noise_factors` — amplification factors (default `(1, 3, 5)`).
    - `resilience.zne.extrapolator` — fit form (e.g. linear, exponential).

    #### Probabilistic error amplification (PEA) — *mitigation*
    PEA is a more accurate amplifier *for* ZNE. Instead of gate folding, it first **learns** the twirled Pauli-Lindblad noise model of each entangling layer, then amplifies by probabilistically injecting single-qubit noise drawn from that learned model — a faithful scaling of the actual device noise rather than a synthetic one. The amplified results still feed ZNE's extrapolation, so PEA is switched on top of ZNE. For utility-scale experiments it is often the best amplifier choice.

    - `resilience.zne_mitigation = True` together with `resilience.zne.amplifier = "pea"`.

    #### Probabilistic error cancellation (PEC) — *mitigation*
    PEC also learns the noise model, but instead of amplifying it, it *inverts* it: it samples an ensemble of "anti-noise" circuits whose average implements the inverse noise channel, giving an **unbiased** estimate. The price is a sampling overhead that scales as $\gamma^2$ and rises quickly with circuit depth and total noise — which is why PEC is practical only for circuits of modest size (we return to this cost in 1.3). In Chapter 3, we will implement PEC using _Samplomatic_ and introduce shaded lightcones (SLC) which is an evolution of PEC.

    - `resilience.pec_mitigation` — turn PEC on.
    - `resilience.pec.max_overhead` — cap on the sampling overhead $\gamma^2$; Runtime backs off if the cap would be exceeded.

    __Note__: ZNE/PEA and PEC are *opposing* strategies — amplify the noise versus cancel it — and cannot be enabled on the **same** `EstimatorOptions`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- <div class="alert alert-block alert-success"> -->

    **Exercise 1 — Configure each method.**

    Using the methods and attribute paths from section 1.1.2, configure each of the five on its own `EstimatorOptions` object, then collect them into a dictionary `options_dict` with keys `"dd"`, `"pt"`, `"trex"`, `"zne"`, `"pec"`. Each method is checked separately — all five must be correct to pass, and the grader reports any that are not.

    - **`dd_options`** — Dynamical decoupling: `enable = True`, `sequence_type = "XY4"`
    - **`pt_options`** — Pauli twirling: `enable_gates = True`, `strategy = "active"`, `num_randomizations = 32`
    - **`trex_options`** — TREX: `measure_mitigation = True`
    - **`zne_options`** — ZNE with PEA: `zne_mitigation = True`, `noise_factors = [1, 3, 5]`, `amplifier = "pea"`
    - **`pec_options`** — PEC: `pec_mitigation = True`, `max_overhead = 100`

    <!-- </div> -->
    """)
    return


@app.cell
def _(EstimatorOptions):
    dd_options = EstimatorOptions()
    dd_options.dynamical_decoupling.enable = True
    dd_options.dynamical_decoupling.sequence_type = "XY4"

    pt_options = EstimatorOptions()
    pt_options.twirling.enable_gates = True
    pt_options.twirling.strategy = "active" 
    pt_options.twirling.num_randomizations = 32

    trex_options = EstimatorOptions()
    trex_options.resilience.measure_mitigation = True

    zne_options = EstimatorOptions()
    zne_options.resilience.zne_mitigation = True
    zne_options.resilience.zne.noise_factors = [1, 3, 5]
    zne_options.resilience.zne.amplifier = "pea"

    pec_options = EstimatorOptions()
    pec_options.resilience.pec_mitigation = True
    pec_options.resilience.pec.max_overhead = 100

    options_dict = {
        "dd": dd_options,
        "pt": pt_options,
        "trex": trex_options,
        "zne": zne_options,
        "pec": pec_options,
    }
    return (options_dict,)


@app.cell
def _(grade_lab3_ex1, options_dict):
    # grade your answer
    grade_lab3_ex1(options_dict)
    return


@app.cell
def _(check_progress):
    # check your progress across all the labs
    check_progress()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1.2  The algebra underneath: dressed layers and commutation

    The options in section 1.1 are applied __once__ to the whole circuit. Several of them share a common underlying operation: wrapping a gate with single-qubit Paulis on either side, chosen so that the gate's logical action is unchanged while the noise attached to it is transformed. Gate twirling uses this operation directly. ZNE/PEA and PEC use it indirectly, through the Pauli noise model they learn. A gate wrapped this way is called a **dressed** gate.

    In this section, we explain what it means to _dress a gate_. This will help you understand why the error-mitigation switches in section 1.1 behave the way they do. It is also the operation the finer, box-by-box tools in the Samplomatic framework uses. You will see in Chapter 2 how this framework enables us to move beyond the _whole-circuit switch_ approach we have seen so far.

    A **dressed layer** is a two-qubit unitary wrapped by single-qubit unitaries on either side. We introduce it first in general, then specialize to dressing a CZ with Paulis — the setting of every two-qubit layer we work with later. The thread holding the section together is the *commutation relation* (Clifford conjugation) between a Pauli and the bare gate: it is what gives the dressing table its structure, and it is the same operation Samplomatic later uses, box by box, to propagate virtual Paulis through a circuit.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1.2.1  Dressing a unitary

    For any $n$-qubit unitary $U$, a *dressed* version is

    $$\tilde{U} \;=\; V_\text{out}\, U\, V_\text{in},$$

    where $V_\text{in}$ and $V_\text{out}$ are products of single-qubit unitaries (one per qubit). When the dressing satisfies $V_\text{out}\,U\,V_\text{in} = U$ up to a global phase we call it *invariant*: the logical action of $U$ is unchanged, but any noise channel attached to $U$ gets *twirled* by $V_\text{in}$ and $V_\text{out}$ ([Wallman & Emerson, *Noise tailoring for scalable quantum computation via randomized compiling*, PRA 94, 2016](https://journals.aps.org/pra/abstract/10.1103/PhysRevA.94.052325)). Two questions follow: which pairs $(V_\text{in}, V_\text{out})$ leave $U$ invariant, and how to enumerate them systematically.

    The case we will work with throughout the lab is the one in which $V_\text{in}$ and $V_\text{out}$ are Paulis and $U$ is a Clifford — the setting of the two-qubit gates on IBM hardware (CZ, CX, ECR). Two helpers from `qiskit.quantum_info` make it concrete: `Pauli("IX").evolve(U, frame='s')` returns $U\,P\,U^\dagger$ with the correct sign, and `Pauli.equiv(other)` compares two Paulis up to overall phase — the "invariant up to global phase" notion we need.
    """)
    return


@app.cell
def _(Pauli, QuantumCircuit):
    def dress(U: QuantumCircuit, v_in: str, v_out: str) -> QuantumCircuit:
        """Build the circuit  V_out . U . V_in  as a QuantumCircuit.
        """
        n = U.num_qubits
        assert not v_in.startswith(('+', '-', 'i')), f'v_in must be an unsigned Pauli string, got {v_in!r}'
        assert not v_out.startswith(('+', '-', 'i')), f'v_out must be an unsigned Pauli string, got {v_out!r}'
        assert len(v_in) == len(v_out) == n, "Pauli string length must match U's num_qubits"
        qc = QuantumCircuit(n)
        for q, _p in enumerate(reversed(v_in)):
            if _p != 'I':
                getattr(qc, _p.lower())(q)
        qc.compose(U, inplace=True)
        for q, _p in enumerate(reversed(v_out)):  # Qiskit string 'q_{n-1}...q_0' — reverse to iterate in qubit order.
            if _p != 'I':
                getattr(qc, _p.lower())(q)
        return qc

    def is_invariant(U: QuantumCircuit, v_in: str, v_out: str) -> bool:
        """True iff  V_out . U . V_in  equals  U  up to a global phase.

        Takes *unsigned* Pauli strings v_in, v_out. The invariance condition is
        U V_in U† = ±V_out; the ± becomes a global phase on the dressed operator,
        so it does not affect invariance. We use `Pauli.equiv`, which is
        phase-insensitive, to compare.
        """
        return Pauli(v_in).evolve(U, frame='s').equiv(Pauli(v_out))

    return (is_invariant,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1.2.2  CZ Example

    We specialize to $U = \mathrm{CZ}$ because that is the two-qubit gate used throughout the lab — the Ising circuit in section 2.6.1 is built entirely from CZ gates. After verifying by direct calculation that a specific Pauli dressing leaves CZ invariant, we propagate all 16 two-qubit Paulis through CZ to build the full map $V_\text{in} \mapsto V_\text{out}$. There is exactly one valid $V_\text{out}$ (up to sign) for each $V_\text{in}$.

    Two distinct pieces of information live in the resulting table we print below and they should not be conflated. The *dressing map* records which **unsigned** Pauli to physically apply as $V_\text{out}$, and is what `dress()` consumes.

    The __algebraic sign__, which defines whether $\mathrm{CZ}\cdot V_\text{in}\cdot \mathrm{CZ}$ equals $+V_\text{out}$ or $-V_\text{out}$ does **not** affect gate invariance (the sign is absorbed as a global phase), but it **does** matter for the propagation rules in section 1.2.3.

    We will see that the table itself has a clean structure: $Z$ factors commute through CZ untouched, an $X$ or $Y$ factor on one qubit picks up a $Z$ on the **other** qubit, and the pair $XY \leftrightarrow YX$ picks up a minus sign — visible in the rightmost (sign) column of the printout below.
    """)
    return


@app.cell
def _(QuantumCircuit):
    # Bare CZ layer
    cz_layer = QuantumCircuit(2, name="CZ")
    cz_layer.cz(0, 1)
    cz_layer.draw("mpl")
    return (cz_layer,)


@app.cell
def _(cz_layer, is_invariant):
    # apply X on qubit 0 before CZ, and X on qubit 0 + Z on qubit 1 after.

    print("V_in='IX', V_out='ZX' leaves CZ invariant?",
          is_invariant(cz_layer, "IX", "ZX"))
    return


@app.cell
def _(Pauli, cz_layer):
    # Build two related objects from the Pauli algebra:
    #   cz_twirl_map       : V_in -> V_out  (UNSIGNED — what to apply as a dressing)
    #   cz_commutation_map : V_in -> (sign, V_out)  (signed — for propagation rules)

    PAULIS = ["I", "X", "Y", "Z"]


    def split_sign(label: str) -> tuple[int, str]:
        """Split a signed Pauli label into (+/-1, unsigned_label)."""
        if label.startswith("-"):
            return -1, label[1:]
        if label.startswith("+"):
            return +1, label[1:]
        return +1, label


    cz_twirl_map       = {}
    cz_commutation_map = {}

    for p1 in PAULIS:         # Pauli on qubit 1 (leftmost in string)
        for p0 in PAULIS:     # Pauli on qubit 0 (rightmost in string)
            v_in   = p1 + p0
            signed = Pauli(v_in).evolve(cz_layer, frame="s").to_label()
            sign, bare = split_sign(signed)
            cz_twirl_map[v_in]       = bare
            cz_commutation_map[v_in] = (sign, bare)

    print(f"Total Pauli dressings for CZ: {len(cz_twirl_map)}  (expected 16)")
    print()
    print(f"  {'V_in':<6}{'V_out (apply)':<16}{'algebraic sign'}")
    print(f"  {'-'*6}{'-'*16}{'-'*14}")
    for v_in, v_out in cz_twirl_map.items():
        sign, _ = cz_commutation_map[v_in]
        sign_str = "+" if sign > 0 else "−"
        print(f"  {v_in:<6}{v_out:<16}{sign_str}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1.2.3  Commutation: how a Pauli propagates through a Clifford

    The structure of the table in section 1.2.2 is no accident. For any Pauli $P$ and Clifford $U$,

    $$U\,P\,U^\dagger \;=\; \pm\,P',$$

    where $P'$ is another Pauli. This is the defining property of the Clifford group. Finding $V_\text{out}$ given $V_\text{in}$ amounts to propagating $V_\text{in}$ through $U$ and reading off the result, sign included. This is the operation Samplomatic uses in chapter 2 every time it propagates a virtual Pauli across a gate box. `Pauli.evolve(U, frame='s')` is the Qiskit helper that implements it, and `.to_label()` returns a signed Pauli string such as `"-YX"`.

    Running the same helper on CX produces a structurally similar table with an asymmetry from CX's control/target roles.
    """)
    return


@app.cell
def _(Pauli, QuantumCircuit, cz_layer):
    # The same Pauli.evolve(..., frame="s") helper, applied to two different gates.
    # The propagation rule is fixed by the gate, so CZ and CX give different tables.

    cx_layer = QuantumCircuit(2, name='CX')
    cx_layer.cx(0, 1)  # control = q0, target = q1
    reps = ['IX', 'XI', 'IZ', 'ZI', 'IY', 'YI']

    print('CZ . P . CZ  (symmetric in the two qubits):')
    for _p in reps:
        print(f"  CZ . {_p} . CZ  =  {Pauli(_p).evolve(cz_layer, frame='s').to_label()}")

    print('\nCX . P . CX  (control = q0, target = q1):')
    for _p in reps:
        print(f"  CX . {_p} . CX  =  {Pauli(_p).evolve(cx_layer, frame='s').to_label()}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The two tables above differ because the propagation rule is fixed by the gate. CZ is symmetric: a $Z$ on either qubit passes through, an $X$ or $Y$ picks up a $Z$ on the other qubit. CX is not: an $X$ on the target qubit and a $Z$ on the control qubit each spread to both qubits, but an $X$ on the control qubit and a $Z$ on the target qubit pass through unchanged.

    The procedure is the same in both cases: conjugate the Pauli by the gate and read off the signed result. This is the operation every twirling-based method in the lab is built on, from the `twirling.enable_gates` switch in section 1.1.2 to Samplomatic's per-box `Twirl` annotation we will introduce in Chapter 2.

    What separates those methods is the scale at which the operation is applied. An `EstimatorOptions` switch applies it once to the whole circuit — the coarsest option, and one that doesn't work for some mitigation tasks, such as one which require treating individual layers or observables differently. Secton 1.3 sets out what the Runtime options can and cannot do, along with their resource cost, which is what motivates the finer tools used in the rest of the lab.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1.3  Why we need structure-aware mitigation

    In the previous sections, we showed what the `EstimatorOptions` switch can do and the algebra underneath it. This section looks at where a whole-circuit switch falls short, the error mitigation tasks it cannot express, and the resource cost it incurs as circuits grow. We do this with Samplomatic: the per-box tool that the rest of the lab is built on.

    #### What the Runtime options cannot do

    Runtime options expose **whole-circuit switches** like "insert DD on every idle window" or "twirl every 2Q gate". Each is applied by a single circuit-wide policy, which is sufficient for many small workloads. PEA and PEC do learn a noise model *per entangling layer* internally, but the API exposes no per-layer controls: you cannot inspect a layer's learned noise, override it, or apply a different strategy to different layers. Another capability is out of reach entirely: rewriting the observable itself to absorb learned noise rather than mitigating the circuit (something we will see in Chapter 3 with __propagated noise absorption__ (PNA)).

    Chapter 2 introduces the tools that provide this finer control: the *box* — a slice of the circuit annotated with directives such as `Twirl`, `InjectNoise`, or `ChangeBasis` — together with `NoiseLearnerV3` and `Executor`, the box-aware counterparts to `Sampler` and `Estimator`.

    #### The hidden cost: sampling overhead

    Turning these switches on is not free, and the bill is paid in **shots**, not qubits. Error mitigation trades a _space_ overhead for a _time_ overhead: instead of extra physical qubits (as in error correction), it runs many noisy circuits and post-processes them. Part of this cost is a plain multiplier you can read off the options, like in ZNE's `noise_factors`, `twirling.num_randomizations`, and TREX's readout-calibration batch. For example, three ZNE factors with 32 randomizations already runs on the order of `3 × 32` variants relative to a single unmitigated run.

    What you *cannot* read off from the options is something that limits utility-scale circuits: the __sampling overhead__ of probabilistic methods grows *exponentially*. For PEC, the runtime $J$ is given by
    $$J = \bar{\gamma}^{\,nd}\,\beta^{d},$$
    where $n$ is the number of qubits and $d$ is the depth. The base $\bar{\gamma}$ is set by the *learned* noise model. This can be thought of as a quality metric: a lower gate error gives a smaller $\bar{\gamma}$. $\beta$ is the time per circuit layer (a speed metric). Because $\bar{\gamma}$ enters exponentially, even a small reduction in it, i.e. by having a lower gate error, will reduce the size of $\bar{\gamma}^{nd}$ dramatically.

    <img src="https://research-website-prod-cms-uploads.s3.us.cloud-object-storage.appdomain.cloud/New_Fig_Gamma_Epsilon2_Tex_100q_trotter_a712254dca.jpg" width="450" alt="Estimated PEC circuit overhead for 100-qubit Ising Trotter circuits">

    *Fig. 1: Estimating the PEC circuit overhead for 100 qubit Trotterization circuits of depth 400 and 4000, representing the time evolution of an Ising spin chain. Dotted red line indicates 1 day of runtime assuming a fixed 1kHz sampling rate. Reproduced from K. Temme, E. van den Berg, A. Kandala, and J. Gambetta, "[Error mitigation is the path to quantum computing usefulness](https://www.ibm.com/quantum/blog/gammabar-for-quantum-advantage)," IBM Quantum blog, 2022. © IBM.*

    The figure above is for the same kind of circuit this lab uses — an Ising Hamiltonian Trotter evolution (we will introduce this in section 2.6). The figure shows the overhead dropping by orders of magnitude as the two-qubit gate error falls. The whole-circuit switches available to us with `EstimatorOptions` give no way to see or act on the per-layer noise that sets $\bar{\gamma}$. This is the gap the rest of the lab fills: Chapter 2 *measures* the per-layer noise with `NoiseLearnerV3`, and Chapter 3 *reduces* the overhead by treating layers and observables individually (PNA and SLC).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Chapter 2 — Samplomatic and NoiseLearner

    To mitigate noise at the level of individual layers or gates, three things are needed: a way to address parts of a circuit separately, a measurement of the noise on each part, and a way to run the mitigated program and collect results. Samplomatic, `NoiseLearnerV3`, and the `Executor` primitive supply these three pieces. Together they form Qiskit Runtime's [directed execution model](https://quantum.cloud.ibm.com/docs/en/guides/directed-execution-model), which captures mitigation intent on the client side and shifts the generation of circuit variants to the server.

    [Samplomatic](https://github.com/Qiskit/samplomatic) addresses parts of a circuit through **boxes** and **annotations**. A box is a region of a circuit marked off as a unit — a single gate, a layer, or the final measurement. An annotation is an instruction attached to a box: `Twirl` randomizes the box's dressing, `InjectNoise` declares that a learned noise channel will be applied here, `ChangeBasis` rotates the measurement. The instruction is attached to the box rather than the whole circuit, so each box can be treated separately. A `build` step then turns an annotated circuit into a parametric *template* plus a *samplex* — a recipe for filling the box parameters at run time.

    [`NoiseLearnerV3`](https://quantum.cloud.ibm.com/docs/en/guides/noise-learning) supplies the measurement. It runs characterization circuits on the backend and returns a [Pauli-Lindblad noise model](https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/utils-noise-learner-result-pauli-lindblad-error) for each box, addressed by the same boxes Samplomatic uses. The two fit together through one pattern: a box *declares* with `InjectNoise` that it expects a noise model, and the specific model measured by `NoiseLearnerV3` is plugged in at run time, matched by the `InjectNoise` reference.

    The [`Executor`](https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/executor) primitive runs the mitigated program itself. Both it and `NoiseLearnerV3` submit jobs to a backend, but for different purposes: `NoiseLearnerV3` runs circuits to *measure noise*, while the `Executor` runs the box-aware program built from a template and samplex to *produce the computation's result*. It is the [box-aware counterpart](https://quantum.cloud.ibm.com/docs/en/guides/qiskit-runtime-primitives) to `Sampler` and `Estimator`. __Boxing__ is the structure shared across all three steps (how per-box mitigation is specified, how per-box noise is reported, and what the Executor runs) and it is what the Chapter 3 add-ons, propagated noise absorption (PNA) and shaded lightcones (SLC), act on to mitigate one layer or one observable at a time.

    In the following sections, we will introduce each tool step by step for a small 2-qubit toy model. Then, in section 2.6, we will put them together on a 1D Ising chain, the system Chapter 3 continues with.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2.1  Boxes and the `Twirl` annotation

    We begin with boxing up a circuit. Lets start with a very simple example: a 2-qubit circuit with a single CZ gate. We use the `.box` method to create a box around the CZ gate and tell it that it is annotated with a `Twirl` object.

    In section 1.1.2, we introduced Pauli Twirling as an important tool for error mitigation. Pauli twirling a quantum circuit tailors the noise in the circuit to a _stochastic Pauli channel_. This is done by replacing a single circuit with a random ensemble of circuit, a _randomization_. Importantly, twirling alone is not expected the mitigate errors in the circuit but instead, tailor the noise to be mitigated effectively by other techniques.

    The `Twirl`annotation is used to indicate that the box should be _twirled_.
    """)
    return


@app.cell
def _(QuantumCircuit, Twirl):
    toy = QuantumCircuit(2)

    with toy.box(annotations=[Twirl()]):
        toy.cz(0, 1)

    toy.draw("mpl")
    return (toy,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The circuit diagram shows the box (red square) wrapping the CZ gate, but the `Twirl` annotation itself does not appear in the picture. It is metadata attached to the box. We can read it back by iterating over the circuit's instructions:
    """)
    return


@app.cell
def _(toy):
    for _idx, instruction in enumerate(toy):
        print(f'Box {_idx}: annotations = {instruction.operation.annotations}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The instructions printed above tell us the following:

    There is one box in this circuit, carrying a single annotation: `Twirl(group='pauli', dressing='left', decomposition='rzsx')`. These are the default `Twirl` settings. Lets break them down:
    - `group='pauli'`: applies Pauli-group twirling
    - `dressing='left'`: the random dressing is on the left side of the box
    - `decomposition='rzsx'`: records that the dressing compiles down to the hardware's native `rz` and `sx` gates.

    The box marks *which* part of the circuit to twirl; the annotation records *how*. Turning that intent into runnable circuits is the next step.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2.1.1  Templates

    The next step in Samplomatic workflow is to *build* a template circuit and a samplex. The `build(boxed_circuit)` method turns an annotated circuit into two objects: a *template* (a parametric `QuantumCircuit` with enough free gates to realize any single randomization) and a *samplex* (a recipe describing how to fill those parameters at run time).

    A common error when trying to use `build` is to have a dressing that doesn't have a place to go. We illustrate this in the below cell.
    """)
    return


@app.cell
def _(build, toy):
    try:
        _template_circuit, samplex = build(toy)
    except Exception as e:
        print(f'{type(e).__name__}: {e}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We see that `build` fails. The `Twirl` annotation instructs Samplomatic to place its random-Pauli dressing on the _left_ (input) side of the box. But, for the box's logical action to stay unchanged, that Pauli has to propagate through the CZ and come out the _right_ (output) side as a *virtual gate* that some later box must absorb. Here the circuit just ends after the box, so those right-going virtual gates have _nowhere to land_, hence we obtain a  `SamplexBuildError`. The error reports unterminated virtual gates on qubits `[0, 1]`. A `Twirl` box always needs a *collector*: another box that receives them. In the next cell we add one as a measurement box. We can then successfully implement `build`.
    """)
    return


@app.cell
def _(QuantumCircuit, Twirl, build):
    toy_1 = QuantumCircuit(2)

    with toy_1.box(annotations=[Twirl()]):
        toy_1.cz(0, 1)

    with toy_1.box(annotations=[Twirl()]):
        toy_1.measure_all()

    _template_circuit, samplex_1 = build(toy_1)
    _template_circuit.draw('mpl', fold=-1)
    return (samplex_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Wrapping the measurement in its own `Twirl` box gives the right-side dressings a place to land: the virtual gates coming out of the CZ box are absorbed into the measurement box, which twirls the readout at the same time. `build` now succeeds, returning the `template` and its `samplex`.

    In the circuit diagram for the template, the single-qubit gates are decomposed into `rz` and `sx` and left as free parameters; the `samplex` holds the recipe that fills those parameters with a concrete random-Pauli assignment each time a randomization is drawn. One template plus one samplex stands in for the entire ensemble of randomized circuits.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2.1.2  The samplex

    As we saw above, `build` returns two objects: the _template_ and the _samplex_. The samplex is the runtime recipe: a [directed acyclic graph](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.dagcircuit.DAGCircuit) (DAG) of inputs and outputs that determines, for each randomization, the parameter values to feed into the template circuit and the post-processing to apply to the measured bitstrings.
    """)
    return


@app.cell
def _(display, samplex_1):
    print(samplex_1)
    _fig = display(samplex_1.draw())
    _fig.show(renderer='notebook')
    print(type(_fig))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The printout text above shows the samplex's inputs and outputs and the DAG diagram shows them as a graph. The **Inputs** list is empty. This is because a samplex with only `Twirl` annotations needs no runtime data, unlike when `InjectNoise` annotations are added (which we will see in section 2.4). The two **Outputs**, `parameter_values` and `measurement_flips.meas`, are the collector nodes (bowties) in the diagram.

    The DAG diagram is **not** a quantum circuit. It is the samplex's classical dataflow graph: the template (drawn above in section 2.1.1) is the circuit, and the samplex computes what fills its parameter slots for each randomization. So, a node in the samplex diagram is a computation step and an edge carries a register of classical data between steps.

    Three kinds of nodes appear in the samplex:
    - **Red stars** are *sampling* nodes. There is one per `Twirl` box, drawing that box's random Paulis. Our toy example has two boxes: the CZ box and the measurement box.
    - **Green circles** are processing steps: propagating a Pauli past the CZ (the Clifford conjugation from 1.2, now visualized as a graph node), and slicing or combining registers.
    - **Bowties** are *collectors* that gather data into the outputs. The **blue** ones into `parameter_values` (`[num_randomizations, 12]`, the template's free parameters) and the **purple** one into `measurement_flips.meas` (`[num_randomizations, 1, 2]`, the bit-flips that undo the measurement twirling).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Next is the sampling step. To do this, we use the method `samplex.sample(...)`, specifying the number of randomizations `num_randomizations`. Each call to `samplex.sample(...)` draws `num_randomizations` independent sets of random Paulis from the twirl distribution. It returns them already converted into the form the circuit needs: `parameter_values` to fill the template, and `measurement_flips` to correct the readout afterward.
    """)
    return


@app.cell
def _(samplex_1):
    outputs = samplex_1.sample({}, num_randomizations=5)
    print('parameter_values.shape     :', outputs['parameter_values'].shape)
    print('measurement_flips.meas.shape:', outputs['measurement_flips.meas'].shape)
    print()
    print('First two parameter draws:')
    print(outputs['parameter_values'][:2])
    print()
    print('Bit-flip corrections:')
    print(outputs['measurement_flips.meas'][:, 0, :])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here, we sampled 5 randomizations. The output is a dictionary with two keys: `parameter_values` and `measurement_flips`. The template of the toy model has 12 parameters and the measurement twirl has 2 bits, so the output shapes are as expected. We have 5 sets of 12 parameters for the template, and 5 sets of 2 bit-flip corrections for the measurement twirl.

    This is a purely classical step. No circuit has run yet. The template stays fixed; only the parameter values and measurement flips change from one randomization to the next. Running the filled-in circuits on hardware is the `Executor`'s job, in section 2.5.

    Two questions follow naturally: how many randomizations to draw, and how to box a circuit without writing the `with circuit.box(...)` blocks by hand. The next section answers both.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2.2  Randomizations and the boxing pass manager

    The first of those questions is how many randomizations to draw. Two parameters control this and are easy to confuse: `num_randomizations` (independent random circuits drawn from the twirl distribution) and `shots_per_randomization` (shots taken within each one). They trade off against each other. Past a certain ratio, the variance from twirling dominates the per-shot statistical noise, so adding randomizations helps more than adding shots.

    The second question is how to box a circuit without writing `with circuit.box(...)` blocks by hand. We can do this with a [_boxing pass manager_](https://qiskit.github.io/samplomatic/guides/transpiler.html). `generate_boxing_pass_manager(...)` is a transpiler pass that boxes and annotates a circuit automatically. This section uses three of its options — `enable_gates`, `enable_measures`, and `twirling_strategy`. The `inject_noise_*` options are covered in section 2.3 and measurement annotations in section 2.4.

    Let's box the same toy circuit as in section 2.1 — a CZ followed by a measurement — but this time automatically, with the pass manager instead of hand-written box blocks.
    """)
    return


@app.cell
def _(QuantumCircuit, generate_boxing_pass_manager, isa_pm):
    # create the raw toy circuit
    raw_toy = QuantumCircuit(2, 2)
    raw_toy.cz(0, 1)
    raw_toy.measure([0, 1], [0, 1])

    # transpile the toy circuit using isa_pm we defined at the start of the lab
    raw_toy_isa = isa_pm.run(raw_toy)

    # create the boxing pass manager
    twirl_only_pm = generate_boxing_pass_manager(
        enable_gates=True,
        enable_measures=True,
        twirling_strategy="active",
    )

    # box the toy circuit using the boxing pass manager
    boxed_toy = twirl_only_pm.run(raw_toy_isa)
    boxed_toy.draw("mpl", idle_wires=False)
    return (raw_toy_isa,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The boxing pass manager takes the bare circuit (no boxes) and produces the same boxed circuit we built by hand in section 2.1, automatically.

    - `enable_gates=True` wraps the 2-qubit gate in a `Twirl` box
    - `enable_measures=True` wraps the measurement in a box
    - `twirling_strategy="active"` twirls only the qubits each box acts on

    The circuit diagram shows the two resulting boxes in red, each of which have the default `Twirl` annotation (unseen in the circuit diagram).

    For a circuit with many layers using the boxing pass manager is the practical way to box. Writing `with circuit.box(...)` for every layer by hand does not scale well.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2.3  The `InjectNoise` annotation and `NoiseLearnerV3`

    In section 2.2, we showed that you can box a circuit automatically using the __boxing pass manager__. So far, we have only seen boxes annotated with the `Twirl` annotation. Pauli twirling turns each layer's coherent error into a _stochastic Pauli channel_. This is powerful because it makes the noise tractable. A sparse Pauli channel is a much simpler object than an arbitrary noise process. However, twirling alone does not remove the noise.

    In this section, we introduce the `InjectNoise` annotation. We will use this annotation, along with `NoiseLearnerV3` to learn the noise in each box. This will allow us to implement advanced error mitigation techniques such as __PNA__ and __SLC__ in Chapter 3.

    The section proceeds in three steps. First, in section 2.3.1, the boxing pass manager is extended so that every gate box carries an `InjectNoise` annotation — a declared slot keyed by a `ref` string. Then, in section 2.3.2,  `NoiseLearnerV3` runs on the backend and fills each slot with a learned Pauli-Lindblad model. Finally, in section 2.3.3, we inspect the returned noise model and see which error generators dominate the layer.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2.3.1  Declaring the slot: `InjectNoise` on each gate box

    In the cell below, we begin by generating a new boxing pass manager that we name `noise_learning_boxing_pm`. We keep the options used in the boxing manager `twirl_only_pm` above and add two new `inject_noise_*` options so that every gate box gets an `InjectNoise` annotation alongside its `Twirl`. We then apply this boxing pass manager to the toy circuit.

    `find_unique_box_instructions` then extracts the *distinct* gate layers from the circuit. These are the layers `NoiseLearnerV3` will actually characterize, since equivalent boxes (up to single-qubit dressing) share the same noise model. This is particularly efficient for circuits with many equivalent boxes as the noise learner only has to learn the noise in the _unique_ layers.
    """)
    return


@app.cell
def _(find_unique_box_instructions, generate_boxing_pass_manager, raw_toy_isa):
    noise_learning_boxing_pm = generate_boxing_pass_manager(enable_gates=True, enable_measures=True, twirling_strategy='active', inject_noise_targets='gates', inject_noise_strategy='no_modification')
    boxed_toy_1 = noise_learning_boxing_pm.run(raw_toy_isa)
    unique_toy_layers = find_unique_box_instructions(boxed_toy_1, normalize_annotations=None, undress_boxes=True)
    return boxed_toy_1, noise_learning_boxing_pm, unique_toy_layers


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As before, this boxing pass manager produces two boxes: one for the CZ layer and one for the measurement. Now, the CZ gate box carries an `InjectNoise` (from `inject_noise_targets="gates"`) and a `Twirl` annotation, while the measurement box keeps just its `Twirl`.

    The option `inject_noise_strategy="no_modification"` means that all the equivalent boxes (from `find_unique_box_instructions`) are assigned an inject noise annotation with the _same_ ref. `ref`is a `string` which uniquely identifies the Pauli-Lindblad map from which to inject noise. We can think of this as assigning all identical boxes with the same label.

    In Chapter 3 we will have to change this option to `inject_noise_strategy=uniform_modification` (PNA) and `inject_noise_strategy=individual_modification` (SLC).

    For more information on the boxing pass manager, see the documentation [here](https://qiskit.github.io/samplomatic/api/auto/samplomatic.transpiler.generate_boxing_pass_manager.html#samplomatic.transpiler.generate_boxing_pass_manager).
    """)
    return


@app.cell
def _(InjectNoise, display, get_annotation, unique_toy_layers):
    for _i, _inst in enumerate(unique_toy_layers):
        _a = get_annotation(_inst.operation, InjectNoise)
        _ref = _a.ref if _a else '(none)'
        print(f'Layer {_i}: ref = {_ref}')
        display(_inst.operation.body.draw('mpl', fold=-1, idle_wires=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In the cell above, we print the `ref` string for each unique layer and draw the circuit diagram of the corresponding layers.

    Each unique layer with an `InjectNoise` annotation carries its own `ref` string. We can see above that the CZ box has a `ref` but the measurement layer, which carries no `InjectNoise` annotation, does not.

    `ref` is the label that `NoiseLearnerV3` will use to report each unique boxes noise once learnt. The same `ref` label will be used by `InjectNoise` to find the learned noise model again at runtime.

    The slots are now declared but empty. The next subsection sets out *what* `NoiseLearnerV3` will write into them.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### What `NoiseLearnerV3` learns

    `NoiseLearnerV3` characterizes each layer as a sparse *Pauli–Lindblad* channel,

    $$\Lambda \;=\; \exp(\mathcal{L}), \qquad \mathcal{L}(\rho) \;=\; \sum_k \lambda_k\,(P_k\,\rho\,P_k - \rho),$$

    following the model formalized by van den Berg, Minev, Kandala & Temme in [*Probabilistic error cancellation with sparse Pauli–Lindblad models on noisy quantum processors* , Nat. Phys. **19**, 1116–1121 (2023)](https://www.nature.com/articles/s41567-023-02042-2). Here $\mathcal{L}$ is a superoperator (it acts on density matrices $\rho$), and $\Lambda = e^{\mathcal{L}}$ is its formal exponential. Because the generators $\{P_k\}$ are Hermitian Paulis ($P_k^\dagger = P_k$, $P_k^2 = I$), the dissipator reduces to the form on the right.

    The set of generators is fixed by the layer's connectivity: each involved qubit contributes the three 1-body Paulis $X_i, Y_i, Z_i$, and each gate edge contributes the nine non-identity 2-body Paulis $\{XX, XY, \ldots, ZZ\}$. For example, a single CZ on qubits $(0,1)$ therefore has $2\times 3 + 9 = 15$ generators in its model. The rates of these generators are what define the structure of the noise in the layer and `NoiseLearnerV3` learns the value of these generator rates. In section 2.3.2, we will learn the rates for the toy circuit and in section 2.3.3 we will inspect them, gaining insight into the structure of the noise.

    _Note_: The model does not capture:
    - __coherent error__: we assumed that coherent error hase been twirled into stochastic Pauli noise
    - __cross-layer crosstalk__: any generator outside the layer's connectivity would not appear. E.g. the generator $X_0 X_2$ would not appear in any layer that does not have gates acting on qubits $q_0$ and $q_2$.

    The noise learner is configured by three options that trade accuracy for QPU time: `num_randomizations` (independent random benchmarking circuits per configuration), `shots_per_randomization` (shots per circuit), and `layer_pair_depths` (the depths $d$ at which the layer is repeated; the learner fits the resulting fidelity-vs-depth decay to extract each generator's rate).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2.3.2  Run noise learning job on toy circuit

    With the layers boxed up and declared, we send them to the backend. For this first toy circuit example, we choose small settings (`num_randomizations=5`, `shots_per_randomization=20`, `layer_pair_depths=[1, 2]`) so the QPU time stays short.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    _Note:_
    The following cell executes a job on quantum hardware. Ensure you are ready to do this before proceeding. After first execution, we recommend pasting the job id into the `TOY_NOISE_LEARN_JOB_ID` parameter and setting `SUBMIT_TOY_NOISE_JOB = False`. This will prevent accidentally resubmitting the job and keeps the notebook re-runnable after a kernel restart.

    _Estimated QPU execution time is 3 seconds (tested on ibm_pittsburgh)._ The usage estimate above reflects backend execution time only. Queue time, calibration, and runtime session delays may be longer.
    """)
    return


@app.cell
def _(
    NoiseLearnerV3,
    NoiseLearnerV3Options,
    backend,
    service,
    unique_toy_layers,
):
    TOY_NOISE_LEARN_JOB_ID = "d9hila3sbqfc73eq4b7g" # paste job_id here on re-run
    SUBMIT_TOY_NOISE_JOB   = True # set True to submit a fresh learning job

    nl_options = NoiseLearnerV3Options(
        num_randomizations=5,
        shots_per_randomization=20,
        layer_pair_depths=[1, 2],
    )
    learner = NoiseLearnerV3(backend, nl_options)
    learner.options.environment.job_tags = ["qgss26"]

    if TOY_NOISE_LEARN_JOB_ID is not None:
        learner_job = service.job(TOY_NOISE_LEARN_JOB_ID)
        print(f"Re-using saved job: {TOY_NOISE_LEARN_JOB_ID}")
    elif SUBMIT_TOY_NOISE_JOB:
        learner_job = learner.run(unique_toy_layers)
        TOY_NOISE_LEARN_JOB_ID = learner_job.job_id()
        print(f"Submitted: {TOY_NOISE_LEARN_JOB_ID}")
    else:
        print("Set SUBMIT_TOY_NOISE_JOB=True to submit a fresh job, "
              "or paste a saved job id into TOY_NOISE_LEARN_JOB_ID and re-run.")
    return TOY_NOISE_LEARN_JOB_ID, learner


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    After submitting your noise learning job, run the cell below to check on the status of your job. It should either be: `QUEUED`, `RUNNING` or `DONE`. Once the job is done, proceed to the next cell.
    """)
    return


@app.cell
def _(TOY_NOISE_LEARN_JOB_ID, service):
    learner_job_1 = service.job(TOY_NOISE_LEARN_JOB_ID)
    print(f'{TOY_NOISE_LEARN_JOB_ID}  (status: {learner_job_1.status()})')
    return (learner_job_1,)


@app.cell
def _(learner_job_1):
    if learner_job_1.status() == 'DONE':
        toy_noise_result = learner_job_1.result()
    else:
        print(f'Not done yet (status={learner_job_1.status()}). Re-run cell when DONE.')
    return (toy_noise_result,)


@app.cell
def _(toy_noise_result, unique_toy_layers):
    if 'toy_noise_result' in dir() and toy_noise_result is not None:
        toy_refs_to_noise = toy_noise_result.to_dict(unique_toy_layers, require_refs=False)
        print(f"toy_refs_to_noise has {len(toy_refs_to_noise)} entries")
    else:
        print("Run the noise-learning cell above and wait for it to finish first.")
    return (toy_refs_to_noise,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In the cell above, we use the `to_dict` method to collect the results of the noise learning job into `toy_refs_to_noise`. There should be one Pauli-Lindblad model per learned layer, each labelled by the same `ref`s used in the boxed circuit. We know the toy circuit has only one layer with the `InjectNoise` annotation (the CZ layer). So we expect the noise learning job to return a single learned noise model. We see this is the case.

    The slots are now full. To see what was actually learned, in section 2.3.3, we will inspect the learned noise model for the single CZ layer.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2.3.3  Inspecting the learned noise model

    In the cell below, we use the method `PauliLindbladMap.to_sparse_list()` to return the noise model as a sequence of `(pauli, qubits, rate)` tuples. There is one tuple per nonzero generator of $\mathcal{L}$.

    We sort these tuples by rate to show which error channels dominate the CZ layer and print the top 10 generators. This information is the input every per-layer error mitigation strategy uses to decide where to spend its budget. we will see how this is implemented for PNA, PEC, and SLC in Chapter 3.
    """)
    return


@app.cell
def _(toy_refs_to_noise):
    if "toy_refs_to_noise" not in globals() or not toy_refs_to_noise:
        print("No learned toy noise model yet. Run the noise-learning result cell above first.")
    else:
        ref0, plm0 = next(iter(toy_refs_to_noise.items()))
        generators = plm0.to_sparse_list()
        generators.sort(key=lambda g: -abs(g[2]))

        print(f"Layer ref = {ref0}, total generators = {len(generators)}\n")
        print(f"  {'Pauli':<6}{'qubits':<14}{'rate':>10}")
        print(f"  {'-'*6}{'-'*14}{'-'*10}")
        for pauli, qubits, rate in generators[:10]:
            print(f"  {pauli:<6}{str(qubits):<14}{rate:>10.4e}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    One annotation still remains to introduce: `ChangeBasis`, for measurements in non-$Z$ bases. We do that next in section 2.4.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2.4  The `ChangeBasis` annotation

    `ChangeBasis` is needed for measurements in non-$Z$ bases. It follows the same pattern as `InjectNoise`: the annotation is attached statically and supplied at runtime. It goes on a measurement box, and its values are bound at runtime through the samplex's `basis_changes` input.

    We don't make use of `ChangeBasis` in the rest of Chapter 2 as the observable we consider in section 2.6 is diagonal in the computational basis. But, in Chapter 3 we use it once PNA introduces a noise mitigating observable $\tilde{O}$ with non-$Z$ terms.

    The cell below shows that `measure_annotations="all"` adds both `Twirl` and `ChangeBasis` to the measurement box, which adds a `basis_changes.<ref>` slot to `samplex.inputs()`.
    """)
    return


@app.cell
def _(build, generate_boxing_pass_manager, raw_toy_isa):
    # A boxing pass manager that ALSO annotates the measurement box with
    # ChangeBasis. 
    change_basis_pm = generate_boxing_pass_manager(
        enable_gates=True,
        enable_measures=True,
        measure_annotations="all",
        twirling_strategy="active",
        inject_noise_targets="gates",
        inject_noise_strategy="no_modification",
    )

    demo_boxed = change_basis_pm.run(raw_toy_isa)
    _, demo_samplex = build(demo_boxed)
    print(demo_samplex)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The samplex now reports two **Inputs** instead of none as we saw in section 2.1.2 when there were only `Twirl` annotations on the boxes. The two inputs are:
    - `basis_changes.basisX` (where X is an integer): the basis rotation that occurs per-randomization to be applied at measurement. This is encoded symplectically — `I=0, Z=1, X=2, Y=3`
    - `pauli_lindblad_maps.<ref>`: the learned noise model for the gate box

    Adding `ChangeBasis` and `InjectNoise` to the circuit changed what data the samplex expects to receive at run time. The `ref` strings (of the general form `basisX`, `rYYYY` where X is an integer and Y is an integer or letter) are the dictionary keys we will use to supply that data.

    The **Outputs** gain `pauli_signs` as well: with `InjectNoise` present, each randomization samples a Pauli error from the noise model, and the parity of negative-rate factors becomes a $\pm 1$ correction that the post-processing applies to expectation values later.

    So the same pattern carries through here: annotations *declare* what is needed (e.g. basis change, noise model, twirl), and the samplex *exposes* the slots and reports the runtime-bound results. Section 2.5 supplies the values for these slots and runs the program with `Executor`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2.5  Submitting a job with the `Executor`

    Now, we have learned the noise in the circuit, we submit a job using the [__Executor primitive__](https://quantum.cloud.ibm.com/docs/en/guides/get-started-with-executor). `Executor` is the Runtime primitive that honors Samplomatic annotations.

    As a quick refresher, remember that the __Sampler__ and __Estimator__ primitives take in a [Primitive Unified Bloc (PUB)](https://quantum.cloud.ibm.com/docs/en/guides/primitive-input-output#pubs). PUBs are tuples of which `QuantumCircuit`'s, parameters and for the Estimator, observables, are some of their inputs.

    The inputs and outputs of the Executor primitive are very different from those of the Sampler and Estimator primitives. Instead of taking a list of PUBs as the input, Executor takes a `QuantumProgram`, which contains a list of `QuantumProgramItem` objects. These container classes allow for more flexibility than a PUB, which is a simple tuple data structure. These `QuantumProgramItem`s can either be a:
    - `CircuitItem` which stores a circuit and its parameter values
    - `SamplexItem` which stores a template circuit, a samplex and samplex arguments

    Here, we are focussing on an Executor job that uses `SamplexItem`'s. First, we use `build` to build the template and samplex for the toy circuit:
    """)
    return


@app.cell
def _(boxed_toy_1, build):
    toy_template, toy_samplex = build(boxed_toy_1)
    print(toy_samplex)
    return toy_samplex, toy_template


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Next, we construct the samplex arguments. The keys of `samplex_arguments` must match those returned by `samplex.inputs()` exactly, including the auto-generated ref names like `noise_scales.<ref>` or `basis_changes.<ref>`.
    """)
    return


@app.cell
def _(toy_refs_to_noise, toy_samplex):
    samplex_arguments = (
        toy_samplex.inputs()
        .make_broadcastable()
        .bind(pauli_lindblad_maps=toy_refs_to_noise)
    )
    return (samplex_arguments,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we can construct the `QuantumProgram`. We use the method `append_samplex_item(...)` to add a `SamplexItem` to the `QuantumProgram` (more than one can coexist, which is how batched mitigated jobs are built).
    """)
    return


@app.cell
def _(QuantumProgram, samplex_arguments, toy_samplex, toy_template):
    program = QuantumProgram(shots=64)
    program.append_samplex_item(
        toy_template,
        samplex=toy_samplex,
        samplex_arguments=samplex_arguments,
        shape=(16,),
    )
    return (program,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We are now ready to run the Executor job on the QPU.

    _Note:_ The following cell executes a job on quantum hardware. Ensure you are ready to do this before proceeding. After first execution, we recommend pasting the job id into the `TOY_EXECUTOR_JOB_ID` parameter and setting `SUBMIT_TOY_EXEC_JOB = False`. This will prevent accidentally resubmitting the job and keeps the notebook re-runnable after a kernel restart.

    _Estimated QPU execution time is 2 seconds (tested on ibm_fez)._ The usage estimate reflects backend execution time only. Queue time, calibration, and runtime session delays may be longer.
    """)
    return


@app.cell
def _(Executor, backend, program, service):
    TOY_EXECUTOR_JOB_ID = "d9hila3sbqfc73eq4b7g" # paste job_id here on re-run
    SUBMIT_TOY_EXEC_JOB = True # set True to submit a fresh executor job
    _executor = Executor(backend)
    _executor.options.environment.job_tags = ['qgss26']
    if TOY_EXECUTOR_JOB_ID is not None:
        toy_job = service.job(TOY_EXECUTOR_JOB_ID)
        print(f'Re-using saved job: {TOY_EXECUTOR_JOB_ID}')
    elif SUBMIT_TOY_EXEC_JOB:
        toy_job = _executor.run(program)
        TOY_EXECUTOR_JOB_ID = toy_job.job_id()
        print(f'Submitted Executor job: {TOY_EXECUTOR_JOB_ID}')
    else:
        print('Set SUBMIT_TOY_EXEC_JOB=True to submit a fresh executor job, or paste a saved job id into TOY_EXECUTOR_JOB_ID and re-run.')
    return (TOY_EXECUTOR_JOB_ID,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Check on the status of the job with the cell below:
    """)
    return


@app.cell
def _(TOY_EXECUTOR_JOB_ID, service):
    toy_job_1 = service.job(TOY_EXECUTOR_JOB_ID)
    print(f'{TOY_EXECUTOR_JOB_ID}  (status: {toy_job_1.status()})')
    return (toy_job_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Extract the results and look at the expectation value of $Z$ on qubit 0 and qubit 1 separately:
    """)
    return


@app.cell
def _(np, toy_job_1):
    if toy_job_1.status() == 'DONE':
        toy_result = toy_job_1.result()
        _data = toy_result[0]
        _meas = _data['c']
        _flips = _data['measurement_flips.c']
        print(f'meas shape  : {_meas.shape}')
        print(f'flips shape : {_flips.shape}')
        _corrected = np.bitwise_xor(_meas, _flips)
        _z_vals = 1 - 2 * _corrected
        _z_means = _z_vals.reshape(-1, _z_vals.shape[-1]).mean(axis=0)
        print(f'\n<Z_0> = {_z_means[0]:+.4f}')
        print(f'<Z_1> = {_z_means[1]:+.4f}')
    else:
        print(f'Not done yet (status={toy_job_1.status()}). Re-run cell when DONE.')
    return (toy_result,)


@app.cell
def _(toy_result):
    toy_result[0]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The ideal value is $\langle Z_i \rangle = +1$ on both qubits. This is because CZ acts trivially on $|00\rangle$, so the final state should remain $|00\rangle$. Any deviation from this state is hardware noise. In a typical run the deviation is at the percent level, with a size depending on backend, qubit layout, calibration at queue time, and shot budget.

    There are typically three contributions: __readout error__ on the two physical qubits, __idle decoherence__ during the single-qubit dressing rotations, and __residual stochastic Pauli error__ from the CZ.

    The deviation is also typically asymmetric between the two qubits because we transpiled at `optimization_level=0`: the qubit pair was chosen by index rather than by fidelity, so each qubit carries a different error budget. The dominant generator rates in 2.3.3 (order $10^{-3}$) give us an order-of-magnitude diagnostic, but the observed deviation also includes readout error, idle time, layout-dependent calibration, and accumulated box overhead, so the rates alone do not determine the gap.

    Small per-layer rates like we saw in section 2.3.3 need to compound for mitigation effects to be visible. In section 2.6, we take the same pipeline to a deeper circuit (the 1D Ising mirror) and produces the `refs_to_noise_models` dict that Chapter 3's PNA and SLC will consume.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2.6  Putting it together: the 1D Ising chain

    Up until now, we have been using a 2-qubit toy CZ circuit to introduce each Samplomatic tool and understand the overall workflow. From here on, we work with a 1D transverse-field Ising chain. This is the same system Chapter 3 continues with.

    The boxing → build → noise-learning → execute workflow is the same and the circuit is now deep enough for per-layer rates to compound into a measurable deviation.

    There are two exercises at the end of this section that put your knowledge of everything we have covered in Chapter 2 to the test. Exercise 2 asks you to box a deeper Ising mirror so `NoiseLearnerV3` has more layers to characterize, and Exercise 3 assembles the resulting program — boxed circuit, learned noise, samplex, `QuantumProgram` — into the form the `Executor` consumes.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2.6.1  Hamiltonian and Trotter circuit

    The system under consideration is the __1D transverse-field Ising chain__, with the following Hamiltonian:

    $$H \;=\; -J \sum_{\langle i,j\rangle} Z_i Z_j \;+\; h \sum_i X_i.$$

    This Hamiltonian is a standard utility-scale benchmark; the same Hamiltonian (on a 2D heavy-hex lattice) drove IBM's 127-qubit utility demonstration, [Kim et al., *Evidence for the utility of quantum computing before fault tolerance*, Nature **618**, 500–505 (2023)](https://www.nature.com/articles/s41586-023-06096-3). We use a 1D chain because it makes the brickwork structure easy to inspect, and Chapter 3's PNA and SLC tutorials continue with the same system.

    We define the helper function `construct_ising_circuit(num_qubits, num_trotter_steps, rx_angle, barrier=True)` below. This function builds each Ising circuit by applying $S^\dagger$ on both qubits followed by a $\mathrm{CZ}$. Because all three are diagonal and commute, the sequence equals $R_{ZZ}(-\pi/2)$ up to a global phase. Writing the circuit this way rather than as a parametric `RZZ` keeps every two-qubit gate a CZ, so the boxing and dressing machinery from sections 2.1–2.5 applies directly.

    The circuit is a simple fixed-angle, kicked-Ising-style Trotter step. The transverse-field rotation is controlled by `rx_angle` and the ZZ-interaction is realized by a fixed CZ-based block. We won't go into any more detail here about the physics of the Ising circuit as the focus of this lab is on noise learning and error mitigation and the Ising circuit simply provides us with a nice example to work with.
    """)
    return


@app.cell
def _(QuantumCircuit, np):
    def construct_ising_circuit(num_qubits: int, num_trotter_steps: int, rx_angle: float, barrier: bool=True) -> QuantumCircuit:
        qc = QuantumCircuit(num_qubits)
        for _ in range(num_trotter_steps):
            qc.rx(rx_angle, range(num_qubits))
            if barrier:
                qc.barrier()
            for first_qubit in (1, 2):
                for _idx in range(first_qubit, num_qubits, 2):
                    qc.sdg([_idx - 1, _idx])
                    qc.cz(_idx - 1, _idx)
            if barrier:
                qc.barrier()
        return qc
    ising = construct_ising_circuit(num_qubits=4, num_trotter_steps=1, rx_angle=np.pi / 8)
    ising.draw('mpl', fold=-1)
    return construct_ising_circuit, ising


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2.6.2  The mirror trick

    In Chapter 3, we will be comparing _unmitigated_ results to _error mitigated_ results for the 1D Ising chain circuit. In order to verify the effect of the error mitigation techniques implemented, we need to know the ideal result that we are aiming for. For an arbitrary circuit, this would require a separate classical simulation, and at utility scale that simulation is itself expensive or even untractable. This is where the mirror trick comes in.

    The mirror trick takes the circuit of interest and appends its inverse onto the end of the circuit, i.e. we are applying the circuit forwards and then backwards. For an ideal quantum computer with no noise, the quantum state will return to the initial state: $|0\rangle^{\otimes N}$. A useful consequence of this is that we can easily calculate the ideal expectation value for any observable without having to perform any expensive classical simulations of the circuit. For example,  we know the ideal expectation value of $Z$ on every qubit is 1, i.e. $\langle Z_i \rangle = +1$, for all $i$. Any deviation of the measured $\langle Z_i \rangle$ from $+1$ is due hardware noise. That is what makes the mirror a standard benchmark for error mitigation.

    In Qiskit, this is implemented using `ising.compose(ising.inverse())`, appending $U^\dagger$ to $U$. With Qiskit's right-to-left convention this realizes $U_\text{mirror} = U^\dagger U = I$.
    """)
    return


@app.cell
def _(isa_pm, ising):
    mirror = ising.compose(ising.inverse())
    mirror.measure_all()
    mirror_isa = isa_pm.run(mirror)
    mirror_isa.draw("mpl", fold=-1, idle_wires=False, scale=0.5)
    return (mirror_isa,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2.6.3  Boxing the Ising mirror

    We have the circuit and the workflow; the next step is to put them together.

    Below we convert the mirrored circuit into the form that `NoiseLearnerV3` consumes. We reuse `noise_learning_boxing_pm` from section 2.3.1 unchanged: both circuits are built from CZ entangling gates, so the same boxing strategy applies and each gate layer ends up wrapped in a `Twirl` + `InjectNoise` box.

    `find_unique_box_instructions(...)` then collapses the boxed circuit to its *structurally distinct* layers, remember that equivalent boxes share one noise model so `NoiseLearnerV3` only needs to characterize each unique layer once.
    - `undress_boxes=True` strips the random-Pauli dressing before comparison to find unique layers, since dressing differs between boxes but the underlying layer does not.
    - `normalize_annotations=None` keeps only `Twirl` and `InjectNoise` box annotations and discards everything else
    """)
    return


@app.cell
def _(
    InjectNoise,
    find_unique_box_instructions,
    get_annotation,
    mirror_isa,
    noise_learning_boxing_pm,
):
    boxed_circuit_ising = noise_learning_boxing_pm.run(mirror_isa)
    unique_layers_ising = find_unique_box_instructions(boxed_circuit_ising, normalize_annotations=None, undress_boxes=True)
    print(f'Unique 2Q-gate layers: {len(unique_layers_ising)}')
    for _i, _inst in enumerate(unique_layers_ising):
        _a = get_annotation(_inst.operation, InjectNoise)
        _ref = _a.ref if _a is not None else '(none)'
        print(f'  layer {_i}: ref = {_ref}')
    boxed_circuit_ising.draw('mpl', idle_wires=False)
    return (unique_layers_ising,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    With the unique layers extracted, we inspect them: their `ref` strings (which `NoiseLearnerV3` will report back under) and the gate content of each. We see that even though the Ising circuit has 5 boxes, there are only 3 unique layers, one of which is the measurement layer.
    """)
    return


@app.cell
def _(InjectNoise, display, get_annotation, unique_layers_ising):
    for _i, _inst in enumerate(unique_layers_ising):
        _a = get_annotation(_inst.operation, InjectNoise)
        _ref = _a.ref if _a else '(none)'
        print(f'Layer {_i}: ref = {_ref}')
        display(_inst.operation.body.draw('mpl', fold=-1, idle_wires=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2.6.4  Learning the noise

    The boxed circuit is ready; now we can learn its noise. We pass `unique_layers_ising` to `NoiseLearnerV3` and assemble the result into `refs_to_noise_models_ising`, a dictionary mapping each layer's `InjectNoise.ref` to the learned `PauliLindbladMap`. Once both gate layers are characterized, we can read off how different their noise profiles are.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    _Note:_ The following cell executes a job on quantum hardware. Ensure you are ready to do this before proceeding.After first execution, we recommend pasting the job id into the `NOISE_LEARN_JOB_ID_ISING` parameter and setting  `SUBMIT_NOISE_JOB_ISING = False`. This will prevent accidentally resubmitting the job and keeps the notebook re-runnable after a kernel restart.

    _Estimated QPU execution time is 10 seconds (tested on ibm_fez)._ The usage estimate reflects backend execution time only. Queue time, calibration, and runtime session delays may be longer.
    """)
    return


@app.cell
def _(learner, service, unique_layers_ising):
    NOISE_LEARN_JOB_ID_ISING = "d9hila3sbqfc73eq4b7g" # paste job_id here on re-run
    SUBMIT_NOISE_JOB_ISING   = True # set True to submit a fresh learning job
    learner.options.environment.job_tags = ["qgss26"]

    if NOISE_LEARN_JOB_ID_ISING is not None:
        learner_job_ising = service.job(NOISE_LEARN_JOB_ID_ISING)
        print(f"Re-using saved job: {NOISE_LEARN_JOB_ID_ISING}")
    elif SUBMIT_NOISE_JOB_ISING:
        learner_job_ising = learner.run(unique_layers_ising)
        NOISE_LEARN_JOB_ID_ISING = learner_job_ising.job_id()
        print(f"Submitted: {NOISE_LEARN_JOB_ID_ISING}")
    else:
        print("Set SUBMIT_NOISE_JOB_ISING=True to submit a fresh job, "
              "or paste a saved job id into NOISE_LEARN_JOB_ID_ISING and re-run.")
    return (NOISE_LEARN_JOB_ID_ISING,)


@app.cell
def _(NOISE_LEARN_JOB_ID_ISING, service):
    learner_job_ising_1 = service.job(NOISE_LEARN_JOB_ID_ISING)
    print(f'{NOISE_LEARN_JOB_ID_ISING}  (status: {learner_job_ising_1.status()})')
    return (learner_job_ising_1,)


@app.cell
def _(learner_job_ising_1):
    if learner_job_ising_1.status() == 'DONE':
        noise_learner_result_ising = learner_job_ising_1.result()
    else:
        print(f'Not done yet (status={learner_job_ising_1.status()}). Re-run cell when DONE.')
    return (noise_learner_result_ising,)


@app.cell
def _(noise_learner_result_ising, unique_layers_ising):
    if 'noise_learner_result_ising' in dir() and noise_learner_result_ising is not None:
        refs_to_noise_models_ising = noise_learner_result_ising.to_dict(unique_layers_ising, require_refs=False)
        print(f"refs_to_noise_models_ising has {len(refs_to_noise_models_ising)} entries")
    else:
        print("Run the noise-learning cell above and wait for it to finish first.")
    return (refs_to_noise_models_ising,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The dict is ready: each entry is one learned layer. To see what was learned, the cell below prints the two layers properties. For each layer, we print  the number of generators, how many of those carry a nonzero rate, the largest generator rate, the sum of all the rates in the layer (total noise), and which Pauli term contributes the most.
    """)
    return


@app.cell
def _(refs_to_noise_models_ising):
    if 'refs_to_noise_models_ising' not in globals() or not refs_to_noise_models_ising:
        print('Fetch a completed Ising noise-learning result first.')
    else:
        print('Layer comparison:\n')
        print(f"  {'ref':<10}{'#gens':>8}{'#nonzero':>10}{'max rate':>14}{'sum rates':>14}{'top generator':>22}")
        print('  ' + '─' * 78)
        for _ref, _plm in refs_to_noise_models_ising.items():
            _gens = _plm.to_sparse_list()
            _rates = [abs(r) for _, _, r in _gens]
            nonzero = [r for r in _rates if r > 0]
            top = max(_gens, key=lambda g: abs(g[2]))
            top_label = f'{top[0]}@{tuple(top[1])} ({top[2]:.2e})'
            print(f'  {_ref:<10}{len(_gens):>8}{len(nonzero):>10}{max(_rates):>14.4e}{sum(_rates):>14.4e}{top_label:>22}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    While the two unique layers play similar roles in the brickwork — they implement the even bonds (here the layer with two CZ gates) and odd bonds (here the layer with just one CZ gate). The table above shows that their learned noise is different.

    The `sum rates` column gives each layer's total noise; the `top generator` column shows which channel dominates, and the dominant channel of one layer can be weak or absent in the other; the `#nonzero` column shows that one layer can concentrate its noise on fewer channels while the other spreads it across more.

    This per-layer noise difference is the reason we want to implement error mitigation per layer. A uniform correction tuned for one layer's dominant generator would miss or over-correct the other's. This is precisely the gap that Runtime's whole-circuit `EstimatorOptions` (section 1.1) cannot close.

    We will see in Chapter 3 how PNA absorbs each layer's *own* inverse channel into a noise mitigating observable and how SLC scales each layer along its own lightcone. Both methods read off the per-layer rates we just printed.

    _Note:_ Your specific results will vary depending on the QPU backend you are using and the noise learned from the QPU. Noise drifts and calibrations happen daily. Even for the same QPU, the noise will change over time.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 2 — Box a deeper Ising mirror

    Sections 2.6.1–2.6.4 walked through the full noise learning workflow on a 4-qubit, 1-Trotter-step Ising circuit.

    Run the same workflow yourself on a deeper circuit. Exercise 3 will then take what you build here and assemble it into an `Executor` program.

    - **Circuit:** 6-qubit Ising chain, 2 Trotter steps, `rx_angle = π/8`, `barrier=False`
    - **Mirror:** compose `ising_ex2`, add a `barrier()`, compose `ising_ex2.inverse()`, then `measure_all()`
    - **Transpile:** through `isa_pm`
    - **Box:** through `noise_learning_boxing_pm`

    The `barrier()` between the forward and inverse halves prevents the transpiler's optimization passes from cancelling the mirror into the identity.

    Fill in the cell below so that `boxed_circuit_ex2` is a Twirl + InjectNoise–annotated boxed mirror circuit that `build()` accepts.
    """)
    return


@app.cell
def _(
    QuantumCircuit,
    construct_ising_circuit,
    isa_pm,
    noise_learning_boxing_pm,
    np,
):
    ising_ex2 = None
    mirror_ex2 = None
    boxed_circuit_ex2 = None

    #TODO: Your code below.

    num_qubits_ex2 = 6
    num_trotter_steps_ex2 = 2
    rx_angle_ex2 = np.pi / 8

    # 1. Build the 6-qubit, 2-step Ising circuit (rx_angle = π/8, barrier=False)
    ising_ex2 = construct_ising_circuit(
        num_qubits_ex2, num_trotter_steps_ex2, rx_angle_ex2, barrier=False
    )

    # 2. Build mirror_ex2: forward + barrier + inverse + measure_all
    #    (The barrier keeps the transpiler from cancelling the mirror.)
    mirror_ex2 = QuantumCircuit(num_qubits_ex2)
    mirror_ex2.compose(ising_ex2, inplace=True)   # forward
    mirror_ex2.barrier()
    mirror_ex2.compose(ising_ex2.inverse(), inplace=True)   # inverse
    mirror_ex2.measure_all()

    # 3. Transpile through isa_pm and box through noise_learning_boxing_pm
    mirror_ex2_isa = isa_pm.run(mirror_ex2)
    boxed_circuit_ex2 = noise_learning_boxing_pm.run(mirror_ex2_isa)
    return boxed_circuit_ex2, ising_ex2, mirror_ex2


@app.cell
def _(boxed_circuit_ex2, grade_lab3_ex2, ising_ex2, mirror_ex2):
    # grade your answer
    grade_lab3_ex2(ising_ex2, mirror_ex2, boxed_circuit_ex2)
    return


@app.cell
def _(check_progress):
    # check your progress across all the labs
    check_progress()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In Exercise 2 you produced `boxed_circuit_ex2`, the boxed Ising mirror circuit with an `InjectNoise` slot on every gate layer. This boxed circuit is now ready for characterization.

    Before Exercise 3 assembles it into a runnable program, we fill those slots: this is the same `NoiseLearnerV3` workflow as in section 2.6.4, now on the deeper circuit. We run it the exact same way: submit the job, poll its status, then fetch the result. From the learned noise, we produce `refs_to_noise_models_ex3`, a `{ref: PauliLindbladMap}` dict that we need for Exercise 3.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Learn the noise (necessary for Exercise 3):

    _Note:_ The following cell executes a job on quantum hardware. Ensure you are ready to do this before proceeding. After first execution, we recommend pasting the job id into the `NOISE_LEARN_JOB_ID_EX3` parameter and setting `SUBMIT_NOISE_JOB_EX3 = False`. This will prevent accidentally resubmitting the job and keeps the notebook re-runnable after a kernel restart.

    _Estimated QPU execution time is 4 seconds (tested on ibm_fez)._ The usage estimate reflects backend execution time only. Queue time, calibration, and runtime session delays may be longer.
    """)
    return


@app.cell
def _(boxed_circuit_ex2, find_unique_box_instructions, learner, service):
    unique_layers_ex3 = find_unique_box_instructions(
        boxed_circuit_ex2,
        normalize_annotations=None,
        undress_boxes=True,
    )

    NOISE_LEARN_JOB_ID_EX3 = "d9jguv3jf64c739gq5hg" # paste a saved job id to re-fetch
    SUBMIT_NOISE_JOB_EX3   = True # set True to submit a fresh job
    learner.options.environment.job_tags = ["qgss26"]

    if NOISE_LEARN_JOB_ID_EX3 is not None:
        learner_job_ex3 = service.job(NOISE_LEARN_JOB_ID_EX3)
        print(f"Re-using saved job: {NOISE_LEARN_JOB_ID_EX3}")
    elif SUBMIT_NOISE_JOB_EX3:
        learner_job_ex3 = learner.run(unique_layers_ex3)
        NOISE_LEARN_JOB_ID_EX3 = learner_job_ex3.job_id()
        print(f"Submitted: {NOISE_LEARN_JOB_ID_EX3}")
    else:
        print("Set SUBMIT_NOISE_JOB_EX3=True to submit a fresh job, "
              "or paste a saved job id into NOISE_LEARN_JOB_ID_EX3 and re-run.")
    return NOISE_LEARN_JOB_ID_EX3, unique_layers_ex3


@app.cell
def _(NOISE_LEARN_JOB_ID_EX3, service):
    learner_job_ex3_1 = service.job(NOISE_LEARN_JOB_ID_EX3)
    status = learner_job_ex3_1.status()
    print(f'job_id : {NOISE_LEARN_JOB_ID_EX3}')
    print(f'status : {status}')
    if status == 'DONE':
        print('\n  Ready — proceed to Exercise 3.')
    return (learner_job_ex3_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Once the job is `DONE`, fetch the result by running the cell below and collect it into `refs_to_noise_models_ex3`: the `{ref: PauliLindbladMap}` dict. one learned model per layer. We need this object for Exercise 3.
    """)
    return


@app.cell
def _(learner_job_ex3_1, unique_layers_ex3):
    noise_result_ex3 = learner_job_ex3_1.result()
    refs_to_noise_models_ex3 = noise_result_ex3.to_dict(unique_layers_ex3, require_refs=False)
    print(f'Learned noise for {len(refs_to_noise_models_ex3)} layers: {list(refs_to_noise_models_ex3.keys())}')
    return (refs_to_noise_models_ex3,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The learned noise models can be understood more clearly as a figure than as raw rates. The plot below shows each layer's 15 largest noise generators, with 1-body (single-qubit) and 2-body (two-qubit) terms colored separately. You can clearly see which generators dominant each layers noise model.
    """)
    return


@app.cell
def _(Patch, plt, refs_to_noise_models_ex3):
    # plot the top 15 noise generators per layer
    _fig, axes = plt.subplots(1, len(refs_to_noise_models_ex3), figsize=(12, 4))
    if len(refs_to_noise_models_ex3) == 1:
        axes = [axes]
    for _ax, (_ref, _plm) in zip(axes, refs_to_noise_models_ex3.items()):
        _gens = sorted(_plm.to_sparse_list(), key=lambda g: -abs(g[2]))[:15]
        _labels = [f'{_p}@{tuple(q)}' for _p, q, _ in _gens]
        _rates = [r for _, _, r in _gens]
        _colors = ['#2c7fb8' if len(_p) == 1 else '#d95f0e' for _p, _, _ in _gens]
        _ax.barh(range(len(_labels)), _rates, color=_colors)
        _ax.set_yticks(range(len(_labels)))
        _ax.set_yticklabels(_labels, fontsize=8)
        _ax.invert_yaxis()
        _ax.set_xlabel('Rate')
        _ax.set_title(f'Layer {_ref}')
        _ax.grid(axis='x', alpha=0.3)
    _fig.legend(handles=[Patch(facecolor='#2c7fb8', label='1-qubit'), Patch(facecolor='#d95f0e', label='2-qubit')], loc='upper right', fontsize=9)
    _fig.suptitle('Top 15 noise generators per layer')
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we have the noise model, in particular the dict `noise_result_ex3`, we can run an Executor job.

    In, Exercise 3, we ask you to prepare the Executor job using `noise_result_ex3` and the `build()` function to prepare the template and samplex using the boxed circuit you prepared in Exercise 2.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 3 — Assemble an `Executor` program

    <div class="alert alert-block alert-success">

    The noise learning job above learned `refs_to_noise_models_ex3`, the `{ref: PauliLindbladMap}` dict with one noise model per layer of `boxed_circuit_ex2`.

    This exercise plugs that noise model into the data structure the `Executor` runs, using all three tools introduced in Chapter 2 in one pass: the **Samplomatic** `build`, the **NoiseLearnerV3** result you just produced, and the **Executor**'s `QuantumProgram`.

    Build the program in four steps:

    - **Build:** call `build(boxed_circuit_ex2)` to get `template_ex3` and `samplex_ex3`
    - **Inspect:** `samplex_ex3.inputs()` reports which `pauli_lindblad_maps.<ref>` slots the samplex expects — these refs must match the keys of `refs_to_noise_models_ex3`
    - **Bind:** from `samplex_ex3.inputs()`, call `make_broadcastable()` then `bind(pauli_lindblad_maps=...)` with the learned dict → `samplex_args_ex3`
    - **Assemble:** create a `QuantumProgram(shots=64)` and `append_samplex_item(...)` the template, samplex, and arguments → `program_ex3`

    The grader checks that the program is assembled correctly — it does not run on hardware. An optional cell afterwards shows the expectation values this program returns from a real backend run.

    </div>
    """)
    return


@app.cell
def _(QuantumProgram, boxed_circuit_ex2, build, refs_to_noise_models_ex3):
    #TODO: Add Your code here and set the missing values.

    template_ex3      = None
    samplex_ex3       = None
    samplex_args_ex3  = None
    program_ex3       = None


    # 1. Build the template and samplex from boxed_circuit_ex2
    template_ex3, samplex_ex3 = build(boxed_circuit_ex2)

    # 2. Inspect what the samplex expects (look at the pauli_lindblad_maps.<ref> slots)
    print(samplex_ex3.inputs())

    # 3. Bind the learned noise models into the samplex inputs.
    #    Start from samplex_ex3.inputs(), make it broadcastable, then bind the
    #    refs_to_noise_models_ex3 dict to the `pauli_lindblad_maps` argument.
    samplex_args_ex3 = (
        samplex_ex3.inputs()
        .make_broadcastable()
        .bind(pauli_lindblad_maps=refs_to_noise_models_ex3)
    )

    # 4. Assemble the QuantumProgram with a single samplex item
    program_ex3 = QuantumProgram(shots=64)
    program_ex3.append_samplex_item(
        template_ex3,
        samplex=samplex_ex3,
        samplex_arguments=samplex_args_ex3,
        shape=(16, )
    )
    return program_ex3, samplex_args_ex3, samplex_ex3, template_ex3


@app.cell
def _(
    grade_lab3_ex3,
    program_ex3,
    refs_to_noise_models_ex3,
    samplex_args_ex3,
    samplex_ex3,
    template_ex3,
):
    # grade your answer
    grade_lab3_ex3(
        template_ex3,
        samplex_ex3,
        samplex_args_ex3,
        program_ex3,
        refs_to_noise_models_ex3,
    )
    return


@app.cell
def _(check_progress):
    # check your progress across all the labs
    check_progress()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### (Optional) Running the program on hardware

    This step is optional and not required to proceed to Chapter 3. It shows what `program_ex3` returns when actually run on hardward. This section follows the same pattern as section 2.5, where we submitted an `Executor` job for the toy circuit.

    The circuit here is the Ising mirror circuit, so the ideal result is $\langle Z_i\rangle = +1$ on every qubit. Any deviation you see from this is due to noise the boxed-and-learned pipeline still leaves. In Chapter 3, we will implement error mitigation techniques to improve the results.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    _Note:_ The following cell executes a job on quantum hardware. Ensure you are ready to do this before proceeding. After first execution, we recommend pasting the job id into the `EXECUTOR_JOB_ID_EX3` parameter and setting `SUBMIT_EXECUTOR_JOB_EX3 = False`. This will prevent accidentally resubmitting the job and keeps the notebook re-runnable after a kernel restart.

    _Estimated QPU execution time is 2 seconds (tested on ibm_pittsburgh)_. The usage estimate above reflects backend execution time only. Queue time, calibration, and runtime session delays may be longer.
    """)
    return


@app.cell
def _(Executor, backend, program_ex3, service):
    _executor = Executor(backend)
    EXECUTOR_JOB_ID_EX3 = None
    SUBMIT_EXECUTOR_JOB_EX3 = "d9jguv3jf64c739gq5hg" # paste an Executor job_id here on re-run
    _executor.options.environment.job_tags = ['qgss26']  # set True to submit a fresh Executor job
    if EXECUTOR_JOB_ID_EX3 is not None:
        exec_job_ex3 = service.job(EXECUTOR_JOB_ID_EX3)
        print(f'Re-using saved job: {EXECUTOR_JOB_ID_EX3}')
    elif SUBMIT_EXECUTOR_JOB_EX3:
        exec_job_ex3 = _executor.run(program_ex3)
        EXECUTOR_JOB_ID_EX3 = exec_job_ex3.job_id()
        print(f'Submitted Executor job: {EXECUTOR_JOB_ID_EX3}')
    else:
        print('Set SUBMIT_EXECUTOR_JOB_EX3=True to submit a fresh Executor job, or paste a saved job id into EXECUTOR_JOB_ID_EX3 and re-run.')
    return (EXECUTOR_JOB_ID_EX3,)


@app.cell
def _(EXECUTOR_JOB_ID_EX3, service):
    exec_job_ex3_1 = service.job(EXECUTOR_JOB_ID_EX3)
    print(f'{EXECUTOR_JOB_ID_EX3}  (status: {exec_job_ex3_1.status()})')
    return (exec_job_ex3_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Plot the results:
    """)
    return


@app.cell
def _(exec_job_ex3_1, np, plt):
    if exec_job_ex3_1.status() == 'DONE':
        exec_result_ex3 = exec_job_ex3_1.result()
        _data = exec_result_ex3[0]
        _meas = _data['meas']
        _flips = _data['measurement_flips.meas']
        _corrected = np.bitwise_xor(_meas, _flips)
        _z_vals = 1 - 2 * _corrected
        _z_means = _z_vals.reshape(-1, _z_vals.shape[-1]).mean(axis=0)
        _fig, _ax = plt.subplots(figsize=(8, 4))
        _ax.bar(range(len(_z_means)), _z_means, color='#2c7fb8')
        _ax.axhline(1.0, color='gray', ls='--', lw=1, label='ideal ⟨Z⟩ = +1')
        _ax.set_xlabel('Qubit')
        _ax.set_ylabel('⟨Z⟩')
        _ax.set_ylim(0, 1.05)
        _ax.set_title('Mirror expectation values (boxed + learned, pre-mitigation)')
        _ax.legend()
        plt.tight_layout()
        plt.show()
        print(f'mean ⟨Z⟩ = {_z_means.mean():+.4f}  (ideal = +1)')
    else:
        print(f'Not done yet (status={exec_job_ex3_1.status()}). Re-run cell when DONE.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Wrapping up Chapter 2:

    Congratulations! You have completed Chapter 2 of Lab 3. In this chapter we introduced all the tools needed to implement the advanced error mitigation techniques of chapter 3.

    We walked through the entire Samplomatic + noise learning workflow first for a simple 2-qubit toy model and then for the more complex 4-qubit Ising chain and finally for the 6-qubit Ising chain. For each circuit, the workflow remained the same and only the circuits changed.

    - In __Exercise 2__ you boxed the 6-qubit Ising mirror circuit and the noise-learning step characterized its layers.
    - In __Exercise 3__, you assembled the boxed circuit, the previously learned noise, and the samplex into the `QuantumProgram` the `Executor` runs.

    Along the way we inspected the per-layer noise structure: we learnt that the `ref` strings attached to every layer with an `InjectNoise` annotation are the labels that we attach the learned noise information to.

    We saw that for the Ising mirror circuit, even though the layers play similar roles in the physics of the circuit, the learned noise model in each layer differs (in particular the layers have different dominant generators). This motivates exactly why we want error mitigation to act __per layer__.

    #### What is missing — and why Chapter 3 exists:

    Importantly, the pipeline we have seen in chapter 2 measures noise and prepares it for execution but it does not remove it. So far, we have seen how twirling reshapes coherent error into a stochastic Pauli channel but does not remove it (it applies a finite number of randomization samples without ever applying the inverse noise). Also, the learned-noise dict describes the noise per layer, but again Chapter 2 never uses its inverse — under `inject_noise_strategy="no_modification"` the dict is a passthrough, which is why the Ising mirror circuit's results for $\langle Z_i\rangle$ sit below the ideal $+1$. As circuits deepen, per-layer rates compound to the point where unmitigated bias makes results untrustworthy and we need per-layer error mitigation.

    Chapter 3 introduces techniques for the next step in which we will need to change the `inject_noise_strategy`.
    - PNA (`inject_noise_strategy=uniform_modification`) absorbs the inverse of the learned channel into a _noise mitigating observable_
    - SLC (`inject_noise_strategy=individual_modification`) samples anti-noise along each observable's _lightcone_
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Chapter 3 — Qiskit add-ons for error mitigation

    Welcome to chapter 3! In this chapter, we will use the tools introduced in chapter 2 to implement advanced _per-layer_ error mitigation techniques. Let's review the story so far: Chapter 1 reviewed the mitigation techniques available as `Estimator` options (`DD`, `PT`, `TREX`, `ZNE`, `PEA` and `PEC`), these are _whole-circuit switches_ (`PEC` and `PEA` do per-layer mitigation *internally*, but the API does not surface per-layer knobs). Chapter 2 introduced Samplomatic allowing us to box circuits and localize error mitigation decisions to specific layers. Chapter 2 also showed us noise learning.

    This chapter combines those ingredients into structure-aware add-ons that go beyond whole-circuit techniques. We focus on three techniques (two Qiskit add-ons):

    - **Section 3.1: Propagated noise absorption (PNA)** — mitigates gate noise by rewriting the observable, leaving the circuit itself unchanged.
    - **Section 3.2: Probabilistic error cancellation (PEC)** — mitigates errors by sampling from inverse-noise rewrites of the circuit.
    - **Section 3.2: Shaded lightcones (SLC)** — applies PEC's idea selectively, mitigating only what can affect the observable to reduce sampling overhead.

    _PNA_ and _SLC_ are the main focus of this lab — these are the *new tools for quantum advantage* the title of the lab points to. By acting per layer, absorbing or cancelling each layer's *own* learned noise, they reach past what the Runtime `Estimator` options can do, and keep the sampling overhead low enough to stay practical as circuits grow.

    We will explore error mitigation techniques using the same 1D transverse-field Ising mirror circuit as in Chapter 2. We reuse the `construct_ising_circuit` function from Section 2.6.1 and the mirror trick but scale it up to a longer chain so the per-layer effects are larger and we can see the impact of the error mitiagtion techniques when we implement them.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3.1 Propagated noise absorption (PNA)

    This section introduces **[Propagated Noise Absorption (PNA)](https://qiskit.github.io/qiskit-addon-pna/)**, an error mitigation technique that inverts learned noise and absorbs it into the observable rather than into the circuit itself. Where traditional probabilistic error cancellation (PEC) requires the sampling of many variants of noisy circuits (as we shall see in section 3.2), PNA sidesteps that overhead and exploits the structure we have built up in Chapters 1 and 2: dressed layers, Pauli propagation through Cliffords, boxed circuits with `Twirl` and `InjectNoise` annotations, and noise learned as a sparse Pauli-Lindblad generator.

    The key insight is that when noise is Pauli (or can be twirled into Pauli form), its inverse can be **propagated forward** through the circuit using the Clifford-conjugation rules from section 1.1.3. The noise can then **absorbed into the measurement observable** to produce a _noise mitigating observable_.

    Because Pauli channels compose and propagate efficiently, PNA computes a single noise mitigating observable $\tilde{O}$ that, when measured on the noisy circuit, yields an estimate of the noise-free expectation value of the original desired observable $\langle O \rangle$.

    This section walks through the four-step PNA workflow: boxing, learning, propagating, and absorbing. We use the Ising mirror circuit from Chapter 2 as our example and scale it up to 10 qubits with 2 Trotter steps, performing the entire PNA workflow for this example.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.1.1 Set-up and scaling up to 10 qubits

    In this section, we continue working with the __1D transverse-field Ising chain__ Hamiltonian introduced in section 2.6:
    $$
    H = -J \sum_{\langle i,j \rangle} Z_i Z_j + h \sum_i X_i \;.
    $$

    We scale up to 10 qubits, keeping 2 Trotter steps and rotation angle π/8. Below, we simply set up the problem: we construct the Ising mirror circuit and transpile.
    """)
    return


@app.cell
def _(construct_ising_circuit, isa_pm, np):
    # create 10 qubit settings
    # ── Circuit ─────────────────────────────────────────────────────────
    num_qubits_pna          = 10           # chain length
    num_trotter_steps_pna   = 2            # Trotter "reps"
    rx_angle           = np.pi / 8    # transverse-field rotation per step

    # create the Ising chain circuit
    ising_pna  = construct_ising_circuit(num_qubits_pna, num_trotter_steps_pna, rx_angle)
    mirror_pna = ising_pna.compose(ising_pna.inverse())
    mirror_pna.measure_all()

    # transpile to obey ISA
    mirror_isa_pna = isa_pm.run(mirror_pna)
    layout_pna     = mirror_isa_pna.layout.final_index_layout()

    print(f"Mirror     : {num_qubits_pna}q × {num_trotter_steps_pna} Trotter steps, "
          f"rx_angle = π/{round(np.pi / rx_angle)}")
    print(f"ISA layout : physical qubits {layout_pna}")
    return layout_pna, mirror_isa_pna, num_qubits_pna, rx_angle


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.1.2 Boxing the circuit and learning the noise

    Before we can box the new Ising mirror circuit, we need to create a new boxing pass manager for PNA. Chapter 2 used a boxing pass manager with `inject_noise_strategy="no_modification"`, which fed the learned noise model into the samplex as a passthrough but never applied it to the sampled circuits. We need different strategies in Chapter 3:

    - **PNA** uses `inject_noise_strategy="uniform_modification"`: every layer's noise is modified the _same way_ at sampling time. PNA sets `noise_scales` to 0 on all `ref`'s, which leaves the sampled circuits untouched while still associating each layer with its learned model so the noise model can be propagated into the observable.
    - **SLC** uses `inject_noise_strategy="individual_modification"`: each layer (and each generator) is modified independently, so SLC can scale noise per generator along the observable's lightcone. We will see this in section 3.2.

    For more information on the choice of `inject_noise_strategy`, see the [documentation](https://qiskit.github.io/samplomatic/api/auto/samplomatic.transpiler.generate_boxing_pass_manager.html#samplomatic.transpiler.generate_boxing_pass_manager/inject_noise_strategy) for `generate_boxing_pass_manager`.

    After defining the new boxing pass manager, we find the unique layers in the circuit using `find_unique_box_instructions`. We print the number of unique layers below.
    """)
    return


@app.cell
def _(
    find_unique_box_instructions,
    generate_boxing_pass_manager,
    mirror_isa_pna,
):
    # ═══════════════════════════════════════════════════════════════════
    # PNA — boxing manager for uniform_modification + find unique layers
    # ═══════════════════════════════════════════════════════════════════
    pna_boxing_pm = generate_boxing_pass_manager(
        enable_gates=True,
        enable_measures=True,
        measure_annotations="all",
        twirling_strategy="active",
        inject_noise_targets="gates",
        inject_noise_strategy="uniform_modification",
    )

    # box the circuit for pna
    boxed_circuit_pna = pna_boxing_pm.run(mirror_isa_pna)
    # find the unique layers in the circuit
    unique_layers_pna = find_unique_box_instructions(
        boxed_circuit_pna, normalize_annotations=None, undress_boxes=True,
    )
    print(f"PNA boxed  : {len(unique_layers_pna)} unique layers")
    return boxed_circuit_pna, unique_layers_pna


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we are ready to learn the noise in the circuit. We need to this again here for the 10-qubit Ising circuit since this circuit is different to the circuits we learned the noise for previously. Noise in a quantum computer changes over time (calibration happens everyday), so cached learning results from a previous calibration window should be re-learned in general.

    First, we initialize the noise learner options:
    """)
    return


@app.cell
def _(NoiseLearnerV3, NoiseLearnerV3Options, backend):
    # ── NoiseLearnerV3 new options (used by PNA, SLC, and indirectly by PEC) ───────
    NL_NUM_RANDOMIZATIONS  = 16
    NL_SHOTS_PER_RAND      = 32
    NL_LAYER_PAIR_DEPTHS   = [1, 2, 4, 8]

    pna_nl_options = NoiseLearnerV3Options(
        num_randomizations=NL_NUM_RANDOMIZATIONS,
        shots_per_randomization=NL_SHOTS_PER_RAND,
        layer_pair_depths=NL_LAYER_PAIR_DEPTHS,
    )
    pna_learner = NoiseLearnerV3(backend, pna_nl_options)
    return (pna_learner,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    _Note:_ The following cell executes a job on quantum hardware. Ensure you are ready to do this before proceeding. After first execution, we recommend pasting the job id into the `NOISE_LEARN_JOB_ID_PNA` parameter and setting `SUBMIT_NOISE_JOB_PNA = False`. This will prevent accidentally resubmitting the job and keeps the notebook re-runnable after a kernel restart.

    _Estimated QPU execution time is 15 seconds (tested on ibm_pittsburgh)_. The usage estimate above reflects backend execution time only. Queue time, calibration, and runtime session delays may be longer.
    """)
    return


@app.cell
def _(pna_learner, service, unique_layers_pna):
    NOISE_LEARN_JOB_ID_PNA = "d9jh093jf64c739gq7ng" # paste job_id here on re-run
    SUBMIT_NOISE_JOB_PNA   = True # set True to submit a fresh learning job
    pna_learner.options.environment.job_tags = ["qgss26"]

    if NOISE_LEARN_JOB_ID_PNA is not None:
        learner_job_pna = service.job(NOISE_LEARN_JOB_ID_PNA)
        print(f"Re-using saved job: {NOISE_LEARN_JOB_ID_PNA}")
    elif SUBMIT_NOISE_JOB_PNA:
        learner_job_pna = pna_learner.run(unique_layers_pna)
        NOISE_LEARN_JOB_ID_PNA = learner_job_pna.job_id()
        print(f"Submitted: {NOISE_LEARN_JOB_ID_PNA}")
    else:
        print("Set SUBMIT_NOISE_JOB_PNA=True to submit a fresh job, "
              "or paste a saved job id into NOISE_LEARN_JOB_ID_PNA and re-run.")
    return (NOISE_LEARN_JOB_ID_PNA,)


@app.cell
def _(NOISE_LEARN_JOB_ID_PNA, service):
    learner_job_pna_1 = service.job(NOISE_LEARN_JOB_ID_PNA)
    print(f'{NOISE_LEARN_JOB_ID_PNA}  (status: {learner_job_pna_1.status()})')
    return (learner_job_pna_1,)


@app.cell
def _(learner_job_pna_1):
    if learner_job_pna_1.status() == 'DONE':
        noise_learner_result_pna = learner_job_pna_1.result()
    else:
        print(f'Not done yet (status={learner_job_pna_1.status()}). Re-run cell when DONE.')
    return (noise_learner_result_pna,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Extract the dict `refs_to_noise_models_pna` containing the learned noise in each unique layer:
    """)
    return


@app.cell
def _(noise_learner_result_pna, unique_layers_pna):
    if 'noise_learner_result_pna' in dir() and noise_learner_result_pna is not None:
        refs_to_noise_models_pna = noise_learner_result_pna.to_dict(unique_layers_pna, require_refs=False)
        print(f"refs_to_noise_models_pna has {len(refs_to_noise_models_pna)} entries")
    else:
        print("Run the noise-learning cell above and wait for it to finish first.")
    return (refs_to_noise_models_pna,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### The observable of interest

    Part of the transverse-field Ising Hamiltonian is a ZZ-interaction energy term. For our observable of interest, we consider one such term, on the middle two qubits:

    $$
    O \;=\;  Z_{4} Z_{5}, \;
    $$
    for $N=10$ qubits. This is a nearest-neighbor ZZ correlator. On the mirror circuit's ideal output $|0\rangle^{\otimes N}$, every $\langle Z_i Z_{i+1}\rangle = +1$, so the ideal expectation value is $\langle O\rangle = 1$.

    PNA rewrites the observable $O$ into an modified _noise mitigating_ observable $\tilde{O}$. This modified observable will contain additional terms with different coefficients. The idea is that the noisy expectation value of $\tilde{O}$ matches the ideal expectation of the original $O$.

    First, we construct the observable $O$ and then apply the circuits's layout to it.
    """)
    return


@app.cell
def _(SparsePauliOp, num_qubits_pna):
    # create observable for the Ising model
    # Single ZZ on the middle two qubits (1 term, ideal exp val = 1).
    mid = num_qubits_pna // 2
    observable_pna =  SparsePauliOp.from_sparse_list(
        [("ZZ", [mid - 1, mid], 1.0)], num_qubits=num_qubits_pna)

    print(observable_pna)
    return (observable_pna,)


@app.cell
def _(mirror_isa_pna, observable_pna):
    # apply layout to observable
    observable_pna_isa = observable_pna.apply_layout(mirror_isa_pna.layout)
    return (observable_pna_isa,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.1.3  Computing the noise mitigating observable $\tilde{O}$

    Now we have constructed the observable $O$, the next step in the PNA workflow is to calculate the noise mitigating observable $\tilde{O}$ using the function [`generate_noise_mitigating_observable`](https://qiskit.github.io/qiskit-addon-pna/apidocs/qiskit_addon_pna.html#qiskit_addon_pna.generate_noise_mitigating_observable) from the PNA add-on. The function takes in the boxed circuit, the observable and the learned noise dict.

    Each `InjectNoise(ref=...)` annotation knows its layer's `PauliLindbladMap` from the noise learning step. PNA propagates the inverse of those channels through the circuit and folds them into the observable. The result is a new observable $\tilde{O}$ whose noisy expectation equals the ideal expectation of the original $O$.

    A truncation step keeps only the dominant terms so $\tilde{O}$ remains measurable. The more terms an observable has the more measurements of the circuit required to estimate its expectation value. The truncation is controlled by `max_err_terms` and `max_obs_terms`.

    The boxed circuit itself is unchanged; only the observable changes.
    """)
    return


@app.cell
def _(
    boxed_circuit_pna,
    generate_noise_mitigating_observable,
    observable_pna_isa,
    refs_to_noise_models_pna,
):
    # PNA parameters
    _num_processes = 8
    _max_err_terms = 10000
    _max_obs_terms = 10000
    # generate the noise mitigating observable
    obs_tilde_isa = generate_noise_mitigating_observable(boxed_circuit_pna, observable_pna_isa, refs_to_noise_models_pna, max_err_terms=_max_err_terms, max_obs_terms=_max_obs_terms, num_processes=_num_processes, print_progress=True, search_step=8)
    return (obs_tilde_isa,)


@app.cell
def _(obs_tilde_isa):
    print(f"Number of Pauli terms in the noise mitigating observable: {len(obs_tilde_isa)}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We need to do some post-processing to build the noise mitigating observable $\tilde{O}$ in logical qubit space. This is useful so we can inspect the observable and see what terms it contains.
    """)
    return


@app.cell
def _(SparsePauliOp, layout_pna, num_qubits_pna, obs_tilde_isa):
    ### Mapping the noise mitigating observable from physical to logical qubits

    # Create an inverse layout: physical qubit index → logical qubit index
    physical_to_logical = {
        physical_q: logical_q
        for logical_q, physical_q in enumerate(layout_pna)
    }

    # Extract the noise mitigating observable in sparse (Pauli, qubits, coeff) form
    isa_pauli_terms = obs_tilde_isa.to_sparse_list()

    # Remap each Pauli term from physical qubits to logical qubits
    logical_pauli_terms = [
        (
            pauli_string,                                  # Pauli operators (e.g. "ZIX")
            [physical_to_logical[q] for q in phys_qubits], # physical → logical indices
            coefficient                                    # real-valued coefficient
        )
        for (pauli_string, phys_qubits, coefficient) in isa_pauli_terms
    ]

    # Rebuild the observable in the logical (virtual) qubit space
    obs_tilde_virtual = SparsePauliOp.from_sparse_list(
        logical_pauli_terms,
        num_qubits=num_qubits_pna
    )
    return (obs_tilde_virtual,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Below we plot the distribution of magnitudes of every term in $\tilde{O}$.
    """)
    return


@app.cell
def _(np, obs_tilde_virtual, plt):
    # sort the observable magnitudes in descending order for plotting
    obs_tilde_virtual_1 = obs_tilde_virtual[np.argsort(np.abs(obs_tilde_virtual.coeffs))][::-1]
    plt.figure(figsize=(8, 5))
    plt.plot(np.abs(obs_tilde_virtual_1.coeffs), 'o', color='tab:blue', markersize=6, alpha=0.7)
    plt.yscale('log')
    plt.xlabel('Pauli term index', fontsize=14)
    plt.ylabel('Magnitude', fontsize=14)
    plt.title('$\\tilde{O}$ coefficient magnitudes', fontsize=14)
    plt.grid(axis='both', alpha=0.3)
    plt.tight_layout()
    plt.show()
    return (obs_tilde_virtual_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can see that $\tilde{O}$ has many terms, lots of which are very low in magnitude. Let's sort by magnitude and show the first 10 terms to inspect the structure. Remember that the original observable had only 1 term (ZZ on the central two qubits).
    """)
    return


@app.cell
def _(np, obs_tilde_virtual_1):
    num_terms_to_plot = 10
    coeff_magnitudes = np.abs(obs_tilde_virtual_1.coeffs)
    _sorted_indices = np.argsort(coeff_magnitudes)
    sorted_indices_desc = _sorted_indices[::-1]
    obs_tilde_virtual_2 = obs_tilde_virtual_1[sorted_indices_desc]
    obs_tilde_virtual_2 = obs_tilde_virtual_2[:num_terms_to_plot]
    return num_terms_to_plot, obs_tilde_virtual_2


@app.cell
def _(np, obs_tilde_virtual_2, observable_pna, plt):
    def _full_pauli_string(pstr, qubits, n):
        full = ['I'] * n
        for _p, q in zip(pstr, qubits):
            full[q] = _p
        return ''.join(reversed(full))
    _sorted_idx = np.argsort(np.abs(obs_tilde_virtual_2.coeffs))[::-1][:10]
    _obs_tilde_top = obs_tilde_virtual_2[_sorted_idx]
    _target_paulis_virtual = {_full_pauli_string(_p, q, obs_tilde_virtual_2.num_qubits) for _p, q, _ in observable_pna.to_sparse_list()}
    _labels = [_full_pauli_string(_p, q, obs_tilde_virtual_2.num_qubits) for _p, q, _ in _obs_tilde_top.to_sparse_list()]
    _coeffs = np.abs(_obs_tilde_top.coeffs)
    _is_orig = np.array([l in _target_paulis_virtual for l in _labels])
    _fig, _ax = plt.subplots(figsize=(10, 4))
    _idx = np.arange(len(_labels))
    _ax.plot(_idx[_is_orig], _coeffs[_is_orig], 's', color='C3', markersize=12, label='Original ZZ term')
    _ax.plot(_idx[~_is_orig], _coeffs[~_is_orig], 'o', color='C0', markersize=10, label='PNA-added')
    _ax.set_yscale('log')
    _ax.set_xticks(_idx)
    _ax.set_xticklabels(_labels, rotation=45, ha='right', family='monospace')
    _ax.set_xlabel('Pauli term (virtual qubits)')
    _ax.set_ylabel('$|\\tilde{c}|$')
    _ax.set_title('Top 10 terms in $\\tilde{O}_{Z}$')
    _ax.legend()
    _ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You should see the original ZZ term has the largest magnitude. The additional terms are accounting for noise in the circuit and so we expect them to be much smaller in magnitude.

    Let's directly compare the magnitudes of terms in the original observable $O$ and the noise mitigating observable $\tilde{O}$.
    """)
    return


@app.cell
def _(num_terms_to_plot, observable_pna):
    # Extract Pauli strings and coefficients
    _pauli_strings = observable_pna.paulis.to_labels()
    _coeffs = observable_pna.coeffs
    _sorted_indices = sorted(range(len(_coeffs)), key=lambda i: abs(_coeffs[i]), reverse=True)
    # Sort by coefficient magnitude
    print('\n Original Observable Pauli Terms:\n')
    print(f"{'Pauli string':<{observable_pna.num_qubits + 2}}  Coefficient")
    print('-' * (observable_pna.num_qubits + 20))
    for _i in _sorted_indices[:num_terms_to_plot]:
    # Print header
    # Print terms 
        print(f'{_pauli_strings[_i]}  {_coeffs[_i].real:+.3f}')
    return


@app.cell
def _(obs_tilde_virtual_2):
    num_terms_to_plot_1 = 10
    _pauli_strings = obs_tilde_virtual_2.paulis.to_labels()
    _coeffs = obs_tilde_virtual_2.coeffs
    _sorted_indices = sorted(range(len(_coeffs)), key=lambda i: abs(_coeffs[i]), reverse=True)
    print('\n Noise mitigating Observable Pauli Terms (top 10):\n')
    print(f"{'Pauli string':<{obs_tilde_virtual_2.num_qubits + 2}}  Coefficient")
    print('-' * (obs_tilde_virtual_2.num_qubits + 20))
    for _i in _sorted_indices[:num_terms_to_plot_1]:
        print(f'{_pauli_strings[_i]}  {_coeffs[_i].real:+.3f}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The middle ZZ term had magnitude 1 in the original observable. In $\tilde{O}$ it is slightly above 1 and remains the dominant term: PNA amplified the original term and added new ones to absorb the per-layer noise. The table above shows the 10 largest terms.

    Your results will vary depending on the QPU you are using and the noise learned from the QPU. Noise drifts and calibrations happen daily. Even for the same QPU, the noise will change over time. For the most accurate results, you should always relearn your noise just before running the final job.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 4 — Mitigate the magnetization observable
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <b>Exercise 4 — Mitigate the magnetization observable</b>

    In this exercise you need to build the PNA noise mitigating observable of the **magnetization** observable for a 10-qubit Ising chain:

    $$
    O_Z = \sum_{i=0}^{N-1} Z_i, \;
    $$

    the sum of a $Z$ on each qubit. On the mirror's ideal output $|0\rangle^{\otimes N}$ every $\langle Z_i \rangle = +1$, so the ideal expectation value is $\langle O_Z \rangle = 10$ for the 10-qubit chain.

    PNA absorbs each layer's learned noise into the observable instead of the circuit. Here, you will build $\tilde{O}_Z$, the noise mitigating magnetization observable, on the 10-qubit boxed mirror, then look at the anti-noise terms PNA propagated into it.

    Build the noise mitigating observable in three steps:

    - **Target:** define `target_observable_ex4` as a `SparsePauliOp` for $O_Z = \sum_{i=0}^{9} Z_i$ on 10 qubits, using `SparsePauliOp.from_sparse_list` with one entry per qubit.
    - **Layout:** PNA matches noise layers by physical qubit index, so ISA-map the observable with `apply_layout(mirror_isa_pna.layout)` → `target_observable_ex4_isa`.
    - **Mitigate:** call `generate_noise_mitigating_observable` on the ISA observable, passing the pre-set truncation parameters from the stub as keyword arguments → `obs_tilde_ex4`.

    The grader checks the target and the noise mitigating observable.
    """)
    return


@app.cell
def _(
    SparsePauliOp,
    boxed_circuit_pna,
    generate_noise_mitigating_observable,
    mirror_isa_pna,
    num_qubits_pna,
    refs_to_noise_models_pna,
):
    #TODO: Add Your code here and set the missing values.
    _num_processes = 8
    _max_err_terms = 10000
    _max_obs_terms = 10000

    # PNA parameters (same as in section 3.1.3 main text).

    target_observable_ex4 = SparsePauliOp.from_sparse_list(
        [("Z", [i], 1.0) for i in range(num_qubits_pna)],
        num_qubits=num_qubits_pna
    )

    target_observable_ex4_isa = target_observable_ex4.apply_layout(mirror_isa_pna.layout)

    # 1. Build target_observable_ex4 as a SparsePauliOp with 10 Z terms one
    #    on each qubit
    # 2. Apply mirrored_isa_pna.layout to the target so PNA receives an ISA-mapped observable.
    # 3. Call generate_noise_mitigating_observable(boxed_circuit_pna, target_observable_ex4_isa,
    #    refs_to_noise_models_pna, max_err_terms=..., max_obs_terms=..., num_processes=...).
    obs_tilde_ex4 = generate_noise_mitigating_observable(
        boxed_circuit_pna,
        target_observable_ex4_isa,
        refs_to_noise_models_pna,
        max_err_terms=_max_err_terms,
        max_obs_terms=_max_obs_terms,
        num_processes=_num_processes
    )
    return obs_tilde_ex4, target_observable_ex4, target_observable_ex4_isa


@app.cell
def _(
    grade_lab3_ex4,
    obs_tilde_ex4,
    target_observable_ex4,
    target_observable_ex4_isa,
):
    # grade your answer
    grade_lab3_ex4(
        target_observable_ex4,
        target_observable_ex4_isa,
        obs_tilde_ex4
    )
    return


@app.cell
def _(check_progress):
    # check your progress across all the labs
    check_progress()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ####  What does $\tilde{O}_{Z}$ look like?

    The plot below shows the 20 largest terms of $\tilde{O}_{Z}$ with their Pauli strings on virtual qubits. You should see the original 10 terms (red squares) sit at the top, slightly amplified. The blue circles are the anti-noise corrections that PNA propagated from the learned noise model.
    """)
    return


@app.cell
def _(
    SparsePauliOp,
    layout_pna,
    np,
    num_qubits_pna,
    obs_tilde_ex4,
    plt,
    target_observable_ex4,
):
    # Map obs_tilde back to virtual qubits for readable Pauli labels.
    _p_2_v = {_p: v for v, _p in enumerate(layout_pna)}
    obs_tilde_virtual_ex4 = SparsePauliOp.from_sparse_list([(_p, [_p_2_v[q] for q in qs], c) for _p, qs, c in obs_tilde_ex4.to_sparse_list()], num_qubits=num_qubits_pna)
    _sorted_idx = np.argsort(np.abs(obs_tilde_virtual_ex4.coeffs))[::-1][:20]
    _obs_tilde_top = obs_tilde_virtual_ex4[_sorted_idx]

    def _full_pauli_string(pstr, qubits, n):
    # Sort by |coefficient| descending and keep top 20.
        full = ['I'] * n
        for _p, q in zip(pstr, qubits):
            full[q] = _p
        return ''.join(reversed(full))
    _target_paulis_virtual = {_full_pauli_string(_p, q, num_qubits_pna) for _p, q, _ in target_observable_ex4.to_sparse_list()}
    _labels = [_full_pauli_string(_p, q, num_qubits_pna) for _p, q, _ in _obs_tilde_top.to_sparse_list()]
    _coeffs = np.abs(_obs_tilde_top.coeffs)
    _is_orig = np.array([l in _target_paulis_virtual for l in _labels])  # qubit 0 leftmost
    _fig, _ax = plt.subplots(figsize=(10, 4))
    _idx = np.arange(len(_labels))
    # Identify which top-20 terms are originals vs PNA-added.
    _ax.plot(_idx[_is_orig], _coeffs[_is_orig], 's', color='C3', markersize=12, label='Original observable terms')
    _ax.plot(_idx[~_is_orig], _coeffs[~_is_orig], 'o', color='C0', markersize=10, label='PNA-added')
    _ax.set_yscale('log')
    _ax.set_xticks(_idx)
    _ax.set_xticklabels(_labels, rotation=45, ha='right', family='monospace')
    _ax.set_xlabel('Pauli term (virtual qubits)')
    _ax.set_ylabel('$|\\tilde{c}|$')
    _ax.set_title('Top 20 terms in $\\tilde{O}$')
    _ax.legend()
    # Plot.
    _ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()
    return (obs_tilde_virtual_ex4,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.1.4  Running on hardware

    With $\tilde{O}$ ready, we build the Executor program and submit.

    This section requires:
    - `boxed_circuit_pna` (with uniform_modification)
    - `obs_tilde_ex4` from Exercise 4 (for the magnetization observable)
    - `refs_to_noise_models_pna` from the noise learner for 10 qubits

    In section 3.1.5, we will compare the expectation value results for three cases: the unmitigated observable, the noise mitigating observable from the PNA workflow, and the noise mitigation observable from PNA + TREX.
    """)
    return


@app.cell
def _(boxed_circuit_pna, samplomatic):
    # Build template circuit and samplex for use with the "Executor"
    template_circuit_pna, samplex_pna = samplomatic.build(boxed_circuit_pna)
    return samplex_pna, template_circuit_pna


@app.cell
def _(
    ChangeBasis,
    boxed_circuit_pna,
    get_annotation,
    get_measurement_bases,
    layout_pna,
    np,
    num_qubits_pna,
    obs_tilde_virtual_ex4,
):
    num_to_measure = 10
    meas_box = boxed_circuit_pna.data[-1]
    canonical_qubits = [_i for _i, q in enumerate(boxed_circuit_pna.qubits) if q in meas_box.qubits]
    canonical_to_physical = dict(enumerate(canonical_qubits))
    physical_to_virtual = {_p: v for v, _p in enumerate(layout_pna)}
    canonical_to_virtual = {c: physical_to_virtual[_p] for c, _p in canonical_to_physical.items()}
    _change_basis_ann = get_annotation(meas_box.operation, ChangeBasis)
    if _change_basis_ann is None:
        raise RuntimeError("No ChangeBasis annotation on the measurement box. The boxing pass manager must be built with measure_annotations='all'.")
    _basis_ref = _change_basis_ann.ref
    print(f'ChangeBasis ref: {_basis_ref!r}')
    obs_tilde_virtual_ex4_1 = obs_tilde_virtual_ex4[np.argsort(np.abs(obs_tilde_virtual_ex4.coeffs))[::-1]][:num_to_measure]
    meas_bases, bases_reverser = get_measurement_bases(obs_tilde_virtual_ex4_1)
    meas_bases_canonical = [np.array([base[canonical_to_virtual[c]] for c in sorted(canonical_to_virtual)], dtype=np.uint8) for base in meas_bases]
    all_z_canonical = np.ones(num_qubits_pna, dtype=np.uint8)
    if any((np.array_equal(b, all_z_canonical) for b in meas_bases_canonical)):
        all_z_idx = next((_i for _i, b in enumerate(meas_bases_canonical) if np.array_equal(b, all_z_canonical)))
        print(f'all-Z basis already present at index {all_z_idx}')
    else:
        meas_bases_canonical.append(all_z_canonical)
        all_z_idx = len(meas_bases_canonical) - 1
        print(f'Appended all-Z basis at index {all_z_idx}')

    def _decode(b):
        return ''.join(('IZXY'[v] for v in b))
    print(f'\nMeasurement bases (canonical order, qubit 0 leftmost):')
    for _i, b in enumerate(meas_bases_canonical):
        note = '  ← unmitigated baseline' if _i == all_z_idx else ''
        print(f'  [{_i}] {_decode(b)}{note}')
    return (
        all_z_idx,
        bases_reverser,
        meas_bases_canonical,
        meas_box,
        num_to_measure,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Aside: term count vs. measurement-basis count

    The truncation above keeps a fixed *number* of terms, but the quantity that drives shot cost is the number of distinct **measurement bases**. `get_measurement_bases` groups qubit-wise commuting Pauli terms so they share a basis and therefore share shots. A PNA-added term that is diagonal in a basis we already measure can be kept at no extra *basis* cost.

    The cell below rebuilds the full $\tilde{O}_Z$ and counts how many terms just past the `num_to_measure` cut fall into the already-required basis set. Keeping those is "free" in measurement-basis terms — though not entirely free statistically: every extra term still contributes its own coefficient and shot noise to the summed estimate of $\langle\tilde{O}_Z\rangle$. The saving is that no new basis, and hence no new shot allocation, is required.
    """)
    return


@app.cell
def _(
    SparsePauliOp,
    get_measurement_bases,
    layout_pna,
    np,
    num_qubits_pna,
    num_to_measure,
    obs_tilde_ex4,
):
    _p_2_v = {_p: v for v, _p in enumerate(layout_pna)}
    obs_tilde_virtual_full = SparsePauliOp.from_sparse_list([(_p, [_p_2_v[q] for q in qs], c) for _p, qs, c in obs_tilde_ex4.to_sparse_list()], num_qubits=num_qubits_pna)
    obs_full_sorted = obs_tilde_virtual_full[np.argsort(np.abs(obs_tilde_virtual_full.coeffs))[::-1]]
    bases_cut, _ = get_measurement_bases(obs_full_sorted[:num_to_measure])
    n_bases_cut = len(bases_cut)
    print(f'Truncation : {num_to_measure} terms  ->  {n_bases_cut} measurement bases')
    free = 0
    for k in range(num_to_measure + 1, len(obs_full_sorted) + 1):
        bases_k, _ = get_measurement_bases(obs_full_sorted[:k])
        if len(bases_k) == n_bases_cut:
            free = free + 1
        else:
            break
    if free:
        print(f'Past cut   : {free} further term(s) fit the existing {n_bases_cut} bases -- keeping {num_to_measure + free} terms costs no extra basis.')
    else:
        print('Past cut   : the next term needs a new basis -- no free terms here.')
    print('(Free in *basis* cost; each extra term still adds its own shot noise.)')
    return


@app.cell
def _(
    ChangeBasis,
    get_annotation,
    meas_bases_canonical,
    meas_box,
    np,
    refs_to_noise_models_pna,
):
    shots_per_randomization_exec = 64
    num_randomizations_exec = 1024
    samplex_inputs_pna = {f'noise_scales.{_ref}': 0.0 for _ref in refs_to_noise_models_pna}
    samplex_inputs_pna = samplex_inputs_pna | {'pauli_lindblad_maps': refs_to_noise_models_pna}
    bases_broadcastable = np.expand_dims(np.array(meas_bases_canonical), axis=1)
    _change_basis_ann = get_annotation(meas_box.operation, ChangeBasis)
    _basis_ref = _change_basis_ann.ref
    samplex_inputs_pna = samplex_inputs_pna | {'basis_changes': {_basis_ref: bases_broadcastable}}
    return (
        num_randomizations_exec,
        samplex_inputs_pna,
        shots_per_randomization_exec,
    )


@app.cell
def _(
    QuantumProgram,
    num_randomizations_exec,
    samplex_inputs_pna,
    samplex_pna,
    shots_per_randomization_exec,
    template_circuit_pna,
):
    # Convert samplex_inputs into a dict to pass to QuantumProgram.
    samplex_arguments_pna = samplex_pna.inputs().make_broadcastable().bind(**samplex_inputs_pna)
    program_1 = QuantumProgram(shots=shots_per_randomization_exec)
    # Instantiate the QuantumProgram with the specified parameters.
    program_1.append_samplex_item(circuit=template_circuit_pna, samplex=samplex_pna, samplex_arguments=samplex_arguments_pna, shape=(num_randomizations_exec,))
    return (program_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Run the Executor job

    _Note:_ The following cell executes a job on quantum hardware. Ensure you are ready to do this before proceeding.After first execution, we recommend pasting the job id into the `EXECUTOR_JOB_ID_PNA` parameter and setting  `SUBMIT_EXECUTOR_JOB_PNA = False`. This will prevent accidentally resubmitting the job and keeps the notebook re-runnable after a kernel restart.

    _Estimated QPU execution time is 30 seconds (tested on ibm_fez)._ The usage estimate reflects backend execution time only. Queue time, calibration, and runtime session delays may be longer.
    """)
    return


@app.cell
def _(Executor, backend, program_1, service):
    _executor = Executor(backend)
    EXECUTOR_JOB_ID_PNA = "d9jh493jf64c739gqdl0" 
    SUBMIT_EXECUTOR_JOB_PNA = False 
    _executor.options.environment.job_tags = ['qgss26']
    if EXECUTOR_JOB_ID_PNA is not None:
        job_exec_pna = service.job(EXECUTOR_JOB_ID_PNA)
        print(f'Re-using saved job: {EXECUTOR_JOB_ID_PNA}')
    elif SUBMIT_EXECUTOR_JOB_PNA:
        job_exec_pna = _executor.run(program_1)
        EXECUTOR_JOB_ID_PNA = job_exec_pna.job_id()
        print(f'Submitted: {EXECUTOR_JOB_ID_PNA}')
    else:
        print('Set SUBMIT_EXECUTOR_JOB_PNA=True to submit a fresh job, or paste a saved Executor job id into EXECUTOR_JOB_ID_PNA and re-run.')
    return EXECUTOR_JOB_ID_PNA, job_exec_pna


@app.cell
def _(EXECUTOR_JOB_ID_PNA, job_exec_pna):
    # Verify the job type and status
    if EXECUTOR_JOB_ID_PNA is not None:
        print(f"Program id  : {job_exec_pna.job_id()}")
        print(f"Status      : {job_exec_pna.status()}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Extract the job results:
    """)
    return


@app.cell
def _(job_exec_pna):
    if job_exec_pna.status() == "DONE":
        exec_results_pna = job_exec_pna.result()
    else:
        print(f"Not done yet (status={job_exec_pna.status()}). Re-run cell when DONE.")
    return (exec_results_pna,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Adding the TREX error mitigation technique

    In sections 1.1.1 and 1.1.2, we introduced [Twirled readout error extinction (TREX)](https://journals.aps.org/pra/abstract/10.1103/PhysRevA.105.032620) as an error mitigation technique that can be switched on easily with the `Estimator` primitive. TREX mitigates read-out errors from measurements by randomly inserting an $X$ gate before a measurement and flipping the outcome classically. This diagonalizes the readout error matrix, allowing the read-out error to be mitigated.

    Here, in the PNA workflow, we can implement TREX easily using the function `trex_factors` from the [Qiskit add-ons utils library](https://github.com/Qiskit/qiskit-addon-utils).
    """)
    return


@app.cell
def _(bases_reverser, noise_learner_result_pna, trex_factors):
    # Computing the TREX factors
    _measurement_noise_map = noise_learner_result_pna[2].to_pauli_lindblad_map()
    _trex_rescale_factors = trex_factors(_measurement_noise_map, bases_reverser)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.1.5  Analyzing results

    In this section, we compare three estimates of the magnetization expectation: unmitigated, PNA-only, and PNA + TREX. The ideal value of the expectation value on the mirror`s output state $|0\rangle^{\otimes N}$ equals $N=10$.

    We use the function `executor_expectation_values` from the Qiskit add-on utils library to calculate the expectation value in all three cases.

    Let`s begin with the expectation value that is error mitigated with PNA alone.
    """)
    return


@app.cell
def _(bases_reverser, exec_results_pna, executor_expectation_values):
    # Expectation value with PNA only.
    # `bases_reverser` was constructed from `obs_tilde_virtual_ex4`, so it pairs
    # each measurement basis to the (post-PNA) Pauli terms diagonal in that basis.
    #
    # The data axis-0 length is len(meas_bases_canonical), which may be one larger
    # than len(bases_reverser) — we appended an all-Z basis for the unmitigated
    # baseline. Slice the data to the original PNA bases before passing in.
    _n_pna_bases = len(bases_reverser)
    results_pna = executor_expectation_values(exec_results_pna[0]['meas'][:_n_pna_bases], bases_reverser, meas_basis_axis=0, avg_axis=1, measurement_flips=exec_results_pna[0]['measurement_flips.meas'][:_n_pna_bases], pauli_signs=None, rescale_factors=None)
    exp_val_pna = results_pna[0][0]
    std_pna = results_pna[0][1]
    print(f'PNA only    : <O_Z> = {exp_val_pna:+.4f}  std = {std_pna:.4e}')  # noise_scales=0 ⇒ no PEC ⇒ no Pauli signs
    return exp_val_pna, std_pna


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Next, we calculate the noisy unmitigated expectation value:
    """)
    return


@app.cell
def _(
    Pauli,
    all_z_idx,
    exec_results_pna,
    executor_expectation_values,
    num_qubits_pna,
    target_observable_ex4,
):
    # ─── Unmitigated expectation value ───
    # We added the all-Z basis to meas_bases_canonical above (index `all_z_idx`),
    # so the executor measured it as part of the same job. Slice that subset of
    # the data and pair it with the original observable O_Z.

    meas_z  = exec_results_pna[0]["meas"][all_z_idx]
    flips_z = exec_results_pna[0]["measurement_flips.meas"][all_z_idx]

    bases_reverser_unmit = {Pauli("Z" * num_qubits_pna): [target_observable_ex4]}

    res_unmit = executor_expectation_values(
        meas_z,
        bases_reverser_unmit,
        meas_basis_axis=None,   # already sliced — no basis axis remaining
        avg_axis=0,              # average over randomizations (now axis 0)
        measurement_flips=flips_z,
        pauli_signs=None,        # noise_scales=0 ⇒ no PEC ⇒ no Pauli signs
        rescale_factors=None,
    )
    exp_val_unmit, std_unmit = res_unmit[0][0], res_unmit[0][1]
    print(f"Unmitigated : <O_Z> = {exp_val_unmit:+.4f}  std = {std_unmit:.4e}")
    return exp_val_unmit, std_unmit


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Finally, we calculate the expectation value with both error mitigation techniques PNA and TREX:
    """)
    return


@app.cell
def _(
    bases_reverser,
    exec_results_pna,
    executor_expectation_values,
    noise_learner_result_pna,
    trex_factors,
):
    # ─── PNA + TREX ───
    # TREX rescales the data per-basis to absorb the readout (measurement) noise
    # learned by NoiseLearnerV3's measurement-layer model. As above, slice the
    # data to the original PNA bases (skipping the appended all-Z basis used only
    # for the unmitigated baseline).
    _measurement_noise_map = noise_learner_result_pna[2].to_pauli_lindblad_map()
    _trex_rescale_factors = trex_factors(_measurement_noise_map, bases_reverser)
    _n_pna_bases = len(bases_reverser)
    results_pna_trex = executor_expectation_values(exec_results_pna[0]['meas'][:_n_pna_bases], bases_reverser, meas_basis_axis=0, avg_axis=1, measurement_flips=exec_results_pna[0]['measurement_flips.meas'][:_n_pna_bases], pauli_signs=None, rescale_factors=_trex_rescale_factors)
    exp_val_pna_trex = results_pna_trex[0][0]
    std_pna_trex = results_pna_trex[0][1]
    print(f'PNA + TREX  : <O_Z> = {exp_val_pna_trex:+.4f}  std = {std_pna_trex:.4e}')  # noise_scales=0 ⇒ no PEC ⇒ no Pauli signs
    return exp_val_pna_trex, std_pna_trex


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Plot the results:
    """)
    return


@app.cell
def _(
    exp_val_pna,
    exp_val_pna_trex,
    exp_val_unmit,
    np,
    num_qubits_pna,
    plt,
    std_pna,
    std_pna_trex,
    std_unmit,
):
    # Compare: Unmitigated, PNA, PNA+TREX vs. ideal (= N = 10 for the 10q chain).
    experiments = ['Unmitigated', 'PNA', 'PNA+TREX']
    _colors = ['tab:gray', 'tab:blue', 'tab:orange']
    markers = ['o', 's', '^']
    evs = [exp_val_unmit, exp_val_pna, exp_val_pna_trex]
    _errs = [std_unmit, std_pna, std_pna_trex]
    _x = np.arange(len(experiments))
    plt.figure(figsize=(6, 4))
    for _xi, yi, ei, label, color, marker in zip(_x, evs, _errs, experiments, _colors, markers):
        plt.errorbar(_xi, yi, yerr=ei, color=color, marker=marker, markersize=12, linestyle='none', capsize=5, label=label, zorder=3)
    plt.axhline(y=num_qubits_pna, color='green', linestyle='--', linewidth=2, label=f'Ideal = N = {num_qubits_pna}', zorder=2)
    plt.xticks(_x, experiments)
    plt.ylabel('Expectation value', fontsize=14)
    plt.title('10 qubit Ising chain, 2 Trotter steps, $O_Z$ obs', fontsize=14)
    plt.legend(loc='lower right')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In the plot above, You should see a clear difference in results for the three implementations. The unmitigated expectation value should be the worst (i.e. the furthest from the ideal value of 10). Implementing PNA by measuring the expectation value of the noise mitigating observable $\tilde{O}$ instead of the unmitigated observable $O$ should improve the result. Finally, by further adding TREX to mitigate read-out errors as well as PNA, we should see the result improve even further.

    This concludes section 3.1 which covered propagated noise absorption (PNA). In section 3.2, we turn to PEC and SLC.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3.2 Probabilistic Error Cancellation (PEC) and Shaded lightcones (SLC)

    ### 3.2.1 Probabilistic Error Cancellation (PEC) Overview
    [Probabilistic error cancellation (PEC)](https://quantum.cloud.ibm.com/docs/en/guides/error-mitigation-and-suppression-techniques#probabilistic-error-cancellation-pec) acts at the circuit level. It uses the learned Pauli-noise model from Chapter 2 to construct an inverse noise map (anti-noise), then samples from that inverse with per-shot signs from the quasi-probability weights. After a final rescaling by $\gamma$, the averaged expectation value is unbiased for the ideal circuit when the noise model is exact.

    Conceptually, PEC is the circuit-side analogue of PNA:
    - **PNA** keeps the circuit fixed and rewrites the observable.
    - **PEC** keeps the observable fixed and probabilistically rewrites the circuit.

    PEC is general: with an accurate noise model, it mitigates errors without requiring the observable to have any special structure. The cost of this generality is an increase in estimator variance. The number of shots grows with circuit depth and total noise, summarized by the overhead factor $\gamma^2$. Quantitatively, $$\gamma = \exp\!\big(2\sum_{l,\sigma}\lambda_{l,\sigma}\big),$$ where $\lambda_{l,\sigma}$ is the learned rate of generator $\sigma$ at layer $l$ in the circuit. The sampling cost grows as $\gamma^2$.

    You saw in section 1.1.2 that the Runtime `Estimator` exposes a one-flag PEC option (`resilience.pec_mitigation = True`). The switch is convenient and *internally* uses per-layer noise models, but it exposes no per-layer or per-generator knobs to you and the sampling overhead $\gamma^2$ can blow up exponentially with depth because every learned generator is cancelled.

    In this section, we will focus on using the **Shaded lightcones** (SLC) add-on to bring $\gamma^2$ down to something workable on utility-scale circuits. You will see in the following sections how SLC works to reduce the sampling overhead compared to full PEC. You will compare the sampling overhead for three different observables when using full PEC versus the SLC add-on.

    ### 3.2.2 Shaded Lightcones (SLC) Overview

    [Shaded lightcones (SLC)](https://qiskit.github.io/qiskit-addon-slc/) is an evolution of PEC. Rather than cancelling _all_ noise in the circuit, it bounds how each noise generator in the circuit affects the observable of interest. It scales down or skips generators with small bounded impact, reducing PEC's sampling overhead $\gamma^2$ at the same residual bias.

    The intuition is causal: an observable measured at the end of the circuit can only be affected by noise _within_ its backward lightcone, the set of locations whose perturbations can propagate to the measurement. Errors outside of the lightcone cannot affect the measured outcome and can therefore be excluded from the error cancellation procedure. SLC goes beyond a standard binary lightcone. It assigns each noise generator a bound on how strongly it can shift the observable (rather than a binary in/out cone). See [Lightcone Shading for Classically Accelerated Quantum Error Mitigation](https://arxiv.org/abs/2409.04401) for the underlying method.

    The workflow for SLC is:

    1. Compute **forward bounds**: this defines how each noise generator, if present, would propagate forward to affect the final observable.

    2. Compute **backward bounds**: this defines how the observable, evolved backward, picks up contributions from each noise location.

    3. **Merge**: We merge the forward and backward bounds with a learned noise model to get a per-error-generator relevance score.

    4. Use those scores via the function `compute_local_scales` to pick which errors are worth mitigating, trading a controlled bias for a smaller $\gamma^2$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### SLC add-on imports:
    """)
    return


@app.cell
def _():
    # All SLC add-on imports were already loaded at the top of the notebook in Setup & Imports

    # Quick sanity check that we have all the necessary imports:
    required = [
        "compute_backward_bounds", "compute_forward_bounds", "compute_local_scales",
        "merge_bounds", "generate_noise_model_paulis", "map_modifier_ref_to_ref",
        "draw_shaded_lightcone",
    ]
    missing = [name for name in required if name not in globals()]
    if missing:
        raise ImportError(
            f"Missing SLC names: {missing}. Re-run the master imports cell at the "
            f"top of the notebook."
        )
    print("SLC imports OK.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.2.3 Set up and local observables

    To see SLC's effect, we want to look at an example circuit that is deep enough to observe a lightcone. To this end, we continue with the Ising mirror circuit example and increase the Trotter step count to 10. More steps means a deeper circuit and therefore a deeper lightcone.

    - `num_qubits_pna` $= 10$
    - Increase the number of Trotter steps to 10 (`num_trotter_steps_slc` $= 10$)
    - Keep `rx_angle` = $\pi / 8$

    _Note:_ SLC requires a different noise-injection strategy to the one we used in section 3.1 for PNA. PNA's `uniform_modification` exposes one global `noise_scales` slot, while SLC needs *per-generator* control to scale each Pauli generator along the observable's lightcone. SLC's `inject_noise_strategy="individual_modification"` exposes a separate `noise_scales.<ref>` slot for each `InjectNoise` annotation.
    """)
    return


@app.cell
def _(generate_boxing_pass_manager):
    # new boxing pass manager for SLC with individual modification
    slc_boxing_pm = generate_boxing_pass_manager(
        enable_gates=True,
        enable_measures=True,
        measure_annotations="all",
        twirling_strategy="active",
        inject_noise_targets="gates",
        inject_noise_strategy="individual_modification",
    )
    return (slc_boxing_pm,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### The observable of interest

    The observable we consider in this section is the local observable $O = Z_4$, i.e. a $Z$ on qubit 4 in the 10-qubit Ising chain. This observable is _local_ because it only acts on 1 of the 10 qubits.
    """)
    return


@app.cell
def _(SparsePauliOp, get_measurement_bases, num_qubits_pna):
    # Local observable: Z on central qubit and identity elsewhere.
    target_obs_local: list[tuple[str, list[int], float]] = [("Z", [4], 1.0)]

    # Build the observable.
    observable_local = SparsePauliOp.from_sparse_list(target_obs_local, num_qubits=num_qubits_pna)
    print(observable_local)

    # Build the measurement bases. 
    bases_virt, reverser_virt = get_measurement_bases(observable_local)
    return (observable_local,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Why is SLC well-suited to local observables?

    The SLC method is particularly well-suited to local observables because it exploits the causal structure of quantum circuits. Since local observables only act on a small subset of qubits, SLC can efficiently identify and focus on the relevant lightcone, i.e. the subset of gates that causally affect the observable's expectation value. Errors outside this lightcone can be safely ignored, dramatically reducing computational overhead. This targeted approach makes SLC more efficient for local observables compared to methods that must track all errors.

    In contrast, if we consider an observable acting on all 10 qubits, the corresponding lightcone will span more of the circuit. As a result, SLC would need to track errors in more gates in the circuit, meaning SLC might not provide much of a sampling overhead reduction compared to PEC alone.

    In Exercise 5, you will consider 3 different observables with different degrees of locality. You will see firsthand how the locality of the observable affects the sampling overhead for SLC.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now that we have defined the local observable, we need to set up the problem following the steps we have used many times now throughout this lab:

    1. Create the Ising circuit (now for 10 Trotter steps)
    2. Mirror the circuit and measure all qubits at the end
    3. Transpile the mirrored circuit to obey the backend ISA
    4. Map the observable to ISA layout
    5. Box the circuit and find the unique layers in the circuit

    We implement all 5 of these steps in the cell below.
    """)
    return


@app.cell
def _(
    construct_ising_circuit,
    find_unique_box_instructions,
    isa_pm,
    num_qubits_pna,
    observable_local,
    rx_angle,
    slc_boxing_pm,
):
    num_trotter_steps_slc = 10 # increase to 10 to see the light cone

    # Build the mirrored Ising circuit.
    ising_slc = construct_ising_circuit(num_qubits_pna, num_trotter_steps_slc, rx_angle)
    mirror_slc = ising_slc.compose(ising_slc.inverse())
    mirror_slc.measure_all()

    # Transpile to the backend ISA and capture the layout.
    mirror_isa_slc = isa_pm.run(mirror_slc)

    # Map observable to ISA layout 
    observable_local_isa = observable_local.apply_layout(mirror_isa_slc.layout, num_qubits=mirror_isa_slc.num_qubits)
    layout_slc = mirror_isa_slc.layout.final_index_layout()
    wire_order_slc = layout_slc + [q for q in range(mirror_isa_slc.num_qubits) if q not in layout_slc]

    # Box for SLC (uses `individual_modification` so we can scale per-error-term later).
    boxed_circuit_slc = slc_boxing_pm.run(mirror_isa_slc)
    unique_layer_slc = find_unique_box_instructions(
        boxed_circuit_slc, normalize_annotations=None, undress_boxes=True
    )
    return (
        boxed_circuit_slc,
        observable_local_isa,
        unique_layer_slc,
        wire_order_slc,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.2.4 Predict the to-be-learned noise-model Paulis

    We use the function `generate_noise_model_paulis` from the [Qiskit SLC add-on](https://qiskit.github.io/qiskit-addon-slc/) to construct a Pauli-level noise description of the circuit:

    - This step is performed _without_ knowledge of any noise learning.
    - The function scans each boxed layer of the circuit.
    - It generates all relevant __weight‑one__ and __weight‑two__ Pauli noise terms.
    - Pauli terms are restricted by the circuit’s qubit connectivity (only terms supported on active qubits and edges are kept)
    - The resulting Pauli set defines the possible noise support, independent of noise strength.
    - These Pauli terms are used to compute __forward and backward noise bounds__, which define the shaded lightcones.
    - Later, noise learning will be used to assign __layer‑specific Pauli‑Lindblad coefficients__ to this fixed Pauli basis.

    Ordering: SLC first determines where noise can matter from circuit structure and observable locality; noise learning later determines how much it matters.
    """)
    return


@app.cell
def _(
    backend,
    boxed_circuit_slc,
    generate_noise_model_paulis,
    unique_layer_slc,
):
    noise_model_paulis = generate_noise_model_paulis(unique_layer_slc, backend.coupling_map, boxed_circuit_slc)
    noise_model_rates = {_ref: None for _ref in noise_model_paulis}
    return (noise_model_paulis,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.2.5 Compute forward and backward bounds

    We compute forward and backward bounds to determine which parts of the circuit can influence the observable. Adjusting the settings changes the shape and color of the lightcone, showing how different circuit regions affect the final measurement. This analysis runs in simulation before any noise learning, so it uses no QPU time.

    The bounds are computed using the `compute_forward_bounds` and `compute_backward_bounds` functions. These functions take in the boxed circuit and the noise model Pauli set. The `compute_forward_bounds` function also takes in the observable mapped to the ISA layout.

    We define some additional parameters for the SLC bounds calculation:
    - `slc_atol` - Absolute tolerance for truncating small Pauli terms during evolution. Terms with coefficients below this threshold are discarded to manage computational complexity.
    - `slc_eigval_max_qubits` - Maximum number of qubits of a commutator for which the eigenvalue will still be attempted to be computed. When this value is exceeded, the bound is approximated via a simpler and more loose triangle inequality.
    - `slc_evolution_max_terms` - the maximum number of Pauli terms to retain during time evolution. Limits the size of the evolved operator to prevent exponential growth in complexity.
    - `slc_num_processes` - the number of parallel processes to use. Enables parallel computation to speed up forward/backward bound calculations.
    - `slc_timeout` - Maximum time (in seconds) allowed for each bound computation. Prevents individual calculations from running indefinitely.

    For more information on these parameter choices, see the documentation for the [`compute_forward_bounds`](https://qiskit.github.io/qiskit-addon-slc/apidocs/qiskit_addon_slc.bounds.html#qiskit_addon_slc.bounds.compute_forward_bounds) and [`compute_backward_bounds`](https://qiskit.github.io/qiskit-addon-slc/apidocs/qiskit_addon_slc.bounds.html#qiskit_addon_slc.bounds.compute_backward_bounds) functions.
    """)
    return


@app.cell
def _():
    slc_atol = 1e-8
    slc_eigval_max_qubits = 18
    slc_evolution_max_terms = 1000
    slc_num_processes = 8
    slc_timeout = 300
    return (
        slc_atol,
        slc_eigval_max_qubits,
        slc_evolution_max_terms,
        slc_num_processes,
        slc_timeout,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    _Note_: The following cell will take approximately 45 seconds when run locally on your computer. If you are using a cloud service such as `qBraid`, this could take up to 5 minutes. If needed, adjust `slc_timeout` above to a longer time.
    """)
    return


@app.cell
def _(
    boxed_circuit_slc,
    compute_backward_bounds,
    compute_forward_bounds,
    noise_model_paulis,
    observable_local_isa,
    slc_atol,
    slc_eigval_max_qubits,
    slc_evolution_max_terms,
    slc_num_processes,
    slc_timeout,
):
    forward_bounds = compute_forward_bounds(
        boxed_circuit_slc,
        noise_model_paulis,
        observable_local_isa,
        evolution_max_terms=slc_evolution_max_terms,
        eigval_max_qubits=slc_eigval_max_qubits,
        atol=slc_atol,
        num_processes=slc_num_processes,
        timeout=slc_timeout,
    )

    backward_bounds = compute_backward_bounds(
        boxed_circuit_slc,
        noise_model_paulis,
        evolution_max_terms=slc_evolution_max_terms,
        num_processes=slc_num_processes,
        timeout=slc_timeout,
    )
    return backward_bounds, forward_bounds


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can now plot the forward and backward lightcones:
    """)
    return


@app.cell
def _(
    backward_bounds,
    boxed_circuit_slc,
    display,
    draw_shaded_lightcone,
    forward_bounds,
    noise_model_paulis,
    wire_order_slc,
):
    print('forward bounds:')
    for _p in 'XYZ':
        display(draw_shaded_lightcone(boxed_circuit_slc, forward_bounds, noise_model_paulis, pauli_filter=_p, scale=0.15, fold=-1, idle_wires=False, measure_arrows=False))
    print('backward bounds:')
    for _p in 'XYZ':
        display(draw_shaded_lightcone(boxed_circuit_slc, backward_bounds, noise_model_paulis, pauli_filter=_p, scale=0.15, fold=-1, idle_wires=False, wire_order=wire_order_slc, measure_arrows=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Yellow regions indicate higher sensitivity to noise (any errors here will have a stronger impact on the observable), while darker regions show lower sensitivity (errors here matter less). Importantly, these figures do not show where the actual noise is as we have not learned it yet. Instead, they show how strongly noise at a given location would affect the observable in question, if it were present.

    In the next section, you will scale this example up to 15 qubits. We will learn the noise on the hardware and combine it with the shaded lightcones to mitigate errors at low sampling overhead.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 5 — Investigate the locality of 3 observables for 15 qubits

    We have seen the shaded lightcones (forward and backward bounds) for the Ising Hamiltonian on 10 qubits, 10 Trotter steps, with observable $Z_4$. This exercise scales the example to 15 qubits but reduces the number of Trotter steps to 3.

    SLC's advantage over PEC comes from a reduced sampling overhead. This is particularly effective when the observable is _local_. The reduction in sampling overhead depends on the observable's locality and complexity. In this exercise you construct three observables of different locality and calculate the corresponding forward and backward bounds.

    You will set up a 15-qubit mirrored Ising circuit with 3 Trotter steps and construct three observables:
    - `obs_Z7` - Z on qubit 7
    - `obs_X3_Z11` - X on qubit 3, Z on qubit 11
    - `obs_7_Zs` - Z on central 7 qubits

    For each of these observables, you need to calculate the forward and backward bounds.

    <div class="alert alert-block alert-success">

    <b>Exercise 5.</b> Investigate the locality of 3 observables for 15 qubits

    - **Create a 15-qubit Ising chain mirrored circuit with 3 Trotter steps.**
        - Use the function `construct_ising_circuit`
    - **Create the 3 required observables as `SparsePauliOp` objects**:
        - `obs_Z7` - Z on qubit 7
        - `obs_X3_Z11` - X on qubit 3, Z on qubit 11
        - `obs_7_Zs` - Z's on central 7 qubits in Ising chain
        - Each observable should be a single-term observable with a coefficient of 1.
    - **Compute shaded light cone bounds:**
        - For each of the 3 observables:
            - Map the observable to the physical (ISA) qubit layout.
            - Compute the forward bounds using `compute_forward_bounds`
            - append the forward bounds to the `forward_bounds_list`
        - Backwards bounds doesn't depend on the observable, so you only need to calculate it once:
            - Compute the backward bounds using `compute_backward_bounds`

    Fill in the cell below.

    </div>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    _Note:_ Calculating the forward and backward bounds will take approximately 30 seconds, so be patient!
    """)
    return


@app.cell
def _(
    SparsePauliOp,
    backend,
    compute_backward_bounds,
    compute_forward_bounds,
    construct_ising_circuit,
    find_unique_box_instructions,
    generate_noise_model_paulis,
    isa_pm,
    np,
    slc_boxing_pm,
):
    num_qubits_ex5 = 15
    num_trotter_steps_ex5 = 3
    rx_angle_1 = np.pi / 8

    circuit_ising_ex5 = construct_ising_circuit(num_qubits_ex5, num_trotter_steps_ex5, rx_angle_1) 
    mirrored_circuit_ex5 = circuit_ising_ex5.compose(circuit_ising_ex5.inverse())
    mirrored_circuit_ex5.measure_all()

    isa_circuit_ex5 = isa_pm.run(mirrored_circuit_ex5)
    final_layout_ex5 = isa_circuit_ex5.layout.final_index_layout()
    boxed_circuit_ex5 = slc_boxing_pm.run(isa_circuit_ex5)
    unique_layers_ex5 = find_unique_box_instructions(boxed_circuit_ex5, normalize_annotations=None, undress_boxes=True)
    noise_model_paulis_ex5 = generate_noise_model_paulis(unique_layers_ex5, backend.coupling_map, boxed_circuit_ex5)
    noise_model_rates_ex5 = {_ref: None for _ref in noise_model_paulis_ex5}

    obs_Z7 = SparsePauliOp.from_sparse_list([("Z", [7], 1.0)], num_qubits=num_qubits_ex5)
    obs_X3_Z11 = SparsePauliOp.from_sparse_list([("XZ", [3, 11], 1.0)], num_qubits=num_qubits_ex5)
    obs_7_Zs = SparsePauliOp.from_sparse_list(
        [("ZZZZZZZ", list(range(4, 11)), 1.0)], num_qubits=num_qubits_ex5
    )
    obs_list = [obs_Z7, obs_X3_Z11, obs_7_Zs]

    slc_atol_1 = 1e-08
    slc_eigval_max_qubits_1 = 18
    slc_evolution_max_terms_1 = 1000
    slc_num_processes_1 = 8
    slc_timeout_1 = 600

    # Forward bounds, one per observable
    forward_bounds_list = []
    for obs in obs_list:
        obs_isa = obs.apply_layout(isa_circuit_ex5.layout, num_qubits=isa_circuit_ex5.num_qubits)
        fb = compute_forward_bounds(
            boxed_circuit_ex5,
            noise_model_paulis_ex5,
            obs_isa,
            evolution_max_terms=slc_evolution_max_terms_1,
            eigval_max_qubits=slc_eigval_max_qubits_1,
            atol=slc_atol_1,
            num_processes=slc_num_processes_1,
            timeout=slc_timeout_1,
        )
        forward_bounds_list.append(fb)

    # Backward bounds, computed once (doesn't depend on the observable)
    backward_bounds_1 = compute_backward_bounds(
        boxed_circuit_ex5,
        noise_model_paulis_ex5,
        evolution_max_terms=slc_evolution_max_terms_1,
        num_processes=slc_num_processes_1,
        timeout=slc_timeout_1,
    )
    return (
        backward_bounds_1,
        boxed_circuit_ex5,
        circuit_ising_ex5,
        final_layout_ex5,
        forward_bounds_list,
        mirrored_circuit_ex5,
        noise_model_paulis_ex5,
        obs_Z7,
        obs_list,
        unique_layers_ex5,
    )


@app.cell
def _(
    backward_bounds_1,
    boxed_circuit_ex5,
    circuit_ising_ex5,
    forward_bounds_list,
    grade_lab3_ex5,
    mirrored_circuit_ex5,
    obs_list,
):
    # grade your answer
    grade_lab3_ex5(circuit_ising_ex5, mirrored_circuit_ex5, boxed_circuit_ex5, obs_list, forward_bounds_list, backward_bounds_1)
    return


@app.cell
def _(check_progress):
    # check your progress across all the labs
    check_progress()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The plots below show the forward and backward bounds for the three observables.
    """)
    return


@app.cell
def _(
    boxed_circuit_ex5,
    display,
    draw_shaded_lightcone,
    forward_bounds_list,
    noise_model_paulis_ex5,
):
    print(f'forward bounds for observable obs_Z7 :')
    for _p in 'XYZ':
        display(draw_shaded_lightcone(boxed_circuit_ex5, forward_bounds_list[0], noise_model_paulis_ex5, pauli_filter=_p, scale=0.15, fold=-1, idle_wires=False, measure_arrows=False))
    return


@app.cell
def _(
    boxed_circuit_ex5,
    display,
    draw_shaded_lightcone,
    forward_bounds_list,
    noise_model_paulis_ex5,
):
    print('forward bounds for observable obs_X3_Z11 :')
    for _p in 'XYZ':
        display(draw_shaded_lightcone(boxed_circuit_ex5, forward_bounds_list[1], noise_model_paulis_ex5, pauli_filter=_p, scale=0.15, fold=-1, idle_wires=False, measure_arrows=False))
    return


@app.cell
def _(
    boxed_circuit_ex5,
    display,
    draw_shaded_lightcone,
    forward_bounds_list,
    noise_model_paulis_ex5,
):
    print('forward bounds for observable obs_7_Zs :')
    for _p in 'XYZ':
        display(draw_shaded_lightcone(boxed_circuit_ex5, forward_bounds_list[2], noise_model_paulis_ex5, pauli_filter=_p, scale=0.15, fold=-1, idle_wires=False, measure_arrows=False))
    return


@app.cell
def _(
    backward_bounds_1,
    boxed_circuit_ex5,
    display,
    draw_shaded_lightcone,
    noise_model_paulis_ex5,
    wire_order_slc,
):
    print('backward bounds:')
    for _p in 'XYZ':
        display(draw_shaded_lightcone(boxed_circuit_ex5, backward_bounds_1, noise_model_paulis_ex5, pauli_filter=_p, scale=0.15, fold=-1, idle_wires=False, wire_order=wire_order_slc, measure_arrows=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.2.6 Merged bounds

    We are now ready to merge the forward and backward bounds to define the shaded lightcone that minimizes sampling overhead.

    #### Why merge bounds?

    The function `merge_bounds` picks a transition point in the circuit where the backward bound switches to the forward bound. The transition is chosen to minimize the total estimated bias, producing a tight lightcone.

    This requires learned noise rates from hardware: the noise model tells the merge algorithm which parts of the circuit dominate the error.

    #### Re-learning noise on the bigger circuit

    Exercise 5 scaled up to 15 qubits, so the circuit changed and its unique layers live on different physical qubits to the previous learned noise model from the 10-qubit PNA setup. So, before we can merge the bounds, we need to re-learn the noise on the 15-qubit layers. We reuse the noise learner parameters defined for PNA in `pna_learner`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    _Note:_ The following cell executes a job on quantum hardware. Ensure you are ready to do this before proceeding. After first execution, we recommend pasting the job id into the `NOISE_LEARN_JOB_ID_SLC` parameter and setting `SUBMIT_NOISE_JOB_SLC = False`. This will prevent accidentally resubmitting the job and keeps the notebook re-runnable after a kernel restart.

    _Estimated QPU execution time is 13 seconds (tested on ibm_pittsburgh)_. The usage estimate above reflects backend execution time only. Queue time, calibration, and runtime session delays may be longer.
    """)
    return


@app.cell
def _(pna_learner, service, unique_layers_ex5):
    NOISE_LEARN_JOB_ID_SLC = None   # paste job_id here on re-run
    SUBMIT_NOISE_JOB_SLC   = False  # set True to submit a fresh learning job
    pna_learner.options.environment.job_tags = ["qgss26"]

    if NOISE_LEARN_JOB_ID_SLC is not None:
        learner_job_slc = service.job(NOISE_LEARN_JOB_ID_SLC)
        print(f"Re-using saved job: {NOISE_LEARN_JOB_ID_SLC}")
    elif SUBMIT_NOISE_JOB_SLC:
        learner_job_slc = pna_learner.run(unique_layers_ex5)
        NOISE_LEARN_JOB_ID_SLC = learner_job_slc.job_id()
        print(f"Submitted: {NOISE_LEARN_JOB_ID_SLC}")
    else:
        print("Set SUBMIT_NOISE_JOB_SLC=True to submit a fresh job, "
              "or paste a saved job id into NOISE_LEARN_JOB_ID_SLC and re-run.")
    return (NOISE_LEARN_JOB_ID_SLC,)


@app.cell
def _(NOISE_LEARN_JOB_ID_SLC, service):
    learner_job_slc_1 = service.job(NOISE_LEARN_JOB_ID_SLC)
    print(f'{NOISE_LEARN_JOB_ID_SLC}  (status: {learner_job_slc_1.status()})')
    return (learner_job_slc_1,)


@app.cell
def _(learner_job_slc_1):
    if learner_job_slc_1.status() == 'DONE':
        noise_learner_result_slc = learner_job_slc_1.result()
    else:
        print(f'Not done yet (status={learner_job_slc_1.status()}). Re-run cell when DONE.')
    return (noise_learner_result_slc,)


@app.cell
def _(noise_learner_result_slc, unique_layers_ex5):
    if 'noise_learner_result_slc' in dir() and noise_learner_result_slc is not None:
        refs_to_noise_models_slc = noise_learner_result_slc.to_dict(unique_layers_ex5, require_refs=False)
        print(f"refs_to_noise_models_slc has {len(refs_to_noise_models_slc)} entries")
    else:
        print("Run the noise-learning cell above and wait for it to finish first.")
    return (refs_to_noise_models_slc,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Compute merged bounds

    For each observable, we compute the merged bounds with the learned noise model `refs_to_noise_models_slc`.

    _Note:_ You may see the following warning message "_Optimal spacetime partitioning not implemented!Just partitioning list of noisy boxes._" This is expected and not an error.
    """)
    return


@app.cell
def _(
    backward_bounds_1,
    boxed_circuit_ex5,
    forward_bounds_list,
    merge_bounds,
    refs_to_noise_models_slc,
):
    merged_bounds_with_noise = []
    for _i in range(3):
        merged_bounds_with_noise.append(merge_bounds(boxed_circuit_ex5, forward_bounds_list[_i], backward_bounds_1, refs_to_noise_models_slc))
    return (merged_bounds_with_noise,)


@app.cell
def _(
    boxed_circuit_ex5,
    display,
    draw_shaded_lightcone,
    merged_bounds_with_noise,
    noise_model_paulis_ex5,
):
    print('Merged bounds with noise model for observable obs_Z7:')
    for _p in 'XYZ':
        display(draw_shaded_lightcone(boxed_circuit_ex5, merged_bounds_with_noise[0], noise_model_paulis_ex5, pauli_filter=_p, scale=0.15, fold=-1, idle_wires=False, measure_arrows=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.2.7 Comparing Sampling Overhead

    In this section, we compute the sampling overhead when implementing SLC versus PEC alone for the 3 observables you constructed in Exercise 5.

    We defined the sampling overhead for PEC in section 3.2.1 as $\gamma^2$ where $$\gamma = \exp\!\big(2\sum_{l,\sigma}\lambda_{l,\sigma}\big),$$ and $\lambda_{l,\sigma}$ is the learned rate of generator $\sigma$ at layer $l$ in the circuit.

    In the cell below, we calculate the quantity $\gamma$ both from the equation above and using the helper function `gamma_from_noisy_boxes` and see that they agree.
    """)
    return


@app.cell
def _(
    boxed_circuit_ex5,
    gamma_from_noisy_boxes,
    map_modifier_ref_to_ref,
    np,
    refs_to_noise_models_slc,
):
    id_map = map_modifier_ref_to_ref(boxed_circuit_ex5)
    summed_rates = 0.0
    # Manual γ from the Pauli-Lindblad formula: γ = exp(2 · Σ λ).
    for box_id, noise_id in id_map.items():
        learned_plm_ex5 = refs_to_noise_models_slc[noise_id]
        summed_rates = summed_rates + np.sum(learned_plm_ex5.rates)
    total_gamma = np.exp(2 * summed_rates)
    gamma_full_helper = gamma_from_noisy_boxes(refs_to_noise_models_slc, id_map)
    assert np.isclose(total_gamma, gamma_full_helper), f'Manual γ ({total_gamma:.6e}) disagrees with gamma_from_noisy_boxes ({gamma_full_helper:.6e})'
    # Cross-check against the helper. This guards against edge cases
    # (negative fitted rates, mis-mapped refs, etc.).
    print(f'Full PEC γ = {total_gamma:.6f},  sampling cost γ² = {total_gamma ** 2:.6f}')
    print(f'(helper agrees: γ = {gamma_full_helper:.6f})')
    return id_map, total_gamma


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Computing Local Scales

    The function `compute_local_scales` ranks each possible noise generator in the circuit by how much that error could contribute to the bias in the final measurement. It also considers the mitigation cost to correct that error. It selects the subset of noise generators whose error mitigation reduces bias as much as possible within a defined `bias_tolerance` budget. The function then returns three things:

    - `local_scales`: the per-generator scale factors that say which Paulis to actively mitigate vs leave alone
    - `sampling_cost`: the predicted $\gamma^2$ overhead
    - `residual_bias_bound`: the bias kept by leaving some generators unmitigated
    """)
    return


@app.cell
def _(
    boxed_circuit_ex5,
    compute_local_scales,
    merged_bounds_with_noise,
    np,
    refs_to_noise_models_slc,
):
    # Bias-cost tradeoff sweep for all 3 observables (obs_Z7, obs_X3_Z11, obs_7_Zs).
    # bias_tolerance from 0.001 to 0.101 in steps of 0.01 (no 0.0 — see note).
    biases = [[], [], []]
    costs = [[], [], []]
    local_scales = [[], [], []]
    bias_tolerance_values = np.arange(0.001, 0.102, 0.01).tolist()
    for _i in range(3):
        for bias in bias_tolerance_values:
            try:
                local_scale_, cost_, bias_ = compute_local_scales(boxed_circuit_ex5, merged_bounds_with_noise[_i], refs_to_noise_models_slc, sampling_cost_budget=np.inf, bias_tolerance=bias)
                biases[_i].append(bias_)
                costs[_i].append(cost_)
                local_scales[_i].append(local_scale_)  # circuit with noise boxes
            except (IndexError, ValueError):  # merged bounds for observable i
                continue  # learned noise model rates  # no cost budget — find optimal tradeoff  # maximum allowed bias  # compute_local_scales may not converge for every bound/bias combination  # (depends on bounds structure); skip silently so the rest of the curve  # still renders.
    return biases, costs


@app.cell
def _(biases, costs, np, plt, total_gamma):
    xticks = np.arange(0, 11)
    _fig, _ax = plt.subplots(figsize=(8, 5))
    _ax.axhline(y=total_gamma ** 2, color='tab:orange', linestyle='--', linewidth=2, label='Full PEC')
    observable_names = ['Z on q7', 'X on q3, Z on q11', 'Z on 7 central qubits']
    # Full-PEC reference (no SLC truncation).
    _colors = ['tab:blue', 'tab:green', 'tab:red']
    for _i in range(3):
    # Bias-cost tradeoff curves for all 3 observables.
        if not biases[_i]:
            continue
        _ax.plot(100 * np.array(biases[_i]), np.array(costs[_i]), 'o-', c=_colors[_i], label=f'SLC ({observable_names[_i]})')
    _ax.set_yscale('log')
    _ax.set_xticks(xticks, [f'{_x:.1f}' for _x in xticks])
    _ax.set_xlabel('Remaining bias [%]', fontsize=12)  # sweep produced no points for this observable
    _ax.set_ylabel('Sampling overhead, $\\gamma^2$', fontsize=12)
    _ax.grid(True, which='both', alpha=0.3)
    _ax.legend(loc='upper right')
    _fig.suptitle('PEC sampling-overhead reduction enabled by SLC', fontsize=13)
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The plot shows the sampling overhead $\gamma^2$ versus the remaining bias for each of the three observables, with the full-PEC value as a horizontal reference. Some takeaways:

    - the local single-qubit observable on qubit 7 (blue) has the smallest overhead
    - the two-body observable: X on qubit 3 and Z on qubit 11 (green) sits higher because its forward and backward lightcones cover more layers
    -  the 7 qubit observable Z's on qubits 4-10 (red) has the widest lightcone.
    - Across the scanned bias-tolerance range all three overheads stay below full PEC.

    In the next section we focus on the most local observable, `obs_Z7`, executing the circuit on the QPU to compare full PEC against SLC.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.2.8 Executing the error-mitigated job on the QPU

    We run the QPU job for one observable: the local single-qubit `obs_Z7`.
    """)
    return


@app.cell
def _(
    boxed_circuit_ex5,
    compute_local_scales,
    merged_bounds_with_noise,
    np,
    refs_to_noise_models_slc,
    total_gamma,
):
    # Operating point: bias_tolerance = 0.02 (recommended trade-off between
    # sampling cost reduction and residual bias bound). Observable: obs_Z7.
    chosen_bias_thres = 0.02

    local_scales_chosen, sampling_cost_chosen, residual_bias_chosen = compute_local_scales(
        boxed_circuit_ex5,
        merged_bounds_with_noise[0],   # obs_Z7 → index 0
        refs_to_noise_models_slc,
        sampling_cost_budget=np.inf,
        bias_tolerance=chosen_bias_thres,
    )
    print(f"Operating point: bias_tolerance = {chosen_bias_thres}")
    print(f"  sampling cost (γ²)  = {sampling_cost_chosen:.3f}  "
          f"(vs full PEC γ² = {total_gamma**2:.3f})")
    print(f"  residual bias bound = {100*residual_bias_chosen:.1f}%")
    return chosen_bias_thres, local_scales_chosen


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Extract the basis reference from the boxed circuit's `ChangeBasis` annotation and bind the measurement basis through `samplex_inputs_slc`.

    - Basis encoding: $0=I$, $1=Z$, $2=X$, $3=Y$.

    (`get_annotation` and `ChangeBasis` are imported at the top of the notebook)
    """)
    return


@app.cell
def _(
    ChangeBasis,
    boxed_circuit_ex5,
    final_layout_ex5,
    get_annotation,
    get_measurement_bases,
    np,
    obs_Z7,
    samplomatic,
):
    # Build template circuit + samplex for the boxed_circuit_ex5 (15-qubit).
    template_circuit_slc, samplex_slc = samplomatic.build(boxed_circuit_ex5)
    meas_boxes_slc = [_inst for _inst in boxed_circuit_ex5.data if _inst.operation.name == 'box' and get_annotation(_inst.operation, ChangeBasis) is not None]
    # Find the measurement box and extract its ChangeBasis ref.
    basis_ref_slc = get_annotation(meas_boxes_slc[0].operation, ChangeBasis).ref
    canonical_qubits_ex5 = [_i for _i, q in enumerate(boxed_circuit_ex5.qubits) if q in meas_boxes_slc[0].qubits]
    p_2_v_ex5 = {_p: v for v, _p in enumerate(final_layout_ex5)}
    c_2_v_ex5 = {c: p_2_v_ex5[_p] for c, _p in enumerate(canonical_qubits_ex5)}
    bases_virt_obs1, reverser_virt_obs1 = get_measurement_bases(obs_Z7)
    # Canonical → physical → virtual mapping for boxed_circuit_ex5.
    # Bases for obs_Z7 (single Pauli term → single basis) in canonical order.
    meas_bases_slc_canonical = [np.array([base[c_2_v_ex5[c]] for c in range(15)], dtype=np.uint8) for base in bases_virt_obs1]
    return (
        basis_ref_slc,
        meas_bases_slc_canonical,
        reverser_virt_obs1,
        samplex_slc,
        template_circuit_slc,
    )


@app.cell
def _(
    basis_ref_slc,
    local_scales_chosen,
    meas_bases_slc_canonical,
    samplex_slc,
):
    samplex_inputs_unmit = {f'noise_scales.{_ref}': 0.0 for _ref in local_scales_chosen}
    samplex_inputs_unmit = samplex_inputs_unmit | {'basis_changes': {basis_ref_slc: meas_bases_slc_canonical[0]}}
    samplex_args_unmit = samplex_slc.inputs().make_broadcastable().bind(**samplex_inputs_unmit)
    samplex_inputs_slc = {f'noise_scales.{_ref}': -1.0 for _ref in local_scales_chosen}
    samplex_inputs_slc = samplex_inputs_slc | {'basis_changes': {basis_ref_slc: meas_bases_slc_canonical[0]}}
    samplex_inputs_slc = samplex_inputs_slc | {'local_scales': local_scales_chosen}
    samplex_args_slc = samplex_slc.inputs().make_broadcastable().bind(**samplex_inputs_slc)
    return samplex_args_slc, samplex_args_unmit


@app.cell
def _(
    QuantumProgram,
    refs_to_noise_models_slc,
    samplex_args_slc,
    samplex_args_unmit,
    samplex_slc,
    template_circuit_slc,
):
    # Parameters for the SLC executor job — tuned for tight stats with minimal QPU.
    # Each samplex_item gets these many shots; we have 2 items (unmit + PEC+SLC).
    shots_per_randomization_slc = 64
    num_randomizations_slc      = 256

    # Build the QuantumProgram. noise_maps at program level — keyed by unique-layer
    # refs from the SLC NoiseLearner result.
    program_slc = QuantumProgram(
        shots=shots_per_randomization_slc,
        noise_maps=refs_to_noise_models_slc,
    )

    # Item 0: unmitigated baseline (noise_scales = 0)
    program_slc.append_samplex_item(
        circuit=template_circuit_slc,
        samplex=samplex_slc,
        samplex_arguments=samplex_args_unmit,
        shape=(num_randomizations_slc,),
    )
    # Item 1: PEC+SLC (noise_scales = -1, with local_scales)
    program_slc.append_samplex_item(
        circuit=template_circuit_slc,
        samplex=samplex_slc,
        samplex_arguments=samplex_args_slc,
        shape=(num_randomizations_slc,),
    )

    print(f"Program built: 2 samplex_items (unmit + PEC+SLC), "
          f"{num_randomizations_slc} randomizations × {shots_per_randomization_slc} shots each")
    return (program_slc,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    _Note:_ The following cell executes a job on quantum hardware. Ensure you are ready to do this before proceeding. After first execution, we recommend pasting the job id into the `EXECUTOR_JOB_ID_SLC` parameter and setting `SUBMIT_EXECUTOR_JOB_SLC = False`. This will prevent accidentally resubmitting the job and keeps the notebook re-runnable after a kernel restart.

    _Estimated QPU execution time is 12 seconds (tested on ibm_fez)_. The usage estimate above reflects backend execution time only. Queue time, calibration, and runtime session delays may be longer.
    """)
    return


@app.cell
def _(Executor, backend, program_slc, service):
    #  qpu time = 12s, tested on ibm_fez
    _executor = Executor(backend)
    EXECUTOR_JOB_ID_SLC = None
    SUBMIT_EXECUTOR_JOB_SLC = False
    _executor.options.environment.job_tags = ['qgss26']  # paste job_id here after first submission
    if EXECUTOR_JOB_ID_SLC is not None:  # set True to submit a fresh job
        job_exec_slc = service.job(EXECUTOR_JOB_ID_SLC)
        print(f'Re-using saved job: {EXECUTOR_JOB_ID_SLC}')
    elif SUBMIT_EXECUTOR_JOB_SLC:
        job_exec_slc = _executor.run(program_slc)
        EXECUTOR_JOB_ID_SLC = job_exec_slc.job_id()
        print(f'Submitted: {EXECUTOR_JOB_ID_SLC}')
    else:
        print('Set SUBMIT_EXECUTOR_JOB_SLC=True to submit a fresh job, or paste a saved job id into EXECUTOR_JOB_ID_SLC and re-run.')
    return EXECUTOR_JOB_ID_SLC, job_exec_slc


@app.cell
def _(EXECUTOR_JOB_ID_SLC, job_exec_slc):
    if EXECUTOR_JOB_ID_SLC is not None:
        if job_exec_slc.status() == "DONE":
            exec_results_slc = job_exec_slc.result()
            print(f"Got {len(exec_results_slc)} samplex_item results "
                  f"(item 0 = unmitigated, item 1 = PEC+SLC).")
        else:
            print(f"Not done yet: {job_exec_slc.status()}")
    return (exec_results_slc,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.2.9 Analyse Results
    """)
    return


@app.cell
def _(
    chosen_bias_thres,
    exec_results_slc,
    executor_expectation_values,
    gamma_from_noisy_boxes,
    id_map,
    local_scales_chosen,
    np,
    plt,
    refs_to_noise_models_slc,
    reverser_virt_obs1,
    total_gamma,
):
    # Extract two results from the same Executor job:
    #   results[0] → unmitigated (noise_scales=0, no gamma_factor)
    #   results[1] → PEC+SLC      (noise_scales=-1, local_scales applied)
    gamma_slc = gamma_from_noisy_boxes(refs_to_noise_models_slc, id_map, local_scales_chosen)
    # γ for PEC+SLC normalization
    res_unmit_slc = executor_expectation_values(exec_results_slc[0]['meas'], reverser_virt_obs1, meas_basis_axis=None, avg_axis=0, measurement_flips=exec_results_slc[0]['measurement_flips.meas'], pauli_signs=exec_results_slc[0].get('pauli_signs', None), rescale_factors=None, gamma_factor=None)
    exp_val_unmit_slc = res_unmit_slc[0][0]
    # Item 0 — Unmitigated
    std_unmit_slc = res_unmit_slc[0][1]
    res_slc = executor_expectation_values(exec_results_slc[1]['meas'], reverser_virt_obs1, meas_basis_axis=None, avg_axis=0, measurement_flips=exec_results_slc[1]['measurement_flips.meas'], pauli_signs=exec_results_slc[1].get('pauli_signs', None), rescale_factors=None, gamma_factor=gamma_slc)
    exp_val_slc = res_slc[0][0]
    std_slc = res_slc[0][1]
    ideal_obs_Z7 = 1.0
    print(f"{'Method':<14} {'<O_Z7>':>10} {'std':>12} {'γ²':>10}")
    print('─' * 50)
    print(f"{'Unmitigated':<14} {exp_val_unmit_slc:>+10.4f} {std_unmit_slc:>12.4e} {'1.000':>10}")
    print(f"{'PEC+SLC':<14} {exp_val_slc:>+10.4f} {std_slc:>12.4e} {gamma_slc ** 2:>10.3f}")
    print(f"{'Ideal':<14} {ideal_obs_Z7:>+10.4f}")
    print()
    print(f'Sampling-overhead reduction: {total_gamma ** 2 / gamma_slc ** 2:.2f}× vs full PEC  (γ² {total_gamma ** 2:.2f} → {gamma_slc ** 2:.2f})')
    # Item 1 — PEC+SLC
    print(f'Mitigation: {(exp_val_slc - exp_val_unmit_slc) / (ideal_obs_Z7 - exp_val_unmit_slc) * 100:.1f}% of the unmitigated error closed')
    _fig, _ax = plt.subplots(figsize=(7, 4.5))
    methods = ['Unmitigated', 'PEC+SLC']
    values = [exp_val_unmit_slc, exp_val_slc]
    _errs = [std_unmit_slc, std_slc]
    _colors = ['tab:gray', 'tab:purple']
    _x = np.arange(len(methods))
    _ax.errorbar(_x, values, yerr=_errs, fmt='o', markersize=14, capsize=6, color='black', ecolor='gray', linewidth=2, zorder=3)
    for _xi, vi, ci in zip(_x, values, _colors):
        _ax.scatter([_xi], [vi], color=ci, s=120, zorder=4)
    _ax.axhline(ideal_obs_Z7, color='green', linestyle='--', linewidth=2, label=f'Ideal = {ideal_obs_Z7}', zorder=2)
    _ax.set_xticks(_x)
    _ax.set_xticklabels(methods)  # Z@7 on a Trotter mirror with |0⟩ initial state → +1
    _ax.set_ylabel('$\\langle Z_7 \\rangle$', fontsize=13)
    _ax.set_title(f'15-qubit Ising mirror — PEC+SLC at bias_tolerance={chosen_bias_thres}', fontsize=12)
    _ax.legend(loc='lower right')
    _ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    # Comparison plot
    #ax.set_ylim(0, max(1.2, max(values) * 1.2))
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.2.10 Conclusion
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The key advantage of the SLC technique is sampling-cost reduction. By keeping only the noise generators inside the propagated lightcone of the target observable, the full PEC overhead $\gamma^2$ drops at the chosen `bias_tolerance`. The trade-off is bias for cost: a small admitted bias buys a large reduction in sampling overhead.

    For a local observable like $Z_7$ on this 15-qubit Ising mirror, the lightcone is narrow enough that pruning preserves the expectation value: the recovered $\langle Z_7\rangle$ is close to the ideal value of 1, and the sampling overhead is reduced compared to plain PEC.

    This concludes Chapter 3. We covered three structure-aware error-mitigation strategies:

    - PNA: rewrite the observable to absorb anti-noise
    - PEC: rewrite the circuit with anti-noise
    - SLC: prune PEC's noise generators using the shaded lightcone

    These techniques are all built on the Samplomatic + NoiseLearnerV3 foundation from Chapter 2.

    Congratulations! You have completed Lab 3.

    Next, in Lab 4, we introduce the concept of quantum advantage and how to measure it, including the use of IBM’s Quantum Advantage Tracker to evaluate experiments. You will also demonstrate these ideas in practice by implementing a quantum optimization algorithm with error mitigation techniques and smart encoding strategies to reduce the number of qubits.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Additional information

    **Created by:** Sophy Shin & Sophie Engineer

    **Version:** 1.0.0
    """)
    return


if __name__ == "__main__":
    app.run()
