# Libraries
# Built-ins

# Third-party developed
import pandas as pd

# In-project development
from pyscripts.helpers import add_method, time_execution


@time_execution
def obtain_prepped_data(trans_train, trans_test, ident_train, ident_test):
    return \
        pd.concat([
            trans_train.assign(sample="dev"),
            trans_test.assign(sample="val")
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
def subvalue_replacement(df, pat, repl, subset=None):

    if subset is None:
        anti_subset = df._get_numeric_data().columns
        subset = [x for x in df.columns if x not in anti_subset]

    return \
        pd.concat([
            df.drop(subset, axis=1),
            df.filter(subset, axis=1). \
                apply(lambda x: x.str.replace(pat=pat, repl=repl))
        ], axis=1). \
        filter(df.columns, axis=1)


@add_method(pd.DataFrame)
def der_dummies(df, subset, dummy_na=True):
    return pd.get_dummies(df, columns=subset, dummy_na=dummy_na)


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
def fill_na_with_mean(df, subset=None):

    if subset is None:
        subset = df._get_numeric_data().columns
        # or alternatively
        # df.select_dtypes(include=[np.number])

    rdf = pd.concat([
        df.drop(subset, axis=1),
        df.filter(subset, axis=1).apply(lambda x: x.fillna(x.mean()), axis=0)
    ], axis=1). \
    filter(df.columns, axis=1)

    return rdf
