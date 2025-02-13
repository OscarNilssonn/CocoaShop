import sqlite3
from datetime import date

class User:
    def __init__(self, db_name="users.db"):
        self.db_name = db_name
        self.logged_in_user = None
        self._initialize_database()

    def _initialize_database(self):
        """Creates the users table if it does not exist."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    email TEXT UNIQUE,
                    address TEXT,
                    city TEXT,
                    tel TEXT,
                    location_preference TEXT,
                    chocolate_preference TEXT,
                    first_visit TEXT,
                    password TEXT
                )
            ''')
            conn.commit()

    def create_account(self, name, email, address, city, tel, location_preference, chocolate_preference, first_visit,
                       password):
        """Inserts a new user record into the database."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (name, email, address, city, tel, location_preference, chocolate_preference, first_visit, password)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                           (name, email, address, city, tel, location_preference, chocolate_preference,
                            first_visit.strftime("%Y-%m-%d"), password))
            conn.commit()
            return cursor.lastrowid

    def open_account(self):
        print('*** Open new account ***')
        name = input('What is your name? ')
        email = input('What is your email? ')
        address = input('What is your address? ')
        city = input('What is your city? ')
        tel = input('What is your phone number? ')
        location_preference = input('What is your location preference? ')
        chocolate_preference = input('What is your chocolate preference? ')
        user_password = input('What is the password you want to use for the account? ')
        user_account_number = self.create_account(name, email, address, city, tel, location_preference,
                                                  chocolate_preference, date.today(), user_password)
        print(f'Your new account ID is: {user_account_number}')
        print()

    def login(self):
        print('*** User Login ***')
        email = input('Enter your email: ')
        password = input('Enter your password: ')

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
            user = cursor.fetchone()

        if user:
            self.logged_in_user = {
                "id": user[0],
                "name": user[1],
                "email": user[2],
                "address": user[3],
                "city": user[4],
                "tel": user[5],
                "location_preference": user[6],
                "chocolate_preference": user[7],
                "first_visit": user[8],
                "password": user[9],
            }
            print(f'Login successful! Welcome, {user[1]}')
        else:
            print('Error: Incorrect email or password!')

    def view_personal_info(self):
        if self.logged_in_user is None:
            print("Error: You must be logged in to view personal information!")
            return

        print("\n*** Personal Information ***")
        print(f"Name: {self.logged_in_user['name']}")
        print(f"Email: {self.logged_in_user['email']}")
        print(f"Address: {self.logged_in_user['address']}")
        print(f"City: {self.logged_in_user['city']}")
        print(f"Phone Number: {self.logged_in_user['tel']}")
        print(f"Location Preference: {self.logged_in_user['location_preference']}")
        print(f"Chocolate Preference: {self.logged_in_user['chocolate_preference']}")
        print(f"First Visit: {self.logged_in_user['first_visit']}")

    def delete_account(self):
        if self.logged_in_user is None:
            print("Error: You must be logged in to delete your account!")
            return

        email = input("Confirm your email: ")
        password = input("Confirm your password: ")

        if email != self.logged_in_user["email"] or password != self.logged_in_user["password"]:
            print("Error: Email or password does not match!")
            return

        confirm = input("Are you sure you want to delete your account? (yes/no): ").strip().lower()
        if confirm == "yes":
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM users WHERE email = ?", (self.logged_in_user["email"],))
                conn.commit()
                print("Your account has been deleted successfully.")
                self.logged_in_user = None
        else:
            print("Account deletion cancelled.")

    def list_users(self):
        """Displays a list of all registered users."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, email FROM users")
            users = cursor.fetchall()

        if users:
            print("\n*** Registered Users ***")
            for user in users:
                print(f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")
        else:
            print("No registered users found.")

    def getName(self, name):
        return name

