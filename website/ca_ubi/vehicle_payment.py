from openfisca_us.model_api import *
from openfisca_us.tools.baseline_variables import baseline_variables

def set_parameters(parameters):
    parameters.states.ca.per_vehicle_payment.amount.CA.update(value=400, period="year:2022:1")
    parameters.states.ca.per_vehicle_payment.max_vehicles.CA.update(value=2, period="year:2022:1")
    return parameters

class spm_unit_net_income(baseline_variables["spm_unit_net_income"]):
    def formula(spm_unit, period, parameters):
        original_net_income = baseline_variables["spm_unit_net_income"].formula(spm_unit, period, parameters)
        vehicle_payment = add(spm_unit, period, ["per_vehicle_payment"])
        return original_net_income + vehicle_payment

class vehicle_payment(Reform):
    def apply(self):
        self.update_variable(spm_unit_net_income)
        self.modify_parameters(set_parameters)