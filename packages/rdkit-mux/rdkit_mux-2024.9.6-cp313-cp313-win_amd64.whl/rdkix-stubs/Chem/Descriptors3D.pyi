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
descList: list  # value = [('PMI1', <function <lambda> at 0x000001FCD4BF5E40>), ('PMI2', <function <lambda> at 0x000001FCD4BF65C0>), ('PMI3', <function <lambda> at 0x000001FCD4BF6660>), ('NPR1', <function <lambda> at 0x000001FCD4BF6700>), ('NPR2', <function <lambda> at 0x000001FCD4BF67A0>), ('RadiusOfGyration', <function <lambda> at 0x000001FCD4BF6840>), ('InertialShapeFactor', <function <lambda> at 0x000001FCD4BF68E0>), ('Eccentricity', <function <lambda> at 0x000001FCD4BF6980>), ('Asphericity', <function <lambda> at 0x000001FCD4BF6A20>), ('SpherocityIndex', <function <lambda> at 0x000001FCD4BF6AC0>), ('PBF', <function <lambda> at 0x000001FCD4BF6B60>)]
