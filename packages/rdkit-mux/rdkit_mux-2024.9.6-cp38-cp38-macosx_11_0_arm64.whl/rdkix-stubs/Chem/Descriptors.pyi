from __future__ import annotations
from collections import abc
from rdkix import Chem
import rdkix.Chem.ChemUtils.DescriptorUtilities
from rdkix.Chem.ChemUtils import DescriptorUtilities as _du
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_1
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_10
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_100
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_101
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_102
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_103
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_104
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_105
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_106
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_107
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_108
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_109
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_11
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_110
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_111
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_112
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_113
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_114
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_115
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_116
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_117
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_118
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_119
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_12
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_120
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_121
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_122
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_123
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_124
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_125
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_126
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_127
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_128
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_129
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_13
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_130
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_131
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_132
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_133
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_134
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_135
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_136
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_137
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_138
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_139
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_14
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_140
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_141
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_142
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_143
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_144
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_145
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_146
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_147
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_148
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_149
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_15
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_150
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_151
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_152
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_153
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_154
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_155
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_156
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_157
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_158
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_159
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_16
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_160
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_161
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_162
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_163
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_164
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_165
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_166
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_167
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_168
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_169
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_17
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_170
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_171
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_172
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_173
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_174
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_175
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_176
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_177
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_178
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_179
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_18
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_180
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_181
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_182
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_183
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_184
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_185
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_186
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_187
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_188
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_189
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_19
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_190
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_191
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_192
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_2
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_20
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_21
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_22
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_23
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_24
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_25
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_26
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_27
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_28
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_29
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_3
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_30
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_31
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_32
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_33
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_34
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_35
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_36
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_37
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_38
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_39
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_4
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_40
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_41
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_42
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_43
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_44
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_45
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_46
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_47
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_48
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_49
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_5
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_50
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_51
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_52
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_53
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_54
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_55
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_56
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_57
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_58
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_59
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_6
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_60
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_61
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_62
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_63
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_64
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_65
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_66
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_67
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_68
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_69
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_7
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_70
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_71
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_72
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_73
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_74
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_75
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_76
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_77
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_78
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_79
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_8
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_80
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_81
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_82
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_83
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_84
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_85
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_86
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_87
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_88
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_89
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_9
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_90
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_91
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_92
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_93
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_94
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_95
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_96
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_97
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_98
from rdkix.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_99
from rdkix.Chem.ChemUtils.DescriptorUtilities import BCUT2D_CHGHI
from rdkix.Chem.ChemUtils.DescriptorUtilities import BCUT2D_CHGLO
from rdkix.Chem.ChemUtils.DescriptorUtilities import BCUT2D_LOGPHI
from rdkix.Chem.ChemUtils.DescriptorUtilities import BCUT2D_LOGPLOW
from rdkix.Chem.ChemUtils.DescriptorUtilities import BCUT2D_MRHI
from rdkix.Chem.ChemUtils.DescriptorUtilities import BCUT2D_MRLOW
from rdkix.Chem.ChemUtils.DescriptorUtilities import BCUT2D_MWHI
from rdkix.Chem.ChemUtils.DescriptorUtilities import BCUT2D_MWLOW
import rdkix.Chem.EState.EState
from rdkix.Chem.EState.EState import MaxAbsEStateIndex
from rdkix.Chem.EState.EState import MaxEStateIndex
from rdkix.Chem.EState.EState import MinAbsEStateIndex
from rdkix.Chem.EState.EState import MinEStateIndex
import rdkix.Chem.EState.EState_VSA
from rdkix.Chem.EState.EState_VSA import EState_VSA1
from rdkix.Chem.EState.EState_VSA import EState_VSA10
from rdkix.Chem.EState.EState_VSA import EState_VSA11
from rdkix.Chem.EState.EState_VSA import EState_VSA2
from rdkix.Chem.EState.EState_VSA import EState_VSA3
from rdkix.Chem.EState.EState_VSA import EState_VSA4
from rdkix.Chem.EState.EState_VSA import EState_VSA5
from rdkix.Chem.EState.EState_VSA import EState_VSA6
from rdkix.Chem.EState.EState_VSA import EState_VSA7
from rdkix.Chem.EState.EState_VSA import EState_VSA8
from rdkix.Chem.EState.EState_VSA import EState_VSA9
import rdkix.Chem.GraphDescriptors
from rdkix.Chem.GraphDescriptors import AvgIpc
from rdkix.Chem.GraphDescriptors import BalabanJ
from rdkix.Chem.GraphDescriptors import BertzCT
from rdkix.Chem.GraphDescriptors import Chi0
from rdkix.Chem.GraphDescriptors import Chi1
from rdkix.Chem.GraphDescriptors import Ipc
import rdkix.Chem.Lipinski
from rdkix.Chem.Lipinski import HeavyAtomCount
import rdkix.Chem.QED
from rdkix.Chem.QED import qed
import rdkix.Chem.SpacialScore
from rdkix.Chem.SpacialScore import SPS
from rdkix.Chem import rdFingerprintGenerator
from rdkix.Chem import rdMolDescriptors
import rdkix.Chem.rdMolDescriptors
from rdkix.Chem import rdMolDescriptors as _rdMolDescriptors
from rdkix.Chem import rdPartialCharges
__all__ = ['AUTOCORR2D_1', 'AUTOCORR2D_10', 'AUTOCORR2D_100', 'AUTOCORR2D_101', 'AUTOCORR2D_102', 'AUTOCORR2D_103', 'AUTOCORR2D_104', 'AUTOCORR2D_105', 'AUTOCORR2D_106', 'AUTOCORR2D_107', 'AUTOCORR2D_108', 'AUTOCORR2D_109', 'AUTOCORR2D_11', 'AUTOCORR2D_110', 'AUTOCORR2D_111', 'AUTOCORR2D_112', 'AUTOCORR2D_113', 'AUTOCORR2D_114', 'AUTOCORR2D_115', 'AUTOCORR2D_116', 'AUTOCORR2D_117', 'AUTOCORR2D_118', 'AUTOCORR2D_119', 'AUTOCORR2D_12', 'AUTOCORR2D_120', 'AUTOCORR2D_121', 'AUTOCORR2D_122', 'AUTOCORR2D_123', 'AUTOCORR2D_124', 'AUTOCORR2D_125', 'AUTOCORR2D_126', 'AUTOCORR2D_127', 'AUTOCORR2D_128', 'AUTOCORR2D_129', 'AUTOCORR2D_13', 'AUTOCORR2D_130', 'AUTOCORR2D_131', 'AUTOCORR2D_132', 'AUTOCORR2D_133', 'AUTOCORR2D_134', 'AUTOCORR2D_135', 'AUTOCORR2D_136', 'AUTOCORR2D_137', 'AUTOCORR2D_138', 'AUTOCORR2D_139', 'AUTOCORR2D_14', 'AUTOCORR2D_140', 'AUTOCORR2D_141', 'AUTOCORR2D_142', 'AUTOCORR2D_143', 'AUTOCORR2D_144', 'AUTOCORR2D_145', 'AUTOCORR2D_146', 'AUTOCORR2D_147', 'AUTOCORR2D_148', 'AUTOCORR2D_149', 'AUTOCORR2D_15', 'AUTOCORR2D_150', 'AUTOCORR2D_151', 'AUTOCORR2D_152', 'AUTOCORR2D_153', 'AUTOCORR2D_154', 'AUTOCORR2D_155', 'AUTOCORR2D_156', 'AUTOCORR2D_157', 'AUTOCORR2D_158', 'AUTOCORR2D_159', 'AUTOCORR2D_16', 'AUTOCORR2D_160', 'AUTOCORR2D_161', 'AUTOCORR2D_162', 'AUTOCORR2D_163', 'AUTOCORR2D_164', 'AUTOCORR2D_165', 'AUTOCORR2D_166', 'AUTOCORR2D_167', 'AUTOCORR2D_168', 'AUTOCORR2D_169', 'AUTOCORR2D_17', 'AUTOCORR2D_170', 'AUTOCORR2D_171', 'AUTOCORR2D_172', 'AUTOCORR2D_173', 'AUTOCORR2D_174', 'AUTOCORR2D_175', 'AUTOCORR2D_176', 'AUTOCORR2D_177', 'AUTOCORR2D_178', 'AUTOCORR2D_179', 'AUTOCORR2D_18', 'AUTOCORR2D_180', 'AUTOCORR2D_181', 'AUTOCORR2D_182', 'AUTOCORR2D_183', 'AUTOCORR2D_184', 'AUTOCORR2D_185', 'AUTOCORR2D_186', 'AUTOCORR2D_187', 'AUTOCORR2D_188', 'AUTOCORR2D_189', 'AUTOCORR2D_19', 'AUTOCORR2D_190', 'AUTOCORR2D_191', 'AUTOCORR2D_192', 'AUTOCORR2D_2', 'AUTOCORR2D_20', 'AUTOCORR2D_21', 'AUTOCORR2D_22', 'AUTOCORR2D_23', 'AUTOCORR2D_24', 'AUTOCORR2D_25', 'AUTOCORR2D_26', 'AUTOCORR2D_27', 'AUTOCORR2D_28', 'AUTOCORR2D_29', 'AUTOCORR2D_3', 'AUTOCORR2D_30', 'AUTOCORR2D_31', 'AUTOCORR2D_32', 'AUTOCORR2D_33', 'AUTOCORR2D_34', 'AUTOCORR2D_35', 'AUTOCORR2D_36', 'AUTOCORR2D_37', 'AUTOCORR2D_38', 'AUTOCORR2D_39', 'AUTOCORR2D_4', 'AUTOCORR2D_40', 'AUTOCORR2D_41', 'AUTOCORR2D_42', 'AUTOCORR2D_43', 'AUTOCORR2D_44', 'AUTOCORR2D_45', 'AUTOCORR2D_46', 'AUTOCORR2D_47', 'AUTOCORR2D_48', 'AUTOCORR2D_49', 'AUTOCORR2D_5', 'AUTOCORR2D_50', 'AUTOCORR2D_51', 'AUTOCORR2D_52', 'AUTOCORR2D_53', 'AUTOCORR2D_54', 'AUTOCORR2D_55', 'AUTOCORR2D_56', 'AUTOCORR2D_57', 'AUTOCORR2D_58', 'AUTOCORR2D_59', 'AUTOCORR2D_6', 'AUTOCORR2D_60', 'AUTOCORR2D_61', 'AUTOCORR2D_62', 'AUTOCORR2D_63', 'AUTOCORR2D_64', 'AUTOCORR2D_65', 'AUTOCORR2D_66', 'AUTOCORR2D_67', 'AUTOCORR2D_68', 'AUTOCORR2D_69', 'AUTOCORR2D_7', 'AUTOCORR2D_70', 'AUTOCORR2D_71', 'AUTOCORR2D_72', 'AUTOCORR2D_73', 'AUTOCORR2D_74', 'AUTOCORR2D_75', 'AUTOCORR2D_76', 'AUTOCORR2D_77', 'AUTOCORR2D_78', 'AUTOCORR2D_79', 'AUTOCORR2D_8', 'AUTOCORR2D_80', 'AUTOCORR2D_81', 'AUTOCORR2D_82', 'AUTOCORR2D_83', 'AUTOCORR2D_84', 'AUTOCORR2D_85', 'AUTOCORR2D_86', 'AUTOCORR2D_87', 'AUTOCORR2D_88', 'AUTOCORR2D_89', 'AUTOCORR2D_9', 'AUTOCORR2D_90', 'AUTOCORR2D_91', 'AUTOCORR2D_92', 'AUTOCORR2D_93', 'AUTOCORR2D_94', 'AUTOCORR2D_95', 'AUTOCORR2D_96', 'AUTOCORR2D_97', 'AUTOCORR2D_98', 'AUTOCORR2D_99', 'AvgIpc', 'BCUT2D_CHGHI', 'BCUT2D_CHGLO', 'BCUT2D_LOGPHI', 'BCUT2D_LOGPLOW', 'BCUT2D_MRHI', 'BCUT2D_MRLOW', 'BCUT2D_MWHI', 'BCUT2D_MWLOW', 'BalabanJ', 'BertzCT', 'CalcMolDescriptors', 'Chem', 'Chi0', 'Chi1', 'EState_VSA1', 'EState_VSA10', 'EState_VSA11', 'EState_VSA2', 'EState_VSA3', 'EState_VSA4', 'EState_VSA5', 'EState_VSA6', 'EState_VSA7', 'EState_VSA8', 'EState_VSA9', 'FpDensityMorgan1', 'FpDensityMorgan2', 'FpDensityMorgan3', 'HeavyAtomCount', 'HeavyAtomMolWt', 'Ipc', 'MaxAbsEStateIndex', 'MaxAbsPartialCharge', 'MaxEStateIndex', 'MaxPartialCharge', 'MinAbsEStateIndex', 'MinAbsPartialCharge', 'MinEStateIndex', 'MinPartialCharge', 'NumRadicalElectrons', 'NumValenceElectrons', 'PropertyFunctor', 'SPS', 'abc', 'autocorr', 'descList', 'names', 'qed', 'rdFingerprintGenerator', 'rdMolDescriptors', 'rdPartialCharges', 'setupAUTOCorrDescriptors']
class PropertyFunctor(rdkix.Chem.rdMolDescriptors.PythonPropertyFunctor):
    """
    Creates a python based property function that can be added to the
        global property list.  To use, subclass this class and override the
        __call__ method.  Then create an instance and add it to the
        registry.  The __call__ method should return a numeric value.
    
        Example:
    
          class NumAtoms(Descriptors.PropertyFunctor):
            def __init__(self):
              Descriptors.PropertyFunctor.__init__(self, "NumAtoms", "1.0.0")
            def __call__(self, mol):
              return mol.GetNumAtoms()
    
          numAtoms = NumAtoms()
          rdMolDescriptors.Properties.RegisterProperty(numAtoms)
        
    """
    def __call__(self, mol):
        ...
    def __init__(self, name, version):
        ...
def CalcMolDescriptors(mol, missingVal = None, silent = True):
    """
     calculate the full set of descriptors for a molecule
        
        Parameters
        ----------
        mol : RDKix molecule
        missingVal : float, optional
                     This will be used if a particular descriptor cannot be calculated
        silent : bool, optional
                 if True then exception messages from descriptors will be displayed
    
        Returns
        -------
        dict 
             A dictionary with decriptor names as keys and the descriptor values as values
        
    """
def FpDensityMorgan1(x):
    ...
def FpDensityMorgan2(x):
    ...
def FpDensityMorgan3(x):
    ...
def HeavyAtomMolWt(x):
    """
    The average molecular weight of the molecule ignoring hydrogens
    
      >>> HeavyAtomMolWt(Chem.MolFromSmiles('CC'))
      24.02...
      >>> HeavyAtomMolWt(Chem.MolFromSmiles('[NH4+].[Cl-]'))
      49.46
    
    """
def MaxAbsPartialCharge(mol, force = False):
    ...
def MaxPartialCharge(mol, force = False):
    ...
def MinAbsPartialCharge(mol, force = False):
    ...
def MinPartialCharge(mol, force = False):
    ...
def NumRadicalElectrons(mol):
    """
     The number of radical electrons the molecule has
          (says nothing about spin state)
    
        >>> NumRadicalElectrons(Chem.MolFromSmiles('CC'))
        0
        >>> NumRadicalElectrons(Chem.MolFromSmiles('C[CH3]'))
        0
        >>> NumRadicalElectrons(Chem.MolFromSmiles('C[CH2]'))
        1
        >>> NumRadicalElectrons(Chem.MolFromSmiles('C[CH]'))
        2
        >>> NumRadicalElectrons(Chem.MolFromSmiles('C[C]'))
        3
    
        
    """
def NumValenceElectrons(mol):
    """
     The number of valence electrons the molecule has
    
        >>> NumValenceElectrons(Chem.MolFromSmiles('CC'))
        14
        >>> NumValenceElectrons(Chem.MolFromSmiles('C(=O)O'))
        18
        >>> NumValenceElectrons(Chem.MolFromSmiles('C(=O)[O-]'))
        18
        >>> NumValenceElectrons(Chem.MolFromSmiles('C(=O)'))
        12
    
        
    """
def _ChargeDescriptors(mol, force = False):
    ...
def _FingerprintDensity(mol, func, *args, **kwargs):
    ...
def _getMorganCountFingerprint(mol, radius):
    ...
def _isCallable(thing):
    ...
def _runDoctests(verbose = None):
    ...
def _setupDescriptors(namespace):
    ...
def setupAUTOCorrDescriptors():
    """
    Adds AUTOCORR descriptors to the default descriptor lists
    """
_descList: list  # value = [('MaxAbsEStateIndex', rdkix.Chem.EState.EState.MaxAbsEStateIndex), ('MaxEStateIndex', rdkix.Chem.EState.EState.MaxEStateIndex), ('MinAbsEStateIndex', rdkix.Chem.EState.EState.MinAbsEStateIndex), ('MinEStateIndex', rdkix.Chem.EState.EState.MinEStateIndex), ('qed', rdkix.Chem.QED.qed), ('SPS', rdkix.Chem.SpacialScore.SPS), ('MolWt', <function <lambda> at 0x10f9821f0>), ('HeavyAtomMolWt', HeavyAtomMolWt), ('ExactMolWt', <function <lambda> at 0x10f982310>), ('NumValenceElectrons', NumValenceElectrons), ('NumRadicalElectrons', NumRadicalElectrons), ('MaxPartialCharge', MaxPartialCharge), ('MinPartialCharge', MinPartialCharge), ('MaxAbsPartialCharge', MaxAbsPartialCharge), ('MinAbsPartialCharge', MinAbsPartialCharge), ('FpDensityMorgan1', FpDensityMorgan1), ('FpDensityMorgan2', FpDensityMorgan2), ('FpDensityMorgan3', FpDensityMorgan3), ('BCUT2D_MWHI', rdkix.Chem.ChemUtils.DescriptorUtilities.BCUT2D_MWHI), ('BCUT2D_MWLOW', rdkix.Chem.ChemUtils.DescriptorUtilities.BCUT2D_MWLOW), ('BCUT2D_CHGHI', rdkix.Chem.ChemUtils.DescriptorUtilities.BCUT2D_CHGHI), ('BCUT2D_CHGLO', rdkix.Chem.ChemUtils.DescriptorUtilities.BCUT2D_CHGLO), ('BCUT2D_LOGPHI', rdkix.Chem.ChemUtils.DescriptorUtilities.BCUT2D_LOGPHI), ('BCUT2D_LOGPLOW', rdkix.Chem.ChemUtils.DescriptorUtilities.BCUT2D_LOGPLOW), ('BCUT2D_MRHI', rdkix.Chem.ChemUtils.DescriptorUtilities.BCUT2D_MRHI), ('BCUT2D_MRLOW', rdkix.Chem.ChemUtils.DescriptorUtilities.BCUT2D_MRLOW), ('AvgIpc', rdkix.Chem.GraphDescriptors.AvgIpc), ('BalabanJ', rdkix.Chem.GraphDescriptors.BalabanJ), ('BertzCT', rdkix.Chem.GraphDescriptors.BertzCT), ('Chi0', rdkix.Chem.GraphDescriptors.Chi0), ('Chi0n', <function <lambda> at 0x10fcbf550>), ('Chi0v', <function <lambda> at 0x10fcbf1f0>), ('Chi1', rdkix.Chem.GraphDescriptors.Chi1), ('Chi1n', <function <lambda> at 0x10fcbf5e0>), ('Chi1v', <function <lambda> at 0x10fcbf280>), ('Chi2n', <function <lambda> at 0x10fcbf670>), ('Chi2v', <function <lambda> at 0x10fcbf310>), ('Chi3n', <function <lambda> at 0x10fcbf700>), ('Chi3v', <function <lambda> at 0x10fcbf3a0>), ('Chi4n', <function <lambda> at 0x10fcbf790>), ('Chi4v', <function <lambda> at 0x10fcbf430>), ('HallKierAlpha', <function <lambda> at 0x10f995670>), ('Ipc', rdkix.Chem.GraphDescriptors.Ipc), ('Kappa1', <function <lambda> at 0x10f995700>), ('Kappa2', <function <lambda> at 0x10f995790>), ('Kappa3', <function <lambda> at 0x10f995820>), ('LabuteASA', <function <lambda> at 0x10f973ca0>), ('PEOE_VSA1', <function _InstallDescriptors.<locals>.<lambda> at 0x10f973430>), ('PEOE_VSA10', <function _InstallDescriptors.<locals>.<lambda> at 0x10f973940>), ('PEOE_VSA11', <function _InstallDescriptors.<locals>.<lambda> at 0x10f9739d0>), ('PEOE_VSA12', <function _InstallDescriptors.<locals>.<lambda> at 0x10f973a60>), ('PEOE_VSA13', <function _InstallDescriptors.<locals>.<lambda> at 0x10f973af0>), ('PEOE_VSA14', <function _InstallDescriptors.<locals>.<lambda> at 0x10f973b80>), ('PEOE_VSA2', <function _InstallDescriptors.<locals>.<lambda> at 0x10f9734c0>), ('PEOE_VSA3', <function _InstallDescriptors.<locals>.<lambda> at 0x10f973550>), ('PEOE_VSA4', <function _InstallDescriptors.<locals>.<lambda> at 0x10f9735e0>), ('PEOE_VSA5', <function _InstallDescriptors.<locals>.<lambda> at 0x10f973670>), ('PEOE_VSA6', <function _InstallDescriptors.<locals>.<lambda> at 0x10f973700>), ('PEOE_VSA7', <function _InstallDescriptors.<locals>.<lambda> at 0x10f973790>), ('PEOE_VSA8', <function _InstallDescriptors.<locals>.<lambda> at 0x10f973820>), ('PEOE_VSA9', <function _InstallDescriptors.<locals>.<lambda> at 0x10f9738b0>), ('SMR_VSA1', <function _InstallDescriptors.<locals>.<lambda> at 0x10f96d790>), ('SMR_VSA10', <function _InstallDescriptors.<locals>.<lambda> at 0x10f96dca0>), ('SMR_VSA2', <function _InstallDescriptors.<locals>.<lambda> at 0x10f96d820>), ('SMR_VSA3', <function _InstallDescriptors.<locals>.<lambda> at 0x10f96d8b0>), ('SMR_VSA4', <function _InstallDescriptors.<locals>.<lambda> at 0x10f96d940>), ('SMR_VSA5', <function _InstallDescriptors.<locals>.<lambda> at 0x10f96d9d0>), ('SMR_VSA6', <function _InstallDescriptors.<locals>.<lambda> at 0x10f96da60>), ('SMR_VSA7', <function _InstallDescriptors.<locals>.<lambda> at 0x10f96daf0>), ('SMR_VSA8', <function _InstallDescriptors.<locals>.<lambda> at 0x10f96db80>), ('SMR_VSA9', <function _InstallDescriptors.<locals>.<lambda> at 0x10f96dc10>), ('SlogP_VSA1', <function _InstallDescriptors.<locals>.<lambda> at 0x10f96dd30>), ('SlogP_VSA10', <function _InstallDescriptors.<locals>.<lambda> at 0x10f973280>), ('SlogP_VSA11', <function _InstallDescriptors.<locals>.<lambda> at 0x10f973310>), ('SlogP_VSA12', <function _InstallDescriptors.<locals>.<lambda> at 0x10f9733a0>), ('SlogP_VSA2', <function _InstallDescriptors.<locals>.<lambda> at 0x10f96ddc0>), ('SlogP_VSA3', <function _InstallDescriptors.<locals>.<lambda> at 0x10f96de50>), ('SlogP_VSA4', <function _InstallDescriptors.<locals>.<lambda> at 0x10f96dee0>), ('SlogP_VSA5', <function _InstallDescriptors.<locals>.<lambda> at 0x10f96df70>), ('SlogP_VSA6', <function _InstallDescriptors.<locals>.<lambda> at 0x10f973040>), ('SlogP_VSA7', <function _InstallDescriptors.<locals>.<lambda> at 0x10f9730d0>), ('SlogP_VSA8', <function _InstallDescriptors.<locals>.<lambda> at 0x10f973160>), ('SlogP_VSA9', <function _InstallDescriptors.<locals>.<lambda> at 0x10f9731f0>), ('TPSA', <function <lambda> at 0x10f973e50>), ('EState_VSA1', rdkix.Chem.EState.EState_VSA.EState_VSA1), ('EState_VSA10', rdkix.Chem.EState.EState_VSA.EState_VSA10), ('EState_VSA11', rdkix.Chem.EState.EState_VSA.EState_VSA11), ('EState_VSA2', rdkix.Chem.EState.EState_VSA.EState_VSA2), ('EState_VSA3', rdkix.Chem.EState.EState_VSA.EState_VSA3), ('EState_VSA4', rdkix.Chem.EState.EState_VSA.EState_VSA4), ('EState_VSA5', rdkix.Chem.EState.EState_VSA.EState_VSA5), ('EState_VSA6', rdkix.Chem.EState.EState_VSA.EState_VSA6), ('EState_VSA7', rdkix.Chem.EState.EState_VSA.EState_VSA7), ('EState_VSA8', rdkix.Chem.EState.EState_VSA.EState_VSA8), ('EState_VSA9', rdkix.Chem.EState.EState_VSA.EState_VSA9), ('VSA_EState1', <function _descriptor_VSA_EState.<locals>.VSA_EState_bin at 0x10fcc2280>), ('VSA_EState10', <function _descriptor_VSA_EState.<locals>.VSA_EState_bin at 0x10fcc2790>), ('VSA_EState2', <function _descriptor_VSA_EState.<locals>.VSA_EState_bin at 0x10fcc2310>), ('VSA_EState3', <function _descriptor_VSA_EState.<locals>.VSA_EState_bin at 0x10fcc23a0>), ('VSA_EState4', <function _descriptor_VSA_EState.<locals>.VSA_EState_bin at 0x10fcc2430>), ('VSA_EState5', <function _descriptor_VSA_EState.<locals>.VSA_EState_bin at 0x10fcc24c0>), ('VSA_EState6', <function _descriptor_VSA_EState.<locals>.VSA_EState_bin at 0x10fcc2550>), ('VSA_EState7', <function _descriptor_VSA_EState.<locals>.VSA_EState_bin at 0x10fcc25e0>), ('VSA_EState8', <function _descriptor_VSA_EState.<locals>.VSA_EState_bin at 0x10fcc2670>), ('VSA_EState9', <function _descriptor_VSA_EState.<locals>.VSA_EState_bin at 0x10fcc2700>), ('FractionCSP3', <function <lambda> at 0x10fcc6310>), ('HeavyAtomCount', rdkix.Chem.Lipinski.HeavyAtomCount), ('NHOHCount', <function <lambda> at 0x10fcc6160>), ('NOCount', <function <lambda> at 0x10fcc60d0>), ('NumAliphaticCarbocycles', <function <lambda> at 0x10fcc6820>), ('NumAliphaticHeterocycles', <function <lambda> at 0x10fcc6790>), ('NumAliphaticRings', <function <lambda> at 0x10fcc6700>), ('NumAmideBonds', <function <lambda> at 0x10fcc69d0>), ('NumAromaticCarbocycles', <function <lambda> at 0x10fcc6550>), ('NumAromaticHeterocycles', <function <lambda> at 0x10fcc64c0>), ('NumAromaticRings', <function <lambda> at 0x10fcc63a0>), ('NumAtomStereoCenters', <function <lambda> at 0x10fcc6a60>), ('NumBridgeheadAtoms', <function <lambda> at 0x10fcc6940>), ('NumHAcceptors', <function <lambda> at 0x10fcbfd30>), ('NumHDonors', <function <lambda> at 0x10fcbfc10>), ('NumHeteroatoms', <function <lambda> at 0x10fcbfe50>), ('NumHeterocycles', <function <lambda> at 0x10fcc6af0>), ('NumRotatableBonds', <function <lambda> at 0x10fcbff70>), ('NumSaturatedCarbocycles', <function <lambda> at 0x10fcc6670>), ('NumSaturatedHeterocycles', <function <lambda> at 0x10fcc65e0>), ('NumSaturatedRings', <function <lambda> at 0x10fcc6430>), ('NumSpiroAtoms', <function <lambda> at 0x10fcc6b80>), ('NumUnspecifiedAtomStereoCenters', <function <lambda> at 0x10fcc68b0>), ('Phi', <function <lambda> at 0x10fcc6c10>), ('RingCount', <function <lambda> at 0x10fcc61f0>), ('MolLogP', <function <lambda> at 0x10f96d280>), ('MolMR', <function <lambda> at 0x10f96d310>), ('fr_Al_COO', <function _LoadPatterns.<locals>.<lambda> at 0x10f98d3a0>), ('fr_Al_OH', <function _LoadPatterns.<locals>.<lambda> at 0x10f98d0d0>), ('fr_Al_OH_noTert', <function _LoadPatterns.<locals>.<lambda> at 0x10f992a60>), ('fr_ArN', <function _LoadPatterns.<locals>.<lambda> at 0x10f992f70>), ('fr_Ar_COO', <function _LoadPatterns.<locals>.<lambda> at 0x10f98d430>), ('fr_Ar_N', <function _LoadPatterns.<locals>.<lambda> at 0x10f98da60>), ('fr_Ar_NH', <function _LoadPatterns.<locals>.<lambda> at 0x10f98daf0>), ('fr_Ar_OH', <function _LoadPatterns.<locals>.<lambda> at 0x10f98d160>), ('fr_COO', <function _LoadPatterns.<locals>.<lambda> at 0x10f98d4c0>), ('fr_COO2', <function _LoadPatterns.<locals>.<lambda> at 0x10f98d550>), ('fr_C_O', <function _LoadPatterns.<locals>.<lambda> at 0x10f985f70>), ('fr_C_O_noCOO', <function _LoadPatterns.<locals>.<lambda> at 0x10f98d040>), ('fr_C_S', <function _LoadPatterns.<locals>.<lambda> at 0x10f98f940>), ('fr_HOCCN', <function _LoadPatterns.<locals>.<lambda> at 0x10f995040>), ('fr_Imine', <function _LoadPatterns.<locals>.<lambda> at 0x10f98dc10>), ('fr_NH0', <function _LoadPatterns.<locals>.<lambda> at 0x10f98d9d0>), ('fr_NH1', <function _LoadPatterns.<locals>.<lambda> at 0x10f98d940>), ('fr_NH2', <function _LoadPatterns.<locals>.<lambda> at 0x10f98d8b0>), ('fr_N_O', <function _LoadPatterns.<locals>.<lambda> at 0x10f98dee0>), ('fr_Ndealkylation1', <function _LoadPatterns.<locals>.<lambda> at 0x10f992d30>), ('fr_Ndealkylation2', <function _LoadPatterns.<locals>.<lambda> at 0x10f992dc0>), ('fr_Nhpyrrole', <function _LoadPatterns.<locals>.<lambda> at 0x10f98f430>), ('fr_SH', <function _LoadPatterns.<locals>.<lambda> at 0x10f98f8b0>), ('fr_aldehyde', <function _LoadPatterns.<locals>.<lambda> at 0x10f98d790>), ('fr_alkyl_carbamate', <function _LoadPatterns.<locals>.<lambda> at 0x10f992e50>), ('fr_alkyl_halide', <function _LoadPatterns.<locals>.<lambda> at 0x10f98f790>), ('fr_allylic_oxid', <function _LoadPatterns.<locals>.<lambda> at 0x10f992ca0>), ('fr_amide', <function _LoadPatterns.<locals>.<lambda> at 0x10f98f1f0>), ('fr_amidine', <function _LoadPatterns.<locals>.<lambda> at 0x10f98f310>), ('fr_aniline', <function _LoadPatterns.<locals>.<lambda> at 0x10f98db80>), ('fr_aryl_methyl', <function _LoadPatterns.<locals>.<lambda> at 0x10f992c10>), ('fr_azide', <function _LoadPatterns.<locals>.<lambda> at 0x10f98f160>), ('fr_azo', <function _LoadPatterns.<locals>.<lambda> at 0x10f98f040>), ('fr_barbitur', <function _LoadPatterns.<locals>.<lambda> at 0x10f98fb80>), ('fr_benzene', <function _LoadPatterns.<locals>.<lambda> at 0x10f992670>), ('fr_benzodiazepine', <function _LoadPatterns.<locals>.<lambda> at 0x10f992af0>), ('fr_bicyclic', <function _LoadPatterns.<locals>.<lambda> at 0x10f9924c0>), ('fr_diazo', <function _LoadPatterns.<locals>.<lambda> at 0x10f98f0d0>), ('fr_dihydropyridine', <function _LoadPatterns.<locals>.<lambda> at 0x10f9929d0>), ('fr_epoxide', <function _LoadPatterns.<locals>.<lambda> at 0x10f992430>), ('fr_ester', <function _LoadPatterns.<locals>.<lambda> at 0x10f98d310>), ('fr_ether', <function _LoadPatterns.<locals>.<lambda> at 0x10f98d670>), ('fr_furan', <function _LoadPatterns.<locals>.<lambda> at 0x10f98fdc0>), ('fr_guanido', <function _LoadPatterns.<locals>.<lambda> at 0x10f98f3a0>), ('fr_halogen', <function _LoadPatterns.<locals>.<lambda> at 0x10f98f700>), ('fr_hdrzine', <function _LoadPatterns.<locals>.<lambda> at 0x10f98ddc0>), ('fr_hdrzone', <function _LoadPatterns.<locals>.<lambda> at 0x10f98dd30>), ('fr_imidazole', <function _LoadPatterns.<locals>.<lambda> at 0x10f98fd30>), ('fr_imide', <function _LoadPatterns.<locals>.<lambda> at 0x10f98f4c0>), ('fr_isocyan', <function _LoadPatterns.<locals>.<lambda> at 0x10f98f550>), ('fr_isothiocyan', <function _LoadPatterns.<locals>.<lambda> at 0x10f98f5e0>), ('fr_ketone', <function _LoadPatterns.<locals>.<lambda> at 0x10f98d5e0>), ('fr_ketone_Topliss', <function _LoadPatterns.<locals>.<lambda> at 0x10f992ee0>), ('fr_lactam', <function _LoadPatterns.<locals>.<lambda> at 0x10f992280>), ('fr_lactone', <function _LoadPatterns.<locals>.<lambda> at 0x10f992310>), ('fr_methoxy', <function _LoadPatterns.<locals>.<lambda> at 0x10f98d1f0>), ('fr_morpholine', <function _LoadPatterns.<locals>.<lambda> at 0x10f9921f0>), ('fr_nitrile', <function _LoadPatterns.<locals>.<lambda> at 0x10f98dca0>), ('fr_nitro', <function _LoadPatterns.<locals>.<lambda> at 0x10f98df70>), ('fr_nitro_arom', <function _LoadPatterns.<locals>.<lambda> at 0x10f992820>), ('fr_nitro_arom_nonortho', <function _LoadPatterns.<locals>.<lambda> at 0x10f9928b0>), ('fr_nitroso', <function _LoadPatterns.<locals>.<lambda> at 0x10f98de50>), ('fr_oxazole', <function _LoadPatterns.<locals>.<lambda> at 0x10f98ff70>), ('fr_oxime', <function _LoadPatterns.<locals>.<lambda> at 0x10f98d280>), ('fr_para_hydroxylation', <function _LoadPatterns.<locals>.<lambda> at 0x10f992b80>), ('fr_phenol', <function _LoadPatterns.<locals>.<lambda> at 0x10f98d700>), ('fr_phenol_noOrthoHbond', <function _LoadPatterns.<locals>.<lambda> at 0x10f992940>), ('fr_phos_acid', <function _LoadPatterns.<locals>.<lambda> at 0x10f992700>), ('fr_phos_ester', <function _LoadPatterns.<locals>.<lambda> at 0x10f992790>), ('fr_piperdine', <function _LoadPatterns.<locals>.<lambda> at 0x10f9920d0>), ('fr_piperzine', <function _LoadPatterns.<locals>.<lambda> at 0x10f992160>), ('fr_priamide', <function _LoadPatterns.<locals>.<lambda> at 0x10f98f280>), ('fr_prisulfonamd', <function _LoadPatterns.<locals>.<lambda> at 0x10f98faf0>), ('fr_pyridine', <function _LoadPatterns.<locals>.<lambda> at 0x10f992040>), ('fr_quatN', <function _LoadPatterns.<locals>.<lambda> at 0x10f98d820>), ('fr_sulfide', <function _LoadPatterns.<locals>.<lambda> at 0x10f98f820>), ('fr_sulfonamd', <function _LoadPatterns.<locals>.<lambda> at 0x10f98fa60>), ('fr_sulfone', <function _LoadPatterns.<locals>.<lambda> at 0x10f98f9d0>), ('fr_term_acetylene', <function _LoadPatterns.<locals>.<lambda> at 0x10f98fca0>), ('fr_tetrazole', <function _LoadPatterns.<locals>.<lambda> at 0x10f9923a0>), ('fr_thiazole', <function _LoadPatterns.<locals>.<lambda> at 0x10f98fee0>), ('fr_thiocyan', <function _LoadPatterns.<locals>.<lambda> at 0x10f98f670>), ('fr_thiophene', <function _LoadPatterns.<locals>.<lambda> at 0x10f98fe50>), ('fr_unbrch_alkane', <function _LoadPatterns.<locals>.<lambda> at 0x10f9925e0>), ('fr_urea', <function _LoadPatterns.<locals>.<lambda> at 0x10f98fc10>)]
autocorr: rdkix.Chem.ChemUtils.DescriptorUtilities.VectorDescriptorWrapper  # value = <rdkix.Chem.ChemUtils.DescriptorUtilities.VectorDescriptorWrapper object>
descList: list  # value = [('MaxAbsEStateIndex', rdkix.Chem.EState.EState.MaxAbsEStateIndex), ('MaxEStateIndex', rdkix.Chem.EState.EState.MaxEStateIndex), ('MinAbsEStateIndex', rdkix.Chem.EState.EState.MinAbsEStateIndex), ('MinEStateIndex', rdkix.Chem.EState.EState.MinEStateIndex), ('qed', rdkix.Chem.QED.qed), ('SPS', rdkix.Chem.SpacialScore.SPS), ('MolWt', <function <lambda> at 0x10f9821f0>), ('HeavyAtomMolWt', HeavyAtomMolWt), ('ExactMolWt', <function <lambda> at 0x10f982310>), ('NumValenceElectrons', NumValenceElectrons), ('NumRadicalElectrons', NumRadicalElectrons), ('MaxPartialCharge', MaxPartialCharge), ('MinPartialCharge', MinPartialCharge), ('MaxAbsPartialCharge', MaxAbsPartialCharge), ('MinAbsPartialCharge', MinAbsPartialCharge), ('FpDensityMorgan1', FpDensityMorgan1), ('FpDensityMorgan2', FpDensityMorgan2), ('FpDensityMorgan3', FpDensityMorgan3), ('BCUT2D_MWHI', rdkix.Chem.ChemUtils.DescriptorUtilities.BCUT2D_MWHI), ('BCUT2D_MWLOW', rdkix.Chem.ChemUtils.DescriptorUtilities.BCUT2D_MWLOW), ('BCUT2D_CHGHI', rdkix.Chem.ChemUtils.DescriptorUtilities.BCUT2D_CHGHI), ('BCUT2D_CHGLO', rdkix.Chem.ChemUtils.DescriptorUtilities.BCUT2D_CHGLO), ('BCUT2D_LOGPHI', rdkix.Chem.ChemUtils.DescriptorUtilities.BCUT2D_LOGPHI), ('BCUT2D_LOGPLOW', rdkix.Chem.ChemUtils.DescriptorUtilities.BCUT2D_LOGPLOW), ('BCUT2D_MRHI', rdkix.Chem.ChemUtils.DescriptorUtilities.BCUT2D_MRHI), ('BCUT2D_MRLOW', rdkix.Chem.ChemUtils.DescriptorUtilities.BCUT2D_MRLOW), ('AvgIpc', rdkix.Chem.GraphDescriptors.AvgIpc), ('BalabanJ', rdkix.Chem.GraphDescriptors.BalabanJ), ('BertzCT', rdkix.Chem.GraphDescriptors.BertzCT), ('Chi0', rdkix.Chem.GraphDescriptors.Chi0), ('Chi0n', <function <lambda> at 0x10fcbf550>), ('Chi0v', <function <lambda> at 0x10fcbf1f0>), ('Chi1', rdkix.Chem.GraphDescriptors.Chi1), ('Chi1n', <function <lambda> at 0x10fcbf5e0>), ('Chi1v', <function <lambda> at 0x10fcbf280>), ('Chi2n', <function <lambda> at 0x10fcbf670>), ('Chi2v', <function <lambda> at 0x10fcbf310>), ('Chi3n', <function <lambda> at 0x10fcbf700>), ('Chi3v', <function <lambda> at 0x10fcbf3a0>), ('Chi4n', <function <lambda> at 0x10fcbf790>), ('Chi4v', <function <lambda> at 0x10fcbf430>), ('HallKierAlpha', <function <lambda> at 0x10f995670>), ('Ipc', rdkix.Chem.GraphDescriptors.Ipc), ('Kappa1', <function <lambda> at 0x10f995700>), ('Kappa2', <function <lambda> at 0x10f995790>), ('Kappa3', <function <lambda> at 0x10f995820>), ('LabuteASA', <function <lambda> at 0x10f973ca0>), ('PEOE_VSA1', <function _InstallDescriptors.<locals>.<lambda> at 0x10f973430>), ('PEOE_VSA10', <function _InstallDescriptors.<locals>.<lambda> at 0x10f973940>), ('PEOE_VSA11', <function _InstallDescriptors.<locals>.<lambda> at 0x10f9739d0>), ('PEOE_VSA12', <function _InstallDescriptors.<locals>.<lambda> at 0x10f973a60>), ('PEOE_VSA13', <function _InstallDescriptors.<locals>.<lambda> at 0x10f973af0>), ('PEOE_VSA14', <function _InstallDescriptors.<locals>.<lambda> at 0x10f973b80>), ('PEOE_VSA2', <function _InstallDescriptors.<locals>.<lambda> at 0x10f9734c0>), ('PEOE_VSA3', <function _InstallDescriptors.<locals>.<lambda> at 0x10f973550>), ('PEOE_VSA4', <function _InstallDescriptors.<locals>.<lambda> at 0x10f9735e0>), ('PEOE_VSA5', <function _InstallDescriptors.<locals>.<lambda> at 0x10f973670>), ('PEOE_VSA6', <function _InstallDescriptors.<locals>.<lambda> at 0x10f973700>), ('PEOE_VSA7', <function _InstallDescriptors.<locals>.<lambda> at 0x10f973790>), ('PEOE_VSA8', <function _InstallDescriptors.<locals>.<lambda> at 0x10f973820>), ('PEOE_VSA9', <function _InstallDescriptors.<locals>.<lambda> at 0x10f9738b0>), ('SMR_VSA1', <function _InstallDescriptors.<locals>.<lambda> at 0x10f96d790>), ('SMR_VSA10', <function _InstallDescriptors.<locals>.<lambda> at 0x10f96dca0>), ('SMR_VSA2', <function _InstallDescriptors.<locals>.<lambda> at 0x10f96d820>), ('SMR_VSA3', <function _InstallDescriptors.<locals>.<lambda> at 0x10f96d8b0>), ('SMR_VSA4', <function _InstallDescriptors.<locals>.<lambda> at 0x10f96d940>), ('SMR_VSA5', <function _InstallDescriptors.<locals>.<lambda> at 0x10f96d9d0>), ('SMR_VSA6', <function _InstallDescriptors.<locals>.<lambda> at 0x10f96da60>), ('SMR_VSA7', <function _InstallDescriptors.<locals>.<lambda> at 0x10f96daf0>), ('SMR_VSA8', <function _InstallDescriptors.<locals>.<lambda> at 0x10f96db80>), ('SMR_VSA9', <function _InstallDescriptors.<locals>.<lambda> at 0x10f96dc10>), ('SlogP_VSA1', <function _InstallDescriptors.<locals>.<lambda> at 0x10f96dd30>), ('SlogP_VSA10', <function _InstallDescriptors.<locals>.<lambda> at 0x10f973280>), ('SlogP_VSA11', <function _InstallDescriptors.<locals>.<lambda> at 0x10f973310>), ('SlogP_VSA12', <function _InstallDescriptors.<locals>.<lambda> at 0x10f9733a0>), ('SlogP_VSA2', <function _InstallDescriptors.<locals>.<lambda> at 0x10f96ddc0>), ('SlogP_VSA3', <function _InstallDescriptors.<locals>.<lambda> at 0x10f96de50>), ('SlogP_VSA4', <function _InstallDescriptors.<locals>.<lambda> at 0x10f96dee0>), ('SlogP_VSA5', <function _InstallDescriptors.<locals>.<lambda> at 0x10f96df70>), ('SlogP_VSA6', <function _InstallDescriptors.<locals>.<lambda> at 0x10f973040>), ('SlogP_VSA7', <function _InstallDescriptors.<locals>.<lambda> at 0x10f9730d0>), ('SlogP_VSA8', <function _InstallDescriptors.<locals>.<lambda> at 0x10f973160>), ('SlogP_VSA9', <function _InstallDescriptors.<locals>.<lambda> at 0x10f9731f0>), ('TPSA', <function <lambda> at 0x10f973e50>), ('EState_VSA1', rdkix.Chem.EState.EState_VSA.EState_VSA1), ('EState_VSA10', rdkix.Chem.EState.EState_VSA.EState_VSA10), ('EState_VSA11', rdkix.Chem.EState.EState_VSA.EState_VSA11), ('EState_VSA2', rdkix.Chem.EState.EState_VSA.EState_VSA2), ('EState_VSA3', rdkix.Chem.EState.EState_VSA.EState_VSA3), ('EState_VSA4', rdkix.Chem.EState.EState_VSA.EState_VSA4), ('EState_VSA5', rdkix.Chem.EState.EState_VSA.EState_VSA5), ('EState_VSA6', rdkix.Chem.EState.EState_VSA.EState_VSA6), ('EState_VSA7', rdkix.Chem.EState.EState_VSA.EState_VSA7), ('EState_VSA8', rdkix.Chem.EState.EState_VSA.EState_VSA8), ('EState_VSA9', rdkix.Chem.EState.EState_VSA.EState_VSA9), ('VSA_EState1', <function _descriptor_VSA_EState.<locals>.VSA_EState_bin at 0x10fcc2280>), ('VSA_EState10', <function _descriptor_VSA_EState.<locals>.VSA_EState_bin at 0x10fcc2790>), ('VSA_EState2', <function _descriptor_VSA_EState.<locals>.VSA_EState_bin at 0x10fcc2310>), ('VSA_EState3', <function _descriptor_VSA_EState.<locals>.VSA_EState_bin at 0x10fcc23a0>), ('VSA_EState4', <function _descriptor_VSA_EState.<locals>.VSA_EState_bin at 0x10fcc2430>), ('VSA_EState5', <function _descriptor_VSA_EState.<locals>.VSA_EState_bin at 0x10fcc24c0>), ('VSA_EState6', <function _descriptor_VSA_EState.<locals>.VSA_EState_bin at 0x10fcc2550>), ('VSA_EState7', <function _descriptor_VSA_EState.<locals>.VSA_EState_bin at 0x10fcc25e0>), ('VSA_EState8', <function _descriptor_VSA_EState.<locals>.VSA_EState_bin at 0x10fcc2670>), ('VSA_EState9', <function _descriptor_VSA_EState.<locals>.VSA_EState_bin at 0x10fcc2700>), ('FractionCSP3', <function <lambda> at 0x10fcc6310>), ('HeavyAtomCount', rdkix.Chem.Lipinski.HeavyAtomCount), ('NHOHCount', <function <lambda> at 0x10fcc6160>), ('NOCount', <function <lambda> at 0x10fcc60d0>), ('NumAliphaticCarbocycles', <function <lambda> at 0x10fcc6820>), ('NumAliphaticHeterocycles', <function <lambda> at 0x10fcc6790>), ('NumAliphaticRings', <function <lambda> at 0x10fcc6700>), ('NumAmideBonds', <function <lambda> at 0x10fcc69d0>), ('NumAromaticCarbocycles', <function <lambda> at 0x10fcc6550>), ('NumAromaticHeterocycles', <function <lambda> at 0x10fcc64c0>), ('NumAromaticRings', <function <lambda> at 0x10fcc63a0>), ('NumAtomStereoCenters', <function <lambda> at 0x10fcc6a60>), ('NumBridgeheadAtoms', <function <lambda> at 0x10fcc6940>), ('NumHAcceptors', <function <lambda> at 0x10fcbfd30>), ('NumHDonors', <function <lambda> at 0x10fcbfc10>), ('NumHeteroatoms', <function <lambda> at 0x10fcbfe50>), ('NumHeterocycles', <function <lambda> at 0x10fcc6af0>), ('NumRotatableBonds', <function <lambda> at 0x10fcbff70>), ('NumSaturatedCarbocycles', <function <lambda> at 0x10fcc6670>), ('NumSaturatedHeterocycles', <function <lambda> at 0x10fcc65e0>), ('NumSaturatedRings', <function <lambda> at 0x10fcc6430>), ('NumSpiroAtoms', <function <lambda> at 0x10fcc6b80>), ('NumUnspecifiedAtomStereoCenters', <function <lambda> at 0x10fcc68b0>), ('Phi', <function <lambda> at 0x10fcc6c10>), ('RingCount', <function <lambda> at 0x10fcc61f0>), ('MolLogP', <function <lambda> at 0x10f96d280>), ('MolMR', <function <lambda> at 0x10f96d310>), ('fr_Al_COO', <function _LoadPatterns.<locals>.<lambda> at 0x10f98d3a0>), ('fr_Al_OH', <function _LoadPatterns.<locals>.<lambda> at 0x10f98d0d0>), ('fr_Al_OH_noTert', <function _LoadPatterns.<locals>.<lambda> at 0x10f992a60>), ('fr_ArN', <function _LoadPatterns.<locals>.<lambda> at 0x10f992f70>), ('fr_Ar_COO', <function _LoadPatterns.<locals>.<lambda> at 0x10f98d430>), ('fr_Ar_N', <function _LoadPatterns.<locals>.<lambda> at 0x10f98da60>), ('fr_Ar_NH', <function _LoadPatterns.<locals>.<lambda> at 0x10f98daf0>), ('fr_Ar_OH', <function _LoadPatterns.<locals>.<lambda> at 0x10f98d160>), ('fr_COO', <function _LoadPatterns.<locals>.<lambda> at 0x10f98d4c0>), ('fr_COO2', <function _LoadPatterns.<locals>.<lambda> at 0x10f98d550>), ('fr_C_O', <function _LoadPatterns.<locals>.<lambda> at 0x10f985f70>), ('fr_C_O_noCOO', <function _LoadPatterns.<locals>.<lambda> at 0x10f98d040>), ('fr_C_S', <function _LoadPatterns.<locals>.<lambda> at 0x10f98f940>), ('fr_HOCCN', <function _LoadPatterns.<locals>.<lambda> at 0x10f995040>), ('fr_Imine', <function _LoadPatterns.<locals>.<lambda> at 0x10f98dc10>), ('fr_NH0', <function _LoadPatterns.<locals>.<lambda> at 0x10f98d9d0>), ('fr_NH1', <function _LoadPatterns.<locals>.<lambda> at 0x10f98d940>), ('fr_NH2', <function _LoadPatterns.<locals>.<lambda> at 0x10f98d8b0>), ('fr_N_O', <function _LoadPatterns.<locals>.<lambda> at 0x10f98dee0>), ('fr_Ndealkylation1', <function _LoadPatterns.<locals>.<lambda> at 0x10f992d30>), ('fr_Ndealkylation2', <function _LoadPatterns.<locals>.<lambda> at 0x10f992dc0>), ('fr_Nhpyrrole', <function _LoadPatterns.<locals>.<lambda> at 0x10f98f430>), ('fr_SH', <function _LoadPatterns.<locals>.<lambda> at 0x10f98f8b0>), ('fr_aldehyde', <function _LoadPatterns.<locals>.<lambda> at 0x10f98d790>), ('fr_alkyl_carbamate', <function _LoadPatterns.<locals>.<lambda> at 0x10f992e50>), ('fr_alkyl_halide', <function _LoadPatterns.<locals>.<lambda> at 0x10f98f790>), ('fr_allylic_oxid', <function _LoadPatterns.<locals>.<lambda> at 0x10f992ca0>), ('fr_amide', <function _LoadPatterns.<locals>.<lambda> at 0x10f98f1f0>), ('fr_amidine', <function _LoadPatterns.<locals>.<lambda> at 0x10f98f310>), ('fr_aniline', <function _LoadPatterns.<locals>.<lambda> at 0x10f98db80>), ('fr_aryl_methyl', <function _LoadPatterns.<locals>.<lambda> at 0x10f992c10>), ('fr_azide', <function _LoadPatterns.<locals>.<lambda> at 0x10f98f160>), ('fr_azo', <function _LoadPatterns.<locals>.<lambda> at 0x10f98f040>), ('fr_barbitur', <function _LoadPatterns.<locals>.<lambda> at 0x10f98fb80>), ('fr_benzene', <function _LoadPatterns.<locals>.<lambda> at 0x10f992670>), ('fr_benzodiazepine', <function _LoadPatterns.<locals>.<lambda> at 0x10f992af0>), ('fr_bicyclic', <function _LoadPatterns.<locals>.<lambda> at 0x10f9924c0>), ('fr_diazo', <function _LoadPatterns.<locals>.<lambda> at 0x10f98f0d0>), ('fr_dihydropyridine', <function _LoadPatterns.<locals>.<lambda> at 0x10f9929d0>), ('fr_epoxide', <function _LoadPatterns.<locals>.<lambda> at 0x10f992430>), ('fr_ester', <function _LoadPatterns.<locals>.<lambda> at 0x10f98d310>), ('fr_ether', <function _LoadPatterns.<locals>.<lambda> at 0x10f98d670>), ('fr_furan', <function _LoadPatterns.<locals>.<lambda> at 0x10f98fdc0>), ('fr_guanido', <function _LoadPatterns.<locals>.<lambda> at 0x10f98f3a0>), ('fr_halogen', <function _LoadPatterns.<locals>.<lambda> at 0x10f98f700>), ('fr_hdrzine', <function _LoadPatterns.<locals>.<lambda> at 0x10f98ddc0>), ('fr_hdrzone', <function _LoadPatterns.<locals>.<lambda> at 0x10f98dd30>), ('fr_imidazole', <function _LoadPatterns.<locals>.<lambda> at 0x10f98fd30>), ('fr_imide', <function _LoadPatterns.<locals>.<lambda> at 0x10f98f4c0>), ('fr_isocyan', <function _LoadPatterns.<locals>.<lambda> at 0x10f98f550>), ('fr_isothiocyan', <function _LoadPatterns.<locals>.<lambda> at 0x10f98f5e0>), ('fr_ketone', <function _LoadPatterns.<locals>.<lambda> at 0x10f98d5e0>), ('fr_ketone_Topliss', <function _LoadPatterns.<locals>.<lambda> at 0x10f992ee0>), ('fr_lactam', <function _LoadPatterns.<locals>.<lambda> at 0x10f992280>), ('fr_lactone', <function _LoadPatterns.<locals>.<lambda> at 0x10f992310>), ('fr_methoxy', <function _LoadPatterns.<locals>.<lambda> at 0x10f98d1f0>), ('fr_morpholine', <function _LoadPatterns.<locals>.<lambda> at 0x10f9921f0>), ('fr_nitrile', <function _LoadPatterns.<locals>.<lambda> at 0x10f98dca0>), ('fr_nitro', <function _LoadPatterns.<locals>.<lambda> at 0x10f98df70>), ('fr_nitro_arom', <function _LoadPatterns.<locals>.<lambda> at 0x10f992820>), ('fr_nitro_arom_nonortho', <function _LoadPatterns.<locals>.<lambda> at 0x10f9928b0>), ('fr_nitroso', <function _LoadPatterns.<locals>.<lambda> at 0x10f98de50>), ('fr_oxazole', <function _LoadPatterns.<locals>.<lambda> at 0x10f98ff70>), ('fr_oxime', <function _LoadPatterns.<locals>.<lambda> at 0x10f98d280>), ('fr_para_hydroxylation', <function _LoadPatterns.<locals>.<lambda> at 0x10f992b80>), ('fr_phenol', <function _LoadPatterns.<locals>.<lambda> at 0x10f98d700>), ('fr_phenol_noOrthoHbond', <function _LoadPatterns.<locals>.<lambda> at 0x10f992940>), ('fr_phos_acid', <function _LoadPatterns.<locals>.<lambda> at 0x10f992700>), ('fr_phos_ester', <function _LoadPatterns.<locals>.<lambda> at 0x10f992790>), ('fr_piperdine', <function _LoadPatterns.<locals>.<lambda> at 0x10f9920d0>), ('fr_piperzine', <function _LoadPatterns.<locals>.<lambda> at 0x10f992160>), ('fr_priamide', <function _LoadPatterns.<locals>.<lambda> at 0x10f98f280>), ('fr_prisulfonamd', <function _LoadPatterns.<locals>.<lambda> at 0x10f98faf0>), ('fr_pyridine', <function _LoadPatterns.<locals>.<lambda> at 0x10f992040>), ('fr_quatN', <function _LoadPatterns.<locals>.<lambda> at 0x10f98d820>), ('fr_sulfide', <function _LoadPatterns.<locals>.<lambda> at 0x10f98f820>), ('fr_sulfonamd', <function _LoadPatterns.<locals>.<lambda> at 0x10f98fa60>), ('fr_sulfone', <function _LoadPatterns.<locals>.<lambda> at 0x10f98f9d0>), ('fr_term_acetylene', <function _LoadPatterns.<locals>.<lambda> at 0x10f98fca0>), ('fr_tetrazole', <function _LoadPatterns.<locals>.<lambda> at 0x10f9923a0>), ('fr_thiazole', <function _LoadPatterns.<locals>.<lambda> at 0x10f98fee0>), ('fr_thiocyan', <function _LoadPatterns.<locals>.<lambda> at 0x10f98f670>), ('fr_thiophene', <function _LoadPatterns.<locals>.<lambda> at 0x10f98fe50>), ('fr_unbrch_alkane', <function _LoadPatterns.<locals>.<lambda> at 0x10f9925e0>), ('fr_urea', <function _LoadPatterns.<locals>.<lambda> at 0x10f98fc10>)]
names: list = ['AUTOCORR2D_1', 'AUTOCORR2D_2', 'AUTOCORR2D_3', 'AUTOCORR2D_4', 'AUTOCORR2D_5', 'AUTOCORR2D_6', 'AUTOCORR2D_7', 'AUTOCORR2D_8', 'AUTOCORR2D_9', 'AUTOCORR2D_10', 'AUTOCORR2D_11', 'AUTOCORR2D_12', 'AUTOCORR2D_13', 'AUTOCORR2D_14', 'AUTOCORR2D_15', 'AUTOCORR2D_16', 'AUTOCORR2D_17', 'AUTOCORR2D_18', 'AUTOCORR2D_19', 'AUTOCORR2D_20', 'AUTOCORR2D_21', 'AUTOCORR2D_22', 'AUTOCORR2D_23', 'AUTOCORR2D_24', 'AUTOCORR2D_25', 'AUTOCORR2D_26', 'AUTOCORR2D_27', 'AUTOCORR2D_28', 'AUTOCORR2D_29', 'AUTOCORR2D_30', 'AUTOCORR2D_31', 'AUTOCORR2D_32', 'AUTOCORR2D_33', 'AUTOCORR2D_34', 'AUTOCORR2D_35', 'AUTOCORR2D_36', 'AUTOCORR2D_37', 'AUTOCORR2D_38', 'AUTOCORR2D_39', 'AUTOCORR2D_40', 'AUTOCORR2D_41', 'AUTOCORR2D_42', 'AUTOCORR2D_43', 'AUTOCORR2D_44', 'AUTOCORR2D_45', 'AUTOCORR2D_46', 'AUTOCORR2D_47', 'AUTOCORR2D_48', 'AUTOCORR2D_49', 'AUTOCORR2D_50', 'AUTOCORR2D_51', 'AUTOCORR2D_52', 'AUTOCORR2D_53', 'AUTOCORR2D_54', 'AUTOCORR2D_55', 'AUTOCORR2D_56', 'AUTOCORR2D_57', 'AUTOCORR2D_58', 'AUTOCORR2D_59', 'AUTOCORR2D_60', 'AUTOCORR2D_61', 'AUTOCORR2D_62', 'AUTOCORR2D_63', 'AUTOCORR2D_64', 'AUTOCORR2D_65', 'AUTOCORR2D_66', 'AUTOCORR2D_67', 'AUTOCORR2D_68', 'AUTOCORR2D_69', 'AUTOCORR2D_70', 'AUTOCORR2D_71', 'AUTOCORR2D_72', 'AUTOCORR2D_73', 'AUTOCORR2D_74', 'AUTOCORR2D_75', 'AUTOCORR2D_76', 'AUTOCORR2D_77', 'AUTOCORR2D_78', 'AUTOCORR2D_79', 'AUTOCORR2D_80', 'AUTOCORR2D_81', 'AUTOCORR2D_82', 'AUTOCORR2D_83', 'AUTOCORR2D_84', 'AUTOCORR2D_85', 'AUTOCORR2D_86', 'AUTOCORR2D_87', 'AUTOCORR2D_88', 'AUTOCORR2D_89', 'AUTOCORR2D_90', 'AUTOCORR2D_91', 'AUTOCORR2D_92', 'AUTOCORR2D_93', 'AUTOCORR2D_94', 'AUTOCORR2D_95', 'AUTOCORR2D_96', 'AUTOCORR2D_97', 'AUTOCORR2D_98', 'AUTOCORR2D_99', 'AUTOCORR2D_100', 'AUTOCORR2D_101', 'AUTOCORR2D_102', 'AUTOCORR2D_103', 'AUTOCORR2D_104', 'AUTOCORR2D_105', 'AUTOCORR2D_106', 'AUTOCORR2D_107', 'AUTOCORR2D_108', 'AUTOCORR2D_109', 'AUTOCORR2D_110', 'AUTOCORR2D_111', 'AUTOCORR2D_112', 'AUTOCORR2D_113', 'AUTOCORR2D_114', 'AUTOCORR2D_115', 'AUTOCORR2D_116', 'AUTOCORR2D_117', 'AUTOCORR2D_118', 'AUTOCORR2D_119', 'AUTOCORR2D_120', 'AUTOCORR2D_121', 'AUTOCORR2D_122', 'AUTOCORR2D_123', 'AUTOCORR2D_124', 'AUTOCORR2D_125', 'AUTOCORR2D_126', 'AUTOCORR2D_127', 'AUTOCORR2D_128', 'AUTOCORR2D_129', 'AUTOCORR2D_130', 'AUTOCORR2D_131', 'AUTOCORR2D_132', 'AUTOCORR2D_133', 'AUTOCORR2D_134', 'AUTOCORR2D_135', 'AUTOCORR2D_136', 'AUTOCORR2D_137', 'AUTOCORR2D_138', 'AUTOCORR2D_139', 'AUTOCORR2D_140', 'AUTOCORR2D_141', 'AUTOCORR2D_142', 'AUTOCORR2D_143', 'AUTOCORR2D_144', 'AUTOCORR2D_145', 'AUTOCORR2D_146', 'AUTOCORR2D_147', 'AUTOCORR2D_148', 'AUTOCORR2D_149', 'AUTOCORR2D_150', 'AUTOCORR2D_151', 'AUTOCORR2D_152', 'AUTOCORR2D_153', 'AUTOCORR2D_154', 'AUTOCORR2D_155', 'AUTOCORR2D_156', 'AUTOCORR2D_157', 'AUTOCORR2D_158', 'AUTOCORR2D_159', 'AUTOCORR2D_160', 'AUTOCORR2D_161', 'AUTOCORR2D_162', 'AUTOCORR2D_163', 'AUTOCORR2D_164', 'AUTOCORR2D_165', 'AUTOCORR2D_166', 'AUTOCORR2D_167', 'AUTOCORR2D_168', 'AUTOCORR2D_169', 'AUTOCORR2D_170', 'AUTOCORR2D_171', 'AUTOCORR2D_172', 'AUTOCORR2D_173', 'AUTOCORR2D_174', 'AUTOCORR2D_175', 'AUTOCORR2D_176', 'AUTOCORR2D_177', 'AUTOCORR2D_178', 'AUTOCORR2D_179', 'AUTOCORR2D_180', 'AUTOCORR2D_181', 'AUTOCORR2D_182', 'AUTOCORR2D_183', 'AUTOCORR2D_184', 'AUTOCORR2D_185', 'AUTOCORR2D_186', 'AUTOCORR2D_187', 'AUTOCORR2D_188', 'AUTOCORR2D_189', 'AUTOCORR2D_190', 'AUTOCORR2D_191', 'AUTOCORR2D_192']
