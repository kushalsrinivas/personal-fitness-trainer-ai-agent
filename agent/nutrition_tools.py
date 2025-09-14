"""
Nutrition and diet planning tools for the personal trainer AI system.
"""
from typing import Any, Dict, List, Optional
import random


# Comprehensive nutrition database
NUTRITION_DATABASE = {
    "proteins": {
        "lean_meats": [
            {"name": "Chicken Breast", "calories_per_100g": 165, "protein": 31, "carbs": 0, "fat": 3.6, "prep_time": 15},
            {"name": "Turkey Breast", "calories_per_100g": 135, "protein": 30, "carbs": 0, "fat": 1, "prep_time": 15},
            {"name": "Lean Beef", "calories_per_100g": 250, "protein": 26, "carbs": 0, "fat": 15, "prep_time": 20},
            {"name": "Salmon", "calories_per_100g": 208, "protein": 25, "carbs": 0, "fat": 12, "prep_time": 12},
            {"name": "Tuna", "calories_per_100g": 132, "protein": 28, "carbs": 0, "fat": 1, "prep_time": 5},
        ],
        "dairy": [
            {"name": "Greek Yogurt", "calories_per_100g": 97, "protein": 10, "carbs": 4, "fat": 5, "prep_time": 0},
            {"name": "Cottage Cheese", "calories_per_100g": 98, "protein": 11, "carbs": 3.4, "fat": 4.3, "prep_time": 0},
            {"name": "Milk (2%)", "calories_per_100g": 50, "protein": 3.4, "carbs": 5, "fat": 2, "prep_time": 0},
        ],
        "plant_based": [
            {"name": "Tofu", "calories_per_100g": 76, "protein": 8, "carbs": 1.9, "fat": 4.8, "prep_time": 10},
            {"name": "Lentils", "calories_per_100g": 116, "protein": 9, "carbs": 20, "fat": 0.4, "prep_time": 25},
            {"name": "Chickpeas", "calories_per_100g": 164, "protein": 8.9, "carbs": 27, "fat": 2.6, "prep_time": 20},
            {"name": "Quinoa", "calories_per_100g": 120, "protein": 4.4, "carbs": 22, "fat": 1.9, "prep_time": 15},
        ]
    },
    "carbohydrates": {
        "complex": [
            {"name": "Brown Rice", "calories_per_100g": 123, "protein": 2.6, "carbs": 25, "fat": 0.9, "prep_time": 25},
            {"name": "Sweet Potato", "calories_per_100g": 86, "protein": 1.6, "carbs": 20, "fat": 0.1, "prep_time": 25},
            {"name": "Oats", "calories_per_100g": 68, "protein": 2.4, "carbs": 12, "fat": 1.4, "prep_time": 5},
            {"name": "Whole Wheat Bread", "calories_per_100g": 247, "protein": 13, "carbs": 41, "fat": 4.2, "prep_time": 0},
        ],
        "fruits": [
            {"name": "Banana", "calories_per_100g": 89, "protein": 1.1, "carbs": 23, "fat": 0.3, "prep_time": 0},
            {"name": "Apple", "calories_per_100g": 52, "protein": 0.3, "carbs": 14, "fat": 0.2, "prep_time": 0},
            {"name": "Berries (mixed)", "calories_per_100g": 57, "protein": 0.7, "carbs": 14, "fat": 0.3, "prep_time": 0},
        ]
    },
    "fats": {
        "healthy": [
            {"name": "Avocado", "calories_per_100g": 160, "protein": 2, "carbs": 9, "fat": 15, "prep_time": 2},
            {"name": "Nuts (mixed)", "calories_per_100g": 607, "protein": 20, "carbs": 22, "fat": 54, "prep_time": 0},
            {"name": "Olive Oil", "calories_per_100g": 884, "protein": 0, "carbs": 0, "fat": 100, "prep_time": 0},
            {"name": "Seeds (chia/flax)", "calories_per_100g": 486, "protein": 17, "carbs": 42, "fat": 31, "prep_time": 0},
        ]
    },
    "vegetables": [
        {"name": "Broccoli", "calories_per_100g": 34, "protein": 2.8, "carbs": 7, "fat": 0.4, "prep_time": 8},
        {"name": "Spinach", "calories_per_100g": 23, "protein": 2.9, "carbs": 3.6, "fat": 0.4, "prep_time": 3},
        {"name": "Bell Peppers", "calories_per_100g": 31, "protein": 1, "carbs": 7, "fat": 0.3, "prep_time": 5},
        {"name": "Carrots", "calories_per_100g": 41, "protein": 0.9, "carbs": 10, "fat": 0.2, "prep_time": 5},
        {"name": "Cucumber", "calories_per_100g": 16, "protein": 0.7, "carbs": 4, "fat": 0.1, "prep_time": 2},
    ]
}

MEAL_TEMPLATES = {
    "weight_loss": {
        "breakfast": ["protein", "complex_carbs", "healthy_fats"],
        "lunch": ["lean_protein", "vegetables", "complex_carbs"],
        "dinner": ["lean_protein", "vegetables", "minimal_carbs"],
        "snacks": ["protein", "fruits"]
    },
    "muscle_gain": {
        "breakfast": ["protein", "complex_carbs", "healthy_fats"],
        "lunch": ["protein", "complex_carbs", "vegetables"],
        "dinner": ["protein", "complex_carbs", "vegetables"],
        "snacks": ["protein", "nuts", "fruits"]
    },
    "maintenance": {
        "breakfast": ["protein", "complex_carbs"],
        "lunch": ["balanced_protein", "vegetables", "complex_carbs"],
        "dinner": ["protein", "vegetables", "moderate_carbs"],
        "snacks": ["fruits", "nuts"]
    }
}


def calculate_daily_calories(
    weight_kg: float,
    height_cm: float,
    age: int,
    gender: str,
    activity_level: str,
    goal: str = "maintenance"
) -> Dict[str, Any]:
    """
    Calculate daily caloric needs using Mifflin-St Jeor equation.
    
    Args:
        weight_kg: Current weight in kg
        height_cm: Height in centimeters
        age: Age in years
        gender: "male" or "female"
        activity_level: sedentary, light, moderate, active, very_active
        goal: weight_loss, muscle_gain, or maintenance
    
    Returns:
        Dictionary with caloric requirements and macronutrient breakdown
    """
    try:
        # Basal Metabolic Rate (BMR) calculation
        if gender.lower() == "male":
            bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
        else:
            bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
        
        # Activity multipliers
        activity_multipliers = {
            "sedentary": 1.2,
            "light": 1.375,
            "moderate": 1.55,
            "active": 1.725,
            "very_active": 1.9
        }
        
        tdee = bmr * activity_multipliers.get(activity_level, 1.55)
        
        # Goal adjustments
        if goal == "weight_loss":
            target_calories = tdee - 500  # 1 lb per week loss
        elif goal == "muscle_gain":
            target_calories = tdee + 300  # Moderate surplus
        else:
            target_calories = tdee
        
        # Macronutrient calculations
        if goal == "muscle_gain":
            protein_ratio = 0.30
            carb_ratio = 0.40
            fat_ratio = 0.30
        elif goal == "weight_loss":
            protein_ratio = 0.35
            carb_ratio = 0.30
            fat_ratio = 0.35
        else:
            protein_ratio = 0.25
            carb_ratio = 0.45
            fat_ratio = 0.30
        
        protein_calories = target_calories * protein_ratio
        carb_calories = target_calories * carb_ratio
        fat_calories = target_calories * fat_ratio
        
        return {
            "status": "success",
            "data": {
                "bmr": round(bmr),
                "tdee": round(tdee),
                "target_calories": round(target_calories),
                "macronutrients": {
                    "protein": {
                        "calories": round(protein_calories),
                        "grams": round(protein_calories / 4),
                        "percentage": round(protein_ratio * 100)
                    },
                    "carbohydrates": {
                        "calories": round(carb_calories),
                        "grams": round(carb_calories / 4),
                        "percentage": round(carb_ratio * 100)
                    },
                    "fats": {
                        "calories": round(fat_calories),
                        "grams": round(fat_calories / 9),
                        "percentage": round(fat_ratio * 100)
                    }
                },
                "goal": goal,
                "activity_level": activity_level
            }
        }
    except Exception as e:
        return {"status": "error", "error_message": f"Calorie calculation failed: {e}"}


def create_meal_plan(
    target_calories: int,
    goal: str = "maintenance",
    dietary_restrictions: Optional[List[str]] = None,
    meals_per_day: int = 3,
    days: int = 1
) -> Dict[str, Any]:
    """
    Create a personalized meal plan.
    
    Args:
        target_calories: Daily caloric target
        goal: weight_loss, muscle_gain, or maintenance
        dietary_restrictions: List of restrictions (vegetarian, vegan, gluten_free, etc.)
        meals_per_day: Number of meals per day (3-6)
        days: Number of days to plan for
    
    Returns:
        Dictionary with complete meal plan
    """
    try:
        dietary_restrictions = dietary_restrictions or []
        
        # Calorie distribution across meals
        if meals_per_day == 3:
            meal_distribution = [0.25, 0.45, 0.30]  # breakfast, lunch, dinner
        elif meals_per_day == 4:
            meal_distribution = [0.25, 0.35, 0.25, 0.15]  # + snack
        elif meals_per_day == 5:
            meal_distribution = [0.20, 0.10, 0.35, 0.10, 0.25]  # + 2 snacks
        else:
            meal_distribution = [0.20, 0.10, 0.30, 0.10, 0.20, 0.10]  # 6 meals
        
        meal_plan = []
        
        for day in range(days):
            daily_meals = []
            
            for meal_index, calorie_percentage in enumerate(meal_distribution):
                meal_calories = int(target_calories * calorie_percentage)
                
                # Determine meal type
                if meal_index == 0:
                    meal_type = "Breakfast"
                elif meal_index == len(meal_distribution) - 1:
                    meal_type = "Dinner"
                elif "lunch" in MEAL_TEMPLATES.get(goal, {}) and meal_index == 1:
                    meal_type = "Lunch"
                else:
                    meal_type = "Snack"
                
                # Create meal
                meal = _create_single_meal(
                    meal_calories, 
                    goal, 
                    meal_type.lower(), 
                    dietary_restrictions
                )
                
                daily_meals.append({
                    "meal_type": meal_type,
                    "target_calories": meal_calories,
                    "foods": meal["foods"],
                    "total_calories": meal["total_calories"],
                    "macronutrients": meal["macronutrients"]
                })
            
            meal_plan.append({
                "day": day + 1,
                "meals": daily_meals,
                "daily_totals": _calculate_daily_totals(daily_meals)
            })
        
        return {
            "status": "success",
            "data": {
                "meal_plan": meal_plan,
                "target_calories": target_calories,
                "goal": goal,
                "dietary_restrictions": dietary_restrictions,
                "days": days
            }
        }
    except Exception as e:
        return {"status": "error", "error_message": f"Meal plan creation failed: {e}"}


def _create_single_meal(
    target_calories: int, 
    goal: str, 
    meal_type: str, 
    restrictions: List[str]
) -> Dict[str, Any]:
    """Create a single balanced meal."""
    foods = []
    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0
    
    # Get meal template
    template = MEAL_TEMPLATES.get(goal, MEAL_TEMPLATES["maintenance"])
    meal_components = template.get(meal_type, ["protein", "carbs", "vegetables"])
    
    remaining_calories = target_calories
    
    for component in meal_components:
        if remaining_calories <= 0:
            break
        
        # Allocate calories for this component
        if component in ["protein", "lean_protein", "balanced_protein"]:
            component_calories = min(remaining_calories * 0.3, remaining_calories)
            food_items = _get_foods_by_type("proteins", restrictions)
        elif component in ["complex_carbs", "carbs", "moderate_carbs", "minimal_carbs"]:
            if "minimal" in component:
                component_calories = min(remaining_calories * 0.15, remaining_calories)
            elif "moderate" in component:
                component_calories = min(remaining_calories * 0.25, remaining_calories)
            else:
                component_calories = min(remaining_calories * 0.4, remaining_calories)
            food_items = _get_foods_by_type("carbohydrates", restrictions)
        elif component in ["healthy_fats", "fats"]:
            component_calories = min(remaining_calories * 0.25, remaining_calories)
            food_items = _get_foods_by_type("fats", restrictions)
        elif component == "vegetables":
            component_calories = min(remaining_calories * 0.2, remaining_calories)
            food_items = NUTRITION_DATABASE["vegetables"]
        elif component in ["fruits", "nuts"]:
            component_calories = min(remaining_calories * 0.15, remaining_calories)
            if component == "fruits":
                food_items = NUTRITION_DATABASE["carbohydrates"]["fruits"]
            else:
                food_items = [item for item in NUTRITION_DATABASE["fats"]["healthy"] if "nuts" in item["name"].lower()]
        else:
            continue
        
        # Select a food item
        if food_items:
            food = random.choice(food_items)
            # Calculate portion size
            portion_size = component_calories / food["calories_per_100g"] * 100
            
            foods.append({
                "name": food["name"],
                "portion_grams": round(portion_size, 1),
                "calories": round(component_calories),
                "protein": round(food["protein"] * portion_size / 100, 1),
                "carbs": round(food["carbs"] * portion_size / 100, 1),
                "fat": round(food["fat"] * portion_size / 100, 1),
                "prep_time": food["prep_time"]
            })
            
            total_calories += component_calories
            total_protein += food["protein"] * portion_size / 100
            total_carbs += food["carbs"] * portion_size / 100
            total_fat += food["fat"] * portion_size / 100
            remaining_calories -= component_calories
    
    return {
        "foods": foods,
        "total_calories": round(total_calories),
        "macronutrients": {
            "protein": round(total_protein, 1),
            "carbohydrates": round(total_carbs, 1),
            "fat": round(total_fat, 1)
        }
    }


def _get_foods_by_type(food_type: str, restrictions: List[str]) -> List[Dict[str, Any]]:
    """Get foods of a specific type, filtered by dietary restrictions."""
    all_foods = []
    
    if food_type == "proteins":
        all_foods.extend(NUTRITION_DATABASE["proteins"]["lean_meats"])
        if "vegetarian" not in restrictions and "vegan" not in restrictions:
            all_foods.extend(NUTRITION_DATABASE["proteins"]["dairy"])
        if "vegan" in restrictions or "vegetarian" in restrictions:
            all_foods.extend(NUTRITION_DATABASE["proteins"]["plant_based"])
    elif food_type == "carbohydrates":
        all_foods.extend(NUTRITION_DATABASE["carbohydrates"]["complex"])
        all_foods.extend(NUTRITION_DATABASE["carbohydrates"]["fruits"])
    elif food_type == "fats":
        all_foods.extend(NUTRITION_DATABASE["fats"]["healthy"])
    
    # Apply restrictions
    if "vegan" in restrictions:
        # Remove animal products
        all_foods = [f for f in all_foods if f["name"] not in 
                    ["Chicken Breast", "Turkey Breast", "Lean Beef", "Salmon", "Tuna", 
                     "Greek Yogurt", "Cottage Cheese", "Milk (2%)"]]
    elif "vegetarian" in restrictions:
        # Remove meat/fish but keep dairy
        all_foods = [f for f in all_foods if f["name"] not in 
                    ["Chicken Breast", "Turkey Breast", "Lean Beef", "Salmon", "Tuna"]]
    
    if "gluten_free" in restrictions:
        all_foods = [f for f in all_foods if "Wheat" not in f["name"]]
    
    return all_foods


def _calculate_daily_totals(meals: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate daily nutritional totals from meals."""
    total_calories = sum(meal["total_calories"] for meal in meals)
    total_protein = sum(meal["macronutrients"]["protein"] for meal in meals)
    total_carbs = sum(meal["macronutrients"]["carbohydrates"] for meal in meals)
    total_fat = sum(meal["macronutrients"]["fat"] for meal in meals)
    
    return {
        "calories": total_calories,
        "protein": round(total_protein, 1),
        "carbohydrates": round(total_carbs, 1),
        "fat": round(total_fat, 1)
    }


def get_nutrition_recommendations(goal: str, activity_level: str) -> Dict[str, Any]:
    """Get general nutrition recommendations based on goals."""
    try:
        recommendations = {
            "weight_loss": {
                "key_principles": [
                    "Create a moderate caloric deficit (300-500 calories below maintenance)",
                    "Prioritize protein to preserve muscle mass during weight loss",
                    "Include plenty of fiber-rich vegetables to feel full",
                    "Stay hydrated - drink water before meals",
                    "Practice portion control and mindful eating"
                ],
                "meal_timing": "Eat 3-4 meals per day with focus on protein at each meal",
                "supplements": ["Multivitamin", "Protein powder if needed", "Omega-3"],
                "avoid": ["Highly processed foods", "Sugary drinks", "Large portions"]
            },
            "muscle_gain": {
                "key_principles": [
                    "Maintain a moderate caloric surplus (200-400 calories above maintenance)",
                    "Consume 1.6-2.2g protein per kg body weight",
                    "Include complex carbohydrates around workouts",
                    "Don't neglect healthy fats for hormone production",
                    "Eat frequently throughout the day"
                ],
                "meal_timing": "5-6 meals per day, protein every 3-4 hours",
                "supplements": ["Whey protein", "Creatine", "Multivitamin"],
                "avoid": ["Skipping meals", "Too much cardio", "Dirty bulking"]
            },
            "maintenance": {
                "key_principles": [
                    "Balance caloric intake with expenditure",
                    "Focus on nutrient-dense whole foods",
                    "Include variety in your diet",
                    "Practice the 80/20 rule - healthy 80% of the time",
                    "Listen to your body's hunger and fullness cues"
                ],
                "meal_timing": "3-4 balanced meals per day",
                "supplements": ["Multivitamin", "Vitamin D", "Omega-3"],
                "avoid": ["Extreme restrictions", "All-or-nothing mentality"]
            }
        }
        
        base_recs = recommendations.get(goal, recommendations["maintenance"])
        
        # Activity-specific modifications
        if activity_level in ["active", "very_active"]:
            base_recs["key_principles"].append("Increase carbohydrate intake to fuel workouts")
            base_recs["key_principles"].append("Focus on post-workout recovery nutrition")
        
        return {
            "status": "success",
            "data": {
                "goal": goal,
                "activity_level": activity_level,
                "recommendations": base_recs
            }
        }
    except Exception as e:
        return {"status": "error", "error_message": f"Failed to get recommendations: {e}"}


def analyze_food_item(food_name: str, portion_size: float = 100) -> Dict[str, Any]:
    """Analyze nutritional content of a specific food item."""
    try:
        # Search through all food categories
        found_food = None
        
        for category in NUTRITION_DATABASE.values():
            if isinstance(category, dict):
                for subcategory in category.values():
                    if isinstance(subcategory, list):
                        for food in subcategory:
                            if food_name.lower() in food["name"].lower():
                                found_food = food
                                break
            elif isinstance(category, list):
                for food in category:
                    if food_name.lower() in food["name"].lower():
                        found_food = food
                        break
            
            if found_food:
                break
        
        if not found_food:
            return {"status": "error", "error_message": f"Food '{food_name}' not found in database"}
        
        # Calculate nutrition for specified portion
        multiplier = portion_size / 100
        
        return {
            "status": "success",
            "data": {
                "food_name": found_food["name"],
                "portion_size_grams": portion_size,
                "nutrition": {
                    "calories": round(found_food["calories_per_100g"] * multiplier, 1),
                    "protein": round(found_food["protein"] * multiplier, 1),
                    "carbohydrates": round(found_food["carbs"] * multiplier, 1),
                    "fat": round(found_food["fat"] * multiplier, 1)
                },
                "prep_time_minutes": found_food["prep_time"]
            }
        }
    except Exception as e:
        return {"status": "error", "error_message": f"Food analysis failed: {e}"}
