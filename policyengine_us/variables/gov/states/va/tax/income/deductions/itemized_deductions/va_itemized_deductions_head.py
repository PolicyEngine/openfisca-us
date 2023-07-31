from policyengine_us.model_api import *


class va_itemized_deductions_head(Variable):
    value_type = float
    entity = Person
    label = "Virginia itemized deduction for head when filling separately"
    unit = USD
    definition_period = YEAR
    reference = (
        "https://law.lis.virginia.gov/vacodefull/title58.1/chapter3/article2/",
        "§ 58.1-322.03.(1.a.)",
        "https://www.tax.virginia.gov/sites/default/files/vatax-pdf/2022-760-instructions.pdf#page=18",
    )
    defined_for = StateCode.VA

    def formula(person, period, parameters):
        unit_deds = person.tax_unit("va_itemized_deductions_joint", period)
        return unit_deds * person.tax_unit("va_prorate_fraction_head", period)
