from openfisca_us.model_api import *

def create_ubi_reform(person_amount: float) -> Reform:
    def set_ubi_parameter(parameters: ParameterNode) -> ParameterNode:
        for i in range(3):
            parameters.contrib.ubi_center.basic_income.amount_by_age.brackets[i].amount.update(value=person_amount, period=f"year:2015:10")
        return parameters
    
    class spm_unit_is_in_spm_poverty(Variable):
        value_type = bool
        entity = SPMUnit
        label = "SPM unit in SPM poverty"
        definition_period = YEAR

        def formula(spm_unit, period, parameters):
            income = spm_unit("spm_unit_net_income", period) + add(spm_unit, period, ["basic_income"])
            poverty_threshold = spm_unit("spm_unit_spm_threshold", period)
            return income < poverty_threshold

    class spm_unit_is_in_deep_spm_poverty(Variable):
        value_type = bool
        entity = SPMUnit
        label = "SPM unit in deep SPM poverty"
        definition_period = YEAR

        def formula(spm_unit, period, parameters):
            income = spm_unit("spm_unit_net_income", period) + add(spm_unit, period, ["basic_income"])
            poverty_threshold = spm_unit("spm_unit_spm_threshold", period) / 2
            return income < poverty_threshold

    class ubi_reform(Reform):
        def apply(self):
            self.modify_parameters(set_ubi_parameter)
            self.update_variable(spm_unit_is_in_spm_poverty)
            self.update_variable(spm_unit_is_in_deep_spm_poverty)
    
    return ubi_reform
