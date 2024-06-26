# -*- coding: utf-8 -*-
"""TFG.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/19UvUFDfUDT52m2Dmh1Z6X4aPwoRU27vw
"""

import csv
import random as random
import numpy as np

from tensorflow import keras
import datetime
import matplotlib as plt
import seaborn as sns
import pandas as pd
from pylab import *

import progressbar
import pickle as pkl
from numpy.lib import stride_tricks
from skimage import feature
from sklearn import metrics
from sklearn.model_selection import train_test_split
import time

import csv
import sys
import random
import tensorflow as tf
import numpy as np

def functi(mostres, etiquetes):

    result = np.array(mostres).astype("float")

    resultE = np.array(etiquetes).astype("float")

    X_train, X_test, y_train, y_test = train_test_split(result, resultE, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

def train_model(X, y, classifier):

    if classifier == "SVM":
        from sklearn.svm import SVC
        print ('[INFO] Training Support Vector Machine model.')
        model = SVC(kernel="precomputed")
        model.fit(X, np.ravel(y))

    elif classifier == "RF":
        from sklearn.ensemble import RandomForestClassifier
        print ('[INFO] Training Random Forest model.')
        model = RandomForestClassifier(n_estimators=35, random_state=42)
        model.fit(X,  np.ravel(y))


    elif classifier == "KNN":
        from sklearn.neighbors import KNeighborsClassifier
        print ('[INFO] Training KNeighbors.')
        model = KNeighborsClassifier(n_neighbors=1)
        model.fit(X,  np.ravel(y))




    elif classifier == "ANN":

            # 2: Creación de la red neuronal
        model = keras.Sequential([
            keras.layers.Dense(32, activation='selu'),
            keras.layers.Dense(32, activation='selu'),
            keras.layers.Dense(32, activation='selu'),
            keras.layers.Dense(32, activation='selu'),
            keras.layers.Dense(2, activation='softmax')
        ])

        # 3: Función de optimización y metrica a optimizar
        model.compile(optimizer='adam',
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])

                # 4: Entrenamiento del modelo
        model.fit(
            x = X,
            y = y,
            epochs = 15,
            batch_size= 10
            #validation_split = 0.1
            )
    #print ('[INFO] Model training complete.')
    #print ('[INFO] Training Accuracy: %.2f' %model.score(X, y))
    return model

def test_model(X, y, model):

    pred = model.predict(X)
    pred=np.argmax(pred,axis=1) #Sols xarxa
    precision = metrics.precision_score(y, pred, average='weighted', labels=np.unique(pred))
    recall = metrics.recall_score(y, pred, average='weighted', labels=np.unique(pred))
    f1 = metrics.f1_score(y, pred, average='weighted', labels=np.unique(pred))
    accuracy = metrics.accuracy_score(y, pred)

    print ('--------------------------------')
    print ('[RESULTS] Accuracy: %.2f' %accuracy)
    print ('[RESULTS] Precision: %.2f' %precision)
    print ('[RESULTS] Recall: %.2f' %recall)
    print ('[RESULTS] F1: %.2f' %f1)
    print ('--------------------------------')


    #y_pred=pred
    #y_pred=np.argmax(y_pred,axis=1)
    #y_pred = model.predict_classes(samples_data)
    con_mat = tf.math.confusion_matrix(labels=y, predictions=pred).numpy()
    con_mat_norm = np.around(con_mat.astype('float') / con_mat.sum(axis=1)[:, np.newaxis], decimals=2)

    con_mat_df = pd.DataFrame(con_mat_norm,
                        index = ["Exp", "No"],
                     columns = ["Exp", "No"])


    sns.set(font_scale=2.0)
    figure = plt.figure(figsize=(8, 8))
    sns.heatmap(con_mat_df, annot=True,cmap=plt.cm.Blues)
    plt.tight_layout()
    plt.ylabel('Etiqueta real')
    plt.xlabel('Etiqueta inferida')
    plt.savefig('blau1.png', dpi=900)
    #plt.savefig('figura.pdf',)
    plt.show()

def main(classifier, output_model):

    start = time.time()

    df=pd.read_csv('test.csv', sep=',')
    df = df[~df['action0'].isnull()]
    etiquetes = df.pop("shouldExplain")
    etiquetes = pd.DataFrame(etiquetes)

    features = pd.get_dummies(df)

    (X_train, X_test, y_train, y_test) = functi(features, etiquetes)
    print(X_test)

    model = train_model(X_train, y_train, classifier)
    test_model(X_test, y_test, model)
    pkl.dump(model, open(output_model, "wb"))
    print ('Processing time:',time.time()-start)

main("ANN", "a")

import matplotlib.pyplot as plt

SMALL_SIZE = 8
plt.rc('font', size=SMALL_SIZE)
plt.rc('axes', titlesize=SMALL_SIZE)

fig, ax = plt.subplots()

ax.spines['bottom'].set_color('0')
ax.spines['top'].set_color('0')
ax.spines['right'].set_color('0')
ax.spines['left'].set_color('0')
#ax.patch.set_facecolor('0.1')
ax.grid(False)
NEst = ["1", "5", "10", "15", "20", "25", "30", "35"]
temperaturas = {'Acc_T':[0.93, 0.97, 0.98, 0.99, 0.99, 1, 1,1], 'Acc_Val':[0.85, 0.88, 0.92, 0.90, 0.90, 0.90, 0.88, 0.88 ], 'prec':[0.83, 0.88, 0.91, 0.89, 0.89, 0.89, 0.88, 0.88], "cob":[0.85, 0.88, 0.92, 0.90, 0.90, 0.90, 0.88, 0.88], "f1":[0.84, 0.88, 0.91, 0.90, 0.90, 0.90, 0.88, 0.88]}
ax.plot(NEst, temperaturas['Acc_T'], label = 'Exactitud entrenament')
ax.plot(NEst, temperaturas['Acc_Val'], label = 'Exactitud validació')
ax.plot(NEst, temperaturas['prec'], label = 'Precisió')
ax.plot(NEst, temperaturas['cob'], label = 'Cobertura')
ax.plot(NEst, temperaturas['f1'], label = 'F1')
ax.legend(loc = 'lower right', prop={'size': 7})
#plot.legend(loc=2, prop={'size': 6})
ax.patch.set_edgecolor('black')
ax.patch.set_linewidth('1')

for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
             ax.get_xticklabels() + ax.get_yticklabels()):
    item.set_fontsize(10)
plt.savefig('blau1.png', dpi=400,  transparent=True)
plt.show()

import matplotlib.pyplot as plt

SMALL_SIZE = 8
plt.rc('font', size=SMALL_SIZE)
plt.rc('axes', titlesize=SMALL_SIZE)

fig, ax = plt.subplots()

ax.spines['bottom'].set_color('0')
ax.spines['top'].set_color('0')
ax.spines['right'].set_color('0')
ax.spines['left'].set_color('0')
#ax.patch.set_facecolor('0.1')
ax.grid(False)
NEst = ["1", "3", "5", "7", "9", "11"]
temperaturas = {'Acc_T':[0.99, 0.99, 0.99, 0.99, 1,1], 'Acc_Val':[0.74, 0.75, 0.75, 0.778, 0.71, 0.71], 'prec':[0.73, 0.75, 0.76, 0.79, 0.72, 0.72], "cob":[0.74, 0.75, 0.75, 0.78, 0.71, 0.71], "f1":[0.73, 0.75, 0.76, 0.79, 0.72, 0.72]}
ax.plot(NEst, temperaturas['Acc_T'], label = 'Exactitud entrenament')
ax.plot(NEst, temperaturas['Acc_Val'], label = 'Exactitud validació')
ax.plot(NEst, temperaturas['prec'], label = 'Precisió')
ax.plot(NEst, temperaturas['cob'], label = 'Cobertura')
ax.plot(NEst, temperaturas['f1'], label = 'F1')
ax.legend(loc = 'upper right', prop={'size': 7})
#plot.legend(loc=2, prop={'size': 6})
ax.patch.set_edgecolor('black')
ax.patch.set_linewidth('1')

for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
             ax.get_xticklabels() + ax.get_yticklabels()):
    item.set_fontsize(10)
plt.savefig('blau1.png', dpi=400,  transparent=True)

import matplotlib.pyplot as plt

SMALL_SIZE = 8
plt.rc('font', size=SMALL_SIZE)
plt.rc('axes', titlesize=SMALL_SIZE)

fig, ax = plt.subplots()

ax.spines['bottom'].set_color('0')
ax.spines['top'].set_color('0')
ax.spines['right'].set_color('0')
ax.spines['left'].set_color('0')
#ax.patch.set_facecolor('0.1')
ax.grid(False)
NEst = ["RBF", "Poly", "Linear", "Sigmoid"]
temperaturas = {'Acc_T':[0.74, 0.78, 0.99, 0.74], 'Acc_Val':[0.83, 0.87, 0.88, 0.83], 'prec':[0.83, 0.89, 0.89, 0.83], "cob":[0.82, 0.87, 0.88, 0.83], "f1":[0.76, 0.83, 0.89, 0.76]}
ax.plot(NEst, temperaturas['Acc_T'], label = 'Exactitud entrenament')
ax.plot(NEst, temperaturas['Acc_Val'], label = 'Exactitud validació')
ax.plot(NEst, temperaturas['prec'], label = 'Precisió')
ax.plot(NEst, temperaturas['cob'], label = 'Cobertura')
ax.plot(NEst, temperaturas['f1'], label = 'F1')
ax.legend(loc = 'upper right', prop={'size': 7})
#plot.legend(loc=2, prop={'size': 6})
ax.patch.set_edgecolor('black')
ax.patch.set_linewidth('1')

for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
             ax.get_xticklabels() + ax.get_yticklabels()):
    item.set_fontsize(10)
plt.savefig('blau1.png', dpi=400,  transparent=True)
plt.show()

import matplotlib.pyplot as plt

SMALL_SIZE = 8
plt.rc('font', size=SMALL_SIZE)
plt.rc('axes', titlesize=SMALL_SIZE)

fig, ax = plt.subplots()

ax.spines['bottom'].set_color('0')
ax.spines['top'].set_color('0')
ax.spines['right'].set_color('0')
ax.spines['left'].set_color('0')
#ax.patch.set_facecolor('0.1')
ax.grid(False)
NEst = ["A", "B", "C", "D", "E", "F", "G", "H"]
temperaturas = {'Acc_T':[0.73, 0.94, 0.95, 0.95, 0.93, 0.94, 0.96,0.97], 'Acc_Val':[0.82, 0.92, 0.90, 0.90, 0.95, 0.87, 0.88, 0.88 ], 'prec':[0.76, 0.92, 0.89, 0.91, 0.95, 0.88, 0.87, 0.88], "cob":[0.82, 0.92, 0.90, 0.90, 0.95, 0.87, 0.88, 0.88], "f1":[0.77, 0.90, 0.90, 0.88, 0.91, 0.87, 0.87, 0.88]}
ax.plot(NEst, temperaturas['Acc_T'], label = 'Exactitud entrenament')
ax.plot(NEst, temperaturas['Acc_Val'], label = 'Exactitud validació')
ax.plot(NEst, temperaturas['prec'], label = 'Precisió')
ax.plot(NEst, temperaturas['cob'], label = 'Cobertura')
ax.plot(NEst, temperaturas['f1'], label = 'F1')
ax.legend(loc = 'lower right', prop={'size': 7})
#plot.legend(loc=2, prop={'size': 6})
ax.patch.set_edgecolor('black')
ax.patch.set_linewidth('1')

for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
             ax.get_xticklabels() + ax.get_yticklabels()):
    item.set_fontsize(10)
plt.savefig('blau1.png', dpi=400,  transparent=True)
plt.show()

import matplotlib.pyplot as plt

SMALL_SIZE = 8
plt.rc('font', size=SMALL_SIZE)
plt.rc('axes', titlesize=SMALL_SIZE)

fig, ax = plt.subplots()

ax.spines['bottom'].set_color('0')
ax.spines['top'].set_color('0')
ax.spines['right'].set_color('0')
ax.spines['left'].set_color('0')
#ax.patch.set_facecolor('0.1')
ax.grid(False)
NEst = ["RF", "KNN", "SVM", "ANN"]
temperaturas = {'Acc_T':[0.98, 0.99, 0.99, 0.93], 'Acc_Val':[0.92, 0.78, 0.88, 0.95], 'prec':[0.92, 0.79, 0.89, 0.95], "cob":[0.92, 0.78, 0.88, 0.95], "f1":[0.91, 0.79, 0.89, 0.91]}
ax.plot(NEst, temperaturas['Acc_T'], label = 'Exactitud entrenament')
ax.plot(NEst, temperaturas['Acc_Val'], label = 'Exactitud validació')
ax.plot(NEst, temperaturas['prec'], label = 'Precisió')
ax.plot(NEst, temperaturas['cob'], label = 'Cobertura')
ax.plot(NEst, temperaturas['f1'], label = 'F1')
ax.legend(loc = 'lower right', prop={'size': 7})
#plot.legend(loc=2, prop={'size': 6})
ax.patch.set_edgecolor('black')
ax.patch.set_linewidth('1')

for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
             ax.get_xticklabels() + ax.get_yticklabels()):
    item.set_fontsize(10)
plt.savefig('blau1.png', dpi=400,  transparent=True)
plt.show()

import matplotlib.pyplot as plt

SMALL_SIZE = 8
plt.rc('font', size=SMALL_SIZE)
plt.rc('axes', titlesize=SMALL_SIZE)

fig, ax = plt.subplots()

ax.spines['bottom'].set_color('0')
ax.spines['top'].set_color('0')
ax.spines['right'].set_color('0')
ax.spines['left'].set_color('0')
#ax.patch.set_facecolor('0.1')
ax.grid(False)
NEst = ["1", "3", "5", "7", "9", "11", "13", "15", "17", "19", "21", "23", "25"]
temperaturas = {'Acc_T':[0.34, 0.375, 0.387, 0.38, 0.41, 0.395, 0.39,0.378, 0.37, 0.375, 0.37, 0.368, 0.359]}
ax.plot(NEst, temperaturas['Acc_T'], label = 'Exactitud entrenament')

#ax.legend(loc = 'lower right', prop={'size': 7})
#plot.legend(loc=2, prop={'size': 6})
ax.patch.set_edgecolor('black')
ax.patch.set_linewidth('1')
plt.ylabel('IoU')
plt.xlabel('Number of Neihgbors')
for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
             ax.get_xticklabels() + ax.get_yticklabels()):
    item.set_fontsize(10)
plt.savefig('blau1.png', dpi=400,  transparent=True)
plt.show()

import matplotlib.pyplot as plt

SMALL_SIZE = 8
plt.rc('font', size=SMALL_SIZE)
plt.rc('axes', titlesize=SMALL_SIZE)

fig, ax = plt.subplots()

ax.spines['bottom'].set_color('0')
ax.spines['top'].set_color('0')
ax.spines['right'].set_color('0')
ax.spines['left'].set_color('0')
#ax.patch.set_facecolor('0.1')
ax.grid(False)
NEst = ["RF", "KNN", "SVM", "ANN"]
temperaturas = {'Acc_T':[0.98, 0.99, 0.99, 0.93], 'Acc_Val':[0.92, 0.78, 0.88, 0.95], 'prec':[0.92, 0.79, 0.89, 0.95], "cob":[0.92, 0.78, 0.88, 0.95], "f1":[0.91, 0.79, 0.89, 0.91]}
ax.bar(NEst, temperaturas['Acc_T'], label = 'Exactitud entrenament')
ax.bar(NEst, temperaturas['Acc_Val'], label = 'Exactitud validació')
ax.bar(NEst, temperaturas['prec'], label = 'Precisió')
ax.bar(NEst, temperaturas['cob'], label = 'Cobertura')
ax.bar(NEst, temperaturas['f1'], label = 'F1')
plt.xticks(4, 4)
ax.legend(loc = 'lower right', prop={'size': 7})
#plot.legend(loc=2, prop={'size': 6})
ax.patch.set_edgecolor('black')
ax.patch.set_linewidth('1')

for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
             ax.get_xticklabels() + ax.get_yticklabels()):
    item.set_fontsize(10)
plt.savefig('blau1.png', dpi=400,  transparent=True)
plt.show()

plt.hist([temperaturas['Acc_T'], temperaturas['Acc_Val']])

# Import Library

import numpy as np
import matplotlib.pyplot as plt

# Define Data

team = ['RF','KNN','SVM','XNA']
female = [5, 10, 15, 20, 25]
male = [15, 20, 30, 16, 13]
temperaturas = {'Acc_T':[0.98, 0.99, 0.99, 0.93], 'Acc_Val':[0.92, 0.78, 0.88, 0.95], 'prec':[0.92, 0.79, 0.89, 0.95], "cob":[0.92, 0.78, 0.88, 0.95], "f1":[0.91, 0.79, 0.89, 0.91]}
x_axis = np.arange(len(team))

# Multi bar Chart

#plt.bar(x_axis -0.2, female, width=0.4, label = 'Female')
#plt.bar(x_axis +0.2, male, width=0.4, label = 'Male')
plt.bar(x_axis - 0.3, temperaturas['Acc_T'],width=0.1, label = 'Exactitud entrenament')
plt.bar(x_axis -0.15, temperaturas['Acc_Val'],width=0.1, label = 'Exactitud validació')
plt.bar(x_axis, temperaturas['prec'],width=0.1, label = 'Precisió')
plt.bar(x_axis+0.15, temperaturas['cob'],width=0.1, label = 'Cobertura')
plt.bar(x_axis+0.30, temperaturas['f1'],width=0.1, label = 'F1')

# Xticks

plt.xticks(x_axis, team)

# Add legend

plt.legend()

# Display

plt.show()

import matplotlib.pyplot as plt

SMALL_SIZE = 8
plt.rc('font', size=SMALL_SIZE)
plt.rc('axes', titlesize=SMALL_SIZE)

fig, ax = plt.subplots()

ax.spines['bottom'].set_color('0')
ax.spines['top'].set_color('0')
ax.spines['right'].set_color('0')
ax.spines['left'].set_color('0')
#ax.patch.set_facecolor('0.1')
ax.grid(False)
NEst = ["RF", "KNN", "SVM", "ANN"]
temperaturas = {'Acc_T':[0.98, 0.99, 0.99, 0.93], 'Acc_Val':[0.92, 0.78, 0.88, 0.95], 'prec':[0.92, 0.79, 0.89, 0.95], "cob":[0.92, 0.78, 0.88, 0.95], "f1":[0.91, 0.79, 0.89, 0.91]}
team = ['RF','KNN','SVM','XNA']
female = [5, 10, 15, 20, 25]
male = [15, 20, 30, 16, 13]
temperaturas = {'Acc_T':[0.98, 0.99, 0.99, 0.93], 'Acc_Val':[0.92, 0.78, 0.88, 0.95], 'prec':[0.92, 0.79, 0.89, 0.95], "cob":[0.92, 0.78, 0.88, 0.95], "f1":[0.91, 0.79, 0.89, 0.91]}
x_axis = np.arange(len(team))

# Multi bar Chart

#plt.bar(x_axis -0.2, female, width=0.4, label = 'Female')
#plt.bar(x_axis +0.2, male, width=0.4, label = 'Male')
plt.bar(x_axis - 0.3, temperaturas['Acc_T'],width=0.1, label = 'Exactitud entrenament')
plt.bar(x_axis -0.15, temperaturas['Acc_Val'],width=0.1, label = 'Exactitud validació')
plt.bar(x_axis, temperaturas['prec'],width=0.1, label = 'Precisió')
plt.bar(x_axis+0.15, temperaturas['cob'],width=0.1, label = 'Cobertura')
plt.bar(x_axis+0.30, temperaturas['f1'],width=0.1, label = 'F1')
ax.legend(loc = 'lower right', prop={'size': 7})
#plot.legend(loc=2, prop={'size': 6})
ax.patch.set_edgecolor('black')
ax.patch.set_linewidth('1')
plt.ylim(ymin=0.7, ymax = 1)
for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
             ax.get_xticklabels() + ax.get_yticklabels()):
    item.set_fontsize(10)
plt.xticks(x_axis, team)
plt.savefig('blau1.png', dpi=400,  transparent=True)
plt.show()

import matplotlib.pyplot as plt

SMALL_SIZE = 8
plt.rc('font', size=SMALL_SIZE)
plt.rc('axes', titlesize=SMALL_SIZE)

fig, ax = plt.subplots()

ax.spines['bottom'].set_color('0')
ax.spines['top'].set_color('0')
ax.spines['right'].set_color('0')
ax.spines['left'].set_color('0')
#ax.patch.set_facecolor('0.1')
ax.grid(False)
NEst = ["Exact. entr.", "Exact. val.", "Precisió",'Cobertura', "F1"]
#temperaturas = {'Acc_T':[0.98, 0.99, 0.99, 0.93], 'Acc_Val':[0.92, 0.78, 0.88, 0.95], 'prec':[0.92, 0.79, 0.89, 0.95], "cob":[0.92, 0.78, 0.88, 0.95], "f1":[0.91, 0.79, 0.89, 0.91]}
temperaturas = {'RF':[0.98, 0.92, 0.92,0.92, 0.91], 'KNN':[0.99, 0.78, 0.79, 0.78, 0.79], 'SVM':[0.99, 0.88, 0.89, 0.88, 0.89], "XNA":[0.93, 0.95, 0.95, 0.95, 0.91]}
team = ["Exact. entr.", "Exact. val.", "Precisió",'Cobertura', "F1"]

#temperaturas = {'Acc_T':[0.98, 0.99, 0.99, 0.93], 'Acc_Val':[0.92, 0.78, 0.88, 0.95], 'prec':[0.92, 0.79, 0.89, 0.95], "cob":[0.92, 0.78, 0.88, 0.95], "f1":[0.91, 0.79, 0.89, 0.91]}
x_axis = np.arange(len(team))

# Multi bar Chart

#plt.bar(x_axis -0.2, female, width=0.4, label = 'Female')
#plt.bar(x_axis +0.2, male, width=0.4, label = 'Male')
plt.bar(x_axis - 0.3, temperaturas['RF'],width=0.1, label = 'RF')
plt.bar(x_axis -0.15, temperaturas['KNN'],width=0.1, label = 'KNN')
plt.bar(x_axis, temperaturas['SVM'],width=0.1, label = 'SVM')
plt.bar(x_axis+0.15, temperaturas['XNA'],width=0.1, label = 'XNA')
#plt.bar(x_axis+0.30, temperaturas['f1'],width=0.1, label = 'F1')
ax.legend(loc = 'upper right', prop={'size': 7})
#plot.legend(loc=2, prop={'size': 6})
ax.patch.set_edgecolor('black')
ax.patch.set_linewidth('1')
plt.ylim(ymin=0.7, ymax = 1)
for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
             ax.get_xticklabels() + ax.get_yticklabels()):
    item.set_fontsize(10)
plt.xticks(x_axis, team)
plt.savefig('blau1.png', dpi=400,  transparent=True)
plt.show()

# Import Library

import numpy as np
import matplotlib.pyplot as plt

# Define Data

team = ['RF','KNN','SVM']
female = [5, 10, 15, 20, 25]
male = [15, 20, 30, 16, 13]
temperaturas = {'Acc_T':[0.95, 0.85, 0.92], 'Acc_Val':[0.92, 0.82, 0.88], 'prec':[0.92, 0.80, 0.89], "cob":[0.92, 0.80, 0.88], "f1":[0.91, 0.81, 0.89]}
#team = ["Exact. entr.", "Exact. val.", "Precisió",'Cobertura', "F1"]
x_axis = np.arange(len(team))

# Multi bar Chart

#plt.bar(x_axis -0.2, female, width=0.4, label = 'Female')
#plt.bar(x_axis +0.2, male, width=0.4, label = 'Male')
plt.bar(x_axis - 0.3, temperaturas['Acc_T'],width=0.1, label = 'Training Accuracy')
plt.bar(x_axis -0.15, temperaturas['Acc_Val'],width=0.1, label = 'Validation Accuracy')
plt.bar(x_axis, temperaturas['prec'],width=0.1, label = 'Precision')
plt.bar(x_axis+0.15, temperaturas['cob'],width=0.1, label = 'Recall')
plt.bar(x_axis+0.30, temperaturas['f1'],width=0.1, label = 'F1')

# Xticks

plt.xticks(x_axis, team)

# Add legend

plt.legend()
ax.patch.set_edgecolor('black')
ax.patch.set_linewidth('1')
plt.ylim(ymin=0.7, ymax = 1)
for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
             ax.get_xticklabels() + ax.get_yticklabels()):
    item.set_fontsize(10)
plt.xticks(x_axis, team)
plt.savefig('blau1.png', dpi=400,  transparent=True)
# Display

plt.show()

