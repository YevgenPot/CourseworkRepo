import numpy as np
import os


def main():

    inputMatrix = mainInput()

    m, b = mainCalculations(inputMatrix)
    
    predictionsyHat, MSE = mainPredictions(m, b, inputMatrix)

    mainOutputDisplay(inputMatrix, m, b, predictionsyHat, MSE)


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
################Linear Regression Calculations#################
###############################################################
'''
Input: matrix of x,y's
Output:model param m and b

takes a vector of x's and a vector of y's
calculates the final derivation matrix solution
'''

def mainCalculations(inputX_YMatrix):
    x = inputX_YMatrix[:,0]
    y = inputX_YMatrix[:,1]
    
    sum_x = np.sum(x)
    sum_y = np.sum(y)
    sum_xy = np.sum(x * y)
    sum_x2 = np.sum(x * x)

    m = (sum_xy - (sum_x * sum_y) / len(x)) / (sum_x2 - (sum_x * sum_x) / len(x))
    b = (sum_y - m * sum_x) / len(x)

    return m, b

#########################################################
############### Prediction Generation ###################
#########################################################
'''
Input: model param
Output: list of predictions, MSE
'''
def mainPredictions(m, b, inputX_YMatrix):
    predictionsyHat = []

    for x in inputX_YMatrix[:,0]:
        yhat = m * x + b
        predictionsyHat.append(float(yhat) )

    return predictionsyHat, MSE(predictionsyHat, inputX_YMatrix)

def MSE(predictionsyHat, inputX_YMatrix):
    return np.mean((predictionsyHat - inputX_YMatrix[:,1]) ** 2)

########################################################
################# Output Display #######################
########################################################
"""
a collection of functions 
for output display of data(rounded)"""

def mainOutputDisplay(inputX_YMatrix, m, b, predictionsyHat, MSE):

    print("After sorting the input list of " + str(len(inputX_YMatrix)) + " Inputs: ")
    for i in inputX_YMatrix:
        print( f"{round(i[0] , 2):>5} {round(i[1] , 2):>5}" )

    print("model predictions for parameters (m,b) are: ", round(m,2), round(b,2))

    print("The discrepencies between the model and the data is: (x, y^, y, |ERR|) ")
    for i, j in zip(inputX_YMatrix, predictionsyHat):
        #print(  round(j,2) , round(i[1] ,2 ) , round( np.abs(i[1] - j), 2) )
        print(f" {round(i[0] , 2):<5} {round(j,2):>5} {round(i[1] ,2):>5} {round( np.abs(i[1] - j), 2):>10}")

    print("The Mean Squared Error: " , round(MSE,6) )


if __name__ == "__main__":
    main()