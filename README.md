# Integrated Model
Code for an integrated reservoir-production model

## Oil Properties

* Defined two correlations for the bubble pressure:
  * The original Standing correlation.
  * A modified formula that is an inversion of the Rs formula.
* Option 'auto' in some of the correlation functions will try to estimate any missing values. The user must manually recalculate any values if changes were made to the variables that are arguments to the correlation.

## IPR

* User supplies productivity index and drainage area mean pressure.
  * There's the option to estimate PI from reservoir properties.

## Flow elements

* Defined 3 classes that solve (p,T,Q) for a linear element with oil only (no free gas).
* The main class is **CompositeFlowElement**, that holds a collection of linear elements.
* This class also has an IPR object, so that the user can calculate the operational point. Used the secant method to solve this problem.

## To-Do

* Reorganize PVT calculations to check correlation used by each variable and update automatically if needed.