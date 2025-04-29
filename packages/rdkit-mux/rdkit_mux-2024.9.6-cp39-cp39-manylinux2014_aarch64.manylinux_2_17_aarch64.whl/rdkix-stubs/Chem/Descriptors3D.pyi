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
descList: list  # value = [('PMI1', <function <lambda> at 0xff5048b59940>), ('PMI2', <function <lambda> at 0xff503acb2d30>), ('PMI3', <function <lambda> at 0xff503acb2dc0>), ('NPR1', <function <lambda> at 0xff503acb2e50>), ('NPR2', <function <lambda> at 0xff503acb2ee0>), ('RadiusOfGyration', <function <lambda> at 0xff503acb2f70>), ('InertialShapeFactor', <function <lambda> at 0xff503acc3040>), ('Eccentricity', <function <lambda> at 0xff503acc30d0>), ('Asphericity', <function <lambda> at 0xff503acc3160>), ('SpherocityIndex', <function <lambda> at 0xff503acc31f0>), ('PBF', <function <lambda> at 0xff503acc3280>)]
