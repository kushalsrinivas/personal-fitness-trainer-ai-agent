# Personal Trainer AI - Multi-Agent Fitness & Nutrition System

A sophisticated multi-agent AI system built with Google's Agent Development Kit (ADK) that provides personalized fitness training and nutrition guidance. This system combines the expertise of specialized AI agents to deliver comprehensive health and fitness recommendations for any average joe looking to work on their body.

## 🏋️ System Overview

This AI personal trainer system uses a multi-agent architecture with three specialized agents:

1. **🎯 Personal Trainer AI (Manager Agent)**: Coordinates between specialists and provides overall guidance
2. **💪 Fitness Trainer Agent**: Expert in workout planning, exercise selection, and training programs
3. **🥗 Nutritionist Agent**: Expert in diet planning, meal preparation, and nutritional guidance

## ✨ Key Features

### 🏃‍♂️ Comprehensive Fitness Training

- **800+ Exercise Database**: Access to extensive exercise library with detailed instructions
- **Personalized Workout Plans**: Custom routines based on fitness level, goals, and available equipment
- **Multiple Training Categories**: Strength (581), Stretching (123), Plyometrics (61), Powerlifting (38), Olympic Weightlifting (35), Strongman (21), Cardio (14)
- **All Fitness Levels**: Beginner (523 exercises), Intermediate (293), Expert (57)
- **Equipment Flexibility**: Bodyweight, gym equipment, or home workout options

### 🍎 Intelligent Nutrition Planning

- **Caloric Needs Calculation**: Science-based BMR and TDEE calculations using Mifflin-St Jeor equation
- **Personalized Meal Plans**: Custom meal plans for weight loss, muscle gain, or maintenance
- **Dietary Accommodations**: Vegetarian, vegan, gluten-free, and other dietary restrictions
- **Comprehensive Food Database**: Lean proteins, complex carbs, healthy fats, and vegetables
- **Macro Tracking**: Detailed protein, carbohydrate, and fat breakdowns

### 🎨 Smart Coordination

- **Goal-Based Recommendations**: Integrated fitness and nutrition plans aligned with your objectives
- **Progress Tracking**: BMI calculation and fitness level assessment
- **Safety First**: Medical consultation recommendations when needed
- **Sustainable Approach**: Evidence-based, long-term lifestyle changes

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google ADK installed
- Required dependencies (see requirements.txt)

### Installation & Setup

1. **Clone and navigate to the project:**

   ```bash
   cd /path/to/adk-agent-server-ready-template
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Start the ADK server:**

   ```bash
   python server.py
   ```

4. **Access the web interface:**
   Open your browser to `http://localhost:8080`

## 💬 How to Use

### Getting Started

1. **Initial Assessment**: Provide your basic information (age, weight, height, fitness level, goals)
2. **Goal Setting**: Choose your primary objective (weight loss, muscle gain, strength, endurance, general fitness)
3. **Preferences**: Specify available time, equipment, dietary restrictions, and any injuries

### Example Interactions

**🏋️ For Workout Planning:**

```
"I'm a beginner looking to build muscle. I have 45 minutes, 3 times per week, with gym access."
```

→ Fitness Trainer creates a comprehensive strength training program

**🥗 For Nutrition Guidance:**

```
"I want to lose 1 pound per week. I'm 30 years old, 175cm, 80kg, moderately active male."
```

→ Nutritionist calculates caloric needs and creates a meal plan

**🎯 For Comprehensive Planning:**

```
"Help me get in the best shape of my life in 6 months. I'm intermediate level."
```

→ Personal Trainer AI coordinates both fitness and nutrition strategies

## 🏗️ System Architecture

### Multi-Agent Structure

```
personal_trainer_ai/
├── agent.py                    # Main coordinator agent
├── fitness_tools.py            # Exercise database and workout tools
├── nutrition_tools.py          # Nutrition database and meal planning tools
└── sub_agents/
    ├── fitness_trainer/
    │   ├── __init__.py
    │   └── agent.py            # Specialized fitness agent
    └── nutritionist/
        ├── __init__.py
        └── agent.py            # Specialized nutrition agent
```

### Data Assets

- **📊 Exercise Database**: 22,617 exercises with detailed instructions, muscle groups, equipment needs
- **🍽️ Nutrition Database**: Comprehensive food database with macronutrients and prep times
- **📋 Meal Templates**: Goal-specific meal planning templates

## 🎯 Specialized Agent Capabilities

### 💪 Fitness Trainer Agent

- **Exercise Selection**: Search and filter by muscle groups, equipment, difficulty
- **Workout Creation**: Generate complete routines with sets, reps, and rest periods
- **Progression Planning**: Beginner to expert exercise progressions
- **Form Guidance**: Detailed exercise instructions and safety tips

### 🥗 Nutritionist Agent

- **Caloric Assessment**: BMR/TDEE calculations with activity level adjustments
- **Meal Planning**: Multi-day meal plans with portion sizes and prep times
- **Macro Optimization**: Protein, carb, and fat ratios based on goals
- **Food Analysis**: Nutritional breakdown of individual foods

### 🎯 Personal Trainer AI (Coordinator)

- **Profile Assessment**: Comprehensive fitness and nutrition evaluation
- **Goal Coordination**: Align workout and nutrition strategies
- **Progress Monitoring**: Track improvements and adjust recommendations
- **Motivation & Support**: Encouraging guidance throughout the journey

## 🔧 Technical Features

- **ADK Multi-Agent Framework**: Proper sub-agent delegation using Google's ADK
- **Comprehensive Tool Integration**: Custom tools for fitness and nutrition analysis
- **Error Handling**: Robust error handling with helpful user feedback
- **Scalable Architecture**: Easy to extend with additional specialist agents

## 🎯 Use Cases

### Weight Loss

- Caloric deficit planning with cardio and strength training
- High-protein meal plans to preserve muscle
- Sustainable lifestyle modifications

### Muscle Gain

- Progressive overload strength programs
- Caloric surplus with optimal protein timing
- Recovery-focused nutrition strategies

### General Fitness

- Balanced training combining strength, cardio, and flexibility
- Maintainance nutrition for long-term health
- Sustainable habit formation

### Performance Enhancement

- Sport-specific training programs
- Performance nutrition and timing
- Advanced periodization strategies

## 🚀 Getting Started Examples

### Quick Fitness Assessment

```python
# The system will gather this information through conversation
user_profile = {
    "weight_kg": 70,
    "height_cm": 175,
    "age": 28,
    "gender": "male",
    "fitness_level": "beginner",
    "goal": "muscle_gain",
    "time_per_workout": 45,
    "frequency": 3
}
```

### Sample Workout Output

```
Beginner Strength Workout (45 minutes)
├── Push-ups: 3 sets x 8-10 reps
├── Squats: 3 sets x 10-12 reps
├── Bent-over Rows: 3 sets x 8-10 reps
├── Planks: 3 sets x 30 seconds
└── Estimated calories burned: 270
```

### Sample Meal Plan Output

```
Daily Meal Plan (2,200 calories)
├── Breakfast: Greek yogurt with berries (320 cal)
├── Lunch: Chicken breast with quinoa (480 cal)
├── Dinner: Salmon with sweet potato (520 cal)
├── Snacks: Mixed nuts and apple (280 cal)
└── Macros: 140g protein, 220g carbs, 73g fat
```

## 🛡️ Safety & Disclaimers

- Always consult healthcare providers before starting new fitness programs
- The system provides general guidance, not medical advice
- Listen to your body and modify recommendations as needed
- Progressive overload should be gradual and controlled

## 🔄 Contributing

This system is built for extensibility. You can easily add:

- New exercise categories or equipment types
- Additional nutrition databases or meal types
- Specialized agents for specific sports or conditions
- Integration with fitness tracking devices

## 📞 Support

For questions about the ADK framework, visit the [Google ADK Documentation](https://developers.google.com/agent-dev-kit).

## 🎉 Ready to Transform Your Fitness Journey?

Start the server and begin your personalized fitness and nutrition journey today!

```bash
python server.py
```

Navigate to `http://localhost:8080` and let your AI personal training team guide you to your fitness goals! 💪🥗🎯
