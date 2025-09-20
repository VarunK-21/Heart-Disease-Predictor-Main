import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import pickle
import os

# Step 1: Load the dataset
df = pd.read_csv('dataset/heart_disease.csv')

# Step 2: Handle missing values and encode non-numeric columns
df = df.dropna()  # Drop rows with missing values
for col in df.columns:
    if df[col].dtype == 'object':
        print(f"Encoding non-numeric column: {col}")
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))

# Step 3: Print value counts for the target column
print("Target column value counts:\n", df['target'].value_counts())

# Step 4: Define features and target
X = df.drop('target', axis=1)
y = df['target']

# Step 5: Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Step 6: Feature scaling
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Step 7: Train the models
# Logistic Regression
lr_model = LogisticRegression(max_iter=1000)
lr_model.fit(X_train, y_train)
lr_pred = lr_model.predict(X_test)
lr_accuracy = accuracy_score(y_test, lr_pred)

# Random Forest
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
rf_pred = rf_model.predict(X_test)
rf_accuracy = accuracy_score(y_test, rf_pred)

# Support Vector Machine
svm_model = SVC(kernel='linear', probability=True, random_state=42)
svm_model.fit(X_train, y_train)
svm_pred = svm_model.predict(X_test)
svm_accuracy = accuracy_score(y_test, svm_pred)

# Step 8: Print accuracies
print("Logistic Regression Accuracy:", lr_accuracy)
print("Random Forest Accuracy:", rf_accuracy)
print("SVM Accuracy:", svm_accuracy)

# Step 9: Save models
if not os.path.exists('backend/models'):
    os.makedirs('backend/models')

pickle.dump(lr_model, open('backend/models/logistic_model.pkl', 'wb'))
pickle.dump(rf_model, open('backend/models/random_forest.pkl', 'wb'))
pickle.dump(svm_model, open('backend/models/svm_model.pkl', 'wb'))
pickle.dump(scaler, open('backend/models/scaler.pkl', 'wb'))

print("✅ Models saved successfully!")
