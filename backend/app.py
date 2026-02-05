from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({
        'message': 'API системы учета товаров',
        'version': '1.0.0',
        'endpoint': {
            'GET /': 'Информация об API',
            'GET /health': 'Проверка состояния сервера'
        }
    })
@app.route('/health')
def health_check():
    return jsonify({'status': 'OK'}), 200

if __name__ == '__main__':
    if not os.path.exists('data'):
        os.makedirs('data')
        print("Создана папка 'data'")

    print("=" * 40)
    print("Сервер запущен")
    print("API доступен по адресу: http://localhost:5000")
    print("Фронтэнд: frontend/index.html")
    print("=" * 40)

    app.run(host='0.0.0.0', port=5000)

