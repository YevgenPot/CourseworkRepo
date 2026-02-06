"""
New Design Adapated

   Starting from Input Handling

   now to Model Class and Presenter Class

   Model Class foucses on model calculation logic
   Presenter Class focuses on output display    
        Model Class callback_functions to Presenter optionally

in the future, will compile previous homeworks to their own model classes
"""

import numpy as np
import os
import matplotlib.pyplot as plt


def main():

    EPOCHS = 1000    
    #Learning Rate Initialized in Model Class

    inputMatrix = mainInput()

    model = LogisticRegression()
    presenter = ModelPresenter()
    costs = [] ## collection of cost data for plot


    model.initializeModel()

    #block of model + callback to presenter
    model.getIterations(presenter.printEpoch) # callback to presenter
    model.getCost(inputMatrix, presenter.printCost)
    model.getModelParam(presenter.printModelParam)
    costs.append(model.getCost(inputMatrix)) # model optionally does not callback to presenter here
    presenter.nextLine()

    #learning loop
    while model.getIterations() != EPOCHS:
        model.gradientDescent(inputMatrix)

        if model.getIterations() % 10 and not model.getIterations() % 100 == 0:
            costs.append(model.getCost(inputMatrix))

        if model.getIterations() % 100 == 0:
            model.getIterations(presenter.printEpoch)
            model.getCost(inputMatrix, presenter.printCost)
            model.getModelParam(presenter.printModelParam)
            presenter.nextLine()
    
    #presenter printing new data prediction
    presenter.activePredictions(4.5, model.getPrediction(4.5))
    presenter.nextLine()
    presenter.activePredictions(6.5, model.getPrediction(6.5))
    presenter.nextLine()

    #matlibplot code
    plt.plot( range(len(costs)), costs, color='blue')
    plt.xlabel("Iteration")
    plt.ylabel("Cost")
    plt.title("Cost over Iterations")
    plt.grid(True)
    plt.show()



###############################################################
################Input Handling#################################
###############################################################

def mainInput():
    """
    gets user's choice of file input or terminal input
    exits with a return of matrix of x,y
    """
    userinputX_YList = []
    
    userChoice = 0
    while userChoice != 1 and userChoice != 2:
        userChoice = promptIntInput("Enter 1 for file input or 2 for terminal input: ")
        if userChoice == 1:
            print("file input...")

            userinputX_YList = readFile('dataText.txt')

        elif userChoice == 2:
            print("terminal input...")            
            count_of_data_points = 0
            while count_of_data_points < 2:
                count_of_data_points = promptIntInput("Enter the number of data points: ")
                if count_of_data_points < 2:
                    print("Error: Invalid input. Enter at least 2 data points.")

            userinputX_YList = generateinputX_YList(count_of_data_points)

        else:
             print("Oops. Invalid input.")

    checkInputSizeValidation(userinputX_YList)
    userinputX_YList = sort_AninputX_YList(userinputX_YList)

    userinputX_YMatrix = np.array(userinputX_YList)
    return userinputX_YMatrix

# Sub Functions for Input Handling

def promptIntInput(PromptString):
    """
    gets string that is the view prompt
    process user input
    returns valid integer input"""
    while True:
        try:
            return int( input( PromptString))
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
    
def generateinputX_YList(count_of_data_points):
    userinputX_YList = []
    for i in range(count_of_data_points):
        while True:
            try:
                x_input = int(input("Enter x value: "))
                y_input = int(input("Enter y value: "))
                userinputX_YList.append((x_input,y_input))
                break
            except ValueError:
                print("Invalid input. Please enter valid integer values.")

    return userinputX_YList

def readFile(fileString):
    """
    expects a string of the file name and returns a list of tuples of the file contents
    using os.path to get the file path
    """
    userinputX_YList = []

    filePath = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(filePath, fileString)

    with open( path, 'r') as file:

        for line in file:
            if line.strip().startswith('#') or line.strip() == '':
                continue
            x, y = map(lambda value: int(float(value)), line.strip().split())
            userinputX_YList.append((x, y))

    return userinputX_YList


def checkInputSizeValidation(inputX_YList): 
    if len(inputX_YList) < 2:
        raise ValueError("Input list must have at least 2 elements.")

def sort_AninputX_YList(inputX_YList):
    """
    expects input of a list of integers with the first row element the x value
    expected output of a sorted list of tuples with the first element the x value"""
    return sorted(inputX_YList, key=lambda x: x[0])


###############################################################
##############Logistic Regression Calculations#################
###############################################################
'''
class model
logic for logistic regression
'''

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

###############################################################

class LogisticRegression:
    def __init__(self):
        self.m , self.b, self.learningRate, self.iterations= self.initializeModel()

    def initializeModel(self): # placeholder func if involved initialization process is needed
        return .5, 0, 0.1 , 0
    
    def getModelParam(self, callback_PresentParams = None):

        if callback_PresentParams is not None: ## optional 
            callback_PresentParams(self.m, self.b)
        return self.m, self.b
    
    def getPrediction(self, x_new_instance, callback_PresentPrediction = None):
        prediction = 1 if sigmoid(self.m * x_new_instance + self.b) >= 0.5 else 0

        if callback_PresentPrediction is not None: ## optional present callback
            callback_PresentPrediction(prediction)
        return prediction
    
    def getCost(self, inputX_YMatrix, callback_PresentCost = None):

        x = inputX_YMatrix[:,0]
        y = inputX_YMatrix[:,1]
        yhat = sigmoid(self.m * x + self.b)
        yhat = np.clip(yhat, 1e-8, 1 - 1e-8) ## prevent log 0

        BCE = (-1/len(x)) * np.sum(y * np.log(yhat) + (1 - y) * np.log(1 - yhat)) # binary cross entropy

        if callback_PresentCost is not None: ## optional give return to presenter
            callback_PresentCost(BCE)
        return BCE

    def getIterations(self, callback_PresentIterations = None):
        if callback_PresentIterations is not None: ## optional 
            callback_PresentIterations(self.iterations)
        return self.iterations
    
    def gradientDescent(self, inputX_YMatrix):
        x = inputX_YMatrix[:,0]
        y = inputX_YMatrix[:,1]
        z = self.m * x + self.b # z vector used in sigmoid
        yhat = sigmoid(z)
        yhat = np.clip(yhat, 1e-8, 1 - 1e-8) ## prevent log 0

        sigmoidDerivative = yhat * (1 - yhat) # i think this simplifies to yhat-y

        costGradient = 4*(yhat - y) # for some reason the cost gradient is 4 times

        loss_grad_m = (1/len(x)) * np.sum(costGradient * x)
        loss_grad_b = (1/len(x)) * np.sum(costGradient)

        self.m -= (self.learningRate * loss_grad_m)
        self.b -= ( self.learningRate * loss_grad_b )
        self.iterations += 1
   

########################################################
################# Output Display #######################
########################################################
"""
a class ModelPresenter
uses optional callback functions
called from a model class
in main
"""


class ModelPresenter:
    def __init__(self):
        pass
    
    def printModelParam(self, m, b):
        print(f"W: {m:8.4f}  | B: {b:8.4f}", end="|  ")

    def printCost(self, cost):
        print(f"Cost: {cost:10.4f}", end="|  ")

    def printEpoch(self, epoch):
        print(f"Epoch: {epoch:<6}", end="|  ")

    def activePredictions(self, x, yhat): # x new data, model's getPrediction
        print(f"Prediction for x: {x:6.1f}  ŷ: {yhat:6.0f}", end="  ")

    def nextLine(self):
        print()


if __name__ == "__main__":
    main()