def base_prompt(plan_type, user, target_calories, protein_goal, custom_note):

    prompt = f"""
    Design a {plan_type} {user.diet_preference} meal plan tailored for an individual with the following health metrics:

    - Daily calorie target: {target_calories} kcal
    - Daily protein goal: {protein_goal} grams
    - Weight: {user.weight} kg
    - Fitness goal: {user.goal.capitalize()}
    - Dietary preference: {user.diet_preference.capitalize()}

    The meal plan should include:
    - Breakfast
    - Lunch
    - Dinner
    - 1–2 snacks

    Ensure the meals:
    - Are high in protein to meet the daily goal
    - Reflect authentic Indian cuisine, using regional ingredients and traditional flavors
    - Are balanced with carbohydrates and fats to support the fitness goal
    - Stay within the daily calorie target

    Also remember to use this custom note and if it is empty, just proceed:
    {custom_note}

    Format the response as follows:
    - List each meal category (Breakfast, Lunch, Dinner, Snack 1, Snack 2) in bold
    - Under each category, provide:
      - A brief description of the meal
      - Approximate macronutrients (protein, carbs, fats) in grams for that specific meal
    - At the end of the meal plan, include a **Recipes** section in bold
      - For each meal, list:
        - The meal name
        - Ingredients with quantities
        - Step-by-step preparation instructions
    - Summarize total daily macronutrients (protein, carbs, fats) and calories at the end of the meal plan

    If specific dishes are unavailable or unclear, suggest alternatives that align with Indian culinary traditions and the dietary preference.
    """

    return prompt