import csv
import datetime
from dateutil import parser
import importlib.resources
import os
from pathlib import Path
import subprocess
import sys
from typing import Sequence

from diatomics.diatomic import DiatomicMolecule


DATABASE_URL: str ="https://rios.mp.fhi.mpg.de/export_table.php"
MOLECULE_DATA: str = "moleculedata.csv"


def get_database_path() -> Path:
    with importlib.resources.path("diatomics") as home:
        return Path(home / "data" / MOLECULE_DATA)

    
def refresh_database():
    """ TODO: work in progress """
    # Get the appropriate data directory using XDG spec when available
    if os.environ.get('XDG_DATA_HOME'):
        # Use XDG_DATA_HOME if defined (Linux)
        base_dir = Path(os.environ['XDG_DATA_HOME'])
    else:
        # macOS fallback: ~/Library/Application Support
        # Linux fallback: ~/.local/share
        if os.path.exists(str(Path.home() / "Library")):
            base_dir = Path.home() / "Library" / "Application Support"
        else:
            base_dir = Path.home() / ".local" / "share"
    
    # Create application-specific directory using the package name
    data_dir = base_dir / "diatomics" / "data"
    
    # Create the directory if it doesn't exist
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Full path to the file
    file_path = data_dir / MOLECULE_DATA
    
    # Check if the file already exists
    if file_path.exists():
        return file_path
    
    # If file doesn't exist, download it
    try:
        subprocess.run(
            [
                "wget",
                "--trust-server-names",
                DATABASE_URL,
                "-O", str(file_path)
            ],
            check=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"Error downloading file: {e}", file=sys.stderr)
        print(f"stderr: {e.stderr.decode()}", file=sys.stderr)
        raise
    
    return file_path


def parse_date(date_str: str) -> datetime.date | None:
    """Parse a date string into a datetime object."""
    try:
        date = parser.parse(date_str)
        return date.date()
    except ValueError:
        print(f"Cannot parse the date {date_str}", file=sys.stderr)
        return None


def float_or_None(value: str) -> float | None:
    try:
        return float(value)
    except ValueError:
        return None


def get_diatomics() -> Sequence[DiatomicMolecule]:
    raw_diatomics = list()
    try:
        db_path = get_database_path()
    except:
        print(
            "Cannot access the database."
            " Local file unavailable or online download failed.",
            file=sys.stderr
        )
        raise

    with open(db_path, newline='', encoding='latin1') as db_file:
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
