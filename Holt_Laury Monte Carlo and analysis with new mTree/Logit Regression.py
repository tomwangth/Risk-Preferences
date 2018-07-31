import pandas as pd
import numpy as np
import sklearn
import matplotlib.pyplot as plt
import seaborn as sns

'Logit regression for Holt Laury simulation output, plus graphing ROC curve'

# Receive Data
data = pd.read_csv("HL.csv")
print(data)
col = ["delta", "epsilon", "cross_term"]
dep_var = data["hits"].tolist()
X = data[col]

# Run Logit Regression
import statsmodels.api as sm
logit_model=sm.Logit(dep_var,X)
result=logit_model.fit()
print(result.summary())

#ROC
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, dep_var, test_size=0.3, random_state=0)
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
logreg = LogisticRegression()
logreg.fit(X_train, y_train)
y_pred = logreg.predict(X_test)
print('Accuracy of logistic regression classifier on test set: {:.2f}'.format(logreg.score(X_test, y_test)))


from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
logit_roc_auc = roc_auc_score(y_test, logreg.predict(X_test))
fpr, tpr, thresholds = roc_curve(y_test, logreg.predict_proba(X_test)[:,1])
plt.figure()
plt.plot(fpr, tpr, label='Logistic Regression (area = %0.2f)' % logit_roc_auc)
plt.plot([0, 1], [0, 1],'r--')
#plt.xlim([0.0, 1.0])
#plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic')
plt.legend(loc="lower right")
plt.savefig('Log_ROC')
plt.show()

