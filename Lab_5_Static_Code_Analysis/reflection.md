# Lab 5: Static Code Analysis — Reflection

## 1. What is static code analysis?

Static code analysis examines source code without executing it to identify potential bugs, security vulnerabilities, and style violations. It helps developers detect problems early and improve maintainability.

## 2. What are the purposes of Pylint, Bandit, and Flake8?

Pylint checks Python code quality, naming, programming practices, and potential logical issues. Bandit identifies potentially insecure coding patterns. Flake8 checks formatting and compliance with Python style conventions.

## 3. What issues did you identify and fix?

The original program had incorrect EMI calculations, a mutable default argument, an invalid loan-type approval path, insecure FTP usage, unsafe deserialization, a hardcoded password, and code-formatting problems. I corrected the EMI calculation and eligibility checks, replaced `marshal` storage with JSON, removed the FTP implementation, used `secrets` for application IDs, and improved file handling and code style.

## 4. What did you learn from this lab?

I learned that a program can run successfully while still containing logical errors, security risks, and maintainability problems. Using multiple static analysis tools helps identify different categories of issues. Rerunning the tools after fixing the code provides evidence that the reported findings have been addressed.
