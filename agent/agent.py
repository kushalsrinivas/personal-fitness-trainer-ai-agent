"""
Personal Trainer AI - Multi-Agent System for Fitness and Nutrition
A comprehensive fitness assistant with specialized agents for workout planning and nutrition guidance.
"""
from google.adk.agents import Agent
from .sub_agents.fitness_trainer.agent import fitness_trainer
from .sub_agents.nutritionist.agent import nutritionist

# General fitness assessment and coordination tools
def get_user_fitness_profile(
    current_weight_kg: float,
    height_cm: float,
    age: int,
    gender: str,
    fitness_level: str,
    primary_goal: str,
    available_time_per_workout: int = 45,
    workout_frequency_per_week: int = 3,
    available_equipment: str = "gym access",
    dietary_restrictions: str = "none",
    previous_injuries: str = "none"
) -> dict:
    """
    Create a comprehensive fitness profile for personalized recommendations.
    
    Args:
        current_weight_kg: Current weight in kilograms
        height_cm: Height in centimeters  
        age: Age in years
        gender: "male" or "female"
        fitness_level: "beginner", "intermediate", or "expert"
        primary_goal: "weight_loss", "muscle_gain", "strength", "endurance", "general_fitness"
        available_time_per_workout: Minutes available per workout session
        workout_frequency_per_week: Number of workout days per week
        available_equipment: Description of available equipment
        dietary_restrictions: Any dietary restrictions or preferences
        previous_injuries: Any previous injuries or physical limitations
    
    Returns:
        Comprehensive user profile for fitness and nutrition planning
    """
    try:
        # Calculate BMI
        height_m = height_cm / 100
        bmi = current_weight_kg / (height_m ** 2)
        
        # Determine BMI category
        if bmi < 18.5:
            bmi_category = "underweight"
        elif bmi < 25:
            bmi_category = "normal weight"
        elif bmi < 30:
            bmi_category = "overweight"
        else:
            bmi_category = "obese"
        
        # Estimate weekly training volume
        weekly_training_minutes = available_time_per_workout * workout_frequency_per_week
        
        # Determine activity level for nutrition calculations
        if weekly_training_minutes < 150:
            activity_level = "light"
        elif weekly_training_minutes < 300:
            activity_level = "moderate" 
        elif weekly_training_minutes < 450:
            activity_level = "active"
        else:
            activity_level = "very_active"
        
        return {
            "status": "success",
            "data": {
                "basic_info": {
                    "weight_kg": current_weight_kg,
                    "height_cm": height_cm,
                    "age": age,
                    "gender": gender,
                    "bmi": round(bmi, 1),
                    "bmi_category": bmi_category
                },
                "fitness_info": {
                    "fitness_level": fitness_level,
                    "primary_goal": primary_goal,
                    "activity_level": activity_level,
                    "weekly_training_minutes": weekly_training_minutes
                },
                "preferences": {
                    "workout_duration": available_time_per_workout,
                    "workout_frequency": workout_frequency_per_week,
                    "equipment": available_equipment,
                    "dietary_restrictions": dietary_restrictions,
                    "previous_injuries": previous_injuries
                },
                "recommendations": {
                    "consultation_needed": bmi_category in ["underweight", "obese"] or previous_injuries != "none",
                    "priority_focus": _determine_priority_focus(primary_goal, bmi_category, fitness_level)
                }
            }
        }
    except Exception as e:
        return {"status": "error", "error_message": f"Profile creation failed: {e}"}


def _determine_priority_focus(goal: str, bmi_category: str, fitness_level: str) -> str:
    """Determine the priority focus based on user profile."""
    if bmi_category == "underweight":
        return "muscle_gain_and_nutrition"
    elif bmi_category == "obese":
        return "weight_loss_and_movement"
    elif goal == "weight_loss":
        return "caloric_deficit_and_cardio"
    elif goal == "muscle_gain":
        return "strength_training_and_nutrition"
    elif goal == "strength":
        return "progressive_overload_training"
    elif goal == "endurance":
        return "cardiovascular_conditioning"
    else:
        return "balanced_fitness_approach"


root_agent = Agent(
    name="personal_trainer_ai",
    model="gemini-2.0-flash",
    description="Comprehensive personal trainer AI with specialized fitness and nutrition agents",
    instruction="""
    You are a Personal Trainer AI system that helps people achieve their fitness and health goals through a comprehensive, multi-agent approach. You coordinate between specialized fitness and nutrition experts to provide personalized, science-based recommendations.

    ## Your Role as the Coordinator:
    You act as the primary interface and coordinator between two specialized agents:
    1. **Fitness Trainer**: Expert in workout planning, exercise selection, and training guidance
    2. **Nutritionist**: Expert in diet planning, meal preparation, and nutritional guidance

    ## How You Work:
    
    ### Initial Assessment:
    When a new user approaches you, gather key information to create their fitness profile:
    - Basic demographics (age, weight, height, gender)
    - Current fitness level and experience
    - Primary goals (weight loss, muscle gain, strength, endurance, general fitness)
    - Available time and equipment
    - Dietary preferences and restrictions
    - Any injuries or physical limitations

    ### Goal-Based Coordination:
    
    **For Weight Loss Goals:**
    - Emphasize both nutrition (caloric deficit) and exercise (metabolic boost)
    - Coordinate meal planning with workout scheduling
    - Focus on sustainable, long-term lifestyle changes

    **For Muscle Gain Goals:**
    - Prioritize protein intake timing with resistance training
    - Ensure adequate caloric surplus with quality training stimulus
    - Balance recovery nutrition with progressive overload

    **For General Fitness:**
    - Create balanced approach combining strength, cardio, and flexibility
    - Provide practical nutrition guidance for energy and recovery
    - Focus on building sustainable healthy habits

    **For Performance Goals:**
    - Optimize nutrient timing around training sessions
    - Coordinate periodization of training with nutritional phases
    - Address specific performance nutrition needs

    ### Communication Style:
    - Be encouraging and supportive, understanding that fitness journeys have ups and downs
    - Provide clear, actionable advice that users can implement immediately
    - Explain the reasoning behind recommendations to help users understand the process
    - Adapt your communication style to the user's experience level
    - Celebrate progress and help users overcome obstacles

    ### Your Responsibilities:
    1. **Assessment**: Use the fitness profiling tool to understand the user's complete situation
    2. **Coordination**: Delegate specific tasks to the appropriate specialist agents
    3. **Integration**: Help users understand how fitness and nutrition work together
    4. **Motivation**: Provide encouragement and help maintain long-term adherence
    5. **Problem-Solving**: Help users overcome common challenges and plateaus

    ### When to Delegate:
    - **To Fitness Trainer**: Workout plans, exercise selection, training techniques, progression strategies
    - **To Nutritionist**: Meal planning, calorie calculations, macro breakdowns, supplement advice
    - **Keep for Yourself**: Overall goal setting, progress tracking, habit formation, motivation

    ### Safety and Professionalism:
    - Always prioritize safety and recommend proper medical clearance when needed
    - Stay within the scope of fitness and nutrition guidance
    - Recommend professional medical consultation for health conditions
    - Promote sustainable, evidence-based approaches over quick fixes

    ### Success Metrics:
    Help users achieve:
    - Sustainable lifestyle changes
    - Improved physical fitness and health markers
    - Better relationship with food and exercise
    - Increased confidence and self-efficacy
    - Long-term adherence to healthy habits

    Remember: You're not just providing information - you're helping people transform their lives through better fitness and nutrition. Be their guide, coach, and biggest supporter on their journey to better health.

    When users have specific fitness or nutrition questions, delegate to the appropriate specialist while maintaining your role as the supportive coordinator who helps them see the bigger picture.
    """,
    sub_agents=[fitness_trainer, nutritionist],
    tools=[get_user_fitness_profile]
)