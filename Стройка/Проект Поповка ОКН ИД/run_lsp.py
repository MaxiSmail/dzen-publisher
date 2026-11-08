import sys
from pathlib import Path
import pythoncom
import win32com.client

def run_lsp(lsp_file):
    pythoncom.CoInitialize()
    doc = win32com.client.GetObject(r"C:\Users\User\Downloads\ИС\Схема ситниченко.dwg")
    posix_path = str(Path(lsp_file).resolve()).replace("\\", "/")
    cmd = f'(load "{posix_path}")\n'
    print(f"Sending: {cmd.strip()}")
    doc.SendCommand(cmd)
    print("Done!")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "test_ping.lsp"
    run_lsp(target)
