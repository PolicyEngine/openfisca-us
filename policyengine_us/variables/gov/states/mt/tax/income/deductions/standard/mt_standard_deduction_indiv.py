from policyengine_us.model_api import *


class mt_standard_deduction_indiv(Variable):
    value_type = float
    entity = Person
    label = "Montana standard deduction when married couples are filing separately"
    unit = USD
    definition_period = YEAR
    defined_for = StateCode.MT

    def formula(person, period, parameters):
        us_filing_status = person.tax_unit("filing_status", period)
        fsvals = us_filing_status.possible_values
        filing_status = select(
            [
                us_filing_status == fsvals.JOINT,
                us_filing_status == fsvals.SINGLE,
                us_filing_status == fsvals.SEPARATE,
                us_filing_status == fsvals.HEAD_OF_HOUSEHOLD,
                us_filing_status == fsvals.WIDOW,
            ],
            [
                fsvals.SEPARATE,  # couples are filing separately on Montana form
                fsvals.SINGLE,
                fsvals.SEPARATE,
                fsvals.HEAD_OF_HOUSEHOLD,
                fsvals.WIDOW,
            ],
        )
        p = parameters(period).gov.states.mt.tax.income.deductions.standard
        agi = person("mt_agi", period)
        # standard deduction is a percentage of AGI that
        # is bounded by a min/max by filing status.
        min_amount = p.min[filing_status]
        max_amount = p.max[filing_status]
        uncapped_amount = p.rate * agi
        deduction_amount = min_(uncapped_amount, max_amount)
        is_head_or_spouse = person("is_tax_unit_head_or_spouse", period)
        return is_head_or_spouse * max_(deduction_amount, min_amount)
