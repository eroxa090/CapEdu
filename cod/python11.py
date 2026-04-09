import random 

участники = ["Алихан","Алишер","Илон Маск","Цукерберг"]
команды = ["команда1","команда2"]

for участник in участники:
    команда = random.choice(команды)
    print(f"{участник} попал в {команда}")


    варианты=["Уррен Баффет","Илон Маск","Цукерберг"]
    выбор = random.choice(варианты)
    print(f"winner{выбор}")

import random
number = random.randint(1, 100)

guess = int(input("Угадайте число от 1 до 100: "))

while guess != number:
    if guess < number:
        print("Загаданное число больше")
    else:
        print("Загаданное число меньше")
    guess = int(input("Попробуйте снова: "))

print("Поздравляем, вы угадали!")