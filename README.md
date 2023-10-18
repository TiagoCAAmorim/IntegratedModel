# Integrated Model
Code for an integrated reservoir-production model

## Oil Properties

* Defined two correlations for the bubble pressure:
  * The original Standing correlation.
  * A modified formula that is an inversion of the Rs formula.

## General Comments

* Option 'auto' in some of the correlation functions will try to estimate any missing values. The user must manually recalculate any values if changes were made to the variables that are arguments to the correlation. 

## To-Do

* Class that is a list of linear segments and calculates for the whole thing.
  * Plot everything together.
  * Check if p < p_bubble in calculations.
* Compare to IPR Pwf and try to find operational point (use Secant method?).
* Reorganize PVT calculations to check correlation used by each variable and update automatically if needed.