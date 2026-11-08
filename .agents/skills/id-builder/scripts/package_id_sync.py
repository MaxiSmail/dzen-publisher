"""
Скрипт синхронизации и комплектования папки ИД:
- Создает бэкап папки ИД с временной меткой
- Распределяет новые исполнительные схемы из папки ИС сразу после соответствующих актов
- Архивирует старые схемы и избыточные сертификаты
- Обновляет АОСР (Excel):
    * Акт 1 (Грунтовка): только КНАУФ-Миттельгрунд, объемы СТРОГО в м2 (без м.п.)
    * Акт 2 (Маяки): Профиль маячковый 6мм + Уголок перфорированный ПВХ 6мм
    * Акт 3 (Сетка): Паспорт качества Сетка стеклотканная 5х5
    * Акт 4 (Цементная): СТРОГО только Волма-Аквастарт и ее декларация (строки 65, 68, 85)
    * Акт 5 (Гипсовая): СТРОГО только КНАУФ МП-75 и ее декларация (строки 65, 68, 85)
    * Высота строки 72 = 15.0 pt, разрыв страницы после строки 54, масштаб 66%
- Выполняет сквозную нумерацию файлов в папке ИД (1..N)
- Пересобирает 2 Реестр.xlsx с формулами сквозной нумерации =F{r-1}+E{r-1} и суммой =SUM(E13:E{N})+2
"""

import os
import shutil
import re
import glob
import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side
from datetime import datetime
import sys

def sync_id_package(position_dir, pos_num=6, total_floors=7):
    sys.stdout.reconfigure(encoding='utf-8')
    id_dir = os.path.join(position_dir, "ИД")
    is_dir = os.path.join(position_dir, "ИС")
    
    if not os.path.exists(id_dir):
        raise FileNotFoundError(f"Папка ИД не найдена: {id_dir}")
        
    # 1. Бэкап
    timestamp = datetime.now().strftime("%Y_%m_%d_%H%M%S")
    backup_dir = os.path.join(position_dir, f"ИД_backup_{timestamp}")
    shutil.copytree(id_dir, backup_dir)
    print(f" Создан бэкап папки ИД: {backup_dir}")
    
    archive_old_schemes = os.path.join(position_dir, "Архив_старые_схемы_ИД")
    archive_old_certs = os.path.join(position_dir, "Архив_удаленные_сертификаты_ИД")
    os.makedirs(archive_old_schemes, exist_ok=True)
    os.makedirs(archive_old_certs, exist_ok=True)
    
    elevations = {
        1: "0,000",
        2: "+3,000",
        3: "+6,000",
        4: "+9,000",
        5: "+12,000",
        6: "+15,000",
        7: "+18,000"
    }
    
    def get_scheme_title(floor, scheme):
        elev = elevations.get(floor, "0,000")
        if scheme == 1:
            return f"Исполнительная схема № {pos_num}.{floor}.2.2.2.4-1-1 на покрытие поверхностей стен и откосов грунтовкой глубокого проникновения на отм. {elev}"
        elif scheme == 2:
            return f"Исполнительная схема № {pos_num}.{floor}.2.2.2.4-2-2 на установку профиля маячкового и углов перфорированных на стенах и откосах на отм. {elev}"
        elif scheme == 3:
            return f"Исполнительная схема № {pos_num}.{floor}.2.2.2.4-3-3 на армирование разнородных материалов стеклопластиковой сеткой на отм. {elev}"
        elif scheme == 4:
            if floor == 1:
                return f"Исполнительная схема № {pos_num}.1.2.2.2.4-4-4 на механизированное полимер-цементное оштукатуривание с/у и в МОП на отм. 0,000"
            else:
                return f"Исполнительная схема № {pos_num}.{floor}.2.2.2.4-4-4 на механизированное полимер-цементное оштукатуривание с/у и откосов на отм. {elev}"
        elif scheme == 5:
            return f"Исполнительная схема № {pos_num}.{floor}.2.2.2.4-5-5 на механизированное гипсовое оштукатуривание стен и откосов толщиной слоя 1,5см на отм. {elev}"
        return ""

    VOLMA_MATERIAL = "Волма-Аквастарт штукатурка цементная 25кг (Декларация о соответствии № РОСС RU Д-RU.PA01.B.50460/23 с 13.12.2023г. по 13.12.2028г.)"
    VOLMA_DECLARATION = "Декларация о соответствии № РОСС RU Д-RU.PA01.B.50460/23 с 13.12.2023г. по 13.12.2028г."

    KNAUF_MATERIAL = "КНАУФ (KNAUF) МП-75 штукатурка гипсовая машинного нанесения Серая (30 кг) (Декларация о соответствии № РОСС RU Д-RU.PA01 .В.06030/26 с 04.03.2026г. по 31.08.2030г.)"
    KNAUF_DECLARATION = "Декларация о соответствии № РОСС RU Д-RU.PA01 .В.06030/26 с 04.03.2026г. по 31.08.2030г."

    # 2. Обновление АОСР в Excel
    print("-> Обновление строк 65, 68, 85 в АОСР...")
    for f in range(1, total_floors + 1):
        # Акт 4
        a4 = glob.glob(os.path.join(id_dir, f"*Акт №{pos_num}.{f}.2.2.2.4-4.xlsx"))
        if a4:
            p4 = a4[0]
            wb4 = openpyxl.load_workbook(p4)
            ws4 = wb4.active
            ws4.cell(65, 1).value = VOLMA_MATERIAL
            sch4 = get_scheme_title(f, 4)
            d4 = f"{sch4}; {VOLMA_DECLARATION}"
            ws4.cell(68, 1).value = d4
            ws4.cell(85, 1).value = d4
            ws4.row_dimensions[72].height = 15.0
            wb4.save(p4)
            wb4.close()

        # Акт 5
        a5 = glob.glob(os.path.join(id_dir, f"*Акт №{pos_num}.{f}.2.2.2.4-5.xlsx"))
        if a5:
            p5 = a5[0]
            wb5 = openpyxl.load_workbook(p5)
            ws5 = wb5.active
            ws5.cell(65, 1).value = KNAUF_MATERIAL
            sch5 = get_scheme_title(f, 5)
            d5 = f"{sch5}; {KNAUF_DECLARATION}"
            ws5.cell(68, 1).value = d5
            ws5.cell(85, 1).value = d5
            ws5.row_dimensions[72].height = 15.0
            wb5.save(p5)
            wb5.close()
            
        # Акты 1, 2, 3 - обновление наименований схем
        for s_idx in (1, 2, 3):
            as_files = glob.glob(os.path.join(id_dir, f"*Акт №{pos_num}.{f}.2.2.2.4-{s_idx}.xlsx"))
            if as_files:
                p_s = as_files[0]
                wb_s = openpyxl.load_workbook(p_s)
                ws_s = wb_s.active
                sch_t = get_scheme_title(f, s_idx)
                v68 = str(ws_s.cell(68, 1).value or '')
                parts = [p.strip() for p in v68.split(';') if p.strip()]
                certs_part = [p for p in parts if not p.lower().startswith('исполнительная схема')]
                combined = f"{sch_t}; " + "; ".join(certs_part) if certs_part else sch_t
                ws_s.cell(68, 1).value = combined
                ws_s.cell(85, 1).value = combined
                ws_s.row_dimensions[72].height = 15.0
                wb_s.save(p_s)
                wb_s.close()

    print(" Акты АОСР успешно актуализированы.")

    # 3. Парсинг групп и фильтрация сертификатов
    def get_num(fname):
        m = re.match(r"^(\d+)\s*(.*)", fname)
        return (int(m.group(1)), m.group(2), fname) if m else (999999, fname, fname)

    sorted_files = sorted(os.listdir(id_dir), key=lambda f: get_num(f)[0])

    groups = []
    cur_floor = None
    cur_scheme = None
    cur_act = None
    cur_sch_file = None
    cur_certs = []

    for f in sorted_files:
        num, rest, fname = get_num(f)
        if "Титульник" in f or "Реестр" in f:
            continue
        
        m_act = re.search(r"Акт №(\d+)\.([1-7])\.2\.2\.2\.4-([1-5])\.xlsx", f)
        if m_act:
            if cur_act:
                groups.append((cur_floor, cur_scheme, cur_act, cur_sch_file, cur_certs))
            cur_floor = int(m_act.group(2))
            cur_scheme = int(m_act.group(3))
            cur_act = (fname, rest)
            cur_sch_file = None
            cur_certs = []
        elif "Исполнительная схема" in f:
            cur_sch_file = (fname, rest)
        else:
            cur_certs.append((fname, rest))

    if cur_act:
        groups.append((cur_floor, cur_scheme, cur_act, cur_sch_file, cur_certs))

    filtered_groups = []
    for fl, sch, act_tuple, sch_tuple, certs_list in groups:
        keep_certs = []
        for c_fname, c_rest in certs_list:
            if sch == 4:
                if "Волма-Аквастарт" in c_rest:
                    keep_certs.append((c_fname, c_rest))
                else:
                    shutil.move(os.path.join(id_dir, c_fname), os.path.join(archive_old_certs, c_fname))
            elif sch == 5:
                if "КНАУФ МП-75" in c_rest or "МП-75" in c_rest:
                    keep_certs.append((c_fname, c_rest))
                else:
                    shutil.move(os.path.join(id_dir, c_fname), os.path.join(archive_old_certs, c_fname))
            else:
                keep_certs.append((c_fname, c_rest))
        filtered_groups.append((fl, sch, act_tuple, sch_tuple, keep_certs))

    # 4. Переименование файлов (сквозная нумерация 1..N)
    temp_map = {}
    for f in os.listdir(id_dir):
        if "Титульник" in f or "Реестр" in f:
            continue
        tmp = f"_tmp_{f}"
        os.rename(os.path.join(id_dir, f), os.path.join(id_dir, tmp))
        temp_map[f] = tmp

    new_idx = 3
    for fl, sch, act_tuple, sch_tuple, certs_list in filtered_groups:
        act_orig, act_base = act_tuple
        new_act_name = f"{new_idx} {act_base}"
        os.rename(os.path.join(id_dir, temp_map[act_orig]), os.path.join(id_dir, new_act_name))
        new_idx += 1
        
        sch_orig, sch_base = sch_tuple
        new_sch_name = f"{new_idx} {sch_base}"
        os.rename(os.path.join(id_dir, temp_map[sch_orig]), os.path.join(id_dir, new_sch_name))
        new_idx += 1
        
        for c_orig, c_base in certs_list:
            new_c_name = f"{new_idx} {c_base}"
            os.rename(os.path.join(id_dir, temp_map[c_orig]), os.path.join(id_dir, new_c_name))
            new_idx += 1

    print(f" Файлы перенумерованы со сквозной нумерацией от 1 до {new_idx - 1}")

    # 5. Пересборка Реестра
    reestr_file = os.path.join(id_dir, "2 Реестр.xlsx")
    wb_reestr = openpyxl.load_workbook(reestr_file)
    ws_reestr = wb_reestr.active

    thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
    top_bot_border = Border(top=Side(style='thin'), bottom=Side(style='thin'))
    font_regular = Font(name="Times New Roman", size=9, bold=False, italic=False)
    font_bold = Font(name="Times New Roman", size=9, bold=True, italic=False)
    font_calibri_11 = Font(name="Calibri", size=11, bold=False, italic=False)

    align_center = Alignment(horizontal="center", vertical="center")
    align_left_wrap = Alignment(horizontal="left", vertical="center", wrap_text=True)

    reestr_rows = []
    cur_num = 3

    for fl, sch, act_tuple, sch_tuple, certs_list in filtered_groups:
        elev = elevations.get(fl, "0,000")
        if sch == 1:
            act_name = f"Акт освидетельствования скрытых работ. Покрытие поверхностей грунтовкой глубокого проникновения стен и откосов в осях 1-13/А-Н на отм. {elev}"
        elif sch == 2:
            act_name = f"Акт освидетельствования скрытых работ. Установка профиля маячкового и углов перфорированных на стенах и откосах в осях 1-13/А-Н на отм. {elev}"
        elif sch == 3:
            act_name = f"Акт освидетельствования скрытых работ. Армирование разнородных материалов стеклопластиковой сеткой в осях 1-13/А-Н на отм. {elev}"
        elif sch == 4:
            if fl == 1:
                act_name = f"Акт освидетельствования скрытых работ. Механизированное полимер-цементное оштукатуривание с/у и в МОП толщиной слоя 1,5см в осях 1-13/А-Н на отм. 0,000"
            else:
                act_name = f"Акт освидетельствования скрытых работ. Механизированное полимер-цементное оштукатуривание с/у и откосов толщиной слоя 1,5см в осях 1-13/А-Н на отм. {elev}"
        elif sch == 5:
            act_name = f"Акт освидетельствования скрытых работ. Механизированное гипсовое оштукатуривание стен и откосов толщиной слоя 1,5см в осях 1-13/А-Н на отм. {elev}"
        
        reestr_rows.append({"num": cur_num, "name": act_name, "doc_no": f"№{pos_num}.{fl}.2.2.2.4-{sch}", "org": "ООО «Техстрой»", "sheets": 1})
        cur_num += 1
        
        sch_name = get_scheme_title(fl, sch)
        reestr_rows.append({"num": cur_num, "name": sch_name, "doc_no": f"№{pos_num}.{fl}.2.2.2.4-{sch}-{sch}", "org": "ООО «Техстрой»", "sheets": 1})
        cur_num += 1
        
        for c_orig, c_base in certs_list:
            if "Волма-Аквастарт" in c_base:
                c_name = "Декларация о соответствии с 13.12.2023г. по 13.12.2028г."
                c_doc = "№ РОСС RU Д-RU.PA01.B.50460/23 "
                c_org = 'ООО "ВОЛМА-Воскресенск"'
                c_sh = 1
            elif "КНАУФ МП-75" in c_base or "МП-75" in c_base:
                c_name = "Декларация о соответствии с 04.03.2026г. по 31.08.2030г."
                c_doc = "№ РОСС RU Д-RU.PA01 .В.06030/26 "
                c_org = 'ООО "КНАУФ ГИПС НОВОМОСКОВСК"'
                c_sh = 1
            elif "Миттельгрунд" in c_base:
                c_name = "Сертификат соответствия с 09.02.2024г. по 08.02.2027г."
                c_doc = "№ RU.CMMK.001.H.00330 "
                c_org = 'ООО "СТМ"'
                c_sh = 1
            elif "маячковый" in c_base:
                c_name = "Сертификат соответствия с 16.07.2025г. по 15.07.2028г."
                c_doc = "№ РОСС RU.32623.OC13.11112 "
                c_org = 'ООО "Эксперт"'
                c_sh = 1
            elif "перфорированный" in c_base:
                c_name = "Сертификат соответствия с 29.11.2023г. по 28.11.2028г."
                c_doc = "№ RU С-RU.ПБ68.В.О1723/23 "
                c_org = 'ООО "ПластПрофиль"'
                c_sh = 2
            elif "Сетка" in c_base:
                c_name = "Паспорт качества / Сертификат соответствия с 23.06.2025г. по 22.06.2028г."
                c_doc = "№ РОСС RU.32001.04ИБФ1.0СП32.79153 "
                c_org = 'ООО "Техпроект"'
                c_sh = 1
            else:
                c_name = c_base
                c_doc = ""
                c_org = ""
                c_sh = 1
                
            reestr_rows.append({"num": cur_num, "name": c_name, "doc_no": c_doc, "org": c_org, "sheets": c_sh})
            cur_num += 1

    start_row = 13
    for i, rdata in enumerate(reestr_rows):
        row_idx = start_row + i
        cA = ws_reestr.cell(row_idx, 1, rdata["num"])
        cA.font, cA.alignment, cA.border = font_regular, align_center, thin_border
        
        cB = ws_reestr.cell(row_idx, 2, rdata["name"])
        cB.font, cB.alignment, cB.border = font_regular, align_left_wrap, thin_border
        
        cC = ws_reestr.cell(row_idx, 3, rdata["doc_no"])
        cC.font, cC.alignment, cC.border = font_regular, align_center, thin_border
        
        cD = ws_reestr.cell(row_idx, 4, rdata["org"])
        cD.font, cD.alignment, cD.border = font_regular, align_left_wrap, thin_border
        
        cE = ws_reestr.cell(row_idx, 5, rdata["sheets"])
        cE.font, cE.alignment, cE.border = font_regular, align_center, thin_border
        
        cF = ws_reestr.cell(row_idx, 6)
        cF.value = 3 if row_idx == 13 else f"=F{row_idx - 1}+E{row_idx - 1}"
        cF.font, cF.alignment, cF.border = font_regular, align_center, thin_border

    last_data_row = start_row + len(reestr_rows) - 1
    totals_row = last_data_row + 1

    # Totals
    for c in range(1, 10):
        cell = ws_reestr.cell(totals_row, c, None)
        cell.border = Border()

    c_tot_label = ws_reestr.cell(totals_row, 4, "Всего страниц в ИД:")
    c_tot_label.font, c_tot_label.border = font_bold, top_bot_border
    c_tot_label.alignment = Alignment(horizontal="right", vertical="center")

    c_tot_val = ws_reestr.cell(totals_row, 5, f"=SUM(E13:E{last_data_row})+2")
    c_tot_val.font, c_tot_val.border = font_bold, top_bot_border
    c_tot_val.alignment = align_center

    # Signatures
    for r in range(totals_row + 1, max(ws_reestr.max_row + 1, totals_row + 50)):
        for c in range(1, 10):
            cell = ws_reestr.cell(r, c, None)
            cell.border = Border()

    sig_rows = [
        (totals_row + 2, 2, "Документы по реестру сдал:", font_calibri_11, Alignment(horizontal="left")),
        (totals_row + 3, 2, "Представитель подрядной строительной организации", font_calibri_11, Alignment(horizontal="left")),
        (totals_row + 4, 2, "Производитель работ ООО «Техстрой» Морщаков А.С.", font_calibri_11, Alignment(horizontal="left")),
        (totals_row + 5, 1, "(должность, фамилия, инициалы, подпись)", font_calibri_11, Alignment(horizontal="left")),
        (totals_row + 7, 2, "Документы по реестру принял:", font_calibri_11, Alignment(horizontal="left")),
        (totals_row + 8, 2, "Представитель застройщика или технического заказчика", font_calibri_11, Alignment(horizontal="left")),
        (totals_row + 10, 1, "(должность, фамилия, инициалы, подпись)", font_calibri_11, Alignment(horizontal="left")),
    ]
    for r, c, val, fnt, aln in sig_rows:
        cell = ws_reestr.cell(r, c, val)
        cell.font, cell.alignment = fnt, aln

    wb_reestr.save(reestr_file)
    wb_reestr.close()
    print(" Реестр 2 Реестр.xlsx успешно пересобран с формулами и подписями!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        sync_id_package(sys.argv[1])
    else:
        print("Использование: python package_id_sync.py <путь_к_папке_позиции>")
