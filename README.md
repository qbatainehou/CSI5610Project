# CSI5610Project
This Python-based program processes JavaScript files from a local directory and performs the following tasks:
1. Reads each JavaScript file.
2. Uses two main functions:
   Generates the AST (Abstract Syntax Tree) of the code.
   Generates the CFG (Control Flow Graph) of the code.
3. Saves the AST and CFG outputs into text files in a specified local path.
4. Measures and records:
       Time complexity
       Space complexity
       Execution time for each file
5. Stores the performance metrics for all files in a CSV file.
6. Generates a final summary report that compiles all results into a clear table.

Quick Start:
1. Install Required Packages
Make sure you have Python installed. Then install the required packages by running:
pip install -r requirements.txt
2. update the pathes in the program to point to the folders on your machiene.
3.Run the Program
Execute the script to analyze JavaScript files:
python main.py


