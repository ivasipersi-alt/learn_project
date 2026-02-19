'use strict';

const API_BASE_URL = 'http://localhost:5000';
const API_CHECK_INTERVAL = 5000;
let apiCheckTimer = null;
async function chekApiStatus(){
    const statusElement = document.getElementById('api-status');
    const spinnerElement = document.getElementById('loading-spinner');
    try {
        const response = await fetch(`${API_BASE_URL}/`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        });
        if (response.ok) {
            const data = await response.json();
            statusElement.textContent = `API работает (версия ${data.version})`;
            spinnerElement.style.display = 'none';
            console.log('API сервер доступен');
        } else {
            throw new Error(`Ошибка сервера: ${response.status}`);
        }
    } catch (error) {
        if (error.message.includes('Failed to fetch')) {
            statusElement.textContent = 'API сервер недоступен';
            console.log('API сервер недоступен. Запустите backend/app.py');
        }
        else if (error.message.includes('Ошибка сервера')) {
            statusElement.textContent = 'Проблема с API сервером';
            console.log('API сервер ответил с ошибкой');
        }
        else {
            statusElement.textContent = 'Ошибка соединения';
            console.log('Неизвестная ошибка:', error.message);
        }
        spinnerElement.style.display = 'inline-block';

    }
}
function startApiMonitoring() {
    chekApiStatus();
    apiCheckTimer = setInterval(chekApiStatus, API_CHECK_INTERVAL);
    console.log('Мониторинг API запущен')
}
function stopApiMonitoring() {
    clearInterval(apiCheckTimer);
    apiCheckTimer = null;
    console.log('Мониторинг API остановлен');
}
function initApp() {
    console.log('Приложение инициализируется...');
    startApiMonitoring();
    setupEventListeners();
    console.log('Приложение готово к работе');
}
function setupEventListeners() {
    window.addEventListener('beforeunload', stopApiMonitoring);
    window.addEventListener('online', chekApiStatus);
    window.addEventListener('offline',function () {
        const statusElement = document.getElementById('api-status')
        if (statusElement) {
            statusElement.textContent = 'Нет интернет-соединения'
        }
    });
}
document.addEventListener('DOMContentLoaded', initApp)
function formatDate(date) {
    return date.toLocaleDateString('ru-RU');
}
window.appDebug = {
    chekApiStatus: chekApiStatus,
    stopApiMonitoring: stopApiMonitoring,
    formatDate: formatDate,
};
console.log('Для отладки используйте window.appDebug в консоли браузера (F12)');
console.log('Доступные команды:');
console.log(' window.appDebug.chekApiStatus() - проверить API');
console.log(' window.appDebug.stopApiMonitoring() - остановить проверку');
console.log(' window.appDebug.formatDate(new Date()) - форматировать дату');
