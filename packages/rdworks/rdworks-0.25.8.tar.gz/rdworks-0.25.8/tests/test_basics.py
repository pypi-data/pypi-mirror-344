from pathlib import Path
from rdkit import Chem

import rdworks
import rdworks.autograph
import math
import copy
import numpy as np


datadir = Path(__file__).parent.resolve() / "data"
workdir = Path(__file__).parent.resolve() / "outfiles"

workdir.mkdir(exist_ok=True)


# python >=3.12 raises SyntaxWarning: invalid escape sequence
# To address this warning in general, we can make the string literal a raw string literal r"...". 
# Raw string literals do not process escape sequences. 
# For example, r"\n" is treated simply as the characters \ and n and not as a newline escape sequence.
drug_smiles = [
    "Fc1cc(c(F)cc1F)C[C@@H](N)CC(=O)N3Cc2nnc(n2CC3)C(F)(F)F", # [0]
    r"O=C(O[C@@H]1[C@H]3C(=C/[C@H](C)C1)\C=C/[C@@H]([C@@H]3CC[C@H]2OC(=O)C[C@H](O)C2)C)C(C)(C)CC",
    "C[C@@H](C(OC(C)C)=O)N[P@](OC[C@@H]1[C@H]([C@@](F)([C@@H](O1)N2C=CC(NC2=O)=O)C)O)(OC3=CC=CC=C3)=O",
    "C1CNC[C@H]([C@@H]1C2=CC=C(C=C2)F)COC3=CC4=C(C=C3)OCO4",
    "CC1=C(C=NO1)C(=O)NC2=CC=C(C=C2)C(F)(F)F",
    "CN1[C@@H]2CCC[C@H]1CC(C2)NC(=O)C3=NN(C4=CC=CC=C43)C", # [5] - Granisetron
    "CCCN1C[C@@H](C[C@H]2[C@H]1CC3=CNC4=CC=CC2=C34)CSC",
    "CCC1=C(NC2=C1C(=O)C(CC2)CN3CCOCC3)C", # [7] Molidone
    r"C[C@H]1/C=C/C=C(\C(=O)NC2=C(C(=C3C(=C2O)C(=C(C4=C3C(=O)[C@](O4)(O/C=C/[C@@H]([C@H]([C@H]([C@@H]([C@@H]([C@@H]([C@H]1O)C)O)C)OC(=O)C)C)OC)C)C)O)O)/C=N/N5CCN(CC5)C)/C",
    r"C=CC1=C(N2[C@@H]([C@@H](C2=O)NC(=O)/C(=N\O)/C3=CSC(=N3)N)SC1)C(=O)O",
    "CC1=C(N=CN1)CSCCNC(=NC)NC#N", # [10] - Cimetidine
    """C1=C(N=C(S1)N=C(N)N)CSCC/C(=N/S(=O)(=O)N)/N""",
    "C1CC(CCC1C2=CC=C(C=C2)Cl)C3=C(C4=CC=CC=C4C(=O)C3=O)O",
    "CN(CC/C=C1C2=CC=CC=C2SC3=C/1C=C(Cl)C=C3)C",
    "CN(C)CCCN1C2=CC=CC=C2CCC3=C1C=C(C=C3)Cl",
    "CN1CCCC(C1)CC2C3=CC=CC=C3SC4=CC=CC=C24", # [15] - Methixene
    "CCN(CC)C(C)CN1C2=CC=CC=C2SC3=CC=CC=C31",
    "CC(=O)OC1=CC=CC=C1C(=O)O",
    "C1=CC(=C(C=C1F)F)C(CN2C=NC=N2)(CN3C=NC=N3)O",
    "CC(=O)NC[C@H]1CN(C(=O)O1)C2=CC(=C(C=C2)N3CCOCC3)F", # [19]
    ]

drug_names = [
    "Sitagliptin", "Simvastatin", "Sofosbuvir", "Paroxetine", "Leflunomide",
    "Granisetron", "Pergolide", "Molindone", "Rifampin", "Cefdinir",
    "Cimetidine", "Famotidine", "Atovaquone", "Chlorprothixene", "Clomipramine",
    "Methixene",  "Ethopropazine", "Aspirin", "Fluconazole", "Linezolid",
    ]

# Lahey, S.-L. J., Thien Phuc, T. N. & Rowley, C. N. 
# Benchmarking Force Field and the ANI Neural Network Potentials for the 
# Torsional Potential Energy Surface of Biaryl Drug Fragments. 
# J. Chem. Inf. Model. 60, 6258–6268 (2020)

torsion_dataset_smiles = [
    "C1(C2=CC=CN2)=CC=CC=C1",
    "C1(C2=NC=CN2)=CC=CC=C1",
    "C1(N2C=CC=C2)=NC=CC=N1",
    "C1(C2=NC=NC=N2)=CC=CC=C1",
    "C1(N2C=CC=C2)=CC=CC=C1",
    "O=C(N1)C=CC=C1C2=COC=C2",
    "C1(C2=NC=CC=N2)=NC=CC=N1",
    "O=C(N1)C=CC=C1C2=NC=CN2",
    ]

torsion_dataset_names=["07", "09","20", "39", "10", "23", "12", "29"]


def test_init_mol():
    mol = rdworks.Mol(drug_smiles[0], drug_names[0])
    assert mol.count() == 0
    assert mol.name == drug_names[0]
    rdmol = Chem.MolFromSmiles(drug_smiles[0])
    rdmol.SetProp('_Name', drug_names[0])
    mol = rdworks.Mol(rdmol, drug_names[0])
    assert mol.rdmol.GetProp('_Name') == drug_names[0]
    assert mol.name == drug_names[0]


def test_init_mollibr():
    libr = rdworks.MolLibr(drug_smiles[:5], drug_names[:5])
    assert libr.count() == 5
    libr = rdworks.MolLibr([Chem.MolFromSmiles(_) for _ in drug_smiles[5:10]], drug_names[5:10])
    assert libr.count() == 5
    libr = rdworks.MolLibr([rdworks.Mol(smi,name) for smi,name in zip(drug_smiles[10:15], drug_names[10:15])])
    assert libr.count() == 5


def test_operators():
    libr = rdworks.MolLibr(drug_smiles, drug_names)
    other = rdworks.MolLibr(drug_smiles[5:10], drug_names[5:10])
    assert libr.count() == 20
    assert other.count() == 5
    assert libr[10] == rdworks.Mol("CC1=C(N=CN1)CSCCNC(=NC)NC#N")
    assert (libr + other).count() == 25
    assert (libr - other).count() == 15
    assert (libr & other).count() == 5
    assert libr.count() == 20 # libr object is not changed
    libr += other
    assert libr.count() == 25


def test_copy():
    libr1 = rdworks.MolLibr(drug_smiles[:5], drug_names[:5])
    for i in range(5):
        libr1.libr[i].rdmol.SetProp("_Name", f"_Name_{i}")
        libr1.libr[i].rdmol.SetProp("Property", f"Property_{i}")
    libr2 = copy.deepcopy(libr1) # copied
    for i in range(5):
        assert libr2.libr[i].rdmol.GetProp("_Name") == f"_Name_{i}"
        assert libr2.libr[i].rdmol.GetProp("Property") == f"Property_{i}"
        assert libr1.libr[i].smiles == libr2.libr[i].smiles


def test_unique():
    libr = rdworks.MolLibr(
        drug_smiles[:3] + ["N[C@@H](CC(=O)N1CCN2C(C1)=NN=C2C(F)(F)F)CC1=CC(F)=C(F)C=C1F"], 
        drug_names[:3] + ["Januvia"])
    libr_unique = libr.unique()
    assert libr_unique.count() == 3
    assert libr_unique[0].props['aka'] == ['Januvia']


def test_nn_applicable():
    libr = rdworks.MolLibr(drug_smiles, drug_names)
    libr_subset = libr.nn_applicable('ANI-2x', progress=False)
    assert libr_subset.count() == 19


def test_qed():
    libr = rdworks.MolLibr(drug_smiles[:3], drug_names[:3]).qed(progress=False)
    assert math.isclose(libr[0].props['MolWt'], 407.318, rel_tol=1.0e-6, abs_tol=1.0e-3)
    assert math.isclose(libr[0].props['QED'], 0.62163, rel_tol=1.0e-6, abs_tol=1.0e-3)
    # calculate all available descriptors:
    # "MolWt", "TPSA", "LogP", "HBA", "HBD", "QED", "LipinskiHBA", "LipinskiHBD",
    # "HAC", "RotBonds", "RingCount", "Hetero", "FCsp3"
    libr = rdworks.MolLibr(drug_smiles, drug_names).qed(
        properties=[k for k in rdworks.rd_descriptor_f], 
        progress=False)              

   
def test_drop():
    libr = rdworks.MolLibr(drug_smiles, drug_names, progress=False)
    not_druglike_names = ['Sofosbuvir','Rifampin','Cefdinir','Famotidine','Atovaquone','Chlorprothixene','Methixene','Ethopropazine']
    cnsmpo_compliant_names = ['Sitagliptin','Simvastatin','Paroxetine','Leflunomide','Granisetron','Molindone','Cimetidine','Fluconazole','Linezolid']

    obj = libr.drop()

    obj = libr.drop('ZINC_druglike')
    assert obj.count() == 8
    assert set([_.name for _ in obj]) == set(not_druglike_names)
    
    obj = libr.drop('~ZINC_druglike')       
    assert obj.count() == 12
    assert set([_.name for _ in obj]) == set(drug_names)-set(not_druglike_names)
    
    # Keep CNS compliant compounds
    # Below three drop() functions have the same effect
    # and obj1, obj2, and obj3 should be identical
    obj1 = libr.drop('CNS', invert=True)
    assert obj1.count() == 9
    assert set([_.name for _ in obj1]) == set(cnsmpo_compliant_names)

    obj2 = libr.drop('~CNS')
    assert obj2.count() == 9
    assert set([_.name for _ in obj2]) == set(cnsmpo_compliant_names)
    
    obj3 = libr.drop(datadir / 'cns.xml', invert=True)
    assert obj3.count() == 9
    assert set([_.name for _ in obj3]) == set(cnsmpo_compliant_names)
        

def test_similar():
    libr = rdworks.MolLibr(drug_smiles, drug_names, progress=False)
    query = rdworks.Mol('[H][C@@]1(CC[C@]([H])(C2=C(F)C=C(F)C(F)=C2)[C@@]([H])(N)C1)N1CCN2C(C1)=NN=C2C(F)(F)F', 'DB07072')
    assert libr.similar(query, threshold=0.2).count() == 1
    query = libr[15] # Methixene
    sim = libr.similar(query, threshold=0.2)
    sim_expected = ['Pergolide', 'Methixene', 'Ethopropazine']
    sim_names = [_.name for _ in sim]
    assert set(sim_names) == set(sim_expected)


def test_merge_csv():
    libr = rdworks.MolLibr(drug_smiles, drug_names)
    libr = rdworks.merge_csv(libr, datadir / "drugs_20.csv", on='name')
    libr.to_csv(workdir / "test_merge_csv.csv")
    assert libr.count() == 20


def test_read_smi():
    libr1 = rdworks.read_smi(datadir / "cdk2.smi", progress=False)
    assert libr1.count() == 47, "failed to read .smi file"
    libr2 = rdworks.read_smi(datadir / "cdk2.smi.gz", progress=False)
    assert libr2.count() == 47, "failed to read .smi.gz file"
    assert libr1 == libr2


def test_read_sdf():
    libr1 = rdworks.read_sdf(datadir / "cdk2.sdf", progress=False)
    assert libr1.count() == 47, "failed to read .sdf file"
    libr2 = rdworks.read_sdf(datadir / "cdk2.sdf.gz", progress=False)
    assert libr2.count() == 47, "failed to read .sdf.gz file"
    assert libr1 == libr2


def test_mae_to_dict():
    d = rdworks.mae_to_dict(datadir / "ligprep-SJ506rev-out.mae")
    print(len(d))

    i = 0 # molecule index
    for molecule in d:
        print(molecule['f_m_ct']['i_epik_Tot_Q'])
        print(molecule['f_m_ct']['r_epik_Population'])
        print(molecule['f_m_ct']['s_epik_macro-pKa'])

    while True:
        try:
            data = []
            basic_pKa = []
            acidic_pKa = []
            for iv, (v, dv) in enumerate(zip(
                d[i]['f_m_ct']['m_atom']['r_epik_H2O_pKa'], 
                d[i]['f_m_ct']['m_atom']['r_epik_H2O_pKa_uncertainty'])):
                try:
                    pKa = float(v) # empty value = <>
                    dpKa = float(dv) # empty value = <>
                    print(iv, pKa, dpKa)
                except:
                    continue
                atomic_number = int(d[i]['f_m_ct']['m_atom']['i_m_atomic_number'][iv])
                formal_charge = int(d[i]['f_m_ct']['m_atom']['i_m_formal_charge'][iv])
                if atomic_number != 1 and pKa >= 5.0: # basic
                    basic_pKa.append(pKa)
                if atomic_number == 1 and pKa <= 9.0: # acidic (already protonated by Epik)
                    acidic_pKa.append(pKa)
                # data.append(pKa)
                print(iv+1, atomic_number, formal_charge, pKa, "basic=", basic_pKa, "acidic=", acidic_pKa)
            if basic_pKa :
                molecule_pKa = max(basic_pKa)
            elif acidic_pKa:
                molecule_pKa = min(acidic_pKa)
            else:
                molecule_pKa = 8.81
            print("Row=",i+1, "pKa=", molecule_pKa, data, "basic=", basic_pKa, "acidic=", acidic_pKa)
            # print()
            i += 1
        except:
            break


def test_read_mae():
    libr = rdworks.read_mae(datadir / "ligprep-SJ506rev-out.mae")
    print(libr.count())


def test_to_csv():
    libr1 = rdworks.MolLibr(drug_smiles, drug_names, progress=False)
    libr1.qed(progress=False).to_csv(workdir / "test_to_csv.csv")
    libr2 = rdworks.read_csv(workdir / "test_to_csv.csv", smiles='smiles', name='name', progress=False)
    assert libr1 == libr2


def test_to_smi():
    libr = rdworks.MolLibr(drug_smiles, drug_names, progress=False)
    libr.to_smi(workdir / "test_to_smi.smi.gz")
    libr.to_smi(workdir / "test_to_smi.smi")

   
def test_to_sdf():
    libr = rdworks.MolLibr(drug_smiles, drug_names, progress=False)
    libr.to_sdf(workdir / "test_to_sdf.sdf.gz")
    libr.to_sdf(workdir / "test_to_sdf.sdf")
    libr.qed().to_sdf(workdir / "test_to_sdf_with_qed.sdf") # QED and other properties should be here
    supp = Chem.SDMolSupplier(workdir / "test_to_sdf_with_qed.sdf")
    for m, mol in zip(supp, libr):
        assert math.isclose(float(m.GetProp('MolWt')), 
                            mol.props['MolWt'], rel_tol=1.0e-6, abs_tol=1.0e-3)
        assert math.isclose(float(m.GetProp('QED')), 
                            mol.props['QED'], rel_tol=1.0e-6, abs_tol=1.0e-3)


def test_to_png():
    libr = rdworks.MolLibr(drug_smiles, drug_names, progress=False)
    libr.to_png(workdir / "test_to_png.png")
    libr.to_png(workdir / "test_to_png_with_index.png", index=True)


def test_to_svg():
    libr = rdworks.MolLibr(drug_smiles, drug_names, progress=False)
    with open(workdir / "test_to_svg.svg", "w") as svg:
        svg.write(libr.to_image())
    head = libr.to_image()[:100]
    assert head.startswith('<?xml') and ("<svg" in head)


def test_expand_rgroup():
    X = ["[*]C#N", "[*]C(O)=O", "[*]CO", "[*]COC", "[*]C(NC)=O", "[*]CNC(C)=O", "[*]CC=C", "[*][H]" ] # (8)
    Y = ["[*][H]", "[*]O", "[*]OC", "[*]CC(F)(F)F", "[*]OCCOC"] # (5)
    core = "[*:1]-c1ccc2ccn(-[*:2])c2c1"
    libr = rdworks.expand_rgroup(core=core, r={1:X, 2:Y}, prefix='RGX', progress=False)
    assert libr.count() == 40 # 8x5


def test_scaffold_tree():
    libr = rdworks.MolLibr(drug_smiles[:4], drug_names[:4])
    for mol in libr:
        adhoc_libr = rdworks.MolLibr(rdworks.scaffold_tree(mol.rdmol)).rename(prefix=mol.name)
        adhoc_libr.to_png(workdir / f'unittest_84_{mol.name}.png')


def test_MatchedSeries():
    # https://greglandrum.github.io/rdkit-blog/posts/2023-01-09-rgd-tutorial.html
    X = ["[*]C#N", "[*]C(O)=O", "[*]CO", "[*]COC", "[*]C(NC)=O", "[*]CNC(C)=O", "[*]CC=C", "[*][H]" ] # (8)
    Y = ["[*][H]", "[*]O", "[*]OC", "[*]CC(F)(F)F", "[*]OCCOC"] # (5)
    core = "[*:1]-c1ccc2ccn(-[*:2])c2c1"
    libr = rdworks.expand_rgroup(core=core, r={1:X, 2:Y}, prefix='RGX', progress=False)
    series = rdworks.MatchedSeries(libr, sort_props=['QED','HAC'])
    assert series.count() == 10


def test_complete_tautomers():
    m = rdworks.Mol("Oc1c(cccc3)c3nc2ccncc12", "tautomer")
    libr = rdworks.complete_tautomers(m)
    assert libr.count() == 3
    expected_names = ['tautomer.1','tautomer.2','tautomer.3']
    names = [_.name for _ in libr]
    assert names == expected_names
    expected_canonical_smiles = [
        'O=c1c2c[nH]ccc-2nc2ccccc12',
        'O=c1c2ccccc2[nH]c2ccncc12',
        'Oc1c2ccccc2nc2ccncc12',
        ]
    canonical_smiles = [_.smiles for _ in libr]
    difference = set(expected_canonical_smiles) - set(canonical_smiles)
    assert len(difference) == 0


def test_remove_stereo():
    m = rdworks.Mol("C/C=C/C=C\\C", "double_bond")
    assert m.remove_stereo().smiles == "CC=CC=CC"


def test_complete_stereoisomers():
    m = rdworks.Mol("CC=CC", "double_bond")
    assert m.is_stereo_specified() is False, "double bond stereo is not properly handled"
    libr = rdworks.complete_stereoisomers(m)
    assert libr.count() == 2, "cis and trans are expected"
    assert all([_.is_stereo_specified() for _ in libr])
    expected_canonical_smiles = [r'C/C=C/C', r'C/C=C\C']
    canonical_smiles = [_.smiles for _ in libr]
    difference = set(expected_canonical_smiles) - set(canonical_smiles)
    assert len(difference) == 0

    # 0 out of 3 atom stereocenters is specified
    m = rdworks.Mol("N=C1OC(CN2CC(C)OC(C)C2)CN1", "stereoisomer")
    assert m.is_stereo_specified() is False
    libr = rdworks.complete_stereoisomers(m)
    assert libr.count() == 6, "0 out of 3 atom stereocenters is specified"
    assert all([_.is_stereo_specified() for _ in libr])
    expected_names = [f'stereoisomer.{i}' for i in [1,2,3,4,5,6]]
    names = [_.name for _ in libr]
    assert names == expected_names
    expected_canonical_smiles = [
        'C[C@@H]1CN(C[C@@H]2CNC(=N)O2)C[C@H](C)O1',
        'C[C@@H]1CN(C[C@H]2CNC(=N)O2)C[C@H](C)O1',
        'C[C@@H]1CN(C[C@@H]2CNC(=N)O2)C[C@@H](C)O1',
        'C[C@@H]1CN(C[C@H]2CNC(=N)O2)C[C@@H](C)O1',
        'C[C@H]1CN(C[C@@H]2CNC(=N)O2)C[C@H](C)O1',
        'C[C@H]1CN(C[C@H]2CNC(=N)O2)C[C@H](C)O1',
        ]
    canonical_smiles = [_.smiles for _ in libr]
    difference = set(expected_canonical_smiles) - set(canonical_smiles)
    assert len(difference) == 0
    
    # 1 out of 3 atom stereocenters is specified
    m = rdworks.Mol("N=C1OC(CN1)CN2CC(O[C@H](C2)C)C", "stereoisomer") 
    assert m.is_stereo_specified() is False
    libr = rdworks.complete_stereoisomers(m)
    assert libr.count() == 4, "1 out of 3 atom stereocenters is specified"
    assert all([_.is_stereo_specified() for _ in libr])
    expected_names = [f'stereoisomer.{i}' for i in [1,2,3,4]]
    names = [_.name for _ in libr]
    assert names == expected_names
    expected_canonical_smiles = [
        'C[C@@H]1CN(C[C@@H]2CNC(=N)O2)C[C@H](C)O1',
        'C[C@@H]1CN(C[C@H]2CNC(=N)O2)C[C@H](C)O1',
        'C[C@H]1CN(C[C@@H]2CNC(=N)O2)C[C@H](C)O1',
        'C[C@H]1CN(C[C@H]2CNC(=N)O2)C[C@H](C)O1',
        ]
    canonical_smiles = [_.smiles for _ in libr]
    difference = set(expected_canonical_smiles) - set(canonical_smiles)
    assert len(difference) == 0

    # 2 out of 3 atom stereocenters are specified
    m = rdworks.Mol("N=C1OC(CN1)CN2C[C@H](O[C@H](C2)C)C", "stereoisomer") 
    assert m.is_stereo_specified() is False
    libr = rdworks.complete_stereoisomers(m)
    assert libr.count() == 2, "2 out of 3 atom stereocenters is specified"
    assert all([_.is_stereo_specified() for _ in libr])
    expected_names = [f'stereoisomer.{i}' for i in [1,2]]
    names = [_.name for _ in libr]
    assert names == expected_names
    expected_canonical_smiles = ['C[C@@H]1CN(C[C@@H]2CNC(=N)O2)C[C@H](C)O1',
                                    'C[C@@H]1CN(C[C@H]2CNC(=N)O2)C[C@H](C)O1',
                                    ]
    canonical_smiles = [_.smiles for _ in libr]
    difference = set(expected_canonical_smiles) - set(canonical_smiles)
    assert len(difference) == 0
    
    # 3 out of 3 atom stereocenters are specified
    m = rdworks.Mol("N=C1O[C@@H](CN1)CN2C[C@H](O[C@H](C2)C)C", "stereoisomer") 
    assert m.is_stereo_specified() is True
    libr = rdworks.complete_stereoisomers(m)
    assert libr.count() == 1, "3 out of 3 atom stereocenters is specified"
    assert all([_.is_stereo_specified() for _ in libr])
    expected_names = [f'stereoisomer']
    names = [_.name for _ in libr]
    assert names == expected_names
    expected_canonical_smiles = ['C[C@@H]1CN(C[C@@H]2CNC(=N)O2)C[C@H](C)O1']
    canonical_smiles = [_.smiles for _ in libr]
    difference = set(expected_canonical_smiles) - set(canonical_smiles)
    assert len(difference) == 0

    # for 20 molecules
    isomer_libr = rdworks.MolLibr()
    for mol in rdworks.MolLibr(drug_smiles, drug_names):
        isomer_libr += rdworks.complete_stereoisomers(mol)
    assert isomer_libr.count() >= 25
   

def test_cluster():
    libr = rdworks.read_smi(datadir / "cdk2.smi.gz", progress=False)
    assert libr.count() == 47
    clusters = libr.cluster(threshold=0.3)
    assert isinstance(clusters, list)
    assert len(clusters) == 3


def test_align_and_cluster_confs():
    mol = rdworks.Mol("N=C1O[C@@H](CN1)CN2C[C@H](O[C@H](C2)C)C", "stereoisomer")
    mol = mol.make_confs()
    mol = mol.drop_confs(similar=True, similar_rmsd=0.5, window=15.0)
    mol = mol.sort_confs().align_confs().cluster_confs().rename()
    mol.to_sdf(confs=True) # string output


def test_autograph():
    N = 50
    upper_triangle_values = 5.0 *np.random.rand(N*(N-1)//2)
    rmsdMatrix = rdworks.utils.convert_triu_to_symm(upper_triangle_values)
    com, cen = rdworks.autograph.NMRCLUST(rmsdMatrix)
    assert len(com) == N
    assert len(set(com)) == len(cen)
    
    com, cen = rdworks.autograph.DynamicTreeCut(rmsdMatrix)
    assert len(com) == N
    assert len(set(com)) == len(cen)
    
    com, cen = rdworks.autograph.RCKmeans(rmsdMatrix)
    assert len(com) == N
    assert len(set(com)) == len(cen)

    com, cen  = rdworks.autograph.AutoGraph(rmsdMatrix)
    assert len(com) == N
    assert len(set(com)) == len(cen)


def test_make_confs():
    mol = rdworks.Mol("N=C1O[C@@H](CN1)CN2C[C@H](O[C@H](C2)C)C", "stereoisomer")
    mol = mol.make_confs(method='RDKit_ETKDG')
    assert mol.count() > 1
    mol = mol.make_confs(method='CDPL_ConForge')
    assert mol.count() > 1


def test_optimize():
    mol = rdworks.Mol("N=C1O[C@@H](CN1)CN2C[C@H](O[C@H](C2)C)C", "stereoisomer")
    mol = mol.make_confs()
    mol = mol.optimize(calculator='MMFF94')


def test_torsion_energies():
    libr = rdworks.MolLibr(torsion_dataset_smiles, torsion_dataset_names)
    with open(workdir / 'test_torsion_energies.html', 'w') as f:
        for mol in libr:
            mol = mol.make_confs().drop_confs(similar=True, similar_rmsd=0.3).sort_confs().rename()
            mol = mol.optimize(calculator='MMFF94')
            mol = mol.torsion_energies(calculator='MMFF94', interval=15)
            f.write(mol.to_html())
            print(mol.serialize('torsion', decimal_places=2))


def test_workflow():
    state_mol = rdworks.Mol('Cc1nc2cc(Cl)nc(Cl)c2nc1C', 'A-1250')
    state_mol = state_mol.make_confs(method='RDKit_ETKDG').optimize(calculator='MMFF94')
    state_mol = state_mol.rename() # rename conformers
    state_mol = state_mol.drop_confs(similar=True, similar_rmsd=0.3)
    state_mol = state_mol.sort_confs().rename()
    state_mol = state_mol.align_confs(method='rigid_fragment')
    state_mol = state_mol.cluster_confs('QT', threshold=1.0, sortby='energy')
    print(state_mol.name, {k:v for k,v in state_mol.props.items()})
    for conf in state_mol.confs:
        conf.props = rdworks.fix_decimal_places_in_dict(conf.props, decimal_places=2)
        print(conf.name, {k:v for k,v in conf.props.items()})