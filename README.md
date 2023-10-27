# Saner_2024

## GBSR folder includes Datas, Matrix, PageRank, Calculation, and Result five folders. Due to the large experimental data, we only uploaded the relevant code and experimental data about Lang dataset for reference because the project size is too large.

## The Datas folder contains information about each version of Lang, including methods, statements, mutants, tests, and their specific information and associations. Lang_call.py performs a static analysis of all program code in Lang and gets the call relationships between program methods. Lang_call.py performs a static analysis of all program codes in Lang, and obtains the call relationship between program methods and stores it in the file Lang_M2M.txt. The call relationship in the file is shown in Lang1: Lang1 * [[0, []], [1, [0, 2]], [2, []]] means that method 1 calls method 0 and method 2 and no other method calls

## The matrix.py file in the Matrix folder integrates the obtained information to construct the graph and abstract the Matrix. The Passed and Failed tests are constructed separately in the construction process. Into Lang_fail_maxtrix and Lang_pass_matrix folders, respectively

## Pr_value_calculation.py in the PageRank folder calculates the PR value of each program entity as its importance based on the Matrix information and saves it into the PR_value folder.

## The programs in the Calculation folder are sus_calculate, which calculates the suspiciousness of program entities. py and evaluate.py for evaluating technical metrics for fault localization

## The Result file contains a result file that combines the experimental results and the MBFL_G experimental results folder combined with GBSR
