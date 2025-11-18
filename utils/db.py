import streamlit as st
from datetime import datetime,timezone
from sqlalchemy import text

def create_connection():
    conn = st.connection("db", type="sql")
    return conn

def create_table():
    conn = create_connection()
    with conn.session as s:
        s.execute(text('''
            CREATE TABLE IF NOT EXISTS users(
                   id SERIAL PRIMARY KEY,
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
        '''))
        s.execute(text('''
            CREATE TABLE IF NOT EXISTS calculations (
                   id SERIAL PRIMARY KEY,
                   user_id INTEGER,
                   tdee REAL,
                   bmi REAL,
                   bmi_category TEXT,
                   water_intake REAL,
                   timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                   FOREIGN KEY (user_id) REFERENCES users(id)
            )
        '''))
        s.execute(text('''
            CREATE TABLE IF NOT EXISTS macros (
                   id SERIAL PRIMARY KEY,
                   user_id INTEGER,
                   protein REAL,
                   target_calories REAL,
                   carbs REAL,
                   fats REAL,
                   timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                   FOREIGN KEY (user_id) REFERENCES users(id)
            )
        '''))
        s.execute(text('''
                CREATE TABLE IF NOT EXISTS goals(
                   id SERIAL PRIMARY KEY,
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
        '''))
        s.execute(text('''
                CREATE TABLE IF NOT EXISTS user_progress(
                   id SERIAL PRIMARY KEY,
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
        '''))
        s.execute(text('''
                CREATE TABLE IF NOT EXISTS meal_plans(
                   id SERIAL PRIMARY KEY,
                   user_id INTEGER,
                   plan_type TEXT,
                   custom_note TEXT,
                   prompt TEXT,
                   meal_plan TEXT,
                   timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                   FOREIGN KEY (user_id) REFERENCES users(id)
                )
        '''))
        s.execute(text('''
                CREATE TABLE IF NOT EXISTS auth(
                   id SERIAL PRIMARY KEY,
                   username TEXT NOT NULL UNIQUE,
                   email TEXT NOT NULL UNIQUE,
                   password TEXT NOT NULL
                )
        '''))
        s.commit()


def insert_user(user):
    conn = create_connection()
    with conn.session as s:
        sql = text('''
            INSERT INTO users (name, age, gender, email, height, weight, goal, diet_preference, activity_level)
            VALUES (:name, :age, :gender, :email, :height, :weight, :goal, :diet, :activity)
            RETURNING id
        ''')
        params = {
            "name": user.name, "age": user.age, "gender": user.gender, "email": user.email, 
            "height": user.height, "weight": user.weight, "goal": user.goal, 
            "diet": user.diet_preference, "activity": user.activity_level
        }
        result = s.execute(sql, params)
        user_id = result.fetchone()[0]
        s.commit()
    return user_id

def update_user(user):
    conn = create_connection()
    with conn.session as s:
        sql = text('''
            UPDATE users 
            SET name = :name, age = :age, gender = :gender, email = :email, height = :height, 
                weight = :weight, goal = :goal, diet_preference = :diet, activity_level = :activity
            WHERE id = :id
        ''')
        params = {
            "name": user.name, "age": user.age, "gender": user.gender, "email": user.email,
            "height": user.height, "weight": user.weight, "goal": user.goal,
            "diet": user.diet_preference, "activity": user.activity_level, "id": user.id
        }
        s.execute(sql, params)
        s.commit()


def insert_calculations(user_id, tdee, bmi, bmi_category, water):
    conn = create_connection()
    with conn.session as s:
        sql = text('''
            INSERT INTO calculations (user_id, tdee, bmi, bmi_category, water_intake)
            VALUES (:uid, :tdee, :bmi, :cat, :water)
        ''')
        s.execute(sql, {"uid": user_id, "tdee": tdee, "bmi": bmi, "cat": bmi_category, "water": water})
        s.commit()

def insert_macros(user_id, protein, target_calories, carbs, fats):
    conn = create_connection()
    with conn.session as s:
        sql = text('''
            INSERT INTO macros(user_id, protein, target_calories, carbs, fats)
            VALUES (:uid, :prot, :cal, :carbs, :fats)
        ''')
        s.execute(sql, {"uid": user_id, "prot": protein, "cal": target_calories, "carbs": carbs, "fats": fats})
        s.commit()


def insert_goal(user_id, goal_type, target_weight, target_time_months, daily_change, target_calories, warning):
    conn = create_connection()
    with conn.session as s:
        sql = text('''
            INSERT INTO goals(user_id, goal_type, target_weight, target_time_months, 
                              daily_calorie_change, target_calories, health_warning)
            VALUES (:uid, :type, :tw, :months, :change, :cal, :warn)
        ''')
        s.execute(sql, {
            "uid": user_id, "type": goal_type, "tw": target_weight, "months": target_time_months,
            "change": daily_change, "cal": target_calories, "warn": warning
        })
        s.commit()


def insert_user_progress(user):
    conn = create_connection()
    with conn.session as s:
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        sql = text('''
            INSERT INTO user_progress(user_id, weight, height, age, goal, 
                                      diet_preference, activity_level, timestamp)
            VALUES (:uid, :weight, :height, :age, :goal, :diet, :activity, :ts)
        ''')
        s.execute(sql, {
            "uid": user.id, "weight": user.weight, "height": user.height, "age": user.age,
            "goal": user.goal, "diet": user.diet_preference, "activity": user.activity_level, "ts": timestamp
        })
        s.commit()


def insert_meal_plan(user_id, plan_type, custom_note, prompt, meal_plan):
    conn = create_connection()
    with conn.session as s:
        sql = text('''
            INSERT INTO meal_plans(user_id, plan_type, custom_note, prompt, meal_plan)
            VALUES (:uid, :type, :note, :prompt, :plan)
        ''')
        s.execute(sql, {
            "uid": user_id, "type": plan_type, "note": custom_note, 
            "prompt": prompt, "plan": meal_plan
        })
        s.commit()




