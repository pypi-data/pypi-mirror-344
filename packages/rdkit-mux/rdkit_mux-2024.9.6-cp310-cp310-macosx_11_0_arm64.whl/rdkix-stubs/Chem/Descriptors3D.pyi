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
descList: list  # value = [('PMI1', <function <lambda> at 0x104f36c20>), ('PMI2', <function <lambda> at 0x107d5eef0>), ('PMI3', <function <lambda> at 0x107d5ef80>), ('NPR1', <function <lambda> at 0x107d5f010>), ('NPR2', <function <lambda> at 0x107d5f0a0>), ('RadiusOfGyration', <function <lambda> at 0x107d5f130>), ('InertialShapeFactor', <function <lambda> at 0x107d5f1c0>), ('Eccentricity', <function <lambda> at 0x107d5f250>), ('Asphericity', <function <lambda> at 0x107d5f2e0>), ('SpherocityIndex', <function <lambda> at 0x107d5f370>), ('PBF', <function <lambda> at 0x107d5f400>)]
