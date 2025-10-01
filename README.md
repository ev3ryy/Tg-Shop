# 🤖 [TG Shop] - Портфолио Проект

**Функционал:**
* Интерактивный **Каталог** товаров.
* **Корзина** с функцией добавления/очистки.
* Моделирование **транзакций** и списания **Баланса**.
* Использование **FSM (Finite State Machine)** для сбора данных (ввод количества).

**Стек технологий:**
* Python 3.11+
* **aiogram 3.22**
* **SQLAlchemy 2.0+**
* SQLite

---

## ⚙️ Установка (ctrl c, ctrl v)

### 1. Клонирование репозитория

```bash
git clone https://github.com/ev3ryy/Tg-Shop.git
cd Tg-Shop
```

### 2. Создание виртуального окружения
```
python -m venv venv

# (Linux/macOS)
source venv/bin/activate

# (Windows PowerShell)
.\venv\Scripts\activate
```

### 3. Установка зависимостей
```
pip install -r requirements.txt
```
### 4. Создание конфига
```
echo "BOT_TOKEN = *Токен бота из тг*" > .env
```
