# -*- coding: utf-8 -*-

# Author: Daniel Yang <daniel.yj.yang@gmail.com>
#
# License: BSD 3 clause

from sklearn.neighbors import KNeighborsClassifier

from ..stats import distance

import numpy as np
import pandas as pd

from collections import Counter

class kNN_classifier_from_scratch(object):
    def __init__(self, n_neighbors=5, distance_func=distance(p=2).Minkowski):
        self.X_train = None
        self.y_train = None
        self.n_neighbors = n_neighbors
        self.distance_func = distance_func

    def fit(self, X_train, y_train):
        if type(X_train) in [pd.DataFrame, pd.Series]:
            X_train = X_train.to_numpy()
        if type(y_train) in [pd.DataFrame, pd.Series]:
            y_train = y_train.to_numpy()
        self.X_train = X_train
        self.y_train = y_train
        return self

    def predict(self, X_test):
        y_pred = []
        for this_x_test_sample in X_test:
            train_list = [[self.distance_func(self.X_train[train_index,:], this_x_test_sample), self.y_train[train_index]] for train_index in range(self.X_train.shape[0])]
            train_list.sort() # sorted by the first element
            y_pred_candidates = [data[1] for data in train_list[:self.n_neighbors]]
            y_pred_mode = Counter(y_pred_candidates).most_common(1)
            y_pred.append(y_pred_mode[0][0])
        return y_pred


def kNN_classifier(*args, **kwargs):
    """
    """
    return KNeighborsClassifier(*args, **kwargs)


def _kNN_demo_Social_Network_Ads():
    from ..datasets import public_dataset
    data = public_dataset(name='Social_Network_Ads')
    X = data[['Age', 'EstimatedSalary']].to_numpy()
    y = data['Purchased'].to_numpy()
    y_classes = ['not_purchased (y=0)', 'purchased (y=1)']

    from sklearn.model_selection import train_test_split, GridSearchCV
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=123)

    from sklearn.preprocessing import StandardScaler
    # scaler = StandardScaler()  # removing the mean and scaling to unit variance
    #X_train = scaler.fit_transform(X_train)
    #X_test = scaler.transform(X_test)

    # create pipeline
    from sklearn.pipeline import Pipeline
    pipeline = Pipeline(steps=[('scaler',
                                StandardScaler(with_mean=True, with_std=True)),
                               ('classifier',
                                kNN_classifier(n_neighbors=5, weights='uniform', p=2, metric='minkowski')),
                               ])

    # pipeline parameters to tune
    hyperparameters = {
        'scaler__with_mean': [True],
        'scaler__with_std': [True],
        'classifier__n_neighbors': range(1, 20),
        'classifier__weights': ['uniform', 'distance'],
        'classifier__p': [2**0, 2**0.25, 2**0.5, 2**0.75, 2**1, 2**1.25, 2**1.5, 2**1.75, 2**2, 2**2.25, 2**2.5, 2**2.75, 2**3],
        'classifier__metric': ['minkowski'],
    }
    grid = GridSearchCV(
        pipeline,
        hyperparameters,  # parameters to tune via cross validation
        refit=True,       # fit using all data, on the best detected classifier
        n_jobs=-1,
        scoring='accuracy',
        cv=5,
    )
    classifier_grid = grid.fit(X_train, y_train)
    k = classifier_grid.best_params_['classifier__n_neighbors']
    print(
        f"Using a grid search and a kNN classifier, the best hyperparameters were found as following:\n"
        f"Step1: scaler: StandardScaler(with_mean={repr(classifier_grid.best_params_['scaler__with_mean'])}, with_std={repr(classifier_grid.best_params_['scaler__with_std'])});\n"
        f"Step2: classifier: kNN_classifier(n_neighbors={repr(k)}, weights={repr(classifier_grid.best_params_['classifier__weights'])}, p={classifier_grid.best_params_['classifier__p']:.2f}, metric={repr(classifier_grid.best_params_['classifier__metric'])}).\n")

    y_pred = classifier_grid.predict(X_test)
    y_pred_score = classifier_grid.predict_proba(X_test)

    from ..model_evaluation import plot_confusion_matrix, plot_ROC_and_PR_curves, visualize_classifier_decision_boundary_with_two_features
    plot_confusion_matrix(y_true=y_test, y_pred=y_pred, y_classes=y_classes, model_name=f"kNN (k={k})")
    plot_ROC_and_PR_curves(fitted_model=classifier_grid, X=X_test, y_true=y_test, y_pred_score=y_pred_score[:, 1], y_pos_label=1, model_name=f"kNN (k={k})")

    visualize_classifier_decision_boundary_with_two_features(classifier_grid, X_train, y_train, y_classes, title=f"k-Nearest Neighbors (k={k}) / training set", X1_lab='Age', X2_lab='Estimated Salary')
    visualize_classifier_decision_boundary_with_two_features(classifier_grid, X_test,  y_test,  y_classes, title=f"k-Nearest Neighbors (k={k}) / testing set",  X1_lab='Age', X2_lab='Estimated Salary')


def _kNN_demo_iris():
    from ..datasets import public_dataset
    data = public_dataset(name='iris')
    y_classes = ['setosa', 'versicolor', 'virginica']
    X = data[['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)']]
    y = data['target']

    print(
        f"---------------------------------------------------------------------------------------------------------------------\n"
        f"This demo uses a public dataset of Fisher's Iris, which has a total of {len(data)} samples from three species of Iris ('setosa', 'versicolor', 'virginica').\n"
        f"The goal is to use 'the length and the width of the sepals and petals, in centimeters', to predict which species of Iris the sample belongs to.\n")

    from sklearn.model_selection import train_test_split, GridSearchCV
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=123)

    from sklearn.preprocessing import StandardScaler
    # scaler = StandardScaler()  # removing the mean and scaling to unit variance
    #X_train = scaler.fit_transform(X_train)
    #X_test = scaler.transform(X_test)

    # create pipeline
    from sklearn.pipeline import Pipeline
    pipeline = Pipeline(steps=[('scaler',
                                StandardScaler(with_mean=True, with_std=True)),
                               ('classifier',
                                kNN_classifier(n_neighbors=5, weights='uniform', p=2, metric='minkowski')),
                               ])

    # pipeline parameters to tune
    hyperparameters = {
        'scaler__with_mean': [True, False],
        'scaler__with_std': [True, False],
        'classifier__n_neighbors': range(1, 20),
        'classifier__weights': ['uniform', 'distance'],
        'classifier__p': [2**0, 2**0.25, 2**0.5, 2**0.75, 2**1, 2**1.25, 2**1.5, 2**1.75, 2**2, 2**2.25, 2**2.5, 2**2.75, 2**3],
        'classifier__metric': ['minkowski'],
    }
    grid = GridSearchCV(
        pipeline,
        hyperparameters,  # parameters to tune via cross validation
        refit=True,       # fit using all data, on the best detected classifier
        n_jobs=-1,
        scoring='accuracy',
        cv=5,
    )
    classifier_grid = grid.fit(X_train, y_train)
    k = classifier_grid.best_params_['classifier__n_neighbors']
    print(
        f"Using a grid search and a kNN classifier, the best hyperparameters were found as following:\n"
        f"Step1: scaler: StandardScaler(with_mean={repr(classifier_grid.best_params_['scaler__with_mean'])}, with_std={repr(classifier_grid.best_params_['scaler__with_std'])});\n"
        f"Step2: classifier: kNN_classifier(n_neighbors={repr(k)}, weights={repr(classifier_grid.best_params_['classifier__weights'])}, p={classifier_grid.best_params_['classifier__p']:.2f}, metric={repr(classifier_grid.best_params_['classifier__metric'])}).\n")

    y_pred = classifier_grid.predict(X_test)
    y_pred_score = classifier_grid.predict_proba(X_test)

    from ..model_evaluation import plot_confusion_matrix, plot_ROC_and_PR_curves, visualize_classifier_decision_boundary_with_two_features
    plot_confusion_matrix(y_true=y_test, y_pred=y_pred, y_classes=y_classes, figsize=(7,7), model_name=f"kNN (k={k})")


def _kNN_demo_iris_from_scratch():
    from ..datasets import public_dataset
    data = public_dataset(name='iris')
    y_classes = ['setosa', 'versicolor', 'virginica']
    X = data[['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)']]
    y = data['target']
    n_neighbors = 12

    print(
        f"---------------------------------------------------------------------------------------------------------------------\n"
        f"This demo uses a public dataset of Fisher's Iris, which has a total of {len(data)} samples from three species of Iris ('setosa', 'versicolor', 'virginica').\n"
        f"The goal is to use 'the length and the width of the sepals and petals, in centimeters', to predict which species of Iris the sample belongs to.\n")

    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=123)

    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    model = kNN_classifier_from_scratch(n_neighbors=n_neighbors)
    model.fit(scaler.fit_transform(X_train), y_train)
    y_pred = model.predict(scaler.transform(X_test))
    from ..model_evaluation import plot_confusion_matrix
    plot_confusion_matrix(y_true=y_test, y_pred=y_pred, y_classes=y_classes, figsize=(7,7), model_name=f"kNN (k={n_neighbors})")


def demo(dataset="Social_Network_Ads"):
    """

    This function provides a demo of selected functions in this module.

    Required arguments:
        dataset: A string. Possible values: "Social_Network_Ads", "iris"

    """
    if dataset == "Social_Network_Ads":
        _kNN_demo_Social_Network_Ads()
    elif dataset == "iris":
        _kNN_demo_iris()
    else:
        raise TypeError(f"dataset [{dataset}] is not defined")


def demo_from_scratch(dataset="iris"):
    """

    This function provides a demo of selected functions in this module.

    Required arguments:
        dataset: A string. Possible values: "iris"

    """
    if dataset == "iris":
        _kNN_demo_iris_from_scratch()
    else:
        raise TypeError(f"dataset [{dataset}] is not defined")
