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
descList: list  # value = [('PMI1', <function <lambda> at 0x1012e6660>), ('PMI2', <function <lambda> at 0x1042dd120>), ('PMI3', <function <lambda> at 0x1042dd260>), ('NPR1', <function <lambda> at 0x1042dd300>), ('NPR2', <function <lambda> at 0x1042dd3a0>), ('RadiusOfGyration', <function <lambda> at 0x1042dd440>), ('InertialShapeFactor', <function <lambda> at 0x1042dd4e0>), ('Eccentricity', <function <lambda> at 0x1042dd580>), ('Asphericity', <function <lambda> at 0x1042dd620>), ('SpherocityIndex', <function <lambda> at 0x1042dd6c0>), ('PBF', <function <lambda> at 0x1042dd760>)]
