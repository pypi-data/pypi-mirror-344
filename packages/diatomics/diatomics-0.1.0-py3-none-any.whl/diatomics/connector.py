import csv
import datetime
from dateutil import parser
from pathlib import Path
import sys
from typing import Sequence
from diatomics.diatomic import DiatomicMolecule


def parse_date(date_str: str) -> datetime.date | None:
    """Parse a date string into a datetime object."""
    try:
        date = parser.parse(date_str)
        return date.date()
    except ValueError:
        print(f"Cannot parse the date {date_str}", file=sys.stderr)
        return None

DB_PATH = Path('moleculedata.csv')

def float_or_None(value: str) -> float | None:
    try:
        return float(value)
    except ValueError:
        return None

def get_diatomics() -> Sequence[DiatomicMolecule]:
    raw_diatomics = list()
    with open(DB_PATH, newline='', encoding='latin1') as db_file:
        db_reader = csv.DictReader(db_file)
        for molecule in db_reader:
            raw_diatomics.append(molecule)

    mols = [
        DiatomicMolecule(
            name = raw_mol['Molecule'],
            electronic_state = raw_mol['Electronic state'],
            reduced_mass = float_or_None(raw_mol['Reduced mass']),
            Te_cm = float_or_None(raw_mol['Te (cm^{-1})']),
            omega_e_cm = float_or_None(raw_mol['omega_e (cm^{-1})']),
            omega_ex_e_cm = float_or_None(raw_mol['omega_ex_e (cm^{-1})']),
            Be_cm = float_or_None(raw_mol['Be (cm^{-1})']),
            alpha_e_cm = float_or_None(raw_mol['alpha_e (cm^{-1})']),
            De_10em7_cm = float_or_None(raw_mol['De (10^{-7}cm^{-1})']),
            Re_AA = float_or_None(raw_mol['Re (\\AA)']),
            D0_eV = float_or_None(raw_mol['D0 (eV)']),
            IP_eV = float_or_None(raw_mol['IP (eV)']),
            reference = raw_mol['Reference'],
            date_of_reference = parse_date(raw_mol['Date of reference']),
        )
        for raw_mol in raw_diatomics
    ]
    return  mols
