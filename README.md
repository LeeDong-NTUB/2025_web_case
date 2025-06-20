## Python install
請先安裝 Python（建議版本 3.10 以上）：
https://www.python.org/

## 開啟CMD
使用命令提示字元（Command Prompt / Terminal）切換到專案目錄：
cd 2025_web_case

## install
安裝 Django JET Reboot 後台介面：
pip install git+https://github.com/assem-ch/django-jet-reboot

安裝所有必要套件（來自 requirements.txt）：
pip install -r requirements.txt

## Run
執行以下指令初始化專案並啟動伺服器：

python manage.py collectstatic      # 收集靜態資源
python manage.py makemigrations     # 產生資料庫遷移檔
python manage.py migrate            # 執行資料庫遷移
python manage.py runserver          # 啟動本地開發伺服器（預設 http://127.0.0.1:8000/）
