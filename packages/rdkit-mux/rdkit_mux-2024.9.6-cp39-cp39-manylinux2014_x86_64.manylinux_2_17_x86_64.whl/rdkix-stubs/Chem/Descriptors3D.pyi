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
descList: list  # value = [('PMI1', <function <lambda> at 0x7f682d7faa60>), ('PMI2', <function <lambda> at 0x7f681e197e50>), ('PMI3', <function <lambda> at 0x7f681e197ee0>), ('NPR1', <function <lambda> at 0x7f681e197f70>), ('NPR2', <function <lambda> at 0x7f681e1af040>), ('RadiusOfGyration', <function <lambda> at 0x7f681e1af0d0>), ('InertialShapeFactor', <function <lambda> at 0x7f681e1af160>), ('Eccentricity', <function <lambda> at 0x7f681e1af1f0>), ('Asphericity', <function <lambda> at 0x7f681e1af280>), ('SpherocityIndex', <function <lambda> at 0x7f681e1af310>), ('PBF', <function <lambda> at 0x7f681e1af3a0>)]
