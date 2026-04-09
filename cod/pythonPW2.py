import re
import time
import random
import threading
import sys
import queue
from dataclasses import dataclass, field
from typing import List, Dict, Optional


def timed_input(prompt: str, timeout: float) -> Optional[str]:
    """
    Запрос ввода у пользователя с таймаутом в секундах.
    Если пользователь не ввёл за timeout, возвращает None.
    Работает кроссплатформенно (использует поток).
    Замечание: поток ввода помечен daemon=True, поэтому при выходе он не будет блокировать программу.
    """
    q = queue.Queue()

    def input_thread():
        try:
            s = input(prompt)
            q.put(s)
        except Exception:
            q.put(None)

    t = threading.Thread(target=input_thread, daemon=True)
    t.start()

    try:
        answer = q.get(timeout=timeout)
        return answer
    except queue.Empty:
        return None


@dataclass
class Card:
    question: str
    answer: str

@dataclass
class Note:
    title: str
    content: str

@dataclass
class User:
    username: str
    password: str  
    cards: List[Card] = field(default_factory=list)
    notes: List[Note] = field(default_factory=list)

class StudyApp:
    def __init__(self):
       
        self.users: Dict[str, User] = {}
        self.current_user: Optional[User] = None

    def register(self):
        print("\n--- Регистрация ---")
        username = input("Имя пользователя: ").strip()
        if username == "":
            print("Имя пользователя не может быть пустым.")
            return
        if username in self.users:
            print("Пользователь с таким именем уже зарегистрирован.")
            return

        password = input("Пароль (латинские буквы и цифры, минимум 5 символов): ").strip()
        if not self.validate_password(password):
            print("Неправильный формат пароля.")
            return

       
        user = User(username=username, password=password)
        self.users[username] = user
        print(f"Пользователь '{username}' успешно зарегистрирован.")

    def login(self):
        print("\n--- Вход ---")
        username = input("Имя пользователя: ").strip()
        password = input("Пароль: ").strip()
        user = self.users.get(username)
        if user and user.password == password:
            self.current_user = user
            print(f"Добро пожаловать, {username}!")
        else:
            print("Неправильное имя пользователя или пароль.")

    @staticmethod
    def validate_password(pw: str) -> bool:
    
        return bool(re.fullmatch(r"[A-Za-z0-9]{5,}", pw))

   
    def add_card(self):
        if not self._require_login(): return
        q = input("Вопрос: ").strip()
        a = input("Ответ: ").strip()
        if q == "" or a == "":
            print("Вопрос и ответ не могут быть пустыми.")
            return
        self.current_user.cards.append(Card(question=q, answer=a))
        print("Карточка добавлена.")

    def show_random_card(self):
        if not self._require_login(): return
        if not self.current_user.cards:
            print("У вас пока нет карточек.")
            return
        card = random.choice(self.current_user.cards)
        print("\n--- Случайная карточка ---")
        print("Вопрос:", card.question)
        input("Нажмите Enter, чтобы увидеть ответ...")
        print("Ответ:", card.answer)

  
    def quiz(self):
        if not self._require_login(): return
        cards = self.current_user.cards.copy()
        if not cards:
            print("Добавьте карточки перед запуском викторины.")
            return

        num_questions = min(len(cards), int(input("Сколько вопросов в викторине? (по умолчанию все): ") or len(cards)))
        random.shuffle(cards)
        cards = cards[:num_questions]
        correct = 0

        print("\nВикторина начинается! У вас 30 секунд на каждый ответ.")
        for i, card in enumerate(cards, start=1):
            print(f"\nВопрос {i}/{num_questions}: {card.question}")
            start = time.time()  
            remaining = 30.0
            answer = timed_input("> Ваш ответ (30s): ", timeout=remaining)
            elapsed = time.time() - start
            if answer is None:
                print("Время вышло! Переход к следующему вопросу.")
                print("Правильный ответ:", card.answer)
                continue
           
            if answer.strip().lower() == card.answer.strip().lower():
                print("Правильно!")
                correct += 1
            else:
                print("Неправильно.")
                print("Правильный ответ:", card.answer)

        print(f"\nВикторина окончена. Правильных ответов: {correct}/{num_questions}")

    def notes_menu(self):
        if not self._require_login(): return
        while True:
            print("\n--- Заметки ---")
            print("1. Создать заметку")
            print("2. Просмотреть заметки")
            print("3. Редактировать заметку")
            print("4. Удалить заметку")
            print("0. Назад")
            choice = input("> ").strip()
            if choice == "1":
                self.create_note()
            elif choice == "2":
                self.list_notes()
            elif choice == "3":
                self.edit_note()
            elif choice == "4":
                self.delete_note()
            elif choice == "0":
                return
            else:
                print("Неизвестный выбор.")

    def create_note(self):
        title = input("Заголовок заметки: ").strip()
        content = input("Текст заметки: ").strip()
        if title == "":
            print("Заголовок не может быть пустым.")
            return
        self.current_user.notes.append(Note(title=title, content=content))
        print("Заметка сохранена.")

    def list_notes(self):
        notes = self.current_user.notes
        if not notes:
            print("У вас нет заметок.")
            return
        print("\nВаши заметки:")
        for idx, n in enumerate(notes, 1):
            print(f"{idx}. {n.title} — {n.content[:60]}{'...' if len(n.content) > 60 else ''}")

    def edit_note(self):
        notes = self.current_user.notes
        if not notes:
            print("Нечего редактировать.")
            return
        self.list_notes()
        try:
            idx = int(input("Номер заметки для редактирования: ").strip())
            if not (1 <= idx <= len(notes)):
                print("Неверный номер.")
                return
            note = notes[idx-1]
            title = input(f"Новый заголовок (Enter — оставить '{note.title}'): ").strip()
            content = input(f"Новый текст (Enter — оставить): ").strip()
            if title:
                note.title = title
            if content:
                note.content = content
            print("Заметка обновлена.")
        except ValueError:
            print("Ожидалось число.")

    def delete_note(self):
        notes = self.current_user.notes
        if not notes:
            print("Нечего удалять.")
            return
        self.list_notes()
        try:
            idx = int(input("Номер заметки для удаления: ").strip())
            if not (1 <= idx <= len(notes)):
                print("Неверный номер.")
                return
            removed = notes.pop(idx-1)
            print(f"Заметка '{removed.title}' удалена.")
        except ValueError:
            print("Ожидалось число.")

    def logout(self):
        if self.current_user:
            print(f"Пользователь {self.current_user.username} вышел.")
        self.current_user = None

    def _require_login(self) -> bool:
        if not self.current_user:
            print("Сначала войдите в систему.")
            return False
        return True

    def optional_save_to_file(self):
        """
        Пример использования работы с файлами.
        В задании сказано: данные не сохраняются, поэтому эта функция только демонстрационная.
        Раскомментируй вызов, если хочешь экспортировать свои карточки в файл.
        """
        if not self._require_login(): return
        fname = input("Имя файла для сохранения (например export.txt): ").strip()
        try:
            with open(fname, "w", encoding="utf-8") as f:
                for c in self.current_user.cards:
                    f.write(f"Q:{c.question}\nA:{c.answer}\n---\n")
            print("Экспорт завершён (файл создан).")
        except Exception as e:
            print("Ошибка при сохранении:", e)

    def optional_create_zip_in_memory(self):
        """
        Демонстрация использования zip (в памяти).
        Возвращает bytes zip-архива (не сохраняется в файл).
        """
        import io, zipfile
        if not self._require_login(): return None
        bio = io.BytesIO()
        with zipfile.ZipFile(bio, "w") as zf:
          
            cards_txt = "\n".join(f"Q:{c.question}\nA:{c.answer}\n" for c in self.current_user.cards)
            zf.writestr("cards.txt", cards_txt)
            
            notes_txt = "\n".join(f"{n.title}\n{n.content}\n---\n" for n in self.current_user.notes)
            zf.writestr("notes.txt", notes_txt)
        bio.seek(0)
        print("ZIP-архив создан в памяти (не сохранён на диск).")
        return bio.getvalue()

    def optional_turtle_visual(self):
        """
        Можете использовать turtle для простой визуализации (нужно запускать в среде, где доступен GUI).
        Пример: нарисовать прогресс-бар — демонстрация модуля turtle.
        """
        try:
            import turtle
        except Exception:
            print("Модуль turtle недоступен в этой среде.")
            return
        screen = turtle.Screen()
        t = turtle.Turtle()
        t.hideturtle()
        t.penup()
        t.goto(-200, 0)
        t.pendown()
        t.forward(400)
        screen.mainloop()

   
    def main_menu(self):
        while True:
            print("\n=== StudyApp ===")
            if self.current_user:
                print(f"[Вход как: {self.current_user.username}]")
            print("1. Регистрация")
            print("2. Вход")
            print("3. Добавить карточку")
            print("4. Показать случайную карточку")
            print("5. Запустить викторину")
            print("6. Заметки (опционально)")
            print("7. Выйти из аккаунта")
            print("8. (Опц.) Экспорт карточек в файл (демо)")
            print("9. (Опц.) Создать ZIP в памяти (демо)")
            print("0. Выход из программы")
            choice = input("> ").strip()
            if choice == "1":
                self.register()
            elif choice == "2":
                self.login()
            elif choice == "3":
                self.add_card()
            elif choice == "4":
                self.show_random_card()
            elif choice == "5":
                self.quiz()
            elif choice == "6":
                self.notes_menu()
            elif choice == "7":
                self.logout()
            elif choice == "8":
            
                self.optional_save_to_file()
            elif choice == "9":
                self.optional_create_zip_in_memory()
            elif choice == "0":
                print("Выход. Данные будут потеряны (хранятся только в памяти).")
                return
            else:
                print("Неизвестная команда.")

def main():
    app = StudyApp()
    app.main_menu()

if __name__ == "__main__":
    main()