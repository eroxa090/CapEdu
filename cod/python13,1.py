print("=== Задание 1 ===")
my_list = [10, 20, 30, 40, 50]
print("Исходный список:", my_list)
my_list[2] = 99
print("Изменённый список:", my_list)
print()

print("=== Задание 2 ===")
my_tuple = (1, 2, 3, 4)
print("Исходный кортеж:", my_tuple)
try:
    my_tuple[1] = 99
except TypeError as e:
    print("Ошибка при изменении:", e)
print()

print("=== Задание 3 ===")
my_list2 = [5, 6, 7]
my_tuple2 = tuple(my_list2)
print("Кортеж из списка:", my_tuple2)
new_list = list(my_tuple2)
print("Список обратно из кортежа:", new_list)