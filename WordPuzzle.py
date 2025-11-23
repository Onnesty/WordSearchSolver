# Wrote by Onnesty (Genshin Gooner) Oct 20, 2025
# Personal Project
import customtkinter as ctk
import random

class Main():

    def __init__(self):
        self.App = ctk.CTk()

        Device_Screen_Width = self.App.winfo_screenwidth()
        Device_Screen_Height = self.App.winfo_screenheight()

        self.AppWidth = int(Device_Screen_Width * 0.3)
        self.AppHeight = int(Device_Screen_Height * 0.7)


        self.App.title("Word Search Solver")
        self.App.geometry(f"{self.AppWidth}x{self.AppHeight}")
        ctk.set_appearance_mode("dark")


        self.Height = 9
        self.Width = 9
        self.WordList = [] 
        self.CellList = [] # For tracking where to input , Contains the string names of the Cells
        self.CellTextDict = {} # For tracking the text inside the Labels, Contains { strname, textinside }
        self.CellDict = {} # For easy access to Label Objs, Contains { strname, actualobj }
        self.FoundWordsDict = {} # For easy access to the Objs that form the found word ( This is for the individual word showing ), 
                                 #Contains { wordname, list of obj where each contain the list of label objs and their assigned color}
                                 # [Obj1, OBj2, Obj3] Where each object signifies an instance of the word, and Obj1.ObjList contains the actual objs 

        self.DefaultTheme = {
            "bg_color" : "#1f1f1f",
            "font" : ("Century Schoolbook", 24),
        }


    def Start(self): # Initializes

        self.InitialQuery()

        self.App.mainloop()

   
    def InitialQuery(self): # Asks Information about the supposed Grid

        Height = ctk.IntVar(value = "9")
        Width = ctk.IntVar(value = "9")

        GridValues = [str(i) for i in range(9,21)]

        def EnterText(event = None):
            input = WordInput.get().replace(" ","")
            if not input :
                return # If theres no input
            self.WordList.append(input.upper())
            
            WordDisplay.configure(state = "normal")
            WordDisplay.insert("end", input.upper() + " ")
            WordDisplay.see("end")
            WordDisplay.configure(state = "disabled")

            WordInput.delete(0, "end")

        def QueryEnd():
            WordInput.unbind("<Return>")
            self.Height = Height.get()
            self.Width = Width.get()
            self.InitCont.place_forget()  
            self.Draw()
            

        self.InitCont = ctk.CTkFrame(master = self.App, width = self.AppWidth, height = self.AppHeight, fg_color = "#242424")
        self.InitCont.place(relx = 0.5, rely = 0.5, anchor = "center")
    
        StartButton = ctk.CTkButton(master = self.InitCont, text = "Next", bg_color = "transparent", fg_color = "gray" , font = ("Century Schoolbook", 18),
                                     text_color = "white", height = 30, width = 70, hover = "disable", cursor = "hand2", command = QueryEnd)
        StartButton.place(relx = 0.85, rely = 0.01)


        HigLabel = ctk.CTkLabel(master = self.InitCont, text = "Input Height", **self.DefaultTheme)
        HigLabel.place(relx = 0.5, rely = 0.1, anchor = "center")

        HigInput = ctk.CTkOptionMenu(master = self.InitCont, width = 100, height = 30, variable = Height, values = GridValues, **self.DefaultTheme)
        HigInput.place(relx = 0.5, rely = 0.18, anchor = "center")


        WidLabel = ctk.CTkLabel(master = self.InitCont, text = "Input Width", **self.DefaultTheme)
        WidLabel.place(relx = 0.5, rely = 0.3, anchor = "center")
        
        WidInput = ctk.CTkOptionMenu(master = self.InitCont, width = 100, height = 30, variable = Width, values = GridValues, **self.DefaultTheme)
        WidInput.place(relx = 0.5, rely = 0.38, anchor = "center")
        

        WordLabel = ctk.CTkLabel(master = self.InitCont, text = "Input Words To Find", **self.DefaultTheme)
        WordLabel.place(relx = 0.5, rely = 0.5, anchor = "center")
        
        WordInput = ctk.CTkEntry(master = self.InitCont, width = 200, height = 30, justify = "center", bg_color = "#1f1f1f", font = ("Century Schoolbook", 16))
        WordInput.place(relx = 0.5, rely = 0.57, anchor = "center")
        WordInput.bind("<Return>", EnterText) 


        WordDisplay = ctk.CTkTextbox(master = self.InitCont, state = "disabled", bg_color = "#1f1f1f", width = 400, wrap = "word",
                                     font = ("Century Schoolbook", 12), border_color = "gray", border_width = 2, )
        WordDisplay.place(relx = 0.5, rely = 0.8, anchor = "center", )

    
    def Draw(self): # Draws the Grid
        def Reset():
            self.BoardCont.place_forget()
            self.App.unbind("<Key>")
            self.CurrPosition = 0
            self.Limit = len(self.CellList)
            self.Height = 9
            self.Width = 9
            self.WordList = [] 
            self.CellList = [] 
            self.CellTextDict = {}
            self.CellDict = {} 
            self.FoundWordsDict = {}
            self.InitialQuery()
        

        self.BoardCont = ctk.CTkFrame(master = self.App, fg_color = "#242424", width = self.AppWidth, height = self.AppHeight)
        self.BoardCont.place(relx = 0.5, rely = 0.5, anchor = "center")

        Instruction = ctk.CTkLabel(master = self.BoardCont, text = "Input Letters Then Enter", font = ("Century Schoolbook", 16))
        Instruction.place(relx = 0.5, rely = 0.03, anchor = "center")

        Board = ctk.CTkFrame(master = self.BoardCont,  fg_color = "#242424")
        Board.place(relx = 0.5, rely = 0.1, anchor = "n", relwidth = 0.9, relheight = 0.6)

        self.FoundWords = ctk.CTkScrollableFrame(master = self.BoardCont, fg_color = "#242424", height=100, width=200)
       
        ResetButton = ctk.CTkButton(master = self.BoardCont, text = "Reset", bg_color = "transparent", fg_color = "gray" , font = ("Century Schoolbook", 18),
                                     text_color = "white", height = 30, width = 70, hover = "disable", cursor = "hand2", command = Reset)
        ResetButton.place(relx = 0.85, rely = 0.01)

        XIncrement = self.AppWidth / self.Width / self.AppWidth 
        YIncrement = self.AppHeight / self.Height / self.AppHeight 
        for Row in range(self.Height):
            for Col in range(self.Width):
                Name = f"{chr(ord('A')+ Row)}{Col+1}"
                LabelObj = ctk.CTkLabel(master = Board, text = "", fg_color="#242424", font = ("Century Schoolbook", 14),)
                LabelObj.place(relx = 0.001 + (XIncrement * Col), rely = 0.001 + (YIncrement * Row), anchor = "nw", relwidth = XIncrement, relheight = YIncrement) 
                
                self.CellList.append(Name)
                self.CellDict[Name] = LabelObj

        self.App.bind("<Key>", self.KeyPress) # Allow typing after drawing
        self.CurrPosition = 0 # Set the input to the first ( input in the Cell List )
        self.Limit = len(self.CellList) # Limit so that our Curr Position doesnt go out of bounds


    def KeyPress(self, event):
        if event.char:
            if event.char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
                self.Input (event.char)
            if event.keysym == "Return" or event.keysym == "BackSpace":
                self.Input (event.keysym)
    
    def Input(self, data):
        if (data == "BackSpace"):
            if (self.CurrPosition != 0): # To avoid going out of bounds when 0
                self.CurrPosition -= 1
            ObjName = self.CellList[self.CurrPosition]
            self.CellDict[ObjName].configure( text = "" )

        elif (data == "Return" and self.CurrPosition == self.Limit):
            
            self.FoundWords.place(relx = 0.5, rely = 0.7, anchor = "n") # For Mainlogic to add buttons to this
            
            self.MainLogic()
            self.App.unbind("<Key>")


        elif (self.CurrPosition < self.Limit and data != "Return"): # Should prevent it from config when at limit
            ObjName = self.CellList[self.CurrPosition]
            self.CellDict[ObjName].configure( text = data.upper() )
            self.CellTextDict[ObjName] = data.upper() 
            self.CurrPosition += 1 # Overflows 1 over the limit


    def MainLogic(self):
        
        self.CharDict = {}
        for Words in self.WordList: # Stores all the words by their first char
            if (Words[0] in self.CharDict):
                self.CharDict[Words[0]].append(Words)
            else:
                self.CharDict[Words[0]] = [Words]
        
        for Cells in self.CellList: # Goes over every Cell
            CharKey = self.CellTextDict[Cells] # Get the letter in that Cell
            if (CharKey in self.CharDict): # Matched first char or letter

                for Words in self.CharDict[CharKey]: # For every word in list that starts with that letter
                    # For every word checks in every direction
                    # NOTE: The layout starts at the top left so going north is -1 and south is +1

                    # One Color per Word
                    RndNums = random.sample( range(0,256), k = 3 )
                    AssignedColor = f"#{ hex( RndNums[0] )[2:] }{ hex( RndNums[1] )[2:] }{ hex( RndNums[2] )[2:] }"
                    while (len(AssignedColor) < 7): # For missing Shi ( I guess cuz the hex omits trailing zeros )
                        AssignedColor += '0'
                    for x,y in [ [0,-1], [0,1], [1,0], [-1,0], [1,-1], [-1,-1], [1,1], [-1,1]]: # N S E W NE NW SE SW
                        NextCell = ( chr(ord(Cells[0]) + y) + (str( int(Cells[1:])+x )) ) # (str( int(Cells[1:])+x )) since the last part is a number, cant ord chr that and it could be multiple chars like 11 or 12
                        DFSOBJ = self.DFS(1, Words, [x,y], NextCell)

                        if (DFSOBJ.Verdict): 
                            SuccessCell = self.CellDict[Cells]
                            DFSOBJ.ObjList.append(SuccessCell) # Add current cell to the Obj
                            DFSOBJ.AssignedColor = AssignedColor 

                            if (Words in self.FoundWordsDict): # If word already exists
                                self.FoundWordsDict[Words].append(DFSOBJ) # Append since the val is a list
                            else: # IF not
                                self.FoundWordsDict[Words] = [DFSOBJ] # Initialize pair

                                FoundWordButton = ctk.CTkButton(master  = self.FoundWords, text = Words, fg_color = "transparent", height = 30, font = ("Century Schoolbook", 16),
                                                            command = lambda Name = Words: self.DisplayWord(Name)) # Sends own name to Display Word
                                FoundWordButton.pack(fill = "x") # Place into the Found Word scrollbar


                        


                        # I could just put the non recursive solution here but the DFS allows for backtracking for when a successfull match happens, 
                        # it will return 1 and it will signify to the previous Obj Labels to highlight themselves


    def DFS(self, IndexToCheck, Word, Direction, CurrCell):
        FalseObj = DFSReturnObj()
        if CurrCell not in self.CellList:
            return FalseObj # Do not continue if it is out of bounds, No arguments means its 0 by default
        
        CellChar = self.CellTextDict[CurrCell]
        if Word[IndexToCheck] == CellChar: # If the expected char is seen in the curr cell
            IndexToCheck += 1
            
            if (IndexToCheck == len(Word)): # Means that the index has surpassed the length of the Word meaning it was the last match needed
                SuccessCell = self.CellDict[CurrCell]
                return DFSReturnObj(1, [SuccessCell])
            else: # Go to next Cell in given direction
                x, y = Direction
                NextCell = ( ( chr(ord(CurrCell[0]) + y) + (str( int(CurrCell[1:])+x )) ) )
                
                DFSOBJ = self.DFS(IndexToCheck, Word, Direction, NextCell) 
                # We are expecting a verdict here from the cells ahead
                if (DFSOBJ.Verdict): # If there is a full match
                    SuccessCell = self.CellDict[CurrCell]
                    DFSOBJ.ObjList.append(SuccessCell) # Add current cell to the Obj
                    return DFSOBJ # Signify to previous cells
                else:
                    return DFSOBJ # No modifications since its already Verdict 0
        else:
            return FalseObj
        

    def DisplayWord (self, Name):
        # Clears Color
        for strname in self.CellList:
            self.CellDict[strname].configure(text_color = "white")

        # Colors specific Label
        for Objs in self.FoundWordsDict[Name]: # Accesses the Objs paired with the name, they contain the Label Objs where the words can be found
            for LabelObj in Objs.ObjList:
                LabelObj.configure(text_color = Objs.AssignedColor)




class DFSReturnObj: # For  our DFS callbacks to return a multitude of data
    
    def  __init__(self, Ver = 0, OLst = [], Color = ""):
        self.Verdict = Ver
        self.AssignedColor = Color
        self.ObjList = OLst

        
if __name__ == "__main__":
    main = Main()
    main.Start()