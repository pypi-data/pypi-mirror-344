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
descList: list  # value = [('PMI1', <function <lambda> at 0x000002319AB97DC0>), ('PMI2', <function <lambda> at 0x00000231A18199D0>), ('PMI3', <function <lambda> at 0x00000231A1819A60>), ('NPR1', <function <lambda> at 0x00000231A1819AF0>), ('NPR2', <function <lambda> at 0x00000231A1819B80>), ('RadiusOfGyration', <function <lambda> at 0x00000231A1819C10>), ('InertialShapeFactor', <function <lambda> at 0x00000231A1819CA0>), ('Eccentricity', <function <lambda> at 0x00000231A1819D30>), ('Asphericity', <function <lambda> at 0x00000231A1819DC0>), ('SpherocityIndex', <function <lambda> at 0x00000231A1819E50>), ('PBF', <function <lambda> at 0x00000231A1819EE0>)]
