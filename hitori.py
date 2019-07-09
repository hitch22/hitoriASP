"""
@author: Jaesub Shim
@email:jashim@ttu.edu
@date: 5 July, 2019
@version: 0.1
@requried: clingo, mkatoms, PyQt5

@desc: This program solves Hitori puzzle using Anser Set Programming. It uses PyQt5 for UI to let user input numbers, 
and it passes on the user input along with ASP logic file onto ASP solver through system call to get the puzzle solution, 
which is displayed on GUI. It requires dependencies, such as clingo, mkatoms, and PyQt5, and has been tested to work on Ubuntu Linux 14.04. 
The GUI is built using PyQt5 and styling used is "Fusion", which may or may not display correctly in other systems.

To sovle a Hitori puzzle with the program, supply numbers to the input boxes and click on the set button to finish input.
Then, click on solve button to solve the puzzle. Reset button can be used to clear the input box grid. 
The program will display a message box if no answer can be found.

The program will not work and display the error messages with no solutions if required dependencies are not met or not installed.

"""

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QVBoxLayout, QMessageBox, QGridLayout, QLineEdit, QMainWindow, QPushButton
from PyQt5.QtCore import QSize, pyqtSlot, pyqtSignal, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import os
from collections import *
import logging


logging.basicConfig(filename='hitori.log',level=logging.DEBUG)


"""@desc: The class represents the main UI window for the program with an 5x5 inputbox grid, set, reset, and solve buttons.
Set button causes the user input to be encoded into a file. Reset button clears all the inputboxes. 
Solve executes the routine for solving the puzzle in ASP. """
# App Window
class MainWindow(QWidget):
    
    cell2DVal = [[0]*5 for v in range(5)]
    
    # set up the main window
    def __init__(self):

        # set up the QWidget window
        super().__init__()
        # set the layout to grid
        grid = QGridLayout()
        grid.setVerticalSpacing(0)
        grid.setHorizontalSpacing(0)
        grid.setSpacing(0)
        
        
        self.setLayout(grid)
        self.setWindowTitle("Hitori Solver")
                 
        # create a 5x5 2D array of QLineEdit objects
        self.cell2D = [[QLineEdit(self) for j in range(5)] for i in range(5)]
              
        for i in range(5):
            for j in range (5):
                self.cell2D[i][j].setFixedWidth(100)
                self.cell2D[i][j].setFixedHeight(100)
                self.cell2D[i][j].setAlignment(Qt.AlignCenter)
                                
                # QLabels with coordinates for easier debugging
                # grid.addWidget(QLabel("("+str(i)+" , "+str(j)+")") , i,j)

                # add QLineEdit obj to the grid
                grid.addWidget(self.cell2D[i][j] , i,j, alignment = Qt.AlignLeft )
                
                # validate user input values. marshall them to be a single digit number btw 0 and 9
                regex=QRegExp("[0-9]")
                validator = QRegExpValidator(regex, self.cell2D[i][j])
                # set the defined validator to each QLineEdit obj
                self.cell2D[i][j].setValidator(validator)

        # set up the buttons
        setBtn = QPushButton("Set")
        resetBtn = QPushButton("Reset")
        solveBtn = QPushButton("Solve")

        setBtn.setFixedWidth(100)
        resetBtn.setFixedWidth(100)
        solveBtn.setFixedWidth(100)

        # add the buttons to the grid layout
        grid.addWidget(setBtn)
        grid.addWidget(resetBtn)
        grid.addWidget(solveBtn)
        
        # set up button event handler and signals
        setBtn.clicked.connect(self.setGrid)
        # for debugging
        #setBtn.clicked.connect(self.setTestGrid)
        resetBtn.clicked.connect(self.resetGrid)
        solveBtn.clicked.connect(self.solveHitoriPuzzle)

    """@desc: The method reads user input values from the QLineEdit objects and calls methods 
    to print them and store them into userInput.lp file
    @param: None
    @returns: None"""
    def setGrid(self):
        print(">>>>>>Begin setGrid Routine<<<<<")
        for i in range(5):
            for j in range(5):
                #print(self.cell2D[i][j].text())
                self.cell2DVal[i][j] = self.cell2D[i][j].text()
        self.printValGrid()
        self.printValGrid2F("userInput.lp")
        print(">>>>>>End setGrid Routine<<<<<")
    
    # for debugging
    # test case for a known grid and answer
    def setTestGrid(self):
        print(">>>>>>Begin setTestGrid Routine<<<<<")
        
        self.cell2D[0][0].setText("4")
        self.cell2D[0][1].setText("1")
        self.cell2D[0][2].setText("5")
        self.cell2D[0][3].setText("3")
        self.cell2D[0][4].setText("2")

        self.cell2D[1][0].setText("1")
        self.cell2D[1][1].setText("2")
        self.cell2D[1][2].setText("3")
        self.cell2D[1][3].setText("5")
        self.cell2D[1][4].setText("5")

        self.cell2D[2][0].setText("3")
        self.cell2D[2][1].setText("4")
        self.cell2D[2][2].setText("4")
        self.cell2D[2][3].setText("5")
        self.cell2D[2][4].setText("1")

        self.cell2D[3][0].setText("3")
        self.cell2D[3][1].setText("5")
        self.cell2D[3][2].setText("1")
        self.cell2D[3][3].setText("5")
        self.cell2D[3][4].setText("4")

        self.cell2D[4][0].setText("5")
        self.cell2D[4][1].setText("2")
        self.cell2D[4][2].setText("5")
        self.cell2D[4][3].setText("1")
        self.cell2D[4][4].setText("3")

        for i in range(5):
            for j in range(5):
                #print(self.cell2D[i][j].text())
                self.cell2DVal[i][j] = self.cell2D[i][j].text()

        self.printValGrid()
        self.printValGrid2F("userInput.lp")
        print(">>>>>>End setTestGrid Routine<<<<<")

    # for debugging
    def printValGrid(self):
        print(">>>>>>Begin printValGrid Routine<<<<<")
        for i in range(5):
            for j in range(5):
                print(self.cell2DVal[i][j], end=' ')
                logging.debug(self.cell2DVal[i][j]+" ")
            print("\n")
            logging.debug("\n")
        print(">>>>>>End printValGrid Routine<<<<<")


    """@desc: The method takes output file name and prints out the user-input values in the cell grids
    into a file that contains facts about the cell values in the form of cell(row idx, col idx, value)
    @param: output filename for user input.
    @returns: None. """
    def printValGrid2F(self, outFile):
        print(">>>>>>Begin printValGrid2F Routine<<<<<")
        with open(outFile, "w") as out:
            for i in range(5):
                for j in range(5):
                    # Skip, in case user misses to fill out some cells.
                    if self.cell2D[i][j].text() == "":
                        continue
                    else:
                        out.write("cv("+str(i)+","+str(j)+","+str(self.cell2DVal[i][j])+").")
                out.write("\n")
        print(">>>>>>End printValGrid2F Routine<<<<<")

    """@desc: The method resets and clears the user-input grid as well as the data file fed into clingo. Also, it clears the black cells.
    @param: None.
    @returns: None."""
    def resetGrid(self):

        dataFile = "userInput.lp"
        print(">>>>>>Begin resetGrid Routine<<<<<")
        print("Reset Grid!")
        for i in range(5):
            for j in range(5):
                self.cell2D[i][j].setText("")
                self.cell2D[i][j].setStyleSheet("""QLineEdit { background-color: white;}""")
                self.cell2D[i][j].setEnabled(True)
        
        if(os.path.exists(dataFile)):
            os.remove(dataFile)
        

        print(">>>>>>End resetGrid Routine<<<<<")
    
    """@desc: The method takes userInput.lp file for data and logic.lp file for logic and passes them onto clingo system call as arguments.
    @param: None.
    @returns: None. """
    def solveHitoriPuzzle(self):
        print(">>>>>>Begin solveHitoriPuzzle Routine<<<<<")
        dataFile = "userInput.lp"
        logicFile = "logic.lp"
        outFile = "hitoriOut.txt"
        
        # make system call to clingo and pass arguments
        retVal = os.system("clingo "+dataFile+" "+logicFile+" | mkatoms > " +outFile)
        
        print("Return value: "+str(retVal))
        #self.displayOutput(outFile)
        listBLK=self.getBlackCells(outFile)
        

        # display error message if there is no answer
        if (len(listBLK) == 0):
            errDialog=QtWidgets.QErrorMessage()
            errDialog.showMessage("No Solution Found!")
            errDialog.show()
            errDialog.exec_()
            print("No Solution Found!")
        else:
            self.blackOutGrid(listBLK)
        
        print(">>>>>>End solveHitoriPuzzle Routine<<<<<")

    """@desc: The method takes a list of black cells and goes through it to change the cell color to indicate where they are in the grid
    @param: a list of black cells.
    @returns: None. """
    def blackOutGrid(self,listBLK):
        print(">>>>>>Begin blackOutGrid Routine<<<<<")
        
        if (len(listBLK) > 0):
            for item in listBLK:
                self.cell2D[int(item.row)][int(item.col)].setStyleSheet("""QLineEdit { background-color: gray; color: white }""")
        else:
            print("Error: Empty list. No black cells.")
            logging.debug("Error: Empty list. No black cells.")
        

        print(">>>>>>End blackOutGrid Routine<<<<<")

    # for debugging
    def displayOutput(self, target):
        
        with open(target, "r") as file:
            for line in file:
                if(line[0] != ':'):
                    print(line)
    
    """ @desc: The method parses lines from target file generated by piping the output of clingo to mkatoms to get the answer set for blacked out cells.
    It takes the coordinates for rows and cols from the parsed lines and builds a list of blacks cells and returns it.
    @param: file containing a list of black cells.
    @returns: a list of black cells.
    """
    def getBlackCells(self,target):
        black = namedtuple('BlackCell', ['row', 'col'])
        listBLK = []

        with open(target, "r") as file:
            for line in file:
                if(line[0] != ':' and line[0] != '*'):
                    listBLK.append(black(line[6],line[8]))
                

        print(listBLK)
        return listBLK
        
        
    
        
# main method
def main():
    print("===============Begin Main Routine=============")
    logging.debug("Program Started..")

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    mainWind = MainWindow()
    mainWind.show()
    logging.debug("Program Terminated..")

    print("===============End Main Routine=============")

    sys.exit(app.exec_())


if __name__=='__main__':
    main()