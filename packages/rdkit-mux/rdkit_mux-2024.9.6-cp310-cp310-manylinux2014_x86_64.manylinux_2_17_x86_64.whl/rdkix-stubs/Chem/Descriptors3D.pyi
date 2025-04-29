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
descList: list  # value = [('PMI1', <function <lambda> at 0x7f50918569e0>), ('PMI2', <function <lambda> at 0x7f50813a7d90>), ('PMI3', <function <lambda> at 0x7f50813a7e20>), ('NPR1', <function <lambda> at 0x7f50813a7eb0>), ('NPR2', <function <lambda> at 0x7f50813a7f40>), ('RadiusOfGyration', <function <lambda> at 0x7f5081418040>), ('InertialShapeFactor', <function <lambda> at 0x7f50814180d0>), ('Eccentricity', <function <lambda> at 0x7f5081418160>), ('Asphericity', <function <lambda> at 0x7f50814181f0>), ('SpherocityIndex', <function <lambda> at 0x7f5081418280>), ('PBF', <function <lambda> at 0x7f5081418310>)]
