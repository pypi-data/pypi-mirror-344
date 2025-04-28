# Copyright © 2021-2025 HQS Quantum Simulations GmbH. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License. You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the
# License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing permissions and
# limitations under the License.

"""Qutip interface to spins."""

import qutip as qt
from struqture_py import spins  # type: ignore
from typing import Union, Optional


def _pauli_str_to_matrix(pauli_str: str) -> qt.Qobj:
    """Returns Pauli matrix from index.

    Transform integer to QuTiP Pauli matrix (0 -> qeye(2),
    1 -> sigmax(), 2 -> sigmay(), 3 -> sigmaz())

    Args:
        pauli_str: integer representing the Pauli type of the PauliProduct

    Returns:
        qt.Qobj

    Raises:
        ValueError: if pauli_int not in [0, 1, 2, 3]
    """
    if pauli_str == "I":
        return qt.qeye(2)
    elif pauli_str == "X":
        return qt.sigmax()
    elif pauli_str == "Y":
        return qt.sigmay()
    elif pauli_str == "Z":
        return qt.sigmaz()
    else:
        raise ValueError("pauli_str definition must be int in [I, X, Y, Z]")


def _decoherence_str_to_matrix(decoh_str: str) -> qt.Qobj:
    """Returns Pauli matrix from index.

    Transform integer to QuTiP Pauli matrix (0 -> qeye(2),
    1 -> sigmax(), 2 -> sigmay(), 3 -> sigmaz())

    Args:
        decoh_str: integer representing the Pauli type of the DecoherenceProduct

    Returns:
        qt.Qobj

    Raises:
        ValueError: if pauli_int not in [0, 1, 2, 3]
    """
    if decoh_str == "I":
        return qt.qeye(2)
    elif decoh_str == "X":
        return qt.sigmax()
    elif decoh_str == "iY":
        return qt.sigmay() * 1j
    elif decoh_str == "Z":
        return qt.sigmaz()
    else:
        raise ValueError("decoh_str definition must be int in [I, X, iY, Z]")


class SpinQutipInterface(object):
    """QuTiP interface for PauliHamiltonian objects."""

    @staticmethod
    def pauli_product_to_qutip(
        product: str, number_spins: int, endianess: str = "little"
    ) -> qt.Qobj:
        r"""Returns QuTiP representation of a PauliProduct.

        Args:
            product: the PauliProduct
            number_spins: The total number of spins in the system
            endianess: first qubit to the right (little) or left (big)

        Returns:
            Qobj: The QuTiP representation
        """

        def to_index(index: int) -> int:
            if endianess == "little":
                return number_spins - 1 - index
            elif endianess == "big":
                return index
            else:
                raise ValueError("endianess needs to be either little or big")

        ops = [qt.qeye(2)] * number_spins
        pp = spins.PauliProduct.from_string(str(product))
        for index in pp.keys():
            if index < number_spins:
                ops[to_index(index)] = _pauli_str_to_matrix(pp.get(index))
        return qt.tensor(ops)

    @staticmethod
    def decoherence_product_to_qutip(
        product: str, number_spins: int, endianess: str = "little"
    ) -> qt.Qobj:
        r"""Returns QuTiP representation of a PauliProduct.

        Args:
            product: the PauliProduct
            number_spins: The total number of spins in the system
            endianess: first qubit to the right (little) or left (big)

        Returns:
            Qobj: The QuTiP representation
        """

        def to_index(index: int) -> int:
            if endianess == "little":
                return number_spins - 1 - index
            elif endianess == "big":
                return index
            else:
                raise ValueError("endianess needs to be either little or big")

        ops = [qt.qeye(2)] * number_spins
        dp = spins.DecoherenceProduct.from_string(str(product))
        for index in dp.keys():
            if index < number_spins:
                ops[to_index(index)] = _decoherence_str_to_matrix(dp.get(index))
        return qt.tensor(ops)

    @staticmethod
    def qobj(
        system: Union[spins.PauliHamiltonian, spins.PauliOperator],
        endianess: str = "little",
        number_spins: Optional[int] = None,
    ) -> qt.Qobj:
        r"""Returns a QuTiP representation of a spin system or a spin hamiltonian.

        Args:
            system: The spin based system
            endianess: first qubit to the right (little) or left (big)
            number_spins: optional number of spins in the system

        Returns:
            qt.Qobj: The QuTiP representation of spin based system

        """
        number_qubits: int = (
            system.current_number_spins() if number_spins is None else number_spins
        )
        if number_qubits != 0:
            spin_operator: qt.Qobj = qt.Qobj(
                [[0.0] * 2**number_qubits] * 2**number_qubits,
                dims=[[2 for _ in range(number_qubits)], [2 for _ in range(number_qubits)]],
            )
        else:
            spin_operator = qt.Qobj()
        for key in system.keys():
            coeff: complex = complex(system.get(key))
            spin_operator += coeff * SpinQutipInterface.pauli_product_to_qutip(
                key, number_qubits, endianess=endianess
            )

        return spin_operator


class SpinOpenSystemQutipInterface(object):
    """QuTiP interface for PauliLindbladOpenSystem objects."""

    @staticmethod
    def open_system_to_qutip(
        open_system: Union[spins.PauliLindbladOpenSystem, spins.PauliLindbladNoiseOperator],
        endianess: str = "little",
        number_spins: Optional[int] = None,
    ) -> qt.Qobj:
        r"""Returns QuTiP representation of an PauliLindbladOpenSystem.

        This function can also be used to convert mu matrices from the NoiseModel.
        The inputs are then:
            open_system = Tuple[System = the system the NoiseModel is run on,
                                Dict = NoiseModel(circuit, calc).mu_matrix]

        Args:
            open_system: the LindbladOpenSystem considered (here, a PauliLindbladOpenSystem)
            endianess: first qubit to the right (little) or left (big)
            number_spins: optional number of spins in the system

        Returns:
            Qobj: The QuTiP representation
        """

        def lind_dis(An: qt.Qobj, Am: qt.Qobj) -> qt.Qobj:
            """Creates the Lindblad dissipator term from two operators.

            Args:
                An: first QuTiP quantum object for the Lindblad dissipator
                Am: second QuTiP quantum object for the Lindblad dissipator

            Returns:
                qt.Qobj
            """
            # uses column major
            return (
                qt.sprepost(An, Am.dag())
                - 0.5 * qt.spre(Am.dag() * An)
                - 0.5 * qt.spost(Am.dag() * An)
            )

        def coherent_hamiltonian(coherent: qt.Qobj) -> qt.Qobj:
            """Creates the coherent part of the Lindblad equation from the given Hamiltonian.

            Args:
                coherent: the Hamiltonian to be turned into the closed part of the Lindblad

            Returns:
                qt.Qobj

            Raises:
                TypeError: Coherent part of the Hamiltonian cannot be converted to QuTiP
            """
            if isinstance(coherent, qt.Qobj):
                hamiltonian = -1j * (qt.spre(coherent) - qt.spost(coherent))
            elif coherent == 0:
                hamiltonian = 0
            else:
                raise TypeError("Coherent part of the Hamiltonian cannot be converted to QuTiP")
            return hamiltonian

        try:
            system = open_system.system()
            noise = open_system.noise()
            number_qubits = (
                max(system.current_number_spins(), noise.current_number_spins())
                if number_spins is None
                else number_spins
            )
        except AttributeError:
            number_qubits = (
                open_system.current_number_spins() if number_spins is None else number_spins
            )
            system = {}
            noise = open_system

        coherent_part = 0
        noisy_part = 0

        for pp in system.keys():
            pp_qt = SpinQutipInterface.pauli_product_to_qutip(pp, number_qubits, endianess)
            key_qt = system.get(key=pp)
            coherent_part += complex(key_qt) * pp_qt
        coherent_part = coherent_hamiltonian(coherent_part)

        for A_n, A_m in noise.keys():
            spin_op_1 = SpinQutipInterface.decoherence_product_to_qutip(
                A_n, number_qubits, endianess
            )
            spin_op_2 = SpinQutipInterface.decoherence_product_to_qutip(
                A_m, number_qubits, endianess
            )
            try:
                h_nm_value = noise.get(key=(str(A_n), str(A_m)))
            except AttributeError:
                h_nm_value = noise.get((A_n, A_m))
            noisy_part += complex(h_nm_value) * lind_dis(spin_op_1, spin_op_2)

        return (coherent_part, noisy_part)
