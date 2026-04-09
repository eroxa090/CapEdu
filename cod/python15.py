import zipfile
import os

for i in range(1, 4):
    with open(f"file{i}.txt", "w") as f:
        f.write(f"Это содержимое файла {i}")
print("✅ Тестовые файлы созданы.")

files = ["file1.txt", "file2.txt", "file3.txt"]

try:
    with zipfile.ZipFile("archive.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in files:
            zipf.write(file)
            print(f"📦 Добавлен в архив: {file}")
    print("🎉 Архив 'archive.zip' успешно создан!\n")

except Exception as e:
    print("❌ Ошибка при создании архива:", e)


try:
    with zipfile.ZipFile("archive.zip", "r") as zipf:
        print("📂 Содержимое архива:")
        print(zipf.namelist())
        print()

except FileNotFoundError:
    print("❌ Архив не найден.")
except zipfile.BadZipFile:
    print("❌ Повреждённый ZIP файл.")
except Exception as e:
    print("❌ Ошибка:", e)



extract_path = "output_folder"

try:
    with zipfile.ZipFile("archive.zip", "r") as zipf:
        zipf.extractall(extract_path)
        print(f"📎 Файлы успешно извлечены в: {extract_path}\n")

except FileNotFoundError:
    print("❌ Архив не найден.")
except zipfile.BadZipFile:
    print("❌ Повреждённый ZIP файл.")
except PermissionError:
    print("❌ Нет прав на запись.")
except Exception as e:
    print("❌ Ошибка:", e)


print("📁 Содержимое извлечённой папки:")
for file in os.listdir(extract_path):
    print("✅", file)