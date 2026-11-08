"""
AutoCAD Automation Toolkit для Исполнительных Схем:
- Подключение к запущенному инстансу AutoCAD через COM (с фиксом Desktop Thread для фонового режима)
- Пакетное обновление штампов чертежей:
    * Верхний штамп: "к акту № {act_num} от {act_date}"
    * Нижний штамп: дата подписания в формате ММ.ГГ (например, "07.26")
- Клонирование пространства листа (Layouts):
    * Копирование эталонного листа (_.layout _c)
    * Привязка видового экрана к целевым координатам модели (_.zoom _c)
    * Блокировка видового экрана (DisplayLocked = :vlax-true)
- Экспорт листов в PDF в папку ИС
"""

import ctypes
import sys
import re
import os

def init_autocad():
    """Инициализация COM соединения с AutoCAD и фикс прав рабочего стола."""
    sys.stdout.reconfigure(encoding='utf-8')
    user32 = ctypes.windll.user32
    access = 0x10000000 | 0x0100 | 0x0001 | 0x0002 | 0x0004 | 0x0008 | 0x0010 | 0x0020 | 0x0040 | 0x0080
    hdesk = user32.OpenDesktopW("default", 0, False, access)
    if hdesk:
        user32.SetThreadDesktop(hdesk)

    import pythoncom
    import win32com.client.gencache

    pythoncom.CoInitialize()
    acad = win32com.client.gencache.EnsureDispatch(win32com.client.GetActiveObject("AutoCAD.Application"))
    doc = acad.ActiveDocument
    print(f" Подключено к чертежу: {doc.Name}")
    return acad, doc

def update_all_stamps(doc, stamp_mapping, log_path=None):
    """
    Обновление верхних и нижних штампов чертежей по списку.
    stamp_mapping: список словарей с ключами:
      - 'handle': хэндл объекта текста
      - 'type': 'up_act' | 'up_date' | 'low_date'
      - 'text': новый текст
    """
    import win32com.client
    updated = 0
    errors = 0
    
    for item in stamp_mapping:
        try:
            ent = doc.HandleToObject(item['handle'])
            mtext = win32com.client.CastTo(ent, "IAcadMText")
            mtext.TextString = item['text']
            updated += 1
        except Exception as e:
            print(f"Ошибка при обновлении хэндла {item.get('handle')}: {e}")
            errors += 1
            
    print(f" Обновлено штампов: {updated}, ошибок: {errors}")
    return updated, errors

def clone_layout_with_viewport(doc, template_layout, new_layout_name, center_pt, zoom_height=163442.0):
    """
    Клонирование листа и позиционирование видового экрана через AutoLISP.
    """
    x, y = center_pt[0], center_pt[1]
    lisp_cmd = f"""
    (vl-load-com)
    (setvar "CMDECHO" 0)
    (setvar "EXPERT" 5)
    (setvar "CTAB" "Model")
    (if (member "{new_layout_name}" (layoutlist))
      (command "_.layout" "_d" "{new_layout_name}")
    )
    (command "_.layout" "_c" "{template_layout}" "{new_layout_name}")
    (setvar "CTAB" "{new_layout_name}")
    (command "_.mspace")
    (if (= (getvar "CVPORT") 2)
      (progn
        (command "_.zoom" "_c" (list {x} {y} 0.0) {zoom_height})
        (command "_.pspace")
        (setq ss (ssget "_X" (list '(0 . "VIEWPORT") (cons 410 "{new_layout_name}") '(69 . 2))))
        (if ss
          (vla-put-DisplayLocked (vlax-ename->vla-object (ssname ss 0)) :vlax-true)
        )
      )
    )
    (setvar "CMDECHO" 1)
    (princ)
    """
    doc.SendCommand(lisp_cmd)
    print(f" Лист '{new_layout_name}' успешно создан и отцентрирован на ({x}, {y})")

if __name__ == "__main__":
    acad, doc = init_autocad()
    print("AutoCAD Toolkit готов к работе.")
