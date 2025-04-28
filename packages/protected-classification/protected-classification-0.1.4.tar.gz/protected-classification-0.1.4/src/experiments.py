from river import datasets
import numpy as np
import matplotlib.pyplot as plt
import random

import calibration as cal

from sklearn.calibration import CalibrationDisplay

import pandas as pd

from river import drift, compose, feature_extraction
from river import linear_model, forest, ensemble, tree, naive_bayes, neighbors
from river import metrics, preprocessing

from src.protected_classification import ProtectedClassification, y_pred_encode, p_pred_encode
from sklearn.metrics import log_loss, brier_score_loss



dsets_binary = {
    'Phishing': datasets.Phishing(),
    'Bananas': datasets.Bananas(),
    'CreditCard': datasets.CreditCard(),
    'Elec2': datasets.Elec2(),
    'HTTP': datasets.HTTP(),
    'SMTP': datasets.SMTP(),
    'MaliciousURL': datasets.MaliciousURL(),
    # 'SMSSpam': datasets.SMSSpam(),
    # 'TREC07': datasets.TREC07()
}

dsets_multiclass = {
    'ImageSegments': datasets.ImageSegments(),
    'Insects': datasets.Insects(),
    'Keystroke': datasets.Keystroke(),
}


models = {
    'ARF': forest.ARFClassifier(),
    'SRP': ensemble.SRPClassifier(),
    'Naive': naive_bayes.GaussianNB(),
    'kNN': neighbors.KNNClassifier(),
    'Logistic': linear_model.LogisticRegression(),
    'ADWIN': ensemble.ADWINBaggingClassifier(forest.ARFClassifier()),
    'Bagging': ensemble.BaggingClassifier(forest.ARFClassifier()),
    'Hoeffding': tree.HoeffdingAdaptiveTreeClassifier(),
    'EFTree': tree.ExtremelyFastDecisionTreeClassifier(),
    'DriftSRP': drift.DriftRetrainingClassifier(
        model=ensemble.SRPClassifier(),
        drift_detector=drift.binary.DDM()),
    'DriftARF': drift.DriftRetrainingClassifier(
        model=forest.ARFClassifier(),
        drift_detector=drift.binary.DDM())
}

adaptive_models = ['ARF', 'SRP']

seeds = range(100, 110)

df_container = pd.DataFrame()

for dset_name, dset in dsets_binary.items():
    for model_name, mod in models.items():
        for random_seed in seeds:

            print(dset_name + ' ' + model_name + ' ' + str(random_seed))

            random.seed(random_seed)

            dataset = dset

            if model_name in adaptive_models:
                mod.clear()

            model = compose.Pipeline(
                # preprocessing.OneHotEncoder(),
                # feature_extraction.TFIDF(on='body'),
                preprocessing.StandardScaler(),
                mod
            )

            pc = ProtectedClassification()

            scratch = []

            metric_base_acc = metrics.Accuracy()
            metric_prot_acc = metrics.Accuracy()
            metric_base_roc = metrics.ROCAUC()
            metric_prot_roc = metrics.ROCAUC()

            ll_base = []
            ll_prot = []
            br_base = []
            br_prot = []
            acc_base = []
            acc_prot = []

            y_preds = []
            y_primes = []
            p_preds = []
            p_primes = []

            opa = 0
            classes = []
            for x, y in dataset:
                opa += 1
                print('\r', "{:.0%}".format(opa/dataset.n_samples), end='')
                classes.append(y)
                # classes.append(y)
                classes_unique = np.unique(np.array(classes))

                y_pred = model.predict_one(x)     # make a prediction
                p_pred = model.predict_proba_one(x)
                p_prime, y_prime = pc.predict_proba_one(p_pred)

                if len(classes_unique) > 1 and len(p_prime) > 0:

                    metric_base_acc = metric_base_acc.update(y, y_pred)
                    metric_prot_acc = metric_prot_acc.update(y, y_prime)
                    metric_base_roc = metric_base_roc.update(y, y_pred)
                    metric_prot_roc = metric_prot_roc.update(y, y_prime)

                    # opa > int(dataset.n_samples / 20)
                    ll_base.append(
                       log_loss(y_pred_encode(y, classes_unique)[0], p_pred_encode(p_pred, classes_unique)[0]))
                    ll_prot.append(
                       log_loss(y_pred_encode(y, classes_unique)[0], p_pred_encode(p_prime, classes_unique)[0]))
                    br_base.append(
                        brier_score_loss(y_pred_encode(y, classes_unique)[0],
                                 p_pred_encode(p_pred, classes_unique)[0]))
                    br_prot.append(
                        brier_score_loss(y_pred_encode(y, classes_unique)[0],
                                         p_pred_encode(p_prime, classes_unique)[0]))

                    # acc_base.append(y_pred == y)
                    # acc_prot.append(y_prime == y)

                    y_preds.append(y_pred_encode(y_pred, classes_unique)[0])
                    y_primes.append(y_pred_encode(y_prime, classes_unique)[0])
                    p_preds.append(p_pred_encode(p_pred, classes_unique)[0])
                    p_primes.append(p_pred_encode(p_prime, classes_unique)[0])

                model = model.learn_one(x, y)
                pc.learn_one(p_pred, y_pred)

            print('\r', metric_base_acc)

            scratch.append(['log_loss', np.mean(np.array(ll_base)), np.mean(np.array(ll_prot))])
            scratch.append(['brier_loss', np.mean(np.array(br_base)), np.mean(np.array(br_prot))])
            scratch.append(['accuracy', metric_base_acc.get(), metric_prot_acc.get()])
            scratch.append(['ROC', metric_base_roc.get(), metric_prot_roc.get()])
            scratch.append([
                'cal_error',
                cal.get_calibration_error(np.array(p_preds), np.argmax(np.array(y_preds), axis=1), debias=True),
                cal.get_calibration_error(np.array(p_primes), np.argmax(np.array(y_primes), axis=1), debias=True)])

            scratch = pd.DataFrame(scratch, columns=['metric', 'base', 'protected'])
            scratch['seed'] = random_seed
            scratch['dataset'] = dset_name
            scratch['model'] = model_name
            df_container = pd.concat((df_container, scratch), axis=0)
            df_container.to_csv('results_summary_final_opa.csv')

results = pd.read_csv('results_summary_final_opa.csv')
print(results)
        #
        # print(np.mean(np.array(ll_base)))
        # print(np.mean(np.array(ll_prot)))
        #
        # print(np.mean(np.array(br_base)))
        # print(np.mean(np.array(br_prot)))
        #
        # print(np.mean(np.array(acc_base)))
        # print(np.mean(np.array(acc_prot)))
        #
        # print(cal.get_calibration_error(np.array(p_preds), np.argmax(np.array(y_preds), axis=1), debias=False))
        # print(cal.get_calibration_error(np.array(p_primes), np.argmax(np.array(y_primes), axis=1), debias=False))


# fig, ax = plt.subplots(1, 1)
#
# display = CalibrationDisplay.from_predictions(
#             np.argmax(np.array(y_preds), axis=1),
#             np.array(p_preds)[:, 1],
#             n_bins=10,
#             ax=ax
#         )
#
# display = CalibrationDisplay.from_predictions(
#             np.argmax(np.array(y_primes), axis=1),
#             np.array(p_primes)[:, 1],
#             n_bins=10,
#             ax=ax
#         )
#
# plt.show()

# dataset = datasets.Phishing()
# metric = metrics.F1()
# model = compose.Pipeline(
#     # preprocessing.StandardScaler(),
#     ensemble.SRPClassifier(),
#     # ensemble.ADWINBaggingClassifier(forest.ARFClassifier())
# )
#
# dataset = datasets.CreditCard().take(10000)

# model = drift.DriftRetrainingClassifier(
#     ensemble.SRPClassifier(),
#     drift_detector=drift.binary.EDDM()
# )

# model = compose.Pipeline(
#     # preprocessing.StandardScaler(),
#     # ensemble.SRPClassifier(),
#     # ensemble.ADWINBaggingClassifier(forest.ARFClassifier())
#     ensemble.SRPClassifier()
# )


