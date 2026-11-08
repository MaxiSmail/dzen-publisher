"""
Генератор 4-х исполнительных схем в AutoCAD для объекта в с. Поповка:
1. ИС №1: Демонтаж конструкций
2. ИС №2: Разработка грунта (земляные работы)
3. ИС №3: Армирование ленточного фундамента и буронабивных свай
4. ИС №4: Бетонирование ленточного фундамента и буронабивных свай

Формат: А3 альбомный (М 1:50) в пространстве Модели.
Разработчик: Ерышев М.С. (ООО «БМК»).
"""

import sys
import math
from pathlib import Path
import pythoncom
import win32com.client

def get_drawing():
    pythoncom.CoInitialize()
    dwg_path = r"C:\Users\User\Downloads\ИС\Схема ситниченко.dwg"
    try:
        doc = win32com.client.GetObject(dwg_path)
        print(f"Успешно подключились к файлу: {doc.Name}")
        return doc
    except Exception as e:
        print(f"Ошибка подключения: {e}")
        return None

if __name__ == "__main__":
    doc = get_drawing()
    if doc:
        print(f"Active document name: {doc.Name}")
