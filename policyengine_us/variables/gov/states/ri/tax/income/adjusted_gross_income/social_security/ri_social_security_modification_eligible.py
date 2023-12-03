from policyengine_us.model_api import *


class ri_social_security_modification_eligible(Variable):
    value_type = bool
    entity = TaxUnit
    label = "Eligible for the Rhode Island Social Security Modification"
    definition_period = YEAR
    reference = "https://tax.ri.gov/sites/g/files/xkgbur541/files/2022-12/Social%20Security%20Worksheet_w.pdf"
    # MODIFICATION FOR TAXABLE SOCIAL SECURITY INCOME WORKSHEET STEP 1: Eligibility
    defined_for = StateCode.RI

    def formula(tax_unit, period, parameters):
        person = tax_unit.members
        income = tax_unit("adjusted_gross_income", period)
        filing_status = tax_unit("filing_status", period)
        age = person("age", period)
        birth_year = period.start.year - age

        p = parameters(
            period
        ).gov.states.ri.tax.income.adjusted_gross_income.subtractions.social_security.threshold

        # Age eligibility.
        age_conditions = birth_year <= p.birth_year
        head_or_spouse = person("is_tax_unit_head_or_spouse", period)
        age_eligible = tax_unit.any(age_conditions & head_or_spouse)

        # Income eligibility.
        income_eligible = income < p.income[filing_status]

        return age_eligible & income_eligible
