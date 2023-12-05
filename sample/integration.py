import reservoir
import pvt
import flow
import topside
from tqdm import tqdm

class Integration:

    def __init__(self, debug=False):
        self.pvt = pvt.PVT()
        self.reservoir = reservoir.Simple2D_OW()
        self.flow_prod = flow.CompositeFlowElement()
        self.flow_inj = flow.CompositeFlowElement()
        self.gas_compressor = topside.GasCompressor()
        self.water_pump = topside.WaterPump()
        self.separator = topside.Separator()
        self.emission = topside.CO2_Emission()

        self._reservoir_t = None
        self._reservoir_p = None

        self._well_head_t = None
        self._well_head_p = None

        self._gas_loss = 0.

        self._last_pwf = None
        self._dt = None

        self._t = None
        self._qo = None
        self._qw = None
        self._qg = None
        self._qwi = None
        self._pwf_prod = None
        self._pwf_inj = None
        self._pwh_prod = None
        self._pwh_inj = None
        self._pump_power = None
        self._esp_power = None
        self._export_power = None
        self._qg_flare = None
        self._qg_fuel = None
        self._qg_export = None
        self._total_power = None
        self._gas_emission = None
        self._diesel_emission = None
        self._total_emission = None
        self._cumulative_emission = None
        self._emission_boe = None

        self._file_name = None
        self._file = None
        self._debug = debug

    def _log(self, message):
        if self._debug:
            print(message)

    def set_reservoir_t(self, value):
        self._reservoir_t = value
    def set_reservoir_p(self, value):
        self._reservoir_p = value
    def set_well_head_t(self, value):
        self._well_head_t = value
    def set_well_head_p(self, value):
        self._well_head_p = value
    def set_gas_loss(self, value):
        self._gas_loss = value
    def set_file_name(self, value):
        self._file_name = value

    def initialize(self):
        self._file = open(self._file_name, 'w')
        self.print_heading()


        self.pvt.set_t(self._reservoir_t)
        self.pvt.set_p(self._reservoir_p)
        self.pvt.calculate_bo_Standing(auto=True)
        self.pvt.calculate_uo_Standing(auto=True)

        self.reservoir.set_bo(self.pvt.get_bo())
        self.reservoir.set_uo(self.pvt.get_uo())
        self.reservoir.set_bw(1.)
        self.reservoir.set_uw(1.)
        self.reservoir.set_p_init(self._reservoir_p)

        self._last_pwf = 0.8 * self._reservoir_p

        self.flow_prod.pvt = self.pvt.copy()
        self.flow_prod.set_p_out(self._well_head_p)
        self.flow_prod.set_t_out(self._well_head_t)
        self.flow_prod.set_reservoir(self.reservoir)
        self.flow_prod.update_pvt()

        self.flow_inj.pvt = self.pvt.copy()
        self.flow_inj.pvt.set_wfr(1.)
        self.flow_inj.set_q_std(self.reservoir.get_qwi())
        self.flow_inj.set_t_out(self._reservoir_t)
        self.flow_inj.update_pvt()

        self.gas_compressor.pvt = self.pvt.copy()
        self.gas_compressor.pvt.set_t(self._well_head_t)
        self.gas_compressor.pvt.set_p(self._well_head_p)

        self._t = [0.]
        self._qo = [0.]
        self._qw = [0.]
        self._qg = [0.]
        self._qwi = [0.]
        self._pwf_prod = [0.]
        self._pwf_inj = [0.]
        self._pwh_prod = [0.]
        self._pwh_inj = [0.]
        self._pump_power = [0.]
        self._esp_power = [0.]
        self._export_power = [0.]
        self._qg_flare = [0.]
        self._qg_fuel = [0.]
        self._qg_export = [0.]
        self._total_power = [0.]
        self._gas_emission = [0.]
        self._diesel_emission = [0.]
        self._total_emission = [0.]
        self._cumulative_emission = [0.]
        self._emission_boe = [0.]

    def advance_simulation(self, dt):
        self.flow_prod.set_dt(dt)
        self.flow_prod.solve_operation_point(self._last_pwf)
        self._last_pwf = self.flow_prod.get_pwf()

        self.reservoir.run_simulation(dt, True)
        while not self.reservoir.check_convergence(dt):
            dt = max(dt / 2., self.reservoir.get_min_dt())
            print(f" {self.reservoir.get_t()[-1]:10.2f} days: time-step cut. New dt = {dt:10.5f} days")
            self.reservoir.run_simulation(dt, True)
        self._t = self.reservoir.get_t()
        self._qo = self.reservoir.get_well_qo()
        self._qw = self.reservoir.get_well_qw()
        self._qwi.append(self.reservoir.get_qwi())
        self._pwf_prod.append(self.flow_prod.get_pwf())
        self._pwf_inj.append(self.reservoir.get_inj_pwf())
        self._pwh_prod.append(self.flow_prod.get_p_out()[-1])
        # pwf_flow = self.flow_prod.get_p_in()[0]
        # self._log(f' t = {self._t[-1]:0.2f} days, Pwf_prod = {self._pwf_prod[-1]:0.2f} bar, Qo = {self._qo[-1]:0.2f} m3/d, Qw = {self._qw[-1]:0.2f} m3/d, , Pwf_flow = {pwf_flow:0.2f} bar, Phead = {self._pwh_prod[-1]:0.2f} bar')
        dt = min(dt * 1.2, self.reservoir.get_max_dt())
        print(f" {self.reservoir.get_t()[-1]:10.2f} days: time-step advance. New dt = {dt:10.5f} days")
        return dt

     def run_simulation(self, dt):
        self.initialize()
        t = 0.
        dti = dt

        progress_bar = tqdm(total=100, desc="Progress", bar_format="{percentage:3.0f}% {elapsed} {bar}")
        while t < self.reservoir.get_t_end():
            dti = min(dti, self.reservoir.get_t_end() - t)
            dti = self.advance_simulation(dti)
            self.solve_water_injection()
            self.solve_esp()
            self.solve_gas_balance()
            self.solve_emissions()
            self.print_results()
            t += dti
            percentage_completion = min(0.999, t / self.reservoir.get_t_end()) * 100
            progress_bar.update(percentage_completion - progress_bar.n)
        progress_bar.close()
        self._file.close()
        print("End of simulation.")

    def solve_water_injection(self):
        self.water_pump.set_qw(self._qwi[-1])
        self.flow_inj.set_p_out(self._pwf_inj[-1])
        self.flow_inj.solve_in_flow()
        self._pwh_inj = [self.flow_inj.get_p_in()[0]]
        self._pump_power.append(self.water_pump.get_power_from_delta_p(self._pwh_inj[-1] - 1.))
        # self._log(f' Pwf_injw = {self._pwf_inj[-1]:0.2f}, Phead_injw = {self._pwh_inj[-1]:0.2f} bar, Power = {self._pump_power[-1]:0.2f} MW')

    def solve_esp(self):
        self._esp_power.append(self.flow_prod.get_esp_power())

    def solve_gas_balance(self):
        self._qg.append(self._qo[-1] * self.pvt.get_rs())
        self._qg_flare.append(self._qg[-1] * self._gas_loss)

        qg_export = self._qg[-1] - self._qg_flare[-1]
        self.gas_compressor.set_qg(qg_export)
        compressor_power = self.gas_compressor.get_power()
        power = self._pump_power[-1] + self._esp_power[-1] + compressor_power
        qg_fuel = self.emission.generator.get_fuel(power)
        qg_export = self._qg[-1] - self._qg_flare[-1] - qg_fuel

        if qg_export > 0:
            self.gas_compressor.set_qg(qg_export)
            compressor_power = self.gas_compressor.get_power()
            power = self._pump_power[-1] + self._esp_power[-1] + compressor_power
            qg_fuel = self.emission.generator.get_fuel(power)
            qg_export = self._qg[-1] - self._qg_flare[-1] - qg_fuel
        else:
            qg_export = 0.
            self.gas_compressor.set_qg(qg_export)
            compressor_power = 0.
            power = self._pump_power[-1] + self._esp_power[-1]
            qg_fuel = self.emission.generator.get_fuel(power)

            if qg_fuel < (self._qg[-1] - self._qg_flare[-1]):
                self._qg_flare[-1] = self._qg[-1] - qg_fuel
            else:
                qg_fuel = self._qg[-1] - self._qg_flare[-1]
                power_gas = self.emission.generator.get_power(qg_fuel)
                self.emission.set_diesel_power(power - power_gas)

        self._qg_fuel.append(qg_fuel)
        self._export_power.append(compressor_power)
        self._qg_export.append(qg_export)
        self._total_power.append(power)

    def solve_emissions(self):
        gas_power_demand = self._total_power[-1] - self.emission.get_diesel_power()
        self._gas_emission.append(self.emission.get_gas_emission(gas_power_demand))
        self._diesel_emission.append(self.emission.get_diesel_emission())
        self._total_emission.append(self._gas_emission[-1] + self._diesel_emission[-1])
        self._cumulative_emission.append(self._cumulative_emission[-1] + self._total_emission[-1] * (self._t[-1] - self._t[-2]))
        self._emission_boe.append(self._total_emission[-1] / (self._qo[-1] + self._qg[-1]/1000.))

    def print_heading(self):
        s = f'{"Time[d]":25s}'
        s += f'\t{"TimeStep[d]":25s}'
        s += f'\t{"Qo[m3/d]":25s}'
        s += f'\t{"Qw[m3/d]":25s}'
        s += f'\t{"Qg[m3/d]":25s}'
        s += f'\t{"Qwi[m3/d]":25s}'
        s += f'\t{"PwfProd[bar]":25s}'
        s += f'\t{"PwfInj[bar]":25s}'
        s += f'\t{"PwhProd[bar]":25s}'
        s += f'\t{"PwhInj[bar]":25s}'
        s += f'\t{"QgFlare[m3/d]":25s}'
        s += f'\t{"QgFuel[m3/d]":25s}'
        s += f'\t{"QgExp[m3/d]":25s}'
        s += f'\t{"Pump[MW]":25s}'
        s += f'\t{"ESP[MW]":25s}'
        s += f'\t{"ExpCompr[MW]":25s}'
        s += f'\t{"TotalPower[MW]":25s}'
        s += f'\t{"GasEmission[tonCO2/d]":25s}'
        s += f'\t{"DieselEmission[tonCO2/d]":25s}'
        s += f'\t{"TotalEmission[tonCO2/d]":25s}'
        s += f'\t{"CumEmission[tonCO2]":25s}'
        s += f'\t{"RelEmission[kgCO2/boe]":25s}'
        self._file.write(s + '\n')

    def print_results(self):
        s  =   f'{self._t[-1]:25.2f}'
        s += f'\t{self._t[-1]-self._t[-2]:25.2f}'
        s += f'\t{self._qo[-1]:25.2f}'
        s += f'\t{self._qw[-1]:25.2f}'
        s += f'\t{self._qg[-1]:25.2f}'
        s += f'\t{self._qwi[-1]:25.2f}'
        s += f'\t{self._pwf_prod[-1]:25.2f}'
        s += f'\t{self._pwf_inj[-1]:25.2f}'
        s += f'\t{self._pwh_prod[-1]:25.2f}'
        s += f'\t{self._pwh_inj[-1]:25.2f}'
        s += f'\t{self._qg_flare[-1]:25.2f}'
        s += f'\t{self._qg_fuel[-1]:25.2f}'
        s += f'\t{self._qg_export[-1]:25.2f}'
        s += f'\t{self._pump_power[-1]:25.2f}'
        s += f'\t{self._esp_power[-1]:25.2f}'
        s += f'\t{self._export_power[-1]:25.2f}'
        s += f'\t{self._total_power[-1]:25.2f}'
        s += f'\t{self._gas_emission[-1]/1000.:25.2f}'
        s += f'\t{self._diesel_emission[-1]/1000.:25.2f}'
        s += f'\t{self._total_emission[-1]/1000.:25.2f}'
        s += f'\t{self._cumulative_emission[-1]/1000.:25.2f}'
        s += f'\t{self._emission_boe[-1]:25.2f}'
        self._file.write(s + '\n')
