// SPDX-FileCopyrightText: 2025 Evandro Chagas Ribeiro da Rosa <evandro@quantuloop.com>
//
// SPDX-License-Identifier: Apache-2.0

use crate::{
    error::{KetError, Result},
    execution::ExecutionProtocol,
    ir::qubit::LogicalQubit,
};

use super::Process;

impl Process {
    pub(super) fn flatten_control_qubits(&mut self) {
        if !self.ctrl_list_is_valid {
            self.ctrl_list = self
                .ctrl_stack
                .last()
                .unwrap()
                .clone()
                .into_iter()
                .flatten()
                .collect();
            self.ctrl_list_is_valid = true;
        }
    }

    pub(super) fn non_gate_checks(
        &mut self,
        qubits: Option<&[LogicalQubit]>,
        feature: bool,
    ) -> Result<()> {
        if !feature {
            Err(KetError::MeasurementDisabled)
        } else if !(self.ctrl_stack.len() == 1 && self.ctrl_stack[0].is_empty()) {
            Err(KetError::ControlledScope)
        } else if !self.adj_stack.is_empty() {
            Err(KetError::InverseScope)
        } else if qubits.is_some_and(|qubits| {
            qubits
                .iter()
                .any(|qubit| !*self.valid_qubit.entry(*qubit).or_insert(true))
        }) {
            Err(KetError::QubitUnavailable)
        } else if self.execution_strategy.is_some() {
            Err(KetError::TerminatedProcess)
        } else {
            Ok(())
        }
    }

    pub(super) fn gate_checks(&mut self, target: LogicalQubit) -> Result<()> {
        if !*self.valid_qubit.entry(target).or_insert(true) {
            Err(KetError::QubitUnavailable)
        } else if self.ctrl_list.contains(&target) {
            Err(KetError::ControlTargetOverlap)
        } else if self.execution_strategy.is_some() {
            Err(KetError::TerminatedProcess)
        } else {
            Ok(())
        }
    }

    pub(super) fn adj_ctrl_checks(&mut self, qubits: Option<&[LogicalQubit]>) -> Result<()> {
        if qubits.is_some_and(|qubits| {
            qubits
                .iter()
                .any(|qubit| !*self.valid_qubit.entry(*qubit).or_insert(true))
        }) {
            Err(KetError::QubitUnavailable)
        } else if qubits
            .is_some_and(|qubits| qubits.iter().any(|qubit| self.ctrl_list.contains(qubit)))
        {
            Err(KetError::ControlTwice)
        } else if self.execution_strategy.is_some() {
            Err(KetError::TerminatedProcess)
        } else {
            Ok(())
        }
    }

    pub(crate) fn execute_after_sample(&self) -> bool {
        match &self.execution_target.execution_protocol {
            ExecutionProtocol::ManagedByTarget { sample, .. } => {
                matches!(sample, crate::execution::Capability::Basic)
            }
            ExecutionProtocol::SampleBased(_) => true,
        }
    }

    pub(crate) fn execute_after_exp_value(&mut self) -> bool {
        match &self.execution_target.execution_protocol {
            ExecutionProtocol::ManagedByTarget { exp_value, .. } => {
                matches!(exp_value, crate::execution::Capability::Basic)
            }
            ExecutionProtocol::SampleBased(Some(_)) => {
                self.features.measure = false;
                self.features.sample = false;
                false
            }
            ExecutionProtocol::SampleBased(None) => unreachable!(),
        }
    }

    pub(crate) fn execute_after_dump(&self) -> bool {
        match &self.execution_target.execution_protocol {
            ExecutionProtocol::ManagedByTarget { dump, .. } => {
                matches!(dump, crate::execution::Capability::Basic)
            }
            ExecutionProtocol::SampleBased(_) => unreachable!(),
        }
    }
}
