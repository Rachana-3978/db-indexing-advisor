import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import numpy as np

data = pd.read_csv('data/real_query_data.csv')

print(data.head())

# Step 2: Train-test split
X = data.drop('label', axis=1)
y = data['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 3: Model train karo
model = DecisionTreeClassifier(max_depth=5, random_state=42)
model.fit(X_train, y_train)

# Step 4: Accuracy check
predictions = model.predict(X_test)
print(f"\nAccuracy: {accuracy_score(y_test, predictions):.2f}")

# Step 5: Model save karo
joblib.dump(model, 'model/indexing_model.pkl')
print("\nModel saved as model/indexing_model.pkl")