-- First, create a test user
INSERT INTO users (user_id, email, password, name, allergens, created_at) 
VALUES (
    'test_user_1',
    'test@example.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewYpR1IOBYyGqK8y', -- hashed password for 'test123'
    'Test User',
    'dairy,soy',
    NOW()
);

-- Then insert the saved recipes data
INSERT INTO saved_recipes (user_id, recipe_name, image_url, recipe_url, diet_type, ingredients, calories, protein, fat, carbohydrates, fiber, saved_at, allergens) VALUES
-- Recent entries (last 2 months)
('test_user_1', 'Grilled Salmon with Lemon', 'https://example.com/salmon.jpg', 'https://example.com/recipes/salmon', 'high-protein', '["salmon fillet", "lemon", "olive oil", "garlic", "dill"]', 450.00, 35.00, 28.00, 2.00, 0.50, DATE_SUB(NOW(), INTERVAL 5 DAY), 'fish'),
('test_user_1', 'Quinoa Buddha Bowl', 'https://example.com/buddha-bowl.jpg', 'https://example.com/recipes/buddha-bowl', 'vegan', '["quinoa", "chickpeas", "kale", "avocado", "sweet potato"]', 380.00, 12.00, 15.00, 45.00, 8.00, DATE_SUB(NOW(), INTERVAL 12 DAY), NULL),
('test_user_1', 'Chicken Stir Fry', 'https://example.com/stir-fry.jpg', 'https://example.com/recipes/stir-fry', 'balanced', '["chicken breast", "broccoli", "carrots", "soy sauce", "ginger"]', 420.00, 40.00, 12.00, 35.00, 5.00, DATE_SUB(NOW(), INTERVAL 15 DAY), 'soy'),
('test_user_1', 'Greek Yogurt Parfait', 'https://example.com/parfait.jpg', 'https://example.com/recipes/parfait', 'high-protein', '["greek yogurt", "honey", "granola", "berries"]', 280.00, 20.00, 8.00, 35.00, 4.00, DATE_SUB(NOW(), INTERVAL 20 DAY), 'dairy'),
('test_user_1', 'Vegetable Curry', 'https://example.com/curry.jpg', 'https://example.com/recipes/curry', 'vegan', '["coconut milk", "chickpeas", "spinach", "tomatoes", "curry powder"]', 350.00, 10.00, 18.00, 42.00, 7.00, DATE_SUB(NOW(), INTERVAL 25 DAY), NULL),
('test_user_1', 'Turkey Meatballs', 'https://example.com/meatballs.jpg', 'https://example.com/recipes/meatballs', 'high-protein', '["ground turkey", "breadcrumbs", "egg", "parmesan", "herbs"]', 380.00, 32.00, 22.00, 15.00, 2.00, DATE_SUB(NOW(), INTERVAL 30 DAY), 'egg'),
('test_user_1', 'Cauliflower Rice Bowl', 'https://example.com/cauliflower.jpg', 'https://example.com/recipes/cauliflower', 'low-carb', '["cauliflower", "chicken", "bell peppers", "olive oil"]', 320.00, 25.00, 18.00, 12.00, 4.00, DATE_SUB(NOW(), INTERVAL 35 DAY), NULL),
('test_user_1', 'Tofu Scramble', 'https://example.com/tofu.jpg', 'https://example.com/recipes/tofu', 'vegan', '["tofu", "turmeric", "onions", "bell peppers", "spinach"]', 250.00, 18.00, 12.00, 15.00, 3.00, DATE_SUB(NOW(), INTERVAL 40 DAY), 'soy'),
('test_user_1', 'Protein Pancakes', 'https://example.com/pancakes.jpg', 'https://example.com/recipes/pancakes', 'high-protein', '["protein powder", "oats", "banana", "egg whites", "almond milk"]', 350.00, 25.00, 8.00, 45.00, 5.00, DATE_SUB(NOW(), INTERVAL 45 DAY), 'egg'),
('test_user_1', 'Mediterranean Salad', 'https://example.com/salad.jpg', 'https://example.com/recipes/salad', 'balanced', '["mixed greens", "feta", "olives", "cucumber", "tomatoes"]', 280.00, 12.00, 18.00, 15.00, 4.00, DATE_SUB(NOW(), INTERVAL 50 DAY), 'dairy'),

-- Older entries (3-6 months ago)
('test_user_1', 'Beef Stir Fry', 'https://example.com/beef-stir-fry.jpg', 'https://example.com/recipes/beef-stir-fry', 'high-protein', '["beef strips", "broccoli", "soy sauce", "ginger", "garlic"]', 450.00, 35.00, 25.00, 20.00, 3.00, DATE_SUB(NOW(), INTERVAL 90 DAY), 'soy'),
('test_user_1', 'Lentil Soup', 'https://example.com/lentil-soup.jpg', 'https://example.com/recipes/lentil-soup', 'vegan', '["lentils", "carrots", "celery", "onion", "vegetable broth"]', 280.00, 15.00, 5.00, 45.00, 12.00, DATE_SUB(NOW(), INTERVAL 100 DAY), NULL),
('test_user_1', 'Grilled Chicken Salad', 'https://example.com/chicken-salad.jpg', 'https://example.com/recipes/chicken-salad', 'high-protein', '["chicken breast", "mixed greens", "avocado", "tomatoes", "balsamic"]', 380.00, 35.00, 18.00, 15.00, 5.00, DATE_SUB(NOW(), INTERVAL 110 DAY), NULL),
('test_user_1', 'Vegetable Pasta', 'https://example.com/veg-pasta.jpg', 'https://example.com/recipes/veg-pasta', 'balanced', '["whole wheat pasta", "zucchini", "bell peppers", "tomato sauce", "basil"]', 420.00, 12.00, 8.00, 75.00, 8.00, DATE_SUB(NOW(), INTERVAL 120 DAY), 'wheat'),
('test_user_1', 'Tuna Salad', 'https://example.com/tuna-salad.jpg', 'https://example.com/recipes/tuna-salad', 'high-protein', '["tuna", "celery", "onion", "mayo", "lemon"]', 320.00, 28.00, 18.00, 5.00, 2.00, DATE_SUB(NOW(), INTERVAL 130 DAY), 'fish'),
('test_user_1', 'Quinoa Salad', 'https://example.com/quinoa-salad.jpg', 'https://example.com/recipes/quinoa-salad', 'vegan', '["quinoa", "cucumber", "tomatoes", "feta", "olive oil"]', 350.00, 10.00, 15.00, 45.00, 6.00, DATE_SUB(NOW(), INTERVAL 140 DAY), 'dairy'),

-- Even older entries (6-12 months ago)
('test_user_1', 'Chicken Curry', 'https://example.com/chicken-curry.jpg', 'https://example.com/recipes/chicken-curry', 'balanced', '["chicken", "coconut milk", "curry paste", "vegetables"]', 450.00, 30.00, 25.00, 35.00, 5.00, DATE_SUB(NOW(), INTERVAL 180 DAY), NULL),
('test_user_1', 'Vegetable Stir Fry', 'https://example.com/veg-stir-fry.jpg', 'https://example.com/recipes/veg-stir-fry', 'vegan', '["tofu", "broccoli", "carrots", "soy sauce", "ginger"]', 320.00, 15.00, 12.00, 35.00, 6.00, DATE_SUB(NOW(), INTERVAL 200 DAY), 'soy'),
('test_user_1', 'Salmon Bowl', 'https://example.com/salmon-bowl.jpg', 'https://example.com/recipes/salmon-bowl', 'high-protein', '["salmon", "rice", "avocado", "cucumber", "seaweed"]', 480.00, 35.00, 22.00, 45.00, 4.00, DATE_SUB(NOW(), INTERVAL 220 DAY), 'fish'),
('test_user_1', 'Greek Salad', 'https://example.com/greek-salad.jpg', 'https://example.com/recipes/greek-salad', 'balanced', '["cucumber", "tomatoes", "feta", "olives", "olive oil"]', 280.00, 8.00, 20.00, 12.00, 3.00, DATE_SUB(NOW(), INTERVAL 240 DAY), 'dairy'),
('test_user_1', 'Tofu Bowl', 'https://example.com/tofu-bowl.jpg', 'https://example.com/recipes/tofu-bowl', 'vegan', '["tofu", "rice", "vegetables", "teriyaki sauce"]', 380.00, 20.00, 15.00, 45.00, 5.00, DATE_SUB(NOW(), INTERVAL 260 DAY), 'soy'),

-- Very old entries (1+ year ago)
('test_user_1', 'Chicken Pasta', 'https://example.com/chicken-pasta.jpg', 'https://example.com/recipes/chicken-pasta', 'balanced', '["chicken", "pasta", "tomato sauce", "basil", "parmesan"]', 520.00, 35.00, 18.00, 55.00, 4.00, DATE_SUB(NOW(), INTERVAL 365 DAY), 'dairy'),
('test_user_1', 'Vegetable Soup', 'https://example.com/veg-soup.jpg', 'https://example.com/recipes/veg-soup', 'vegan', '["vegetables", "vegetable broth", "herbs", "garlic"]', 220.00, 5.00, 8.00, 35.00, 8.00, DATE_SUB(NOW(), INTERVAL 380 DAY), NULL),
('test_user_1', 'Beef Stew', 'https://example.com/beef-stew.jpg', 'https://example.com/recipes/beef-stew', 'high-protein', '["beef", "potatoes", "carrots", "onion", "beef broth"]', 450.00, 35.00, 22.00, 35.00, 5.00, DATE_SUB(NOW(), INTERVAL 400 DAY), NULL),
('test_user_1', 'Quinoa Bowl', 'https://example.com/quinoa-bowl.jpg', 'https://example.com/recipes/quinoa-bowl', 'vegan', '["quinoa", "black beans", "corn", "avocado", "lime"]', 380.00, 12.00, 15.00, 45.00, 8.00, DATE_SUB(NOW(), INTERVAL 420 DAY), NULL),
('test_user_1', 'Turkey Wrap', 'https://example.com/turkey-wrap.jpg', 'https://example.com/recipes/turkey-wrap', 'high-protein', '["turkey", "lettuce", "tomato", "whole wheat wrap"]', 350.00, 25.00, 12.00, 35.00, 5.00, DATE_SUB(NOW(), INTERVAL 440 DAY), 'wheat'),

-- Additional entries for variety
('test_user_1', 'Shrimp Stir Fry', 'https://example.com/shrimp-stir-fry.jpg', 'https://example.com/recipes/shrimp-stir-fry', 'high-protein', '["shrimp", "vegetables", "soy sauce", "ginger"]', 320.00, 28.00, 12.00, 25.00, 4.00, DATE_SUB(NOW(), INTERVAL 460 DAY), 'shellfish'),
('test_user_1', 'Mushroom Risotto', 'https://example.com/risotto.jpg', 'https://example.com/recipes/risotto', 'balanced', '["arborio rice", "mushrooms", "parmesan", "white wine"]', 420.00, 10.00, 15.00, 55.00, 3.00, DATE_SUB(NOW(), INTERVAL 480 DAY), 'dairy'),
('test_user_1', 'Chickpea Curry', 'https://example.com/chickpea-curry.jpg', 'https://example.com/recipes/chickpea-curry', 'vegan', '["chickpeas", "coconut milk", "spinach", "curry powder"]', 350.00, 12.00, 15.00, 45.00, 8.00, DATE_SUB(NOW(), INTERVAL 500 DAY), NULL),
('test_user_1', 'Steak Salad', 'https://example.com/steak-salad.jpg', 'https://example.com/recipes/steak-salad', 'high-protein', '["steak", "mixed greens", "blue cheese", "balsamic"]', 450.00, 35.00, 28.00, 12.00, 4.00, DATE_SUB(NOW(), INTERVAL 520 DAY), 'dairy'),
('test_user_1', 'Vegetable Lasagna', 'https://example.com/veg-lasagna.jpg', 'https://example.com/recipes/veg-lasagna', 'balanced', '["pasta", "ricotta", "spinach", "tomato sauce"]', 420.00, 15.00, 18.00, 45.00, 5.00, DATE_SUB(NOW(), INTERVAL 540 DAY), 'dairy'); 