import tkinter as tk
import random
from tkinter import messagebox

class game:
    def __init__(self, rows, columns, bombCount, debugMode):
        self.window = tk.Tk()
        self.rows = rows
        self.columns = columns
        self.bombCount = bombCount
        self.debugMode = debugMode #When True shows all bombs from beginning on
        self.firstClick = True # For leftMB() to check if it is the first time it gets ran to run setBombsRevealField()
        self.fields = []

    def startGame(self): #Creates the grid of buttons
        i = 0
        
        self.window.rowconfigure(1, weight=1)
        self.window.columnconfigure(0, weight=1)
        self.window.title("Minesweeper")

        fieldFrame = tk.Frame()
        fieldFrame.grid(row=1, column=0, sticky="nesw")
        for row in range(self.rows):
            fieldFrame.rowconfigure(row, weight=1)
            for column in range(self.columns):
                fieldFrame.columnconfigure(column, weight=1)
                self.fields.append(fieldClass(fieldFrame, row, column, i))
                self.fields[i].button["command"] = lambda i=i: self.leftMB(self.fields[i])
                self.fields[i].button.bind("<Button-3>", lambda e, i=i: self.rightMB(self.fields[i]))
                self.fields[i].button.grid(row=row, column=column, sticky="nesw")
                i += 1
        
        statframe = tk.Frame()
        statframe.grid(row=0, column=0)

        self.flagLabel = tk.Label(statframe, text="Flaggen/Bombem: 0/" + str(self.bombCount))
        self.openedLabel = tk.Label(statframe, text="Offene Felder: 0/" + str(self.rows * self.columns - self.bombCount))
        self.flagLabel.grid(column=0, row=0)
        self.openedLabel.grid(column=1, row=0)

        self.window.mainloop()
    
    def setBombs(self): #Randomly chooses bomb positions / Gets ran on first leftclick
        for bomb in range(self.bombCount):
            while True:
                chosen = random.randint(0, len(self.fields) - 1)
                if self.checkBomb()[chosen] == True:
                    continue
                else:
                    self.fields[chosen].mine = True
                    if self.debugMode == True:
                        self.fields[chosen].button["text"] = "O"
                    break

    def revealLoop(self, field): # Reveals the area around a chosen field
        surroundings = self.checkSurroundings(field)
        field.state = "open"
        if surroundings > 0: # Checks if bomb is by that field. If yes shows amount of bombs around the field and jumps back a field to reveal somewhere else.
            field.button["text"] = str(surroundings)
            field.button["bg"] = "#ffb957"
            field.flagged = False
        else: # If no bomb is by that field it continues to reveal towards the same direction.
            field.button["bg"] = "#d3f79c"
            field.button["text"] = "  "
            field.flagged = False
            for fld in [[field.row - 1, field.column - 1], [field.row - 1, field.column], [field.row - 1, field.column + 1], [field.row, field.column - 1], [field.row + 1, field.column - 1], [field.row, field.column + 1], [field.row + 1, field.column], [field.row + 1, field.column + 1]]: #[[field.row, field.column -1], [field.row, field.column + 1], [field.row - 1, field.column], [field.row + 1, field.column]]
                fld = self.getFieldByCoords(fld[0], fld[1])
                if fld != "outside":
                    if fld.state == "closed":
                        self.revealLoop(fld)
    
    def updateInfo(self): # Changes info on top of window
        openFieldCount = 0
        for fld in self.fields:
            if fld.state == "open" and fld.mine == False:
                openFieldCount += 1
        self.openedLabel["text"] = "Offene Felder: " + str(openFieldCount) + "/" + str(self.rows * self.columns - self.bombCount)

        remainingFlagCount = 0
        for fld in self.fields:
            if fld.flagged == True:
                remainingFlagCount += 1
        self.flagLabel["text"] = "Flaggen/Bomben: " + str(remainingFlagCount) + "/" + str(self.bombCount)
    
    def checkWin(self): # Checks if there are any closed non mines remaining. If not it returns True to say that the game has been won.
        for field in self.fields:
            if field.state == "closed" and not field.mine == True:
                return False
        return True
    
    def leftMB(self, field): # Gets ran on every left click. On the first click of the game it makes sure that no bombs are on ore around the first field.
        if self.firstClick == True:
            field.state = "open"
            for fld in [[field.row - 1, field.column - 1], [field.row - 1, field.column], [field.row - 1, field.column + 1], [field.row, field.column - 1], [field.row + 1, field.column - 1], [field.row, field.column + 1], [field.row + 1, field.column], [field.row + 1, field.column + 1]]:   
                fld = self.getFieldByCoords(fld[0], fld[1])
                if fld != "outside":
                    fld.state = "blocked"
            self.setBombs()
            for fld in self.fields:
                if fld.state == "blocked":
                    fld.state = "closed"
            self.revealLoop(field)
            self.firstClick = False
        else: # Gets ran on any other than the first left click. Check if it is mine, if yes the game has been lost.
            if field.mine == True:
                ids = []
                for bomb in self.fields:
                    if bomb.mine == True and bomb.flagged == False:
                        bomb.button["bg"] = "#ff7369"
                    elif bomb.mine == True and bomb.flagged == True:
                        bomb.button["bg"] = "#68c3fc"
                
                messagebox.showinfo("Verloren.", "Du hast diese Runde verloren.")
                self.window.destroy()
                return

            elif field.state == "closed":
                self.revealLoop(field)
            
        if self.checkWin() == True: # Checks if the game has been won. If yes it shows all unflagged bombs as red and all flagged bombs as blue
            for bomb in self.fields:
                if bomb.mine == True and bomb.flagged == False:
                    bomb.button["bg"] = "#ff7369"
                    bomb.button["text"] == "O"
                elif bomb.mine == True and bomb.flagged == True:
                    bomb.button["bg"] = "#68c3fc"
            messagebox.showinfo("GEWONNEN!", "Du hast diese Runde gewonnen!")
            self.window.destroy()

        self.updateInfo()

    def checkBomb(self): # Returns a list. Every variable is either True or False, stating if the field is a bomb. The index of the variable is also the id/index of the bomb
        output = []
        for field in self.fields:
            if field.mine == True or field.state != "closed":
                output.append(True)
            else:
                output.append(False)
        return output

    def rightMB(self, field): # Gets ran on every rightclick. Either turns a flagged field unflagged or an unflagged field flagged.
        if field.flagged == True:
            if self.checkSurroundings(field) != 0 and field.state == "open":
                field.button["text"] = self.checkSurroundings(field)
            else:
                field.button["text"] = "  "
            field.flagged = False
        else:
            field.button["text"] = "X"
            field.flagged = True
        
        self.updateInfo()
    
    def getFieldByCoords(self, row, column): # Returns field object of field at given grid coordinates.
        output = ""
        for field in self.fields:
            if field.row == row:
                if field.column == column:
                    output = field
                    return output
        return "outside"
    
    def checkSurroundings(self, field): # Checks if any bombs are around given field object.
        bombCounter = 0
        for fld in [[field.row - 1, field.column - 1], [field.row - 1, field.column], [field.row - 1, field.column + 1], [field.row, field.column - 1], [field.row + 1, field.column - 1], [field.row, field.column + 1], [field.row + 1, field.column], [field.row + 1, field.column + 1]]:
            if self.getFieldByCoords(fld[0], fld[1]) != "outside":
                if self.getFieldByCoords(fld[0], fld[1]).mine == True:
                    bombCounter += 1
        return bombCounter

class fieldClass: # The class of a field. Stores all the important variables of a field.
    def __init__(self, frame, row, column, id):
        self.row = row
        self.column = column
        self.id = id
        self.state = "closed"
        self.mine = False
        self.flagged = False
        self.button = tk.Button(frame, text="  ", height=1, width=2)