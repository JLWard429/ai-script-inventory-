import os
import shutil

BASE_DIR = 'ai-script-inventory-'

for item in os.listdir(BASE_DIR):
    path = os.path.join(BASE_DIR, item)
    if os.path.isfile(path):
        ext = os.path.splitext(item)[1].lower().replace('.', '')
        if not ext:
            ext = 'no_extension'
        target_dir = os.path.join(BASE_DIR, ext)
        os.makedirs(target_dir, exist_ok=True)
        shutil.move(path, os.path.join(target_dir, item))
import os
import shutil

BASE_DIR = 'ai-script-inventory-'

for item in os.listdir(BASE_DIR):
    path = os.path.join(BASE_DIR, item)
    if os.path.isfile(path):
        ext = os.path.splitext(item)[1].lower().replace('.', '')
        if not ext:
            ext = 'no_extension'
        target_dir = os.path.join(BASE_DIR, ext)
        os.makedirs(target_dir, exist_ok=True)
        shutil.move(path, os.path.join(target_dir, item))
