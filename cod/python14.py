
try:
    with open("example.txt","w",encoding="utf-8") as file:
        file.write("первая строка\n")
        file.write("вторая строка\n")
        file.write("третья строка\n")

    print("file created")

    with open("example.txt","r",encoding="utf-8") as file:
         content = file.read()
         print("Содержимое файла:")
         print(content)
         

except FileNotFoundError:
    print("Ошибка: файл не найден!")
except Exception as e:
    print("Произошла ошибка:",e)