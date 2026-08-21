import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import numpy as np

# Step 1: Synthetic data banate hain (baad mein real query logs se replace karenge)
np.random.seed(42)
n_samples = 500

data = pd.DataFrame({
    'is_join_column': np.random.randint(0, 2, n_samples),
    'selectivity_ratio': np.round(np.random.uniform(0, 1, n_samples), 2),
    'table_row_count': np.random.randint(100, 1000000, n_samples),
    'scan_type_frequency': np.random.randint(0, 100, n_samples),
})

# Simple rule-based label generation (fake logic — real data se train hoga baad mein)
data['label'] = (
    (data['is_join_column'] == 1) |
    (data['selectivity_ratio'] < 0.3) & (data['scan_type_frequency'] > 50)
).astype(int)

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