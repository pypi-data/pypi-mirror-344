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
descList: list  # value = [('PMI1', <function <lambda> at 0x1054e9f80>), ('PMI2', <function <lambda> at 0x1054ea660>), ('PMI3', <function <lambda> at 0x1054ea700>), ('NPR1', <function <lambda> at 0x1054ea7a0>), ('NPR2', <function <lambda> at 0x1054ea840>), ('RadiusOfGyration', <function <lambda> at 0x1054ea8e0>), ('InertialShapeFactor', <function <lambda> at 0x1054ea980>), ('Eccentricity', <function <lambda> at 0x1054eaa20>), ('Asphericity', <function <lambda> at 0x1054eaac0>), ('SpherocityIndex', <function <lambda> at 0x1054eab60>), ('PBF', <function <lambda> at 0x1054eac00>)]
