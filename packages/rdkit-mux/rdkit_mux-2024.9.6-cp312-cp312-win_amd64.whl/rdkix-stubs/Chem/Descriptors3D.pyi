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
descList: list  # value = [('PMI1', <function <lambda> at 0x0000025C98965C60>), ('PMI2', <function <lambda> at 0x0000025C98966340>), ('PMI3', <function <lambda> at 0x0000025C989663E0>), ('NPR1', <function <lambda> at 0x0000025C98966480>), ('NPR2', <function <lambda> at 0x0000025C98966520>), ('RadiusOfGyration', <function <lambda> at 0x0000025C989665C0>), ('InertialShapeFactor', <function <lambda> at 0x0000025C98966660>), ('Eccentricity', <function <lambda> at 0x0000025C98966700>), ('Asphericity', <function <lambda> at 0x0000025C989667A0>), ('SpherocityIndex', <function <lambda> at 0x0000025C98966840>), ('PBF', <function <lambda> at 0x0000025C989668E0>)]
