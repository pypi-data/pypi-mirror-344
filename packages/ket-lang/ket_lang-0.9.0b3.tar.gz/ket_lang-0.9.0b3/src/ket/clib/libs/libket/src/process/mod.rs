// SPDX-FileCopyrightText: 2024 Evandro Chagas Ribeiro da Rosa <evandro@quantuloop.com>
//
// SPDX-License-Identifier: Apache-2.0

mod execution;
mod measure;
mod util;

use crate::{
    circuit::Circuit,
    decompose::{AuxMode, Registry, Schema, State},
    error::{KetError, Result},
    execution::{Capability, ExecutionProtocol, QuantumExecution},
    graph::GraphMatrix,
    ir::{
        gate::{Param, QuantumGate},
        instructions::Instruction,
        qubit::{LogicalQubit, PhysicalQubit, Qubit},
    },
    prelude::ExecutionTarget,
};
use serde::{Deserialize, Serialize};
use std::collections::{HashMap, HashSet};

/// Ket quantum process.
#[derive(Debug, Default)]
pub struct Process {
    /// Control qubits stack.
    ctrl_stack: Vec<CtrlStack>,
    /// List of control qubits.
    ctrl_list: QubitList,
    /// If the list of control qubits are up to date.
    ctrl_list_is_valid: bool,

    /// List of gates to be applied when inverse scopes ends.
    adj_stack: Vec<GateList>,

    /// Logical circuit with decomposed gates, if necessary.
    logical_circuit: Circuit<LogicalQubit>,
    /// Physical circuit, if coupling graph is available.
    physical_circuit: Option<Circuit<PhysicalQubit>>,

    /// List of measurement results.
    measurements: Vec<Option<u64>>,
    /// List of sample results.
    samples: Vec<Option<Sample>>,
    /// List of expected value result.
    exp_values: Vec<Option<f64>>,
    /// List of dump results.
    dumps: Vec<Option<DumpData>>,

    /// Quantum execution target configuration.
    execution_target: ExecutionTarget,
    /// Quantum execution target.
    quantum_execution: Option<QuantumExecution>,
    /// QPU qubit coupling graph
    coupling_graph: Option<GraphMatrix<PhysicalQubit>>,

    /// Number of qubits allocated by the user.
    allocated_qubits: usize,
    /// Number of qubits allocated by the user or the runtime lib.
    qubit_count: usize,
    /// Number of auxiliary qubits allocated by the runtime lib.
    aux_count: usize,
    /// Allocated qubits that has been measured.
    valid_qubit: HashMap<LogicalQubit, bool>,
    /// Qubits ready to be allocated.
    alloc_stack: Vec<LogicalQubit>,
    /// Qubits that can be used as clean auxiliary.
    clean_qubits: HashSet<LogicalQubit>,

    /// Gradient results.
    gradients: Vec<Option<f64>>,
    /// Quantum gates parameters for gradient computation.
    parameters: Vec<f64>,

    /// Number of U4 gates (value) generated from each decomposition algorithm (key).
    decomposition_stats: HashMap<String, i64>,

    /// Measurement features enabled.
    features: FeaturesAvailable,

    /// Defined execution strategy
    execution_strategy: Option<ExecutionStrategy>,
}

#[derive(Debug, Clone, Copy, Default)]
enum ExecutionStrategy {
    #[default]
    ManagedByTarget,
    MeasureFromSample,
    ClassicalShadows {
        /// Weights for selecting the random measurement basis (X, Y,Z).
        bias: (u8, u8, u8),
        /// Number of measurement rounds.
        samples: usize,
        /// Number of shorts for each measurement round.
        shots: usize,
    },
    DirectSample(usize),
}

#[derive(Debug)]
enum GateInstruction {
    Gate {
        gate: QuantumGate,
        target: LogicalQubit,
        control: Vec<LogicalQubit>,
    },
    AuxRegistry(std::rc::Rc<std::cell::RefCell<Registry>>),
}

impl GateInstruction {
    fn inverse(self) -> Self {
        match self {
            Self::Gate {
                gate,
                target,
                control,
            } => Self::Gate {
                gate: gate.inverse(),
                target,
                control,
            },
            Self::AuxRegistry(registry) => Self::AuxRegistry(registry),
        }
    }
}

type GateList = Vec<GateInstruction>;

type QubitList = Vec<LogicalQubit>;
type CtrlStack = Vec<QubitList>;

#[derive(Debug, Default, Clone)]
struct FeaturesAvailable {
    measure: bool,
    sample: bool,
    dump: bool,
    exp_value: bool,
    gradient: bool,
}

pub type Sample = (Vec<u64>, Vec<u64>);

#[derive(Debug, Clone, Default, Deserialize, Serialize)]
pub struct DumpData {
    pub basis_states: Vec<Vec<u64>>,
    pub amplitudes_real: Vec<f64>,
    pub amplitudes_imag: Vec<f64>,
}

#[derive(Debug, Serialize)]
pub struct Metadata {
    pub logical_gate_count: HashMap<usize, i64>,
    pub logical_circuit_depth: usize,
    pub physical_gate_count: Option<HashMap<usize, i64>>,
    pub physical_circuit_depth: Option<usize>,
    pub allocated_qubits: usize,
    pub terminated: bool,
    pub decomposition: HashMap<String, i64>,
}

impl Process {
    pub fn new(
        execution_target: ExecutionTarget,
        quantum_execution: Option<QuantumExecution>,
    ) -> Self {
        let features = match &execution_target.execution_protocol {
            ExecutionProtocol::ManagedByTarget {
                measure,
                sample,
                exp_value,
                dump,
            } => {
                if execution_target.gradient.is_some()
                    && !matches!(exp_value, Capability::Unsupported)
                {
                    FeaturesAvailable {
                        exp_value: true,
                        gradient: true,
                        ..Default::default()
                    }
                } else {
                    FeaturesAvailable {
                        measure: !matches!(measure, Capability::Unsupported),
                        sample: !matches!(sample, Capability::Unsupported),
                        dump: !matches!(dump, Capability::Unsupported),
                        exp_value: !matches!(exp_value, Capability::Unsupported),
                        gradient: false,
                    }
                }
            }
            ExecutionProtocol::SampleBased(Some(_)) => {
                if execution_target.gradient.is_some() {
                    FeaturesAvailable {
                        exp_value: true,
                        gradient: true,
                        ..Default::default()
                    }
                } else {
                    FeaturesAvailable {
                        measure: true,
                        sample: true,
                        exp_value: true,
                        ..Default::default()
                    }
                }
            }
            ExecutionProtocol::SampleBased(None) => FeaturesAvailable {
                measure: true,
                sample: true,
                ..Default::default()
            },
        };

        let coupling_graph = execution_target.qpu.as_ref().and_then(|qpu| {
            qpu.coupling_graph.as_ref().map(|graph| {
                let mut cq = GraphMatrix::<PhysicalQubit>::new(0);
                for (i, j) in graph {
                    cq.set_edge((*i).into(), (*j).into(), 1);
                }
                cq.calculate_distance();
                cq
            })
        });

        Self {
            ctrl_stack: vec![Vec::new()],
            execution_target,
            quantum_execution,
            coupling_graph,
            features,
            ..Default::default()
        }
    }

    pub fn alloc(&mut self) -> Result<LogicalQubit> {
        self.non_gate_checks(None, true)?;

        self.reserve_qubits(1)?;
        self.allocated_qubits += 1;

        Ok(self.alloc_stack.pop().unwrap())
    }

    fn reserve_qubits(&mut self, num_qubits: usize) -> Result<()> {
        while self.alloc_stack.len() < num_qubits {
            if self.allocated_qubits > self.execution_target.num_qubits {
                return Err(KetError::MaxQubitsReached);
            }

            let qubit = LogicalQubit::main(self.qubit_count);

            self.qubit_count += 1;

            self.alloc_stack.push(qubit);
            assert!(self.clean_qubits.insert(qubit));
        }

        Ok(())
    }

    fn try_alloc_aux(
        &mut self,
        num_qubits: usize,
        interacting_qubits: Option<&[LogicalQubit]>,
    ) -> Option<Vec<LogicalQubit>> {
        if (interacting_qubits.is_none()
            && (num_qubits + self.allocated_qubits) > self.execution_target.num_qubits)
            || (interacting_qubits.is_some()
                && (num_qubits + interacting_qubits.unwrap().len())
                    > self.execution_target.num_qubits)
        {
            return None;
        }

        let result: Vec<_> = (0..num_qubits)
            .map(|index| LogicalQubit::aux(index + self.aux_count))
            .collect();

        self.aux_count += num_qubits;

        let reserver_qubits = if let Some(interacting_qubits) = interacting_qubits {
            let dirty_available = self.allocated_qubits - interacting_qubits.len();
            num_qubits.saturating_sub(dirty_available)
        } else {
            num_qubits
        };

        self.reserve_qubits(reserver_qubits).unwrap(); // this should not fail if the first check is correct

        Some(result)
    }

    fn free_aux(&mut self, registry: &Registry) {
        if let Some(aux_qubits) = &registry.aux_qubits {
            let mut allocated = HashSet::new();
            for aux_qubit in aux_qubits {
                let mut main_qubit = None;
                for interacting_qubit in self.logical_circuit.interacting_qubits(*aux_qubit) {
                    for candidate_qubit in self
                        .logical_circuit
                        .interacting_qubits_rev(*interacting_qubit)
                    {
                        if candidate_qubit.is_aux() {
                            continue;
                        }
                        let use_this = match &registry.interacting_qubits {
                            Some(interacting_qubits) => {
                                !interacting_qubits.contains(candidate_qubit)
                                    && !allocated.contains(candidate_qubit)
                            }
                            None => {
                                self.clean_qubits.contains(candidate_qubit)
                                    && !allocated.contains(candidate_qubit)
                            }
                        };

                        if use_this {
                            main_qubit = Some(*candidate_qubit);
                            break;
                        }
                    }
                }
                let main_qubit = if let Some(main_qubit) = main_qubit {
                    main_qubit
                } else {
                    let mut main_qubit = None;
                    for candidate_qubit in &self.clean_qubits {
                        if !allocated.contains(candidate_qubit) {
                            main_qubit = Some(*candidate_qubit);
                            break;
                        }
                    }

                    if main_qubit.is_none() {
                        for candidate_qubit in 0..self.allocated_qubits {
                            let candidate_qubit = LogicalQubit::main(candidate_qubit);
                            if !allocated.contains(&candidate_qubit)
                                && !registry
                                    .interacting_qubits
                                    .as_ref()
                                    .unwrap()
                                    .contains(&candidate_qubit)
                            {
                                main_qubit = Some(candidate_qubit);
                                break;
                            }
                        }
                    }

                    main_qubit.unwrap()
                };
                allocated.insert(main_qubit);
                self.logical_circuit.alloc_aux_qubit(*aux_qubit, main_qubit);
            }
        }
    }

    pub fn gate(&mut self, mut gate: QuantumGate, target: LogicalQubit) -> Result<()> {
        if gate.is_identity() {
            return Ok(());
        }

        self.flatten_control_qubits();

        let parameter_gate = matches!(
            gate,
            QuantumGate::RotationX(Param::Ref { .. })
                | QuantumGate::RotationY(Param::Ref { .. })
                | QuantumGate::RotationZ(Param::Ref { .. })
                | QuantumGate::Phase(Param::Ref { .. })
        );

        if parameter_gate {
            if !self.ctrl_list.is_empty() {
                return Err(KetError::ControlledParameter);
            } else if let QuantumGate::RotationX(param)
            | QuantumGate::RotationY(param)
            | QuantumGate::RotationZ(param)
            | QuantumGate::Phase(param) = &mut gate
            {
                param.update_ref(self.parameters[param.index()]);
            }
        }

        self.gate_checks(target)?;

        for qubit in self.ctrl_list.iter().chain([&target]) {
            self.clean_qubits.remove(qubit);
        }

        if !self.ctrl_list.is_empty() && self.execution_target.qpu.is_some() {
            let mut schema = Schema::default();
            let interacting_qubits: Vec<_> =
                self.ctrl_list.iter().cloned().chain([target]).collect();

            for algorithm in gate.decomposition_list(self.ctrl_list.len()) {
                if !algorithm.need_aux() {
                    schema = Schema {
                        algorithm,
                        aux_qubits: None,
                    };
                    break;
                }

                if let Some(qubits) = self.try_alloc_aux(
                    algorithm.aux_needed(self.ctrl_list.len()),
                    if matches!(algorithm.aux_mode(), AuxMode::Dirty) {
                        Some(&interacting_qubits)
                    } else {
                        None
                    },
                ) {
                    schema = Schema {
                        algorithm,
                        aux_qubits: Some(qubits),
                    };
                    break;
                }
            }

            let registry: std::rc::Rc<std::cell::RefCell<Registry>> =
                std::rc::Rc::new(std::cell::RefCell::new(Registry {
                    algorithm: schema.algorithm,
                    aux_qubits: schema.aux_qubits.clone(),
                    interacting_qubits: if schema.algorithm.aux_mode() == AuxMode::Dirty {
                        Some(interacting_qubits)
                    } else {
                        None
                    },
                    ..Default::default()
                }));

            self.push_gate(GateInstruction::AuxRegistry(registry.clone()));

            for (gate, target, control) in gate.decompose(
                target,
                &self.ctrl_list,
                schema,
                self.execution_target.qpu.as_ref().unwrap().u4_gate,
            ) {
                let control = control.map_or(vec![], |control| vec![control]);
                self.push_gate(GateInstruction::Gate {
                    gate,
                    target,
                    control,
                });
            }

            self.push_gate(GateInstruction::AuxRegistry(registry));
        } else {
            self.push_gate(GateInstruction::Gate {
                gate,
                target,
                control: self.ctrl_list.to_owned(),
            });
        }

        Ok(())
    }

    fn push_gate(&mut self, gate: GateInstruction) {
        if let Some(ajd_stack) = self.adj_stack.last_mut() {
            ajd_stack.push(gate);
        } else {
            match gate {
                GateInstruction::Gate {
                    gate,
                    target,
                    control,
                } => {
                    self.logical_circuit.gate(gate, target, &control);
                    if let Some(QuantumExecution::Live(execution)) = self.quantum_execution.as_mut()
                    {
                        execution.gate(gate, target, &control);
                    }
                }
                GateInstruction::AuxRegistry(registry) => {
                    let mut registry = registry.borrow_mut();
                    match registry.state {
                        State::Begin => {
                            registry.num_u4 =
                                *self.logical_circuit.gate_count.entry(2).or_default();
                            registry.state = State::End;
                        }
                        State::End => {
                            *self
                                .decomposition_stats
                                .entry(registry.algorithm.to_string())
                                .or_default() +=
                                *self.logical_circuit.gate_count.entry(2).or_default()
                                    - registry.num_u4;
                            self.free_aux(&registry);
                        }
                    }
                }
            }
        }
    }

    pub fn global_phase(&mut self, angle: f64) -> Result<()> {
        self.adj_ctrl_checks(None)?;
        self.flatten_control_qubits();

        if self.ctrl_list.is_empty() {
            return Ok(());
        }

        let qubits = self.ctrl_list.clone();

        self.ctrl_begin()?;
        self.ctrl_push(&qubits[1..])?;
        self.gate(QuantumGate::Phase(angle.into()), qubits[0])?;
        self.ctrl_pop()?;
        self.ctrl_end()?;
        Ok(())
    }

    pub fn get_measure(&self, index: usize) -> Option<u64> {
        self.measurements.get(index).copied().flatten()
    }

    pub fn get_sample(&self, index: usize) -> Option<&Sample> {
        self.samples.get(index).and_then(|s| s.as_ref())
    }

    pub fn get_exp_value(&self, index: usize) -> Option<f64> {
        self.exp_values.get(index).copied().flatten()
    }

    pub fn get_dump(&self, index: usize) -> Option<&DumpData> {
        self.dumps.get(index).and_then(|d| d.as_ref())
    }

    pub fn ctrl_push(&mut self, qubits: &[LogicalQubit]) -> Result<()> {
        self.flatten_control_qubits();
        self.adj_ctrl_checks(Some(qubits))?;
        self.ctrl_stack.last_mut().unwrap().push(qubits.to_owned());
        self.ctrl_list_is_valid = false;
        Ok(())
    }

    pub fn ctrl_pop(&mut self) -> Result<()> {
        self.ctrl_list_is_valid = false;

        if self.ctrl_stack.last_mut().unwrap().pop().is_none() {
            Err(KetError::ControlStackEmpty)
        } else {
            Ok(())
        }
    }

    pub fn adj_begin(&mut self) -> Result<()> {
        self.adj_ctrl_checks(None)?;
        self.adj_stack.push(vec![]);
        Ok(())
    }

    pub fn adj_end(&mut self) -> Result<()> {
        if let Some(mut gates) = self.adj_stack.pop() {
            while let Some(gate) = gates.pop() {
                self.push_gate(gate.inverse());
            }
            Ok(())
        } else {
            Err(KetError::InverseScopeEmpty)
        }
    }

    pub fn ctrl_begin(&mut self) -> Result<()> {
        self.adj_ctrl_checks(None)?;
        self.ctrl_stack.push(vec![]);
        self.ctrl_list_is_valid = false;
        Ok(())
    }

    pub fn ctrl_end(&mut self) -> Result<()> {
        self.adj_ctrl_checks(None)?;
        match self.ctrl_stack.pop() {
            Some(stack) => {
                if !stack.is_empty() {
                    Err(KetError::ControlStackNotEmpty)
                } else {
                    self.ctrl_list_is_valid = false;
                    if self.ctrl_stack.is_empty() {
                        Err(KetError::ControlStackRemovePrimary)
                    } else {
                        Ok(())
                    }
                }
            }
            None => Err(KetError::ControlStackRemovePrimary),
        }
    }

    pub fn instructions(&self) -> &[Instruction<LogicalQubit>] {
        &self.logical_circuit.instructions
    }

    pub fn instructions_json(&self) -> String {
        serde_json::to_string(&self.instructions()).unwrap()
    }

    pub fn isa_instructions(&self) -> Option<&[Instruction<PhysicalQubit>]> {
        self.physical_circuit
            .as_ref()
            .map(|c| c.instructions.as_ref())
    }

    pub fn isa_instructions_json(&self) -> String {
        serde_json::to_string(&self.isa_instructions()).unwrap()
    }

    pub fn metadata(&self) -> Metadata {
        Metadata {
            logical_gate_count: self.logical_circuit.gate_count.clone(),
            logical_circuit_depth: self.logical_circuit.depth(),
            physical_gate_count: self
                .physical_circuit
                .as_ref()
                .map(|circuit| circuit.gate_count.clone()),
            physical_circuit_depth: self
                .physical_circuit
                .as_ref()
                .map(|circuit| circuit.depth()),
            allocated_qubits: self.allocated_qubits,
            terminated: self.execution_strategy.is_some(),
            decomposition: self.decomposition_stats.clone(),
        }
    }

    pub fn parameter(&mut self, param: f64) -> Result<usize> {
        if !self.features.gradient {
            return Err(KetError::GradientDisabled);
        }

        let parameter_index = self.gradients.len();
        self.gradients.push(None);
        self.parameters.push(param);

        Ok(parameter_index)
    }

    pub fn gradient(&self, index: usize) -> Option<f64> {
        self.gradients[index]
    }

    pub fn save_sim_state(&self) -> Vec<u8> {
        if let Some(QuantumExecution::Live(simulator)) = self.quantum_execution.as_ref() {
            simulator.save()
        } else {
            vec![]
        }
    }

    pub fn load_sim_state(&mut self, data: &[u8]) {
        if let Some(QuantumExecution::Live(simulator)) = self.quantum_execution.as_mut() {
            simulator.load(data);
        }
    }
}
