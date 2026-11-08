import sys
import pythoncom
import win32com.client

print("Step 1: CoInitialize", flush=True)
pythoncom.CoInitialize()

print("Step 2: Dispatch", flush=True)
acad = win32com.client.Dispatch("AutoCAD.Application")
print(f"AutoCAD Caption: {acad.Caption}", flush=True)

print(f"Documents count: {acad.Documents.Count}", flush=True)
for i in range(acad.Documents.Count):
    d = acad.Documents.Item(i)
    print(f"  [{i}]: {d.Name}", flush=True)

print("Done!", flush=True)
