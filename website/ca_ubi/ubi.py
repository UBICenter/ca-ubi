from openfisca_us.model_api import *

def create_ubi_reform(person_amount: float) -> Reform:   
    class ca_basic_income(Variable):
        value_type = float
        entity = Person
        definition_period = YEAR
        label = "Basic income"

        def formula(person, period):
            return person_amount

    class spm_unit_is_in_spm_poverty(Variable):
        value_type = bool
        entity = SPMUnit
        label = "SPM unit in SPM poverty"
        definition_period = YEAR

        def formula(spm_unit, period, parameters):
            income = spm_unit("spm_unit_net_income", period) + add(spm_unit, period, ["ca_basic_income"])
            poverty_threshold = spm_unit("spm_unit_spm_threshold", period)
            return income < poverty_threshold

    class spm_unit_is_in_deep_spm_poverty(Variable):
        value_type = bool
        entity = SPMUnit
        label = "SPM unit in deep SPM poverty"
        definition_period = YEAR

        def formula(spm_unit, period, parameters):
            income = spm_unit("spm_unit_net_income", period) + add(spm_unit, period, ["ca_basic_income"])
            poverty_threshold = spm_unit("spm_unit_spm_threshold", period) / 2
            return income < poverty_threshold

    class ubi_reform(Reform):
        def apply(self):
            self.add_variable(ca_basic_income)
            self.update_variable(spm_unit_is_in_spm_poverty)
            self.update_variable(spm_unit_is_in_deep_spm_poverty)
    
    return ubi_reform
