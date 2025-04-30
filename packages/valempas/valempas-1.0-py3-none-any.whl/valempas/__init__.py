import re

def is_valid_email(email):
    """
    Validasi format email standar.
    """
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def is_valid_password(password):
    """
    Validasi password:
    - Minimal 8 karakter
    - Kombinasi huruf besar, huruf kecil, angka, dan simbol
    """
    if len(password) < 8:
        return False
    upper_char = re.search(r'[A-Z]', password)
    lower_char = re.search(r'[a-z]', password)
    has_digit = re.search(r'[0-9]', password)
    special_char = re.search(r'[\W_]', password)
    return all([upper_char, lower_char, has_digit, special_char])
