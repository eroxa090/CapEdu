import time 
for i in range(10,0,-1):
    print(i)
    time.sleep(1)



def stopwatch():
    players = {"Игрок 1": 0, "Игрок 2": 0} 
    current_player = None
    start_time = None

    print("Секундомер для двух игроков")
    print("Команды:")
    print("  1 — переключиться на Игрока 1")
    print("  2 — переключиться на Игрока 2")
    print("  e — завершить и показать результаты")

    while True:
        command = input("Введите команду: ").strip()

        if command == "e":
            if current_player is not None:
                players[current_player] += time.time() - start_time
            break

        elif command in ["1", "2"]:
            player = "Игрок 1" if command == "1" else "Игрок 2"

            if current_player is not None:
                players[current_player] += time.time() - start_time

            current_player = player
            start_time = time.time()
            print(f"Теперь ходит {current_player}")

        else:
            print("Неверная команда, используйте 1, 2 или e"
            ".")

    print("\nРезультаты:")
    for p, t in players.items():
        print(f"{p}: {t:.2f} секунд")

stopwatch()