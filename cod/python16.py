import re
text="""
email:user_1@mail.com, info.company@gmail.com, support@site.org
tel:123-456-7890, 098-765-4321
data:18.10.2025, следующая - 19.10.2025.
"""
emails=re.findall(r"[\w.+-]+@[\w.-]+\.\w+", text)
phones=re.findall(r"\b\d{3}-\d{3}-\d{4}\b", text)
new_text=re.sub(r"(\d{2})\.(\d{2})\.(\d{4})", r"\3.\2.\1", text)

print("email-адреса:")
print(emails)
print("\n телефоны:")
print(phones)
print("\n замененные даты:")
print(new_text)