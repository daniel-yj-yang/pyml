# -*- coding: utf-8 -*-

# Author: Daniel Yang <daniel.yj.yang@gmail.com>
#
# License: BSD 3 clause

# Some references:
# https://huggingface.co/docs/datasets/
# https://scikit-learn.org/stable/datasets/index.html#general-dataset-api

import io
from zipfile import ZipFile
import urllib.request
import csv

import pkgutil

import os
import numpy as np

def public_dataset(name=None):
    """
    name can be one of the following:

        - SMS_spam
        - Social_Network_Ads
        - Fashion_MNIST
        - nltk_data_path
        - scikit_learn_data_path

    Disclaimer:
        - The datasets are shared with the sole intention of providing the convenience to access public datasets and reproduce/compare results.
        - They are shared under a good-faith understanding that they are widely viewed and accepted as public-domain datasets.
        - If there is any misunderstanding, please contact the author.
        - The the author does not own any of these datasets.
        - The readme in respective folder (or related Internet link) should be followed for citation/license requirements.
    """
    #print(public_dataset.__doc__)
    if name == 'SMS_spam':
        import pandas as pd
        df = pd.read_csv(io.BytesIO(pkgutil.get_data(__name__, "public/SMS_Spam_Collection/SMSSpamCollection.tsv")), sep='\t', quoting=csv.QUOTE_NONE, names=("label", "message"))
        return df
        #url = urllib.request.urlopen("https://archive.ics.uci.edu/ml/machine-learning-databases/00228/smsspamcollection.zip")
        #df = pd.read_csv(ZipFile(io.BytesIO(url.read())).open('SMSSpamCollection'), sep='\t', quoting=csv.QUOTE_NONE, names=("label", "message"))

    if name == 'Social_Network_Ads':
        import pandas as pd
        df = pd.read_csv(io.BytesIO(pkgutil.get_data(__name__, "public/Social_Network_Ads/Social_Network_Ads.csv")), encoding='utf8', sep=",")
        print("Social Network Ads is a public dataset that can be used to determine what audience a car company should target in its ads in order to sell a SUV on a social network website.\n")
        return df
        #url = urllib.request.urlopen("https://github.com/daniel-yj-yang/machlearn/raw/master/machlearn/datasets/public/Social_Network_Ads/Social_Network_Ads.csv")
        #df = pd.read_csv(io.BytesIO(url.read()), encoding='utf8', sep=",")

    if name == 'Fashion_MNIST':
        # this part of the code is modeled after https://github.com/zalandoresearch/fashion-mnist/blob/master/utils/mnist_reader.py
        import gzip
        path = os.path.dirname(__file__) + "/public/Fashion_MNIST"
        images_train_filepath = os.path.join(path, 'train-images-idx3-ubyte.gz')
        labels_train_filepath = os.path.join(path, 'train-labels-idx1-ubyte.gz')
        images_test_filepath  = os.path.join(path,  't10k-images-idx3-ubyte.gz')
        labels_test_filepath  = os.path.join(path,  't10k-labels-idx1-ubyte.gz')
        with gzip.open(labels_train_filepath, 'rb') as lbpath:
            labels_train = np.frombuffer(lbpath.read(),  dtype=np.uint8, offset=8)
        with gzip.open(images_train_filepath, 'rb') as imgpath:
            images_train = np.frombuffer(imgpath.read(), dtype=np.uint8, offset=16).reshape(len(labels_train), 784)
        with gzip.open(labels_test_filepath,  'rb') as lbpath:
            labels_test  = np.frombuffer(lbpath.read(),  dtype=np.uint8, offset=8)
        with gzip.open(images_test_filepath,  'rb') as imgpath:
            images_test  = np.frombuffer(imgpath.read(), dtype=np.uint8, offset=16).reshape(len(labels_test), 784)
        return images_train, labels_train, images_test, labels_test

    if name == 'nltk_data_path':
        return os.path.dirname(__file__) + "/public/nltk_data"

    if name == 'scikit_learn_data_path':
        return os.path.dirname(__file__) + "/public/scikit_learn_data"

    raise TypeError('recognizable dataset name is not provided')

    
class Fashion_MNIST_methods(object):
    def __init__(self):
        self.description = [
            "T-shirt/top",
            "Trouser",
            "Pullover",
            "Dress",
            "Coat",
            "Sandal",
            "Shirt",
            "Sneaker",
            "Bag",
            "Ankle boot"
        ]

    def get_label_desc(self, label_int):
        """
        Return the description of an integer label, range [0,9]
        """
        return self.description[label_int]

    def reshape_image(self, ndarray):
        return np.reshape(ndarray, (28, 28))

    def demo(self):
        X_train, y_train, X_test, y_test = public_dataset('Fashion_MNIST')
        import matplotlib.pyplot as plt
        for i in range(5000, 5005):
            sample = self.reshape_image(X_test[i])
            plt.figure()
            title = f"label {self.get_label_desc(y_test[i])}"
            print(title)
            plt.title(title)
            plt.imshow(sample, cmap='gray', vmin=0, vmax=255)
        plt.show()

