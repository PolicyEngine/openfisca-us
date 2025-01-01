from policyengine_us.model_api import *


class UtilityType(Enum):
    ELECTRICITY = "Electricity"
    HEATING_OIL = "Heating Oil"
    LIQUID_GAS = "Liquid Gas"
    NATURAL_GAS = "Natural Gas"
    WOOD_PELLETS = "Wood Pellets"


class utlility_type(Variable):
    value_type = Enum
    entity = spm_unit
    possible_values = UtilityType
    default_value = UtilityType.ELECTRICITY
    definition_period = YEAR
    label = "Utiltiy types for LIHEAP payout"
