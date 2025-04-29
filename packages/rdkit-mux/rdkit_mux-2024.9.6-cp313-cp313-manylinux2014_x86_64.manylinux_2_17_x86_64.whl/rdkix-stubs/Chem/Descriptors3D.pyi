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
descList: list  # value = [('PMI1', <function <lambda> at 0x7fa741c3ede0>), ('PMI2', <function <lambda> at 0x7fa741c3efc0>), ('PMI3', <function <lambda> at 0x7fa741c3f600>), ('NPR1', <function <lambda> at 0x7fa741c3f6a0>), ('NPR2', <function <lambda> at 0x7fa741c3f740>), ('RadiusOfGyration', <function <lambda> at 0x7fa741c3f7e0>), ('InertialShapeFactor', <function <lambda> at 0x7fa741c3f880>), ('Eccentricity', <function <lambda> at 0x7fa741c3f920>), ('Asphericity', <function <lambda> at 0x7fa741c3f9c0>), ('SpherocityIndex', <function <lambda> at 0x7fa741c3fa60>), ('PBF', <function <lambda> at 0x7fa741c3fb00>)]
