# AutoCAD MCP Server 📐🤖

Полноценный MCP-сервер (Model Context Protocol) для управления активным чертежом и инстансом **AutoCAD** (поддерживает AutoCAD 2026, 2025, 2024 и более ранние версии через Windows ActiveX / COM Automation).

---

## 🚀 Возможности и Набор Инструментов (40 функций)

### 1. Статус, Документы и Сессия
- `autocad_status(launch_if_closed: bool)` — Подключение, проверка статуса, получение версии, имени открытого чертежа, активного листа, слоя и количества элементов.
- `autocad_list_documents()` — Список всех открытых чертежей в AutoCAD.
- `autocad_activate_document(name: str)` — Переключение активного чертежа по имени.
- `autocad_open_drawing(filepath: str)` — Открытие любого DWG/DXF файла.
- `autocad_save_drawing(filepath: str = None)` — Сохранение текущего чертежа (или `SaveAs` по новому пути).
- `autocad_close_drawing(save_changes: bool = False)` — Закрытие чертежа.

### 2. Универсальные Команды и AutoLISP
- `autocad_send_command(command: str)` — Выполнение **любой** нативной команды AutoCAD или последовательности команд в командной строке.
- `autocad_eval_lisp(code: str)` — Вычисление произвольного выражения AutoLISP с возвратом результата в агента.

### 3. Слои (Layers)
- `autocad_get_layers()` — Полный список слоев с их цветами, состояниями (вкл/выкл, заморозка, блокировка, вес линий, тип линии, печать).
- `autocad_create_layer(name, color, linetype, lineweight)` — Создание или настройка слоя.
- `autocad_modify_layer(name, color, freeze, lock, on, plottable)` — Изменение параметров слоя.
- `autocad_set_active_layer(name)` — Установка текущего рабочего слоя.

### 4. Листы и Пространство Листа (Layouts & PaperSpace)
- `autocad_get_layouts()` — Список всех листов с порядком вкладок.
- `autocad_set_active_layout(name)` — Переключение на указанный лист.
- `autocad_create_layout(name)` — Создание нового чистого листа.
- `autocad_clone_layout(source_name, target_name)` — Клонирование существующего листа (для создания ИС по шаблону).
- `autocad_delete_layout(name)` — Удаление листа.
- `autocad_rename_layout(old_name, new_name)` — Переименование листа.

### 5. Инспекция и Выборка Объектов
- `autocad_get_entities(space, layout_name, entity_type, layer, limit)` — Выборка объектов из пространства модели или любого листа с фильтрацией по типам (Text, MText, BlockReference, Line, Polyline, Circle, Hatch) и слоям.
- `autocad_get_entity_by_handle(handle)` — Подробные свойства объекта по его Handle (координаты, габариты, текст, атрибуты).
- `autocad_delete_entity(handle)` — Удаление объекта по хэндлу.

### 6. Тексты, Штампы и Аннотации
- `autocad_update_text(handle, new_text)` — Изменение текста однострочного или многострочного текста по хэндлу.
- `autocad_batch_update_texts(updates)` — Пакетное обновление штампов чертежей за один вызов `[{"handle": "...", "text": "..."}]`.
- `autocad_add_text(text, insertion_point, height, rotation, layer, space)` — Добавление однострочного текста.
- `autocad_add_mtext(text, insertion_point, width, height, layer, space)` — Добавление многострочного текста.

### 7. Блоки и Атрибуты
- `autocad_get_blocks()` — Список всех определений блоков в чертеже.
- `autocad_insert_block(block_name, insertion_point, scale, rotation, attributes, layer, space)` — Вставка блока с автоматическим заполнением его атрибутов.
- `autocad_get_block_attributes(handle)` — Чтение всех тегов и значений атрибутов блока.
- `autocad_set_block_attributes(handle, attributes)` — Обновление атрибутов блока (штампы, марки, экспликации).

### 8. Черчение и Геометрия
- `autocad_add_line(start_point, end_point, layer, space)` — Отрезок между 3D точками.
- `autocad_add_polyline(points, closed, layer, space)` — 2D полилиния по координатам.
- `autocad_add_circle(center_point, radius, layer, space)` — Окружность.
- `autocad_add_rectangle(corner1, corner2, layer, space)` — Прямоугольник.

### 9. Видовые Экраны и Навигация
- `autocad_zoom(mode, center, scale_or_factor)` — Зумирование (extents, window, center, previous).
- `autocad_configure_viewport(layout_name, center_model_coords, custom_scale, locked)` — Центрирование видового экрана на координатах модели, масштаб и блокировка.

### 10. Печать и Экспорт
- `autocad_plot_to_pdf(layout_name, output_pdf_path)` — Прямой экспорт листа в PDF.

### 11. Системные переменные и Очистка
- `autocad_get_sysvar(name)` — Чтение системной переменной (например, `INSUNITS`, `DIMSCALE`).
- `autocad_set_sysvar(name, value)` — Установка системной переменной.
- `autocad_regen(all_viewports)` — Регенерация чертежа.
- `autocad_purge(all_items)` — Очистка чертежа от мусора (`PurgeAll`).

---

## 🛠️ Запуск и Multi-PC совместимость
Сервер запускается через `uv`:
```bash
uv run --with pywin32 --with "mcp<2" python server.py
```
Или через кросс-платформенный батник `run.bat`.
Конфигурация в `~/.gemini/config/mcp_config.json`:
```json
"autocad": {
  "command": "C:/Users/User/.local/bin/uv.exe",
  "args": [
    "run",
    "--with", "pywin32",
    "--with", "mcp<2",
    "python",
    "D:/Яндекс Диск/Yandex.Disk/выапорпоапраппаапр/Новая папка/Антигравити и Обсидиан/Antigravity/.agents/autocad-mcp/server.py"
  ]
}
```
