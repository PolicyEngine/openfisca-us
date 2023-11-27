from policyengine_us.model_api import *


class md_tanf_gross_unearned_income(Variable):
    value_type = float
    entity = SPMUnit
    label = "Maryland TANF gross unearned income"
    unit = USD
    definition_period = YEAR
    defined_for = StateCode.MD

    def formula(spm_unit, period, parameters):
        p = parameters(period).gov.states.md.tanf.income.sources
        gross_unearned = add(spm_unit, period, p.unearned)
        return gross_unearned
