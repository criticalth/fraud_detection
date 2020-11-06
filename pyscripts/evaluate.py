# Libraries
# Built-ins

# Third-party developed
import pandas as pd
from sklearn.metrics import roc_auc_score as roc_auc
from sklearn.metrics import mean_squared_error as mse
from sklearn.metrics import log_loss as loss

# In-project development
import pyscripts.object_enrichment


class FraudEvaluator:

    def __init__(self, model):
        self.overall_perf = None
        self.grouped_perf = None
        self.model = model

    def calc_perf(self, y_dev, x_dev, y_val, x_val):
        """ Main method to calculate performance measures. Blueprint for project
            fraud model evaluation, ensuring comparability between models.

        :param y_dev: array-like, development target
        :param y_dev_hat: array-like, development target predictions
        :param y_val: array-like, validation target
        :param y_val_hat: array-like, validation target predictions
        :return: None """

        y_dev_hat = self.model.predict(x_dev)
        y_val_hat = self.model.predict(x_val)

        self.metric_perf = self.calc_metrics(y_dev, y_dev_hat, y_val, y_val_hat)
        self.binned_perf = self.calc_groups(y_dev, y_dev_hat, y_val, y_val_hat)

    def export(self):
        pass

    def calc_metrics(self, y_dev, y_dev_hat, y_val, y_val_hat):

        return \
            pd.DataFrame({
                "mse": [mse(y_dev, y_dev_hat), mse(y_val, y_val_hat)],
                "log_loss": [loss(y_dev, y_dev_hat), loss(y_val, y_val_hat)],
                "auc": [roc_auc(y_dev, y_dev_hat), roc_auc(y_val, y_val_hat)]
            }). \
            apply(lambda x: [round(y, 4) for y in x]). \
            assign(sample=["dev", "val"], index=["i", "i"]). \
            pivoting(index=["index"], columns=["sample"])

    def calc_groups(self, y_dev, y_dev_hat, y_val, y_val_hat):
        pass
