"""
Course Registration Parser Module
Fixed and hardened implementation with comprehensive defensive input validation.
Handles malformed, unexpected, edge-case, and fuzz-generated inputs safely without crashing.
"""

# Valid academic student statuses
VALID_STATUSES = {"regular", "probation", "honors", "backlog", "waitlist", "audit"}


def format_course_code(code):
    """
    Formats a course code string into standard uppercase concatenated format (e.g. 'cs 301' -> 'CS301').

    Input Contract & Validation Rules:
    - Must be a non-empty string.
    - Must consist of exactly two whitespace-separated components: department and course number.
    - Department must contain only alphabetic characters (2 to 6 characters, e.g., 'CS', 'MATH').
    - Course number must be alphanumeric, contain at least one numeric digit, and be 1 to 10 characters long.
    - Returns formatted code as uppercase 'DEPTNUMBER' string on success.
    - Returns None if input is None, invalid type, empty, malformed, or has extra/missing components.
    """
    if not isinstance(code, str):
        return None

    cleaned = code.strip()
    if not cleaned:
        return None

    parts = cleaned.split()
    if len(parts) != 2:
        return None

    dept, number = parts

    # Validate department: alphabetic, 2 to 6 characters
    if not (dept.isalpha() and 2 <= len(dept) <= 6):
        return None

    # Validate course number: alphanumeric, must contain at least one digit, max 10 characters
    if not (number.isalnum() and any(c.isdigit() for c in number) and len(number) <= 10):
        return None

    return f"{dept.upper()}{number.upper()}"


def total_credits(text):
    """
    Calculates the total credits from a comma-separated string of course credit values.

    Input Contract & Validation Rules:
    - Must be a string (returns 0 if None, empty, whitespace, or invalid type).
    - Splits string by comma delimiters into credit tokens.
    - Each token is stripped and validated as an integer:
      - Valid credit range is 0 to 30 credits per course (0 allowed for audit/non-credit courses).
      - Negative values (< 0) are invalid and rejected.
      - Decimal numbers (e.g. 3.5), alphabetic strings, and special characters are rejected.
      - Missing/empty entries (e.g. ',,') are skipped.
      - Excessively large integers (> 30) are rejected to prevent overflow and DoS attacks.
    - Returns the integer sum of all valid course credits.
    """
    if not isinstance(text, str):
        return 0

    cleaned = text.strip()
    if not cleaned:
        return 0

    total = 0
    for item in cleaned.split(','):
        token = item.strip()
        if not token:
            continue

        try:
            val = int(token)
        except (ValueError, OverflowError):
            continue

        # Validation rule: credit must be a non-negative integer within reasonable academic limits (0-30)
        if 0 <= val <= 30:
            total += val

    return total


def parse_student_record(line):
    """
    Parses a single student record formatted as 'SRN|name|status' into a dictionary.

    Input Contract & Validation Rules:
    - Must be a string containing exactly two pipe '|' delimiters (exactly three non-empty fields).
    - Field 1 (SRN): Stripped and normalized to uppercase. Must be alphanumeric (plus optional hyphens/underscores),
      between 3 and 30 characters long, and contain both letters and digits (e.g., 'PES1UG24CS062').
    - Field 2 (Name): Stripped to preserve student's actual casing and internal spacing. Must contain at least
      one alphabetic character, length between 1 and 100 characters.
    - Field 3 (Status): Stripped and normalized to lowercase. Must be a valid student status
      ('regular', 'probation', 'honors', 'backlog', 'waitlist', 'audit') or non-empty alphabetic string.
    - Returns a dictionary: {'srn': SRN, 'name': Name, 'status': Status}.
    - Returns None if input is None, invalid type, missing fields, contains extra delimiters, or has invalid field values.
    """
    if not isinstance(line, str):
        return None

    if '|' not in line:
        return None

    parts = line.split('|')
    if len(parts) != 3:
        return None

    srn_raw = parts[0].strip()
    name_raw = parts[1].strip()
    status_raw = parts[2].strip()

    # Reject if any required field is empty
    if not srn_raw or not name_raw or not status_raw:
        return None

    srn = srn_raw.upper()
    # SRN validation: length 3-30, alphanumeric with optional hyphens/underscores, must contain letters and digits
    if not (3 <= len(srn) <= 30 and all(c.isalnum() or c in "-_" for c in srn)
            and any(c.isalpha() for c in srn) and any(c.isdigit() for c in srn)):
        return None

    name = name_raw
    # Name validation: length 1-100, must contain at least one alphabetic character
    if not (1 <= len(name) <= 100 and any(c.isalpha() for c in name)):
        return None

    status = status_raw.lower()
    # Status validation: must be an alphabetic academic status
    if not (status.isalpha() and (status in VALID_STATUSES or len(status) <= 20)):
        return None

    return {
        "srn": srn,
        "name": name,
        "status": status
    }


def main():
    print("==== Running format_course_code ====")
    value = input("Enter a course code as DEPT NUMBER (e.g. cs 301): ")
    print("Formatted course code:", format_course_code(value))

    print("\n==== Running total_credits ====")
    value = input("Enter course credits separated by commas (e.g. 4,3,4): ")
    print("Total credits:", total_credits(value))

    print("\n==== Running parse_student_record ====")
    value = input("Enter a student record as SRN|name|status (e.g. pes1ug23cs001|Asha|regular): ")
    print("Student record:", parse_student_record(value))


if __name__ == "__main__":
    main()
