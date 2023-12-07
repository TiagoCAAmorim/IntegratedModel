# Integrated Model
Code for an integrated reservoir-production model

`sample`: Modules in Python

`tests` Python scripts that test the modules

`docs`: Reports on the modules and tests (in Portuguese)

## Oil Properties

* Defined two correlations for the bubble pressure:
  * The original Standing correlation.
  * A modified formula that is an inversion of the Rs formula.
* Option 'auto' in some of the correlation functions will try to estimate any missing values. The user must manually recalculate any values if changes were made to the variables that are arguments to the correlation.
* Implements Roenningsen's correlation to estimate emulsion viscosity, and Arirachakaran's to estimate phase inversion.

## IPR

* User supplies productivity index and drainage area mean pressure.
  * There's the option to estimate PI from reservoir properties.

## Flow elements

* Defined 3 classes that solve (p,T,Q) for a linear element with oil and water only (no free gas).
* The main class is **CompositeFlowElement**, that holds a collection of linear elements.
* This class also has an IPR object, so that the user can calculate the operational point. Used the secant method to solve this problem.

## Simulation model

* Incompressible model. Only deals with oil and water.
* Uses Fixed Point method to solve non-linear equations.
* 2D model, with water injector (prescribed Qwi) in 1st cell and producer (prescribed Pwf) in last cell.

## Topside

* __Separator__: Calculates maximum gas rate for the separator.
* __GasCompressor__: Calculates power demand based on efficiency and pressure demand.
* __WaterPump__: Calculates power demand based on efficiency and head increase demand.
* __GasTurbine__: Implements an interpolator between fuel gas and power generation.
* __CO2Emission__: Calculates CO2 emissions based on power demand and turbine characteristics.

## Integration

* Solves a simple integrated model:
  * Solves producer Pwf based on simulation model and wellhead pressure.
  * Estimates water pump power demand based on injection pressures needed.
  * Makes a simple gas balance: production = export + flare + fuel (no gas injection).
  * Outputs CO2 emissions for the system.

## To-Do

* Reorganize PVT calculations to check correlation used by each variable and update automatically if needed.
* Deal with free gas in the vfp formulas and simulation model.
* Use Newton-Raphson to solve non-linear equations in simulation model.
* Deal with variable properties in simulation model: porosity, Bo and Uo.