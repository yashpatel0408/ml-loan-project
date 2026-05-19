import pandas as pd
import joblib

pipe = joblib.load("models/loan_model.pkl")

applicant_income = 50000
loan_amount = 12000

new_customer = {
    "ApplicantIncome": applicant_income,
    "LoanAmount": loan_amount,
    "Income_Loan_Ratio": applicant_income / loan_amount,
    "Credit_History": 1,
    "Gender_Male": 1,
    "Married_Yes": 1,
    "Education_Not Graduate": 0,
    "Self_Employed_Yes": 0
}

new_df = pd.DataFrame([new_customer])
new_df = new_df.reindex(columns=pipe.feature_names_in_, fill_value=0)

prob = pipe.predict_proba(new_df)[0][1]
decision = "APPROVED" if prob >= 0.5 else "REJECTED"

print("Approval Probability:", round(prob, 2))
print("Decision:", decision)