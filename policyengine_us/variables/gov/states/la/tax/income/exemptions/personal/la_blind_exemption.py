from policyengine_us.model_api import *


class la_blind_exemption(Variable):
    value_type = float
    entity = TaxUnit
    label = "Louisiana blind exemption"
    unit = USD
    definition_period = YEAR
    reference = (
        "https://www.revenue.louisiana.gov/taxforms/6935(11_02)F.pdf#page=1"
    )
    defined_for = StateCode.LA

    def formula(tax_unit, period, parameters):
        amount = parameters(
            period
        ).gov.states.la.tax.income.exemptions.personal.blind
        blind_head = tax_unit("blind_head", period)
        blind_spouse = tax_unit("blind_spouse", period)
        head_eligible = (blind_head).astype(int)
        spouse_eligible = (blind_spouse).astype(int)
        return (head_eligible + spouse_eligible) * amount
