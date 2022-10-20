# Binary-Search-Tree-Project
In this project, I worked to analyze a large dataset of every mortgage loan application from Wisconsin in 2020. 

Loans.py contains 3 classes. The Bank class allows the user to input a Wisconsin bank's name and looks up all loans within the large dataset that come from this bank and adds them to a list. The Loan class parses through the each loan to create attributes that allow the user to look up the number of applicants, interest rate, loan amount, etc. Finally the applicant class parses through the list of applicants within each loan and creates age and race attributes.

Search.py creates the binary search tree. It contains an add method which places nodes in the correct order (children on the left subtree are less than their parent, which are less than those in the right subtree). The nodes are keys, which allows the BST to behave like a dictionary, allowing you to look up values by a key. The add method takes a key and value parameter, allowing the user to create a tree with whatever information they need. In the example in the .ipynb file, I created a tree from loans from one bank, where the key was an interest rate and the values were all of the loans that had that interest rate.

The zip file contains the main project Jupyter notebook, the Loans and Search modules, and the test cases.

This was a class project, certain methods in the Search and Loans modules were outlined for us in our instructions.
