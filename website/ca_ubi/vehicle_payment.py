from openfisca_us.model_api import *

class ca_vehicle_payment(Variable):
    value_type = float
    entity = SPMUnit
    definition_period = YEAR
    label = "Vehicle payment"
    
    def formula(spm_unit, period):
        spm_unit_fips = spm_unit("spm_unit_fips", period)
        in_ca = spm_unit_fips == 6
        person = spm_unit.members
        eligible_vehicles = min_(2, person("vehicles_owned", period))
        amount = eligible_vehicles * 400
        return spm_unit.sum(amount) * in_ca

class spm_unit_is_in_spm_poverty(Variable):
    value_type = bool
    entity = SPMUnit
    label = "SPM unit in SPM poverty"
    definition_period = YEAR

    def formula(spm_unit, period, parameters):
        income = spm_unit("spm_unit_net_income", period) + spm_unit("ca_vehicle_payment", period)
        poverty_threshold = spm_unit("spm_unit_spm_threshold", period)
        return income < poverty_threshold

class spm_unit_is_in_deep_spm_poverty(Variable):
    value_type = bool
    entity = SPMUnit
    label = "SPM unit in deep SPM poverty"
    definition_period = YEAR

    def formula(spm_unit, period, parameters):
        income = spm_unit("spm_unit_net_income", period) + spm_unit("ca_vehicle_payment", period)
        poverty_threshold = spm_unit("spm_unit_spm_threshold", period) / 2
        return income < poverty_threshold

class vehicle_subsidy(Reform):
    def apply(self):
        self.update_variable(spm_unit_is_in_spm_poverty)
        self.update_variable(spm_unit_is_in_deep_spm_poverty)
        self.add_variable(ca_vehicle_payment)