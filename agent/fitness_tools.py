"""
Fitness and exercise tools for the personal trainer AI system.
"""
import json
import random
from typing import Any, Dict, List, Optional
from pathlib import Path


def load_exercises_data() -> List[Dict[str, Any]]:
    """Load the exercises dataset from JSON file."""
    try:
        data_path = Path(__file__).parent.parent / "data" / "exercises.json"
        with open(data_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        return []


def search_exercises(
    category: Optional[str] = None,
    level: Optional[str] = None,
    equipment: Optional[str] = None,
    muscle_groups: Optional[List[str]] = None,
    limit: int = 10
) -> Dict[str, Any]:
    """
    Search for exercises based on criteria.
    
    Args:
        category: Exercise category (cardio, strength, stretching, etc.)
        level: Difficulty level (beginner, intermediate, expert)
        equipment: Equipment type (body only, dumbbell, barbell, etc.)
        muscle_groups: List of target muscle groups
        limit: Maximum number of exercises to return
    
    Returns:
        Dictionary with status and filtered exercises data
    """
    try:
        exercises = load_exercises_data()
        if not exercises:
            return {"status": "error", "error_message": "Could not load exercises data"}
        
        filtered = exercises
        
        # Filter by category
        if category:
            filtered = [ex for ex in filtered if ex.get('category', '').lower() == category.lower()]
        
        # Filter by level
        if level:
            filtered = [ex for ex in filtered if ex.get('level', '').lower() == level.lower()]
        
        # Filter by equipment
        if equipment:
            filtered = [ex for ex in filtered if equipment.lower() in ex.get('equipment', '').lower()]
        
        # Filter by muscle groups
        if muscle_groups:
            muscle_groups_lower = [mg.lower() for mg in muscle_groups]
            filtered = [
                ex for ex in filtered 
                if any(mg.lower() in muscle_groups_lower 
                      for mg in ex.get('primaryMuscles', []) + ex.get('secondaryMuscles', []))
            ]
        
        # Limit results
        filtered = filtered[:limit]
        
        return {
            "status": "success", 
            "data": {
                "exercises": filtered,
                "total_found": len(filtered),
                "search_criteria": {
                    "category": category,
                    "level": level,
                    "equipment": equipment,
                    "muscle_groups": muscle_groups
                }
            }
        }
    except Exception as e:
        return {"status": "error", "error_message": f"Search failed: {e}"}


def get_exercise_categories() -> Dict[str, Any]:
    """Get all available exercise categories with counts."""
    try:
        exercises = load_exercises_data()
        if not exercises:
            return {"status": "error", "error_message": "Could not load exercises data"}
        
        categories = {}
        for exercise in exercises:
            cat = exercise.get('category', 'unknown')
            categories[cat] = categories.get(cat, 0) + 1
        
        return {
            "status": "success",
            "data": {
                "categories": [{"name": k, "count": v} for k, v in categories.items()],
                "total_categories": len(categories)
            }
        }
    except Exception as e:
        return {"status": "error", "error_message": f"Failed to get categories: {e}"}


def get_muscle_groups() -> Dict[str, Any]:
    """Get all available muscle groups with exercise counts."""
    try:
        exercises = load_exercises_data()
        if not exercises:
            return {"status": "error", "error_message": "Could not load exercises data"}
        
        muscle_counts = {}
        for exercise in exercises:
            for muscle in exercise.get('primaryMuscles', []) + exercise.get('secondaryMuscles', []):
                muscle_counts[muscle] = muscle_counts.get(muscle, 0) + 1
        
        sorted_muscles = sorted(muscle_counts.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "status": "success",
            "data": {
                "muscle_groups": [{"name": k, "exercise_count": v} for k, v in sorted_muscles],
                "total_muscle_groups": len(muscle_counts)
            }
        }
    except Exception as e:
        return {"status": "error", "error_message": f"Failed to get muscle groups: {e}"}


def create_workout_plan(
    fitness_level: str = "beginner",
    target_muscles: Optional[List[str]] = None,
    workout_type: str = "strength",
    duration_minutes: int = 45,
    equipment: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a personalized workout plan.
    
    Args:
        fitness_level: beginner, intermediate, or expert
        target_muscles: List of muscle groups to target
        workout_type: strength, cardio, stretching, etc.
        duration_minutes: Target workout duration
        equipment: Available equipment type
    
    Returns:
        Dictionary with complete workout plan
    """
    try:
        exercises = load_exercises_data()
        if not exercises:
            return {"status": "error", "error_message": "Could not load exercises data"}
        
        # Filter exercises based on criteria
        filtered = exercises
        
        # Filter by level
        filtered = [ex for ex in filtered if ex.get('level', '').lower() == fitness_level.lower()]
        
        # Filter by category/workout type
        if workout_type != "mixed":
            filtered = [ex for ex in filtered if ex.get('category', '').lower() == workout_type.lower()]
        
        # Filter by equipment if specified
        if equipment:
            filtered = [ex for ex in filtered if equipment.lower() in ex.get('equipment', '').lower()]
        
        # Filter by target muscles if specified
        if target_muscles:
            muscle_groups_lower = [mg.lower() for mg in target_muscles]
            filtered = [
                ex for ex in filtered 
                if any(mg.lower() in muscle_groups_lower 
                      for mg in ex.get('primaryMuscles', []))
            ]
        
        if not filtered:
            return {"status": "error", "error_message": "No exercises found matching criteria"}
        
        # Calculate number of exercises based on duration
        estimated_time_per_exercise = 3  # minutes including rest
        target_exercise_count = max(3, min(duration_minutes // estimated_time_per_exercise, 10))
        
        # Select diverse exercises
        selected_exercises = []
        used_primary_muscles = set()
        
        # Try to get variety in muscle groups
        for _ in range(target_exercise_count):
            available = [ex for ex in filtered if not any(
                muscle in used_primary_muscles for muscle in ex.get('primaryMuscles', [])
            )]
            
            if not available:
                available = filtered  # Reset if we've covered all muscle groups
                used_primary_muscles.clear()
            
            if available:
                exercise = random.choice(available)
                selected_exercises.append(exercise)
                used_primary_muscles.update(exercise.get('primaryMuscles', []))
                filtered.remove(exercise)
        
        # Create sets and reps based on fitness level and exercise type
        workout_exercises = []
        for exercise in selected_exercises:
            sets, reps = _calculate_sets_reps(exercise, fitness_level)
            workout_exercises.append({
                "exercise": exercise,
                "sets": sets,
                "reps": reps,
                "rest_seconds": 60 if exercise.get('category') == 'strength' else 30
            })
        
        return {
            "status": "success",
            "data": {
                "workout_plan": {
                    "title": f"{fitness_level.title()} {workout_type.title()} Workout",
                    "duration_minutes": duration_minutes,
                    "exercises": workout_exercises,
                    "total_exercises": len(workout_exercises),
                    "target_muscles": target_muscles or "Full body",
                    "equipment_needed": equipment or "Various",
                    "estimated_calories": _estimate_calories(duration_minutes, workout_type, fitness_level)
                }
            }
        }
    except Exception as e:
        return {"status": "error", "error_message": f"Workout plan creation failed: {e}"}


def _calculate_sets_reps(exercise: Dict[str, Any], fitness_level: str) -> tuple[int, str]:
    """Calculate appropriate sets and reps based on exercise and fitness level."""
    category = exercise.get('category', 'strength')
    
    if category == 'cardio':
        if fitness_level == 'beginner':
            return 3, "30 seconds"
        elif fitness_level == 'intermediate':
            return 4, "45 seconds"
        else:
            return 5, "60 seconds"
    
    elif category == 'stretching':
        return 1, "30 seconds hold"
    
    elif category == 'strength':
        if fitness_level == 'beginner':
            return 3, "8-10 reps"
        elif fitness_level == 'intermediate':
            return 3, "10-12 reps"
        else:
            return 4, "12-15 reps"
    
    else:  # plyometrics, olympic weightlifting, etc.
        if fitness_level == 'beginner':
            return 2, "5-8 reps"
        elif fitness_level == 'intermediate':
            return 3, "8-10 reps"
        else:
            return 4, "10-12 reps"


def _estimate_calories(duration_minutes: int, workout_type: str, fitness_level: str) -> int:
    """Estimate calories burned based on workout parameters."""
    base_rate = {
        'cardio': 8,
        'strength': 6,
        'stretching': 3,
        'plyometrics': 10,
        'powerlifting': 7,
        'olympic weightlifting': 7,
        'strongman': 8
    }.get(workout_type, 6)
    
    level_multiplier = {
        'beginner': 0.8,
        'intermediate': 1.0,
        'expert': 1.2
    }.get(fitness_level, 1.0)
    
    return int(duration_minutes * base_rate * level_multiplier)


def get_exercise_by_name(exercise_name: str) -> Dict[str, Any]:
    """Get detailed information about a specific exercise by name."""
    try:
        exercises = load_exercises_data()
        if not exercises:
            return {"status": "error", "error_message": "Could not load exercises data"}
        
        # Find exercise by name (case insensitive)
        found_exercise = None
        for exercise in exercises:
            if exercise.get('name', '').lower() == exercise_name.lower():
                found_exercise = exercise
                break
        
        if not found_exercise:
            # Try partial match
            for exercise in exercises:
                if exercise_name.lower() in exercise.get('name', '').lower():
                    found_exercise = exercise
                    break
        
        if found_exercise:
            return {"status": "success", "data": {"exercise": found_exercise}}
        else:
            return {"status": "error", "error_message": f"Exercise '{exercise_name}' not found"}
    
    except Exception as e:
        return {"status": "error", "error_message": f"Search failed: {e}"}
