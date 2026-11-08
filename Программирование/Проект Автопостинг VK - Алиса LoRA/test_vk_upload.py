import asyncio
import io
import json
import ssl
import uuid
import urllib.request
import urllib.parse
from PIL import Image

token = "vk1.a.tEmX73caYQoXJv4SATgm9WktS977eQ-JRZioeQ_MXscej10WqZOPTsD9RmcODitVwpUKwOpBrVrZlec18YpUVmbo6ycWCupVgfTZk87ZxY2hCKLxB6M4E37y29ZtHACzOxKLXijBPc-NDkrd_1TMj4wbSH4bJHhDPFfWKdrjH7OvUFstn4lGOBlhogdGHlsDRP0-euUh26YsRZjuOOG24A"
group_id = 241210070

# 1. Get upload URL
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(
    "https://api.vk.com/method/photos.getWallUploadServer",
    data=urllib.parse.urlencode({"access_token": token, "v": "5.199", "group_id": group_id}).encode()
)
with urllib.request.urlopen(req, context=ssl_ctx) as r:
    upload_url = json.loads(r.read())["response"]["upload_url"]
    print("Upload URL:", upload_url)

# 2. Upload via manual multipart
img = Image.new("RGB", (500, 500), color=(200, 50, 50))
buf = io.BytesIO()
img.save(buf, format="JPEG", quality=90)
img_bytes = buf.getvalue()

boundary = f"----WebKitFormBoundary{uuid.uuid4().hex}"
body = bytearray()
body.extend(f"--{boundary}\r\n".encode())
body.extend(b'Content-Disposition: form-data; name="photo"; filename="image.jpg"\r\n')
body.extend(b"Content-Type: image/jpeg\r\n\r\n")
body.extend(img_bytes)
body.extend(f"\r\n--{boundary}--\r\n".encode())

req_upload = urllib.request.Request(
    upload_url,
    data=bytes(body),
    headers={
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "User-Agent": "Mozilla/5.0"
    }
)

with urllib.request.urlopen(req_upload, context=ssl_ctx) as r:
    up_res = json.loads(r.read().decode("utf-8"))
    print("Upload Result:", up_res)

# 3. Save photo
save_params = urllib.parse.urlencode({
    "access_token": token,
    "v": "5.199",
    "group_id": group_id,
    "photo": up_res["photo"],
    "server": up_res["server"],
    "hash": up_res["hash"]
}).encode()

req_save = urllib.request.Request("https://api.vk.com/method/photos.saveWallPhoto", data=save_params)
with urllib.request.urlopen(req_save, context=ssl_ctx) as r:
    saved = json.loads(r.read().decode("utf-8"))
    print("Saved Photo Response:", saved)
