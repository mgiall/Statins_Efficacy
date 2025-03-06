import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multitest import multipletests
import pandas as pd
import numpy as np
import os

def linear_regression_results(dependent_features, independent_features,
                              formula_string, df, test_df, metabolite_anns=False):
    """
    Get a single association (x --> y) for a specific combination of features. 
    --------
    Input: (1) list of dependent features, (2) list of independent
    features, (3) `str` specifying the linear regression formula 
    to use, (4) df of data to use for fitting the model, and (5) 
    df of data to test fit. 
    --------
    metabolite_anns=False by default and can be made `True` if 
    the user wishes to add metabolite annotations for those regressions.
    --------
    Output: df containing summary statistics for our association.
    The df will specify formula, dependent, and independent features
    used. P-values FDR-corrected using Benjamini Hochberg.
    """
    all_results = [] # Initialize an empty list to store the results
    
    # Iterate through all combinations of dependent and independent features
    for dependent_feature in dependent_features:
        for independent_feature in independent_features:
            # Define the formula using the provided dependent and independent variables
            formula = formula_string.format(dependent_feature = dependent_feature,
                                            independent_feature = independent_feature)
            fitted = ols(formula, data=df).fit()
            # Compute R2 for the fitted model on the holdout test df
            # Get the residuals and calculate their sum of squares
            y_test = test_df[dependent_feature]
            predictions = fitted.predict(test_df)
            residuals = y_test - predictions
            RSS = np.sum(residuals**2)
            # Calculate the total sum of squares
            y_mean = np.mean(y_test)
            TSS = np.sum((y_test - y_mean)**2)
            # Calculate R-squared
            r2_test = 1 - (RSS / TSS)
            # Create a Series with the results
            result_series = pd.Series({
                "dependent_feature": dependent_feature,
                "independent_feature": independent_feature,
                "beta": fitted.params,
                "t_statistic": fitted.tvalues[independent_feature],
                "p": fitted.pvalues[independent_feature],
                "n": fitted.nobs,
                "r2_train": fitted.rsquared,
                "r2_test": r2_test,
                "formula": formula
                })
            all_results.append(result_series)
            """
            # Code to make residual plots
            # modify figure size
            fig = plt.figure(figsize=(14, 8))
            # creating regression plots
            fig = sm.graphics.plot_regress_exog(fitted, independent_feature, fig=fig)
            fig.show()
            """
    # Turn the all_results list into a pandas df
    tests = pd.DataFrame(all_results)
    # Perform multiple testing correction
    tests["q"] = multipletests(tests["p"], method="fdr_bh")[1]
    return tests