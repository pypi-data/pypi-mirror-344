from __future__ import annotations
import rdkix.Chem
import typing
from .FilterMatchOps import *
__all__ = ['ExclusionList', 'FilterCatalog', 'FilterCatalogCanSerialize', 'FilterCatalogEntry', 'FilterCatalogEntryList', 'FilterCatalogListOfEntryList', 'FilterCatalogParams', 'FilterHierarchyMatcher', 'FilterMatch', 'FilterMatchOps', 'FilterMatcherBase', 'GetFlattenedFunctionalGroupHierarchy', 'GetFunctionalGroupHierarchy', 'IntPair', 'MolList', 'PythonFilterMatcher', 'RunFilterCatalog', 'SmartsMatcher', 'VectFilterMatch']
class ExclusionList(FilterMatcherBase):
    __instance_size__: typing.ClassVar[int] = 80
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def AddPattern(self, base: FilterMatcherBase) -> None:
        """
            Add a FilterMatcherBase that should not appear in a molecule
        
            C++ signature :
                void AddPattern(RDKix::ExclusionList {lvalue},RDKix::FilterMatcherBase)
        """
    def SetExclusionPatterns(self, list: typing.Any) -> None:
        """
            Set a list of FilterMatcherBases that should not appear in a molecule
        
            C++ signature :
                void SetExclusionPatterns(RDKix::ExclusionList {lvalue},boost::python::api::object)
        """
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(_object*)
        """
class FilterCatalog(Boost.Python.instance):
    __getstate_manages_dict__: typing.ClassVar[bool] = True
    __instance_size__: typing.ClassVar[int] = 72
    __safe_for_unpickling__: typing.ClassVar[bool] = True
    @staticmethod
    def AddEntry(entry: FilterCatalog, updateFPLength: FilterCatalogEntry = False) -> None:
        """
            Add a FilterCatalogEntry to the catalog
        
            C++ signature :
                void AddEntry(RDKix::FilterCatalog {lvalue} [,RDKix::FilterCatalogEntry*=False])
        """
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def GetEntry(self, idx: int) -> FilterCatalogEntry:
        """
            Return the FilterCatalogEntry at the specified index
        
            C++ signature :
                boost::shared_ptr<RDKix::FilterCatalogEntry const> GetEntry(RDKix::FilterCatalog {lvalue},unsigned int)
        """
    def GetEntryWithIdx(self, idx: int) -> FilterCatalogEntry:
        """
            Return the FilterCatalogEntry at the specified index
        
            C++ signature :
                boost::shared_ptr<RDKix::FilterCatalogEntry const> GetEntryWithIdx(RDKix::FilterCatalog {lvalue},unsigned int)
        """
    def GetFilterMatches(self, mol: Mol) -> VectFilterMatch:
        """
            Return every matching filter from all catalog entries that match mol
        
            C++ signature :
                std::vector<RDKix::FilterMatch, std::allocator<RDKix::FilterMatch> > GetFilterMatches(RDKix::FilterCatalog {lvalue},RDKix::ROMol)
        """
    def GetFirstMatch(self, mol: Mol) -> FilterCatalogEntry:
        """
            Return the first catalog entry that matches mol
        
            C++ signature :
                boost::shared_ptr<RDKix::FilterCatalogEntry const> GetFirstMatch(RDKix::FilterCatalog {lvalue},RDKix::ROMol)
        """
    def GetMatches(self, mol: Mol) -> FilterCatalogEntryList:
        """
            Return all catalog entries that match mol
        
            C++ signature :
                std::vector<boost::shared_ptr<RDKix::FilterCatalogEntry const>, std::allocator<boost::shared_ptr<RDKix::FilterCatalogEntry const> > > GetMatches(RDKix::FilterCatalog {lvalue},RDKix::ROMol)
        """
    def GetNumEntries(self) -> int:
        """
            Returns the number of entries in the catalog
        
            C++ signature :
                unsigned int GetNumEntries(RDKix::FilterCatalog {lvalue})
        """
    def HasMatch(self, mol: Mol) -> bool:
        """
            Returns True if the catalog has an entry that matches mol
        
            C++ signature :
                bool HasMatch(RDKix::FilterCatalog {lvalue},RDKix::ROMol)
        """
    def RemoveEntry(self, obj: typing.Any) -> bool:
        """
            Remove the given entry from the catalog
        
            C++ signature :
                bool RemoveEntry(RDKix::FilterCatalog {lvalue},boost::python::api::object)
        """
    def Serialize(self) -> typing.Any:
        """
            C++ signature :
                boost::python::api::object Serialize(RDKix::FilterCatalog)
        """
    def __getinitargs__(self) -> tuple:
        """
            C++ signature :
                boost::python::tuple __getinitargs__(RDKix::FilterCatalog)
        """
    def __getstate__(self) -> tuple:
        """
            C++ signature :
                boost::python::tuple __getstate__(boost::python::api::object)
        """
    @typing.overload
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(_object*)
        """
    @typing.overload
    def __init__(self, binStr: str) -> None:
        """
            C++ signature :
                void __init__(_object*,std::string)
        """
    @typing.overload
    def __init__(self, params: FilterCatalogParams) -> None:
        """
            C++ signature :
                void __init__(_object*,RDKix::FilterCatalogParams)
        """
    @typing.overload
    def __init__(self, catalogs: FilterCatalogs) -> None:
        """
            C++ signature :
                void __init__(_object*,RDKix::FilterCatalogParams::FilterCatalogs)
        """
    def __setstate__(self, data: tuple) -> None:
        """
            C++ signature :
                void __setstate__(boost::python::api::object,boost::python::tuple)
        """
class FilterCatalogEntry(Boost.Python.instance):
    """
    FilterCatalogEntry
    A filter catalog entry is an entry in a filter catalog.
    Each filter is named and is used to flag a molecule usually for some
    undesirable property.
    
    For example, a PAINS (Pan Assay INterference) catalog entry be appear as
    follows:
    
    >>> from rdkix.Chem.FilterCatalog import *
    >>> params = FilterCatalogParams()
    >>> params.AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS_A)
    True
    >>> catalog = FilterCatalog(params)
    >>> mol = Chem.MolFromSmiles('O=C(Cn1cnc2c1c(=O)n(C)c(=O)n2C)N/N=C/c1c(O)ccc2c1cccc2')
    >>> entry = catalog.GetFirstMatch(mol)
    >>> print (entry.GetProp('Scope'))
    PAINS filters (family A)
    >>> print (entry.GetDescription())
    hzone_phenol_A(479)
    
    
    """
    __instance_size__: typing.ClassVar[int] = 40
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def ClearProp(self, key: str) -> None:
        """
            C++ signature :
                void ClearProp(RDKix::FilterCatalogEntry {lvalue},std::string)
        """
    def GetDescription(self) -> str:
        """
            Get the description of the catalog entry
        
            C++ signature :
                std::string GetDescription(RDKix::FilterCatalogEntry {lvalue})
        """
    def GetFilterMatches(self, mol: Mol) -> VectFilterMatch:
        """
            Retrieve the list of filters that match the molecule
        
            C++ signature :
                std::vector<RDKix::FilterMatch, std::allocator<RDKix::FilterMatch> > GetFilterMatches(RDKix::FilterCatalogEntry {lvalue},RDKix::ROMol)
        """
    def GetProp(self, key: str) -> str:
        """
            C++ signature :
                std::string GetProp(RDKix::FilterCatalogEntry {lvalue},std::string)
        """
    def GetPropList(self) -> _vectSs:
        """
            C++ signature :
                std::vector<std::string, std::allocator<std::string> > GetPropList(RDKix::FilterCatalogEntry {lvalue})
        """
    def HasFilterMatch(self, mol: Mol) -> bool:
        """
            Returns True if the catalog entry contains filters that match the molecule
        
            C++ signature :
                bool HasFilterMatch(RDKix::FilterCatalogEntry {lvalue},RDKix::ROMol)
        """
    def IsValid(self) -> bool:
        """
            C++ signature :
                bool IsValid(RDKix::FilterCatalogEntry {lvalue})
        """
    def Serialize(self) -> typing.Any:
        """
            C++ signature :
                boost::python::api::object Serialize(RDKix::FilterCatalogEntry)
        """
    def SetDescription(self, description: str) -> None:
        """
            Set the description of the catalog entry
        
            C++ signature :
                void SetDescription(RDKix::FilterCatalogEntry {lvalue},std::string)
        """
    def SetProp(self, key: str, val: str) -> None:
        """
            C++ signature :
                void SetProp(RDKix::FilterCatalogEntry {lvalue},std::string,std::string)
        """
    @typing.overload
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(_object*)
        """
    @typing.overload
    def __init__(self, name: str, matcher: FilterMatcherBase) -> None:
        """
            C++ signature :
                void __init__(_object*,std::string,RDKix::FilterMatcherBase {lvalue})
        """
class FilterCatalogEntryList(Boost.Python.instance):
    __instance_size__: typing.ClassVar[int] = 48
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def __contains__(self, item: typing.Any) -> bool:
        """
            C++ signature :
                bool __contains__(std::vector<boost::shared_ptr<RDKix::FilterCatalogEntry const>, std::allocator<boost::shared_ptr<RDKix::FilterCatalogEntry const> > > {lvalue},_object*)
        """
    def __delitem__(self, item: typing.Any) -> None:
        """
            C++ signature :
                void __delitem__(std::vector<boost::shared_ptr<RDKix::FilterCatalogEntry const>, std::allocator<boost::shared_ptr<RDKix::FilterCatalogEntry const> > > {lvalue},_object*)
        """
    def __getitem__(self, item: typing.Any) -> typing.Any:
        """
            C++ signature :
                boost::python::api::object __getitem__(boost::python::back_reference<std::vector<boost::shared_ptr<RDKix::FilterCatalogEntry const>, std::allocator<boost::shared_ptr<RDKix::FilterCatalogEntry const> > >&>,_object*)
        """
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(_object*)
        """
    def __iter__(self) -> typing.Any:
        """
            C++ signature :
                boost::python::objects::iterator_range<boost::python::return_value_policy<boost::python::return_by_value, boost::python::default_call_policies>, __gnu_cxx::__normal_iterator<boost::shared_ptr<RDKix::FilterCatalogEntry const>*, std::vector<boost::shared_ptr<RDKix::FilterCatalogEntry const>, std::allocator<boost::shared_ptr<RDKix::FilterCatalogEntry const> > > > > __iter__(boost::python::back_reference<std::vector<boost::shared_ptr<RDKix::FilterCatalogEntry const>, std::allocator<boost::shared_ptr<RDKix::FilterCatalogEntry const> > >&>)
        """
    def __len__(self) -> int:
        """
            C++ signature :
                unsigned long __len__(std::vector<boost::shared_ptr<RDKix::FilterCatalogEntry const>, std::allocator<boost::shared_ptr<RDKix::FilterCatalogEntry const> > > {lvalue})
        """
    def __setitem__(self, item: typing.Any, value: typing.Any) -> None:
        """
            C++ signature :
                void __setitem__(std::vector<boost::shared_ptr<RDKix::FilterCatalogEntry const>, std::allocator<boost::shared_ptr<RDKix::FilterCatalogEntry const> > > {lvalue},_object*,_object*)
        """
    def append(self, item: typing.Any) -> None:
        """
            C++ signature :
                void append(std::vector<boost::shared_ptr<RDKix::FilterCatalogEntry const>, std::allocator<boost::shared_ptr<RDKix::FilterCatalogEntry const> > > {lvalue},boost::python::api::object)
        """
    def extend(self, other: typing.Any) -> None:
        """
            C++ signature :
                void extend(std::vector<boost::shared_ptr<RDKix::FilterCatalogEntry const>, std::allocator<boost::shared_ptr<RDKix::FilterCatalogEntry const> > > {lvalue},boost::python::api::object)
        """
class FilterCatalogListOfEntryList(Boost.Python.instance):
    __instance_size__: typing.ClassVar[int] = 48
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def __contains__(self, item: typing.Any) -> bool:
        """
            C++ signature :
                bool __contains__(std::vector<std::vector<boost::shared_ptr<RDKix::FilterCatalogEntry const>, std::allocator<boost::shared_ptr<RDKix::FilterCatalogEntry const> > >, std::allocator<std::vector<boost::shared_ptr<RDKix::FilterCatalogEntry const>, std::allocator<boost::shared_ptr<RDKix::FilterCatalogEntry const> > > > > {lvalue},_object*)
        """
    def __delitem__(self, item: typing.Any) -> None:
        """
            C++ signature :
                void __delitem__(std::vector<std::vector<boost::shared_ptr<RDKix::FilterCatalogEntry const>, std::allocator<boost::shared_ptr<RDKix::FilterCatalogEntry const> > >, std::allocator<std::vector<boost::shared_ptr<RDKix::FilterCatalogEntry const>, std::allocator<boost::shared_ptr<RDKix::FilterCatalogEntry const> > > > > {lvalue},_object*)
        """
    def __getitem__(self, item: typing.Any) -> typing.Any:
        """
            C++ signature :
                boost::python::api::object __getitem__(boost::python::back_reference<std::vector<std::vector<boost::shared_ptr<RDKix::FilterCatalogEntry const>, std::allocator<boost::shared_ptr<RDKix::FilterCatalogEntry const> > >, std::allocator<std::vector<boost::shared_ptr<RDKix::FilterCatalogEntry const>, std::allocator<boost::shared_ptr<RDKix::FilterCatalogEntry const> > > > >&>,_object*)
        """
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(_object*)
        """
    def __iter__(self) -> typing.Any:
        """
            C++ signature :
                boost::python::objects::iterator_range<boost::python::return_internal_reference<1ul, boost::python::default_call_policies>, __gnu_cxx::__normal_iterator<std::vector<boost::shared_ptr<RDKix::FilterCatalogEntry const>, std::allocator<boost::shared_ptr<RDKix::FilterCatalogEntry const> > >*, std::vector<std::vector<boost::shared_ptr<RDKix::FilterCatalogEntry const>, std::allocator<boost::shared_ptr<RDKix::FilterCatalogEntry const> > >, std::allocator<std::vector<boost::shared_ptr<RDKix::FilterCatalogEntry const>, std::allocator<boost::shared_ptr<RDKix::FilterCatalogEntry const> > > > > > > __iter__(boost::python::back_reference<std::vector<std::vector<boost::shared_ptr<RDKix::FilterCatalogEntry const>, std::allocator<boost::shared_ptr<RDKix::FilterCatalogEntry const> > >, std::allocator<std::vector<boost::shared_ptr<RDKix::FilterCatalogEntry const>, std::allocator<boost::shared_ptr<RDKix::FilterCatalogEntry const> > > > >&>)
        """
    def __len__(self) -> int:
        """
            C++ signature :
                unsigned long __len__(std::vector<std::vector<boost::shared_ptr<RDKix::FilterCatalogEntry const>, std::allocator<boost::shared_ptr<RDKix::FilterCatalogEntry const> > >, std::allocator<std::vector<boost::shared_ptr<RDKix::FilterCatalogEntry const>, std::allocator<boost::shared_ptr<RDKix::FilterCatalogEntry const> > > > > {lvalue})
        """
    def __setitem__(self, item: typing.Any, value: typing.Any) -> None:
        """
            C++ signature :
                void __setitem__(std::vector<std::vector<boost::shared_ptr<RDKix::FilterCatalogEntry const>, std::allocator<boost::shared_ptr<RDKix::FilterCatalogEntry const> > >, std::allocator<std::vector<boost::shared_ptr<RDKix::FilterCatalogEntry const>, std::allocator<boost::shared_ptr<RDKix::FilterCatalogEntry const> > > > > {lvalue},_object*,_object*)
        """
    def append(self, item: typing.Any) -> None:
        """
            C++ signature :
                void append(std::vector<std::vector<boost::shared_ptr<RDKix::FilterCatalogEntry const>, std::allocator<boost::shared_ptr<RDKix::FilterCatalogEntry const> > >, std::allocator<std::vector<boost::shared_ptr<RDKix::FilterCatalogEntry const>, std::allocator<boost::shared_ptr<RDKix::FilterCatalogEntry const> > > > > {lvalue},boost::python::api::object)
        """
    def extend(self, other: typing.Any) -> None:
        """
            C++ signature :
                void extend(std::vector<std::vector<boost::shared_ptr<RDKix::FilterCatalogEntry const>, std::allocator<boost::shared_ptr<RDKix::FilterCatalogEntry const> > >, std::allocator<std::vector<boost::shared_ptr<RDKix::FilterCatalogEntry const>, std::allocator<boost::shared_ptr<RDKix::FilterCatalogEntry const> > > > > {lvalue},boost::python::api::object)
        """
class FilterCatalogParams(Boost.Python.instance):
    class FilterCatalogs(Boost.Python.enum):
        ALL: typing.ClassVar[FilterCatalogs]  # value = rdkix.Chem.rdfiltercatalog.FilterCatalogs.ALL
        BRENK: typing.ClassVar[FilterCatalogs]  # value = rdkix.Chem.rdfiltercatalog.FilterCatalogs.BRENK
        CHEMBL: typing.ClassVar[FilterCatalogs]  # value = rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL
        CHEMBL_BMS: typing.ClassVar[FilterCatalogs]  # value = rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL_BMS
        CHEMBL_Dundee: typing.ClassVar[FilterCatalogs]  # value = rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL_Dundee
        CHEMBL_Glaxo: typing.ClassVar[FilterCatalogs]  # value = rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL_Glaxo
        CHEMBL_Inpharmatica: typing.ClassVar[FilterCatalogs]  # value = rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL_Inpharmatica
        CHEMBL_LINT: typing.ClassVar[FilterCatalogs]  # value = rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL_LINT
        CHEMBL_MLSMR: typing.ClassVar[FilterCatalogs]  # value = rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL_MLSMR
        CHEMBL_SureChEMBL: typing.ClassVar[FilterCatalogs]  # value = rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL_SureChEMBL
        NIH: typing.ClassVar[FilterCatalogs]  # value = rdkix.Chem.rdfiltercatalog.FilterCatalogs.NIH
        PAINS: typing.ClassVar[FilterCatalogs]  # value = rdkix.Chem.rdfiltercatalog.FilterCatalogs.PAINS
        PAINS_A: typing.ClassVar[FilterCatalogs]  # value = rdkix.Chem.rdfiltercatalog.FilterCatalogs.PAINS_A
        PAINS_B: typing.ClassVar[FilterCatalogs]  # value = rdkix.Chem.rdfiltercatalog.FilterCatalogs.PAINS_B
        PAINS_C: typing.ClassVar[FilterCatalogs]  # value = rdkix.Chem.rdfiltercatalog.FilterCatalogs.PAINS_C
        ZINC: typing.ClassVar[FilterCatalogs]  # value = rdkix.Chem.rdfiltercatalog.FilterCatalogs.ZINC
        __slots__: typing.ClassVar[tuple] = tuple()
        names: typing.ClassVar[dict]  # value = {'PAINS_A': rdkix.Chem.rdfiltercatalog.FilterCatalogs.PAINS_A, 'PAINS_B': rdkix.Chem.rdfiltercatalog.FilterCatalogs.PAINS_B, 'PAINS_C': rdkix.Chem.rdfiltercatalog.FilterCatalogs.PAINS_C, 'PAINS': rdkix.Chem.rdfiltercatalog.FilterCatalogs.PAINS, 'BRENK': rdkix.Chem.rdfiltercatalog.FilterCatalogs.BRENK, 'NIH': rdkix.Chem.rdfiltercatalog.FilterCatalogs.NIH, 'ZINC': rdkix.Chem.rdfiltercatalog.FilterCatalogs.ZINC, 'CHEMBL_Glaxo': rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL_Glaxo, 'CHEMBL_Dundee': rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL_Dundee, 'CHEMBL_BMS': rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL_BMS, 'CHEMBL_SureChEMBL': rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL_SureChEMBL, 'CHEMBL_MLSMR': rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL_MLSMR, 'CHEMBL_Inpharmatica': rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL_Inpharmatica, 'CHEMBL_LINT': rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL_LINT, 'CHEMBL': rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL, 'ALL': rdkix.Chem.rdfiltercatalog.FilterCatalogs.ALL}
        values: typing.ClassVar[dict]  # value = {2: rdkix.Chem.rdfiltercatalog.FilterCatalogs.PAINS_A, 4: rdkix.Chem.rdfiltercatalog.FilterCatalogs.PAINS_B, 8: rdkix.Chem.rdfiltercatalog.FilterCatalogs.PAINS_C, 14: rdkix.Chem.rdfiltercatalog.FilterCatalogs.PAINS, 16: rdkix.Chem.rdfiltercatalog.FilterCatalogs.BRENK, 32: rdkix.Chem.rdfiltercatalog.FilterCatalogs.NIH, 64: rdkix.Chem.rdfiltercatalog.FilterCatalogs.ZINC, 128: rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL_Glaxo, 256: rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL_Dundee, 512: rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL_BMS, 1024: rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL_SureChEMBL, 2048: rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL_MLSMR, 4096: rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL_Inpharmatica, 8192: rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL_LINT, 16256: rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL, 16382: rdkix.Chem.rdfiltercatalog.FilterCatalogs.ALL}
    __instance_size__: typing.ClassVar[int] = 40
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def AddCatalog(self, catalogs: FilterCatalogs) -> bool:
        """
            C++ signature :
                bool AddCatalog(RDKix::FilterCatalogParams {lvalue},RDKix::FilterCatalogParams::FilterCatalogs)
        """
    @typing.overload
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(_object*)
        """
    @typing.overload
    def __init__(self, catalogs: FilterCatalogs) -> None:
        """
            Construct from a FilterCatalogs identifier (i.e. FilterCatalogParams.PAINS)
        
            C++ signature :
                void __init__(_object*,RDKix::FilterCatalogParams::FilterCatalogs)
        """
class FilterHierarchyMatcher(FilterMatcherBase):
    """
    Hierarchical Filter
     basic constructors: 
       FilterHierarchyMatcher( matcher )
       where can be any FilterMatcherBase (SmartsMatcher, etc)
     FilterHierarchyMatcher's have children and can form matching
      trees.  then GetFilterMatches is called, the most specific (
      i.e. lowest node in a branch) is returned.
    
     n.b. A FilterHierarchicalMatcher of functional groups is returned
      by calling GetFunctionalGroupHierarchy()
    
    >>> from rdkix.Chem import MolFromSmiles
    >>> from rdkix.Chem.FilterCatalog import *
    >>> functionalGroups = GetFunctionalGroupHierarchy()
    >>> [match.filterMatch.GetName() 
    ...     for match in functionalGroups.GetFilterMatches(
    ...         MolFromSmiles('c1ccccc1Cl'))]
    ['Halogen.Aromatic', 'Halogen.NotFluorine.Aromatic']
    
    """
    __instance_size__: typing.ClassVar[int] = 40
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def AddChild(self, hierarchy: FilterHierarchyMatcher) -> FilterHierarchyMatcher:
        """
            Add a child node to this hierarchy.
        
            C++ signature :
                boost::shared_ptr<RDKix::FilterHierarchyMatcher> AddChild(RDKix::FilterHierarchyMatcher {lvalue},RDKix::FilterHierarchyMatcher)
        """
    def SetPattern(self, matcher: FilterMatcherBase) -> None:
        """
            Set the filtermatcher pattern for this node.  An empty node is considered a root node and passes along the matches to the children.
        
            C++ signature :
                void SetPattern(RDKix::FilterHierarchyMatcher {lvalue},RDKix::FilterMatcherBase)
        """
    @typing.overload
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(_object*)
        """
    @typing.overload
    def __init__(self, matcher: FilterMatcherBase) -> None:
        """
            Construct from a filtermatcher
        
            C++ signature :
                void __init__(_object*,RDKix::FilterMatcherBase)
        """
class FilterMatch(Boost.Python.instance):
    """
    Object that holds the result of running FilterMatcherBase::GetMatches
    
     - filterMatch holds the FilterMatchBase that triggered the match
     - atomParis holds the [ (query_atom_idx, target_atom_idx) ] pairs for the matches.
    
    
    Note that some matches may not have atom pairs (especially matches that use FilterMatchOps.Not
    """
    __instance_size__: typing.ClassVar[int] = 40
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def __init__(self, filter: FilterMatcherBase, atomPairs: MatchTypeVect) -> None:
        """
            C++ signature :
                void __init__(_object*,boost::shared_ptr<RDKix::FilterMatcherBase>,std::vector<std::pair<int, int>, std::allocator<std::pair<int, int> > >)
        """
    @property
    def atomPairs(*args, **kwargs):
        ...
    @property
    def filterMatch(*args, **kwargs):
        ...
class FilterMatcherBase(Boost.Python.instance):
    """
    Base class for matching molecules to filters.
    
     A FilterMatcherBase supplies the following API 
     - IsValid() returns True if the matcher is valid for use, False otherwise
     - HasMatch(mol) returns True if the molecule matches the filter
     - GetMatches(mol) -> [FilterMatch, FilterMatch] returns all the FilterMatch data
           that matches the molecule
    
    
    print( FilterMatcherBase ) will print user-friendly information about the filter
    Note that a FilterMatcherBase can be combined from may FilterMatcherBases
    This is why GetMatches can return multiple FilterMatcherBases.
    >>> from rdkix.Chem.FilterCatalog import *
    >>> carbon_matcher = SmartsMatcher('Carbon', '[#6]', 0, 1)
    >>> oxygen_matcher = SmartsMatcher('Oxygen', '[#8]', 0, 1)
    >>> co_matcher = FilterMatchOps.Or(carbon_matcher, oxygen_matcher)
    >>> mol = Chem.MolFromSmiles('C')
    >>> matches = co_matcher.GetMatches(mol)
    >>> len(matches)
    1
    >>> print(matches[0].filterMatch)
    Carbon
    
    """
    @staticmethod
    def __init__(*args, **kwargs):
        """
        Raises an exception
        This class cannot be instantiated from Python
        """
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def GetMatches(self, mol: Mol) -> VectFilterMatch:
        """
            Returns the list of matching subfilters mol matches any filter
        
            C++ signature :
                std::vector<RDKix::FilterMatch, std::allocator<RDKix::FilterMatch> > GetMatches(RDKix::FilterMatcherBase {lvalue},RDKix::ROMol)
        """
    def GetName(self) -> str:
        """
            C++ signature :
                std::string GetName(RDKix::FilterMatcherBase {lvalue})
        """
    def HasMatch(self, mol: Mol) -> bool:
        """
            Returns True if mol matches the filter
        
            C++ signature :
                bool HasMatch(RDKix::FilterMatcherBase {lvalue},RDKix::ROMol)
        """
    def IsValid(self) -> bool:
        """
            Return True if the filter matcher is valid, False otherwise
        
            C++ signature :
                bool IsValid(RDKix::FilterMatcherBase {lvalue})
        """
    def __str__(self) -> str:
        """
            C++ signature :
                std::string __str__(RDKix::FilterMatcherBase {lvalue})
        """
class IntPair(Boost.Python.instance):
    __instance_size__: typing.ClassVar[int] = 32
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def __getitem__(self, idx: int) -> int:
        """
            C++ signature :
                int __getitem__(std::pair<int, int> {lvalue},unsigned long)
        """
    @typing.overload
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(_object*)
        """
    @typing.overload
    def __init__(self, query: int, target: int) -> None:
        """
            C++ signature :
                void __init__(_object*,int,int)
        """
    @property
    def query(*args, **kwargs):
        ...
    @query.setter
    def query(*args, **kwargs):
        ...
    @property
    def target(*args, **kwargs):
        ...
    @target.setter
    def target(*args, **kwargs):
        ...
class MolList(Boost.Python.instance):
    __instance_size__: typing.ClassVar[int] = 48
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def __contains__(self, item: typing.Any) -> bool:
        """
            C++ signature :
                bool __contains__(std::vector<RDKix::ROMol*, std::allocator<RDKix::ROMol*> > {lvalue},_object*)
        """
    def __delitem__(self, item: typing.Any) -> None:
        """
            C++ signature :
                void __delitem__(std::vector<RDKix::ROMol*, std::allocator<RDKix::ROMol*> > {lvalue},_object*)
        """
    def __getitem__(self, item: typing.Any) -> typing.Any:
        """
            C++ signature :
                boost::python::api::object __getitem__(boost::python::back_reference<std::vector<RDKix::ROMol*, std::allocator<RDKix::ROMol*> >&>,_object*)
        """
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(_object*)
        """
    def __iter__(self) -> typing.Any:
        """
            C++ signature :
                boost::python::objects::iterator_range<boost::python::return_value_policy<boost::python::return_by_value, boost::python::default_call_policies>, __gnu_cxx::__normal_iterator<RDKix::ROMol**, std::vector<RDKix::ROMol*, std::allocator<RDKix::ROMol*> > > > __iter__(boost::python::back_reference<std::vector<RDKix::ROMol*, std::allocator<RDKix::ROMol*> >&>)
        """
    def __len__(self) -> int:
        """
            C++ signature :
                unsigned long __len__(std::vector<RDKix::ROMol*, std::allocator<RDKix::ROMol*> > {lvalue})
        """
    def __setitem__(self, item: typing.Any, value: typing.Any) -> None:
        """
            C++ signature :
                void __setitem__(std::vector<RDKix::ROMol*, std::allocator<RDKix::ROMol*> > {lvalue},_object*,_object*)
        """
    def append(self, item: typing.Any) -> None:
        """
            C++ signature :
                void append(std::vector<RDKix::ROMol*, std::allocator<RDKix::ROMol*> > {lvalue},boost::python::api::object)
        """
    def extend(self, other: typing.Any) -> None:
        """
            C++ signature :
                void extend(std::vector<RDKix::ROMol*, std::allocator<RDKix::ROMol*> > {lvalue},boost::python::api::object)
        """
class PythonFilterMatcher(FilterMatcherBase):
    __instance_size__: typing.ClassVar[int] = 72
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def __init__(self, callback: typing.Any) -> None:
        """
            C++ signature :
                void __init__(_object*,_object*)
        """
class SmartsMatcher(FilterMatcherBase):
    """
    Smarts Matcher Filter
     basic constructors: 
       SmartsMatcher( name, smarts_pattern, minCount=1, maxCount=UINT_MAX )
       SmartsMatcher( name, molecule, minCount=1, maxCount=UINT_MAX )
    
      note: If the supplied smarts pattern is not valid, the IsValid() function will
       return False
    >>> from rdkix.Chem.FilterCatalog import *
    >>> minCount, maxCount = 1,2
    >>> carbon_matcher = SmartsMatcher('Carbon', '[#6]', minCount, maxCount)
    >>> print (carbon_matcher.HasMatch(Chem.MolFromSmiles('CC')))
    True
    >>> print (carbon_matcher.HasMatch(Chem.MolFromSmiles('CCC')))
    False
    >>> carbon_matcher.SetMinCount(2)
    >>> print (carbon_matcher.HasMatch(Chem.MolFromSmiles('C')))
    False
    >>> carbon_matcher.SetMaxCount(3)
    >>> print (carbon_matcher.HasMatch(Chem.MolFromSmiles('CCC')))
    True
    
    """
    __instance_size__: typing.ClassVar[int] = 80
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def GetMaxCount(self) -> int:
        """
            Get the maximum times pattern can appear for the filter to match
        
            C++ signature :
                unsigned int GetMaxCount(RDKix::SmartsMatcher {lvalue})
        """
    def GetMinCount(self) -> int:
        """
            Get the minimum times pattern must appear for the filter to match
        
            C++ signature :
                unsigned int GetMinCount(RDKix::SmartsMatcher {lvalue})
        """
    def GetPattern(self) -> rdkix.Chem.Mol:
        """
            C++ signature :
                boost::shared_ptr<RDKix::ROMol> GetPattern(RDKix::SmartsMatcher {lvalue})
        """
    def IsValid(self) -> bool:
        """
            Returns True if the SmartsMatcher is valid
        
            C++ signature :
                bool IsValid(RDKix::SmartsMatcher {lvalue})
        """
    def SetMaxCount(self, count: int) -> None:
        """
            Set the maximum times pattern can appear for the filter to match
        
            C++ signature :
                void SetMaxCount(RDKix::SmartsMatcher {lvalue},unsigned int)
        """
    def SetMinCount(self, count: int) -> None:
        """
            Set the minimum times pattern must appear to match
        
            C++ signature :
                void SetMinCount(RDKix::SmartsMatcher {lvalue},unsigned int)
        """
    @typing.overload
    def SetPattern(self, pat: Mol) -> None:
        """
            Set the pattern molecule for the SmartsMatcher
        
            C++ signature :
                void SetPattern(RDKix::SmartsMatcher {lvalue},RDKix::ROMol)
        """
    @typing.overload
    def SetPattern(self, pat: str) -> None:
        """
            Set the smarts pattern for the Smarts Matcher (warning: MinimumCount is not reset)
        
            C++ signature :
                void SetPattern(RDKix::SmartsMatcher {lvalue},std::string)
        """
    @typing.overload
    def __init__(self, name: str) -> None:
        """
            C++ signature :
                void __init__(_object*,std::string)
        """
    @typing.overload
    def __init__(self, rhs: Mol) -> None:
        """
            Construct from a molecule
        
            C++ signature :
                void __init__(_object*,RDKix::ROMol)
        """
    @typing.overload
    def __init__(self, name: str, mol: Mol, minCount: int = 1, maxCount: int = 4294967295) -> None:
        """
            Construct from a name, molecule, minimum and maximum count
        
            C++ signature :
                void __init__(_object*,std::string,RDKix::ROMol [,unsigned int=1 [,unsigned int=4294967295]])
        """
    @typing.overload
    def __init__(self, name: str, smarts: str, minCount: int = 1, maxCount: int = 4294967295) -> None:
        """
            Construct from a name,smarts pattern, minimum and maximum count
        
            C++ signature :
                void __init__(_object*,std::string,std::string [,unsigned int=1 [,unsigned int=4294967295]])
        """
class VectFilterMatch(Boost.Python.instance):
    __instance_size__: typing.ClassVar[int] = 48
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def __contains__(self, item: typing.Any) -> bool:
        """
            C++ signature :
                bool __contains__(std::vector<RDKix::FilterMatch, std::allocator<RDKix::FilterMatch> > {lvalue},_object*)
        """
    def __delitem__(self, item: typing.Any) -> None:
        """
            C++ signature :
                void __delitem__(std::vector<RDKix::FilterMatch, std::allocator<RDKix::FilterMatch> > {lvalue},_object*)
        """
    def __getitem__(self, item: typing.Any) -> typing.Any:
        """
            C++ signature :
                boost::python::api::object __getitem__(boost::python::back_reference<std::vector<RDKix::FilterMatch, std::allocator<RDKix::FilterMatch> >&>,_object*)
        """
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(_object*)
        """
    def __iter__(self) -> typing.Any:
        """
            C++ signature :
                boost::python::objects::iterator_range<boost::python::return_internal_reference<1ul, boost::python::default_call_policies>, __gnu_cxx::__normal_iterator<RDKix::FilterMatch*, std::vector<RDKix::FilterMatch, std::allocator<RDKix::FilterMatch> > > > __iter__(boost::python::back_reference<std::vector<RDKix::FilterMatch, std::allocator<RDKix::FilterMatch> >&>)
        """
    def __len__(self) -> int:
        """
            C++ signature :
                unsigned long __len__(std::vector<RDKix::FilterMatch, std::allocator<RDKix::FilterMatch> > {lvalue})
        """
    def __setitem__(self, item: typing.Any, value: typing.Any) -> None:
        """
            C++ signature :
                void __setitem__(std::vector<RDKix::FilterMatch, std::allocator<RDKix::FilterMatch> > {lvalue},_object*,_object*)
        """
    def append(self, item: typing.Any) -> None:
        """
            C++ signature :
                void append(std::vector<RDKix::FilterMatch, std::allocator<RDKix::FilterMatch> > {lvalue},boost::python::api::object)
        """
    def extend(self, other: typing.Any) -> None:
        """
            C++ signature :
                void extend(std::vector<RDKix::FilterMatch, std::allocator<RDKix::FilterMatch> > {lvalue},boost::python::api::object)
        """
def FilterCatalogCanSerialize() -> bool:
    """
        Returns True if the FilterCatalog is serializable (requires boost serialization
    
        C++ signature :
            bool FilterCatalogCanSerialize()
    """
def GetFlattenedFunctionalGroupHierarchy(normalized: bool = False) -> dict:
    """
        Returns the flattened functional group hierarchy as a dictionary  of name:ROMOL_SPTR substructure items
    
        C++ signature :
            boost::python::dict GetFlattenedFunctionalGroupHierarchy([ bool=False])
    """
def GetFunctionalGroupHierarchy() -> FilterCatalog:
    """
        Returns the functional group hierarchy filter catalog
    
        C++ signature :
            RDKix::FilterCatalog GetFunctionalGroupHierarchy()
    """
def RunFilterCatalog(filterCatalog: FilterCatalog, smiles: _vectSs, numThreads: int = 1) -> FilterCatalogListOfEntryList:
    """
        Run the filter catalog on the input list of smiles strings.
        Use numThreads=0 to use all available processors. Returns a vector of vectors.  For each input smiles, a vector of FilterCatalogEntry objects are returned for each matched filter.  If a molecule matches no filter, the vector will be empty. If a smiles string can't be parsed, a 'Bad smiles' entry is returned.
    
        C++ signature :
            std::vector<std::vector<boost::shared_ptr<RDKix::FilterCatalogEntry const>, std::allocator<boost::shared_ptr<RDKix::FilterCatalogEntry const> > >, std::allocator<std::vector<boost::shared_ptr<RDKix::FilterCatalogEntry const>, std::allocator<boost::shared_ptr<RDKix::FilterCatalogEntry const> > > > > RunFilterCatalog(RDKix::FilterCatalog,std::vector<std::string, std::allocator<std::string> > [,int=1])
    """
