
"""Loan eligibility, EMI calculation, and application management."""

import json
import os
import secrets
from datetime import datetime

# Global loan book
applications = {}
MAX_FOIR = 0.5


def calculate_emi(principal, annual_rate, years):
    """Calculate monthly EMI using an annual decimal interest rate."""
    if principal <= 0 or years <= 0 or annual_rate < 0:
        raise ValueError("Invalid principal, interest rate, or loan duration.")

    monthly_rate = annual_rate / 12
    months = years * 12

    if monthly_rate == 0:
        return principal / months

    factor = (1 + monthly_rate) ** months
    return principal * monthly_rate * factor / (factor - 1)


def check_eligibility(age, income, credit_score, existing_emi, loan_type):
    """Check basic loan eligibility using the supplied applicant details."""
    valid_loan_types = {"home", "car", "personal"}

    if age < 21 or age > 60:
        return False

    if loan_type not in valid_loan_types:
        return False

    if income <= 0 or existing_emi < 0:
        return False

    if credit_score > 750:
        return True

    if existing_emi / income > MAX_FOIR:
        return False

    return income > 25000


def max_loan_amount(income, existing_emi, annual_rate, years):
    """Estimate the maximum loan from monthly repayment capacity."""
    if income <= 0 or existing_emi < 0 or years <= 0:
        raise ValueError("Invalid income, existing EMI, or loan duration.")

    if annual_rate < 0:
        raise ValueError("Interest rate cannot be negative.")

    available_payment = income * MAX_FOIR - existing_emi

    if available_payment <= 0:
        return 0.0

    monthly_rate = annual_rate / 12
    months = years * 12

    if monthly_rate == 0:
        return available_payment * months

    factor = (1 + monthly_rate) ** months
    return available_payment * (factor - 1) / (
        monthly_rate * factor
    )


def amortisation_schedule(principal, annual_rate, years):
    """Return monthly interest and outstanding balance for each period."""
    emi = calculate_emi(principal, annual_rate, years)
    monthly_rate = annual_rate / 12
    balance = principal
    rows = []

    for month in range(1, years * 12 + 1):
        interest = balance * monthly_rate
        principal_paid = emi - interest
        balance = max(0.0, balance - principal_paid)

        rows.append(
            (month, round(interest, 2), round(balance, 2))
        )

    return rows


def application_id():
    """Generate a random loan application identifier."""
    return f"LN-{secrets.token_hex(6).upper()}"


def save_application(name, amount, file="loans.json"):
    """Save an application record in JSON format."""
    if not name.strip() or amount <= 0:
        raise ValueError("Applicant name and amount must be valid.")

    app_id = application_id()
    applications[app_id] = {
        "name": name,
        "amount": amount,
        "date": datetime.now().isoformat(timespec="seconds"),
    }

    with open(file, "w", encoding="utf-8") as output_file:
        json.dump(applications, output_file, indent=4)

    return app_id


def load_applications(file="loans.json"):
    """Load application records from a JSON file."""
    try:
        with open(file, "r", encoding="utf-8") as input_file:
            records = json.load(input_file)

        if not isinstance(records, dict):
            raise ValueError("Application data must be a JSON object.")

        applications.clear()
        applications.update(records)

    except FileNotFoundError:
        applications.clear()


def upload_to_bureau(report_path):
    """Report that secure bureau upload is not configured."""
    if not os.path.isfile(report_path):
        raise FileNotFoundError(report_path)

    print("Bureau upload skipped: secure transfer is not configured.")


def notify_applicant(email, status):
    """Report that email notification is not configured."""
    if "@" not in email:
        raise ValueError("A valid email address is required.")

    print(
        f"Email notification is not configured for status: {status}"
    )


def interest_saved(principal, annual_rate, years, prepayment):
    """Estimate interest reduction from a principal prepayment."""
    if prepayment < 0 or prepayment >= principal:
        raise ValueError(
            "Prepayment must be non-negative and less than principal."
        )

    original_total = (
        calculate_emi(principal, annual_rate, years) * years * 12
    )

    reduced_total = (
        calculate_emi(
            principal - prepayment, annual_rate, years
        ) * years * 12
    )

    return original_total - reduced_total


def risk_band(credit_score):
    """Assign a risk band based on the credit score."""
    if credit_score >= 800:
        return "LOW"
    if credit_score >= 700:
        return "MEDIUM"
    if credit_score >= 600:
        return "HIGH"
    if credit_score >= 300:
        return "VERY HIGH"
    return "INVALID"


def main():
    """Run the loan calculator demonstration."""
    print(
        "EMI for 5L at 9% for 5 years:",
        round(calculate_emi(500000, 0.09, 5), 2),
    )

    print(
        "Eligible (score 760):",
        check_eligibility(35, 15000, 760, 12000, "personal"),
    )

    print(
        "Eligible (unknown loan type):",
        check_eligibility(30, 80000, 650, 0, "crypto"),
    )

    print(
        "Maximum loan for income 40000:",
        round(max_loan_amount(40000, 5000, 0.09, 5), 2),
    )

    print(
        "Last schedule row:",
        amortisation_schedule(100000, 0.12, 1)[-1],
    )

    print("Risk band for 950:", risk_band(950))

    print(
        "Interest saved by prepaying 50000:",
        round(
            interest_saved(500000, 0.09, 5, 50000),
            2,
        ),
    )

    print("Saved as:", save_application("Anil", 500000))
    load_applications()
    print("Applications on file:", len(applications))


if __name__ == "__main__":
    main()
