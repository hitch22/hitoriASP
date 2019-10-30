Author: Jaesub Shim  
Email:jashim@ttu.edu  
Date: 5 July, 2019  
Version: 0.1  
Requried: clingo, mkatoms, PyQt5  

Description: 

This program solves Hitori puzzle problem using Answer Set Programming concepts. It demonstrates "Generate and Test" paradigm. All possibilities with regards to the terms are grounded solid via the grounding process and the constraints are used for weeding out inconsistent stable models, thus leaving only the correct and consistant stable models to be used as the solution to the problem. Put simply, the Clingo solver tries to make all the terms true.

It uses PyQt5 for UI to let user input numbers, which along with ASP logic file, are passed onto the ASP solver through system call to get the puzzle solution to be displayed in the GUI. It requires dependencies, such as clingo, mkatoms, and PyQt5, and has been tested to work on Ubuntu Linux 14.04. The GUI is built using PyQt5 and styling used is "Fusion", which may or may not display correctly in other systems.

To sovle a Hitori puzzle with the program, supply numbers to the input boxes and click on the set button to finish input.
Then, click on solve button to solve the puzzle. Reset button can be used to clear the input box grid. 
The program will display a message box if no answer can be found.

The program will not work and display the error messages with no solutions if required dependencies are not met or not installed. The ASP business logic is in *.lp extension.

The following are the rules for the puzzle from https://www.conceptispuzzles.com/index.aspx?uri=puzzle/hitori/rules:

Each puzzle consists of a square grid with numbers appearing in all squares. The object is to shade squares so:

- No number appears in a row or column more than once.
- Shaded (black) squares do not touch each other vertically or horizontally.
- When completed, all un-shaded (white) squares create a single continuous area.


![Screenshot](screenshot.jpg)
