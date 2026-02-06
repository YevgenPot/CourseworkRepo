"""
ML regression

 +------------------+        +------------------------+        +------------------------+
 | Input Handling   | ---->  | Linear Regression       | ---->  | Prediction Generation   |
 | (Data Input)     |        | Calculation (m, b)      |        | (Generate predictions)  |
 +------------------+        +------------------------+        +------------------------+
          |                           |                       /         
          v                           v                      /          
 +------------------+        +------------------------+     /                            
 | Output Generation| <----  | Display Results        |<---/                                
 | (Return Results) |        | (e.g., Console, File)  |                                   
 +------------------+        +------------------------+                                  


Entry Criteria-
    Input handler reads terminal inputs or data file
    Data in file is a set of labeled data points : (x_values, y_values)
    at least 2 data points must be provided(both terminal and file)

Exit Criteria-
    Program ends after execution
    print out original set of data
    print out line of best fit values m and b
    print out mean squared error
    print out model predition y_hat for each x_values

"""

import os

def main():

    userDataList = mainInput()

    mAndBList = mainPiecewiseCalculation(userDataList)

    modelYhatList, modelSlope, modelIntercept, MSE = mainPredictions(userDataList,mAndBList)

    mainOutputDisplay(userDataList,mAndBList,modelYhatList,modelSlope,modelIntercept, MSE)
    
    print("finished")

################INPUT HANDLING########################
"""
a collection of input related functions
including some user input validation
outputs a list of data points x and y"""

def mainInput():
    """
    gets user's choice of file input or terminal input
    exits with a return of list of data points x and y
    """
    userinputX_YList = []
    
    userChoice = 0
    while userChoice != 1 and userChoice != 2:
        userChoice = promptIntInput("Enter 1 for file input or 2 for terminal input: ")
        if userChoice == 1:
            print("file input...")

            userinputX_YList = readFile()

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
    return userinputX_YList
            
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

def readFile():
    userinputX_YList = []

    filePath = os.path.dirname(os.path.abspath(__file__))

    path = os.path.join(filePath, 'dataText.txt')

    with open(path, 'r') as file:

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

"""methods related to individual
    linear regression calculations
    input a list of data points(sorted)
    outputs a list of piecewise slope and intercepts"""

def mainPiecewiseCalculation(inputX_YList): 
    mAndBList = generate_m_And_B_List(inputX_YList)
    return mAndBList

def calculate_Slope_and_Intercept(x1,x2,y1,y2):
    slope = (y2 - y1) / (x2 - x1) 
    y_intercept = (- x1*y2 + x2*y1)/ (x2 - x1)
    return slope, y_intercept

def generate_m_And_B_List(inputX_YList):
    mAndBList = []
    for i in range(len(inputX_YList)-1):
        mAndBList.append(calculate_Slope_and_Intercept(inputX_YList[i][0],inputX_YList[i+1][0],inputX_YList[i][1],inputX_YList[i+1][1]))
    return mAndBList    


#########################################################
############### Prediction Generation ###################
#########################################################

"""
expects input of list of piecewise slope and intercepts
expected output of list of yhats, and avgerage slope and intercept"""

def mainPredictions(inputX_YList,mAndBList):

    avgSlope = generate_Average_Slope(mAndBList)
    avgIntercept = generate_Average_Intercept(mAndBList)

    predictions = []
    for i in range(len(inputX_YList)):
        predictions.append(avgSlope*inputX_YList[i][0] + avgIntercept)

    return predictions, avgSlope, avgIntercept, caLculate_MSE(inputX_YList,predictions)

def calculateAverageColumns(mAndBList, columnIndex):
    sum = 0
    for i in range(len(mAndBList)):
        sum += mAndBList[i][columnIndex]
    return ( sum/len(mAndBList) )

def generate_Average_Slope(mAndBList):
    calculateAverage = calculateAverageColumns(mAndBList,0)
    return calculateAverage

def generate_Average_Intercept(mAndBList):
    calculateAverage = calculateAverageColumns(mAndBList,1)
    return calculateAverage

def caLculate_MSE(inputX_YList,yHatList):
    sum = 0
    for i in range(len(inputX_YList)):
        sum += ( yHatList[i] - (inputX_YList[i][1]) )**2
    return (1/len(inputX_YList)) * sum


########################################################
################# Output Display #######################
########################################################
"""
a collection of functions 
for output display of data(rounded)"""

def mainOutputDisplay(inputX_YList,mAndBList,predictionsyHat,avgSlope,avgIntercept, MSE):

    print("After sorting the input list of " + str(len(inputX_YList)) + " Inputs: ")
    for i in inputX_YList:
        print( round(i[0] , 2) , round(i[1] , 2))

    print("The piecewise slopes and intercepts are: ")
    for i in mAndBList:
        print(round(i[0] , 2), round(i[1], 2 ))

    print("model predictions for parameters are: ", avgSlope, avgIntercept)

    print("The discrepencies between the model and the data is: ")
    for i, j in zip(inputX_YList, predictionsyHat):
        print(  round(j,2) , round(i[1] ,2 ) )

    print("The Mean Squared Error: " , round(MSE,6) )  



if __name__ == "__main__":
    main()
