"""
Descriptors derived from a molecule's 3D structure

"""
from __future__ import annotations
from rdkix.Chem.Descriptors import _isCallable
from rdkix.Chem import rdMolDescriptors
__all__ = ['CalcMolDescriptors3D', 'descList', 'rdMolDescriptors']
def CalcMolDescriptors3D(mol, confId = None):
    """
    
    Compute all 3D descriptors of a molecule
    
    Arguments:
    - mol: the molecule to work with
    - confId: conformer ID to work with. If not specified the default (-1) is used
    
    Return:
    
    dict
        A dictionary with decriptor names as keys and the descriptor values as values
    
    raises a ValueError 
        If the molecule does not have conformers
    """
def _setupDescriptors(namespace):
    ...
descList: list  # value = [('PMI1', <function <lambda> at 0xffeb3d9a2e80>), ('PMI2', <function <lambda> at 0xffeb3d9a3060>), ('PMI3', <function <lambda> at 0xffeb3d9a36a0>), ('NPR1', <function <lambda> at 0xffeb3d9a3740>), ('NPR2', <function <lambda> at 0xffeb3d9a37e0>), ('RadiusOfGyration', <function <lambda> at 0xffeb3d9a3880>), ('InertialShapeFactor', <function <lambda> at 0xffeb3d9a3920>), ('Eccentricity', <function <lambda> at 0xffeb3d9a39c0>), ('Asphericity', <function <lambda> at 0xffeb3d9a3a60>), ('SpherocityIndex', <function <lambda> at 0xffeb3d9a3b00>), ('PBF', <function <lambda> at 0xffeb3d9a3ba0>)]
