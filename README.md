# Integrated Model
Code for an integrated reservoir-production model

## Oil Properties

* Defined two correlations for the bubble pressure:
  * The original Standing correlation.
  * A modified formula that is an inversion of the Rs formula.

## General Comments

* Option 'auto' in some of the correlation functions will try to estimate any missing values. The user must manually recalculate any values if changes were made to the variables that are arguments to the correlation. 