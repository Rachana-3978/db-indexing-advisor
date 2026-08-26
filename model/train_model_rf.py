import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

data = pd.read_csv('data/real_query_data.csv')

X = data.drop('label', axis=1)
y = data['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
model.fit(X_train, y_train)

predictions = model.predict(X_test)
print(f"Random Forest Accuracy: {accuracy_score(y_test, predictions):.2f}")

joblib.dump(model, 'model/indexing_model_rf.pkl')
print("Model saved as model/indexing_model_rf.pkl")