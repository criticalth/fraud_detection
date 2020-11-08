# Libraries
# Build-ins
import time

# Third-party developed
import pandas as pd

# In-project development
from pyscripts.dtype_helpers import get_identity_dtypes, get_transaction_dtypes


def import_train_identity(file="data/train_identity.csv"):
    """ A function to import train identity data
    :param file: full file path
    :return: pandas.DataFrame """
    return pd.read_csv(file, dtype=get_identity_dtypes())


def import_train_transaction(file="data/train_transaction.csv"):
    """ A function to import train transaction data
    :param file: full file path
    :return: pandas.DataFrame """
    return pd.read_csv(file, dtype=get_transaction_dtypes())


def import_test_identity(file="data/test_identity.csv"):
    """ A function to import test identity data
    :param file: full file path
    :return: pandas.DataFrame """
    return pd.read_csv(file, dtype=get_identity_dtypes())


def import_test_transaction(file="data/test_transaction.csv"):
    """ A function to import test transaction data
    :param file: full file path
    :return: pandas.DataFrame """
    return pd.read_csv(file, dtype=get_transaction_dtypes())
