# Diet & Nutritional Planner

A comprehensive web application built with Streamlit that helps users track their nutrition, set weight goals, and generate personalized meal plans using AI. This intelligent health companion provides science-based calculations for TDEE, BMI, macronutrients, and water intake while offering AI-powered meal planning through Google Gemini or OpenAI ChatGPT.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.51.0-FF4B4B.svg)

---

## ✨ Key Features

🔐 ###Secure Authentication###: User registration and login system with secure password hashing (bcrypt).

🏠 ###Interactive Dashboard###: A central hub displaying real-time key metrics (Current Weight, Target Calories, Protein Goal) and visual progress charts.

🤖 ###AI Meal Planner###: Generate daily or weekly meal plans tailored to your macros and cuisine preferences using Google Gemini or OpenAI models.

🧮 ###Health Calculators###: Automatically calculates TDEE (Total Daily Energy Expenditure), BMI, and optimal macronutrient splits based on your profile.

⚖️ ###Goal Tracking###: Set specific weight loss or gain goals with realistic timelines. The app tracks your progress against these targets.

📈 ###Progress Visualization###: View interactive charts (Altair) for weight trends, BMI changes, and TDEE fluctuations over time.

🥕 ###Food Info Database###: A built-in nutritional lookup tool for common food items (specifically tailored for Indian cuisine).

👤 ###Profile Management###: Easily update your physical stats, activity levels, and dietary preferences to keep your plan accurate.  

---

## 🚀 Installation Instructions

### Prerequisites

Before you begin, ensure you have the following installed:
- **Python 3.8 or higher** ([Download Python](https://www.python.org/downloads/))
- **pip** (Python package manager, comes with Python)
- **PostgreSQL** database (local or cloud-based)
- **Git** (optional, for cloning the repository)

### Step 1: Clone or Download the Repository

```bash
# Using Git
git clone https://github.com/prathamjain671/Digital-Diet-Nutritional-Planner.git
cd Digital-Diet-Nutritional-Planner

# Or download and extract the ZIP file from GitHub
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up PostgreSQL Database

1. **Install PostgreSQL** if not already installed ([Download here](https://www.postgresql.org/download/))

2. **Create a new database:**
   ```sql
   CREATE DATABASE diet_planner;
   ```

3. **Create a database user** (optional but recommended):
   ```sql
   CREATE USER diet_user WITH PASSWORD 'your_secure_password';
   GRANT ALL PRIVILEGES ON DATABASE diet_planner TO diet_user;
   ```

### Step 5: Configure Database Connection

Create a `.streamlit/secrets.toml` file in the project root:

```bash
mkdir -p .streamlit
touch .streamlit/secrets.toml  # On Windows: type nul > .streamlit\secrets.toml
```

Add your database credentials to `.streamlit/secrets.toml`:

```toml
[connections.db]
dialect = "postgresql"
host = "localhost"
port = 5432
database = "diet_planner"
username = "diet_user"
password = "your_secure_password"
```

**Note:** This file is already in `.gitignore` and will not be committed to version control.

### Step 6: Prepare Food Database (Optional)

The application includes a food database CSV. Ensure `data/food_db.csv` exists. If you have a different CSV file name, update the path in `views/Food_Info.py`:

```python
df = pd.read_csv("data/food_db.csv")  # Update this path if needed
```

### Step 7: Run the Application

```bash
streamlit run App.py
```

The application will open in your default browser at `http://localhost:8501`.

### Step 8: Get API Keys for Meal Planning

To use the AI meal planner, you'll need at least one API key:

#### **Option 1: [Google Gemini](https://aistudio.google.com/app/apikey) (Recommended - Free Tier Available)**

#### **Option 2: [OpenAI ChatGPT](https://platform.openai.com/api-keys)**

**Note:** API keys are not stored permanently and must be entered each session for security.

---

⚙️ Installation Instructions
Follow these steps to set up the project locally on your machine.

Prerequisites
Python 3.8+ installed.

A PostgreSQL Database (You can use a free cloud provider like Neon.tech or a local Postgres instance).

1. Clone the Repository
Bash

git clone https://github.com/your-username/diet-nutritional-planner.git
cd diet-nutritional-planner
2. Create a Virtual Environment (Recommended)
Bash

# Windows
python -m venv .venv
.\.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
3. Install Dependencies
Bash

pip install -r requirements.txt
4. Set Up Database Secrets
Streamlit needs your database connection string to connect to PostgreSQL.

Create a folder named .streamlit in the root directory.

Inside it, create a file named secrets.toml.

Add your PostgreSQL connection string:

Ini, TOML

# .streamlit/secrets.toml
[connections.db]
dialect = "postgresql"
url = "postgresql://username:password@host:port/database_name"
(Note: Ensure your URL starts with postgresql:// and consider adding ?sslmode=require if using a cloud provider).

5. Run the Application
Bash

streamlit run App.py
The application will automatically create the necessary database tables on the first run.

🛠️ Tech Stack
This project is built using a robust and modern stack:

- Frontend/Framework: Streamlit (Python-based web framework)

- Database: PostgreSQL (Hosted on Cloud)

- ORM/Connection: SQLAlchemy & st.connection

- Data Processing: Pandas

- Data Visualization: Altair (Interactive charts)

- ##Generative AI:

    - google-generativeai (Gemini Pro / Flash)

    - openai (GPT-4o / GPT-4o-mini)

- Authentication: bcrypt (Secure password hashing)

- Styling: Custom CSS injection for a polished, dark-themed UI
---

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### Reporting Bugs

If you find a bug, please create an issue on GitHub with:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior vs. actual behavior
- Screenshots (if applicable)
- Your environment details (OS, Python version, browser)

### Suggesting Enhancements

Have an idea for a new feature? Open an issue with:
- A clear description of the feature
- Why it would be useful
- Any implementation ideas you have

---

## 📋 Roadmap

Planned features and improvements:

- [ ] **Export Reports:** Download progress reports as PDF
- [ ] **Social Features:** Share meal plans and progress with friends
- [ ] **Recipe Database:** Add full recipes, not just nutritional info
- [ ] **Exercise Tracking:** Integrate workout logging and calorie burn
- [ ] **Multi-language Support:** Internationalization for global users
- [ ] **Email Notifications:** Reminders for weight logging and meal planning
- [ ] **Integration with Fitness Trackers:** Sync with Fitbit, Apple Health, etc.

---

## 🐛 Known Issues

- **API Key Persistence:** API keys must be re-entered each session for security
- **Large Database Performance:** Very large food databases (>10,000 items) may slow search
- **Chart Rendering:** Some older browsers may have issues with Altair charts

---

## ⭐ Star This Repository

If you find this project helpful, please consider giving it a star on GitHub! It helps others discover the project and motivates further development.

---

**Made with ❤️ by [Pratham Jain](https://github.com/prathamjain671)**

*Last Updated: November 2025*
