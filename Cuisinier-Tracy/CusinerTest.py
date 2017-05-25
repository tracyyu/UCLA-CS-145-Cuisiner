    def classifyRecipe(self, recipe: Recipe):
        if not isinstance(recipe, Recipe):
            raise TypeError("Cuisinier.classifyRecipe() takes a Recipe")

        # TODO Perform 
        print(recipe)

        cuisineRecipeClassification = {} # <cuisine, <ingredient, 1 or 0>>
        CuisineProb = {} # <cuisine, <ingredient, probability>>

        possibleCusineChoices = [] # cuisines who have all the specified recipe
        cuisineIngredCt = {}      # <cuisine, <ingredient from recipe, frequency>

        chosenCuisine = "" #correct Cuisine

        chosenCuisineProb = 0
        tempChosenCuisineProb = 1.0

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
            #using bag of words model
            #keep track of the ingredient's frequency from the recipe for each cuicine
            #whichever appears more often
            for cuisine in possibleCusineChoices:
                #get frequency of ingredient in for each cusine & compare to other cusines
                cuisineIngredCt[cuisine] = {}
                for ingredient in recipe.ingredients:
                    cuisineIngredCt[cuisine][ingredient] = self.cuisineMatrix[cuisine][ingredient]      

            #now count which cuisine has the highest frequency for which ingredients
            cuisineFreq = {} # <cuisine, freq>
            for ingredient in cuisineIngredCt[cuisine]:
                highestFreq = 0
                cuisineHighFreq = ""
                for cuisine in cuisineIngredCt:
                    # get the highest frequency & cuisine for particular ingredient
                    if cuisineIngredCt[cuisine][ingredient] > highestFreq:
                        highestFreq = cuisineIngredCt[cuisine][ingredient]
                        cuisineHighFreq = cuisine
                    if cuisine not in cuisineFreq:
                        cuisineFreq[cuisine] = 0
                # add a count to speicfic cuisine if has highest frequency for the cuisine
                cuisineFreq[cuisineHighFreq] += 1
            print(cuisineFreq)

            #now we take the one with largest frequency & set it to the be the chosen cuisine
            for cuisine in cuisineFreq:
                CuisineProb[cuisine] = {}
                highestFreq = 0
                cuisineHighFreq = ""
                # if there are multiple highest Freq
                if cuisineFreq[cuisine] == highestFreq and cuisineFreq[cuisine] != 0:
                #calculate the probability of the ingredients in the recipe that would 
                #be in each cuisine. Certain ingredient heavily favored in certain cuisine?

                    #push two of cuisines we are comparing
                    for ingredient in recipe.ingredients:
                    #total frequency of an ingredient
                        ingredCt = self.ingredientCount[ingredient]
                    #freguency of ingredient in particular cuisine
                        ingredInCusineA = self.cuisineMatrix[cuisine][ingredient]
                        ingredInCusineB = self.cuisineMatrix[cuisineHighFreq][ingredient]
                    #probability ingredient is in a certain cuisine, and store probability per cusine
                        CuisineProb[cuisine][ingredient] = float(ingredInCusineA / ingredCt)
                        CuisineProb[cuisineHighFreq][ingredient] = float(ingredInCusineB/ ingredCt)

                    #now we multiply the probabilities together, conditioned on each ingredients in recipe
                    for cuisine in CuisineProb:
                        for ingredient in CuisineProb[cuisine]:
                            tempChosenCuisineProb *=  CuisineProb[cuisine][ingredient]
                    #whichever has the greatest probability is the specified cuisine  
                    if tempChosenCuisineProb > chosenCuisineProb:
                        chosenCuisine = cuisine
                        chosenCuisineProb = tempChosenCuisineProb

                elif cuisineFreq[cuisine] > highestFreq:
                    cuisineHighFreq = cuisine
                    chosenCuisine = cuisine