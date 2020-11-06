# Libraries
# Build-ins

# Third-party developed
from sklearn.model_selection import train_test_split

# In-project development


def select_subsample(data, subsample):
    return data.loc[lambda x: x["sample"]==subsample].drop(["sample"], axis=1)


def test_train_dev_val_split(prepped_df):

    train = select_subsample(prepped_df, "train")
    test = select_subsample(prepped_df, "test")

    dev, val = train_test_split(train, test_size=0.2, random_state=7)

    return dev, val, test
