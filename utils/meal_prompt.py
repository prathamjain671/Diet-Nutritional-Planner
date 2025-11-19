def base_prompt(plan_type, user, target_calories, protein_goal, custom_note):
    note_content = custom_note.strip() if custom_note else "None"

    prompt = f"""
    **Role:** Act as an expert nutritionist and chef specializing in authentic Indian cuisine.
    
    **Task:** Create a detailed {plan_type} {user.diet_preference} meal plan for a user with the following profile:

    **User Profile:**
    - **Current Weight:** {user.weight} kg
    - **Fitness Goal:** {user.goal.capitalize()}
    - **Dietary Preference:** {user.diet_preference.capitalize()}
    - **Daily Calorie Target:** {target_calories} kcal (Strict Limit)
    - **Protein Goal:** {protein_goal} grams (High Priority)

    **Custom User Requests:**
    "{note_content}"
    *(Note: If this request conflicts with the diet type, prioritize the user's request but try to keep it healthy.)*

    **Meal Plan Guidelines:**
    1. **Structure:** Include Breakfast, Lunch, Dinner, and 1-2 Snacks.
    2. **Cuisine:** Focus on authentic Indian flavors using regional ingredients.
    3. **Balance:** Ensure meals are macronutrient-balanced but prioritize hitting the protein goal.
    4. **Clarity:** Dishes should be practical to cook at home.

    **Output Format (Use Markdown):**

    ### **Meal Plan Overview**
    *(Provide a 1-sentence summary of the day's eating philosophy)*

    ---
    
    ### **Breakfast**
    * **Meal Name:** [Name]
    * **Description:** [Brief appetizing description]
    * **Macros:** Protein: [X]g | Carbs: [X]g | Fats: [X]g | Calories: [X] kcal

    *(Repeat this format exactly for **Lunch**, **Snack 1**, **Dinner**, and **Snack 2**)*

    ---

    ### **Recipes & Preparation**
    *(For each complex meal above, provide the following)*
    
    #### **[Meal Name]**
    * **Prep Time:** [X] mins
    * **Ingredients:**
        * [Item 1]
        * [Item 2]
    * **Instructions:**
        1. [Step 1]
        2. [Step 2]

    ---

    ### **Daily Summary Table**
    | Metric | Total |
    | :--- | :--- |
    | **Calories** | [Total] |
    | **Protein** | [Total]g |
    | **Carbs** | [Total]g |
    | **Fats** | [Total]g |

    **Final Note:** If specific Indian ingredients are hard to find, suggest simple alternatives.
    """

    return prompt