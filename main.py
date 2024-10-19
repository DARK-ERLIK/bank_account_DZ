import sqlite3

class BankAccount:
    def __init__(self, db_name="bank.db"):
        self.conn = sqlite3.connect(db_name)
        self.drop_table()  # Удаляет существующую таблицу
        self.create_tables()  # Создаёт таблицу заново

    # Удаление таблицы (для целей разработки)
    def drop_table(self):
        self.conn.execute("DROP TABLE IF EXISTS clients")
        self.conn.commit()

    # Создание таблиц
    def create_tables(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS clients (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                surname TEXT,
                                phone TEXT UNIQUE,
                                password TEXT,
                                balance REAL DEFAULT 0.0
                                )''')
        self.conn.commit()

    # Регистрация клиента
    def register_client(self, name, surname, phone, password):
        # Здесь можно вручную проверять ошибки, если нужно
        result = self.conn.execute("INSERT INTO clients (name, surname, phone, password) VALUES (?, ?, ?, ?)",
                                  (name, surname, phone, password))
        self.conn.commit()
        if result.rowcount > 0:
            print(f"Клиент {name} успешно зарегистрирован")
        else:
            print(f"Ошибка регистрации клиента {name}")

    # Авторизация клиента
    def login(self, phone, password):
        client = self.conn.execute("SELECT * FROM clients WHERE phone=? AND password=?", (phone, password)).fetchone()
        if client:
            print(f"Добро пожаловать, {client[1]}!")
            return client
        else:
            print("Неверный телефон или пароль")
            return None

    # Пополнение баланса
    def deposit(self, phone, amount):
        client = self.conn.execute("SELECT balance FROM clients WHERE phone=?", (phone,)).fetchone()
        if client:
            new_balance = client[0] + amount
            self.conn.execute("UPDATE clients SET balance=? WHERE phone=?", (new_balance, phone))
            self.conn.commit()
            print(f"Баланс пополнен. Текущий баланс: {new_balance:.2f} сумов")
        else:
            print("Клиент не найден")

    # Снятие денег
    def withdraw(self, phone, amount):
        client = self.conn.execute("SELECT balance FROM clients WHERE phone=?", (phone,)).fetchone()
        if client:
            if client[0] >= amount:
                new_balance = client[0] - amount
                self.conn.execute("UPDATE clients SET balance=? WHERE phone=?", (new_balance, phone))
                self.conn.commit()
                print(f"Вы сняли {amount} сумов. Текущий баланс: {new_balance:.2f} сумов")
            else:
                print("Недостаточно средств")
        else:
            print("Клиент не найден")

    # Просмотр баланса
    def show_balance(self, phone):
        client = self.conn.execute("SELECT balance FROM clients WHERE phone=?", (phone,)).fetchone()
        if client:
            print(f"Текущий баланс: {client[0]:.2f} сумов")
        else:
            print("Клиент не найден")

    # Подсчет вклада на 12, 24, 36 месяцев с фиксированной процентной ставкой
    def calculate_investment(self, phone, months, interest_rate=0.01):
        if months not in [12, 24, 36]:
            print("Неправильный срок. Выберите 12, 24 или 36 месяцев.")
            return

        client = self.conn.execute("SELECT balance FROM clients WHERE phone=?", (phone,)).fetchone()
        if client:
            balance = client[0]
            future_value = balance * (1 + interest_rate) ** (months / 12)
            print(f"Вклад через {months} месяцев при ставке {interest_rate*100:.2f}% составит: {future_value:.2f} сумов")
        else:
            print("Клиент не найден")


# Пример использования
bank = BankAccount()

# Личный кабинет
while True:
    action = input("Выберите действие:\n1. Регистрация\n2. Вход в аккаунт\n3. Выход\n")
    if action == "1":
        name = input("Введите ваше имя: ")
        surname = input("Введите вашу фамилию: ")
        phone = input("Введите номер телефона: ")
        password = input("Введите пароль: ")
        bank.register_client(name, surname, phone, password)
    elif action == "2":
        phone = input("Введите номер телефона: ")
        password = input("Введите пароль: ")
        user = bank.login(phone, password)
        if user:
            while True:
                menu = input("Выберите действие:\n"
                             "1- Пополнить баланс\n"
                             "2- Снять деньги\n"
                             "3- Посмотреть баланс\n"
                             "4- Подсчитать вклад (12, 24, 36 месяцев)\n"
                             "5- Выход из аккаунта\n")
                if menu == "1":
                    bank.deposit(phone, amount=int(input("Введите сумму для пополнения: ")))
                elif menu == "2":
                    bank.withdraw(phone, amount=int(input("Введите сумму для снятия: ")))
                elif menu == "3":
                    bank.show_balance(phone)
                elif menu == "4":
                    months = int(input("Введите срок вклада (12, 24, 36 месяцев): "))
                    bank.calculate_investment(phone, months)
                elif menu == "5":
                    print("Выход из аккаунта")
                    break
    elif action == "3":
        break