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
descList: list  # value = [('PMI1', <function <lambda> at 0xfff30b25bf60>), ('PMI2', <function <lambda> at 0xfff2fba33740>), ('PMI3', <function <lambda> at 0xfff2fba33880>), ('NPR1', <function <lambda> at 0xfff2fba33920>), ('NPR2', <function <lambda> at 0xfff2fba339c0>), ('RadiusOfGyration', <function <lambda> at 0xfff2fba33a60>), ('InertialShapeFactor', <function <lambda> at 0xfff2fba33b00>), ('Eccentricity', <function <lambda> at 0xfff2fba33ba0>), ('Asphericity', <function <lambda> at 0xfff2fba33c40>), ('SpherocityIndex', <function <lambda> at 0xfff2fba33ce0>), ('PBF', <function <lambda> at 0xfff2fba33d80>)]
