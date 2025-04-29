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
descList: list  # value = [('PMI1', <function <lambda> at 0xff1a11fef560>), ('PMI2', <function <lambda> at 0xff1a11fefc40>), ('PMI3', <function <lambda> at 0xff1a11fefce0>), ('NPR1', <function <lambda> at 0xff1a11fefd80>), ('NPR2', <function <lambda> at 0xff1a11fefe20>), ('RadiusOfGyration', <function <lambda> at 0xff1a11fefec0>), ('InertialShapeFactor', <function <lambda> at 0xff1a11feff60>), ('Eccentricity', <function <lambda> at 0xff1a0ece8040>), ('Asphericity', <function <lambda> at 0xff1a0ece80e0>), ('SpherocityIndex', <function <lambda> at 0xff1a0ece8180>), ('PBF', <function <lambda> at 0xff1a0ece8220>)]
