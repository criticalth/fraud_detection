# Libraries
# Built-ins
from joblib import load, dump

# Third-party developed
from sklearn.linear_model import LinearRegression

# In-project development
from pyscripts.helpers import import_export, time_execution


@time_execution
@import_export("output/models/qd_lm.joblib", import_func=load, export_func=dump)
def fraud_lm(dev_predictors, dev_outcome):
    tes_lm = LinearRegression()
    tes_lm.fit(dev_predictors, dev_outcome)
    return tes_lm
