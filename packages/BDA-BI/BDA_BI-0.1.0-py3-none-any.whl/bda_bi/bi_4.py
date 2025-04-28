print("""# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Step 1: Load the Titanic dataset
df = pd.read_csv('titanic.csv')  # Make sure 'titanic.csv' is in the same folder or give full path

# Step 2: Preprocessing
# Select relevant features and target
# (Assuming 'Age', 'Sex', 'Fare', 'Pclass', and 'Survived' columns are available)

# Handle missing values (example: fill missing Age and Fare with median)
df['Age'].fillna(df['Age'].median(), inplace=True)
df['Fare'].fillna(df['Fare'].median(), inplace=True)

# Convert 'Sex' into numerical
df['Sex'] = df['Sex'].map({'male': 0, 'female': 1})

# Drop rows where 'Survived' is missing (if any)
df = df.dropna(subset=['Survived'])

# Step 3: Define features (X) and label (y)
X = df[['Age', 'Sex', 'Fare', 'Pclass']]
y = df['Survived']

# Step 4: Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Step 5: Train Logistic Regression model
model = LogisticRegression(max_iter=1000)  # Increased max_iter in case convergence warning
model.fit(X_train, y_train)

# Step 6: Predict on test data
y_pred = model.predict(X_test)

# Step 7: Evaluate the model
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))""")

