import io
import os
import numpy as np
from typing import Optional, List, Tuple

from PIL import Image, ImageChops

from rdkit import Chem, Geometry
from rdkit.Chem import AllChem, Draw, rdDepictor, rdMolTransforms
from rdkit.Chem.Draw import rdMolDraw2D


# https://greglandrum.github.io/rdkit-blog/posts/2023-05-26-drawing-options-explained.html


def twod_depictor(rdmol:Chem.Mol, index:bool=False, coordgen:bool=False) -> Chem.Mol:
    """Sets up for 2D depiction.

    Args:
        rdmol (Chem.Mol): input molecule.
        index (bool, optional): whether to show atom index. Defaults to False.
        coordgen (bool, optional): whether to set rdDepictor.SetPreferCoordGen. Defaults to False.

    Returns:
        Chem.Mol: a copy of rdkit.Chem.Mol object.
    """
    if coordgen:
        rdDepictor.SetPreferCoordGen(True)
    else:
        rdDepictor.SetPreferCoordGen(False)
    
    rdmol_2d = Chem.Mol(rdmol)
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
    
    return rdmol_2d


def svg(rdmol:Chem.Mol, 
        width:int=300, 
        height:int=300, 
        legend:str='',
        index:bool=False, 
        highlight:list[int] | None = None, 
        coordgen:bool = False) -> str:
    """Returns string SVG output of a molecule.

    Examples:
        >>> from IPython.display import SVG
        >>> SVG(libr[0].to_svg())

    Args:
        rdmol (Chem.Mol): input molecule.
        width (int): width. Defaults to 300.
        height (int): height. Defaults to 300.
        legend (str): title of molecule. Defaults to ''.
        index (bool): whether to show atom indexes. Defaults to False.
        highlight (list[int]): list of atom indices to highlight. Defaults to None.
        coordgen (bool): whether to use rdDepictor.SetPreferCoordGen. Defaults to False.

    Returns:
        str: SVG text
    """
    d2d_svg = rdMolDraw2D.MolDraw2DSVG(width, height)
    rdmol_2d = twod_depictor(rdmol, index, coordgen)
    if highlight:
        d2d_svg.DrawMolecule(rdmol_2d, legend=legend, highlightAtoms=highlight)
    else:
        d2d_svg.DrawMolecule(rdmol_2d, legend=legend)
    #rdMolDraw2D.PrepareAndDrawMolecule(d2d_svg, rdmol_2d, highlightAtoms=highlight, legend=legend)
    d2d_svg.FinishDrawing()
    return d2d_svg.GetDrawingText()


def png(rdmol:Chem.Mol, width:int=300, height:int=300, legend:str='', 
        index:bool=False, highlight:Optional[List[int]]=None, coordgen:bool=False) -> Image.Image:
    """Returns a trimmed PIL Image object of a molecule.

    Args:
        rdmol (Chem.Mol): input molecule.
        width (int): width. Defaults to 300.
        height (int): height. Defaults to 300.
        legend (str): title of molecule. Defaults to ''.
        index (bool): whether to show atom indexes. Defaults to False.
        highlight (list): list of atom indices to highlight. Defaults to None.
        coordgen (bool): whether to use rdDepictor.SetPreferCoordGen. Defaults to False.
    
    Returns:
        Image.Image: output PIL Image object.
    """
    rdmol_2d = twod_depictor(rdmol, index, coordgen)
    img = Draw.MolToImage(rdmol_2d, 
                          size=(width,height),
                          highlightAtoms=highlight,
                          kekulize=True,
                          wedgeBonds=True,
                          fitImage=False,
                          )
    # highlightAtoms: list of atoms to highlight (default [])
    # highlightBonds: list of bonds to highlight (default [])
    # highlightColor: RGB color as tuple (default [1, 0, 0])

    return trim_png(img)


def trim_png(img:Image.Image) -> Image.Image:
    """Removes white margin around molecular drawing.

    Args:
        img (Image.Image): input PIL Image object.

    Returns:
        Image.Image: output PIL Image object.
    """
    bg = Image.new(img.mode, img.size, img.getpixel((0,0)))
    diff = ImageChops.difference(img,bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return img.crop(bbox)
    return img


def rescale(rdmol:Chem.Mol, factor:float=1.5) -> Chem.Mol:
    """Returns a copy of `rdmol` by a `factor`.

    Args:
        rdmol (Chem.Mol): input molecule.
        factor (float): scaling factor.
    
    Returns:
        Chem.Mol: a copy of rescaled rdkit.Chem.Mol object.
    """
    transformed_rdmol = Chem.Mol(rdmol)
    center = AllChem.ComputeCentroid(transformed_rdmol.GetConformer())
    tf = np.identity(4, np.float)
    tf[0][3] -= center[0]
    tf[1][3] -= center[1]
    tf[0][0] = tf[1][1] = tf[2][2] = factor
    AllChem.TransformMol(transformed_rdmol, tf)
    return transformed_rdmol


def rotation_matrix(axis:str, degree:float) -> np.ndarray:
    """Returns a numpy rotation matrix of shape (4,4).
    
    Args:
        axis (str): 'x' or 'y' or 'z'.
        degree (float): degree of rotation.

    Returns:
        np.ndarray: a numpy array of shape (4,4).
    """
    rad = (np.pi/180.0) * degree
    c = np.cos(rad)
    s = np.sin(rad)
    if axis.lower() == 'x':
        return np.array([
            [1., 0., 0., 0.],
            [0., c, -s,  0.],
            [0., s,  c,  0.],
            [0., 0., 0., 1.],
            ])
    elif axis.lower() == 'y':
        return np.array([
            [ c,  0., s,  0.],
            [ 0., 1., 0., 0.],
            [-s,  0., c,  0.],
            [ 0., 0., 0., 1.],
            ])
    elif axis.lower() == 'z':
        return np.array([
            [c, -s,  0., 0.],
            [s,  c,  0., 0.],
            [0., 0., 1., 0.],
            [0., 0., 0., 1.],
            ])


def rotate(rdmol:Chem.Mol, axis:str, degree:float) -> None:
    """Rotate `rdmol` around given axis and degree.

    Input `rdmol` will be modified.

    Args:
        rdmol (Chem.Mol): input molecule.
        axis (str): axis of rotation, 'x' or 'y' or 'z'.
        degree (float): degree of rotation.
    """
    try:
        conf = rdmol.GetConformer()
    except:
        AllChem.Compute2DCoords(rdmol)
        conf = rdmol.GetConformer()
    R = rotation_matrix(axis, degree)
    rdMolTransforms.TransformConformer(conf, R)
