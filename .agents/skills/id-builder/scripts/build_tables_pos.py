import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.styles.colors import Color
from openpyxl.utils import get_column_letter
import os
import re
import argparse

src_file = r"D:\YandexDisk\выапорпоапраппаапр\Новая папка\0 Новая папка\ИП Нерсисян\Рыбацкий квартал\Позиция №6 (симонян)\раскладка по квартирам Позиция 6_на 28.09.2026.xlsx"
folder = r"D:\YandexDisk\выапорпоапраппаапр\Новая папка\0 Новая папка\ИП Нерсисян\Рыбацкий квартал\Позиция №6 (симонян)"

wb_src = openpyxl.load_workbook(src_file, data_only=True)
ws_src = wb_src[wb_src.sheetnames[0]]

# Palette matching user-edited sheets exactly
font_header = Font(name='ISOCPEUR', size=10.0, bold=True, italic=True)
font_units  = Font(name='ISOCPEUR', size=10.0, bold=True, italic=True)
font_data   = Font(name='ISOCPEUR', size=10.0, bold=False, italic=True)
font_total  = Font(name='ISOCPEUR', size=10.0, bold=True, italic=True)

font_doc_title = Font(name='ISOCPEUR', size=11.0, bold=True, italic=True, color='002060')
font_doc_sub   = Font(name='ISOCPEUR', size=9.5, bold=False, italic=True, color='595959')
font_doc_work  = Font(name='ISOCPEUR', size=9.5, bold=True, italic=True, color='1F4E78')

fill_theme_4 = PatternFill(
    start_color=Color(theme=4, tint=0.7999816888943144),
    end_color=Color(theme=4, tint=0.7999816888943144),
    fill_type='solid'
)

side_thin = Side(style='thin')
box_border = Border(left=side_thin, right=side_thin, top=side_thin, bottom=side_thin)

align_center_wrap = Alignment(horizontal='center', vertical='center', wrap_text=True)
align_center      = Alignment(horizontal='center', vertical='center')
align_left_wrap   = Alignment(horizontal='left', vertical='center', wrap_text=True)

fl_configs = [
    {
        "fl": 7, "r_st": 93, "elev": "+18,000", "name": "7 этаж", "prefix": "6.7.2.2.2.4",
        "dates": {
            1: ("06 июля 2026г.", "6.7.2.2.2.4-1"),
            2: ("07 июля 2026г.", "6.7.2.2.2.4-2"),
            3: ("07 июля 2026г.", "6.7.2.2.2.4-3"),
            4: ("08 июля 2026г.", "6.7.2.2.2.4-4"),
            5: ("08 июля 2026г.", "6.7.2.2.2.4-5"),
        }
    },
    {
        "fl": 6, "r_st": 78, "elev": "+15,000", "name": "6 этаж", "prefix": "6.6.2.2.2.4",
        "dates": {
            1: ("08 июля 2026г.", "6.6.2.2.2.4-1"),
            2: ("09 июля 2026г.", "6.6.2.2.2.4-2"),
            3: ("09 июля 2026г.", "6.6.2.2.2.4-3"),
            4: ("10 июля 2026г.", "6.6.2.2.2.4-4"),
            5: ("10 июля 2026г.", "6.6.2.2.2.4-5"),
        }
    },
    {
        "fl": 5, "r_st": 63, "elev": "+12,000", "name": "5 этаж", "prefix": "6.5.2.2.2.4",
        "dates": {
            1: ("10 июля 2026г.", "6.5.2.2.2.4-1"),
            2: ("11 июля 2026г.", "6.5.2.2.2.4-2"),
            3: ("11 июля 2026г.", "6.5.2.2.2.4-3"),
            4: ("12 июля 2026г.", "6.5.2.2.2.4-4"),
            5: ("12 июля 2026г.", "6.5.2.2.2.4-5"),
        }
    },
    {
        "fl": 4, "r_st": 48, "elev": "+9,000",  "name": "4 этаж", "prefix": "6.4.2.2.2.4",
        "dates": {
            1: ("12 июля 2026г.", "6.4.2.2.2.4-1"),
            2: ("13 июля 2026г.", "6.4.2.2.2.4-2"),
            3: ("13 июля 2026г.", "6.4.2.2.2.4-3"),
            4: ("14 июля 2026г.", "6.4.2.2.2.4-4"),
            5: ("14 июля 2026г.", "6.4.2.2.2.4-5"),
        }
    },
    {
        "fl": 3, "r_st": 33, "elev": "+6,000",  "name": "3 этаж", "prefix": "6.3.2.2.2.4",
        "dates": {
            1: ("14 июля 2026г.", "6.3.2.2.2.4-1"),
            2: ("15 июля 2026г.", "6.3.2.2.2.4-2"),
            3: ("15 июля 2026г.", "6.3.2.2.2.4-3"),
            4: ("16 июля 2026г.", "6.3.2.2.2.4-4"),
            5: ("16 июля 2026г.", "6.3.2.2.2.4-5"),
        }
    },
    {
        "fl": 2, "r_st": 18, "elev": "+3,000",  "name": "2 этаж", "prefix": "6.2.2.2.2.4",
        "dates": {
            1: ("16 июля 2026г.", "6.2.2.2.2.4-1"),
            2: ("17 июля 2026г.", "6.2.2.2.2.4-2"),
            3: ("17 июля 2026г.", "6.2.2.2.2.4-3"),
            4: ("18 июля 2026г.", "6.2.2.2.2.4-4"),
            5: ("18 июля 2026г.", "6.2.2.2.2.4-5"),
        }
    },
    {
        "fl": 1, "r_st":  3, "elev": "0,000",   "name": "1 этаж", "prefix": "6.1.2.2.2.4",
        "dates": {
            1: ("18 июля 2026г.", "6.1.2.2.2.4-1"),
            2: ("19 июля 2026г.", "6.1.2.2.2.4-2"),
            3: ("19 июля 2026г.", "6.1.2.2.2.4-3"),
            4: ("20 июля 2026г.", "6.1.2.2.2.4-4"),
            5: ("20 июля 2026г.", "6.1.2.2.2.4-5"),
        }
    },
]

def to_num(val):
    if val is None or val == "":
        return None
    try:
        f = float(val)
        return round(f, 2)
    except Exception:
        return None

def clean_apt_name(raw_apt):
    t = raw_apt.strip()
    m = re.match(r'^[Кк]в\.?\s*(\d+)$', t)
    if m:
        return f"Квартира № {m.group(1)}"
    if "моп" in t.lower():
        return "МОП"
    if "балкон" in t.lower():
        return "Балконы"
    return t

def extract_floor_entities(r_st):
    r_apt = r_st + 1
    r_room = r_st + 2
    cur_apt = ""
    entities = []
    
    for c in range(2, 45):
        v_apt = ws_src.cell(r_apt, c).value
        v_room = ws_src.cell(r_room, c).value
        s_apt = str(v_apt or "").strip()
        s_rm = str(v_room or "").strip()
        
        is_grand_total = (c == 42 or "квартиры и моп" in s_apt.lower())
        is_mop_total = (c == 41 or "всего  моп" in s_apt.lower() or "всего моп" in s_apt.lower())
        is_apt_summary_total = (c == 35 or "всего по квартирам" in s_rm.lower() or "всего по квартирам" in s_apt.lower())
        
        if is_grand_total:
            apt_name = "ВСЕГО квартиры и МОП"
        elif is_mop_total:
            apt_name = "МОП"
        elif is_apt_summary_total:
            apt_name = "Всего по квартирам"
        elif 36 <= c <= 40 or any(k in s_rm.lower() for k in ["моп", "куи", "тамбур", "лестн", "лифтов"]):
            apt_name = "МОП"
        elif c == 34 or "балкон" in s_apt.lower():
            apt_name = "Балконы"
        else:
            if s_apt:
                cur_apt = s_apt
            apt_name = cur_apt
            
        vals = {
            "gyps_m2": to_num(ws_src.cell(r_st + 3, c).value),
            "cps_m2": to_num(ws_src.cell(r_st + 4, c).value),
            "gyps_otk_m": to_num(ws_src.cell(r_st + 6, c).value),
            "gyps_otk_s": to_num(ws_src.cell(r_st + 7, c).value),
            "cps_otk_m": to_num(ws_src.cell(r_st + 8, c).value),
            "cps_otk_s": to_num(ws_src.cell(r_st + 9, c).value),
            "mayak_m": to_num(ws_src.cell(r_st + 10, c).value),
            "mayak_pcs": to_num(ws_src.cell(r_st + 11, c).value),
            "ugol_m": to_num(ws_src.cell(r_st + 12, c).value),
            "ugol_pcs": to_num(ws_src.cell(r_st + 13, c).value),
            "setka_m": to_num(ws_src.cell(r_st + 14, c).value),
        }
        
        has_any = any(v is not None for v in vals.values())
        if not s_rm and not has_any:
            continue
            
        is_apt_total = ("всего" in s_rm.lower() or "итого" in s_rm.lower()) and not is_apt_summary_total
        
        entities.append({
            "col": c,
            "apt": clean_apt_name(apt_name),
            "room": s_rm,
            "vals": vals,
            "is_grand_total": is_grand_total,
            "is_mop_total": is_mop_total,
            "is_apt_summary_total": is_apt_summary_total,
            "is_apt_total": is_apt_total,
        })
        
    return entities

def get_work_columns(work_num, floor_num, entities):
    # Determine columns dynamically
    grand_ent = [e for e in entities if e["is_grand_total"]]
    gt_vals = grand_ent[0]["vals"] if grand_ent else {}
    
    if work_num == 1: # Грунтовка
        cols = [
            ("Стены под гипс", "м²", lambda v: v["gyps_m2"]),
            ("Стены под ЦПС", "м²", lambda v: v["cps_m2"]),
            ("Откосы под гипс", "м.п.", lambda v: v["gyps_otk_m"]),
        ]
        # Only add Откосы под ЦПС if floor has non-zero ЦПС откосы
        if gt_vals.get("cps_otk_m") and gt_vals.get("cps_otk_m") > 0:
            cols.append(("Откосы под ЦПС", "м.п.", lambda v: v["cps_otk_m"]))
            
        cols.append(("ВСЕГО стен", "м²", lambda v: round((v["gyps_m2"] or 0) + (v["cps_m2"] or 0), 2) if (v["gyps_m2"] or v["cps_m2"]) else None))
        has_work_fn = lambda v: bool(v["gyps_m2"] or v["cps_m2"] or v["gyps_otk_m"] or v["cps_otk_m"])
        return "Грунтовка", "Покрытие поверхностей стен и откосов грунтовкой глубокого проникновения", cols, has_work_fn

    elif work_num == 2: # Маяки
        cols = [
            ("Профиль маячковый 6мм", "м.п.", lambda v: v["mayak_m"]),
            ("Профиль маячковый 6мм", "шт.", lambda v: v["mayak_pcs"]),
            ("Угол перфорированный 6мм", "м.п.", lambda v: v["ugol_m"]),
            ("Угол перфорированный 6мм", "шт.", lambda v: v["ugol_pcs"]),
        ]
        has_work_fn = lambda v: bool(v["mayak_m"] or v["mayak_pcs"] or v["ugol_m"] or v["ugol_pcs"])
        return "Маяки", "Установка профиля маячкового и углов перфорированных на стенах и откосах", cols, has_work_fn

    elif work_num == 3: # Сетка
        cols = [
            ("Сетка стеклопластиковая 5х5мм", "м.п.", lambda v: v["setka_m"]),
        ]
        has_work_fn = lambda v: bool(v["setka_m"])
        return "Сетка", "Армирование разнородных материалов стеклопластиковой сеткой", cols, has_work_fn

    elif work_num == 4: # ЦПС
        cols = [
            ("Штукатурка стен с/у (ЦПС)", "м²", lambda v: v["cps_m2"]),
        ]
        if gt_vals.get("cps_otk_m") and gt_vals.get("cps_otk_m") > 0:
            cols.append(("Откосы с/у (ЦПС)", "м.п.", lambda v: v["cps_otk_m"]))
        has_work_fn = lambda v: bool(v["cps_m2"] or v["cps_otk_m"])
        return "ЦПС", "Механизированное полимер-цементное оштукатуривание с/у и откосов толщиной слоя 1,5см", cols, has_work_fn

    elif work_num == 5: # Гипс
        cols = [
            ("Штукатурка стен (гипс)", "м²", lambda v: v["gyps_m2"]),
            ("Откосы (гипс)", "м.п.", lambda v: v["gyps_otk_m"]),
        ]
        has_work_fn = lambda v: bool(v["gyps_m2"] or v["gyps_otk_m"])
        return "Гипс", "Механизированное гипсовое оштукатуривание стен и откосов толщиной слоя 1,5см", cols, has_work_fn

def format_cell_val(cv, val, u_str, is_bold=False):
    cv.font = font_total if is_bold else font_data
    cv.alignment = align_center
    cv.border = box_border
    if val is not None and val != 0 and str(val).strip() != "":
        if u_str == "шт.":
            cv.value = int(round(float(val)))
            cv.number_format = '#,##0'
        else:
            # float
            f_val = float(val)
            if f_val == int(f_val):
                cv.value = int(f_val)
                cv.number_format = '0'
            else:
                cv.value = round(f_val, 2)
                cv.number_format = '0.00' if round(f_val, 2) != round(f_val, 1) else '0.0'
    else:
        cv.value = '-'
        cv.alignment = align_center

def create_user_styled_sheet(wb, cfg, work_num, include_header=False):
    fl = cfg["fl"]
    elev = cfg["elev"]
    fl_name = cfg["name"]
    date_str, act_num = cfg["dates"][work_num]
    
    entities = extract_floor_entities(cfg["r_st"])
    short_name, full_title, cols_def, has_work_fn = get_work_columns(work_num, fl, entities)
    num_val_cols = len(cols_def)
    total_cols = 3 + num_val_cols
    
    sheet_title = f"{act_num} ({short_name} {fl}эт)"
    if len(sheet_title) > 31:
        sheet_title = f"{act_num} ({short_name[:8]})"
        
    ws = wb.create_sheet(title=sheet_title)
    ws.views.sheetView[0].showGridLines = True
    
    grand_ent = [e for e in entities if e["is_grand_total"]]
    
    apt_order = []
    apts_data = {}
    for e in entities:
        if e["is_grand_total"] or e["is_apt_summary_total"]:
            continue
        apt_key = e["apt"]
        if apt_key not in apts_data:
            apts_data[apt_key] = {"rooms": [], "total_ent": None}
            apt_order.append(apt_key)
            
        if e["is_apt_total"] or e["is_mop_total"]:
            apts_data[apt_key]["total_ent"] = e
        else:
            apts_data[apt_key]["rooms"].append(e)

    # Starting row
    r_cur = 2
    if include_header:
        # Rows 2-4: Title block
        ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=total_cols)
        c_t = ws.cell(2, 1, f"ВЕДОМОСТЬ ОБЪЕМОВ РАБОТ К ИСПОЛНИТЕЛЬНОЙ СХЕМЕ № {act_num}")
        c_t.font = font_doc_title
        c_t.alignment = align_left_wrap
        ws.row_dimensions[2].height = 22
        
        ws.merge_cells(start_row=3, start_column=1, end_row=3, end_column=total_cols)
        c_s = ws.cell(3, 1, f"Приложение № 1 к акту № {act_num} от {date_str} | Объект: Позиция № 6, {fl_name} (отм. {elev})")
        c_s.font = font_doc_sub
        c_s.alignment = align_left_wrap
        ws.row_dimensions[3].height = 18
        
        ws.merge_cells(start_row=4, start_column=1, end_row=4, end_column=total_cols)
        c_w = ws.cell(4, 1, f"Вид работ: {full_title}")
        c_w.font = font_doc_work
        c_w.alignment = align_left_wrap
        ws.row_dimensions[4].height = 18
        
        r_cur = 6

    # ----------------------------------------------------
    # Table Header Rows
    # ----------------------------------------------------
    h_r1 = r_cur
    h_r2 = r_cur + 1
    ws.row_dimensions[h_r1].height = 50.0 # generous height for multi-line headers
    ws.row_dimensions[h_r2].height = 18.0
    
    # Merge A, B, C across row 1 & 2
    ws.merge_cells(start_row=h_r1, start_column=1, end_row=h_r2, end_column=1)
    c_a = ws.cell(h_r1, 1, "№ п/п")
    c_a.font = font_header
    c_a.fill = fill_theme_4
    c_a.alignment = align_center_wrap
    c_a.border = box_border
    # bottom cell of merge
    ws.cell(h_r2, 1).border = box_border
    ws.cell(h_r2, 1).fill = fill_theme_4
    
    ws.merge_cells(start_row=h_r1, start_column=2, end_row=h_r2, end_column=2)
    c_b = ws.cell(h_r1, 2, "Квартира / Зона")
    c_b.font = font_header
    c_b.fill = fill_theme_4
    c_b.alignment = align_center_wrap
    c_b.border = box_border
    ws.cell(h_r2, 2).border = box_border
    ws.cell(h_r2, 2).fill = fill_theme_4
    
    ws.merge_cells(start_row=h_r1, start_column=3, end_row=h_r2, end_column=3)
    c_c = ws.cell(h_r1, 3, "Помещение")
    c_c.font = font_header
    c_c.fill = fill_theme_4
    c_c.alignment = align_center_wrap
    c_c.border = box_border
    ws.cell(h_r2, 3).border = box_border
    ws.cell(h_r2, 3).fill = fill_theme_4
    
    for v_idx, (col_lbl, u_str, getter) in enumerate(cols_def):
        col_idx = 4 + v_idx
        # Row 1: label
        ch1 = ws.cell(h_r1, col_idx, col_lbl)
        ch1.font = font_header
        ch1.fill = fill_theme_4
        ch1.alignment = align_center_wrap
        ch1.border = box_border
        
        # Row 2: unit
        ch2 = ws.cell(h_r2, col_idx, u_str)
        ch2.font = font_units
        ch2.fill = fill_theme_4
        ch2.alignment = align_center
        ch2.border = box_border

    r_cur += 2
    row_num = 1
    
    # ----------------------------------------------------
    # Data Rows
    # ----------------------------------------------------
    for apt_name in apt_order:
        data = apts_data[apt_name]
        
        active_rooms = [rm for rm in data["rooms"] if has_work_fn(rm["vals"])]
        has_subtotal_work = bool(data["total_ent"] and has_work_fn(data["total_ent"]["vals"]))
        
        if not active_rooms and not has_subtotal_work:
            continue
            
        for rm in active_rooms:
            # Row height: 18 pt or 25.5 pt if room has 'с/у'
            rm_text = rm["room"] if rm["room"] else apt_name
            ws.row_dimensions[r_cur].height = 25.5 if ("с/у" in rm_text.lower() or len(rm_text) > 8) else 18.0
            
            c1 = ws.cell(r_cur, 1, row_num)
            c1.font = font_data
            c1.alignment = align_center_wrap
            c1.border = box_border
            
            # Apartment name in Col B
            c2 = ws.cell(r_cur, 2, apt_name)
            c2.font = font_data
            c2.alignment = align_center_wrap
            c2.border = box_border
            
            c3 = ws.cell(r_cur, 3, rm_text)
            c3.font = font_data
            c3.alignment = align_center_wrap
            c3.border = box_border
            
            for v_idx, (col_lbl, u_str, getter) in enumerate(cols_def):
                col_idx = 4 + v_idx
                cv = ws.cell(r_cur, col_idx)
                val = getter(rm["vals"])
                format_cell_val(cv, val, u_str, is_bold=False)
                
            r_cur += 1
            row_num += 1
            
        # ----------------------------------------------------
        # Apartment Subtotal Row
        # ----------------------------------------------------
        ws.row_dimensions[r_cur].height = 22.5
        c_sub_num = ws.cell(r_cur, 1, None)
        c_sub_num.fill = fill_theme_4
        c_sub_num.border = box_border
        
        # Subtotal label merged B:C
        sub_title = f"Итого по {apt_name}"
        ws.merge_cells(start_row=r_cur, start_column=2, end_row=r_cur, end_column=3)
        c_sub_lbl = ws.cell(r_cur, 2, sub_title)
        c_sub_lbl.font = font_total
        c_sub_lbl.fill = fill_theme_4
        c_sub_lbl.alignment = align_center_wrap
        c_sub_lbl.border = box_border
        ws.cell(r_cur, 3).border = box_border
        ws.cell(r_cur, 3).fill = fill_theme_4
        
        for v_idx, (col_lbl, u_str, getter) in enumerate(cols_def):
            col_idx = 4 + v_idx
            cv = ws.cell(r_cur, col_idx)
            cv.fill = fill_theme_4
            
            val = None
            if data["total_ent"]:
                val = getter(data["total_ent"]["vals"])
            else:
                s = sum(float(getter(rm["vals"]) or 0) for rm in active_rooms)
                val = round(s, 2) if s > 0 else None
                
            format_cell_val(cv, val, u_str, is_bold=True)
            
        r_cur += 1

    # ----------------------------------------------------
    # Grand Total Row
    # ----------------------------------------------------
    ws.row_dimensions[r_cur].height = 24.0
    gt_num = ws.cell(r_cur, 1, None)
    gt_num.fill = fill_theme_4
    gt_num.border = box_border
    
    # Grand total label merged B:C
    gt_title = f"ИТОГО ПО {fl} ЭТАЖ (отм. {elev})"
    ws.merge_cells(start_row=r_cur, start_column=2, end_row=r_cur, end_column=3)
    gt_lbl = ws.cell(r_cur, 2, gt_title)
    gt_lbl.font = font_total
    gt_lbl.fill = fill_theme_4
    gt_lbl.alignment = align_center_wrap
    gt_lbl.border = box_border
    ws.cell(r_cur, 3).border = box_border
    ws.cell(r_cur, 3).fill = fill_theme_4
    
    for v_idx, (col_lbl, u_str, getter) in enumerate(cols_def):
        col_idx = 4 + v_idx
        cv = ws.cell(r_cur, col_idx)
        cv.fill = fill_theme_4
        
        val = None
        if grand_ent:
            val = getter(grand_ent[0]["vals"])
            
        format_cell_val(cv, val, u_str, is_bold=True)
        
    # ----------------------------------------------------
    # Column Widths
    # ----------------------------------------------------
    ws.column_dimensions['A'].width = 7.0
    ws.column_dimensions['B'].width = 13.5
    ws.column_dimensions['C'].width = 7.5
    for v_idx in range(num_val_cols):
        col_letter = get_column_letter(4 + v_idx)
        # width based on work type
        if work_num == 2:
            widths = [8.86, 10.43, 9.43, 8.0]
            ws.column_dimensions[col_letter].width = widths[v_idx] if v_idx < len(widths) else 9.0
        elif work_num == 1:
            widths = [9.43, 7.14, 7.57, 7.57, 8.43]
            ws.column_dimensions[col_letter].width = widths[v_idx] if v_idx < len(widths) else 9.0
        else:
            ws.column_dimensions[col_letter].width = 9.5

def build_workbook(include_header=False):
    wb_new = openpyxl.Workbook()
    wb_new.remove(wb_new.active)
    
    sheet_cnt = 0
    for cfg in fl_configs:
        for work_num in range(1, 6):
            create_user_styled_sheet(wb_new, cfg, work_num, include_header=include_header)
            sheet_cnt += 1
            
    print(f"Generated {sheet_cnt} sheets (include_header={include_header})")
    
    out_file1 = os.path.join(folder, "Ведомости_объемов_по_схемам_Позиция_6_вертикальные_28.09.2026.xlsx")
    out_file2 = os.path.join(folder, "База", "Ведомости_объемов_по_схемам_Позиция_6_вертикальные_28.09.2026.xlsx")
    
    wb_new.save(out_file1)
    wb_new.save(out_file2)
    print("SAVED TO:")
    print(" ", out_file1)
    print(" ", out_file2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--with-header", action="store_true", help="Include title rows above table")
    args = parser.parse_args()
    build_workbook(include_header=args.with_header)
