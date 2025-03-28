import pandas as pd
import unittest
from maxstat.regression import linear_regression_results

class TestDescribeDataframe(unittest.TestCase):

    def test_smoke(self):
        """Smoke test to check that function runs without error"""
        df = pd.read_csv('./data/biomarkers_microbes_cov.csv')
        try:
            formula_string = "{dependent_feature} ~ C(Gender) + Age + BMI + C(Nationality) +" \
            "C(Status) + Activity + Microbial_load + Statin*{independent_feature}"
            result = linear_regression_results(['HMG'], ['Ruminococcus.sp..CAG.177_CAG00760'],
                              formula_string, df, df, metabolite_anns=False)
        except Exception as e:
            self.fail(f"linear_regression_results raised an exception: {e}")

    def test_one_shot(self):
        """Test that output DataFrame contains expected columns"""
        df = pd.read_csv('./data/biomarkers_microbes_cov.csv')
        expected_cols = ["dependent_feature", "independent_feature",
                         "beta", "t_statistic", "p", "n", "r2_train",
                         "r2_test", "formula"]

        formula_string = "{dependent_feature} ~ C(Gender) + Age + BMI + C(Nationality) +" \
            "C(Status) + Activity + Microbial_load + Statin*{independent_feature}"

        associations = linear_regression_results(['HMG'], ['Ruminococcus.sp..CAG.177_CAG00760'],
                              formula_string, df, df, metabolite_anns=False)
        
        # Check if all expected columns exist in associations DataFrame
        self.assertTrue(set(expected_cols).issubset(set(associations.columns)),
                        "Not all expected columns are present in output DataFrame.")

    def test_edge(self):
        """Test that categorical independent variable raises an appropriate error"""
        df = pd.read_csv('./data/biomarkers_microbes_cov.csv')

        formula_string = "{dependent_feature} ~ C(Gender) + Age + BMI + C(Nationality) +" \
            "C(Status) + Activity + Microbial_load + Statin*{independent_feature}"
        
        with self.assertRaises(ValueError):
            linear_regression_results(['HMG'], ['C(Status)'],
                                      formula_string, df, df, metabolite_anns=False)

if __name__ == '__main__':
    unittest.main()
