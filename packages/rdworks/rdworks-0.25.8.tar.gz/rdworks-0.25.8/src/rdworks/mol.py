import io
import copy
import pathlib
import itertools
import json
import logging
import tempfile

from collections import defaultdict
from collections.abc import Callable
from pathlib import Path
from typing import Iterator, Self

import numpy as np
import pandas as pd
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import seaborn as sns

import CDPL
import CDPL.Chem
import CDPL.ConfGen

from rdkit import Chem, DataStructs

from rdkit.Chem import ( 
    rdMolDescriptors, AllChem, Descriptors, QED, 
    rdFingerprintGenerator,
    Draw, rdDepictor,
    rdDistGeom, rdMolAlign, rdMolTransforms, rdmolops
    )

from rdkit.Chem.Draw import rdMolDraw2D

from rdkit.ML.Cluster import Butina

from rdworks.std import desalt_smiles, standardize
from rdworks.xml import list_predefined_xml, get_predefined_xml, parse_xml
from rdworks.scaffold import rigid_fragment_indices
from rdworks.descriptor import rd_descriptor, rd_descriptor_f
from rdworks.display import svg
from rdworks.utils import convert_tril_to_symm, QT, fix_decimal_places_in_dict
from rdworks.units import ev2kcalpermol
from rdworks.autograph import NMRCLUST, DynamicTreeCut, RCKmeans, AutoGraph
from rdworks.bitqt import BitQT
from rdworks.conf import Conf


main_logger = logging.getLogger()


class Mol:
    """Container for molecular structure, conformers, and other information.
    """

    MFP2 = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)
    
    ETKDG_params = rdDistGeom.ETKDGv3()
    ETKDG_params.useSmallRingTorsions = True
    ETKDG_params.maxIterations = 2000
        

    def __init__(self, 
                 molecular_input: str | Chem.Mol, 
                 name:str='', 
                 std:bool=False,
                 max_workers:int=1,
                 chunksize:int=4,
                 progress:bool=False) -> None:
        """Create a rdworks.Mol object.

        Examples:
            >>> import rdworks
            >>> m = rdworks.Mol('c1ccccc1', name='benzene')
            
        Args:
            molecular_input (str | Chem.Mol): SMILES or rdkit.Chem.Mol object
            name (str, optional): name of the molecule. Defaults to ''.
            std (bool, optional): whether to standardize the molecule. Defaults to False.

        Raises:
            ValueError: Invalid SMILES or rdkit.Chem.Mol object.
            TypeError: No SMILES or rdkit.Chem.Mol object is provided.
            RuntimeError: Desalting or standardization process failed.
        """

        self.rdmol = None # rdkit.Chem.Mol object
        self.smiles = None # isomeric SMILES
        self.name = None
        self.props = {}
        self.confs = [] # 3D conformers (iterable)
        self.fp = None
        self.max_workers = max_workers
        self.chunksize = chunksize
        self.progress = progress
        
        if isinstance(molecular_input, str):
            try:
                self.rdmol = Chem.MolFromSmiles(molecular_input)
                assert self.rdmol
                self.smiles = Chem.MolToSmiles(self.rdmol)
            except:
                raise ValueError(f'Mol() received invalid SMILES: {molecular_input}')
        elif isinstance(molecular_input, Chem.Mol):
            try:
                self.rdmol = molecular_input
                assert self.rdmol
                self.smiles = Chem.MolToSmiles(self.rdmol)
            except:
                raise ValueError('Mol() received invalid rdkit.Chem.Mol object')
        else:
            raise TypeError('Mol() expects SMILES or rdkit.Chem.Mol object')
       
        ### desalting
        if "." in self.smiles:
            try:
                (self.smiles, self.rdmol) = desalt_smiles(self.smiles)
                assert self.smiles
                assert self.rdmol
            except:
                raise RuntimeError(f'Mol() error occurred in desalting: {self.smiles}')
        
        ### standardization
        if std:
            # standardization changes self.rdmol
            try:
                self.rdmol = standardize(self.rdmol)
                self.smiles = Chem.MolToSmiles(self.rdmol)
                assert self.smiles
                assert self.rdmol
            except:
                raise RuntimeError('Mol() error occurred in standardization')
        
        ### naming
        try:
            self.name = str(name)
        except:
            self.name = 'untitled'
        self.rdmol.SetProp('_Name', self.name) # _Name can't be None
        
        ### set default properties
        self.props.update({
            'aka' : [], # <-- to be set by MolLibr.unique()
            'atoms' : self.rdmol.GetNumAtoms(), 
            # hydrogens not excluded
            # m = Chem.MolFromSmiles("c1c[nH]cc1")
            # m.GetNumAtoms()
            # >> 5
            # Chem.AddHs(m).GetNumAtoms()
            # >> 10
            'charge': rdmolops.GetFormalCharge(self.rdmol),
            # number of rotatable bonds
            "nrb" : Descriptors.NumRotatableBonds(self.rdmol),
            })
           

    def __str__(self) -> str:
        """String representation of the molecule.

        Examples:
            >>> m = Mol('CCO', name='ethanol')
            >>> print(m)

        Returns:
            str: string representation.
        """
        return f"<Mol({self.smiles} name={self.name} conformers={self.count()})>"
    

    def __hash__(self) -> str:
        """Hashed SMILES string of the molecule.

        When you compare two objects using the `==` operator, Python first checks 
        if their hash values are equal. If they are different, the objects are 
        considered unequal, and the __eq__ method is not called.
        The return value of `__hash__` method is also used as dictionary keys or set elements.

        Examples:
            >>> m1 == m2

        Returns:
            str: hashed SMILES string.
        """
        return hash(self.smiles)
    

    def __eq__(self, other:object) -> bool:
        """True if `other` molecule is identical with the molecule.

        It compares canonicalized SMILES.

        Examples:
            >>> m1 == m2

        Args:
            other (object): other rdworks.Mol object.

        Returns:
            bool: True if identical.
        """
        return self.smiles == other.smiles
    

    def __iter__(self) -> Iterator:
        """Yields an iterator of conformers of the molecule.

        Examples:
            >>> for conformer in mol:
            >>>     print(conformer.name)

        Yields:
            Iterator: conformers of the molecule.
        """
        return iter(self.confs)
    

    def __next__(self) -> Conf:
        """Next conformer of the molecule.

        Returns:
            Conf: Conf object of one of conformers of the molecule.
        """
        return next(self.confs)
    

    def __getitem__(self, index: int | slice) -> Conf:
        """Conformer object of conformers of the molecule with given index or slice of indexes.

        Examples:
            >>> first_conformer = mol[0]

        Args:
            index (int | slice): index for conformers.

        Raises:
            ValueError: conformers are not defined in the molecule or index is out of range. 

        Returns:
            Conf: Conf object matching the index of the molecule.
        """
        if self.count() == 0:
            raise ValueError(f"no conformers")
        try:
            return self.confs[index]
        except:
            raise ValueError(f"index should be 0..{self.count()-1}")
        

    def copy(self) -> Self:
        """Returns a copy of self.

        Returns:
            Self: a copy of self (rdworks.Mol) object.
        """
        return copy.deepcopy(self)


    def rename(self, prefix:str='', sep:str='/', start:int=1) -> Self:
        """Rename conformer names and returns self
        
        The first conformer name is {prefix}{sep}{start}

        Args:
            prefix (str, optional): prefix of the name. Defaults to ''.
            sep (str, optional): separtor betwween prefix and serial number. Defaults to '/'.
            start (int, optional): first serial number. Defaults to 1.

        Returns:
            Self: rdworks.Mol object.
        """
        if prefix :
            self.name = prefix
            self.rdmol.SetProp('_Name', prefix)
        # update conformer names
        num_digits = len(str(self.count())) # ex. '100' -> 3
        for (serial, conf) in enumerate(self.confs, start=start):
            serial_str = str(serial)
            while len(serial_str) < num_digits:
                serial_str = '0' + serial_str
            conf.rename(f'{self.name}{sep}{serial_str}')
        return self
    

    def qed(self, properties:list[str]=['QED', 'MolWt', 'LogP', 'TPSA', 'HBD']) -> Self:
        """Updates quantitative estimate of drug-likeness (QED).

        Args:
            properties (list[str], optional): Defaults to ['QED', 'MolWt', 'LogP', 'TPSA', 'HBD'].

        Raises:
            KeyError: if property key is unknown.

        Returns:
            Self: rdworks.Mol object.
        """
        props_dict = {}
        for k in properties:
            try:
                props_dict[k] = rd_descriptor_f[k](self.rdmol)
            except:
                raise KeyError(f'Mol.qed() received undefined property {k} for {self}')
        self.props.update(props_dict)
        return self
    

    def remove_stereo(self) -> Self:
        """Removes stereochemistry and returns a copy of self. 

        Examples:
            >>> m = rdworks.Mol("C/C=C/C=C\\C", "double_bond")
            >>> m.remove_stereo().smiles == "CC=CC=CC"

        Returns:
            Self: rdworks.Mol object.
        """
        obj = copy.deepcopy(self)
        # keep the original stereo info. for ring double bond
        Chem.RemoveStereochemistry(obj.rdmol)
        Chem.AssignStereochemistry(obj.rdmol, 
                                   cleanIt=False, 
                                   force=False, 
                                   flagPossibleStereoCenters=False)
        obj.smiles = Chem.MolToSmiles(obj.rdmol)
        return obj


    def make_confs(self, 
                   n:int = 50, 
                   method:str = 'RDKit_ETKDG',
                   calculator:str | Callable = 'MMFF94') -> Self:
        """Generates 3D conformers.

        Args:
            n (int, optional): number of conformers to generate. Defaults to 50.
            method (str, optional): conformer generation method.
                Choices are `RDKit_ETKDG`, `CDPL_CONFORGE`.
                Defaults to 'RDKit_ETKDG'.

        Returns:
            Self: rdworks.Mol object

        Reference:
            T. Seidel, C. Permann, O. Wieder, S. M. Kohlbacher, T. Langer, 
            High-Quality Conformer Generation with CONFORGE: Algorithm and Performance Assessment. 
            J. Chem. Inf. Model. 63, 5549-5570 (2023).
        """
        
        # if n is None:
        #     rot_bonds = rd_descriptor_f['RotBonds'](self.rdmol)
        #     n = min(max(1, int(8.481 * (rot_bonds **1.642))), 1000)
        # n = max(1, math.ceil(n * n_rel)) # ensures that n is at least 1
        
        self.confs = []

        if method.upper() == 'RDKIT_ETKDG':
            rdmol_H = Chem.AddHs(self.rdmol, addCoords=True) # returns a copy with hydrogens added
            conf_ids = rdDistGeom.EmbedMultipleConfs(rdmol_H, n, params=self.ETKDG_params)
            for rdConformer in rdmol_H.GetConformers():
                # number of atoms should match with conformer(s)
                rdmol_conf = Chem.Mol(rdmol_H)
                rdmol_conf.RemoveAllConformers()
                rdmol_conf.AddConformer(Chem.Conformer(rdConformer))
                conf = Conf(rdmol_conf)
                self.confs.append(conf)
        
        elif method.upper() == 'CDPL_CONFORGE':
            with tempfile.NamedTemporaryFile() as tmpfile:
                mol = CDPL.Chem.parseSMILES(self.smiles)
                # create and initialize an instance of the class ConfGen.ConformerGenerator which
                # will perform the actual conformer ensemble generation work
                conf_gen = CDPL.ConfGen.ConformerGenerator()
                conf_gen.settings.timeout = 60 * 1000  # 60 sec.
                conf_gen.settings.minRMSD = 0.5
                conf_gen.settings.energyWindow = 20.0 # kcal/mol(?)
                conf_gen.settings.maxNumOutputConformers = n
                # dictionary mapping status codes to human readable strings
                status_to_str = { 
                    CDPL.ConfGen.ReturnCode.UNINITIALIZED                  : 'uninitialized',
                    CDPL.ConfGen.ReturnCode.TIMEOUT                        : 'max. processing time exceeded',
                    CDPL.ConfGen.ReturnCode.ABORTED                        : 'aborted',
                    CDPL.ConfGen.ReturnCode.FORCEFIELD_SETUP_FAILED        : 'force field setup failed',
                    CDPL.ConfGen.ReturnCode.FORCEFIELD_MINIMIZATION_FAILED : 'force field structure refinement failed',
                    CDPL.ConfGen.ReturnCode.FRAGMENT_LIBRARY_NOT_SET       : 'fragment library not available',
                    CDPL.ConfGen.ReturnCode.FRAGMENT_CONF_GEN_FAILED       : 'fragment conformer generation failed',
                    CDPL.ConfGen.ReturnCode.FRAGMENT_CONF_GEN_TIMEOUT      : 'fragment conformer generation timeout',
                    CDPL.ConfGen.ReturnCode.FRAGMENT_ALREADY_PROCESSED     : 'fragment already processed',
                    CDPL.ConfGen.ReturnCode.TORSION_DRIVING_FAILED         : 'torsion driving failed',
                    CDPL.ConfGen.ReturnCode.CONF_GEN_FAILED                : 'conformer generation failed',
                    }
                writer = CDPL.Chem.MolecularGraphWriter( f"{tmpfile.name}.sdf", "sdf" )
                # SB - io.StringIO does not work with Chem.MolecularGraphWriter()
                # We have to create a temporary file and re-read it for storing individual conformers. 
                try:
                    # prepare the molecule for conformer generation
                    CDPL.ConfGen.prepareForConformerGeneration(mol) 
                    # generate the conformer ensemble
                    status = conf_gen.generate(mol)             
                    # if successful, store the generated conformer ensemble as
                    # per atom 3D coordinates arrays (= the way conformers are represented in CDPKit)
                    if status == CDPL.ConfGen.ReturnCode.SUCCESS or status == CDPL.ConfGen.ReturnCode.TOO_MUCH_SYMMETRY:
                        # TOO_MUCH_SYMMETRY: output ensemble may contain duplicates
                        conf_gen.setConformers(mol)
                        writer.write(mol)
                        with Chem.SDMolSupplier(f"{tmpfile.name}.sdf", sanitize=True, removeHs=False) as sdf:
                            self.confs = [ Conf(m) for m in sdf if m is not None ]                            
                    else:
                        raise RuntimeError('Error: conformer generation failed: %s' % status_to_str[status])
                except Exception as e:
                    raise RuntimeError('Error: conformer generation failed: %s' % str(e))
            # tmpfile is automatically closed and deleted here


        # energy evaluations for ranking
        for conf in self.confs:
            conf.get_potential_energy(calculator) # default: MMFF94
        
        # set relative energy, E_rel(kcal/mol)
        sort_by = 'E_tot(kcal/mol)'
        self.confs = sorted(self.confs, key=lambda c: c.props[sort_by]) # ascending order
        lowest_energy = self.confs[0].props[sort_by]
        for conf in self.confs:
            conf.props.update({"E_rel(kcal/mol)": conf.props[sort_by] - lowest_energy})

        return self.rename()


    def optimize(self, calculator:str | Callable = 'MMFF94', fmax:float=0.05) -> Self:
        """Optimizes 3D conformers

        Args:
            calculator (str | Callable): _description_
            fmax (float, optional): _description_. Defaults to 0.05.

        Returns:
            Self: _description_
        """
        self.confs = [ conf.optimize(calculator, fmax) for conf in self.confs ]
        return self


    def sort_confs(self) -> Self:
        """Sorts conformers by `E_tot(eV)` or `E_tot(kcal/mol)` and sets `E_rel(kcal/mol)`. 

        Raises:
            KeyError: if `E_tot(eV)` or `E_tot(kcal/mol)` is not defined.

        Returns:
            Self: rdworks.Mol object.
        """
        if all(['E_tot(eV)' in c.props for c in self.confs]):
            sort_by = 'E_tot(eV)'
            conversion = 23.060547830619026  # eV to kcal/mol
        elif all(['E_tot(kcal/mol)' in c.props for c in self.confs]):
            sort_by = 'E_tot(kcal/mol)'
            conversion = 1.0
        else:
            raise KeyError(f'Mol.sort_confs() requires E_tot(eV) or E_tot(kcal/mol) property')
        self.confs = sorted(self.confs, key=lambda c: c.props[sort_by]) # ascending order
        if self.count() > 0:
            E_lowest = self.confs[0].props[sort_by]
            for conf in self.confs:
                E_rel = (conf.props[sort_by] - E_lowest)* conversion
                conf.props.update({"E_rel(kcal/mol)": E_rel})
        return self
    

    def align_confs(self, method:str='rigid_fragment') -> Self:
        """Aligns all conformers to the first conformer.

        Args:
            method (str, optional): alignment method: 
                `rigid_fragment`, `CrippenO3A`, `MMFFO3A`, `best_rms`.
                Defaults to `rigid_fragment`.

        Returns:
            Self: rdworks.Mol object.
        """

        if self.count() < 2: # nothing to do
            return self

        if method == 'rigid_fragment':
            indices = rigid_fragment_indices(self.confs[0].rdmol)[0] # 3D and H, largest fragment
            atomMap = [(i, i) for i in indices]
            for i in range(1, self.count()):
                # rdMolAlign.AlignMol does not take symmetry into account
                # but we will use atom indices for alignment anyway.
                rmsd = rdMolAlign.AlignMol(prbMol=self.confs[i].rdmol, 
                                           refMol=self.confs[0].rdmol, 
                                           atomMap=atomMap)
                # If atomMap is not given, AlignMol() will attempt to generate atomMap by
                # substructure matching.
        
        elif method == 'CrippenO3A':
            crippen_ref_contrib = rdMolDescriptors._CalcCrippenContribs(self.confs[0].rdmol)
            for i in range(1, self.count()):
                crippen_prb_contrib = rdMolDescriptors._CalcCrippenContribs(self.confs[i].rdmol)
                crippen_O3A = rdMolAlign.GetCrippenO3A(prbMol=self.confs[i].rdmol,
                                                       refMol=self.confs[0].rdmol, 
                                                       prbCrippenContribs=crippen_prb_contrib, 
                                                       refCrippenContribs=crippen_ref_contrib, 
                                                       )
                crippen_O3A.Align()
                # crippen_O3A.Score()

        elif method == 'MMFFO3A':
            mmff_ref_params = AllChem.MMFFGetMoleculeProperties(self.confs[0].rdmol)
            for i in range(1, self.count()):
                mmff_prb_params = AllChem.MMFFGetMoleculeProperties(self.confs[i].rdmol)
                mmff_O3A = rdMolAlign.GetO3A(prbMol=self.confs[i].rdmol, 
                                             refMol=self.confs[0].rdmol, 
                                             prbPyMMFFMolProperties=mmff_prb_params, 
                                             refPyMMFFMolProperties=mmff_ref_params, 
                                            )
                mmff_O3A.Align()
                # mmff_O3A.Score()

        elif method == 'best_rms':
            for i in range(1, self.count()):
                # symmetry-aware alignment / speed can be improved by removing Hs
                rmsd = rdMolAlign.GetBestRMS(prbMol=self.confs[i].rdmol, 
                                             refMol=self.confs[0].rdmol)
        
        return self
    

    def cluster_confs(self, method:str='QT', threshold:float=1.0, sortby:str='size') -> Self:
        """Clusters all conformers and sets cluster properties.
        
        Following cluster properties will be added: `cluster`, `cluster_mean_energy`, 
            `cluster_median_energy`, `cluster_IQR_energy`, `cluster_size`, `cluster_centroid` (True or False)                  
        
        `RCKMeans` algorithm is unreliable and not supported for now.
        
        Args:
            method (str, optional): clustering algorithm:
                `Butina`, 
                `QT`,
                `NMRCLUST`,
                `DQT`,
                `BitQT`, 
                `DynamicTreeCut`, 
                `AutoGraph`.
                Defaults to `QT`.
            threshold (float, optional): RMSD threshold of a cluster. Defaults to 1.0.
            sortby (str, optional): sort cluster(s) by mean `energy` or cluster `size`. 
                Defaults to `size`.

        Raises:
            NotImplementedError: if unsupported method is requested.

        Returns:
            Self: rdworks.Mol object
        """
        if method != 'DQT': # rmsd of x,y,z coordinates (non-H)
            conf_rdmols_noH = [Chem.RemoveHs(Chem.Mol(conf.rdmol)) for conf in self.confs]
            # copies are made for rmsd calculations to prevent coordinates changes
            lower_triangle_values = [] 
            for i in range(self.count()): # number of conformers
                for j in range(i):
                    # rdMolAlign.GetBestRMS takes symmetry into account
                    # removed hydrogens to speed up
                    best_rms = rdMolAlign.GetBestRMS(prbMol=conf_rdmols_noH[i], refMol=conf_rdmols_noH[j])
                    lower_triangle_values.append(best_rms)
        
        else: # rmsd (radian) of dihedral angles
            torsion_atom_indices = self.torsion_atoms()
            # symmmetry-related equivalence is not considered
            torsions = []
            for conf in self.confs:
                t_radians = []
                for (i, j, k, l, rot_indices, fix_indices) in torsion_atom_indices:
                    t_radians.append(
                        rdMolTransforms.GetDihedralRad(conf.rdmol.GetConformer(), i, j, k, l))
                torsions.append(np.array(t_radians))
            # torsions: num.confs x num.torsions
            N = len(torsions)
            lower_triangle_values = []
            for i in range(N):
                for j in range(i):
                    rad_diff = np.fmod(torsions[i] - torsions[j], 2.0*np.pi)
                    rmsd = np.sqrt(np.sum(rad_diff**2)/N)
                    # np.max(np.absolute(rad_diff))
                    lower_triangle_values.append(rmsd)

        cluster_assignment = None
        centroid_indices = None

        if method == 'Butina':
            clusters = Butina.ClusterData(data=lower_triangle_values, 
                                          nPts=self.count(),
                                          distThresh=threshold,
                                          isDistData=True,
                                          reordering=True)
            cluster_assignment = [None,] * self.count()
            centroid_indices = []
            for cluster_idx, indices in enumerate(clusters):
                for conf_idx in indices:
                    cluster_assignment[conf_idx] = cluster_idx
                centroid_indices.append(indices[0])

        elif method == 'QT': 
            # my implementation of the original QT algorithm
            # tighter than Butina
            symm_matrix = convert_tril_to_symm(lower_triangle_values)
            cluster_assignment, centroid_indices = QT(symm_matrix, threshold)
        
        elif method == 'NMRCLUST': 
            # looser than Butina
            # does not require threshold
            symm_matrix = convert_tril_to_symm(lower_triangle_values)
            cluster_assignment, centroid_indices = NMRCLUST(symm_matrix)

        elif method == 'DQT':
            # issues with symmetry related multiplicities
            symm_matrix = convert_tril_to_symm(lower_triangle_values)
            cluster_assignment, centroid_indices = QT(symm_matrix, threshold)

        elif method == 'BitQT':
            # supposed to produce identical result as QT but it does not
            symm_matrix = convert_tril_to_symm(lower_triangle_values)
            cluster_assignment, centroid_indices = BitQT(symm_matrix, threshold)
        
        elif method == 'DynamicTreeCut':
            # often collapses into single cluster. so not very useful.
            symm_matrix = convert_tril_to_symm(lower_triangle_values)
            cluster_assignment, centroid_indices = DynamicTreeCut(symm_matrix)
        
        # elif method == 'RCKmeans':
        #     # buggy
        #     symm_matrix = convert_tril_to_symm(lower_triangle_values)
        #     cluster_assignment, centroid_indices = RCKmeans(symm_matrix)
        
        elif method == 'AutoGraph':
            # not reliable
            symm_matrix = convert_tril_to_symm(lower_triangle_values)
            cluster_assignment, centroid_indices = AutoGraph(symm_matrix)

        else:
            raise NotImplementedError(f'{method} clustering is not implemented yet.')

        # cluster_assignment: ex. [0,1,0,0,2,..]
        # centroid_indices: ex. [10,5,..] i.e. centroids of clusters 0 and 1 are 10 and 5, respectively.

        if cluster_assignment is not None and centroid_indices is not None:
            cluster_raw_data = defaultdict(list)
            for conf_idx, cluster_idx in enumerate(cluster_assignment):
                cluster_raw_data[cluster_idx].append(conf_idx)
            cluster_list = []
            for i, k in enumerate(sorted(cluster_raw_data.keys())):
                energies = [self.confs[conf_idx].props['E_rel(kcal/mol)'] for conf_idx in cluster_raw_data[k]]
                mean_energy = np.mean(energies)
                median_energy = np.median(energies)
                q75, q25 = np.percentile(energies, [75, 25])
                iqr_energy = q75 - q25 # interquartile range (IQR)
                cluster_list.append({'confs' : cluster_raw_data[k],
                                     'centroid' : centroid_indices[i], # conformer index
                                     'size' : len(cluster_raw_data[k]),
                                     'mean_energy' : mean_energy,
                                     'median_energy' : median_energy,
                                     'iqr_energy' : iqr_energy,
                                     })
            # sort cluster index
            if sortby == 'size':
                cluster_list = sorted(cluster_list, key=lambda x: x['size'], reverse=True)
            
            elif sortby == 'energy':
                cluster_list = sorted(cluster_list, key=lambda x: x['median_energy'], reverse=False)
            
            else:
                raise NotImplementedError(f'{sortby} is not implemented yet.')

            for cluster_idx, cluster_dict in enumerate(cluster_list, start=1):
                for conf_idx in cluster_dict['confs']:
                    if conf_idx == cluster_dict['centroid']:
                        self.confs[conf_idx].props.update({
                                'cluster' : cluster_idx,
                                'cluster_mean_energy' : cluster_dict['mean_energy'],
                                'cluster_median_energy' : cluster_dict['median_energy'],
                                'cluster_IQR_energy' : cluster_dict['iqr_energy'],
                                'cluster_size' : cluster_dict['size'],
                                'cluster_centroid' : True,
                                })
                    else:
                        self.confs[conf_idx].props.update({
                                'cluster' : cluster_idx,
                                'cluster_mean_energy' : cluster_dict['mean_energy'],
                                'cluster_median_energy' : cluster_dict['median_energy'],
                                'cluster_IQR_energy' : cluster_dict['iqr_energy'],
                                'cluster_size' : cluster_dict['size'],
                                'cluster_centroid' : False,
                                })
        return self


    def drop_confs(self,
                   stereo_flipped:bool=True,
                   unconverged:bool=True,
                   similar: bool | None = None,
                   similar_rmsd:float=0.3,
                   cluster: bool | None =None,
                   k: int | None = None,
                   window: float | None = None,
                   verbose: bool = False) -> Self:
        """Drop conformers that meet some condition(s).

        Args:
            stereo_flipped (bool): drop conformers whose R/S and cis/trans stereo is unintentionally flipped.
                For example, a trans double bond in a macrocyle can end up with both trans
                and cis isomers in the final optimized conformers.
            unconverged (bool): drop unconverged conformers. see `Converged` property.
            similar (bool, optional): drop similar conformers. see `similar_rmsd`.
            similar_rmsd (float): RMSD (A) below `similar_rmsd` is regarded similar (default: 0.3)
            cluster (bool, optional): drop all except for the lowest energy conformer in each cluster.
            k (int, optional): drop all except for `k` lowest energy conformers.
            window (float, optional): drop all except for conformers within `window` of relative energy.
        
        Returns:
            Self: a copy of rdworks.Mol object.

        Examples:
            To drop similar conformers within rmsd of 0.5 A
            >>> mol.drop_confs(similar=True, similar_rmsd=0.5)
            
            To drop conformers beyond 5 kcal/mol
            >>> mol.drop_confs(window=5.0)
            
        """
        obj = copy.deepcopy(self)
               
        if stereo_flipped and obj.count() > 0:
            mask = [Chem.MolToSmiles(Chem.RemoveHs(_.rdmol)) == obj.smiles for _ in obj.confs]
            obj.confs = list(itertools.compress(obj.confs, mask))
            if verbose:
                main_logger.info(f'drop_confs stereo_flipped={mask.count(False)} -> {obj.count()}')
        
        if unconverged and obj.count() > 0:
            mask = [_.props['Converged'] if 'Converged' in _.props else True for _ in obj.confs]
            obj.confs = list(itertools.compress(obj.confs, mask))
            if verbose:
                main_logger.info(f'drop_confs unconverged={mask.count(False)} -> {obj.count()}')

        if similar and obj.count() > 1:
            # it is observed that there are essentially identical conformers 
            # such as 180-degree ring rotation and there is not minor conformational variations
            # in the RDKit ETKDG generated conformers.
            conf_rdmols_noH = [Chem.RemoveHs(Chem.Mol(_.rdmol)) for _ in obj.confs]
            # copies are made for rmsd calculations to prevent coordinates changes
            lower_triangle_values = []
            for i in range(obj.count()): # number of conformers
                for j in range(i):
                    # rdMolAlign.GetBestRMS takes symmetry into account
                    # removed hydrogens to speed up
                    best_rms = rdMolAlign.GetBestRMS(prbMol=conf_rdmols_noH[i], refMol=conf_rdmols_noH[j])
                    lower_triangle_values.append(best_rms)
            symm_matrix = convert_tril_to_symm(lower_triangle_values)
            cluster_assignment, centroid_indices = QT(symm_matrix, similar_rmsd)
            mask = [conf_idx in centroid_indices for conf_idx, conf in enumerate(obj.confs)]
            obj.confs = list(itertools.compress(obj.confs, mask))
            if verbose:
                main_logger.info(f'drop_confs similar({similar_rmsd})={mask.count(False)} -> {obj.count()}')

            # note: it will retain the conformers with lower index
            # so, it should be sorted before dropping
            # obj = obj.sort_confs()
            # mask = []
            # retained_confs = []
            # for conf_i in obj.confs:
            #     is_dissimilar = True
            #     for conf_j_rdmol_noH in retained_confs:
            #         # symmetry-aware alignment / removing Hs speeds up the calculation
            #         rmsd = rdMolAlign.GetBestRMS(Chem.RemoveHs(conf_i.rdmol), conf_j_rdmol_noH)
            #         if rmsd < similar_rmsd:
            #             is_dissimilar = False
            #             break
            #     mask.append(is_dissimilar)
            #     if is_dissimilar:
            #         retained_confs.append(Chem.RemoveHs(conf_i.rdmol)) # store a copy of H-removed rdmol
            # obj.confs = list(itertools.compress(obj.confs, mask))
        
        if cluster and obj.count() > 1:
            # drop non-centroid cluster member(s)
            mask = [_.props['centroid'] if 'centroid' in _.props else True for _ in obj.confs]
            obj.confs = list(itertools.compress(obj.confs, mask))
            if verbose:
                main_logger.info(f'drop_confs cluster(non-centroid)={mask.count(False)} -> {obj.count()}')

        if (k or window) and obj.count() > 0:
            if k:
                mask_k = [i < k for i,_ in enumerate(obj.confs)]
            else:
                mask_k = [True,] * obj.count()
            if window:
                mask_window = [_.props['E_rel(kcal/mol)'] < window if 'E_rel(kcal/mol)' in _.props else True for _ in obj.confs]
            else:
                mask_window = [True,] * obj.count()
            # retain conformer(s) that satisfy both k and window conditions
            mask = [(x and y) for (x,y) in zip(mask_k, mask_window)]
            obj.confs = list(itertools.compress(obj.confs, mask))
            if verbose:
                main_logger.info(f'drop_confs k and/or window={mask.count(False)} -> {obj.count()}')
        
        return obj


    def count(self) -> int:
        """Returns the total number of conformers.

        Returns:
            int: total count of conformers.
        """
        return len(self.confs)
    

    def is_nn_applicable(self,  model:str) -> bool:
        """Check if a particular neural network model is applicable to current molecule.

        Args:
            model (str): neural network models: `ANI-2x`, `ANI-2xt`, `AIMNET`

        Raises:
            ValueError: if model is not supported.

        Returns:
            bool: True if applicable.
        """
        if model.lower() in ['ani-2x', 'ani-2xt']:
            if self.props['charge'] != 0:
                return False
            # H, C, N, O, F, S, Cl
            atomic_numbers = [1, 6, 7, 8, 9, 16, 17 ]
        
        elif model in ['aimnet', 'aimnet2']:
            # H, B, C, N, O, F, Si, P, S, Cl, As, Se, Br, I
            atomic_numbers = [1, 5, 6, 7, 8, 9, 14, 15, 16, 17, 33, 34, 35, 53 ]
        
        else:
            raise ValueError('is_nn_applicable() supports ANI-2x, ANI-2xt, or AIMNET')
        
        for a in self.rdmol.GetAtoms():
            if a.GetAtomicNum() not in atomic_numbers:
                return False
            
        return True


    def charge(self) -> int:
        """Returns molecular formal charge

        Returns:
            int: molecular formal charge
        """
        return rdmolops.GetFormalCharge(self.rdmol)
    

    def symbols(self) -> list[str]:
        """Returns the element symbols.

        Returns:
            list: list of element symbols.
        """
        return [ a.GetSymbol() for a in self.rdmol.GetAtoms() ]


    def numbers(self) -> list[int]:
        """Returns the atomic numbers.

        Returns:
            list: list of atomic numbers.
        """
        return [ a.GetAtomicNum() for a in self.rdmol.GetAtoms() ]
    

    def torsion_atoms(self, strict:bool=True) -> list[tuple]:
        """Determine dihedral angle atoms (a-b-c-d) and rotating group for each rotatable bond (b-c).

        Args:
            strict (bool): whether to exclude amide/imide/ester/acid bonds.

        Returns:
            [   (a, b, c, d, rot_atom_indices, fix_atom_indices), 
                (a, b, c, d, rot_atom_indices, fix_atom_indices), 
                ...,
            ]
        """
        # https://github.com/rdkit/rdkit/blob/1bf6ef3d65f5c7b06b56862b3fb9116a3839b229/rdkit/Chem/Lipinski.py#L47%3E
        # https://github.com/rdkit/rdkit/blob/de602c88809ea6ceba1e8ed50fd543b6e406e9c4/Code/GraphMol/Descriptors/Lipinski.cpp#L108
        if strict :
            # excludes amide/imide/ester/acid bonds
            rotatable_bond_pattern = Chem.MolFromSmarts(
                (
                "[!$(*#*)&!D1&!$(C(F)(F)F)&!$(C(Cl)(Cl)Cl)&!$(C(Br)(Br)Br)&!$(C([CH3])("
                "[CH3])[CH3])&!$([CD3](=[N,O,S])-!@[#7,O,S!D1])&!$([#7,O,S!D1]-!@[CD3]="
                "[N,O,S])&!$([CD3](=[N+])-!@[#7!D1])&!$([#7!D1]-!@[CD3]=[N+])]-,:;!@[!$"
                "(*#*)&!D1&!$(C(F)(F)F)&!$(C(Cl)(Cl)Cl)&!$(C(Br)(Br)Br)&!$(C([CH3])(["
                "CH3])[CH3])]"
                )
            )
        else:
            rotatable_bond_pattern = Chem.MolFromSmarts('[!$(*#*)&!D1]-&!@[!$(*#*)&!D1]')
        rotatable_bonds = self.rdmol.GetSubstructMatches(rotatable_bond_pattern)
        torsion_angle_atom_indices = []

        # small rings (n=3 or 4)
        small_rings = [ r for r in list(self.rdmol.GetRingInfo().AtomRings()) if len(r) < 5 ]
        # ex. = [(1, 37, 35, 34, 3, 2), (29, 28, 30)]

        forbidden_terminal_nuclei = [1, 9, 17, 35, 53] # H,F,Cl,Br,I

        for (b_idx, c_idx) in rotatable_bonds:
            # determine a atom ``a`` that define a dihedral angle 
            a_candidates = []
            for neighbor in self.rdmol.GetAtomWithIdx(b_idx).GetNeighbors():
                neighbor_idx = neighbor.GetIdx()
                if neighbor_idx == c_idx:
                    continue
                neighbor_atomic_num = neighbor.GetAtomicNum()
                if neighbor_atomic_num not in forbidden_terminal_nuclei:
                    a_candidates.append((neighbor_atomic_num, neighbor_idx))
            
            if not a_candidates:
                continue
            
            (a_atomic_num, a_idx) = sorted(a_candidates, key=lambda x: (x[0], -x[1]), reverse=True)[0]

            # is a-b in a small ring (n=3 or 4)?
            is_in_small_ring = False
            for small_ring in small_rings:
                if (a_idx in small_ring) and (b_idx in small_ring):
                    is_in_small_ring = True
                    break
            
            if is_in_small_ring:
                continue

            # determine a atom ``d`` that define a dihedral angle
            d_candidates = []
            for neighbor in self.rdmol.GetAtomWithIdx(c_idx).GetNeighbors():
                neighbor_idx = neighbor.GetIdx()
                if (neighbor_idx == b_idx):
                    continue
                neighbor_atomic_num = neighbor.GetAtomicNum()
                if neighbor_atomic_num not in forbidden_terminal_nuclei:
                    d_candidates.append((neighbor_atomic_num, neighbor_idx))
            
            if not d_candidates:
                continue
            
            (d_atomic_num, d_idx) = sorted(d_candidates, key=lambda x: (x[0], -x[1]), reverse=True)[0]

            # is c-d in a small ring?
            is_in_small_ring = False
            for small_ring in small_rings:
                if (c_idx in small_ring) and (d_idx in small_ring):
                    is_in_small_ring = True
                    break
            
            if is_in_small_ring:
                continue

            # determine a group of atoms to be rotated
            # https://ctr.fandom.com/wiki/Break_rotatable_bonds_and_report_the_fragments
            em = Chem.EditableMol(self.rdmol)
            em.RemoveBond(b_idx, c_idx)
            fragmented = em.GetMol()
            (frag1, frag2) = Chem.GetMolFrags(fragmented, asMols=False) # returns tuple of tuple
            hac1 = sum([ 1 for i in frag1 if self.rdmol.GetAtomWithIdx(i).GetAtomicNum() > 1 ])
            hac2 = sum([ 1 for i in frag2 if self.rdmol.GetAtomWithIdx(i).GetAtomicNum() > 1 ])
            
            # smaller fragment will be rotated and must contain at least three heavy atoms
            if min(hac1, hac2) >= 3:
                (frag_rot, frag_fix) = sorted([(hac1, frag1), (hac2, frag2)])
                torsion_angle_atom_indices.append((a_idx, b_idx, c_idx, d_idx, frag_rot[1], frag_fix[1]))

        return torsion_angle_atom_indices


    def compute(self, **kwargs) -> Self:
        """Change settings for parallel computing.

        Args:
            max_workers (int): max number of workers.
            chunksize (int): chunksize of splitted workload.
            progress (bool): whether to show progress bar.

        Returns:
            Self: rdworks.MolLibr object.
        """
        self.max_workers = kwargs.get('max_workers', self.max_workers)
        self.chunksize = kwargs.get('chunksize', self.chunksize)
        self.progress = kwargs.get('progress', self.progress)
        return self
    

    @staticmethod
    def _map_optimize_conf(conf:Conf, targs:tuple) -> Conf:
        """A map function to apply Conf.optimize() on `conf`.

        The default behavior of map() is to pass the elements of the iterable to the function by reference. 
        This means that if the function modifies the elements of the iterable, 
        those changes will be reflected in the iterable itself.

        Args:
            conf (Conf): subject rdworks.Conf object.
            targs (tuple): tuple of arguments to be passed to Conf.optimize().

        Returns:
            Conf: rdworks.Conf object
        """
        return conf.optimize(*targs)
    

    def torsion_energies(self,
                         calculator:str | Callable, 
                         fmax:float = 0.05,
                         interval:float = 15.0,
                         use_converged_only: bool = True,
                         optimize_ref: bool = False,
                         **kwargs,
                         ) -> Self:
        """Calculates potential energy profiles for each torsion angle using ASE optimizer.

        Args:
            calculator (str | Callable): 'MMFF', 'UFF', or ASE calculator.
            fmax (float, optional): fmax of ASE optimizer. Defaults to 0.05.
            interval (float, optional): interval of torsion angles in degree. Defaults to 15.0.
            use_converged_only (bool, optional): whether to use only converged data. Defaults to True.

        Returns:
            list[dict]: [{'indices':list, 'angle':list, 'E_rel(kcal/mol)':list}, ...]
        """
        self = self.compute(**kwargs)

        torsion_atoms_indices = self.torsion_atoms()

        ref_conf = self.confs[0].copy() # use the lowest energy conformer as a reference
        if optimize_ref:
            ref_conf = ref_conf.optimize(calculator, fmax)

        # mol.confs will be populated with torsion conformers. 
        # It is designed for a batch optimization in the future.
        mol = self.copy()
        mol.confs = []
        data = []

        for k, (a, b, c, d, rot_indices, fix_indices) in enumerate(torsion_atoms_indices):
            data.append({'angle':[], 'init':[], 'final':[], 'Converged':[]})
            for angle in np.arange(-180.0, 180.0, interval): 
                # Iterated numpy.ndarray does not contain the last 180: -180., ..., (180).
                x = ref_conf.copy()
                x.props.update({'torsion_index': k, 'angle': float(angle)})
                AllChem.SetDihedralDeg(x.rdmol.GetConformer(), a, b, c, d, angle)
                # All atoms bonded to atom d will move.
                mol.confs.append(x)

        # Optimize
        # with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
        #     largs = [ (calculator, fmax,) ] * mol.count()
        #     if self.progress:
        #         lconfs = list(tqdm(
        #             executor.map(Mol._map_optimize_conf, mol.confs, largs, chunksize=1),
        #             desc="Optimize conformers",
        #             total=mol.count()))
        #     else:
        #         lconfs = list(
        #             executor.map(Mol._map_optimize_conf, mol.confs, largs, chunksize=1))
        #     mol.confs = lconfs

        # Calculate relaxation energies
        for conf in mol.confs:
            conf = conf.optimize(calculator, fmax)
            # conf.optimize() updates coordinates and conf.props: 
            #   `angle`, `E_tot_init(kcal/mol)`, `E_tot(kcal/mol)`, `Converged`.
            i = conf.props['torsion_index']
            data[i]['angle'].append(conf.props['angle'])
            data[i]['init'].append(conf.props['E_tot_init(kcal/mol)'])
            data[i]['final'].append(conf.props['E_tot(kcal/mol)'])
            data[i]['Converged'].append(conf.props['Converged'])
        
        # Post-processing
        torsion_energy_profiles = []
        for indices, datadict in zip(torsion_atoms_indices, data):
            if use_converged_only:
                datadict['angle'] = list(itertools.compress(datadict['angle'], datadict['Converged']))
                datadict['init'] = list(itertools.compress(datadict['init'], datadict['Converged']))
                datadict['final'] = list(itertools.compress(datadict['final'], datadict['Converged']))
            relax = np.array(datadict['init']) - np.median(datadict['final'])
            E_rel = relax - np.min(relax)
            torsion_energy_profiles.append({
                'indices': indices, # (a, b, c, d, rot_indices, fix_indices)
                'angle': np.array(datadict['angle']).tolist(), # np.ndarray -> list for serialization
                'E_rel(kcal/mol)': E_rel.tolist(), # np.ndarray -> list for serialization
                })
        self.props['torsion'] = torsion_energy_profiles
        self.props['torsion_calculator'] = str(calculator)

        return self




    def similarity(self, other:object) -> float:
        """Returns Tanimoto similarity with `other` rdworks.Mol object.

        Args:
            other (rdworks.Mol): other rdworks.Mol object.

        Raises:
            TypeError: if `other` is not rdworks.Mol object type.

        Returns:
            float: Tanimoto similarity.
        """
        if not isinstance(other, Mol):
            raise TypeError("Mol.is_similar() expects Mol object")
        if not self.fp:
            self.fp = self.MFP2.GetFingerprint(self.rdmol)
        if not other.fp:
            other.fp = other.MFP2.GetFingerprint(other.rdmol)
        return DataStructs.TanimotoSimilarity(self.fp, other.fp)
    

    def is_similar(self, other:object, threshold:float) -> bool:
        """Check if `other` molecule is similar within `threshold`.

        Args:
            other (rdworks.Mol): other rdworks.Mol object to compare with.
            threshold (float): Tanimoto similarity threshold.

        Returns:
            bool: True if similar.
        """
        return self.similarity(other) >= threshold

        
    def is_matching(self, terms: str | Path, invert:bool=False) -> bool:
        """Determines if the molecule matches the predefined substructure and/or descriptor ranges.

        invert | terms(~ or !) | effect
        ------ | ------------- | -------------
        True   |     ~         | No inversion
        True   |               | Inversion
        False  |     ~         | Inversion
        False  |               | No inversion

        Args:
            terms (str | Path): 
                substructure SMARTS expression or a path to predefined descriptor ranges.
            invert (bool, optional): whether to invert the result. Defaults to False.

        Returns:
            bool: True if matches.
        """
        if isinstance(terms, pathlib.PosixPath):
            path = terms.as_posix()
        elif isinstance(terms, str):
            if terms.startswith('~') or terms.startswith('!'):
                terms = terms.replace('~','').replace('!','')
                invert = (invert ^ True)
            try:
                path = pathlib.Path(terms) # test if terms points to a xml file
                assert path.is_file()
            except:
                path = get_predefined_xml(terms)
        else:
            print(list_predefined_xml())
            return False
        
        (lterms, combine) = parse_xml(path)
        mask = []
        for (name, smarts, lb, ub) in lterms:
            if smarts:
                query= Chem.MolFromSmarts(smarts)
                if len(self.rdmol.GetSubstructMatches(query)) > 0:
                    mask.append(True)
                else:
                    mask.append(False)
            else: # descriptor lower and upper bounds
                if name not in self.props:
                    val = rd_descriptor_f[name](self.rdmol)
                    self.props.update({name: val})
                else:
                    val = self.props[name]
                # return if lower and upper boundaries are satisfied
                if ((not lb) or (val >= lb)) and ((not ub) or (val <= ub)):
                    mask.append(True)
                else:
                    mask.append(False)
            if combine.lower() == 'or' and any(mask):
                # early termination if any term is satisfied
                return invert ^ True # XOR(^) inverts only if invert is True
        if combine.lower() == 'and' and all(mask):
            return invert ^ True
        return invert ^ False


    def is_stereo_specified(self) -> bool:
        """Check if the molecule is stereo-specified at tetrahedral atom and double bond.

        This function uses `Chem.FindPotentialStereo()` function which returns a list of `elements`.
        Explanation of the elements:
            element.type: 
                whether the element is a stereocenter ('stereoAtom') or a stereobond ('stereoBond')
                - Atom_Octahedral
                - Atom_SquarePlanar
                - *Atom_Tetrahedral*
                - Atom_TrigonalBipyramidal
                - Bond_Atropisomer
                - Bond_Cumulene_Even
                - *Bond_Double*m.
                - Unspecified 

            element.centeredOn:
                The atom or bond index where the stereochemistry is centered.
            
            element.specified:
                A boolean indicating whether the stereochemistry at that location 
                is explicitly specified in the molecule.
                values = {
                    0: rdkit.Chem.rdchem.StereoSpecified.Unspecified, 
                    1: rdkit.Chem.rdchem.StereoSpecified.Specified, 
                    2: rdkit.Chem.rdchem.StereoSpecified.Unknown,
                    }
            
            element.descriptor:
                A descriptor that can be used to identify the type of stereochemistry (e.g., 'R', 'S', 'E', 'Z').
                - Bond_Cis = rdkit.Chem.StereoDescriptor.Bond_Cis
                - Bond_Trans = rdkit.Chem.StereoDescriptor.Bond_Trans
                - NoValue = rdkit.Chem.StereoDescriptor.NoValue
                - Tet_CCW = rdkit.Chem.StereoDescriptor.Tet_CCW
                - Tet_CW = rdkit.Chem.StereoDescriptor.Tet_CW

        Returns:
            bool: True if stereo-specified.
        """
        stereos = []
        for element in Chem.FindPotentialStereo(self.rdmol):
            if element.type == Chem.StereoType.Atom_Tetrahedral:
                stereos.append(element.specified == Chem.StereoSpecified.Specified)
            elif element.type == Chem.StereoType.Bond_Double :
                bond = self.rdmol.GetBondWithIdx(element.centeredOn)
                if bond.GetBeginAtom().GetSymbol() == 'N' or bond.GetEndAtom().GetSymbol() == 'N':
                    continue
                else:
                    stereos.append(element.specified == Chem.StereoSpecified.Specified)
        # note all([]) returns True
        return all(stereos)


    def get_ring_bond_stereo(self) -> list[tuple]:
        """Returns double bond and cis/trans stereochemistry information.

        Returns:
            list[tuple]: [(element.centeredOn, element.descriptor), ...]
        """
        stereo_info = Chem.FindPotentialStereo(self.rdmol)
        ring_bond_stereo_info = []
        for element in stereo_info:
            if element.type == Chem.StereoType.Bond_Double:
                if self.rdmol.GetBondWithIdx(element.centeredOn).IsInRing():
                    ring_bond_stereo_info.append((element.centeredOn, element.descriptor))
        return ring_bond_stereo_info


    def report_stereo(self) -> None:
        """Print out stereochemistry information.
        """
        num_chiral_centers = rdMolDescriptors.CalcNumAtomStereoCenters(self.rdmol)
        # Returns the total number of atomic stereocenters (specified and unspecified)
        num_unspecified_chiral_centers = rdMolDescriptors.CalcNumUnspecifiedAtomStereoCenters(self.rdmol)
        print(f"chiral centers = unspecified {num_unspecified_chiral_centers} / total {num_chiral_centers}")
        print(f"stereogenic double bonds =")
        for element in Chem.FindPotentialStereo(self.rdmol):
            # element.type= Atom_Octahedral, Atom_SquarePlanar, Atom_Tetrahedral, 
            #               Atom_TrigonalBipyramidal, 
            #               Bond_Atropisomer, Bond_Cumulene_Even, Bond_Double, 
            #               Unspecified 
            if element.type == Chem.StereoType.Bond_Double:
                bond = self.rdmol.GetBondWithIdx(element.centeredOn)
                atom1 = bond.GetBeginAtom().GetSymbol()
                atom2 = bond.GetEndAtom().GetSymbol()
                is_nitrogen = (atom1 == 'N' or atom2 == 'N')
                print(f'  {element.type} bond: {element.centeredOn}', end=' ')
                print(f'ring: {bond.IsInRing()} N: {is_nitrogen}', end=' ')
            elif element.type == Chem.StereoType.Atom_Tetrahedral:
                print(f'  {element.type} atom: {element.centeredOn}', end=' ')
                print(f'atoms {list(element.controllingAtoms)}', end=' ')
            print(f'{element.specified} {element.descriptor}') # type: Chem.StereoDescriptor


    def report_props(self) -> None:
        """Print out properties.
        """
        if self.props:
            print(f"Properties({len(self.props)}):")
            fixed_width = max([len(k) for k in self.props]) + 4
            for k,v in self.props.items():
                while len(k) <= fixed_width:
                    k = k + ' '
                print(f"  {k} {v}")
        else:
            print(f"Properties: None")


    def to_sdf(self, confs:bool=False, props:bool=True) -> str:
        """Returns strings of SDF output.

        Args:
            confs (bool, optional): whether to include conformers. Defaults to False.
            props (bool, optional): whether to include properties. Defaults to True.

        Returns:
            str: strings of SDF output.
        """
        in_memory = io.StringIO()
        with Chem.SDWriter(in_memory) as f:
            if confs:
                for conf in self.confs:
                    rdmol = Chem.Mol(conf.rdmol)
                    rdmol.SetProp('_Name', conf.name)
                    if props:
                        # molcule props.
                        for k,v in self.props.items():
                            rdmol.SetProp(k, str(v))
                        # conformer props.
                        for k,v in conf.props.items():
                            rdmol.SetProp(k, str(v))
                    f.write(rdmol)
            else:
                rdmol = Chem.Mol(self.rdmol)
                rdmol.SetProp('_Name', self.name)
                if props:
                    for k,v in self.props.items():
                        rdmol.SetProp(k, str(v))
                f.write(rdmol)
        return in_memory.getvalue()
    

    def to_image(self, width:int=300, height:int=300, index:bool=False, svg:bool=True) -> object:            
        """Returns PIL(Python Image Library) image object.

        Use .save(output_filename) method to save as an image file.

        Args:
            width (int, optional): width of image. Defaults to 300.
            height (int, optional): height of image. Defaults to 300.
            index (bool, optional): whether to highlight atom indexes. Defaults to False.
            svg (bool, optional): whether to return in SVG format. Defaults to True.

        Returns:
            object: PIL image object.
        """
        if index:
            for a in self.rdmol.GetAtoms():
                a.SetProp("atomNote", str(a.GetIdx()+1))
        
        return Draw.MolsToImage(self.rdmol, 
                                size=(width,height), 
                                kekulize=True,
                                wedgeBonds=True, # draw wedge (stereo)
                                fitImage=False,
                                options=None,
                                canvas=None,
                                useSVG=svg)
    

    def to_svg(self, 
               width:int = 400, 
               height:int = 400,
               legend:str = '', 
               index:bool = False, 
               highlight: list[int] | None = None,
               coordgen:bool = False) -> str:
        """Returns depiction strings in SVG format.

        Examples:
            For Jupyternotebook, wrap the output with SVG:

            >>> from IPython.display import SVG
            >>> SVG(libr[0].to_svg())

        Args:
            width (int): width (default:400)
            height (int): height (default:400)
            legend (str): legend
            index (bool): True/False whether to display atom index
            highlight (list): list of atom indices to highlight

        Returns:
            str: SVG text
        """
        rdDepictor.SetPreferCoordGen(coordgen)

        rdmol_2d = Chem.Mol(self.rdmol)
        rdDepictor.Compute2DCoords(rdmol_2d)
        rdDepictor.StraightenDepiction(rdmol_2d)

        for atom in rdmol_2d.GetAtoms():
            for key in atom.GetPropsAsDict():
                atom.ClearProp(key)

        if index: # index hides polar hydrogens
            for atom in rdmol_2d.GetAtoms():
                atom.SetProp("atomLabel", str(atom.GetIdx()))
                # atom.SetProp("atomNote", str(atom.GetIdx()))
                # atom.SetProp("molAtomMapNumber", str(atom.GetIdx()))

        drawer = rdMolDraw2D.MolDraw2DSVG(width, height)
        if highlight:
            drawer.DrawMolecule(rdmol_2d, legend=legend, highlightAtoms=highlight)
        else:
            drawer.DrawMolecule(rdmol_2d, legend=legend)
        drawer.FinishDrawing()
        return drawer.GetDrawingText()

        
    def plot_energy(self, df:pd.DataFrame) -> str:
        """Returns Seaborn plot strings for dihedral energy profile in SVG format.

        Input pandas DataFrame must have columns: `angle` and `E_rel(kcal/mol)`

        Args:
            df (pd.DataFrame): input dataframe.

        Returns:
            str: Seaborn plot in strings.
        """
        
        # sns.set_theme()
        sns.color_palette("tab10")
        sns.set_style("whitegrid")
        if len(df['angle']) == len(df['angle'].drop_duplicates()):
            g = sns.lineplot(x="angle",  
                             y="E_rel(kcal/mol)", 
                             data=df, 
                             marker='o', 
                             markersize=10)
        else:
            g = sns.lineplot(x="angle",
                             y="E_rel(kcal/mol)", 
                             data=df, 
                             errorbar=('ci', 95),
                             err_style='bars',
                             marker='o',
                             markersize=10)
        g.xaxis.set_major_locator(ticker.MultipleLocator(30))
        g.xaxis.set_major_formatter(ticker.ScalarFormatter())
        if df["E_rel(kcal/mol)"].max() > 35.0:
            g.set(title=self.name,
                  xlabel='Dihedral Angle (degree)', 
                  ylabel='Relative Energy (Kcal/mol)',
                  xlim=(-190, 190),
                  ylim=(-1.5, 35.0))
        elif df["E_rel(kcal/mol)"].max() < 5.0:
            g.set(title=self.name,
                  xlabel='Dihedral Angle (degree)', 
                  ylabel='Relative Energy (Kcal/mol)',
                  xlim=(-190, 190),
                  ylim=(-1.5, 5.0))
        else:
            g.set(title=self.name, 
                  xlabel='Dihedral Angle (degree)', 
                  ylabel='Relative Energy (Kcal/mol)',
                  xlim=(-190, 190),)
        g.tick_params(axis='x', rotation=30)
        in_memory = io.StringIO()
        plt.savefig(in_memory, format='svg', bbox_inches='tight')
        plt.clf()
        return in_memory.getvalue()
    

    def to_html(self, htmlbody:bool=False) -> str:
        """Returns HTML text of dihedral energy profile.

        Args:
            htmlbody (bool, optional): whether to wrap around with `<html><body>`. Defaults to False.

        Returns:
            str: HTML text.
        """
        if htmlbody:
            HTML = "<html><body>"
        else:
            HTML = ""
        # start of content
        HTML += f'<h1 style="text-align:left">{self.name}</h1>'
        HTML += "<table>"
        for datadict in self.props['torsion']: # list of dict
            (a1, a2, a3, a4, _, _) = datadict['indices']
            df = pd.DataFrame({k:datadict[k] for k in ['angle', 'E_rel(kcal/mol)']})
            svg_rdmol = self.to_svg(highlight=[a1, a2, a3, a4], index=True)
            svg_energy_plot = self.plot_energy(df)
            HTML += f"<tr>"
            HTML += f"<td>{a1}-{a2}-{a3}-{a4}</td>"
            HTML += f"<td>{svg_rdmol}</td>"
            HTML += f"<td>{svg_energy_plot}</td>"
            HTML += f"</tr>"
        HTML += '</table>'
        HTML += '<hr style="height:2px;border-width:0;color:gray;background-color:gray">'
        # end of content
        if htmlbody:
            HTML += "</body></html>"
        return HTML


    def serialize(self, key: str | None = None, decimal_places:int=2) -> str:
        """Returns JSON dumps of properties.

        Args:
            key (str | None): key for a subset of properties. Defaults to None.
            decimal_places (int, optional): decimal places for float numbers. Defaults to 2.

        Returns:
            str: serialized JSON dumps.
        """
        props = fix_decimal_places_in_dict(self.props, decimal_places)
        if key:
            return json.dumps({key:props[key]})
        return json.dumps(props)
