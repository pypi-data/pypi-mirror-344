"""
Module containing classes and functions for working with chemical reactions.
"""
from __future__ import annotations
import rdkix.Chem
import typing
__all__ = ['CartesianProductStrategy', 'ChemicalReaction', 'Compute2DCoordsForReaction', 'CreateDifferenceFingerprintForReaction', 'CreateStructuralFingerprintForReaction', 'EnumerateLibrary', 'EnumerateLibraryBase', 'EnumerateLibraryCanSerialize', 'EnumerationParams', 'EnumerationStrategyBase', 'EvenSamplePairsStrategy', 'FingerprintType', 'GetChemDrawRxnAdjustParams', 'GetDefaultAdjustParams', 'HasAgentTemplateSubstructMatch', 'HasProductTemplateSubstructMatch', 'HasReactantTemplateSubstructMatch', 'HasReactionAtomMapping', 'HasReactionSubstructMatch', 'IsReactionTemplateMoleculeAgent', 'MOL_SPTR_VECT', 'MatchOnlyAtRgroupsAdjustParams', 'MrvBlockIsReaction', 'MrvFileIsReaction', 'PreprocessReaction', 'RandomSampleAllBBsStrategy', 'RandomSampleStrategy', 'ReactionFingerprintParams', 'ReactionFromMolecule', 'ReactionFromMrvBlock', 'ReactionFromMrvFile', 'ReactionFromPNGFile', 'ReactionFromPNGString', 'ReactionFromRxnBlock', 'ReactionFromRxnFile', 'ReactionFromSmarts', 'ReactionMetadataToPNGFile', 'ReactionMetadataToPNGString', 'ReactionToCXSmarts', 'ReactionToCXSmiles', 'ReactionToMolecule', 'ReactionToMrvBlock', 'ReactionToMrvFile', 'ReactionToRxnBlock', 'ReactionToSmarts', 'ReactionToSmiles', 'ReactionToV3KRxnBlock', 'ReactionsFromCDXMLBlock', 'ReactionsFromCDXMLFile', 'ReduceProductToSideChains', 'RemoveMappingNumbersFromReactions', 'SANITIZE_ADJUST_REACTANTS', 'SANITIZE_ALL', 'SANITIZE_ATOM_MAPS', 'SANITIZE_MERGEHS', 'SANITIZE_NONE', 'SANITIZE_RGROUP_NAMES', 'SanitizeFlags', 'SanitizeRxn', 'SanitizeRxnAsMols', 'UpdateProductsStereochemistry', 'VectMolVect']
class CartesianProductStrategy(EnumerationStrategyBase):
    """
    CartesianProductStrategy produces a standard walk through all possible
    reagent combinations:
    
    (0,0,0), (1,0,0), (2,0,0) ...
    """
    __instance_size__: typing.ClassVar[int] = 40
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def __copy__(self) -> EnumerationStrategyBase:
        """
            C++ signature :
                class RDKix::EnumerationStrategyBase * __ptr64 __copy__(class RDKix::CartesianProductStrategy {lvalue})
        """
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64)
        """
class ChemicalReaction(Boost.Python.instance):
    """
    A class for storing and applying chemical reactions.
    
    Sample Usage:
      >>> from rdkix import Chem
      >>> from rdkix.Chem import rdChemReactions
      >>> rxn = rdChemReactions.ReactionFromSmarts('[C:1](=[O:2])O.[N:3]>>[C:1](=[O:2])[N:3]')
      >>> reacts = (Chem.MolFromSmiles('C(=O)O'),Chem.MolFromSmiles('CNC'))
      >>> products = rxn.RunReactants(reacts)
      >>> len(products)
      1
      >>> len(products[0])
      1
      >>> Chem.MolToSmiles(products[0][0])
      'CN(C)C=O'
    """
    __getstate_manages_dict__: typing.ClassVar[bool] = True
    __instance_size__: typing.ClassVar[int] = 40
    __safe_for_unpickling__: typing.ClassVar[bool] = True
    @staticmethod
    def AddRecursiveQueriesToReaction(reaction: ChemicalReaction, queries: dict = {}, propName: str = 'molFileValue', getLabels: bool = False) -> typing.Any:
        """
            adds recursive queries and returns reactant labels
        
            C++ signature :
                class boost::python::api::object AddRecursiveQueriesToReaction(class RDKix::ChemicalReaction {lvalue} [,class boost::python::dict={} [,class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >='molFileValue' [,bool=False]]])
        """
    @staticmethod
    def GetPropNames(*args, **kwargs) -> ...:
        """
            Returns a tuple with all property names for this reaction.
            
              ARGUMENTS:
                - includePrivate: (optional) toggles inclusion of private properties in the result set.
                                  Defaults to 0.
                - includeComputed: (optional) toggles inclusion of computed properties in the result set.
                                  Defaults to 0.
            
              RETURNS: a tuple of strings
            
        
            C++ signature :
                class std::vector<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >,class std::allocator<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > > > GetPropNames(class RDKix::ChemicalReaction {lvalue} [,bool=False [,bool=False]])
        """
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def AddAgentTemplate(self, mol: Mol) -> int:
        """
            adds a agent (a Molecule)
        
            C++ signature :
                unsigned int AddAgentTemplate(class RDKix::ChemicalReaction {lvalue},class boost::shared_ptr<class RDKix::ROMol>)
        """
    def AddProductTemplate(self, mol: Mol) -> int:
        """
            adds a product (a Molecule)
        
            C++ signature :
                unsigned int AddProductTemplate(class RDKix::ChemicalReaction {lvalue},class boost::shared_ptr<class RDKix::ROMol>)
        """
    def AddReactantTemplate(self, mol: Mol) -> int:
        """
            adds a reactant (a Molecule) to the reaction
        
            C++ signature :
                unsigned int AddReactantTemplate(class RDKix::ChemicalReaction {lvalue},class boost::shared_ptr<class RDKix::ROMol>)
        """
    def ClearComputedProps(self) -> None:
        """
            Removes all computed properties from the reaction.
            
            
        
            C++ signature :
                void ClearComputedProps(class RDKix::ChemicalReaction)
        """
    def ClearProp(self, key: str) -> None:
        """
            Removes a property from the reaction.
            
              ARGUMENTS:
                - key: the name of the property to clear (a string).
            
        
            C++ signature :
                void ClearProp(class RDKix::ChemicalReaction,class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >)
        """
    def GetAgentTemplate(self, which: int) -> rdkix.Chem.Mol:
        """
            returns one of our agent templates
        
            C++ signature :
                class RDKix::ROMol * __ptr64 GetAgentTemplate(class RDKix::ChemicalReaction const * __ptr64,unsigned int)
        """
    def GetAgents(self) -> MOL_SPTR_VECT:
        """
            get the agent templates
        
            C++ signature :
                class std::vector<class boost::shared_ptr<class RDKix::ROMol>,class std::allocator<class boost::shared_ptr<class RDKix::ROMol> > > GetAgents(class RDKix::ChemicalReaction {lvalue})
        """
    def GetBoolProp(self, key: str) -> bool:
        """
            Returns the Bool value of the property if possible.
            
              ARGUMENTS:
                - key: the name of the property to return (a string).
            
              RETURNS: a bool
            
              NOTE:
                - If the property has not been set, a KeyError exception will be raised.
            
        
            C++ signature :
                bool GetBoolProp(class RDKix::ChemicalReaction const * __ptr64,class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >)
        """
    def GetDoubleProp(self, key: str) -> float:
        """
            Returns the double value of the property if possible.
            
              ARGUMENTS:
                - key: the name of the property to return (a string).
            
              RETURNS: a double
            
              NOTE:
                - If the property has not been set, a KeyError exception will be raised.
            
        
            C++ signature :
                double GetDoubleProp(class RDKix::ChemicalReaction const * __ptr64,class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >)
        """
    def GetIntProp(self, key: str) -> int:
        """
            Returns the integer value of the property if possible.
            
              ARGUMENTS:
                - key: the name of the property to return (a string).
            
              RETURNS: an integer
            
              NOTE:
                - If the property has not been set, a KeyError exception will be raised.
            
        
            C++ signature :
                int GetIntProp(class RDKix::ChemicalReaction const * __ptr64,class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >)
        """
    def GetNumAgentTemplates(self) -> int:
        """
            returns the number of agents this reaction expects
        
            C++ signature :
                unsigned int GetNumAgentTemplates(class RDKix::ChemicalReaction {lvalue})
        """
    def GetNumProductTemplates(self) -> int:
        """
            returns the number of products this reaction generates
        
            C++ signature :
                unsigned int GetNumProductTemplates(class RDKix::ChemicalReaction {lvalue})
        """
    def GetNumReactantTemplates(self) -> int:
        """
            returns the number of reactants this reaction expects
        
            C++ signature :
                unsigned int GetNumReactantTemplates(class RDKix::ChemicalReaction {lvalue})
        """
    def GetProductTemplate(self, which: int) -> rdkix.Chem.Mol:
        """
            returns one of our product templates
        
            C++ signature :
                class RDKix::ROMol * __ptr64 GetProductTemplate(class RDKix::ChemicalReaction const * __ptr64,unsigned int)
        """
    def GetProducts(self) -> MOL_SPTR_VECT:
        """
            get the product templates
        
            C++ signature :
                class std::vector<class boost::shared_ptr<class RDKix::ROMol>,class std::allocator<class boost::shared_ptr<class RDKix::ROMol> > > GetProducts(class RDKix::ChemicalReaction {lvalue})
        """
    def GetProp(self, key: str) -> str:
        """
            Returns the value of the property.
            
              ARGUMENTS:
                - key: the name of the property to return (a string).
            
              RETURNS: a string
            
              NOTE:
                - If the property has not been set, a KeyError exception will be raised.
            
        
            C++ signature :
                class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > GetProp(class RDKix::ChemicalReaction const * __ptr64,class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >)
        """
    def GetPropsAsDict(self, includePrivate: bool = False, includeComputed: bool = False, autoConvertStrings: bool = True) -> dict:
        """
            Returns a dictionary populated with the reaction's properties.
             n.b. Some properties are not able to be converted to python types.
            
              ARGUMENTS:
                - includePrivate: (optional) toggles inclusion of private properties in the result set.
                                  Defaults to False.
                - includeComputed: (optional) toggles inclusion of computed properties in the result set.
                                  Defaults to False.
            
              RETURNS: a dictionary
            
        
            C++ signature :
                class boost::python::dict GetPropsAsDict(class RDKix::ChemicalReaction [,bool=False [,bool=False [,bool=True]]])
        """
    def GetReactantTemplate(self, which: int) -> rdkix.Chem.Mol:
        """
            returns one of our reactant templates
        
            C++ signature :
                class RDKix::ROMol * __ptr64 GetReactantTemplate(class RDKix::ChemicalReaction const * __ptr64,unsigned int)
        """
    def GetReactants(self) -> MOL_SPTR_VECT:
        """
            get the reactant templates
        
            C++ signature :
                class std::vector<class boost::shared_ptr<class RDKix::ROMol>,class std::allocator<class boost::shared_ptr<class RDKix::ROMol> > > GetReactants(class RDKix::ChemicalReaction {lvalue})
        """
    def GetReactingAtoms(self, mappedAtomsOnly: bool = False) -> typing.Any:
        """
            returns a sequence of sequences with the atoms that change in the reaction
        
            C++ signature :
                class boost::python::api::object GetReactingAtoms(class RDKix::ChemicalReaction [,bool=False])
        """
    def GetSubstructParams(self) -> rdkix.Chem.SubstructMatchParameters:
        """
            get the parameter object controlling the substructure matching
        
            C++ signature :
                struct RDKix::SubstructMatchParameters * __ptr64 GetSubstructParams(class RDKix::ChemicalReaction {lvalue})
        """
    def GetUnsignedProp(self, key: str) -> int:
        """
            Returns the unsigned int value of the property if possible.
            
              ARGUMENTS:
                - key: the name of the property to return (a string).
            
              RETURNS: an unsigned integer
            
              NOTE:
                - If the property has not been set, a KeyError exception will be raised.
            
        
            C++ signature :
                unsigned int GetUnsignedProp(class RDKix::ChemicalReaction const * __ptr64,class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >)
        """
    def HasProp(self, key: str) -> int:
        """
            Queries a molecule to see if a particular property has been assigned.
            
              ARGUMENTS:
                - key: the name of the property to check for (a string).
            
        
            C++ signature :
                int HasProp(class RDKix::ChemicalReaction,class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >)
        """
    def Initialize(self, silent: bool = False) -> None:
        """
            initializes the reaction so that it can be used
        
            C++ signature :
                void Initialize(class RDKix::ChemicalReaction {lvalue} [,bool=False])
        """
    def IsInitialized(self) -> bool:
        """
            checks if the reaction is ready for use
        
            C++ signature :
                bool IsInitialized(class RDKix::ChemicalReaction {lvalue})
        """
    def IsMoleculeAgent(self, mol: Mol) -> bool:
        """
            returns whether or not the molecule has a substructure match to one of the agents.
        
            C++ signature :
                bool IsMoleculeAgent(class RDKix::ChemicalReaction,class RDKix::ROMol)
        """
    def IsMoleculeProduct(self, mol: Mol) -> bool:
        """
            returns whether or not the molecule has a substructure match to one of the products.
        
            C++ signature :
                bool IsMoleculeProduct(class RDKix::ChemicalReaction,class RDKix::ROMol)
        """
    def IsMoleculeReactant(self, mol: Mol) -> bool:
        """
            returns whether or not the molecule has a substructure match to one of the reactants.
        
            C++ signature :
                bool IsMoleculeReactant(class RDKix::ChemicalReaction,class RDKix::ROMol)
        """
    def RemoveAgentTemplates(self, targetList: typing.Any = None) -> None:
        """
            Removes agents from reaction. If targetList is provide the agents will be transferred to that list.
        
            C++ signature :
                void RemoveAgentTemplates(class RDKix::ChemicalReaction {lvalue} [,class boost::python::api::object=None])
        """
    def RemoveUnmappedProductTemplates(self, thresholdUnmappedAtoms: float = 0.2, moveToAgentTemplates: bool = True, targetList: typing.Any = None) -> None:
        """
            Removes molecules with an atom mapping ratio below thresholdUnmappedAtoms from product templates to the agent templates or to a given targetList
        
            C++ signature :
                void RemoveUnmappedProductTemplates(class RDKix::ChemicalReaction * __ptr64 [,double=0.2 [,bool=True [,class boost::python::api::object=None]]])
        """
    def RemoveUnmappedReactantTemplates(self, thresholdUnmappedAtoms: float = 0.2, moveToAgentTemplates: bool = True, targetList: typing.Any = None) -> None:
        """
            Removes molecules with an atom mapping ratio below thresholdUnmappedAtoms from reactant templates to the agent templates or to a given targetList
        
            C++ signature :
                void RemoveUnmappedReactantTemplates(class RDKix::ChemicalReaction * __ptr64 [,double=0.2 [,bool=True [,class boost::python::api::object=None]]])
        """
    def RunReactant(self, reactant: typing.Any, reactionIdx: int) -> typing.Any:
        """
            apply the reaction to a single reactant
        
            C++ signature :
                struct _object * __ptr64 RunReactant(class RDKix::ChemicalReaction * __ptr64,class boost::python::api::object,unsigned int)
        """
    def RunReactantInPlace(self, reactant: Mol, removeUnmatchedAtoms: bool = True) -> bool:
        """
            apply the reaction to a single reactant in place. The reactant itself is modified. This can only be used for single reactant - single product reactions.
        
            C++ signature :
                bool RunReactantInPlace(class RDKix::ChemicalReaction * __ptr64,class RDKix::ROMol * __ptr64 [,bool=True])
        """
    @typing.overload
    def RunReactants(self, reactants: tuple, maxProducts: int = 1000) -> typing.Any:
        """
            apply the reaction to a sequence of reactant molecules and return the products as a tuple of tuples.  If maxProducts is not zero, stop the reaction when maxProducts have been generated [default=1000]
        
            C++ signature :
                struct _object * __ptr64 RunReactants(class RDKix::ChemicalReaction * __ptr64,class boost::python::tuple [,unsigned int=1000])
        """
    @typing.overload
    def RunReactants(self, reactants: list, maxProducts: int = 1000) -> typing.Any:
        """
            apply the reaction to a sequence of reactant molecules and return the products as a tuple of tuples.  If maxProducts is not zero, stop the reaction when maxProducts have been generated [default=1000]
        
            C++ signature :
                struct _object * __ptr64 RunReactants(class RDKix::ChemicalReaction * __ptr64,class boost::python::list [,unsigned int=1000])
        """
    def SetBoolProp(self, key: str, val: bool, computed: bool = False) -> None:
        """
            Sets a boolean valued molecular property
            
              ARGUMENTS:
                - key: the name of the property to be set (a string).
                - value: the property value as a bool.
                - computed: (optional) marks the property as being computed.
                            Defaults to False.
            
            
        
            C++ signature :
                void SetBoolProp(class RDKix::ChemicalReaction,class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >,bool [,bool=False])
        """
    def SetDoubleProp(self, key: str, val: float, computed: bool = False) -> None:
        """
            Sets a double valued molecular property
            
              ARGUMENTS:
                - key: the name of the property to be set (a string).
                - value: the property value as a double.
                - computed: (optional) marks the property as being computed.
                            Defaults to 0.
            
            
        
            C++ signature :
                void SetDoubleProp(class RDKix::ChemicalReaction,class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >,double [,bool=False])
        """
    def SetIntProp(self, key: str, val: int, computed: bool = False) -> None:
        """
            Sets an integer valued molecular property
            
              ARGUMENTS:
                - key: the name of the property to be set (an unsigned number).
                - value: the property value as an integer.
                - computed: (optional) marks the property as being computed.
                            Defaults to False.
            
            
        
            C++ signature :
                void SetIntProp(class RDKix::ChemicalReaction,class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >,int [,bool=False])
        """
    def SetProp(self, key: str, val: str, computed: bool = False) -> None:
        """
            Sets a molecular property
            
              ARGUMENTS:
                - key: the name of the property to be set (a string).
                - value: the property value (a string).
                - computed: (optional) marks the property as being computed.
                            Defaults to False.
            
            
        
            C++ signature :
                void SetProp(class RDKix::ChemicalReaction,class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >,class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > [,bool=False])
        """
    def SetUnsignedProp(self, key: str, val: int, computed: bool = False) -> None:
        """
            Sets an unsigned integer valued molecular property
            
              ARGUMENTS:
                - key: the name of the property to be set (a string).
                - value: the property value as an unsigned integer.
                - computed: (optional) marks the property as being computed.
                            Defaults to False.
            
            
        
            C++ signature :
                void SetUnsignedProp(class RDKix::ChemicalReaction,class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >,unsigned int [,bool=False])
        """
    @typing.overload
    def ToBinary(self) -> typing.Any:
        """
            Returns a binary string representation of the reaction.
        
            C++ signature :
                class boost::python::api::object ToBinary(class RDKix::ChemicalReaction)
        """
    @typing.overload
    def ToBinary(self, propertyFlags: int) -> typing.Any:
        """
            Returns a binary string representation of the reaction.
        
            C++ signature :
                class boost::python::api::object ToBinary(class RDKix::ChemicalReaction,unsigned int)
        """
    def Validate(self, silent: bool = False) -> tuple:
        """
            checks the reaction for potential problems, returns (numWarnings,numErrors)
        
            C++ signature :
                class boost::python::tuple Validate(class RDKix::ChemicalReaction const * __ptr64 [,bool=False])
        """
    def __getinitargs__(self) -> tuple:
        """
            C++ signature :
                class boost::python::tuple __getinitargs__(class RDKix::ChemicalReaction)
        """
    def __getstate__(self) -> tuple:
        """
            C++ signature :
                class boost::python::tuple __getstate__(class boost::python::api::object)
        """
    @typing.overload
    def __init__(self) -> None:
        """
            Constructor, takes no arguments
        
            C++ signature :
                void __init__(struct _object * __ptr64)
        """
    @typing.overload
    def __init__(self, binStr: str) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64,class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >)
        """
    @typing.overload
    def __init__(self, other: ChemicalReaction) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64,class RDKix::ChemicalReaction)
        """
    def __setstate__(self, data: tuple) -> None:
        """
            C++ signature :
                void __setstate__(class boost::python::api::object,class boost::python::tuple)
        """
    def _getImplicitPropertiesFlag(self) -> bool:
        """
            EXPERT USER: returns whether or not the reaction can have implicit properties
        
            C++ signature :
                bool _getImplicitPropertiesFlag(class RDKix::ChemicalReaction {lvalue})
        """
    def _setImplicitPropertiesFlag(self, val: bool) -> None:
        """
            EXPERT USER: indicates that the reaction can have implicit properties
        
            C++ signature :
                void _setImplicitPropertiesFlag(class RDKix::ChemicalReaction {lvalue},bool)
        """
class EnumerateLibrary(EnumerateLibraryBase):
    """
    EnumerateLibrary
    This class allows easy enumeration of reactions.  Simply provide a reaction
    and a set of reagents and you are off the races.
    
    Note that this functionality should be considered beta and that the API may
    change in a future release.
    
    EnumerateLibrary follows the python enumerator protocol, for example:
    
    library = EnumerateLibrary(rxn, bbs)
    for products in library:
       ... do something with the product
    
    It is useful to sanitize reactions before hand:
    
    SanitizeRxn(rxn)
    library = EnumerateLibrary(rxn, bbs)
    
    If ChemDraw style reaction semantics are prefereed, you can apply
    the ChemDraw parameters:
    
    SanitizeRxn(rxn, params=GetChemDrawRxnAdjustParams())
    
    For one, this enforces only matching RGroups and assumes all atoms
    have fully satisfied valences.
    
    Each product has the same output as applying a set of reagents to
    the libraries reaction.
    
    This can be a bit confusing as each product can have multiple molecules
    generated.  The returned data structure is as follows:
    
       [ [products1], [products2],... ]
    Where products1 are the molecule products for the reactions first product
    template and products2 are the molecule products for the second product
    template.  Since each reactant can match more than once, there may be
    multiple product molecules for each template.
    
    for products in library:
        for results_for_product_template in products:
            for mol in results_for_product_template:
                Chem.MolToSmiles(mol) # finally have a molecule!
    
    For sufficiently large libraries, using this iteration strategy is not
    recommended as the library may contain more products than atoms in the
    universe.  To help with this, you can supply an enumeration strategy.
    The default strategy is a CartesianProductStrategy which enumerates
    everything.  RandomSampleStrategy randomly samples the products but
    this strategy never terminates, however, python supplies itertools:
    
    import itertools
    library = EnumerateLibrary(rxn, bbs, rdChemReactions.RandomSampleStrategy())
    for result in itertools.islice(library, 1000):
        # do something with the first 1000 samples
    
    for result in itertools.islice(library, 1000):
        # do something with the next 1000 samples
    
    Libraries are also serializable, including their current state:
    
    s = library.Serialize()
    library2 = EnumerateLibrary()
    library2.InitFromString(s)
    for result in itertools.islice(libary2, 1000):
        # do something with the next 1000 samples
    """
    __instance_size__: typing.ClassVar[int] = 336
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def GetReagents(self) -> VectMolVect:
        """
            Return the reagents used in this library.
        
            C++ signature :
                class std::vector<class std::vector<class boost::shared_ptr<class RDKix::ROMol>,class std::allocator<class boost::shared_ptr<class RDKix::ROMol> > >,class std::allocator<class std::vector<class boost::shared_ptr<class RDKix::ROMol>,class std::allocator<class boost::shared_ptr<class RDKix::ROMol> > > > > GetReagents(class RDKix::EnumerateLibraryWrap {lvalue})
        """
    @typing.overload
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64)
        """
    @typing.overload
    def __init__(self, rxn: ChemicalReaction, reagents: list, params: EnumerationParams) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64,class RDKix::ChemicalReaction,class boost::python::list [,struct RDKix::EnumerationParams])
        """
    @typing.overload
    def __init__(self, rxn: ChemicalReaction, reagents: tuple, params: EnumerationParams) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64,class RDKix::ChemicalReaction,class boost::python::tuple [,struct RDKix::EnumerationParams])
        """
    @typing.overload
    def __init__(self, rxn: ChemicalReaction, reagents: list, enumerator: EnumerationStrategyBase, params: EnumerationParams) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64,class RDKix::ChemicalReaction,class boost::python::list,class RDKix::EnumerationStrategyBase [,struct RDKix::EnumerationParams])
        """
    @typing.overload
    def __init__(self, rxn: ChemicalReaction, reagents: tuple, enumerator: EnumerationStrategyBase, params: EnumerationParams) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64,class RDKix::ChemicalReaction,class boost::python::tuple,class RDKix::EnumerationStrategyBase [,struct RDKix::EnumerationParams])
        """
class EnumerateLibraryBase(Boost.Python.instance):
    @staticmethod
    def __init__(*args, **kwargs):
        """
        Raises an exception
        This class cannot be instantiated from Python
        """
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def GetEnumerator(self) -> EnumerationStrategyBase:
        """
            Returns the enumation strategy for the current library
        
            C++ signature :
                class RDKix::EnumerationStrategyBase GetEnumerator(class RDKix::EnumerateLibraryBase {lvalue})
        """
    def GetPosition(self) -> UnsignedLong_Vect:
        """
            Returns the current enumeration position into the reagent vectors
        
            C++ signature :
                class std::vector<unsigned __int64,class std::allocator<unsigned __int64> > GetPosition(class RDKix::EnumerateLibraryBase {lvalue})
        """
    def GetReaction(self) -> ChemicalReaction:
        """
            Returns the chemical reaction for this library
        
            C++ signature :
                class RDKix::ChemicalReaction GetReaction(class RDKix::EnumerateLibraryBase {lvalue})
        """
    def GetState(self) -> str:
        """
            Returns the current enumeration state (position) of the library.
            This position can be used to restart the library from a known position
        
            C++ signature :
                class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > GetState(class RDKix::EnumerateLibraryBase {lvalue})
        """
    def InitFromString(self, data: str) -> None:
        """
            Inititialize the library from a binary string
        
            C++ signature :
                void InitFromString(class RDKix::EnumerateLibraryBase {lvalue},class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >)
        """
    def ResetState(self) -> None:
        """
            Returns the current enumeration state (position) of the library to the start.
        
            C++ signature :
                void ResetState(class RDKix::EnumerateLibraryBase {lvalue})
        """
    def Serialize(self) -> typing.Any:
        """
            Serialize the library to a binary string.
            Note that the position in the library is serialized as well.  Care should
            be taken when serializing.  See GetState/SetState for position manipulation.
        
            C++ signature :
                class boost::python::api::object Serialize(class RDKix::EnumerateLibraryBase)
        """
    def SetState(self, state: str) -> None:
        """
            Sets the enumeration state (position) of the library.
        
            C++ signature :
                void SetState(class RDKix::EnumerateLibraryBase {lvalue},class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >)
        """
    def __bool__(self) -> bool:
        """
            C++ signature :
                bool __bool__(class RDKix::EnumerateLibraryBase * __ptr64)
        """
    def __iter__(self) -> typing.Any:
        """
            C++ signature :
                class boost::python::api::object __iter__(class boost::python::api::object)
        """
    def __next__(self) -> typing.Any:
        """
            Return the next molecule from the enumeration.
        
            C++ signature :
                struct _object * __ptr64 __next__(class RDKix::EnumerateLibraryBase * __ptr64)
        """
    def __nonzero__(self) -> bool:
        """
            C++ signature :
                bool __nonzero__(class RDKix::EnumerateLibraryBase * __ptr64)
        """
    def next(self) -> typing.Any:
        """
            Return the next molecule from the enumeration.
        
            C++ signature :
                struct _object * __ptr64 next(class RDKix::EnumerateLibraryBase * __ptr64)
        """
    def nextSmiles(self) -> VectorOfStringVectors:
        """
            Return the next smiles string from the enumeration.
        
            C++ signature :
                class std::vector<class std::vector<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >,class std::allocator<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > > >,class std::allocator<class std::vector<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >,class std::allocator<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > > > > > nextSmiles(class RDKix::EnumerateLibraryBase {lvalue})
        """
class EnumerationParams(Boost.Python.instance):
    """
    EnumerationParams
    Controls some aspects of how the enumeration is performed.
    Options:
      reagentMaxMatchCount [ default Infinite ]
        This specifies how many times the reactant template can match a reagent.
    
      sanePartialProducts [default false]
        If true, forces all products of the reagent plus the product templates
         pass chemical sanitization.  Note that if the product template itself
         does not pass sanitization, then none of the products will.
    """
    __instance_size__: typing.ClassVar[int] = 40
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64)
        """
    @property
    def reagentMaxMatchCount(*args, **kwargs):
        ...
    @reagentMaxMatchCount.setter
    def reagentMaxMatchCount(*args, **kwargs):
        ...
    @property
    def sanePartialProducts(*args, **kwargs):
        ...
    @sanePartialProducts.setter
    def sanePartialProducts(*args, **kwargs):
        ...
class EnumerationStrategyBase(Boost.Python.instance):
    @staticmethod
    def __init__(*args, **kwargs):
        """
        Raises an exception
        This class cannot be instantiated from Python
        """
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def GetNumPermutations(self) -> int:
        """
            Returns the total number of results for this enumeration strategy.
            Note that some strategies are effectively infinite.
        
            C++ signature :
                unsigned __int64 GetNumPermutations(class RDKix::EnumerationStrategyBase {lvalue})
        """
    def GetPosition(self) -> UnsignedLong_Vect:
        """
            Return the current indices into the arrays of reagents
        
            C++ signature :
                class std::vector<unsigned __int64,class std::allocator<unsigned __int64> > GetPosition(class RDKix::EnumerationStrategyBase {lvalue})
        """
    def Initialize(self, rxn: ChemicalReaction, ob: list) -> None:
        """
            C++ signature :
                void Initialize(class RDKix::EnumerationStrategyBase {lvalue},class RDKix::ChemicalReaction {lvalue},class boost::python::list)
        """
    def Skip(self, skipCount: int) -> bool:
        """
            Skip the next Nth results. note: this may be an expensive operation
            depending on the enumeration strategy used. It is recommended to use
            the enumerator state to advance to a known position
        
            C++ signature :
                bool Skip(class RDKix::EnumerationStrategyBase {lvalue},unsigned __int64)
        """
    def Type(self) -> str:
        """
            Returns the enumeration strategy type as a string.
        
            C++ signature :
                char const * __ptr64 Type(class RDKix::EnumerationStrategyBase {lvalue})
        """
    def __bool__(self) -> bool:
        """
            C++ signature :
                bool __bool__(class RDKix::EnumerationStrategyBase * __ptr64)
        """
    @typing.overload
    def __copy__(self) -> EnumerationStrategyBase:
        """
            C++ signature :
                class RDKix::EnumerationStrategyBase * __ptr64 __copy__(class RDKix::EnumerationStrategyBase {lvalue})
        """
    @typing.overload
    def __copy__(self) -> None:
        """
            C++ signature :
                void __copy__(class boost::shared_ptr<class RDKix::EnumerationStrategyBase> {lvalue})
        """
    @typing.overload
    def __next__(self) -> UnsignedLong_Vect:
        """
            Return the next indices into the arrays of reagents
        
            C++ signature :
                class std::vector<unsigned __int64,class std::allocator<unsigned __int64> > __next__(class RDKix::EnumerationStrategyBase {lvalue})
        """
    @typing.overload
    def __next__(self) -> None:
        """
            C++ signature :
                void __next__(class boost::shared_ptr<class RDKix::EnumerationStrategyBase> {lvalue})
        """
    def __nonzero__(self) -> bool:
        """
            C++ signature :
                bool __nonzero__(class RDKix::EnumerationStrategyBase * __ptr64)
        """
    @typing.overload
    def next(self) -> UnsignedLong_Vect:
        """
            Return the next indices into the arrays of reagents
        
            C++ signature :
                class std::vector<unsigned __int64,class std::allocator<unsigned __int64> > next(class RDKix::EnumerationStrategyBase {lvalue})
        """
    @typing.overload
    def next(self) -> None:
        """
            C++ signature :
                void next(class boost::shared_ptr<class RDKix::EnumerationStrategyBase> {lvalue})
        """
class EvenSamplePairsStrategy(EnumerationStrategyBase):
    """
    Randomly sample Pairs evenly from a collection of building blocks
    This is a good strategy for choosing a relatively small selection
    of building blocks from a larger set.  As the amount of work needed
    to retrieve the next evenly sample building block grows with the
    number of samples, this method performs progressively worse as the
    number of samples gets larger.
    See EnumerationStrategyBase for more details.
    """
    __instance_size__: typing.ClassVar[int] = 40
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def Stats(self) -> str:
        """
            Return the statistics log of the pairs used in the current enumeration.
        
            C++ signature :
                class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > Stats(class RDKix::EvenSamplePairsStrategy {lvalue})
        """
    def __copy__(self) -> EnumerationStrategyBase:
        """
            C++ signature :
                class RDKix::EnumerationStrategyBase * __ptr64 __copy__(class RDKix::EvenSamplePairsStrategy {lvalue})
        """
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64)
        """
class FingerprintType(Boost.Python.enum):
    AtomPairFP: typing.ClassVar[FingerprintType]  # value = rdkix.Chem.rdChemReactions.FingerprintType.AtomPairFP
    MorganFP: typing.ClassVar[FingerprintType]  # value = rdkix.Chem.rdChemReactions.FingerprintType.MorganFP
    PatternFP: typing.ClassVar[FingerprintType]  # value = rdkix.Chem.rdChemReactions.FingerprintType.PatternFP
    RDKixFP: typing.ClassVar[FingerprintType]  # value = rdkix.Chem.rdChemReactions.FingerprintType.RDKixFP
    TopologicalTorsion: typing.ClassVar[FingerprintType]  # value = rdkix.Chem.rdChemReactions.FingerprintType.TopologicalTorsion
    __slots__: typing.ClassVar[tuple] = tuple()
    names: typing.ClassVar[dict]  # value = {'AtomPairFP': rdkix.Chem.rdChemReactions.FingerprintType.AtomPairFP, 'TopologicalTorsion': rdkix.Chem.rdChemReactions.FingerprintType.TopologicalTorsion, 'MorganFP': rdkix.Chem.rdChemReactions.FingerprintType.MorganFP, 'RDKixFP': rdkix.Chem.rdChemReactions.FingerprintType.RDKixFP, 'PatternFP': rdkix.Chem.rdChemReactions.FingerprintType.PatternFP}
    values: typing.ClassVar[dict]  # value = {1: rdkix.Chem.rdChemReactions.FingerprintType.AtomPairFP, 2: rdkix.Chem.rdChemReactions.FingerprintType.TopologicalTorsion, 3: rdkix.Chem.rdChemReactions.FingerprintType.MorganFP, 4: rdkix.Chem.rdChemReactions.FingerprintType.RDKixFP, 5: rdkix.Chem.rdChemReactions.FingerprintType.PatternFP}
class MOL_SPTR_VECT(Boost.Python.instance):
    __instance_size__: typing.ClassVar[int] = 48
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def __contains__(self, item: typing.Any) -> bool:
        """
            C++ signature :
                bool __contains__(class std::vector<class boost::shared_ptr<class RDKix::ROMol>,class std::allocator<class boost::shared_ptr<class RDKix::ROMol> > > {lvalue},struct _object * __ptr64)
        """
    def __delitem__(self, item: typing.Any) -> None:
        """
            C++ signature :
                void __delitem__(class std::vector<class boost::shared_ptr<class RDKix::ROMol>,class std::allocator<class boost::shared_ptr<class RDKix::ROMol> > > {lvalue},struct _object * __ptr64)
        """
    def __getitem__(self, item: typing.Any) -> typing.Any:
        """
            C++ signature :
                class boost::python::api::object __getitem__(struct boost::python::back_reference<class std::vector<class boost::shared_ptr<class RDKix::ROMol>,class std::allocator<class boost::shared_ptr<class RDKix::ROMol> > > & __ptr64>,struct _object * __ptr64)
        """
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64)
        """
    def __iter__(self) -> typing.Any:
        """
            C++ signature :
                struct boost::python::objects::iterator_range<struct boost::python::return_value_policy<struct boost::python::return_by_value,struct boost::python::default_call_policies>,class std::_Vector_iterator<class std::_Vector_val<struct std::_Simple_types<class boost::shared_ptr<class RDKix::ROMol> > > > > __iter__(struct boost::python::back_reference<class std::vector<class boost::shared_ptr<class RDKix::ROMol>,class std::allocator<class boost::shared_ptr<class RDKix::ROMol> > > & __ptr64>)
        """
    def __len__(self) -> int:
        """
            C++ signature :
                unsigned __int64 __len__(class std::vector<class boost::shared_ptr<class RDKix::ROMol>,class std::allocator<class boost::shared_ptr<class RDKix::ROMol> > > {lvalue})
        """
    def __setitem__(self, item: typing.Any, value: typing.Any) -> None:
        """
            C++ signature :
                void __setitem__(class std::vector<class boost::shared_ptr<class RDKix::ROMol>,class std::allocator<class boost::shared_ptr<class RDKix::ROMol> > > {lvalue},struct _object * __ptr64,struct _object * __ptr64)
        """
    def append(self, item: typing.Any) -> None:
        """
            C++ signature :
                void append(class std::vector<class boost::shared_ptr<class RDKix::ROMol>,class std::allocator<class boost::shared_ptr<class RDKix::ROMol> > > {lvalue},class boost::python::api::object)
        """
    def extend(self, other: typing.Any) -> None:
        """
            C++ signature :
                void extend(class std::vector<class boost::shared_ptr<class RDKix::ROMol>,class std::allocator<class boost::shared_ptr<class RDKix::ROMol> > > {lvalue},class boost::python::api::object)
        """
class RandomSampleAllBBsStrategy(EnumerationStrategyBase):
    """
    RandomSampleAllBBsStrategy randomly samples from the reagent sets
    with the constraint that all building blocks are samples as early as possible.
    Note that this strategy never halts and can produce duplicates.
    """
    __instance_size__: typing.ClassVar[int] = 40
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def __copy__(self) -> EnumerationStrategyBase:
        """
            C++ signature :
                class RDKix::EnumerationStrategyBase * __ptr64 __copy__(class RDKix::RandomSampleAllBBsStrategy {lvalue})
        """
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64)
        """
class RandomSampleStrategy(EnumerationStrategyBase):
    """
    RandomSampleStrategy simply randomly samples from the reagent sets.
    Note that this strategy never halts and can produce duplicates.
    """
    __instance_size__: typing.ClassVar[int] = 40
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def __copy__(self) -> EnumerationStrategyBase:
        """
            C++ signature :
                class RDKix::EnumerationStrategyBase * __ptr64 __copy__(class RDKix::RandomSampleStrategy {lvalue})
        """
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64)
        """
class ReactionFingerprintParams(Boost.Python.instance):
    """
    A class for storing parameters to manipulate the calculation of fingerprints of chemical reactions.
    """
    __instance_size__: typing.ClassVar[int] = 56
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self) -> None:
        """
            Constructor, takes no arguments
        
            C++ signature :
                void __init__(struct _object * __ptr64)
        """
    @typing.overload
    def __init__(self, includeAgents: bool, bitRatioAgents: float, nonAgentWeight: int, agentWeight: int, fpSize: int, fpType: FingerprintType) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64,bool,double,unsigned int,int,unsigned int,enum RDKix::FingerprintType)
        """
    @property
    def agentWeight(*args, **kwargs):
        ...
    @agentWeight.setter
    def agentWeight(*args, **kwargs):
        ...
    @property
    def bitRatioAgents(*args, **kwargs):
        ...
    @bitRatioAgents.setter
    def bitRatioAgents(*args, **kwargs):
        ...
    @property
    def fpSize(*args, **kwargs):
        ...
    @fpSize.setter
    def fpSize(*args, **kwargs):
        ...
    @property
    def fpType(*args, **kwargs):
        ...
    @fpType.setter
    def fpType(*args, **kwargs):
        ...
    @property
    def includeAgents(*args, **kwargs):
        ...
    @includeAgents.setter
    def includeAgents(*args, **kwargs):
        ...
    @property
    def nonAgentWeight(*args, **kwargs):
        ...
    @nonAgentWeight.setter
    def nonAgentWeight(*args, **kwargs):
        ...
class SanitizeFlags(Boost.Python.enum):
    SANITIZE_ADJUST_REACTANTS: typing.ClassVar[SanitizeFlags]  # value = rdkix.Chem.rdChemReactions.SanitizeFlags.SANITIZE_ADJUST_REACTANTS
    SANITIZE_ALL: typing.ClassVar[SanitizeFlags]  # value = rdkix.Chem.rdChemReactions.SanitizeFlags.SANITIZE_ALL
    SANITIZE_ATOM_MAPS: typing.ClassVar[SanitizeFlags]  # value = rdkix.Chem.rdChemReactions.SanitizeFlags.SANITIZE_ATOM_MAPS
    SANITIZE_MERGEHS: typing.ClassVar[SanitizeFlags]  # value = rdkix.Chem.rdChemReactions.SanitizeFlags.SANITIZE_MERGEHS
    SANITIZE_NONE: typing.ClassVar[SanitizeFlags]  # value = rdkix.Chem.rdChemReactions.SanitizeFlags.SANITIZE_NONE
    SANITIZE_RGROUP_NAMES: typing.ClassVar[SanitizeFlags]  # value = rdkix.Chem.rdChemReactions.SanitizeFlags.SANITIZE_RGROUP_NAMES
    __slots__: typing.ClassVar[tuple] = tuple()
    names: typing.ClassVar[dict]  # value = {'SANITIZE_NONE': rdkix.Chem.rdChemReactions.SanitizeFlags.SANITIZE_NONE, 'SANITIZE_ATOM_MAPS': rdkix.Chem.rdChemReactions.SanitizeFlags.SANITIZE_ATOM_MAPS, 'SANITIZE_RGROUP_NAMES': rdkix.Chem.rdChemReactions.SanitizeFlags.SANITIZE_RGROUP_NAMES, 'SANITIZE_ADJUST_REACTANTS': rdkix.Chem.rdChemReactions.SanitizeFlags.SANITIZE_ADJUST_REACTANTS, 'SANITIZE_MERGEHS': rdkix.Chem.rdChemReactions.SanitizeFlags.SANITIZE_MERGEHS, 'SANITIZE_ALL': rdkix.Chem.rdChemReactions.SanitizeFlags.SANITIZE_ALL}
    values: typing.ClassVar[dict]  # value = {0: rdkix.Chem.rdChemReactions.SanitizeFlags.SANITIZE_NONE, 2: rdkix.Chem.rdChemReactions.SanitizeFlags.SANITIZE_ATOM_MAPS, 1: rdkix.Chem.rdChemReactions.SanitizeFlags.SANITIZE_RGROUP_NAMES, 4: rdkix.Chem.rdChemReactions.SanitizeFlags.SANITIZE_ADJUST_REACTANTS, 8: rdkix.Chem.rdChemReactions.SanitizeFlags.SANITIZE_MERGEHS, -1: rdkix.Chem.rdChemReactions.SanitizeFlags.SANITIZE_ALL}
class VectMolVect(Boost.Python.instance):
    __instance_size__: typing.ClassVar[int] = 48
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def __contains__(self, item: typing.Any) -> bool:
        """
            C++ signature :
                bool __contains__(class std::vector<class std::vector<class boost::shared_ptr<class RDKix::ROMol>,class std::allocator<class boost::shared_ptr<class RDKix::ROMol> > >,class std::allocator<class std::vector<class boost::shared_ptr<class RDKix::ROMol>,class std::allocator<class boost::shared_ptr<class RDKix::ROMol> > > > > {lvalue},struct _object * __ptr64)
        """
    def __delitem__(self, item: typing.Any) -> None:
        """
            C++ signature :
                void __delitem__(class std::vector<class std::vector<class boost::shared_ptr<class RDKix::ROMol>,class std::allocator<class boost::shared_ptr<class RDKix::ROMol> > >,class std::allocator<class std::vector<class boost::shared_ptr<class RDKix::ROMol>,class std::allocator<class boost::shared_ptr<class RDKix::ROMol> > > > > {lvalue},struct _object * __ptr64)
        """
    def __getitem__(self, item: typing.Any) -> typing.Any:
        """
            C++ signature :
                class boost::python::api::object __getitem__(struct boost::python::back_reference<class std::vector<class std::vector<class boost::shared_ptr<class RDKix::ROMol>,class std::allocator<class boost::shared_ptr<class RDKix::ROMol> > >,class std::allocator<class std::vector<class boost::shared_ptr<class RDKix::ROMol>,class std::allocator<class boost::shared_ptr<class RDKix::ROMol> > > > > & __ptr64>,struct _object * __ptr64)
        """
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64)
        """
    def __iter__(self) -> typing.Any:
        """
            C++ signature :
                struct boost::python::objects::iterator_range<struct boost::python::return_internal_reference<1,struct boost::python::default_call_policies>,class std::_Vector_iterator<class std::_Vector_val<struct std::_Simple_types<class std::vector<class boost::shared_ptr<class RDKix::ROMol>,class std::allocator<class boost::shared_ptr<class RDKix::ROMol> > > > > > > __iter__(struct boost::python::back_reference<class std::vector<class std::vector<class boost::shared_ptr<class RDKix::ROMol>,class std::allocator<class boost::shared_ptr<class RDKix::ROMol> > >,class std::allocator<class std::vector<class boost::shared_ptr<class RDKix::ROMol>,class std::allocator<class boost::shared_ptr<class RDKix::ROMol> > > > > & __ptr64>)
        """
    def __len__(self) -> int:
        """
            C++ signature :
                unsigned __int64 __len__(class std::vector<class std::vector<class boost::shared_ptr<class RDKix::ROMol>,class std::allocator<class boost::shared_ptr<class RDKix::ROMol> > >,class std::allocator<class std::vector<class boost::shared_ptr<class RDKix::ROMol>,class std::allocator<class boost::shared_ptr<class RDKix::ROMol> > > > > {lvalue})
        """
    def __setitem__(self, item: typing.Any, value: typing.Any) -> None:
        """
            C++ signature :
                void __setitem__(class std::vector<class std::vector<class boost::shared_ptr<class RDKix::ROMol>,class std::allocator<class boost::shared_ptr<class RDKix::ROMol> > >,class std::allocator<class std::vector<class boost::shared_ptr<class RDKix::ROMol>,class std::allocator<class boost::shared_ptr<class RDKix::ROMol> > > > > {lvalue},struct _object * __ptr64,struct _object * __ptr64)
        """
    def append(self, item: typing.Any) -> None:
        """
            C++ signature :
                void append(class std::vector<class std::vector<class boost::shared_ptr<class RDKix::ROMol>,class std::allocator<class boost::shared_ptr<class RDKix::ROMol> > >,class std::allocator<class std::vector<class boost::shared_ptr<class RDKix::ROMol>,class std::allocator<class boost::shared_ptr<class RDKix::ROMol> > > > > {lvalue},class boost::python::api::object)
        """
    def extend(self, other: typing.Any) -> None:
        """
            C++ signature :
                void extend(class std::vector<class std::vector<class boost::shared_ptr<class RDKix::ROMol>,class std::allocator<class boost::shared_ptr<class RDKix::ROMol> > >,class std::allocator<class std::vector<class boost::shared_ptr<class RDKix::ROMol>,class std::allocator<class boost::shared_ptr<class RDKix::ROMol> > > > > {lvalue},class boost::python::api::object)
        """
def Compute2DCoordsForReaction(reaction: ChemicalReaction, spacing: float = 1.0, updateProps: bool = True, canonOrient: bool = True, nFlipsPerSample: int = 0, nSample: int = 0, sampleSeed: int = 0, permuteDeg4Nodes: bool = False, bondLength: float = -1.0) -> None:
    """
        Compute 2D coordinates for a reaction. 
          ARGUMENTS: 
             - reaction - the reaction of interest
             - spacing - the amount of space left between components of the reaction
             - canonOrient - orient the reactants and products in a canonical way
             - updateProps - if set, properties such as conjugation and
                hybridization will be calculated for the reactant and product
                templates before generating coordinates. This should result in
                better depictions, but can lead to errors in some cases.
             - nFlipsPerSample - number of rotatable bonds that are
                        flipped at random at a time.
             - nSample - Number of random samplings of rotatable bonds.
             - sampleSeed - seed for the random sampling process.
             - permuteDeg4Nodes - allow permutation of bonds at a degree 4
                         node during the sampling process 
             - bondLength - change the default bond length for depiction
        
    
        C++ signature :
            void Compute2DCoordsForReaction(class RDKix::ChemicalReaction {lvalue} [,double=1.0 [,bool=True [,bool=True [,unsigned int=0 [,unsigned int=0 [,int=0 [,bool=False [,double=-1.0]]]]]]]])
    """
def CreateDifferenceFingerprintForReaction(reaction: ChemicalReaction, ReactionFingerPrintParams: ReactionFingerprintParams = ...) -> UIntSparseIntVect:
    """
        construct a difference fingerprint for a ChemicalReaction by subtracting the reactant fingerprint from the product fingerprint
    
        C++ signature :
            class RDKix::SparseIntVect<unsigned int> * __ptr64 CreateDifferenceFingerprintForReaction(class RDKix::ChemicalReaction [,struct RDKix::ReactionFingerprintParams=<rdkix.Chem.rdChemReactions.ReactionFingerprintParams object at 0x000001EECEFD1440>])
    """
def CreateStructuralFingerprintForReaction(reaction: ChemicalReaction, ReactionFingerPrintParams: ReactionFingerprintParams = ...) -> ExplicitBitVect:
    """
        construct a structural fingerprint for a ChemicalReaction by concatenating the reactant fingerprint and the product fingerprint
    
        C++ signature :
            class ExplicitBitVect * __ptr64 CreateStructuralFingerprintForReaction(class RDKix::ChemicalReaction [,struct RDKix::ReactionFingerprintParams=<rdkix.Chem.rdChemReactions.ReactionFingerprintParams object at 0x000001EECEFD1540>])
    """
def EnumerateLibraryCanSerialize() -> bool:
    """
        Returns True if the EnumerateLibrary is serializable (requires boost serialization
    
        C++ signature :
            bool EnumerateLibraryCanSerialize()
    """
def GetChemDrawRxnAdjustParams() -> rdkix.Chem.AdjustQueryParameters:
    """
        (deprecated, see MatchOnlyAtRgroupsAdjustParams)
        	Returns the chemdraw style adjustment parameters for reactant templates
    
        C++ signature :
            struct RDKix::MolOps::AdjustQueryParameters GetChemDrawRxnAdjustParams()
    """
def GetDefaultAdjustParams() -> rdkix.Chem.AdjustQueryParameters:
    """
        Returns the default adjustment parameters for reactant templates
    
        C++ signature :
            struct RDKix::MolOps::AdjustQueryParameters GetDefaultAdjustParams()
    """
def HasAgentTemplateSubstructMatch(reaction: ChemicalReaction, queryReaction: ChemicalReaction) -> bool:
    """
        tests if the agents of a queryReaction are the same as those of a reaction
    
        C++ signature :
            bool HasAgentTemplateSubstructMatch(class RDKix::ChemicalReaction,class RDKix::ChemicalReaction)
    """
def HasProductTemplateSubstructMatch(reaction: ChemicalReaction, queryReaction: ChemicalReaction) -> bool:
    """
        tests if the products of a queryReaction are substructures of the products of a reaction
    
        C++ signature :
            bool HasProductTemplateSubstructMatch(class RDKix::ChemicalReaction,class RDKix::ChemicalReaction)
    """
def HasReactantTemplateSubstructMatch(reaction: ChemicalReaction, queryReaction: ChemicalReaction) -> bool:
    """
        tests if the reactants of a queryReaction are substructures of the reactants of a reaction
    
        C++ signature :
            bool HasReactantTemplateSubstructMatch(class RDKix::ChemicalReaction,class RDKix::ChemicalReaction)
    """
def HasReactionAtomMapping(rxn: ChemicalReaction) -> bool:
    """
        tests if a reaction obtains any atom mapping
    
        C++ signature :
            bool HasReactionAtomMapping(class RDKix::ChemicalReaction)
    """
def HasReactionSubstructMatch(reaction: ChemicalReaction, queryReaction: ChemicalReaction, includeAgents: bool = False) -> bool:
    """
        tests if the queryReaction is a substructure of a reaction
    
        C++ signature :
            bool HasReactionSubstructMatch(class RDKix::ChemicalReaction,class RDKix::ChemicalReaction [,bool=False])
    """
def IsReactionTemplateMoleculeAgent(molecule: Mol, agentThreshold: float) -> bool:
    """
        tests if a molecule can be classified as an agent depending on the ratio of mapped atoms and a give threshold
    
        C++ signature :
            bool IsReactionTemplateMoleculeAgent(class RDKix::ROMol,double)
    """
def MatchOnlyAtRgroupsAdjustParams() -> rdkix.Chem.AdjustQueryParameters:
    """
        Only match at the specified rgroup locations in the reactant templates
    
        C++ signature :
            struct RDKix::MolOps::AdjustQueryParameters MatchOnlyAtRgroupsAdjustParams()
    """
def MrvBlockIsReaction(mrvData: str) -> bool:
    """
        returns whether or not an MRV block contains reaction data
    
        C++ signature :
            bool MrvBlockIsReaction(class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >)
    """
def MrvFileIsReaction(filename: str) -> bool:
    """
        returns whether or not an MRV file contains reaction data
    
        C++ signature :
            bool MrvFileIsReaction(class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >)
    """
def PreprocessReaction(reaction: ChemicalReaction, queries: dict = {}, propName: str = 'molFileValue') -> typing.Any:
    """
        A function for preprocessing reactions with more specific queries.
        Queries are indicated by labels on atoms (molFileAlias property by default)
        When these labels are found, more specific queries are placed on the atoms.
        By default, the available quieries come from 
          FilterCatalog.GetFlattenedFunctionalGroupHierarchy(True)n
        Sample Usage:
          >>> from rdkix import Chem, RDConfig
          >>> from rdkix.Chem import MolFromSmiles, AllChem
          >>> from rdkix.Chem.rdChemReactions import PreprocessReaction
          >>> import os
          >>> testFile = os.path.join(RDConfig.RDCodeDir,'Chem','SimpleEnum','test_data','boronic1.rxn')
          >>> rxn = AllChem.ReactionFromRxnFile(testFile)
          >>> rxn.Initialize()
          >>> nWarn,nError,nReacts,nProds,reactantLabels = PreprocessReaction(rxn)
          >>> nWarn
          0
          >>> nError
          0
          >>> nReacts
          2
          >>> nProds
          1
          >>> reactantLabels
          (((0, 'halogen.bromine.aromatic'),), ((1, 'boronicacid'),))
        
        If there are functional group labels in the input reaction (via atoms with molFileValue properties),
        the corresponding atoms will have queries added to them so that they only match such things. We can
        see this here:
          >>> rxn = AllChem.ReactionFromRxnFile(testFile)
          >>> rxn.Initialize()
          >>> r1 = rxn.GetReactantTemplate(0)
          >>> m1 = Chem.MolFromSmiles('CCBr')
          >>> m2 = Chem.MolFromSmiles('c1ccccc1Br')
          
        These both match because the reaction file itself just has R1-Br:
          >>> m1.HasSubstructMatch(r1)
          True
          >>> m2.HasSubstructMatch(r1)
          True
        
        After preprocessing, we only match the aromatic Br:
          >>> d = PreprocessReaction(rxn)
          >>> m1.HasSubstructMatch(r1)
          False
          >>> m2.HasSubstructMatch(r1)
          True
        
        We also support or queries in the values field (separated by commas):
          >>> testFile = os.path.join(RDConfig.RDCodeDir,'Chem','SimpleEnum','test_data','azide_reaction.rxn')
          >>> rxn = AllChem.ReactionFromRxnFile(testFile)
          >>> rxn.Initialize()
          >>> reactantLabels = PreprocessReaction(rxn)[-1]
          >>> reactantLabels
          (((1, 'azide'),), ((1, 'carboxylicacid,acidchloride'),))
          >>> m1 = Chem.MolFromSmiles('CC(=O)O')
          >>> m2 = Chem.MolFromSmiles('CC(=O)Cl')
          >>> m3 = Chem.MolFromSmiles('CC(=O)N')
          >>> r2 = rxn.GetReactantTemplate(1)
          >>> m1.HasSubstructMatch(r2)
          True
          >>> m2.HasSubstructMatch(r2)
          True
          >>> m3.HasSubstructMatch(r2)
          False
        
        unrecognized final group types are returned as None:
          >>> testFile = os.path.join(RDConfig.RDCodeDir,'Chem','SimpleEnum','test_data','bad_value1.rxn')
          >>> rxn = AllChem.ReactionFromRxnFile(testFile)
          >>> rxn.Initialize()
          >>> nWarn,nError,nReacts,nProds,reactantLabels = PreprocessReaction(rxn)
          Traceback (most recent call last):
            ...
          KeyError: 'boromicacid'
        
        One unrecognized group type in a comma-separated list makes the whole thing fail:
          >>> testFile = os.path.join(RDConfig.RDCodeDir,'Chem','SimpleEnum','test_data','bad_value2.rxn')
          >>> rxn = AllChem.ReactionFromRxnFile(testFile)
          >>> rxn.Initialize()
          >>> nWarn,nError,nReacts,nProds,reactantLabels = PreprocessReaction(rxn)
          Traceback (most recent call last):
            ...
          KeyError: 'carboxylicacid,acidchlroide'
          >>> testFile = os.path.join(RDConfig.RDCodeDir,'Chem','SimpleEnum','test_data','bad_value3.rxn')
          >>> rxn = AllChem.ReactionFromRxnFile(testFile)
          >>> rxn.Initialize()
          >>> nWarn,nError,nReacts,nProds,reactantLabels = PreprocessReaction(rxn)
          Traceback (most recent call last):
            ...
          KeyError: 'carboxyliccaid,acidchloride'
          >>> rxn = rdChemReactions.ChemicalReaction()
          >>> rxn.Initialize()
          >>> nWarn,nError,nReacts,nProds,reactantLabels = PreprocessReaction(rxn)
          >>> reactantLabels
          ()
          >>> reactantLabels == ()
          True
        
    
        C++ signature :
            class boost::python::api::object PreprocessReaction(class RDKix::ChemicalReaction {lvalue} [,class boost::python::dict={} [,class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >='molFileValue']])
    """
def ReactionFromMolecule(mol: Mol) -> ChemicalReaction:
    """
        construct a ChemicalReaction from an molecule if the RXN role property of the molecule is set
    
        C++ signature :
            class RDKix::ChemicalReaction * __ptr64 ReactionFromMolecule(class RDKix::ROMol)
    """
@typing.overload
def ReactionFromMrvBlock(rxnblock: typing.Any, sanitize: bool = False, removeHs: bool = False) -> ChemicalReaction:
    """
        construct a ChemicalReaction from a string in Marvin (mrv) format
    
        C++ signature :
            class RDKix::ChemicalReaction * __ptr64 ReactionFromMrvBlock(class boost::python::api::object [,bool=False [,bool=False]])
    """
@typing.overload
def ReactionFromMrvBlock(rxnblock: typing.Any, sanitize: bool = False, removeHs: bool = False) -> ChemicalReaction:
    """
        construct a ChemicalReaction from a string in Marvin (mrv) format
    
        C++ signature :
            class RDKix::ChemicalReaction * __ptr64 ReactionFromMrvBlock(class boost::python::api::object [,bool=False [,bool=False]])
    """
def ReactionFromMrvFile(filename: str, sanitize: bool = False, removeHs: bool = False) -> ChemicalReaction:
    """
        construct a ChemicalReaction from an Marvin (mrv) rxn file
    
        C++ signature :
            class RDKix::ChemicalReaction * __ptr64 ReactionFromMrvFile(char const * __ptr64 [,bool=False [,bool=False]])
    """
def ReactionFromPNGFile(fname: str) -> ChemicalReaction:
    """
        construct a ChemicalReaction from metadata in a PNG file
    
        C++ signature :
            class RDKix::ChemicalReaction * __ptr64 ReactionFromPNGFile(class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >)
    """
def ReactionFromPNGString(data: str) -> ChemicalReaction:
    """
        construct a ChemicalReaction from an string with PNG data
    
        C++ signature :
            class RDKix::ChemicalReaction * __ptr64 ReactionFromPNGString(class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >)
    """
def ReactionFromRxnBlock(rxnblock: str, sanitize: bool = False, removeHs: bool = False, strictParsing: bool = True) -> ChemicalReaction:
    """
        construct a ChemicalReaction from a string in MDL rxn format
    
        C++ signature :
            class RDKix::ChemicalReaction * __ptr64 ReactionFromRxnBlock(class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > [,bool=False [,bool=False [,bool=True]]])
    """
def ReactionFromRxnFile(filename: str, sanitize: bool = False, removeHs: bool = False, strictParsing: bool = True) -> ChemicalReaction:
    """
        construct a ChemicalReaction from an MDL rxn file
    
        C++ signature :
            class RDKix::ChemicalReaction * __ptr64 ReactionFromRxnFile(class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > [,bool=False [,bool=False [,bool=True]]])
    """
def ReactionFromSmarts(SMARTS: str, replacements: dict = {}, useSmiles: bool = False) -> ChemicalReaction:
    """
        construct a ChemicalReaction from a reaction SMARTS string. 
        see the documentation for rdkix.Chem.MolFromSmiles for an explanation
        of the replacements argument.
    
        C++ signature :
            class RDKix::ChemicalReaction * __ptr64 ReactionFromSmarts(char const * __ptr64 [,class boost::python::dict={} [,bool=False]])
    """
def ReactionMetadataToPNGFile(mol: ChemicalReaction, filename: typing.Any, includePkl: bool = True, includeSmiles: bool = True, includeSmarts: bool = False, includeMol: bool = False) -> typing.Any:
    """
        Reads the contents of a PNG file and adds metadata about a reaction to it. The modified file contents are returned.
    
        C++ signature :
            class boost::python::api::object ReactionMetadataToPNGFile(class RDKix::ChemicalReaction,class boost::python::api::object [,bool=True [,bool=True [,bool=False [,bool=False]]]])
    """
def ReactionMetadataToPNGString(mol: ChemicalReaction, pngdata: typing.Any, includePkl: bool = True, includeSmiles: bool = True, includeSmarts: bool = False, includeRxn: bool = False) -> typing.Any:
    """
        Adds metadata about a reaction to the PNG string passed in.The modified string is returned.
    
        C++ signature :
            class boost::python::api::object ReactionMetadataToPNGString(class RDKix::ChemicalReaction,class boost::python::api::object [,bool=True [,bool=True [,bool=False [,bool=False]]]])
    """
@typing.overload
def ReactionToCXSmarts(reaction: ChemicalReaction) -> str:
    """
        construct a reaction SMARTS string for a ChemicalReaction
    
        C++ signature :
            class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > ReactionToCXSmarts(class RDKix::ChemicalReaction)
    """
@typing.overload
def ReactionToCXSmarts(reaction: ChemicalReaction, params: SmilesWriteParams, flags: int = ...) -> str:
    """
        construct a reaction CXSMARTS string for a ChemicalReaction
    
        C++ signature :
            class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > ReactionToCXSmarts(class RDKix::ChemicalReaction,struct RDKix::SmilesWriteParams [,unsigned int=rdkix.Chem.rdmolfiles.CXSmilesFields.CX_ALL])
    """
@typing.overload
def ReactionToCXSmiles(reaction: ChemicalReaction, canonical: bool = True) -> str:
    """
        construct a reaction SMILES string for a ChemicalReaction
    
        C++ signature :
            class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > ReactionToCXSmiles(class RDKix::ChemicalReaction [,bool=True])
    """
@typing.overload
def ReactionToCXSmiles(reaction: ChemicalReaction, params: SmilesWriteParams, flags: int = ...) -> str:
    """
        construct a reaction CXSMILES string for a ChemicalReaction
    
        C++ signature :
            class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > ReactionToCXSmiles(class RDKix::ChemicalReaction,struct RDKix::SmilesWriteParams [,unsigned int=rdkix.Chem.rdmolfiles.CXSmilesFields.CX_ALL])
    """
def ReactionToMolecule(reaction: ChemicalReaction) -> rdkix.Chem.Mol:
    """
        construct a molecule for a ChemicalReaction with RXN role property set
    
        C++ signature :
            class RDKix::ROMol * __ptr64 ReactionToMolecule(class RDKix::ChemicalReaction)
    """
def ReactionToMrvBlock(reaction: ChemicalReaction, prettyPrint: bool = False) -> str:
    """
        construct a string in Marvin (MRV) rxn format for a ChemicalReaction
    
        C++ signature :
            class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > ReactionToMrvBlock(class RDKix::ChemicalReaction [,bool=False])
    """
def ReactionToMrvFile(reaction: ChemicalReaction, filename: str, prettyPrint: bool = False) -> None:
    """
        write a Marvin (MRV) rxn file for a ChemicalReaction
    
        C++ signature :
            void ReactionToMrvFile(class RDKix::ChemicalReaction,class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > [,bool=False])
    """
def ReactionToRxnBlock(reaction: ChemicalReaction, separateAgents: bool = False, forceV3000: bool = False) -> str:
    """
        construct a string in MDL rxn format for a ChemicalReaction
    
        C++ signature :
            class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > ReactionToRxnBlock(class RDKix::ChemicalReaction [,bool=False [,bool=False]])
    """
@typing.overload
def ReactionToSmarts(reaction: ChemicalReaction) -> str:
    """
        construct a reaction SMARTS string for a ChemicalReaction
    
        C++ signature :
            class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > ReactionToSmarts(class RDKix::ChemicalReaction)
    """
@typing.overload
def ReactionToSmarts(reaction: ChemicalReaction, params: SmilesWriteParams) -> str:
    """
        construct a reaction SMARTS string for a ChemicalReaction
    
        C++ signature :
            class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > ReactionToSmarts(class RDKix::ChemicalReaction,struct RDKix::SmilesWriteParams)
    """
@typing.overload
def ReactionToSmiles(reaction: ChemicalReaction, canonical: bool = True) -> str:
    """
        construct a reaction SMILES string for a ChemicalReaction
    
        C++ signature :
            class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > ReactionToSmiles(class RDKix::ChemicalReaction [,bool=True])
    """
@typing.overload
def ReactionToSmiles(reaction: ChemicalReaction, params: SmilesWriteParams) -> str:
    """
        construct a reaction SMILES string for a ChemicalReaction
    
        C++ signature :
            class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > ReactionToSmiles(class RDKix::ChemicalReaction,struct RDKix::SmilesWriteParams)
    """
def ReactionToV3KRxnBlock(reaction: ChemicalReaction, separateAgents: bool = False) -> str:
    """
        construct a string in MDL v3000 rxn format for a ChemicalReaction
    
        C++ signature :
            class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > ReactionToV3KRxnBlock(class RDKix::ChemicalReaction [,bool=False])
    """
def ReactionsFromCDXMLBlock(rxnblock: typing.Any, sanitize: bool = False, removeHs: bool = False) -> typing.Any:
    """
        construct a tuple of ChemicalReactions from a string in CDXML format
    
        C++ signature :
            class boost::python::api::object ReactionsFromCDXMLBlock(class boost::python::api::object [,bool=False [,bool=False]])
    """
def ReactionsFromCDXMLFile(filename: str, sanitize: bool = False, removeHs: bool = False) -> typing.Any:
    """
        construct a tuple of ChemicalReactions from a CDXML rxn file
    
        C++ signature :
            class boost::python::api::object ReactionsFromCDXMLFile(char const * __ptr64 [,bool=False [,bool=False]])
    """
def ReduceProductToSideChains(product: Mol, addDummyAtoms: bool = True) -> rdkix.Chem.Mol:
    """
        reduce the product of a reaction to the side chains added by the reaction.              The output is a molecule with attached wildcards indicating where the product was attached.              The dummy atom has the same reaction-map number as the product atom (if available).
    
        C++ signature :
            class RDKix::ROMol * __ptr64 ReduceProductToSideChains(class boost::shared_ptr<class RDKix::ROMol> [,bool=True])
    """
def RemoveMappingNumbersFromReactions(reaction: ChemicalReaction) -> None:
    """
        Removes the mapping numbers from the molecules of a reaction
    
        C++ signature :
            void RemoveMappingNumbersFromReactions(class RDKix::ChemicalReaction)
    """
def SanitizeRxn(rxn: ChemicalReaction, sanitizeOps: int = 4294967295, params: AdjustQueryParameters = ..., catchErrors: bool = False) -> SanitizeFlags:
    """
        Does some sanitization of the reactant and product templates of a reaction.
        
            - The reaction is modified in place.
            - If sanitization fails, an exception will be thrown unless catchErrors is set
        
          ARGUMENTS:
        
            - rxn: the reaction to be modified
            - sanitizeOps: (optional) reaction sanitization operations to be carried out
              these should be constructed by or'ing together the
              operations in rdkix.Chem.rdChemReactions.SanitizeFlags
            - optional adjustment parameters for changing the meaning of the substructure
              matching done in the templates.  The default is 
              rdkix.Chem.rdChemReactions.DefaultRxnAdjustParams which aromatizes
              kekule structures if possible.
            - catchErrors: (optional) if provided, instead of raising an exception
              when sanitization fails (the default behavior), the 
              first operation that failed (as defined in rdkix.Chem.rdChemReactions.SanitizeFlags)
              is returned. Zero is returned on success.
        
          The operations carried out by default are:
            1) fixRGroups(): sets R group labels on mapped dummy atoms when possible
            2) fixAtomMaps(): attempts to set atom maps on unmapped R groups
            3) adjustTemplate(): calls adjustQueryProperties() on all reactant templates
            4) fixHs(): merges explicit Hs in the reactant templates that don't map to heavy atoms
        
    
        C++ signature :
            enum RDKix::RxnOps::SanitizeRxnFlags SanitizeRxn(class RDKix::ChemicalReaction {lvalue} [,unsigned __int64=4294967295 [,struct RDKix::MolOps::AdjustQueryParameters=<rdkix.Chem.rdmolops.AdjustQueryParameters object at 0x000001EECEFF8860> [,bool=False]]])
    """
def SanitizeRxnAsMols(rxn: ChemicalReaction, sanitizeOps: int = 268435455) -> None:
    """
        Does the usual molecular sanitization on each reactant, agent, and product of the reaction
    
        C++ signature :
            void SanitizeRxnAsMols(class RDKix::ChemicalReaction {lvalue} [,unsigned int=268435455])
    """
def UpdateProductsStereochemistry(reaction: ChemicalReaction) -> None:
    """
        Caution: This is an expert-user function which will change a property (molInversionFlag) of your products.          This function is called by default using the RXN or SMARTS parser for reactions and should really only be called if reactions have been constructed some other way.          The function updates the stereochemistry of the product by considering 4 different cases: inversion, retention, removal, and introduction
    
        C++ signature :
            void UpdateProductsStereochemistry(class RDKix::ChemicalReaction * __ptr64)
    """
SANITIZE_ADJUST_REACTANTS: SanitizeFlags  # value = rdkix.Chem.rdChemReactions.SanitizeFlags.SANITIZE_ADJUST_REACTANTS
SANITIZE_ALL: SanitizeFlags  # value = rdkix.Chem.rdChemReactions.SanitizeFlags.SANITIZE_ALL
SANITIZE_ATOM_MAPS: SanitizeFlags  # value = rdkix.Chem.rdChemReactions.SanitizeFlags.SANITIZE_ATOM_MAPS
SANITIZE_MERGEHS: SanitizeFlags  # value = rdkix.Chem.rdChemReactions.SanitizeFlags.SANITIZE_MERGEHS
SANITIZE_NONE: SanitizeFlags  # value = rdkix.Chem.rdChemReactions.SanitizeFlags.SANITIZE_NONE
SANITIZE_RGROUP_NAMES: SanitizeFlags  # value = rdkix.Chem.rdChemReactions.SanitizeFlags.SANITIZE_RGROUP_NAMES
