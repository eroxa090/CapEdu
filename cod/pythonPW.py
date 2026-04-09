import random

def generate_password(length):
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    digits = "0123456789"
    specials = "!@#$%^&*"
    all_chars = letters + digits + specials

    password = ""
    for i in range (length):
        password += random.choice(all_chars)
    return password

def check_password_strength(password):
    has_letter = False
    has_digit = False
    has_special = False 

    for ch in password:
        if ch.isalpha():
            has_letter = True
        elif ch.isdigit():
            has_digit = True
        elif ch in "!@#$%^&*":
            has_special = True
    
    if len(password) < 8 or (has_letter and not has_digit and not has_special):
        return"Слабый"
    elif len(password) >= 8 and has_letter and has_digit and not has_special:
        return "Средний"
    elif len(password) >= 10 and has_letter and has_digit and has_special:
        return "Сильный"
    else:
        return "Неопределённый"

def main():
    action = input("Введите 'generate' для генерации или 'check' для проверки: ")

    if action == "generate":
        length = int(input("Введите длину пароля: "))
        password = generate_password(length)
        print("Сгенерированный пароль:", password)

    elif action == "check":
        password = input("Введите пароль для проверки: ")
        strength = check_password_strength(password)
        print("Сила пароля:", strength)

    else:
        print("Неверная команда. Используйте 'generate' или 'check'.")

main()
    