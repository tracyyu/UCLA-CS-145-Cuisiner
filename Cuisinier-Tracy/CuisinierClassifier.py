from Cuisinier import Recipe, ClassifiedRecipe, Cuisinier

"""
Uses ingredients to categorize the cuisine of a recipe via the
One-Vs-All algorithm.
@author: Alan Kha
"""

class CuisinierOVA(Cuisinier):
	def __init__(self):
        super().__init__()
        

    def preprocess(self):
        super().preprocess()
        self.cuisineRecipeClassification = {} # <cuisine, <ingredient, 1 or 0>>

     def classifyRecipe(self, recipe: Recipe):
        if not isinstance(recipe, Recipe):
            raise TypeError("Cuisinier.classifyRecipe() takes a Recipe")

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
