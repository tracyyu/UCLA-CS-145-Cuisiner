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
                    self.ingredientMatrix[recipe.cuisine] = 0
                self.ingredientMatrix[recipe.cuisine] += 1

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

        # TODO Perform classification
        CuisineProb = {} # <cuisine, <ingredient, probability>>

        chosenCuisine = ""
        chosenCuisineProb = 0.0
        tempChosenCuisineProb = 0.0

        #loop through all the ingredients in the recipe we are given
        for ingredient in recipe.ingredients:
            #total frequency of ingredient
            ingredCt = self.ingredientCount[ingredient]
            for cuisine in self.cuisineCount:
                CuisineProb[cuisine] = {}
                #frequency ingredient shows up in a specific cuisine
                if ingredient not in self.cuisineMatrix[cuisine]:
                    ingredCuisineCT = 0.0
                else:
                    ingredCuisineCT = self.cuisineMatrix[cuisine][ingredient]
                #probability ingredient exist in specific cuisine stored in matrix
                CuisineProb[cuisine][ingredient] = float(ingredCuisineCT/ingredCt)

        # now we are going to calculate probability that all specified ingredients exist in cuisine
        for cuisine in CuisineProb:
            for ingredient in CuisineProb[cuisine]:
                tempChosenCuisineProb = tempChosenCuisineProb + CuisineProb[cuisine][ingredient]
            #whichever has the greatest probability is the specified cuisine  
            if tempChosenCuisineProb > chosenCuisineProb:
                chosenCuisine = cuisine
                chosenCuisineProb = tempChosenCuisineProb

        return ClassifiedRecipe(recipe.id, chosenCuisine, recipe.ingredients)

    """
    Classifies a list of Recipes.
    @param  recipes List of Recipes
    @return         List of ClassfiedRecipes
    """
    def classifyRecipes(self, recipes):
        # Iterate through recipes
        return [self.classifyRecipe(recipe) for recipe in recipes]