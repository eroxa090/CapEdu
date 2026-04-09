class Person:
    def __init__(self, name, age):
        self.name = name     
        self.age = age       

    def introduce(self):
        print(f"Привет! Меня зовут {self.name}, мне {self.age} лет.")

    def birthday(self):
        self.age += 1
        print(f"{self.name} отметил день рождения! Теперь ему {self.age} лет.")
        

person1 = Person("Ramos", 15)
person2 = Person("Ilon", 16)

person1.introduce()
person2.introduce()

person1.birthday()
person2.birthday()