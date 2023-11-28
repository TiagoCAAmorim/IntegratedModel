import os
from context import topside
import matplotlib.pyplot as plt

path = os.path.abspath(os.path.dirname(__file__))
def save_plot(plt, name):
    plt.savefig(path+'/plots/pvt/'+name+'.png')
    # plt.show()

def sep_test():
    sep = topside.Separator()
    sep.pvt.set_p(15.)
    sep.pvt.set_t(50.)
    sep.pvt.set_api(15.)
    sep.pvt.set_gor(20.)
    sep.pvt.set_dg(0.9)

    sep.set_ks(0.03)
    sep.set_d(0.75)

    qo_max, qg_max = sep.calculate_max_rates()

    print('2-phase separator')
    print(f'  Max oil rate = {qo_max} m3/d')
    print(f'  Max gas rate = {qg_max} m3/d')

def water_pump_test():
    pump = topside.WaterPump()
    pump.set_eff(0.65)
    pump.set_qw(350. * 24.)

    power = pump.get_power_from_head(2100.)

    print(f'Water pump power demand = {power} kW')

def gas_comp_test():
    comp = topside.GasCompressor()
    comp.set_eff(0.76)
    comp.set_qg(2e6)
    comp.set_k(1.4)

    comp.pvt.set_t(20.)
    comp.pvt.set_p(30.)
    comp.set_p_out(90.)
    comp.pvt.set_dg(0.876)

    power = comp.get_power()
    print(f'Gas compressor power demand = {power} kW')

def co2_emission_test():
    emission = topside.CO2_Emission()
    emission.set_mole_pc('co2', 0.8 )
    emission.set_mole_pc('ch4', 95.3)
    emission.set_mole_pc('c2h6', 1.7)
    emission.set_mole_pc('c3h8', 0.5)
    emission.set_mole_pc('c4h10', 0.1)
    emission.set_mole_pc('n2', 1.6)

    emission.calculate_relative_emission()
    print(f'CO2 Emission = {emission.get_relative_emission()} kg/m3')

    emission.turbine.set_rates([0, 1,  1e6, 2.0e6, 2.1e6, 2.2e6, 2.3e6, 2.4e6, 2.5e6, 2.6e6, 2.7e6, 2.8e6, 2.9e6, 3.0e6, 5.0e6])
    emission.turbine.set_power([0, 4.1, 4.1, 4.1, 4.1, 4.4, 4.8, 5.1, 5.4, 5.8, 6.1, 6.4, 6.8, 7.1, 14.2])

    print(f'Total emission = {emission.get_emission(5.) * 1e-3} ton-CO2')

if __name__ == "__main__":
    sep_test()
    water_pump_test()
    gas_comp_test()
    co2_emission_test()

    pass