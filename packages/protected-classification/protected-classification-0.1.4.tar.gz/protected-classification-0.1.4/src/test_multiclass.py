import pandas as pd
import numpy as np
import sys

from sklearn.ensemble import RandomForestClassifier

import matplotlib.pyplot as plt
plt.style.use('ggplot')

from sklearn import metrics

from sklearn.metrics import (
    accuracy_score,
    brier_score_loss,
    log_loss,
    roc_auc_score,
)

from sklearn.calibration import CalibratedClassifierCV, CalibrationDisplay, calibration_curve
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

sys.path.append("../")

from protected_classification import (ProtectedClassification, cox_multiclass, gen_alpha,
                                            generate_protected_params, y_encode)



random_seed = 2025
np.random.seed(seed=random_seed)

n_classes = 3
betas = [1, 0.5, 2]

X, y = make_classification(
    n_samples=10000, n_classes=n_classes, n_informative=10, random_state=random_seed)

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=random_seed)

clf = RandomForestClassifier(random_state=random_seed, n_estimators=1000)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
p_pred = clf.predict_proba(X_test)

y_test_shift = y_test
y_test_shift[0,-1000:] = y_test[1, -1000:]
y_test_shift[1,-1000:] = y_test[0, -1000:]

pc = ProtectedClassification(estimator=clf)
p_prime, stats = pc.predict_proba(X_test, y_test, return_stats=True)
y_prime = pc.predict(X_test, y_test)

