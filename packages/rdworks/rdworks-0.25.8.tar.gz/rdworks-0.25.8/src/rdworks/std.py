import operator
from typing import Tuple, Union

from rdkit import Chem
from rdkit.Chem.MolStandardize import rdMolStandardize


def desalt_smiles(smiles:str) -> Tuple[Union[str, None], Union[Chem.Mol, None]]:
    """Returns (desalted SMILES string, rdkit.Chem.Mol).

    Args:
        smiles (str): input SMILES string.

    Returns:
        Tuple[Union[str, None], Union[Chem.Mol, None]]: (desalted SMILES, desalted rdkit.Chem.Mol)
    """
    mols = []
    for smi in smiles.split("."):
        try:
            rdmol = Chem.MolFromSmiles(smi)
            n = rdmol.GetNumAtoms()
            mols.append((n, smi, rdmol))
        except:
            pass
    if len(mols) > 0:
        # `sorted` function compares the number of atoms first then smiles and rdmol.
        # Comparing smiles string would be okay but comparison of rdmol objects will
        # cause error because comparison operation for Chem.Mol is not supported. 
        # So we need to restrict the key to the number of atoms.
        (n, desalted_smiles, desalted_rdmol) = sorted(mols, key=operator.itemgetter(0), reverse=True)[0]
        return (desalted_smiles, desalted_rdmol)
    else:
        return (None, None)
    

def standardize_smiles(smiles:str) -> str:
    """Returns standardized SMILES string.

    The rdMolStandardize.StandardizeSmiles() function performs the following steps:
    
    1. mol = Chem.MolFromSmiles(sm)
    1. Chem.SanitizeMol(mol)
    1. mol = Chem.RemoveHs(mol)
    1. mol = rdMolStandardize.MetalDisconnector().Disconnect(mol)
    1. mol = rdMolStandardize.Normalize(mol)
    1. mol = rdMolStandardize.Reionize(mol)
    1. Chem.AssignStereochemistry(mol, force=True, cleanIt=True)
    1. Chem.MolToSmiles(mol)
        
    See [rdkit notebook](https://github.com/rdkit/rdkit/blob/master/Docs/Notebooks/MolStandardize.ipynb) and
    [greg's notebook](https://github.com/greglandrum/RSC_OpenScience_Standardization_202104/blob/main/Standardization%20and%20Validation%20with%20the%20RDKit.ipynb),
    and [youtube video](https://www.youtube.com/watch?v=eWTApNX8dJQ).

    Args:
        smiles (str): input SMILES string.

    Returns:
        str: standardized SMILES string.
        
        
    """
    return rdMolStandardize.StandardizeSmiles(smiles)


def standardize(smiles:str) -> Chem.Mol:
    """Returns standardized rdkit.Chem.Mol object.

    Args:
        smiles (str): input SMILES string.

    Returns:
        Chem.Mol: standardized rdkit.Chem.Mol object.
    """
    # follows the steps in
    # https://github.com/greglandrum/RSC_OpenScience_Standardization_202104/blob/main/MolStandardize%20pieces.ipynb
    # as 
    mol = Chem.MolFromSmiles(smiles)
     
    # removeHs, disconnect metal atoms, normalize the molecule, reionize the molecule
    clean_mol = rdMolStandardize.Cleanup(mol) 
     
    # if many fragments, get the "parent" (the actual mol we are interested in) 
    parent_clean_mol = rdMolStandardize.FragmentParent(clean_mol)
         
    # try to neutralize molecule
    uncharger = rdMolStandardize.Uncharger() # annoying, but necessary as no convenience method exists
    uncharged_parent_clean_mol = uncharger.uncharge(parent_clean_mol)
     
    # note that no attempt is made at reionization at this step
    # nor at ionization at some pH (rdkit has no pKa caculator)
    # the main aim to to represent all molecules from different sources
    # in a (single) standard way, for use in ML, catalogue, etc.
     
    te = rdMolStandardize.TautomerEnumerator() # idem
    taut_uncharged_parent_clean_mol = te.Canonicalize(uncharged_parent_clean_mol)
     
    return taut_uncharged_parent_clean_mol


def neutralize_atoms(rdmol:Chem.Mol) -> Chem.Mol:
    """Neutralizes atoms.

    It is adapted from Noel O'Boyle's nocharge code:
    [rdkit cookbook](https://www.rdkit.org/docs/Cookbook.html), 
    [no charge](https://baoilleach.blogspot.com/2019/12/no-charge-simple-approach-to.html).
    It is a neutralization by atom approach and neutralizes atoms with a +1 or -1 charge
    by removing or adding hydrogen where possible. The SMARTS pattern checks for a hydrogen
    in +1 charged atoms and checks for no neighbors with a negative charge (for +1 atoms)
    and no neighbors with a positive charge (for -1 atoms), this is to avoid altering molecules
    with charge separation (e.g., nitro groups).

    The neutralize_atoms() function differs from the rdMolStandardize.Uncharger behavior.
    See the [MolVS documentation for Uncharger](https://molvs.readthedocs.io/en/latest/api.html#molvs-charge).

    > This class uncharges molecules by adding and/or removing hydrogens. 
    In cases where there is a positive charge that is not neutralizable,
    any corresponding negative charge is also preserved. As an example, 
    rdMolStandardize.Uncharger will not change charges on C[N+](C)(C)CCC([O-])=O,
    as there is a positive charge that is not neutralizable. In contrast, the neutralize_atoms()
    function will attempt to neutralize any atoms it can (in this case to C[N+](C)(C)CCC(=O)O).
    That is, neutralize_atoms() ignores the overall charge on the molecule, and attempts to neutralize
    charges even if the neutralization introduces an overall formal charge on the molecule.

    Args:
        rdmol (rdkit.Chem.Mol) : input molecule.

    Returns:
        Chem.Mol: a copy of neutralized rdkit.Chem.Mol object.
    """

    rdmol_ = Chem.Mol(rdmol)
    pattern = Chem.MolFromSmarts("[+1!h0!$([*]~[-1,-2,-3,-4]),-1!$([*]~[+1,+2,+3,+4])]")
    at_matches = rdmol_.GetSubstructMatches(pattern)
    at_matches_list = [y[0] for y in at_matches]
    if len(at_matches_list) > 0:
        for at_idx in at_matches_list:
            atom = rdmol_.GetAtomWithIdx(at_idx)
            chg = atom.GetFormalCharge()
            hcount = atom.GetTotalNumHs()
            atom.SetFormalCharge(0)
            atom.SetNumExplicitHs(hcount - chg)
            atom.UpdatePropertyCache()
    return rdmol_