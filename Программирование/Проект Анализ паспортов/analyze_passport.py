import os
import numpy as np
from PIL import Image

p_dir = r"d:\YandexDisk\выапорпоапраппаапр\Новая папка\Антигравити и Обсидиан\Antigravity\passport_task"
pass_path = os.path.join(p_dir, "passport_2.jpg")

img = Image.open(pass_path).convert('RGB')
arr = np.array(img) # shape: (451, 320, 3)

h, w, _ = arr.shape
print(f"Passport size: {w}x{h}")

# Let's compute color variance along columns and rows to locate photo boundaries
# Photo regions typically have different color texture/variance compared to blank document areas
row_std = np.std(arr, axis=(1, 2))
col_std = np.std(arr, axis=(0, 2))

# Print top regions of interest or crop quadrantal previews
quads = {
    'top_left': arr[0:h//2, 0:w//2],
    'top_right': arr[0:h//2, w//2:w],
    'bottom_left': arr[h//2:h, 0:w//2],
    'bottom_right': arr[h//2:h, w//2:w]
}

for name, q in quads.items():
    print(f"Quadrant {name}: shape={q.shape}, mean_rgb={np.mean(q, axis=(0,1)).round(1)}, std_rgb={np.std(q, axis=(0,1)).round(1)}")

# Save 4 quadrant crops for quick inspection
for name, q in quads.items():
    Image.fromarray(q).save(os.path.join(p_dir, f"crop_{name}.jpg"))

print("Saved quadrant crops!")
