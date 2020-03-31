import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
import pickle


dataset = pd.read_excel('basedata.xlsx', dtype={'TxnRefNo': str})

# Added TAT column in minutes
dataset['TAT'] = (np.ceil((pd.to_datetime(dataset['Credited']) - 
                            pd.to_datetime(dataset['InstrumentIssued']))
                                .dt.total_seconds()/60)*1).astype(int)
# Weekday field added
dataset['WKday'] = dataset['InstrumentIssued'].dt.day_name()

# Mode field added
dataset["Mode"]=dataset['DraweeBankBranchCode'].str.rfind('FL')
dataset["Mode"]=dataset["Mode"].replace([-1],'TT')
dataset["Mode"]=dataset["Mode"].replace([6],'Flash')

# Target field added
dataset["Target"]=dataset["Mode"]
dataset["Target"]=dataset["Target"].replace('Flash',10)
dataset["Target"]=dataset["Target"].replace('TT',2880)

# Success field added
dataset["Success"]=dataset["TAT"]<=dataset["Target"]
dataset["Success"]=dataset["Success"].replace(True,1)
dataset["Success"]=dataset["Success"].replace(False,0)

# Mode changed to numeric
dataset["Mode"]=dataset["Mode"].replace('Flash',1)
dataset["Mode"]=dataset["Mode"].replace('TT',0)

# WKday changed to numeric
dataset['WKday'] = dataset['InstrumentIssued'].dt.dayofweek
dataset['Hour'] = dataset['InstrumentIssued'].dt.hour

# BeneficiaryBankCode changed to numeric
summary= dataset.groupby(['BeneficiaryBankCode']).size().reset_index()
summary.describe
summary.dtypes
dataset["BCODE"]=dataset["BeneficiaryBankCode"]
for index, row in summary.iterrows():
    dataset["BCODE"]=dataset["BCODE"].replace(row["BeneficiaryBankCode"],row.name)

# Payin changed to numeric
summary= dataset.groupby(['PayinCcyCode']).size().reset_index()
summary.describe
summary.dtypes
dataset["PAYIN"]=dataset["PayinCcyCode"]
for index, row in summary.iterrows():
    dataset["PAYIN"]=dataset["PAYIN"].replace(row["PayinCcyCode"],row.name)

# Payout changed to numeric
summary= dataset.groupby(['PayoutCcyCode']).size().reset_index()
summary.describe
summary.dtypes
dataset["PAYOUT"]=dataset["PayoutCcyCode"]
for index, row in summary.iterrows():
    dataset["PAYOUT"]=dataset["PAYOUT"].replace(row["PayoutCcyCode"],row.name)
summary.to_csv('PAYOUT.csv')

# DraweeBankBranchCode changed to numeric
summary= dataset.groupby(['DraweeBankBranchCode']).size().reset_index()
summary.describe
summary.dtypes
dataset["DRC"]=dataset["DraweeBankBranchCode"]
for index, row in summary.iterrows():
    dataset["DRC"]=dataset["DRC"].replace(row["DraweeBankBranchCode"],row.name)
summary.to_csv('DRC.csv')

    
sns.set_style('whitegrid')
sns.countplot(x="Mode",hue='Success',data=dataset)
sns.countplot(x="PayoutCcyCode",hue='Success',data=dataset)
sns.countplot(x="PayinCcyCode",hue='Success',data=dataset)

'''
dataset.to_csv('Customerdata13.csv')

dataset.columns
dataset.dtypes
dataset.info()
dataset.head()

data =dataset['PayinAmount']
bins = np.linspace(0, 1000, 5000,10000)
digitized = np.digitize(data, bins)
bin_means = [data[digitized == i].mean() for i in range(1, len(bins))]
dataset["PayinAmountmean"]=bin_means

for index, bin_means in summary.iterrows():
    dataset["PayinAmountmean"]=dataset["PayinAmountmean"].replace(row["PayinAmountmean"],bin_means)

dataset["PayinAmountmean"] = pd.cut(x=dataset['PayinAmount'], bins=[1,500,1000, 10000, 25000, 50000,100000,1000000])
intervel=(dataset['PayinAmount'].max()-dataset['PayinAmount'].min())/dataset['PayinAmount'].count()
intervel
dataset['PayinAmount'].mean()
pd.value_counts(pd.cut(dataset['PayinAmount'],bins=intervel))
'''

# heatmap
corrmatrix=dataset.corr()
plt.subplots(figsize=(10,10))
sns.heatmap(corrmatrix,vmin=0,vmax=1,cmap='YlGnBu',annot=True,linewidth=0.1)


dataset.to_csv('DataOut.csv')

x=dataset.iloc[:,[9,10,13,17]].values
y=dataset.iloc[:,12].values
print(x)
#spitting the dataset into training set and test set
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x, y, test_size=0.30, random_state=0)

'''
#Feature scaling
from sklearn.preprocessing import StandardScaler
sc=StandardScaler()
x_train=sc.fit_transform(x_train)
x_test=sc.fit_transform(x_test)
'''

#Logistic regression to the traininf set\
from sklearn.linear_model import LogisticRegression
classifier=LogisticRegression(random_state=0)
classifier.fit(x_train,y_train)

y_pred=classifier.predict(x_test)
y_pred
x_test


#making the confusion matric(testing how accuracy of the model)

from sklearn.metrics import confusion_matrix
cm=confusion_matrix(y_test,y_pred)
cm
sd=cm[0,0]+cm[0,1]+cm[1,0]+cm[1,1]
so=cm[0,0]+cm[1,1]
print(so/sd)

from sklearn.metrics import f1_score
f1_score(y_test,y_pred)

pickle.dump(classifier,open('model.pkl','wb'))
model=pickle.load(open('model.pkl','rb'))


#x=[[-0.52739497, -1.17298471, -0.98021771, -0.49938542, -0.63230812]]
#print(model.predict(x))
