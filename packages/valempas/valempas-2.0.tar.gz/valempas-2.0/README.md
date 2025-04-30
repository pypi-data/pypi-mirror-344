# valempas

Library sederhana untuk validasi format email dan password (minimal 8 karakter, kombinasi huruf besar, kecil, angka, dan simbol).

## Contoh Penggunaan

```python
from valempas import is_valid_email, is_valid_password

print(is_valid_email("user@example.com"))         # True
print(is_valid_password("Passw0rd!"))             # True
