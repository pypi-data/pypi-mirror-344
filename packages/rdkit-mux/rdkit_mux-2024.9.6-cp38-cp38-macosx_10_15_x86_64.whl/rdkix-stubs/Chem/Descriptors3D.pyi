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
descList: list  # value = [('PMI1', <function <lambda> at 0x7fed687a9550>), ('PMI2', <function <lambda> at 0x7fed697a4160>), ('PMI3', <function <lambda> at 0x7fed697a41f0>), ('NPR1', <function <lambda> at 0x7fed697a4280>), ('NPR2', <function <lambda> at 0x7fed697a4310>), ('RadiusOfGyration', <function <lambda> at 0x7fed697a43a0>), ('InertialShapeFactor', <function <lambda> at 0x7fed697a4430>), ('Eccentricity', <function <lambda> at 0x7fed697a44c0>), ('Asphericity', <function <lambda> at 0x7fed697a4550>), ('SpherocityIndex', <function <lambda> at 0x7fed697a45e0>), ('PBF', <function <lambda> at 0x7fed697a4670>)]
