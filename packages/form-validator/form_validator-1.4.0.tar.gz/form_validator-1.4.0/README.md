

# Form Validator

A simple Python package for validating forms. It supports:

- ✅ Email validation
- ✅ Password strength check
- ✅ Mobile number validation
- ✅ Age validation (18+)

---

## Installation

```bash
pip install form-validator
```

---

## Usage

First, import the functions you need:

```python
from form_validator import validate_email, validate_password, validate_mobile, validate_age
```

---

## Examples

### 1. Email Validation

```python
email = "example@gmail.com"
if validate_email(email):
    print("✅ Valid Email Address")
else:
    print("❌ Invalid Email Address")
```

---

### 2. Password Strength Check

```python
password = "StrongPass123!"
if validate_password(password):
    print("✅ Strong Password")
else:
    print("❌ Weak Password. Try adding letters, numbers, and special characters.")
```

---

### 3. Mobile Number Validation

```python
mobile = "9876543210"
if validate_mobile(mobile):
    print("✅ Valid Mobile Number")
else:
    print("❌ Invalid Mobile Number")
```

---

### 4. Age Validation (18+ Check)

```python
age = 20
if validate_age(age):
    print("✅ Age is 18 or above")
else:
    print("❌ Must be at least 18 years old")
```

---

## Why use Form Validator?

- 🚀 Lightweight and fast
- 🔥 No external heavy dependencies
- 📦 Easy to plug into any Python project
- 🛡️ Helps prevent invalid user inputs

---

## License

This project is licensed under the [MIT License](LICENSE).

---

Would you also like me to create a **badge version** like:

```
[![PyPI version](https://badge.fury.io/py/form-validator.svg)](https://pypi.org/project/form-validator/)
```

to make your README even more professional? 🚀🎯  
