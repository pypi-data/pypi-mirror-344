import copy
import itertools
import pandas as pd
import gzip

from pathlib import Path
from typing import Optional, Union, Self, Iterator
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm

from rdkit import Chem, DataStructs
from rdkit.Chem import Draw
from rdkit.ML.Cluster import Butina
from rdkit.SimDivFilters.rdSimDivPickers import MaxMinPicker

from rdworks.conf import Conf
from rdworks.mol import Mol
from rdworks.xml import list_predefined_xml


class MolLibr:
    def __init__(self, 
                 molecules: list | tuple | set | None = None,
                 names: list | tuple | set | None = None,
                 std:bool=False,
                 max_workers:int=4,
                 chunksize:int=100,
                 progress:bool=False) -> None:
        """Create a rdworks.MolLibr object.

        Args:
            molecules (Optional[Union[list,tuple,set]], optional): a list/tuple/set of molecules 
                (rdworks.Mol | SMILES | rdkit.Chem.Mol). Defaults to None.
            names (Optional[Union[list,tuple,set]], optional): a list/tuple/set of names. 
                Defaults to None.
            std (bool, optional): whether to standardize molecules. Defaults to False.
            max_workers (int, optional): max workers for parallel calculation. Defaults to 4.
            chunksize (int, optional): chunksize for parallel calculation. Defaults to 100.
            progress (bool, optional): whether to show progress bar. Defaults to False.

        Raises:
            ValueError: if counts of molecules and names differ.
            TypeError: if molecule is not rdworks.Mol | SMILES | rdkit.Chem.Mol )
        """
        self.libr = []
        self.max_workers = max_workers
        self.chunksize = chunksize
        self.progress = progress
        self.query = None
        self.threshold = None
        self.clusters = None

        if molecules and isinstance(molecules, (list, tuple, set)):
            if names and isinstance(names, (list, tuple, set)):
                if len(names) != len(molecules):
                    raise ValueError('MolLibr() counts of molecules and names are different')
            if isinstance(molecules[0], Mol):
                self.libr = molecules
            elif isinstance(molecules[0], Conf):
                self.libr = [Mol(conf.rdmol, name=conf.name).props.update(conf.props) for conf in molecules]
            elif isinstance(molecules[0], str): # SMILES string
                if names:
                    self.libr = [Mol(smi, name=name, std=std) for (smi, name) in zip(molecules, names)]                        
                else:
                    self.libr = [Mol(smi, std=std) for smi in molecules]                        
                    self.rename(prefix='entry') # default name
            elif isinstance(molecules[0], Chem.Mol):
                if names:
                    self.libr = [Mol(rdmol, name=name, std=std) for (rdmol, name) in zip(molecules, names)]
                else:
                    self.libr = [Mol(rdmol, std=std) for rdmol in molecules]
                    self.rename(prefix='entry') # default name
            else:
                raise TypeError('MolLibr() takes a list|tuple|set of Mol|SMILES|Chem.Mol')
    
    def copy(self) -> Self:
        """Returns a copy of self.

        Returns:
            Self: rdworks.MolLibr object.
        """
        return copy.deepcopy(self)
    
    
    def __str__(self) -> str:
        """Returns string representation.

        Returns:
            str: string representation.
        """
        
        return f"<MolLibr({self.count()})>"
    

    def __iter__(self) -> Iterator:
        """Yields an iterator of molecules.

        Yields:
            Iterator: iterator of molecules.
        """
        return iter(self.libr)
    

    def __next__(self) -> Mol:
        """Next molecule.

        Returns:
            Mol: next molecule (rdworks.Mol) object.
        """
        return next(self.libr)
    

    def __eq__(self, other:Self) -> bool:
        """Operator `==`.

        Args:
            other (rdworks.MolLibr): other rdworks.MolLibr object.

        Returns:
            bool: True if other rdworks.MolLibr object is identical with self.
        """
        if isinstance(other, MolLibr):
            return len(frozenset(self.libr) - frozenset(other.libr)) == 0
        else:
            return False
        

    def __getitem__(self, index: int | slice) -> Mol:
        """Operator `[]`.

        Args:
            index (Union[int, slice]): index or slice of indexes.

        Raises:
            ValueError: if library is empty or index is out of range.

        Returns:
            Mol: rdworks.Mol object
        """
        if self.count() == 0:
            raise ValueError(f"library is empty")
        try:
            return self.libr[index]
        except:
            raise ValueError(f"index should be 0..{self.count()-1}")
        

    def __add__(self, other:object) -> Self:
        """Operator `+`. Returns a copy of extended library.

        Args:
            other (object): other rdworks.Mol or rdworks.MolLibr object.

        Raises:
            TypeError: if `other` is not rdworks.Mol or rdworks.MolLibr.

        Returns:
            Self: rdworks.MolLibr object.
        """
        if isinstance(other, Mol):
            obj = copy.deepcopy(self)
            obj.libr.append(other)
            return obj
        elif isinstance(other, MolLibr):
            obj = copy.deepcopy(self)
            obj.libr.extend(other.libr)
            return obj
        else:
            raise TypeError("'+' operator expects rdworks.Mol or rdworks.MolLibr object")


    def __iadd__(self, other: Mol | Self) -> Self:
        """Operator `+=`. Updates self by adding other molecule or library

        Args:
            other (object): other rdworks.Mol or rdworks.MolLibr object.

        Raises:
            TypeError: if `other` is not rdworks.Mol or rdworks.MolLibr.

        Returns:
            Self: rdworks.MolLibr object. 
        """
        if isinstance(other, Mol):
            self.libr.append(other)
        elif isinstance(other, MolLibr):
            self.libr.extend(other.libr)
        else:
            raise TypeError("'+=' operator expects Mol or MolLibr object")
        return self


    def __sub__(self, other: Mol | Self) -> Self:
        """Operator `-`. Returns a copy of subtractive subset.

        Args:
            other (Union[Mol,Self]): other rdworks.Mol or rdworks.MolLibr object.

        Raises:
            TypeError: if `other` is not rdworks.Mol or rdworks.MolLibr.

        Returns:
            Self: a copy of subtractive subset.
        """
        if isinstance(other, Mol):
            difference = frozenset(self.libr) - frozenset([other])
        elif isinstance(other, MolLibr):
            difference = frozenset(self.libr) - frozenset(other.libr)
        else:
            raise TypeError("'-' operator expects rdworks.Mol or rdworks.MolLibr object")
        obj = copy.deepcopy(self)
        obj.libr = list(difference)
        return obj
    

    def __isub__(self, other: Mol | Self) -> Self:
        """Operator `-=`. Updates self by subtracting other molecule or library.

        Args:
            other (Union[Mol,Self]): other molecule or library.

        Raises:
            TypeError: if `other` is not rdworks.Mol or rdworks.MolLibr.

        Returns:
            Self: rdworks.MolLibr object.
        """
        if isinstance(other, Mol):
            difference = frozenset(self.libr) - frozenset([other])
        elif isinstance(other, MolLibr):
            difference = frozenset(self.libr) - frozenset(other.libr)
        else:
            raise TypeError("'-=' operator expects rdworks.Mol or rdworks.MolLibr object")
        self.libr = list(difference)
        return self


    def __and__(self, other: Mol | Self) -> Self:
        """Operator `&`. Returns a copy of common subset.

        Args:
            other (Union[Mol,Self]): other molecule or library.

        Raises:
            TypeError: if `other` is not rdworks.Mol or rdworks.MolLibr.

        Returns:
            Self: a copy of rdworks.MolLibr object.
        """
        if isinstance(other, Mol):
            intersection = frozenset(self.libr) & frozenset([other])
        elif isinstance(other, MolLibr):
            intersection = frozenset(self.libr) & frozenset(other.libr)
        else:
            raise TypeError("'&' operator or overlap() expects rdworks.Mol or rdworks.MolLibr object")
        obj = copy.deepcopy(self)
        obj.libr = list(intersection)
        return obj


    def __iand__(self, other: Mol | Self) -> Self:
        """Operator `&=`. Re-assigns self with common subset.

        Args:
            other (Union[Mol,Self]): other molecule or library.

        Raises:
            TypeError: if `other` is not rdworks.Mol or rdworks.MolLibr.

        Returns:
            Self: rdworks.MolLibr object.
        """
        if isinstance(other, Mol):
            intersection = frozenset(self.libr) & frozenset([other])
        elif isinstance(other, MolLibr):
            intersection = frozenset(self.libr) & frozenset(other.libr)
        else:
            raise TypeError("'&=' operator expects rdworks.Mol or rdworks.MolLibr object")
        self.libr = list(intersection)
        return self
    

    @staticmethod
    def _mask_similar(mol:Mol, targs:tuple) -> bool:
        """A mask function to return True if molecule is similar with target molecules, `targs`.

        Args:
            mol (Mol): subject rdworks.Mol object.
            targs (tuple): a tuple of rdworks.Mol objects to compare.

        Returns:
            bool: True if molecule is similar with target molecules.
        """
        return mol.is_similar(*targs) # unpack tuple of arguments
    

    @staticmethod
    def _mask_drop(mol:Mol, terms:str | Path) -> bool:
        """A mask function to return True if molecule matches `terms`.

        Note that molecules matching the terms will be dropped (NOT be included) in the compression.

        Args:
            mol (Mol): subject rdworks.Mol object.
            terms (str | Path): rule.

        Returns:
            bool: True if molecule matches the terms.
        """
        return not mol.is_matching(terms)
    
    @staticmethod
    def _map_qed(mol:Mol, properties:list[str]=['QED', 'MolWt', 'LogP', 'TPSA', 'HBD']) -> dict:
        """A map function to apply Mol.qed(`properties`) on `mol`.

        The default behavior of map() is to pass the elements of the iterable to the function by reference. 
        This means that if the function modifies the elements of the iterable, 
        those changes will be reflected in the iterable itself.

        Args:
            mol (Mol): subject rdworks.Mol object.
            properties (list[str], optional): properties. Defaults to ['QED', 'MolWt', 'LogP', 'TPSA', 'HBD'].

        Returns:
            dict: dictionary of properties.
        """
        return mol.qed(properties)

    
    def compute(self, **kwargs) -> Self:
        """Change settings for parallel computing.

        Args:
            max_workers (Optional[int], optional): max number of workers. Defaults to None.
            chunksize (Optional[int], optional): chunksize of splitted workload. Defaults to None.
            progress (Optional[bool], optional): whether to show progress bar. Defaults to None.

        Returns:
            Self: rdworks.MolLibr object.
        """
        self.max_workers = kwargs.get('max_workers', self.max_workers)
        self.chunksize = kwargs.get('chunksize', self.chunksize)
        self.progress = kwargs.get('progress', self.progress)
        return self


    def rename(self, prefix:Optional[str]=None, sep:str='.', start:int=1) -> Self:
        """Rename molecules with serial numbers in-place and their conformers.
        
        Molecules will be named by a format, `{prefix}{sep}{serial_number}` and 
        conformers will be named accordingly.

        Examples:
            >>> a.rename(prefix='a')

        Args:
            prefix (str, optional): prefix for new name. If prefix is not given and set to None,
                                    molecules will not renamed but conformers will be still renamed. 
                                    This is useful after dropping some conformers and rename them serially.
            sep (str): separator between prefix and serial number (default: `.`)
            start (int): start number of serial number.

        Returns:
            Self: rdworks.MolLibr object.
        """

        num = self.count()
        num_digits = len(str(num)) # ex. '100' -> 3
        if prefix: 
            # use prefix to rename molecules AND conformers
            for (serial, mol) in enumerate(self.libr, start=start):
                if num > 1:
                    serial_str = str(serial)
                    while len(serial_str) < num_digits:
                        serial_str = '0' + serial_str
                    mol.rename(prefix=f"{prefix}{sep}{serial_str}")
                else:
                    mol.rename(prefix)
        else:
            # rename molecules using serial numbers if they have duplicate names
            # name -> name.1, name.2, ...
            count_names = defaultdict(list)
            for idx, mol in enumerate(self.libr):
                count_names[mol.name].append(idx)
            not_unique_names = [name for name, l in count_names.items() if len(l) > 1]
            for idx, mol in enumerate(self.libr):
                if mol.name in not_unique_names:
                    serial = count_names[mol.name].index(idx) + 1
                    mol.rename(f'{mol.name}.{serial}')
            # rename conformers
            for mol in self.libr:
                mol.rename()
        return self
    

    def overlap(self, other:Self) -> Self:
        """Returns a common subset with `other` library.

        Args:
            other (Self): rdworks.MolLibr object.

        Returns:
            Self: common subset of rdworks.MolLibr.
        """
        return self.__and__(other)
    

    def similar(self, query:Mol, threshold:float=0.2, **kwargs) -> Self:
        """Returns a copy of subset that are similar to `query`.

        Args:
            query (Mol): query molecule.
            threshold (float, optional): similarity threshold. Defaults to 0.2.

        Raises:
            TypeError: if query is not rdworks.Mol type.

        Returns:
            Self: a copy of self.
        """
        obj = copy.deepcopy(self).compute(**kwargs)
        if isinstance(query, Mol):
            largs = [(query, threshold),] * obj.count()
        else:
            raise TypeError("MolLibr.similar() expects Mol object")
        with ProcessPoolExecutor(max_workers=obj.max_workers) as executor:
            if self.progress:
                mask = list(tqdm(executor.map(MolLibr._mask_similar, obj.libr, largs, chunksize=obj.chunksize),
                    desc="Similar",
                    total=obj.count()))
            else:
                mask = list(executor.map(MolLibr._mask_similar, obj.libr, largs, chunksize=obj.chunksize))
            obj.libr = list(itertools.compress(obj.libr, mask))
        return obj



    def unique(self, report=False) -> Self:
        """Removes duplicates and returns a copy of unique library.

        Args:
            report (bool, optional): whether to report duplicates. Defaults to False.

        Returns:
            Self: a copy of self.
        """
        obj = copy.deepcopy(self)
        U = {} # unique SMILES
        mask = []
        for mol in obj.libr:
            if mol.smiles in U:
                mask.append(False)
                # ignore the same name or recorded aka
                if (mol.name != U[mol.smiles].name) and (mol.name not in U[mol.smiles].props['aka']):
                    U[mol.smiles].props['aka'].append(mol.name)
            else:
                mask.append(True)
                U[mol.smiles] = mol
        obj.libr = list(itertools.compress(obj.libr, mask))
        if report:
            print("duplicates:")
            for mol in obj.libr:
                if len(mol.props['aka']) > 0:
                    print(f"  {mol.name}({len(mol.props['aka'])}) - {','.join(mol.props['aka'])}")
            print(f"de-duplicated to {obj.count()} molecules")
        return obj
    

    def qed(self, properties:list[str]=['QED', 'MolWt', 'LogP', 'TPSA', 'HBD'], **kwargs) -> Self:
        """Returns a copy of self with calculated quantitative estimate of drug-likeness (QED).

        Args:
            properties (list[str], optional): _description_. Defaults to ['QED', 'MolWt', 'LogP', 'TPSA', 'HBD'].

        Returns:
            Self: self.
        """
        self = self.compute(**kwargs)
        lprops = [ properties, ] * self.count()
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            if self.progress:
                self.libr = list(tqdm(
                    executor.map(MolLibr._map_qed, self.libr, lprops, chunksize=self.chunksize),
                    desc="QED Properties",
                    total=self.count()
                    ))
            else:
                self.libr = list(
                    executor.map(MolLibr._map_qed, self.libr, lprops, chunksize=self.chunksize)
                    )
        return self
    

    def drop(self, terms:str | Path | None = None, invert:bool=False, **kwargs) -> Self:
        """Drops matched molecules and returns a copy of library with remaining molecules.

        Args:
            terms (str | Path | None, optional): matching terms. Defaults to None.
            invert (bool, optional): whether to invert selection by the `terms`. Defaults to False.

        Returns:
            Self: a copy of self.
        """
        if not terms:
            print(list_predefined_xml())
            return self
        obj = copy.deepcopy(self).compute(**kwargs)
        lterms = [ terms ] * obj.count()
        with ProcessPoolExecutor(max_workers=obj.max_workers) as executor:
            if obj.progress:
                mask = list(tqdm(
                    executor.map(MolLibr._mask_drop, obj.libr, lterms, chunksize=obj.chunksize),
                    desc="Drop",
                    total=obj.count()))
            else:
                mask = list(
                    executor.map(MolLibr._mask_drop, obj.libr, lterms, chunksize=obj.chunksize))
            if invert:
                mask = [not b for b in mask]
            obj.libr = list(itertools.compress(obj.libr, mask))
        return obj
    

    def pick(self, n:int, **kwargs) -> Self:
        """Picks n diverse molecules.

        Args:
            n (int): number of molecules to pick.

        Returns:
            Self: a copy of self.
        """
        obj = copy.deepcopy(self)
        raise NotImplementedError
        return obj
    



    ##################################################
    ### endpoints
    ##################################################

    
    def count(self) -> int:
        """Returns number of molecules.

        Returns:
            int: count of molecules.
        """
        return len(self.libr)
    

    def cluster(self, threshold:float=0.3, ordered:bool=True, drop_singleton:bool=True) -> list:
        """Clusters molecules using fingerprint.

        Args:
            threshold (float, optional): Tanimoto similarity threshold. Defaults to 0.3.
            ordered (bool, optional): order clusters by size of cluster. Defaults to True.
            drop_singleton (bool, optional): exclude singletons. Defaults to True.

        Returns:
            list: [(centroid_1, idx, idx,), (centroid_2, idx, idx,), ...]
        """
        for mol in self.libr:
            if not mol.fp:
                mol.fp = mol.MFP2.GetFingerprint(mol.rdmol)
        fps = [ mol.fp for mol in self.libr if mol.fp ]
        n = len(fps)
        # first generate the distance matrix:
        dmat = []
        for i in range(1, n):
            sims = DataStructs.BulkTanimotoSimilarity(fps[i], fps[:i])
            dmat.extend([1-x for x in sims])
        # Butina hierarchical clustering:
        # clusters is a list of list of indices
        clusters = Butina.ClusterData(dmat, 
                                      nPts=n, 
                                      distThresh=threshold, 
                                      isDistData=True, 
                                      reordering=True)
        if ordered:
            # in the order of cluster size, from the largest to the smallest
            clusters = sorted(clusters, key=lambda indices: len(indices), reverse=True)
        
        if drop_singleton:
            clusters = [indices for indices in clusters if len(indices) > 1]
        
        return clusters
    

    
    def to_sdf(self, 
                path:str | Path, 
                confs:bool=False, 
                props:bool=True, 
                separate:bool=False) -> None:
        """Writes to .sdf or .sdf.gz file.

        Chem.SDWriter is supposed to write all non-private molecular properties.

        `dirname/filename.sdf` -> `dirname/filename_{molecule name}.sdf`
        `dirname/filename.sdf.gz` -> `dirname/filename_{molecule name}.sdf.gz`

        Args:
            path (str or PosixPath) : output filename or path
            confs (bool) : whether to write 3D coordinates and conformer properties. Defaults to False.
            props (bool) : whether to write SDF properties. Defaults to True.
            separate (bool) : write each molecule to separate files. Defaults to False.
        """
        if isinstance(path, str):
            path = Path(path)
        # PurePosixPath('my/dir/mol.sdf.gz').suffix -> '.gz'
        # PurePosixPath('my/dir/mol.sdf.gz').suffixes -> ['.sdf', '.gz']
        # PurePosixPath('my/dir/mol.sdf').name -> 'mol.sdf'
        # PurePosixPath('my/dir/mol.sdf').with_name('mol2.sdf') -> PurePath('my/dir/mol2.sdf')
        suffix = path.suffix 
        suffixes = ''.join(path.suffixes) 
        prefix = path.name.replace(suffixes, '')
        if separate:
            for mol in self.libr:
                if suffix == '.gz':
                    with gzip.open(path.with_name(f'{prefix}_{mol.name}.sdf.gz'), "wt") as f:
                        f.write(mol.to_sdf(confs, props))
                else:
                    with open(path.with_name(f'{prefix}_{mol.name}.sdf'), "w") as f:
                        f.write(mol.to_sdf(confs, props))

        else:
            if suffix == '.gz':
                with gzip.open(path, "wt") as f:
                    for mol in self.libr:
                        f.write(mol.to_sdf(confs, props))
            else:
                with open(path, "w") as f:
                    for mol in self.libr:
                        f.write(mol.to_sdf(confs, props))


    def to_smi(self, path:str | Path) -> None:
        """Writes to .smi file.

        Args:
            path (str | Path): output filename or path.
        """
        if isinstance(path, Path):
            path = path.as_posix() # convert to string
        if path.endswith('.gz'):
            with gzip.open(path, "wt") as smigz:
                for mol in self.libr:
                    smigz.write(f'{mol.smiles} {mol.name}\n')
        else:
            with open(path, "w") as smi:
                for mol in self.libr:
                    smi.write(f'{mol.smiles} {mol.name}\n')


    def to_image(self, width:int=200, height:int=200, index:bool=False, mols_per_row:int=5) -> str:
        """Returns SVG strings for Jupyter notebook.

        Args:
            width (int, optional): width. Defaults to 200.
            height (int, optional): height. Defaults to 200.
            index (bool, optional): whether to show atom index. Defaults to False.
            mols_per_row (int, optional): number of molecules per row. Defaults to 5.

        Returns:
            str: SVG strings for Jupyter notebook.
        """
        
        if index:
            for mol in self.libr: 
                for a in mol.rdmol.GetAtoms():
                    a.SetProp("atomNote", str(a.GetIdx()+1))
        rdmols = [mol.rdmol for mol in self.libr]
        legends = [mol.name for mol in self.libr]
        return Draw.MolsToGridImage(rdmols,
                                    legends=legends,
                                    molsPerRow=min(mols_per_row, len(rdmols)),
                                    subImgSize=(width,height),
                                    useSVG=True)
        

    def to_png(self, path:str | Path, width:int=200, height:int=200, index:bool=False, mols_per_row:int=5) -> None:
        """Writes to a .png file.

        Args:
            path (str | Path): output filename or path.
            width (int, optional): width. Defaults to 200.
            height (int, optional): height. Defaults to 200.
            index (bool, optional): whether to show atom index. Defaults to False.
            mols_per_row (int, optional): number of molecules per row. Defaults to 5.
        """
        if isinstance(path, Path):
            path = path.as_posix() # convert to string
        if index:
            for mol in self.libr: 
                for a in mol.rdmol.GetAtoms():
                    a.SetProp("atomNote", str(a.GetIdx()+1))
        rdmols = [mol.rdmol for mol in self.libr]
        legends = [mol.name for mol in self.libr]
        Draw.MolsToGridImage(rdmols,
                                legends=legends,
                                molsPerRow=min(mols_per_row,len(rdmols)),
                                subImgSize=(width,height),
                                useSVG=False).save(path)


    def to_html(self) -> str:
        """Writes to HTML strings.

        Returns:
            str: HTML strings.
        """
        HTML = "<html><body>"
        for mol in self.libr:
            HTML += mol.to_html(htmlbody=False)
        HTML += "</body></html>"
        return HTML


    def to_dataframe(self, 
                        name:str='name', 
                        smiles:str='smiles', 
                        confs:bool=False) -> pd.DataFrame:
        """Returns a Pandas DataFrame.

        Args:
            name (str, optional): column name for name. Defaults to 'name'.
            smiles (str, optional): column name for SMILES. Defaults to 'smiles'.
            confs (bool, optional): whether to include conformer properties. Defaults to False.

        Returns:
            pd.DataFrame: pandas DataFrame.
        """
        if confs:
            exclude = ['coord']
            property_columns = set()
            for mol in self.libr:
                for conf in mol.confs:
                    for k in conf.props:
                        if k not in exclude:
                            property_columns.add(k)
            property_columns = property_columns - set([name, smiles])
            data = {name:[], smiles:[]}
            data.update({k:[] for k in property_columns})
            for mol in self.libr:
                for conf in mol.confs:
                    data[name].append(conf.name)
                    data[smiles].append(mol.smiles)
                    for k in property_columns:
                        if k in conf.props:
                            data[k].append(conf.props[k])
                        else:
                            data[k].append(None)
        else:
            property_columns = set()
            for mol in self.libr:
                for k in mol.props:
                    property_columns.add(k)
            property_columns = property_columns - set([name, smiles])
            data = {name:[], smiles:[]}
            data.update({k:[] for k in property_columns})
            for mol in self.libr:
                data[name].append(mol.name)
                data[smiles].append(mol.smiles)
                for k in property_columns:
                    if k in mol.props:
                        data[k].append(mol.props[k])
                    else:
                        data[k].append(None)
        return pd.DataFrame(data)


    def to_csv(self, 
                path:str | Path, 
                confs:bool=False, 
                decimal_places:int=3) -> None:
        """Writes to a .csv file.

        Args:
            path (str | Path): output filename or path.
            confs (bool, optional): whether to include conformer properties. Defaults to False.
            decimal_places (int, optional): decimal places for float numbers. Defaults to 3.
        """
        df = self.to_dataframe(confs=confs)
        df.to_csv(path, index=False, float_format=f'%.{decimal_places}f')


    @staticmethod
    def _mask_nn_applicable(mol:Mol, model:str) -> bool:
        """A mask function to return True if molecule is NN applicable. 

        Args:
            mol (Mol): rdworks.Mol object.
            model (str): name of NN model.

        Returns:
            bool: True if molecule is NN applicable.
        """
        return mol.is_nn_applicable(model)
    

    def nn_applicable(self, model:str, **kwargs) -> Self:
        """Returns a copy of subset of library that is applicable to given neural network `model`.

        Examples:
            >>> libr = rdworks.MolLibr(drug_smiles, drug_names)
            >>> ani2x_compatible_subset = libr.nn_applicable('ANI-2x', progress=False)

        Args:
            model (str): name of model.

        Returns:
            Self: subset of library.
        """
        obj = copy.deepcopy(self).compute(**kwargs)
        lmodel = [model,] * self.count()
        with ProcessPoolExecutor(max_workers=obj.max_workers) as executor:
            if obj.progress:
                mask = list(tqdm(
                    executor.map(self.mask_nn_applicable, obj.libr, lmodel, chunksize=obj.chunksize),
                    desc="NN applicable",
                    total=obj.count()))
            else:
                mask = list(
                    executor.map(self._mask_nn_applicable, obj.libr, lmodel, chunksize=obj.chunksize))
            obj.libr = list(itertools.compress(obj.libr, mask))
        return obj
    

    def to_nnbatches(self, batchsize:int=1000) -> list:
        """Split workload flexibily into a numer of batches.

        - Each batch has up to `batchsize` number of atoms.
        - Conformers originated from a same molecule can be splitted into multiple batches.
        - Or one batch can contain conformers originated from multiple molecules.

        coord: coordinates of input molecules (N, m, 3) where N is the number of structures and
        m is the number of atoms in each structure.
        numbers: atomic numbers in the molecule (include H). (N, m)
        charges: (N,)

        Args:
            batchsize: max. number of atoms in a batch.

        Returns:
            list: list of batches.
        """

        pre_batches = []
        batch_confs = []
        batch_mols = []
        batch_n_atoms = 0

        for mol in self.libr:
            for conf in mol.confs:
                n_atoms = conf.props['atoms']
                if (batch_n_atoms + n_atoms) > batchsize:
                    pre_batches.append((batch_mols, batch_confs, batch_n_atoms))
                    # start over a new batch
                    batch_mols =  [mol]
                    batch_confs = [conf]
                    batch_n_atoms = n_atoms
                else:
                    batch_mols.append(mol)
                    batch_confs.append(conf)
                    batch_n_atoms += n_atoms
        
        if batch_n_atoms > 0: # last remaining batch
            pre_batches.append((batch_mols, batch_confs, batch_n_atoms))
        
        batches = []
        
        for i, (batch_mols, batch_confs, batch_n_atoms) in enumerate(pre_batches, start=1):
            charges = [mol.props['charge'] for mol in batch_mols]
            coord = [conf.rdmol.GetConformer().GetPositions().tolist() for conf in batch_confs]
            # to be consistent with legacy code
            coord = [[tuple(xyz) for xyz in inner] for inner in coord]
            # numbers should be got from conformers because of hydrogens
            numbers = [[a.GetAtomicNum() for a in conf.rdmol.GetAtoms()] for conf in batch_confs]
            batches.append((coord, numbers, charges, batch_confs, batch_mols))
        
        return batches