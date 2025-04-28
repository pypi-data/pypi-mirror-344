from dataclasses import dataclass
import datetime


@dataclass
class DiatomicMolecule:
    name: str
    electronic_state: str | None = None
    reduced_mass: float | None = None
    Te_cm: float | None = None
    omega_e_cm: float | None = None
    omega_ex_e_cm: float | None = None
    Be_cm: float | None = None
    alpha_e_cm: float | None = None
    De_10em7_cm: float | None = None
    Re_AA: float | None = None
    D0_eV: float | None = None
    IP_eV: float | None = None
    reference: str | None = None
    date_of_reference: datetime.date | None = None

    def __str__(self) -> str:
        string = f'{self.name}'

        if self.electronic_state is not None:
            el_state = self.electronic_state
            el_state = el_state.replace(r'^+', '⁺')
            el_state = el_state.replace(r'^{+}', '⁺')
            el_state = el_state.replace(r'^-', '⁻')
            el_state = el_state.replace(r'^{-}', '⁻')

            el_state = el_state.replace(r'^1', '¹')
            el_state = el_state.replace(r'^2', '²')
            el_state = el_state.replace(r'^3', '³')
            el_state = el_state.replace(r'^4', '⁴')

            el_state = el_state.replace(r'_0', '₀')
            el_state = el_state.replace(r'_1', '₁')
            el_state = el_state.replace(r'_2', '₂')
            el_state = el_state.replace(r'_3', '₃')
        
            el_state = el_state.replace(r'\Sigma', 'Σ')
            el_state = el_state.replace(r'\Pi', 'Π')
            el_state = el_state.replace(r'\Delta', 'Δ')
            el_state = el_state.replace(r'\Phi', 'Φ')
            el_state = el_state.replace(r'$', '')
            el_state = el_state.replace(r' ', '')
            
            state = '(' + el_state + ')'
            string += f' {state:10}'
            # print(f'{el_state:10} replaced {self.electronic_state}',
            #       file=sys.stderr)

        if self.Te_cm is not None:
            string += f' Tₑ = {self.Te_cm:.3f} cm⁻¹'

        if self.Re_AA is not None:
            string += f' Rₑ = {self.Re_AA:.3f} Å'

        return string
