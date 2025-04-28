import argparse
from diatomics.connector import get_diatomics


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('atoms', nargs='+', type=str)
    args = parser.parse_args()

    if len(args.atoms) > 2:
        print(
            f'No diatomic molecules containing {', '.join(args.atoms)} found.'
        )
        return
    
    atom = args.atoms[0]
    if len(args.atoms) > 1:
        mota = args.atoms[1]
    else:
        mota = None
    
    msg = f"Searching for molecules containing {atom}"
    msg += f" and {mota}." if mota else "."
    print(msg)

    diatomics = get_diatomics()

    for mol in diatomics:
        if atom in mol.name:
            if mota is None:
                print(mol)
            elif mota in mol.name:
                print(mol)
