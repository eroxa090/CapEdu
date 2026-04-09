class Client:
    def __init__(self, name, balance, pin):
        self.name = name
        self.balance = balance
        self.pin = pin

    def verify_pin(self):
        entered_pin = input("Введите PIN: ")
        return entered_pin == self.pin

    def update_name(self):
        if not self.verify_pin():
            print("❌ Неверный PIN, изменение данных невозможно.")
            return
        new_name = input("Введите новое имя: ")
        self.name = new_name
        print(f"✅ Имя успешно изменено на {self.name}")

    def deposit(self, amount):
        if not self.verify_pin():
            print("❌ Неверный PIN, операция отменена")
            return

        self.balance += amount
        print(f"✅ Пополнено: {amount}. Текущий баланс: {self.balance}")

    def withdraw(self, amount):
        if not self.verify_pin():
            print("❌ Неверный PIN, операция отменена")
            return

        if amount > 500:
            print("❗ Нельзя снять более 500 за одну операцию.")
            return

        if amount > self.balance:
            print("❗ Недостаточно средств.")
            return

        self.balance -= amount
        print(f"✅ Снято: {amount}. Остаток: {self.balance}")

client1 = Client("Алия", 1200, "1234")

client1.update_name()
client1.deposit(300)
client1.withdraw(600)  
client1.withdraw(400)  