import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler, Imputer, normalize
from sklearn import datasets
import csv
from sklearn.metrics import accuracy_score
from sklearn.externals import joblib
import cPickle as pkl

data = []
#LabelEncoding
workclass = LabelEncoder()
workclass.fit(["Private", "Self-emp-not-inc", "Self-emp-inc", "Federal-gov", "Local-gov", "State-gov", "Without-pay", "Never-worked", "?"])
education = LabelEncoder()
education.fit(["Bachelors", "Some-college", "11th", "HS-grad", "Prof-school", "Assoc-acdm", "Assoc-voc", "9th", "7th-8th", "12th", "Masters", "1st-4th", "10th", "Doctorate", "5th-6th", "Preschool", "?"])
occupation = LabelEncoder()
occupation.fit(["Tech-support", "Craft-repair", "Other-service", "Sales", "Exec-managerial", "Prof-specialty", "Handlers-cleaners", "Machine-op-inspct", "Adm-clerical", "Farming-fishing", "Transport-moving", "Priv-house-serv", "Protective-serv", "Armed-Forces", "?"])
sex = LabelEncoder()
sex.fit(["Female", "Male"])
result = LabelEncoder()
result.fit(["<=50K", ">50K"])

with open("adult.data", 'rb') as file:
    lines = file.readlines()
    x = 0
    for line in lines:
        if x != 20000:
            line = line.replace(' ', '').replace('\n', '')
            line = line.split(',')
            line[1] = workclass.transform([line[1]])[0]
            line[3] = education.transform([line[3]])[0]
            line[6] = occupation.transform([line[6]])[0]
            line[9] = sex.transform([line[9]])[0]
            line[14] = result.transform([line[14]])[0]
            data.append(line)
            x += 1


print data[2]
data_np = np.array([np.array(x) for x in data])

print data_np.shape

data_np = np.delete(data_np, 13, 1)
data_np = np.delete(data_np, 8, 1)
data_np = np.delete(data_np, 7, 1)
data_np = np.delete(data_np, 5, 1)
data_np = np.delete(data_np, 4, 1)
data_np = np.delete(data_np, 2, 1)

print data_np[8]

data_np = data_np.astype(float)
print data_np[8]



from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()


scaler.fit(data_np)
data_scaled = scaler.transform(data_np)
print data_np[8]


data_x = [] 
data_y = []
for n in data_np:
    data_y.append(n[-1])
    data_x.append(n[:-1])

data_x = np.array(data_x)
data_y = np.array(data_y)  
data_train_x = data_x[:18000]
data_train_y = data_y[:18000]
data_test_x = data_x[18000:]
data_test_y = data_y[18000:]

print data_train_x.shape, data_train_y.shape
print data_test_x.shape, data_test_y.shape


#Create, train and test classifiers
print '----------------------------------------------'
from sklearn import svm
clf = svm.SVC(kernel='rbf', cache_size = 500, degree = 3, decision_function_shape='ovr')
clf.fit(data_train_x, data_train_y)
print clf.score(data_train_x, data_train_y)
pred = clf.predict(data_test_x)
print pred.shape
print data_test_y.shape
print "SVM score: %s" % accuracy_score(data_test_y, pred)

from sklearn.naive_bayes import GaussianNB
gnb = GaussianNB()
gnb.fit(data_train_x, data_train_y)
print gnb.score(data_train_x, data_train_y)
pred = gnb.predict(data_test_x)
print "GaussianNB score: %s" % accuracy_score(data_test_y[:300], pred[:300])

from sklearn.neural_network import MLPClassifier
neu = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(15,), random_state=1)
neu.fit(data_train_x, data_train_y)
print neu.score(data_train_x, data_train_y)
pred = neu.predict(data_test_x)
print "MLPClassifier score: %s" % accuracy_score(data_test_y[:300], pred[:300])

#Save classifiers to files
print '----------------------------------------------'
with open("SVM.pkl", 'wb') as f : pkl.dump(clf, f)
with open("GNB.pkl", 'wb') as f : pkl.dump(gnb, f)
with open("NEU.pkl", 'wb') as f : pkl.dump(neu, f)
print data_test_x[0]
np.savetxt("test1.txt", data_test_x[0])
pred1 = clf.predict(data_test_x[0].reshape(1,-1))
print pred1