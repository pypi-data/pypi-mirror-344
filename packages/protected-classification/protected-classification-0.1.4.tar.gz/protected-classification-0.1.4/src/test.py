from pprint import pprint
from river import datasets
import numpy as np
import matplotlib.pyplot as plt

import calibration as cal

from sklearn.preprocessing import OneHotEncoder

import pandas as pd

from river import compose
from river import linear_model, forest, ensemble, tree, active
from river import metrics, preprocessing

from sklearn.metrics import log_loss

from src.protected_classification import ProtectedClassification, y_pred_encode, p_pred_encode
from sklearn.metrics import log_loss, accuracy_score, brier_score_loss

dataset = datasets.Phishing()

model = compose.Pipeline(
    preprocessing.StandardScaler(),
    forest.ARFClassifier(seed=7, n_models=15),
    # ensemble.ADWINBaggingClassifier(forest.ARFClassifier())
)

pc = ProtectedClassification()

# p_pred = np.array(([0.1, 0.3, 0.6, 0.0], [0.2, 0.2, 0.6, 0.0], [0.4, 0.1, 0.5, 0.0], [0.4, 0.1, 0.2, 0.3]))
# y = np.array((['c', 'b', 'a', 'd']))

# pc.fit(x=None, y=y, test_probs=p_pred)

# opa = pc.predict_proba(test_probs=p_pred)

# def find_first(my_list):
#     return next((i for i, x in enumerate(my_list) if x), None)
#
# opa = [[1.0, 0.0, 0.0],
#  [0.0, 1.0, 0.0],
#  [0.0, 0.0, 1.0],
#  [-1.0, 0.0, 0.0],
#  [0.0, -1.0, 0.0],
#  [0.0, 0.0, -1.0]]
#
# opa.sort(key=find_first)


#
#
# ys = []
#
#
# p_pred = {'a': 0.5, 'c': 0.5}
# y_test = {'b'}
#
# y_stack = np.unique([i for i, _ in p_pred.items()] + list(y_test))
#
# if len(ys) != 0:
#     ys = np.array(list(ys) + [i for i in y_stack if i not in ys])
# else:
#     ys = y_stack
#
# p_pred = {'a': 0.1, 'c': 0.3, 'b': 0.6}
# y_test = {'aa'}
#
# p_pred.items()
#
# enc = OneHotEncoder()
# enc.fit(ys.reshape(-1, 1))
# y_encoded = enc.transform(ys.reshape(-1, 1)).toarray()
#

# pc.fit(x=None, y=y_test, test_probs=p_pred_test)

# metric = metrics.LogLoss()
# metric_prot = metrics.LogLoss()

# ys = []
# y_preds = []
# p_preds = []
# p_descs = []
# p_primes = []

ll_base = []
ll_prot = []
br_base=[]
br_prot=[]
acc_base = []
acc_prot = []

y_preds = []
y_primes = []
p_preds = []
p_primes = []


opa = 0
for x, y in dataset:
    opa += 1
    print(opa)
    y_pred = model.predict_one(x)     # make a prediction
    p_pred = model.predict_proba_one(x)
    p_prime, y_prime = pc.predict_proba_one(p_pred)
    # p_primes.append(p_prime)
    if opa > 1000:
        ll_base.append(
           log_loss(y_pred_encode(y, np.array(list(p_pred.keys())))[0], p_pred_encode(p_pred, np.array(list(p_pred.keys())))[0]))
        ll_prot.append(
           log_loss(y_pred_encode(y, np.array(list(p_prime.keys())))[0], p_pred_encode(p_prime, np.array(list(p_prime.keys())))[0]))
        br_base.append(
            brier_score_loss(y_pred_encode(y, np.array(list(p_pred.keys())))[0],
                     p_pred_encode(p_pred, np.array(list(p_pred.keys())))[0]))
        br_prot.append(
            brier_score_loss(y_pred_encode(y, np.array(list(p_prime.keys())))[0],
                     p_pred_encode(p_prime, np.array(list(p_prime.keys())))[0]))
        acc_base.append(y_pred == y)
        acc_prot.append(y_prime == y)

        y_preds.append(y_pred_encode(y, np.array(list(p_pred.keys())))[0])
        y_primes.append(y_pred_encode(y, np.array(list(p_prime.keys())))[0])
        p_preds.append(p_pred_encode(p_pred, np.array(list(p_pred.keys())))[0])
        p_primes.append(p_pred_encode(p_prime, np.array(list(p_prime.keys())))[0])
    # ys.append(y)
    # y_preds.append(y_pred)
    # p_preds.append([j for i, j in p_pred.items()])
    # p_descs.append([i for i, j in p_pred.items()])
    # if opa > 1000:       # update the metric
    #     metric = metric.update(y, p_pred)
    # if opa > 1000:
    #     metric_prot = metric_prot.update(y, p_prime)
    model = model.learn_one(x, y)
    pc.learn_one(p_pred, y_pred) # make the model learn

print(np.mean(np.array(ll_base)))
print(np.mean(np.array(ll_prot)))

print(np.mean(np.array(br_base)))
print(np.mean(np.array(br_prot)))

print(np.mean(np.array(acc_base)))
print(np.mean(np.array(acc_prot)))

print(cal.get_calibration_error(np.array(p_preds), np.argmax(np.array(y_preds), axis=1), debias=False))
print(cal.get_calibration_error(np.array(p_primes), np.argmax(np.array(y_primes), axis=1), debias=False))

from sklearn.calibration import CalibrationDisplay
fig, ax = plt.subplots(1,1)

display = CalibrationDisplay.from_predictions(
            np.argmax(np.array(y_preds), axis=1),
            np.array(p_preds)[:, 1],
            n_bins=10,
            ax=ax
        )

display = CalibrationDisplay.from_predictions(
            np.argmax(np.array(y_primes), axis=1),
            np.array(p_primes)[:, 1],
            n_bins=10,
            ax=ax
        )

plt.show()

# metric = metrics.LogLoss()
# for yt, yp in zip(y, p_pred):
#     metric = metric.update(yt, yp)
#     print(metric.get())
#
# print(metric_prot)
# print(log_loss())


# 0.23623166697714068
# 0.20540926566805462
# 0.06518416252737808
# 0.05967504941279175
# 0.92
# 0.92
# 0.05830588185494034
# 0.0