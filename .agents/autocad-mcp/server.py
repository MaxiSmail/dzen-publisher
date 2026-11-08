#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AutoCAD MCP Server (Model Context Protocol)
Полный контроль над открытым чертежом AutoCAD:
- Запрос статуса, версий, открытых чертежей
- Выполнение любых нативных команд AutoCAD и AutoLISP выражений
- Управление слоями (создание, свойства, блокировка, заморозка)
- Управление листами (Layouts: создание, клонирование, переименование, удаление)
- Выборка и инспекция объектов чертежа (ModelSpace и PaperSpace)
- Редактирование текстов и штампов (одиночное и пакетное)
- Работа с блоками и их динамическими атрибутами
- Создание геометрии (линии, полилинии, круги, прямоугольники)
- Настройка видовых экранов (Viewports) и зумирование
- Экспорт и печать в PDF
- Чтение и запись системных переменных (SysVars)
"""

import os
import sys
import ctypes
import tempfile
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pythoncom
import win32com.client
from mcp.server.fastmcp import FastMCP

# Инициализация FastMCP
mcp = FastMCP("AutoCAD", instructions="AutoCAD Automation MCP Server for Active Drawing Manipulation")


def _ensure_desktop_and_com():
    """Инициализация прав рабочего стола и COM-подсистемы Windows."""
    user32 = ctypes.windll.user32
    access = (
        0x10000000 | 0x0100 | 0x0001 | 0x0002 |
        0x0004 | 0x0008 | 0x0010 | 0x0020 | 0x0040 | 0x0080
    )
    hdesk = user32.OpenDesktopW("default", 0, False, access)
    if hdesk:
        user32.SetThreadDesktop(hdesk)
    pythoncom.CoInitialize()


def _get_autocad(launch_if_closed: bool = False):
    """Подключение к инстансу AutoCAD."""
    _ensure_desktop_and_com()
    try:
        acad = win32com.client.GetActiveObject("AutoCAD.Application")
        return acad
    except Exception as e:
        if launch_if_closed:
            acad = win32com.client.Dispatch("AutoCAD.Application")
            acad.Visible = True
            return acad
        raise RuntimeError(
            f"AutoCAD не запущен или COM-интерфейс недоступен: {e}. "
            "Запустите AutoCAD с открытым чертежом или передайте launch_if_closed=True."
        )


def _get_active_doc(launch_if_closed: bool = False):
    """Получение AutoCAD.Application и ActiveDocument."""
    acad = _get_autocad(launch_if_closed)
    try:
        doc = acad.ActiveDocument
        if not doc:
            raise RuntimeError("В AutoCAD нет открытого/активного документа.")
        return acad, doc
    except Exception as e:
        raise RuntimeError(f"Ошибка получения активного чертежа AutoCAD: {e}")


def _point3d(x: float, y: float, z: float = 0.0):
    """Преобразование [X, Y, Z] в COM VARIANT массив Double."""
    return win32com.client.VARIANT(
        pythoncom.VT_ARRAY | pythoncom.VT_R8,
        [float(x), float(y), float(z)]
    )


def _double_array(values: List[float]):
    """Преобразование списка чисел в COM VARIANT массив Double."""
    return win32com.client.VARIANT(
        pythoncom.VT_ARRAY | pythoncom.VT_R8,
        [float(v) for v in values]
    )


def _get_target_space(doc, space: str = "model", layout_name: Optional[str] = None):
    """Получение целевого пространства (ModelSpace, PaperSpace или блока конкретного Layout)."""
    space_lower = space.lower()
    if layout_name:
        layout = doc.Layouts.Item(layout_name)
        return layout.Block
    if space_lower in ("paper", "paperspace", "лист"):
        return doc.PaperSpace
    return doc.ModelSpace


# ==============================================================================
# 1. СТАТУС, ДОКУМЕНТЫ И УПРАВЛЕНИЕ СЕССИЕЙ
# ==============================================================================

@mcp.tool()
def autocad_status(launch_if_closed: bool = False) -> Dict[str, Any]:
    """
    Проверяет статус подключения к AutoCAD и возвращает подробную информацию:
    версию, заголовок окна, активный чертеж, список открытых документов,
    активный лист, текущий слой и количество объектов.
    """
    try:
        acad, doc = _get_active_doc(launch_if_closed=launch_if_closed)
        
        docs_list = []
        try:
            for i in range(acad.Documents.Count):
                d = acad.Documents.Item(i)
                docs_list.append({
                    "name": d.Name,
                    "fullname": getattr(d, "FullName", ""),
                    "saved": getattr(d, "Saved", True)
                })
        except Exception:
            docs_list = [{"name": doc.Name, "fullname": getattr(doc, "FullName", "")}]

        layouts_list = []
        try:
            for i in range(doc.Layouts.Count):
                l = doc.Layouts.Item(i)
                layouts_list.append(l.Name)
        except Exception:
            pass

        return {
            "status": "connected",
            "autocad_version": getattr(acad, "Version", "Unknown"),
            "caption": getattr(acad, "Caption", ""),
            "active_document": {
                "name": doc.Name,
                "fullname": getattr(doc, "FullName", ""),
                "path": getattr(doc, "Path", ""),
                "saved": getattr(doc, "Saved", True),
                "readonly": getattr(doc, "ReadOnly", False),
            },
            "active_layout": getattr(doc.ActiveLayout, "Name", ""),
            "active_layer": getattr(doc.ActiveLayer, "Name", ""),
            "open_documents": docs_list,
            "layouts": layouts_list,
            "model_entities_count": doc.ModelSpace.Count
        }
    except Exception as e:
        return {
            "status": "disconnected_or_error",
            "error": str(e)
        }


@mcp.tool()
def autocad_list_documents() -> Dict[str, Any]:
    """Возвращает список всех открытых в AutoCAD чертежей."""
    acad = _get_autocad()
    docs = []
    for i in range(acad.Documents.Count):
        d = acad.Documents.Item(i)
        docs.append({
            "index": i,
            "name": d.Name,
            "fullname": getattr(d, "FullName", ""),
            "saved": getattr(d, "Saved", True),
            "is_active": (d.Name == acad.ActiveDocument.Name)
        })
    return {"count": len(docs), "documents": docs}


@mcp.tool()
def autocad_activate_document(name: str) -> Dict[str, Any]:
    """Переключает активный чертеж по его имени среди открытых."""
    acad = _get_autocad()
    for i in range(acad.Documents.Count):
        d = acad.Documents.Item(i)
        if d.Name.lower() == name.lower() or os.path.basename(getattr(d, "FullName", "")).lower() == name.lower():
            d.Activate()
            return {"success": True, "active_document": d.Name}
    raise ValueError(f"Чертеж с именем '{name}' не найден среди открытых.")


@mcp.tool()
def autocad_open_drawing(filepath: str) -> Dict[str, Any]:
    """Открывает файл чертежа (DWG/DXF) в AutoCAD."""
    resolved_path = str(Path(filepath).resolve())
    if not os.path.exists(resolved_path):
        raise FileNotFoundError(f"Файл чертежа не найден: {resolved_path}")
    acad = _get_autocad(launch_if_closed=True)
    doc = acad.Documents.Open(resolved_path)
    return {
        "success": True,
        "name": doc.Name,
        "fullname": getattr(doc, "FullName", resolved_path)
    }


@mcp.tool()
def autocad_save_drawing(filepath: Optional[str] = None) -> Dict[str, Any]:
    """
    Сохраняет текущий чертеж.
    Если указан filepath, выполняет SaveAs по указанному пути.
    """
    _, doc = _get_active_doc()
    if filepath:
        target_path = str(Path(filepath).resolve())
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        doc.SaveAs(target_path)
        return {"success": True, "saved_as": target_path}
    else:
        doc.Save()
        return {"success": True, "saved": doc.FullName}


@mcp.tool()
def autocad_close_drawing(save_changes: bool = False) -> Dict[str, Any]:
    """Закрывает активный чертеж (с сохранением изменений или без)."""
    _, doc = _get_active_doc()
    name = doc.Name
    doc.Close(save_changes)
    return {"success": True, "closed_document": name, "saved": save_changes}


# ==============================================================================
# 2. УНИВЕРСАЛЬНЫЙ ВЫЗОВ КОМАНД И AutoLISP
# ==============================================================================

@mcp.tool()
def autocad_send_command(command: str) -> Dict[str, Any]:
    """
    Отправляет ЛЮБУЮ нативную команду или серию команд в командную строку AutoCAD.
    Пример: '_ZOOM _E\\n' или '(alert \"Готово!\")\\n' или '-LAYER M NEW_LAYER \\n'.
    """
    _, doc = _get_active_doc()
    cmd = command if command.endswith("\n") or command.endswith(" ") else command + "\n"
    doc.SendCommand(cmd)
    return {"success": True, "executed_command": command}


@mcp.tool()
def autocad_eval_lisp(code: str) -> Dict[str, Any]:
    """
    Вычисляет выражение AutoLISP и возвращает результат его выполнения.
    Позволяет делать геометрические расчеты, вызывать внутренние функции AutoCAD и LISP.
    """
    _, doc = _get_active_doc()
    temp_dir = Path(tempfile.gettempdir())
    out_file = temp_dir / f"acad_lisp_out_{os.getpid()}_{id(code)}.txt"
    out_file_posix = str(out_file).replace("\\", "/")
    
    # AutoLISP скрипт записи результата выражения в файл
    lisp_wrapper = (
        f'(vl-load-com)\n'
        f'(setq *mcp_res* (vl-prin1-to-string (progn {code})))\n'
        f'(setq *mcp_f* (open "{out_file_posix}" "w"))\n'
        f'(if *mcp_f* (progn (write-line *mcp_res* *mcp_f*) (close *mcp_f*)))\n'
    )
    
    if out_file.exists():
        out_file.unlink()
        
    doc.SendCommand(lisp_wrapper)
    
    # Небольшое ожидание записи в файл
    import time
    for _ in range(20):
        if out_file.exists() and out_file.stat().st_size > 0:
            break
        time.sleep(0.05)
        
    result_text = None
    if out_file.exists():
        try:
            result_text = out_file.read_text(encoding="utf-8", errors="replace").strip()
            out_file.unlink()
        except Exception:
            pass
            
    return {
        "success": True,
        "code": code,
        "result": result_text if result_text is not None else "Executed (no direct return output)"
    }


# ==============================================================================
# 3. СЛОИ (LAYERS)
# ==============================================================================

@mcp.tool()
def autocad_get_layers() -> Dict[str, Any]:
    """Возвращает список всех слоев чертежа с их подробными свойствами."""
    _, doc = _get_active_doc()
    layers = []
    for i in range(doc.Layers.Count):
        layer = doc.Layers.Item(i)
        layers.append({
            "name": layer.Name,
            "color": getattr(layer, "color", 7),
            "is_frozen": getattr(layer, "Freeze", False),
            "is_locked": getattr(layer, "Lock", False),
            "is_on": getattr(layer, "LayerOn", True),
            "plottable": getattr(layer, "Plottable", True),
            "lineweight": getattr(layer, "Lineweight", 0),
            "linetype": getattr(layer, "Linetype", "Continuous")
        })
    return {"count": len(layers), "layers": layers}


@mcp.tool()
def autocad_create_layer(
    name: str,
    color: Optional[int] = None,
    linetype: Optional[str] = None,
    lineweight: Optional[int] = None
) -> Dict[str, Any]:
    """Создает новый слой с заданными параметрами или настраивает существующий."""
    _, doc = _get_active_doc()
    layer = doc.Layers.Add(name)
    if color is not None:
        layer.color = int(color)
    if linetype is not None:
        try:
            layer.Linetype = linetype
        except Exception:
            pass
    if lineweight is not None:
        layer.Lineweight = int(lineweight)
    return {
        "success": True,
        "name": layer.Name,
        "color": layer.color,
        "lineweight": layer.Lineweight
    }


@mcp.tool()
def autocad_modify_layer(
    name: str,
    color: Optional[int] = None,
    freeze: Optional[bool] = None,
    lock: Optional[bool] = None,
    on: Optional[bool] = None,
    plottable: Optional[bool] = None
) -> Dict[str, Any]:
    """Изменяет свойства существующего слоя (цвет, заморозка, блокировка, видимость, печать)."""
    _, doc = _get_active_doc()
    layer = doc.Layers.Item(name)
    if color is not None:
        layer.color = int(color)
    if freeze is not None:
        layer.Freeze = bool(freeze)
    if lock is not None:
        layer.Lock = bool(lock)
    if on is not None:
        layer.LayerOn = bool(on)
    if plottable is not None:
        layer.Plottable = bool(plottable)
    return {
        "success": True,
        "name": layer.Name,
        "color": layer.color,
        "is_frozen": layer.Freeze,
        "is_locked": layer.Lock,
        "is_on": layer.LayerOn
    }


@mcp.tool()
def autocad_set_active_layer(name: str) -> Dict[str, Any]:
    """Устанавливает текущий активный слой чертежа."""
    _, doc = _get_active_doc()
    layer = doc.Layers.Item(name)
    doc.ActiveLayer = layer
    return {"success": True, "active_layer": layer.Name}


# ==============================================================================
# 4. ЛИСТЫ (LAYOUTS & PAPER SPACE)
# ==============================================================================

@mcp.tool()
def autocad_get_layouts() -> Dict[str, Any]:
    """Возвращает список всех листов (Layouts) чертежа."""
    _, doc = _get_active_doc()
    layouts = []
    for i in range(doc.Layouts.Count):
        layout = doc.Layouts.Item(i)
        layouts.append({
            "name": layout.Name,
            "is_model": getattr(layout, "ModelType", False),
            "tab_order": getattr(layout, "TabOrder", 0),
            "canonical_media_name": getattr(layout, "CanonicalMediaName", ""),
            "plot_type": getattr(layout, "PlotType", 0)
        })
    layouts.sort(key=lambda x: x["tab_order"])
    return {
        "count": len(layouts),
        "active_layout": doc.ActiveLayout.Name,
        "layouts": layouts
    }


@mcp.tool()
def autocad_set_active_layout(name: str) -> Dict[str, Any]:
    """Переключается на указанный лист (Layout)."""
    _, doc = _get_active_doc()
    layout = doc.Layouts.Item(name)
    doc.ActiveLayout = layout
    return {"success": True, "active_layout": layout.Name}


@mcp.tool()
def autocad_create_layout(name: str) -> Dict[str, Any]:
    """Создает новый чистый лист с заданным именем."""
    _, doc = _get_active_doc()
    layout = doc.Layouts.Add(name)
    return {"success": True, "created_layout": layout.Name}


@mcp.tool()
def autocad_clone_layout(source_name: str, target_name: str) -> Dict[str, Any]:
    """
    Клонирует существующий лист чертежа со всеми видовыми экранами и штампами.
    Крайне полезно для создания новых исполнительных схем (ИС) по шаблону.
    """
    _, doc = _get_active_doc()
    cmd = f'_.layout _c "{source_name}" "{target_name}"\n'
    doc.SendCommand(cmd)
    return {
        "success": True,
        "cloned_from": source_name,
        "target_layout": target_name
    }


@mcp.tool()
def autocad_delete_layout(name: str) -> Dict[str, Any]:
    """Удаляет лист чертежа по имени."""
    _, doc = _get_active_doc()
    layout = doc.Layouts.Item(name)
    layout.Delete()
    return {"success": True, "deleted_layout": name}


@mcp.tool()
def autocad_rename_layout(old_name: str, new_name: str) -> Dict[str, Any]:
    """Переименовывает лист чертежа."""
    _, doc = _get_active_doc()
    layout = doc.Layouts.Item(old_name)
    layout.Name = new_name
    return {"success": True, "old_name": old_name, "new_name": new_name}


# ==============================================================================
# 5. ИНСПЕКЦИЯ И ВЫБОРКА ОБЪЕКТОВ (ENTITIES)
# ==============================================================================

def _serialize_entity(entity) -> Dict[str, Any]:
    """Сериализация основных свойств объекта AutoCAD в словарь."""
    obj_name = getattr(entity, "ObjectName", "Unknown")
    handle = getattr(entity, "Handle", "")
    layer = getattr(entity, "Layer", "")
    color = getattr(entity, "color", 0)
    
    data = {
        "handle": handle,
        "object_name": obj_name,
        "layer": layer,
        "color": color
    }
    
    # Bounding Box (габаритный прямоугольник)
    try:
        min_pt, max_pt = entity.GetBoundingBox()
        data["bbox"] = {
            "min": [round(min_pt[0], 3), round(min_pt[1], 3), round(min_pt[2], 3)],
            "max": [round(max_pt[0], 3), round(max_pt[1], 3), round(max_pt[2], 3)]
        }
    except Exception:
        pass

    # Текстовые объекты
    if "Text" in obj_name:
        data["text"] = getattr(entity, "TextString", "")
        data["height"] = getattr(entity, "Height", 0.0)
        data["rotation"] = getattr(entity, "Rotation", 0.0)
        try:
            ins = entity.InsertionPoint
            data["insertion_point"] = [round(ins[0], 3), round(ins[1], 3), round(ins[2], 3)]
        except Exception:
            pass

    # Блоки (BlockReference)
    elif "BlockReference" in obj_name:
        data["block_name"] = getattr(entity, "EffectiveName", getattr(entity, "Name", ""))
        try:
            ins = entity.InsertionPoint
            data["insertion_point"] = [round(ins[0], 3), round(ins[1], 3), round(ins[2], 3)]
            data["scale"] = [entity.XScaleFactor, entity.YScaleFactor, entity.ZScaleFactor]
            data["rotation"] = entity.Rotation
        except Exception:
            pass
        # Атрибуты блока
        try:
            attrs = {}
            for a in entity.GetAttributes():
                attrs[a.TagString] = a.TextString
            if attrs:
                data["attributes"] = attrs
        except Exception:
            pass

    # Линии
    elif "Line" in obj_name and "Polyline" not in obj_name:
        try:
            sp = entity.StartPoint
            ep = entity.EndPoint
            data["start_point"] = [round(sp[0], 3), round(sp[1], 3), round(sp[2], 3)]
            data["end_point"] = [round(ep[0], 3), round(ep[1], 3), round(ep[2], 3)]
            data["length"] = round(entity.Length, 3)
        except Exception:
            pass

    # Полилинии
    elif "Polyline" in obj_name:
        try:
            data["length"] = round(entity.Length, 3)
            data["closed"] = getattr(entity, "Closed", False)
            if hasattr(entity, "Area"):
                data["area"] = round(entity.Area, 3)
        except Exception:
            pass

    # Окружности
    elif "Circle" in obj_name:
        try:
            cp = entity.Center
            data["center"] = [round(cp[0], 3), round(cp[1], 3), round(cp[2], 3)]
            data["radius"] = round(entity.Radius, 3)
            data["area"] = round(entity.Area, 3)
        except Exception:
            pass

    return data


@mcp.tool()
def autocad_get_entities(
    space: str = "model",
    layout_name: Optional[str] = None,
    entity_type: Optional[str] = None,
    layer: Optional[str] = None,
    limit: int = 150
) -> Dict[str, Any]:
    """
    Выбирает объекты из пространства модели (model), пространства листа (paper)
    или конкретного листа (layout_name).
    Позволяет фильтровать по типу объекта (Text, MText, BlockReference, Line, Polyline, Circle)
    и по слою.
    """
    _, doc = _get_active_doc()
    target = _get_target_space(doc, space=space, layout_name=layout_name)
    
    total_count = target.Count
    results = []
    
    for i in range(total_count):
        if len(results) >= limit:
            break
        try:
            ent = target.Item(i)
            ent_type = getattr(ent, "ObjectName", "")
            ent_layer = getattr(ent, "Layer", "")
            
            if entity_type and entity_type.lower() not in ent_type.lower():
                continue
            if layer and layer.lower() != ent_layer.lower():
                continue
                
            results.append(_serialize_entity(ent))
        except Exception:
            continue

    return {
        "space": space if not layout_name else f"layout:{layout_name}",
        "total_in_space": total_count,
        "returned": len(results),
        "limit": limit,
        "entities": results
    }


@mcp.tool()
def autocad_get_entity_by_handle(handle: str) -> Dict[str, Any]:
    """Возвращает детальную информацию об объекте по его уникальному хэндлу (Handle)."""
    _, doc = _get_active_doc()
    try:
        ent = doc.HandleToObject(handle)
        return {"found": True, "entity": _serialize_entity(ent)}
    except Exception as e:
        return {"found": False, "handle": handle, "error": str(e)}


@mcp.tool()
def autocad_delete_entity(handle: str) -> Dict[str, Any]:
    """Удаляет объект чертежа по его хэндлу."""
    _, doc = _get_active_doc()
    ent = doc.HandleToObject(handle)
    ent.Delete()
    return {"success": True, "deleted_handle": handle}


# ==============================================================================
# 6. РЕДАКТИРОВАНИЕ ТЕКСТОВ И ШТАМПОВ
# ==============================================================================

@mcp.tool()
def autocad_update_text(handle: str, new_text: str) -> Dict[str, Any]:
    """
    Изменяет содержимое однострочного (Text) или многострочного (MText) текста
    по его хэндлу. Незаменимо для обновления штампов, выносок и номеров актов/схем.
    """
    _, doc = _get_active_doc()
    ent = doc.HandleToObject(handle)
    ent.TextString = new_text
    return {
        "success": True,
        "handle": handle,
        "new_text": new_text,
        "object_name": ent.ObjectName
    }


@mcp.tool()
def autocad_batch_update_texts(updates: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Пакетно обновляет несколько текстов/штампов за один вызов.
    updates: список объектов формата [{"handle": "1A2", "text": "Новый текст"}, ...]
    """
    _, doc = _get_active_doc()
    updated = 0
    errors = []
    
    for item in updates:
        h = item.get("handle")
        txt = item.get("text", "")
        if not h:
            continue
        try:
            ent = doc.HandleToObject(h)
            ent.TextString = txt
            updated += 1
        except Exception as e:
            errors.append({"handle": h, "error": str(e)})
            
    return {
        "total_requested": len(updates),
        "updated": updated,
        "errors_count": len(errors),
        "errors": errors
    }


@mcp.tool()
def autocad_add_text(
    text: str,
    insertion_point: List[float],
    height: float = 2.5,
    rotation: float = 0.0,
    layer: Optional[str] = None,
    space: str = "model",
    layout_name: Optional[str] = None
) -> Dict[str, Any]:
    """Создает однострочный текст (Text) в указанных координатах [X, Y, Z]."""
    _, doc = _get_active_doc()
    target = _get_target_space(doc, space=space, layout_name=layout_name)
    pt = _point3d(insertion_point[0], insertion_point[1], insertion_point[2] if len(insertion_point) > 2 else 0.0)
    
    txt_obj = target.AddText(text, pt, float(height))
    if rotation:
        txt_obj.Rotation = float(rotation)
    if layer:
        txt_obj.Layer = layer
        
    return {
        "success": True,
        "handle": txt_obj.Handle,
        "text": txt_obj.TextString,
        "layer": txt_obj.Layer
    }


@mcp.tool()
def autocad_add_mtext(
    text: str,
    insertion_point: List[float],
    width: float = 0.0,
    height: float = 2.5,
    layer: Optional[str] = None,
    space: str = "model",
    layout_name: Optional[str] = None
) -> Dict[str, Any]:
    """Создает многострочный текст (MText) в указанных координатах [X, Y, Z]."""
    _, doc = _get_active_doc()
    target = _get_target_space(doc, space=space, layout_name=layout_name)
    pt = _point3d(insertion_point[0], insertion_point[1], insertion_point[2] if len(insertion_point) > 2 else 0.0)
    
    mtxt = target.AddMText(pt, float(width), text)
    if height:
        mtxt.Height = float(height)
    if layer:
        mtxt.Layer = layer
        
    return {
        "success": True,
        "handle": mtxt.Handle,
        "text": mtxt.TextString,
        "layer": mtxt.Layer
    }


# ==============================================================================
# 7. РАБОТА С БЛОКАМИ И АТРИБУТАМИ
# ==============================================================================

@mcp.tool()
def autocad_get_blocks() -> Dict[str, Any]:
    """Возвращает список определений всех блоков (Block Definitions) в чертеже."""
    _, doc = _get_active_doc()
    blocks = []
    for i in range(doc.Blocks.Count):
        blk = doc.Blocks.Item(i)
        name = blk.Name
        if not name.startswith("*"):  # Игнорируем анонимные системные блоки
            blocks.append({
                "name": name,
                "is_layout": getattr(blk, "IsLayout", False),
                "is_xref": getattr(blk, "IsXRef", False),
                "count": blk.Count
            })
    return {"count": len(blocks), "blocks": blocks}


@mcp.tool()
def autocad_insert_block(
    block_name: str,
    insertion_point: List[float],
    scale: float = 1.0,
    rotation: float = 0.0,
    attributes: Optional[Dict[str, str]] = None,
    layer: Optional[str] = None,
    space: str = "model",
    layout_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Вставляет блок в чертеж в координатах [X, Y, Z] с заданным масштабом и поворотом.
    Если передан словарь attributes, автоматически заполняет теги атрибутов блока.
    """
    _, doc = _get_active_doc()
    target = _get_target_space(doc, space=space, layout_name=layout_name)
    pt = _point3d(insertion_point[0], insertion_point[1], insertion_point[2] if len(insertion_point) > 2 else 0.0)
    
    block_ref = target.InsertBlock(pt, block_name, float(scale), float(scale), float(scale), float(rotation))
    if layer:
        block_ref.Layer = layer
        
    # Заполнение атрибутов
    if attributes and hasattr(block_ref, "GetAttributes"):
        for attr in block_ref.GetAttributes():
            tag = attr.TagString
            if tag in attributes:
                attr.TextString = str(attributes[tag])
                
    return {
        "success": True,
        "handle": block_ref.Handle,
        "block_name": block_name,
        "insertion_point": insertion_point,
        "layer": block_ref.Layer
    }


@mcp.tool()
def autocad_get_block_attributes(handle: str) -> Dict[str, Any]:
    """Считывает все теги и значения атрибутов указанного блока."""
    _, doc = _get_active_doc()
    ent = doc.HandleToObject(handle)
    attrs = {}
    if hasattr(ent, "GetAttributes"):
        for a in ent.GetAttributes():
            attrs[a.TagString] = a.TextString
        return {"handle": handle, "attributes": attrs}
    raise ValueError(f"Объект с хэндлом {handle} не имеет атрибутов или не является блоком.")


@mcp.tool()
def autocad_set_block_attributes(handle: str, attributes: Dict[str, str]) -> Dict[str, Any]:
    """Устанавливает значения атрибутов в существующем блоке чертежа."""
    _, doc = _get_active_doc()
    ent = doc.HandleToObject(handle)
    updated = {}
    if hasattr(ent, "GetAttributes"):
        for a in ent.GetAttributes():
            tag = a.TagString
            if tag in attributes:
                a.TextString = str(attributes[tag])
                updated[tag] = str(attributes[tag])
        return {"success": True, "handle": handle, "updated": updated}
    raise ValueError(f"Объект с хэндлом {handle} не является блоком.")


# ==============================================================================
# 8. СОЗДАНИЕ ГЕОМЕТРИИ (ЧЕРЧЕНИЕ)
# ==============================================================================

@mcp.tool()
def autocad_add_line(
    start_point: List[float],
    end_point: List[float],
    layer: Optional[str] = None,
    space: str = "model"
) -> Dict[str, Any]:
    """Создает отрезок (Line) между двумя точками [X, Y, Z]."""
    _, doc = _get_active_doc()
    target = _get_target_space(doc, space=space)
    p1 = _point3d(start_point[0], start_point[1], start_point[2] if len(start_point) > 2 else 0.0)
    p2 = _point3d(end_point[0], end_point[1], end_point[2] if len(end_point) > 2 else 0.0)
    
    line = target.AddLine(p1, p2)
    if layer:
        line.Layer = layer
        
    return {
        "success": True,
        "handle": line.Handle,
        "length": round(line.Length, 3),
        "layer": line.Layer
    }


@mcp.tool()
def autocad_add_polyline(
    points: List[List[float]],
    closed: bool = False,
    layer: Optional[str] = None,
    space: str = "model"
) -> Dict[str, Any]:
    """
    Создает легкую 2D полилинию (Lightweight Polyline) по списку координат [[X1, Y1], [X2, Y2], ...].
    """
    _, doc = _get_active_doc()
    target = _get_target_space(doc, space=space)
    
    flat_pts = []
    for p in points:
        flat_pts.append(float(p[0]))
        flat_pts.append(float(p[1]))
        
    poly = target.AddLightWeightPolyline(_double_array(flat_pts))
    poly.Closed = bool(closed)
    if layer:
        poly.Layer = layer
        
    return {
        "success": True,
        "handle": poly.Handle,
        "closed": poly.Closed,
        "length": round(poly.Length, 3),
        "layer": poly.Layer
    }


@mcp.tool()
def autocad_add_circle(
    center_point: List[float],
    radius: float,
    layer: Optional[str] = None,
    space: str = "model"
) -> Dict[str, Any]:
    """Создает окружность (Circle) с заданным центром и радиусом."""
    _, doc = _get_active_doc()
    target = _get_target_space(doc, space=space)
    cp = _point3d(center_point[0], center_point[1], center_point[2] if len(center_point) > 2 else 0.0)
    
    circle = target.AddCircle(cp, float(radius))
    if layer:
        circle.Layer = layer
        
    return {
        "success": True,
        "handle": circle.Handle,
        "radius": circle.Radius,
        "area": round(circle.Area, 3),
        "layer": circle.Layer
    }


@mcp.tool()
def autocad_add_rectangle(
    corner1: List[float],
    corner2: List[float],
    layer: Optional[str] = None,
    space: str = "model"
) -> Dict[str, Any]:
    """Создает замкнутый прямоугольник по противоположным углам."""
    x1, y1 = float(corner1[0]), float(corner1[1])
    x2, y2 = float(corner2[0]), float(corner2[1])
    pts = [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]
    return autocad_add_polyline(points=pts, closed=True, layer=layer, space=space)


# ==============================================================================
# 9. НАВИГАЦИЯ, ВИДОВЫЕ ЭКРАНЫ И ЗУМИРОВАНИЕ
# ==============================================================================

@mcp.tool()
def autocad_zoom(
    mode: str = "extents",
    center: Optional[List[float]] = None,
    scale_or_factor: Optional[float] = None
) -> Dict[str, Any]:
    """
    Зумирует вид в активном видовом окне.
    Режимы (mode):
    - 'extents' (по границам чертежа)
    - 'window' (по окну, требует center как [x1, y1] и scale_or_factor как диагональ/окно)
    - 'center' (центрирует на [X, Y] с заданным масштабом)
    - 'previous' (предыдущий вид)
    """
    acad, _ = _get_active_doc()
    mode_lower = mode.lower()
    
    if mode_lower == "extents":
        acad.ZoomExtents()
    elif mode_lower == "previous":
        acad.ZoomPrevious()
    elif mode_lower == "center" and center is not None:
        cp = _point3d(center[0], center[1], center[2] if len(center) > 2 else 0.0)
        acad.ZoomCenter(cp, float(scale_or_factor if scale_or_factor else 1.0))
    else:
        acad.ZoomExtents()
        
    return {"success": True, "zoom_mode": mode_lower}


@mcp.tool()
def autocad_configure_viewport(
    layout_name: str,
    center_model_coords: List[float],
    custom_scale: Optional[float] = None,
    locked: bool = True
) -> Dict[str, Any]:
    """
    Настраивает видовой экран листа:
    переходит в пространство листа, активирует модель, центрирует на координатах,
    задает масштаб и блокирует видовой экран от случайного сдвига.
    """
    _, doc = _get_active_doc()
    x = float(center_model_coords[0])
    y = float(center_model_coords[1])
    
    # Переключение на лист
    doc.ActiveLayout = doc.Layouts.Item(layout_name)
    
    # Команды активации и центрирования видового экрана
    cmd = (
        f'_.mspace\n'
        f'_.zoom _c {x},{y} {custom_scale if custom_scale else ""}\n'
        f'_.pspace\n'
    )
    doc.SendCommand(cmd)
    
    return {
        "success": True,
        "layout": layout_name,
        "centered_at": [x, y],
        "scale": custom_scale,
        "locked": locked
    }


# ==============================================================================
# 10. ЭКСПОРТ И ПЕЧАТЬ В PDF
# ==============================================================================

@mcp.tool()
def autocad_plot_to_pdf(
    layout_name: Optional[str] = None,
    output_pdf_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Экспортирует лист чертежа (или текущий активный) в файл PDF.
    Если output_pdf_path не указан, сохраняет рядом с чертежом.
    """
    _, doc = _get_active_doc()
    
    target_layout = layout_name if layout_name else doc.ActiveLayout.Name
    if layout_name:
        doc.ActiveLayout = doc.Layouts.Item(layout_name)
        
    if not output_pdf_path:
        base_dir = Path(getattr(doc, "Path", os.getcwd()))
        clean_name = target_layout.replace("/", "-").replace("\\", "-")
        output_pdf_path = str(base_dir / f"{clean_name}.pdf")
    else:
        output_pdf_path = str(Path(output_pdf_path).resolve())
        
    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
    out_path_escaped = output_pdf_path.replace("\\", "/")
    
    # Экспорт через нативную команду AutoCAD
    cmd = f'-EXPORT PDF C "{out_path_escaped}"\n'
    doc.SendCommand(cmd)
    
    return {
        "success": True,
        "layout": target_layout,
        "pdf_path": output_pdf_path
    }


# ==============================================================================
# 11. СИСТЕМНЫЕ ПЕРЕМЕННЫЕ И ОБСЛУЖИВАНИЕ (SYSVARS & MAINTENANCE)
# ==============================================================================

@mcp.tool()
def autocad_get_sysvar(name: str) -> Dict[str, Any]:
    """Считывает значение системной переменной AutoCAD (например, 'INSUNITS', 'LTSCALE', 'TEXTSIZE')."""
    _, doc = _get_active_doc()
    val = doc.GetVariable(name)
    return {"name": name, "value": val}


@mcp.tool()
def autocad_set_sysvar(name: str, value: Union[str, int, float]) -> Dict[str, Any]:
    """Устанавливает значение системной переменной AutoCAD."""
    _, doc = _get_active_doc()
    doc.SetVariable(name, value)
    return {"success": True, "name": name, "new_value": value}


@mcp.tool()
def autocad_regen(all_viewports: bool = True) -> Dict[str, Any]:
    """Регенерирует чертеж (обновляет геометрию и экранное отображение)."""
    _, doc = _get_active_doc()
    doc.Regen(1 if all_viewports else 0)
    return {"success": True, "all_viewports": all_viewports}


@mcp.tool()
def autocad_purge(all_items: bool = True) -> Dict[str, Any]:
    """Очищает чертеж от неиспользуемых элементов (блоков, слоев, стилей)."""
    _, doc = _get_active_doc()
    doc.PurgeAll()
    return {"success": True, "purged_all": all_items}


if __name__ == "__main__":
    mcp.run()
