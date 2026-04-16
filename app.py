import os
from dotenv import load_dotenv
from app import create_app

# 讀取 .env 環境變數
load_dotenv()

# 初始化 Flask Application Factory
app = create_app()

if __name__ == '__main__':
    # 啟動應用程式
    is_debug = os.environ.get('FLASK_DEBUG', '1') == '1'
    app.run(debug=is_debug)
