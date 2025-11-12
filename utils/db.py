import sqlite3
from datetime import datetime,timezone

def create_connection():
    conn = sqlite3.connect("database/diet_planner.db")
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS users(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT,
                   age INTEGER,
                   gender TEXT,
                   email TEXT,
                   height REAL,
                   weight REAL,
                   goal TEXT,
                   diet_preference TEXT,
                   activity_level TEXT
            )
    ''')

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS calculations (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_id INTEGER,
                   tdee REAL,
                   bmi REAL,
                   bmi_category TEXT,
                   water_intake REAL,
                   timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                   FOREIGN KEY (user_id) REFERENCES users(id)
            )
    ''')

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS macros (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_id INTEGER,
                   protein REAL,
                   target_calories REAL,
                   carbs REAL,
                   fats REAL,
                   timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                   FOREIGN KEY (user_id) REFERENCES users(id)
            )
    ''')

    cursor.execute('''
                CREATE TABLE IF NOT EXISTS goals(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_id INTEGER,
                   goal_type TEXT,
                   target_weight REAL,
                   target_time_months INTEGER,
                   daily_calorie_change REAL,
                   target_calories REAL,
                   health_warning TEXT,
                   timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                   FOREIGN KEY (user_id) REFERENCES users(id)
                )
        ''')
    
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_progress(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_id INTEGER,
                   weight REAL,
                   height REAL,
                   age INTEGER,
                   goal TEXT,
                   diet_preference TEXT,
                   activity_level TEXT,
                   timestamp TEXT,
                   FOREIGN KEY (user_id) REFERENCES users(id)
                )
        ''')
    
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS meal_plans(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_id INTEGER,
                   plan_type TEXT,
                   custom_note TEXT,
                   prompt TEXT,
                   meal_plan TEXT,
                   timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                   FOREIGN KEY (user_id) REFERENCES users(id)
                )
        ''')
    
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS auth(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT NOT NULL UNIQUE,
                   email TEXT NOT NULL UNIQUE,
                   password TEXT NOT NULL
                )
    ''')

    conn.commit()
    conn.close()


def insert_user(user):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
            INSERT INTO users (name, age, gender, email, height, weight, goal, diet_preference, activity_level)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user.name, user.age, user.gender, user.email, user.height, user.weight, user.goal, user.diet_preference, user.activity_level))

    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return user_id

def update_user(user):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users SET name = ?, age = ?, gender = ?, email = ?, height = ?, weight = ?, goal = ?, diet_preference = ?, activity_level = ?
        WHERE id = ?
    ''', (user.name, user.age, user.gender, user.email, user.height, user.weight, user.goal, user.diet_preference, user.activity_level, user.id))
    conn.commit()
    conn.close()


def insert_calculations(user_id, tdee, bmi, bmi_category, water):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO calculations (user_id, tdee, bmi, bmi_category, water_intake)
        VALUES (?, ?, ?, ?, ?)
        ''', (user_id, tdee, bmi, bmi_category, water))
    
    conn.commit()
    conn.close()


def insert_macros(user_id, protein, target_calories, carbs, fats):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO macros(user_id, protein, target_calories, carbs, fats)
        VALUES (?, ?, ?, ?, ?)
        ''', (user_id, protein, target_calories, carbs, fats))
    
    conn.commit()
    conn.close()


def insert_goal(user_id, goal_type, target_weight, target_time_months, daily_change, target_calories, warning):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO goals(user_id, goal_type, target_weight, target_time_months, daily_calorie_change, target_calories, health_warning)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, goal_type, target_weight, target_time_months, daily_change, target_calories, warning))
    
    conn.commit()
    conn.close()


def insert_user_progress(user):
    conn = create_connection()
    cursor = conn.cursor()

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute('''
        INSERT INTO user_progress(user_id, weight, height, age, goal, diet_preference, activity_level, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user.id, user.weight, user.height, user.age, user.goal, user.diet_preference, user.activity_level, timestamp))

    conn.commit()
    conn.close()


def insert_meal_plan(user_id, plan_type, custom_note, prompt, meal_plan):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
            INSERT INTO meal_plans(user_id, plan_type, custom_note, prompt, meal_plan)
            VALUES (?, ?, ?, ?, ?)
    ''', (user_id, plan_type, custom_note, prompt, meal_plan))

    conn.commit()
    conn.close()





