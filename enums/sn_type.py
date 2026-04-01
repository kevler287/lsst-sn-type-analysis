from enum import Enum
from typing import Optional

class SNLabel(Enum):
    SN_IA = 0
    SN_II = 1
    SN_IBC = 2

class SNType(str, Enum):
    # Ia
    SN_IA = "SN Ia"
    SN_IA_91T = "SN Ia-91T-like"
    SN_IA_91BG = "SN Ia-91bg-like"
    SN_IA_PEC = "SN Ia-pec"
    SN_IA_CSM = "SN Ia-CSM"
    SN_IA_SC = "SN Ia-SC"
    SN_IA_CA_RICH = "SN Ia-Ca-rich"
    SN_IAX = "SN Iax[02cx-like]"

    # II
    SN_II = "SN II"
    SN_IIN = "SN IIn"
    SN_IIP = "SN IIP"
    SN_IIB = "SN IIb"
    SN_IIL = "SN IIL"
    SN_IIN_PEC = "SN IIn-pec"
    SN_II_PEC = "SN II-pec"
    SLSN_II = "SLSN-II"

    # Ib/c
    SN_IC = "SN Ic"
    SN_IB = "SN Ib"
    SN_IC_BL = "SN Ic-BL"
    SN_IBC = "SN Ib/c"
    SN_IBN = "SN Ibn"
    SN_ICN = "SN Icn"
    SN_IB_PEC = "SN Ib-pec"
    SN_IC_PEC = "SN Ic-pec"
    SN_IB_CA_RICH = "SN Ib-Ca-rich"
    SN_IC_CA_RICH = "SN Ic-Ca-rich"
    SN_IBN_ICN = "SN Ibn/Icn"
    SN_IEN = "SN Ien"
    SLSN_I = "SLSN-I"

    # Ambiguous
    SN = "SN"
    SN_I = "SN I"

    @staticmethod
    def from_string(s: str) -> Optional["SNType"]:
        try:
            return SNType(s)
        except ValueError:
            return None

    @staticmethod
    def to_upper_group(s: str) -> Optional[int]:
        IA = {
            SNType.SN_IA, SNType.SN_IA_91T, SNType.SN_IA_91BG,
            SNType.SN_IA_PEC, SNType.SN_IA_CSM, SNType.SN_IA_SC,
            SNType.SN_IA_CA_RICH, SNType.SN_IAX,
        }
        II = {
            SNType.SN_II, SNType.SN_IIN, SNType.SN_IIP, SNType.SN_IIB,
            SNType.SN_IIL, SNType.SN_IIN_PEC, SNType.SN_II_PEC, SNType.SLSN_II,
        }
        IBC = {
            SNType.SN_IC, SNType.SN_IB, SNType.SN_IC_BL, SNType.SN_IBC,
            SNType.SN_IBN, SNType.SN_ICN, SNType.SN_IB_PEC, SNType.SN_IC_PEC,
            SNType.SN_IB_CA_RICH, SNType.SN_IC_CA_RICH, SNType.SN_IBN_ICN,
            SNType.SN_IEN, SNType.SLSN_I,
        }

        sn = SNType.from_string(s)

        if sn in IA:  return SNLabel.SN_IA.value
        if sn in II:  return SNLabel.SN_II.value
        if sn in IBC: return SNLabel.SN_IBC.value
        return None
    
    @staticmethod
    def filter_sub_groups(s: str) -> Optional[int]:
        sn = SNType.from_string(s)

        if sn in [SNType.SN_IA]:  return SNLabel.SN_IA.value
        if sn in [SNType.SN_II]:  return SNLabel.SN_II.value
        if sn in [SNType.SN_IB, SNType.SN_IC, SNType.SN_IBC]: return SNLabel.SN_IBC.value
        return None