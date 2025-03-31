## Keoki's DataHandler module manages 3 different text files: OrderHistoryFile.txt, LiquorInventoryFile.txt, LiqIDListFile.txt

class DataBaseHandler:
    def __init__(self):
        pass

    #Called by theController and saves all of the lists
    def SaveLiquorInv(self, newLiquorList, ChangesList):
        try:
            self.WriteLiquorInv(newLiquorList)
            self.WriteOrderHistory(ChangesList)
            self.WriteLiqIDList(newLiquorList)
            return "Liquor inventory saved successfully."
        except Exception as e:
            return f"Error saving liquor inventory: {str(e)}"
    
    #Returns order History
    def GetOrderHistory(self):
        try:
            return self.ReadOrderHistory()
        except Exception as e:
            return f"Error getting order history: {str(e)}"
    
    #Returns current liquor inventory in [ [ID,NAME,Volume,Quanity] , ... ]
    def GetLiquorInv(self):
        try:
            return self.ReadLiquorInv()
        except Exception as e:
            return f"Error getting liquor inventory: {str(e)}"
    
    #Returns all liquor invintory DOES NOT FUNCTION
    def GetAllLiquors(self):
        try:
            return self.ReadLiqIDList()
        except Exception as e:
            return f"Error getting all liquors: {str(e)}"
    
    #Opens the OrderHistory File
    def ReadOrderHistory(self):
        with open("OrderHistoryFile.txt", "r") as file:
            return [line.strip("[]\n  ").split(',') for line in file.readlines()]
    
    #Opens the LiquorInventoryFile File
    def ReadLiquorInv(self):
        with open("LiquorInventoryFile.txt", "r") as file:
            return [line.strip("[]\n \  ").split(',') for line in file.readlines()]

   #Opens the LiqIDListFile File 
    def ReadLiqIDList(self):
        with open("LiqIDListFile.txt", "r") as file:
            return file.readlines()
    
    #writes to the LiqIDListFile File
    def WriteLiquorInv(self, liquorList):
        with open("LiquorInventoryFile.txt", "w") as file:
            for item in liquorList:
                file.write(f"{item}\n")
   
    #Writes to the OrderHistoryFile File
    def WriteOrderHistory(self, changesList):
        with open("OrderHistoryFile.txt", "a") as file:
            for change in changesList:
                file.write(f"{change}\n")
    
    #Writes to the LiqIDListFile File
    def WriteLiqIDList(self, liquorList):
        with open("LiqIDListFile.txt", "w") as file:
            for item in liquorList:
                file.write(f"{item}\n")

     #Will format the list in some way?
    def FormatLiquorList(rawList):
        formattedList = []
        for item in rawList:
            # Add formatting here
            formattedList.append(item)
        return formattedList
    
    #Sorts by Liquor ID, does not work
    def SortList(listToSort):
        return sorted(listToSort)
    

    def HasNewLiquor(liquorList):
        return len(liquorList) > 0

#EOF

# Example

'''

controller = DataBaseHandler()
newLiquorList = [["001","tito's","1L","6"], ["006","Tanquaray","1L","2"], ["005","Deep Eddy's Lemon","1.5L","3"],["012","Extoico Reposado","1.75L","0"]]
changesList = [["O002","Date HERE"],["001","+3"], ["002","+3"],["005","-1"]]

print(controller.SaveLiquorInv(newLiquorList, changesList))
print(controller.GetOrderHistory())
print(controller.GetLiquorInv())
dave = controller.GetLiquorInv()
print(dave[0][3])
for each in  dave:
    print(each)


'''