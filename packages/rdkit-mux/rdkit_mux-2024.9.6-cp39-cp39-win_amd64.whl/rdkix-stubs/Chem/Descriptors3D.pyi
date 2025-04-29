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
descList: list  # value = [('PMI1', <function <lambda> at 0x0000026509F97A60>), ('PMI2', <function <lambda> at 0x0000026512239670>), ('PMI3', <function <lambda> at 0x0000026512239700>), ('NPR1', <function <lambda> at 0x0000026512239790>), ('NPR2', <function <lambda> at 0x0000026512239820>), ('RadiusOfGyration', <function <lambda> at 0x00000265122398B0>), ('InertialShapeFactor', <function <lambda> at 0x0000026512239940>), ('Eccentricity', <function <lambda> at 0x00000265122399D0>), ('Asphericity', <function <lambda> at 0x0000026512239A60>), ('SpherocityIndex', <function <lambda> at 0x0000026512239AF0>), ('PBF', <function <lambda> at 0x0000026512239B80>)]
