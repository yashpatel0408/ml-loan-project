import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report
import joblib

df = pd.read_csv("data/loan.csv")

df = df.drop("Loan_ID", axis=1, errors="ignore")

df = df.dropna()

df["Income_Loan_Ratio"] = df["ApplicantIncome"] / df["LoanAmount"]

df["Loan_Status"] = df["Loan_Status"].map({"Y": 1, "N": 0})

df = pd.get_dummies(df, drop_first=True)

X = df.drop("Loan_Status", axis=1)
y = df["Loan_Status"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("model", RandomForestClassifier(n_estimators=100, random_state=42))
])

pipe.fit(X_train, y_train)

y_pred = pipe.predict(X_test)
print("Accuracy:", round(accuracy_score(y_test, y_pred), 4))
print(classification_report(y_test, y_pred))

joblib.dump(pipe, "models/loan_model.pkl")
print("Model saved successfully")