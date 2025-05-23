from pathlib import Path
import shutil
import time
import schedule


folder_path = Path(r"C:\Users\hiimd\AppData\Local\Temp") 


for item in folder_path.iterdir():
    try:
        if item.is_file() or item.is_symlink():
            item.unlink()  
        elif item.is_dir():
            shutil.rmtree(item) 
    except Exception as e:
        print(f"無法刪除 {item}: {e}")  

