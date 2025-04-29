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
descList: list  # value = [('PMI1', <function <lambda> at 0x109412660>), ('PMI2', <function <lambda> at 0x109412ca0>), ('PMI3', <function <lambda> at 0x109412d40>), ('NPR1', <function <lambda> at 0x109412de0>), ('NPR2', <function <lambda> at 0x109412e80>), ('RadiusOfGyration', <function <lambda> at 0x109412f20>), ('InertialShapeFactor', <function <lambda> at 0x109412fc0>), ('Eccentricity', <function <lambda> at 0x109413060>), ('Asphericity', <function <lambda> at 0x109413100>), ('SpherocityIndex', <function <lambda> at 0x1094131a0>), ('PBF', <function <lambda> at 0x109413240>)]
