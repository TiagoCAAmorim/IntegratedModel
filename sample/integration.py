import reservoir
import pvt
import flow
import topside

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

    def initialize(self):
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

        self.water_pump.set_qw(self.reservoir.get_qwi())

    def advance_simulation(self, dt):
        self.flow_prod.set_dt(dt)
        self.flow_prod.solve_operation_point(self._last_pwf)
        self._last_pwf = self.flow_prod.get_pwf()
        self.reservoir.run_simulation(dt, True)
        t = self.reservoir.get_t()[-1]
        qo = self.reservoir.get_well_qo()[-1]
        qw = self.reservoir.get_well_qw()[-1]
        phead = self.flow_prod.get_p_out()[-1]
        pwf_flow = self.flow_prod.get_p_in()[0]
        self._log(f' t = {t:0.2f} days, Pwf_res = {self._last_pwf:0.2f} bar, Qo = {qo:0.2f} m3/d, Qw = {qw:0.2f} m3/d, , Pwf_flow = {pwf_flow:0.2f} bar, Phead = {phead:0.2f} bar')

    def solve_water_injection(self):
        pwf_inj = self.reservoir.get_pr_cell(0,0)[-1]
        self.flow_inj.set_p_out(pwf_inj)
        self.flow_inj.solve_in_flow()
        phead = self.flow_inj.get_p_in()[0]
        power_pump = self.water_pump.get_power_from_delta_p(phead - 1.)
        self._log(f' Pwf_injw = {pwf_inj:0.2f}, Phead_injw = {phead:0.2f} bar, Power = {power_pump:0.2f} MW')

    def solve_gas_balance(self):
        pass

    def solve_emissions(self):
        pass

    def run_simulation(self, dt):
        self.initialize()
        t = 0.
        while t < self.reservoir.get_t_end():
            dti = min(dt, self.reservoir.get_t_end() - t)
            self.advance_simulation(dti)
            self.solve_water_injection()
            self.solve_gas_balance()
            self.solve_emissions()
            t += dti