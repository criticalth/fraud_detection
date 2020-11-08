# Libraries
# Built-ins

# Third-party developed
import pandas as pd

# In-project development
from pyscripts.helpers import add_method


@add_method(pd.DataFrame)
def pivoting(self, index=None, columns=None, values=None):
    """ Custom pivot of dataframe with removing multi index names.

    :param self: data.
    :param index: str or object or a list of str, optional.
    :param columns: str or object or a list of str.
    :param values: str, object or a list of the previous, optional.
    :return: pd.DataFrame, pivoted, columns renamed."""
    res = self. \
        pivot(index=index, columns=columns, values=values). \
        reset_index(drop=True)

    res.columns = [x[0] + "_" + x[1] for x in res.columns]

    return res
