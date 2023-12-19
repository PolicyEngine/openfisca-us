from policyengine_us.model_api import *


class ms_taxable_income_indiv(Variable):
    value_type = float
    entity = Person
    label = "Mississippi taxable income individually"
    unit = USD
    definition_period = YEAR
    reference = (
        "https://www.dor.ms.gov/sites/default/files/Forms/Individual/80100221.pdf#page=13",
        "https://www.dor.ms.gov/sites/default/files/Forms/Individual/80105228.pdf",  # Line 38 - 49,
    )
    defined_for = StateCode.MS

    def formula(person, period, parameters):
        agi = person("ms_agi_indiv", period)
        deductions = person("ms_deductions_indiv", period)
        exemptions = person("ms_total_exemptions_indiv", period)
        return max_(agi - deductions - exemptions, 0)
