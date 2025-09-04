from utils.db import insert_goal

def find_tdee(user):
    bmr = 0
    if user.gender == "male":
        bmr += (10 * user.weight) + (6.25 * user.height) - (5 * user.age) + 5
    elif user.gender == "female":
        bmr += (10 * user.weight) + (6.25 * user.height) - (5 * user.age) - 161
    else:
        return None

    if user.activity_level.lower() == "sedentary":
        tdee = bmr * 1.2
    elif user.activity_level.lower() == "lightly active":
        tdee = bmr * 1.375
    elif user.activity_level.lower() == "moderately active":
        tdee = bmr * 1.55
    elif user.activity_level.lower() == "active":
        tdee = bmr * 1.725
    elif user.activity_level.lower() == "very active":
        tdee = bmr * 1.9
    else:
        return None
    
    # return f"Based on your details, your Total Daily Energy Expenditure (TDEE) is approximately: {tdee} calories/day."
    return tdee


def find_bmi(user):
    bmi = user.weight / ((user.height / 100) * (user.height / 100))
    if bmi < 18.5:
        bmi_category = "underweight"
    elif 18.5 <= bmi <= 24.9:
        bmi_category = "healthy weight"
    elif 25 <= bmi <= 29.9:
        bmi_category = "overweight"
    elif 30 <= bmi < 35:
        bmi_category = "class 1 obesity"
    elif 35 <= bmi < 40:
        bmi_category = "class 2 obesity"
    elif bmi > 40:
        bmi_category = "class 3 obesity"

    # return f"Based on your details, your Body Mass Index (BMI) is {bmi} which falls under {bmi_category.capitalize()} category."
    return bmi,bmi_category


def protein_intake(user):
    if user.goal.lower() == "weight loss":
        factor = 1.9
    elif user.goal.lower() == "weight gain":
        factor = 1.8
    elif user.goal.lower() == "muscle gain":
        factor = 2.0
    elif user.goal.lower() == "maintenance":
        factor = 1.4

    protein = user.weight * factor

    # return f"Based on your details, your daily protein intake should be {protein}g."
    return protein


def weight_loss(user, target_weight=None, months=None):
    weight_loss_needed = user.weight - target_weight
    days = months * 30
    total_calorie_deficit = weight_loss_needed * 7700      # As 1kg of fat = 7700 cal
    daily_deficit = total_calorie_deficit / days
    tdee = find_tdee(user)
    target_calories = tdee - daily_deficit

    warning = None

    if user.gender.lower() == "male":  
        if target_calories < 1500:
            warning = (
                f"\nYour goal may be unhealthy.\n"
                f"You'd need to eat only {int(target_calories)} kcal/day which is too low.\n"
                f"At a healthy intake of 1500 kcal/day, it would take "
                f"{int(total_calorie_deficit / (tdee - 1500))} days to reach your goal."
            )
        else:
            message = (
                f"To reach your goal in {days} days, you need a daily deficit of {int(daily_deficit)} kcal.\n"
                f"Your target intake is {int(target_calories)} kcal/day."
            )
    elif user.gender.lower() == "female":
        if target_calories < 1200:
            warning = (
                f"\nYour goal may be unhealthy.\n"
                f"You'd need to eat only {int(target_calories)} kcal/day which is too low.\n"
                f"At a healthy intake of 1200 kcal/day, it would take "
                f"{int(total_calorie_deficit / (tdee - 1200))} days to reach your goal."
            )
        else:
            message = (
                f"To reach your goal in {days} days, you need a daily deficit of {int(daily_deficit)} kcal.\n"
                f"Your target intake is {int(target_calories)} kcal/day."
            )

    insert_goal(user.id, "loss", target_weight, months, daily_deficit, target_calories, warning)
    
    return warning if warning else message


def weight_gain(user, target_weight, months):
    weight_gain_needed = target_weight - user.weight
    days = months * 30
    total_calorie_surplus = weight_gain_needed * 7700
    daily_surplus = total_calorie_surplus / days
    tdee = find_tdee(user)
    target_calories = tdee + daily_surplus

    warning = None

    if daily_surplus > 1000:
        warning = (
            f"\nYour required daily surplus is {int(daily_surplus)} kcal, which is quite high.\n"
            f"Gaining weight this quickly might lead to excess fat gain rather than muscle.\n"
            f"Consider extending your goal duration.\n"
            f"At a healthier surplus of 500 kcal/day, it would take about "
            f"{int(total_calorie_surplus / 500)} days (~{int((total_calorie_surplus / 500) / 30)} months) "
            f"to reach your goal.\n\n"
            f"Still, if you proceed, your target intake would be {int(target_calories)} kcal/day."
        )
    else:
        message = (
            f"To reach your goal in {days} days, you need a daily surplus of {int(daily_surplus)} kcal.\n"
            f"Your target intake is {int(target_calories)} kcal/day."
        )
    
    insert_goal(user.id, "gain", target_weight, months, daily_surplus, target_calories, warning)

    return warning if warning else message


def calculate_macros(user):
    target_calories = find_tdee(user)

    if user.goal.lower() == "weight loss":
        protein_ratio = 0.40
        carb_ratio = 0.30
        fat_ratio = 0.30
    elif user.goal.lower() == "muscle gain":
        protein_ratio = 0.30
        carb_ratio = 0.50
        fat_ratio = 0.20
    elif user.goal.lower() == "weight gain":
        protein_ratio = 0.25
        carb_ratio = 0.55
        fat_ratio = 0.20
    else:  
        protein_ratio = 0.30
        carb_ratio = 0.40
        fat_ratio = 0.30
    
    protein_grams = (target_calories * protein_ratio) / 4
    carb_grams = (target_calories * carb_ratio) / 4
    fat_grams = (target_calories * fat_ratio) / 9

    return {
        "Target Calories" : int(target_calories),
        "Protein (g)" : int(protein_grams),
        "Carbs (g)" : int(carb_grams),
        "Fats (g)" : int(fat_grams)
    }


def water_intake(user):
    daily_water_ml = user.weight * 35
    daily_water_l = daily_water_ml / 1000

    return daily_water_l