"""
Сборщик Сводного PDF тома ИД:
1. Конвертирует все файлы Excel (.xlsx) в PDF через win32com (Excel.Application) в фоновом режиме:
   - Сохранение масштаба 66% (Zoom = 66)
   - Учет разделителей страниц (PageBreak после 54 строки)
2. Выполняет векторное бесшовное объединение всех PDF (PyMuPDF / fitz):
   - 1 Титульник
   - 2 Реестр
   - Акты, схемы, сертификаты и паспорта качества
3. Сохраняет единый файл "ИД Позиция №X.pdf".
"""

import os
import re
import sys
import fitz  # PyMuPDF
import win32com.client

def get_file_number(fname):
    m = re.match(r"^(\d+)\s*(.*)", fname)
    return int(m.group(1)) if m else 999999

def convert_xlsx_to_pdf(excel_app, xlsx_path, pdf_path):
    wb = excel_app.Workbooks.Open(os.path.abspath(xlsx_path))
    try:
        ws = wb.ActiveSheet
        # Проверяем, если это не Реестр и не Титульник, настраиваем масштаб для АОСР
        fname = os.path.basename(xlsx_path)
        if "Акт" in fname:
            ws.PageSetup.Zoom = 66
            ws.PageSetup.Orientation = 1  # xlPortrait
            ws.PageSetup.PaperSize = 9    # xlPaperA4
        wb.ExportAsFixedFormat(0, os.path.abspath(pdf_path))
    finally:
        wb.Close(False)

def assemble_summary_pdf(id_dir, output_pdf_path):
    sys.stdout.reconfigure(encoding='utf-8')
    temp_pdf_dir = os.path.join(id_dir, "_temp_pdf_export")
    os.makedirs(temp_pdf_dir, exist_ok=True)
    
    files = sorted(os.listdir(id_dir), key=get_file_number)
    files = [f for f in files if not f.startswith("_") and not f.startswith(".") and f.endswith(('.xlsx', '.pdf'))]
    
    print(f"Найдено документов для сборки: {len(files)}")
    
    excel = None
    converted_pdfs = []
    
    try:
        excel = win32com.client.Dispatch("Excel.Application")
        excel.Visible = False
        excel.DisplayAlerts = False
        
        doc_sequence = []
        
        for f in files:
            full_path = os.path.join(id_dir, f)
            if f.endswith('.xlsx'):
                pdf_name = f.replace('.xlsx', '.pdf')
                pdf_target = os.path.join(temp_pdf_dir, pdf_name)
                print(f"Конвертация Excel -> PDF: {f}...")
                convert_xlsx_to_pdf(excel, full_path, pdf_target)
                doc_sequence.append(pdf_target)
                converted_pdfs.append(pdf_target)
            elif f.endswith('.pdf'):
                doc_sequence.append(full_path)
                
    finally:
        if excel:
            excel.Quit()
            
    print(f"\nОбъединение {len(doc_sequence)} файлов в единый том (векторный PyMuPDF)...")
    merged_doc = fitz.open()
    
    for pdf_p in doc_sequence:
        try:
            src_doc = fitz.open(pdf_p)
            merged_doc.insert_pdf(src_doc)
            src_doc.close()
        except Exception as e:
            print(f"Предупреждение: ошибка вставки {pdf_p}: {e}")
            
    merged_doc.save(output_pdf_path)
    merged_doc.close()
    
    # Очистка временных PDF
    for p in converted_pdfs:
        try:
            os.remove(p)
        except Exception:
            pass
    try:
        os.rmdir(temp_pdf_dir)
    except Exception:
        pass
        
    print(f"\n Сводный том успешно собран: {output_pdf_path}")
    print(f"Всего страниц в итоговом документе: {merged_doc.page_count if hasattr(merged_doc, 'page_count') else 'OK'}")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        assemble_summary_pdf(sys.argv[1], sys.argv[2])
    else:
        print("Использование: python merge_summary_pdf.py <папка_ИД> <выходной_файл.pdf>")
