import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import numpy as np

data = pd.read_csv('data/real_query_data.csv')

print(data.head())

X = data.drop('label', axis=1)
y = data['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = DecisionTreeClassifier(max_depth=5, random_state=42)
model.fit(X_train, y_train)

predictions = model.predict(X_test)
print(f"\nAccuracy: {accuracy_score(y_test, predictions):.2f}")

joblib.dump(model, 'model/indexing_model.pkl')
print("\nModel saved as model/indexing_model.pkl")