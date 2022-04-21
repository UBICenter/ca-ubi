from openfisca_us.model_api import *
from openfisca_us.tools.baseline_variables import baseline_variables


def create_ubi_reform(person_amount):
    def set_ubi_level(parameters):
        for i in range(3):
            parameters.contrib.ubi_center.basic_income.amount_by_age.brackets[
                i
            ].amount.update(value=person_amount, period="year:2022:1")
        return parameters

    class spm_unit_net_income(baseline_variables["spm_unit_net_income"]):
        def formula(spm_unit, period, parameters):
            original_net_income = baseline_variables[
                "spm_unit_net_income"
            ].formula(spm_unit, period, parameters)
            basic_income = add(spm_unit, period, ["basic_income"])
            return original_net_income + basic_income

    class ubi_reform(Reform):
        def apply(self):
            self.update_variable(spm_unit_net_income)
            self.modify_parameters(set_ubi_level)

    return ubi_reform
