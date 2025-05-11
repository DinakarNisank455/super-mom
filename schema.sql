-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema prr
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema prr
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `prr` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `prr` ;

-- -----------------------------------------------------
-- Table `prr`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `prr`.`users` (
  `user_id` VARCHAR(25) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `allergens` VARCHAR(255) NULL DEFAULT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `name` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE INDEX `email` (`email` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `prr`.`grocery_lists`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `prr`.`grocery_lists` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` VARCHAR(25) NOT NULL,
  `recipe_ids` TEXT NOT NULL,
  `ingredients` TEXT NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `user_id` (`user_id` ASC) VISIBLE,
  CONSTRAINT `grocery_lists_ibfk_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `prr`.`users` (`user_id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `prr`.`meal_log`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `prr`.`meal_log` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` VARCHAR(25) NOT NULL,
  `meal_name` VARCHAR(255) NOT NULL,
  `calories` DECIMAL(10,2) NOT NULL DEFAULT '0.00',
  `protein` DECIMAL(10,2) NOT NULL DEFAULT '0.00',
  `carbs` DECIMAL(10,2) NOT NULL DEFAULT '0.00',
  `fats` DECIMAL(10,2) NOT NULL DEFAULT '0.00',
  `meal_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `meal_log_ibfk_1` (`user_id` ASC) VISIBLE,
  CONSTRAINT `meal_log_ibfk_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `prr`.`users` (`user_id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `prr`.`nutrition_goals`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `prr`.`nutrition_goals` (
  `user_id` VARCHAR(25) NOT NULL,
  `daily_calories` DECIMAL(10,2) NOT NULL DEFAULT '2000.00',
  `daily_protein` DECIMAL(10,2) NOT NULL DEFAULT '50.00',
  `daily_fats` DECIMAL(10,2) NOT NULL DEFAULT '65.00',
  `daily_carbs` DECIMAL(10,2) NOT NULL DEFAULT '300.00',
  `daily_fiber` DECIMAL(10,2) NOT NULL DEFAULT '25.00',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  CONSTRAINT `nutrition_goals_ibfk_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `prr`.`users` (`user_id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `prr`.`nutrition_intake`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `prr`.`nutrition_intake` (
  `user_id` VARCHAR(25) NOT NULL,
  `date` DATE NOT NULL,
  `meal_type` ENUM('breakfast', 'lunch', 'dinner', 'snack') NOT NULL,
  `calories` DECIMAL(10,2) NOT NULL DEFAULT '0.00',
  `protein` DECIMAL(10,2) NOT NULL DEFAULT '0.00',
  `carbs` DECIMAL(10,2) NOT NULL DEFAULT '0.00',
  `fats` DECIMAL(10,2) NOT NULL DEFAULT '0.00',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`, `date`, `meal_type`),
  CONSTRAINT `nutrition_intake_ibfk_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `prr`.`users` (`user_id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `prr`.`profiles`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `prr`.`profiles` (
  `user_id` VARCHAR(25) NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `gym_membership` TINYINT(1) NOT NULL DEFAULT '0',
  `nutrition_plan` VARCHAR(50) NULL DEFAULT NULL,
  `food_allergies` TEXT NULL DEFAULT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  CONSTRAINT `profiles_ibfk_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `prr`.`users` (`user_id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `prr`.`recipes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `prr`.`recipes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` VARCHAR(25) NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `ingredients` TEXT NOT NULL,
  `diet_type` ENUM('high-protein', 'balanced', 'vegan', 'low-carb') NOT NULL,
  `gym_friendly` TINYINT(1) NOT NULL DEFAULT '0',
  `recipe_link` VARCHAR(255) NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `user_id` (`user_id` ASC) VISIBLE,
  CONSTRAINT `recipes_ibfk_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `prr`.`users` (`user_id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `prr`.`saved_recipes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `prr`.`saved_recipes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` VARCHAR(25) NOT NULL,
  `recipe_name` VARCHAR(255) NOT NULL,
  `image_url` TEXT NULL DEFAULT NULL,
  `recipe_url` TEXT NULL DEFAULT NULL,
  `diet_type` VARCHAR(255) NULL DEFAULT NULL,
  `ingredients` TEXT NULL DEFAULT NULL,
  `calories` DECIMAL(10,2) NOT NULL DEFAULT '0.00',
  `protein` DECIMAL(10,2) NOT NULL DEFAULT '0.00',
  `fat` DECIMAL(10,2) NOT NULL DEFAULT '0.00',
  `carbohydrates` DECIMAL(10,2) NOT NULL DEFAULT '0.00',
  `fiber` DECIMAL(10,2) NOT NULL DEFAULT '0.00',
  `saved_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `allergens` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `user_id` (`user_id` ASC) VISIBLE,
  CONSTRAINT `saved_recipes_ibfk_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `prr`.`users` (`user_id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
