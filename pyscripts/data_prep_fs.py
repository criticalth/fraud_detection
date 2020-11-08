# Libraries
# Built-ins

# Third-party developed
import pandas as pd

# In-project development
from pyscripts.helpers import add_method, time_execution


@time_execution
def obtain_prepped_data(trans_train, trans_test, ident_train, ident_test):
    """ A function to outline and perform quick and dirty data prep for all data
        for preliminary model development validation and testing.

    :param trans_train: pandas.DataFrame, transactional train data.
    :param trans_test: pandas.DataFrame, transactional test data.
    :param ident_train: pandas.DataFrame, identity train data.
    :param ident_test: pandas.DataFrame, identity test data.
    :return: pandas.DataFrame, containing prepped for modeling purposes columns.
    """

    # data prep devised in 5 steps:
    # 1) concatenate train and test transactional data as main data source.
    # 2) merge concatenated identity data to transactional data from # 1).
    # 3) replace .0 to _0 in all string variables for better naming convention.
    # 4) derive dummies for pre-specified list of categorical variables.
    # 5) for all other variables - simply impute with their mean.
    return \
        pd.concat([
            trans_train.assign(sample="train"),
            trans_test.assign(sample="test")
        ]). \
        merge(
            pd.concat([
                ident_train,
                ident_test.rename(lambda x: x.replace("-", "_"), axis=1)
            ]),
            on='TransactionID',
            how="left"
        ). \
        subvalue_replacement(".0", "_0"). \
        der_dummies(subset=get_iden_catvar_names() + get_tran_catvar_names()). \
        fill_na_with_mean()


@add_method(pd.DataFrame)
def subvalue_replacement(data, pat, repl, subset=None):
    """ A function that replaces argument `pat` with argument `repl` in all str
        columns in argument `df` if subset is None, otherwise the replacement
        happens in variables specified in the `subset` argument.

    :param data: pd.DataFrame, for which the replacement is performed.
    :param pat: str, to be replaced.
    :param repl: str, to replace with.
    :param subset: list, of variable names for which the replacement to be made.
    :return: pd.DataFrame with the description functionality completed.
    """

    # if subset is None replace all character variables
    # else replace according to argument `subset` value
    if subset is None:
        anti_subset = data._get_numeric_data().columns
        subset = [x for x in data.columns if x not in anti_subset]

    # concatenate replaced and non-replaced columns
    # apply original column order and return the result
    return \
        pd.concat([
            data.drop(subset, axis=1),
            data.filter(subset, axis=1). \
                apply(lambda x: x.str.replace(pat=pat, repl=repl))
        ], axis=1). \
        filter(data.columns, axis=1)


@add_method(pd.DataFrame)
def der_dummies(data, subset, dummy_na=True):
    """ Convert categorical variable into dummy/indicator variables.

    :param data: array-like, Series, or DataFrame, of which to get dummy columns.
    :param subset: list-like, column names in the DataFrame to be encoded.
    :param dummy_na: bool, default True, add a column to indicate NaNs.
    :return: pd.DataFrame, Dummy-coded data.
    """
    return pd.get_dummies(data, columns=subset, dummy_na=dummy_na)


def get_iden_catvar_names():
    """ A function that returns categorical variable names for identity data.
        :return: list
    """
    cts = ["DeviceType", "DeviceInfo"] + ["id_" + str(i) for i in range(12, 39)]
    return cts


def get_tran_catvar_names():
    """ A function that returns categorical variable names for transaction data.
        :return: list
    """
    cts = ["ProductCD", "P_emaildomain", "R_emaildomain", "addr1", "addr2"] + \
          ["card" + str(i) for i in range(1, 7)] + \
          ["M" + str(i) for i in range(1, 10)]
    return cts


@add_method(pd.DataFrame)
def fill_na_with_mean(data, subset=None):
    """ A function to impute missing values with corresponding column mean.

    :param df: pd.DataFrame, data to be imputed.
    :param subset: list, default None, of varaible names to be imputed
    :return: pd.DataFrame, imputed data.
    """

    # if subset is None impute all numeric data
    # else use the argument value
    if subset is None:
        subset = data._get_numeric_data().columns
        # or alternatively
        # df.select_dtypes(include=[np.number])

    # concatenate imputed and non-imputed data
    # apply original column order and return the result
    rdf = pd.concat([
        data.drop(subset, axis=1),
        data.filter(subset, axis=1).apply(lambda x: x.fillna(x.mean()), axis=0)
    ], axis=1). \
    filter(data.columns, axis=1)

    return rdf
