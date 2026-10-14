# Lab 5: Static Code Analysis — Issues and Fixes

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Insecure FTP communication (B402, B321) | High — Security | 3, 68–71 (original) | FTP does not encrypt credentials or transferred data. | Removed the FTP implementation because no secure transfer endpoint was configured. |
| Unsafe deserialization (B302) | Medium — Security | 64 (original) | `marshal.loads()` was used to deserialize application records. | Replaced binary serialization with JSON storage. |
| Mutable default argument (W0102) | Code quality | 20 (original) | `history=[]` could be shared between function calls. | Removed the mutable default argument from the eligibility function. |
| Hardcoded password (B107) | Low — Security | 67 (original) | An FTP password was embedded in the function definition. | Removed the FTP login implementation and hardcoded password. |
| Insecure random generator (B311) | Low — Security | 51 (original) | `random.randint()` was used to generate application IDs. | Replaced it with the `secrets` module. |
| Unclosed files (R1732) | Code quality | 56, 63, 70 (original) | Files were opened without context managers. | Used `with open(...)` for JSON file operations. |
| Incorrect EMI calculation | Logic bug | 14–18 (original) | The annual interest rate was not converted to a monthly decimal rate. | Corrected the EMI formula and standardized interest rates as decimals. |
| Invalid loan type accepted | Logic bug | 20–31 (original) | An early approval condition could approve an unsupported loan type. | Validated loan type before other approval conditions. |
| Naming and documentation issues | Style | Multiple (original) | Several functions lacked docstrings and used non-standard names. | Added docstrings and converted function names to snake_case. |
| Formatting violations | Style | Multiple (original) | Long lines, missing blank lines, and unused code were reported. | Reformatted the code and removed unused imports and unnecessary f-strings. |

## Verification

- Pylint final score: 10.00/10
- Bandit final report: 0 issues
- Flake8 final report: 0 violations

The final program was run successfully after the changes. Secure bureau uploads and email notifications remain unconfigured and are not performed by the cleaned-up implementation.
