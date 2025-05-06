import mysql.connector
import requests

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="yourpassword",
    database="recipe_recommender"
)
cursor = conn.cursor(dictionary=True)

# Get daily nutrition intake
def get_daily_nutrition(user_id):
    query = """
        SELECT meal_type, SUM(calories) AS total_calories, 
               SUM(protein) AS total_protein, 
               SUM(carbs) AS total_carbs, 
               SUM(fats) AS total_fats
        FROM nutrition_intake
        WHERE user_id = %s AND date = CURDATE()
        GROUP BY meal_type
    """
    cursor.execute(query, (user_id,))
    return cursor.fetchall()

# Get monthly nutrition intake
def get_monthly_nutrition(user_id):
    query = """
        SELECT DATE(date) AS day, 
               SUM(calories) AS total_calories, 
               SUM(protein) AS total_protein, 
               SUM(carbs) AS total_carbs, 
               SUM(fats) AS total_fats
        FROM nutrition_intake
        WHERE user_id = %s AND MONTH(date) = MONTH(CURDATE()) AND YEAR(date) = YEAR(CURDATE())
        GROUP BY DATE(date)
    """
    cursor.execute(query, (user_id,))
    return cursor.fetchall()

# Example Usage
user_id = 1
daily_data = get_daily_nutrition(user_id)
monthly_data = get_monthly_nutrition(user_id)

print("Daily Nutrition Intake:")
for meal in daily_data:
    print(meal)

print("\nMonthly Nutrition Intake:")
for day in monthly_data:
    print(day)



# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="yourpassword",
    database="recipe_recommender"
)
cursor = conn.cursor()

def get_recipe_nutrition(ingredient):
    """ Fetch recipes from API and store nutrition data """
    params = {
        "q": ingredient,
        "app_id": "9339488b",
        "app_key": "4f804a4822c6c387579112bcda286297",
        "type": "public",
        "limit": 1
    }
    response = requests.get(f"https://api.edamam.com/api/recipes/v2?q={ingredient_query}&app_id={self.app_id}&app_key={self.app_key}&type=public&limit=5", params=params)
    data = response.json()
    
    if 'hits' in data and len(data['hits']) > 0:
        recipe = data['hits'][0]['recipe']
        name = recipe['label']  
        calories = recipe['calories']
        protein = recipe['totalNutrients'].get('PROCNT', {}).get('quantity', 0)
        carbs = recipe['totalNutrients'].get('CHOCDF', {}).get('quantity', 0)
        fats = recipe['totalNutrients'].get('FAT', {}).get('quantity', 0)
        
        # Store in database
        query = """
            INSERT INTO nutrition_intake (user_id, date, meal_type, calories, protein, carbs, fats) 
            VALUES (%s, CURDATE(), %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (1, 'lunch', calories, protein, carbs, fats))
        conn.commit()
        print(f"Stored: {name} - {calories} kcal, {protein}g protein, {carbs}g carbs, {fats}g fats")
    else:
        print("No recipes found.")

# Example: Fetch recipes for "chicken"
get_recipe_nutrition("chicken")
