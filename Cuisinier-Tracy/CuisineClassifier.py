# -*- coding: utf-8 -*-

import logging
from collections import namedtuple


Recipe = namedtuple("ClassifiedRecipe", "id, ingredients")
ClassifiedRecipe = namedtuple("ClassifiedRecipe", "id, cuisine, ingredients")

"""
Uses ingredients to categorize the cuisine of a recipe.
@author: Alan Kha
"""


class Cuisinier:
    def __init__(self):
        self.recipes = {}  # <id, Recipe>
        self.cuisineCount = {}  # <cuisine, frequency>
        self.cuisineMatrix = {}  # <cuisine, <ingredient, frequency>>
        self.ingredientCount = {}  # <ingredient, frequency>
        self.ingredientMatrix = {}  # <ingredient, <cuisine, frequency>>

    """
    Adds a ClassifiedRecipe to the knowledge base.
    @param  recipe  ClassifiedRecipe Recipe to be added
    @return         True if successful, false otherwise
    """
    def addRecipe(self, recipe: ClassifiedRecipe):
        if not isinstance(recipe, ClassifiedRecipe):
            raise TypeError("Cuisinier.addRecipe() takes a ClassifiedRecipe")

        # Add new recipes to knowledge base
        if recipe.id not in self.recipes:
            self.recipes[recipe.id] = recipe

            # Add to ingredient counter
            if recipe.cuisine not in self.cuisineCount:
                self.cuisineCount[recipe.cuisine] = 0
            self.cuisineCount[recipe.cuisine] += 1

            # Initialize cuisine matrix entry
            if recipe.cuisine not in self.cuisineMatrix:
                self.cuisineMatrix[recipe.cuisine] = {}

            # Iterate through ingredients
            for ingredient in recipe.ingredients:
                # Add to cuisine matrix
                if ingredient not in self.cuisineMatrix[recipe.cuisine]:
                    self.cuisineMatrix[recipe.cuisine][ingredient] = 0
                self.cuisineMatrix[recipe.cuisine][ingredient] += 1

                # Add to ingredient counter
                if ingredient not in self.ingredientCount:
                    self.ingredientCount[ingredient] = 0
                self.ingredientCount[ingredient] += 1

                # Add to ingredient matrix
                if ingredient not in self.ingredientMatrix:
                    self.ingredientMatrix[ingredient] = {}
                if recipe.cuisine not in self.ingredientMatrix[ingredient]:
                    self.ingredientMatrix[ingredient][recipe.cuisine] = 0
                self.ingredientMatrix[ingredient][recipe.cuisine] += 1

            # Return true if successful
            logging.info("Add recipe " + str(recipe.id) + ":\tSUCCESS")
            return True

        logging.info("Add recipe " + str(recipe.id) + ":\tFAIL")
        return False

    """
    Add a list of ClassfiedRecipes.
    @param  recipes List of ClassifedRecipes
    """
    def addRecipes(self, recipes):
        success = 0
        for recipe in recipes:
            if (self.addRecipe(recipe)):
                success += 1

        logging.info(str(success) + "/" + str(len(recipes)) + " recipes added")

    """
    Classifies a given Recipe.
    @param  recipe  Recipe to be classified
    @return         ClassfiedRecipe
    """
    def classifyRecipe(self, recipe: Recipe):
        if not isinstance(recipe, Recipe):
            raise TypeError("Cuisinier.classifyRecipe() takes a Recipe")

        # TODO Perform 
        cuisineRecipeClassification = {} # <cuisine, <ingredient, 1 or 0>>
        CuisineProb = {} # <cuisine, <ingredient, probability>>

        possibleCusineChoices = [] # cuisines who have all the specified recipe
        cuisineIngredCt = {}      # <cuisine, <ingredient from recipe, frequency>

        chosenCuisine = "" #correct Cuisine
        chosenCuisineIngredFreq = 0

        #loop through the databse of cuisine
        for cuisine in self.cuisineCount:
            cuisineRecipeClassification[cuisine] = {}
             #loop through all the ingredients in the recipe we are given
            for ingredient in recipe.ingredients:
                #now mark whether ingredient exists in specific cusine
                #1, for it does
                #0, for it does not
                if ingredient not in self.cuisineMatrix[cuisine]:
                    cuisineRecipeClassification[cuisine][ingredient] = 0
                else:
                    if self.cuisineMatrix[cuisine][ingredient] > 0:
                        cuisineRecipeClassification[cuisine][ingredient] = 1
                    else:
                        cuisineRecipeClassification[cuisine][ingredient] = 0

        #choose only the cuisine that has all the listed ingredients
        for cuisine in cuisineRecipeClassification:
            totalIngredCt = 0
            #loop through all the ingredients in the recipe we are given
            for ingredient in recipe.ingredients:
                totalIngredCt += cuisineRecipeClassification[cuisine][ingredient]
            #sum one the 1's must equal to # of ingredients in recipe
            if totalIngredCt == (len(recipe.ingredients)):
                possibleCusineChoices.append(cuisine)

        #now to compare among the remaining cuisines
        #if there exist only one possible Cusine choice, we have found it
        if len(possibleCusineChoices)  == 1:
            chosenCuisine = possibleCusineChoices[0]
        else:
            recipeIngredCt = {} # <ingredient in recipe, frequency>
            #now we will find the ingredient with lowest frequency out of all cuisines
            for ingredient in recipe.ingredients:
                recipeIngredCt[ingredient] = self.ingredientCount[ingredient]
            ingredWithLowFreq = ""
            for ingredient in recipeIngredCt:
                if ingredWithLowFreq == "":
                    ingredWithLowFreq = ingredient
                elif recipeIngredCt[ingredient] < recipeIngredCt[ingredWithLowFreq]:
                    ingredWithLowFreq = ingredient 

            #now find the cuisine with the highest frequency of the ingredients with lowest overall frequency
            for cuisine in possibleCusineChoices:
                cuisineIngredFreq = self.cuisineMatrix[cuisine][ingredWithLowFreq]
                print(cuisine)
                print(cuisineIngredFreq)
                if chosenCuisine == "":
                    chosenCuisine =  cuisine
                    chosenCuisineIngredFreq = cuisineIngredFreq
                elif cuisineIngredFreq > chosenCuisineIngredFreq:
                    chosenCuisine = cuisine
                    chosenCuisineIngredFreq = cuisineIngredFreq

            print(ingredWithLowFreq) 
            print(chosenCuisineIngredFreq)   


        return ClassifiedRecipe(recipe.id, chosenCuisine, recipe.ingredients)

    """
    Classifies a list of Recipes.
    @param  recipes List of Recipes
    @return         List of ClassfiedRecipes
    """
    def classifyRecipes(self, recipes):
        # Iterate through recipes
        return [self.classifyRecipe(recipe) for recipe in recipes]
