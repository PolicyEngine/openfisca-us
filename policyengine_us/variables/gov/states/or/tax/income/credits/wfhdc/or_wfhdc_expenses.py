from policyengine_us.model_api import *


class or_wfhdc_expenses(Variable):
    value_type = float
    entity = TaxUnit
    label = "Oregon working family household and dependent care expenses"
    unit = USD
    definition_period = YEAR
    reference = ("https://oregon.public.law/statutes/ors_315.264",)

    def formula(tax_unit, period, parameters):
        # First, cap based on the number of eligible care receivers
        expenses = tax_unit("tax_unit_childcare_expenses", period)
        p_cdcc = parameters(period).gov.irs.credits.cdcc
        p_or = parameters(period).gov.states["or"].tax.income.credits.wfhdc
        count_eligible = min_(
            p_cdcc.eligibility.max, tax_unit("count_cdcc_eligible", period)
        )
        eligible_capped_expenses = min_(
            expenses, p_or.max_amount * count_eligible
        )

        # Then, cap further to the lowest earnings between the taxpayer and spouse
        return min_(
            eligible_capped_expenses,
            tax_unit("min_head_spouse_earned", period),
        )
