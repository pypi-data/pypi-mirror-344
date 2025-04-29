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
descList: list  # value = [('PMI1', <function <lambda> at 0x1045e0160>), ('PMI2', <function <lambda> at 0x1096ee790>), ('PMI3', <function <lambda> at 0x1096ee820>), ('NPR1', <function <lambda> at 0x1096ee8b0>), ('NPR2', <function <lambda> at 0x1096ee940>), ('RadiusOfGyration', <function <lambda> at 0x1096ee9d0>), ('InertialShapeFactor', <function <lambda> at 0x1096eea60>), ('Eccentricity', <function <lambda> at 0x1096eeaf0>), ('Asphericity', <function <lambda> at 0x1096eeb80>), ('SpherocityIndex', <function <lambda> at 0x1096eec10>), ('PBF', <function <lambda> at 0x1096eeca0>)]
