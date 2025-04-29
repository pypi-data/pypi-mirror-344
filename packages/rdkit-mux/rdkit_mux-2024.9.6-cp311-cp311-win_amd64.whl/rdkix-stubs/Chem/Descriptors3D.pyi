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
descList: list  # value = [('PMI1', <function <lambda> at 0x00000258A49D8220>), ('PMI2', <function <lambda> at 0x00000258A49D8860>), ('PMI3', <function <lambda> at 0x00000258A49D89A0>), ('NPR1', <function <lambda> at 0x00000258A49D8A40>), ('NPR2', <function <lambda> at 0x00000258A49D8AE0>), ('RadiusOfGyration', <function <lambda> at 0x00000258A49D8B80>), ('InertialShapeFactor', <function <lambda> at 0x00000258A49D8C20>), ('Eccentricity', <function <lambda> at 0x00000258A49D8CC0>), ('Asphericity', <function <lambda> at 0x00000258A49D8D60>), ('SpherocityIndex', <function <lambda> at 0x00000258A49D8E00>), ('PBF', <function <lambda> at 0x00000258A49D8EA0>)]
