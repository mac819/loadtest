import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression


if __name__=="__main__":
    iris_df = pd.read_csv("data/iris.data", header=None)
    columns = ['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm', 'Species']
    iris_df.columns = columns

    x = iris_df.iloc[:, :4]
    y = iris_df.iloc[:, 4]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1)
    print(x_train.shape, x_test.shape, y_train.shape, y_test.shape)

    model = LogisticRegression()
    model.fit(x_train, y_train)

    with open("model/iris_model.pkl", "wb") as f:
        pickle.dump(model, f)