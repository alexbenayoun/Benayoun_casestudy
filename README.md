# Benayoun_casestudy
## Introduction

The file *Benayoun_approach.pdf* is detailing the data analysis and the chosen approach for this case study.

## Prerequisites

Python 3.6 or later version.  

Python Libraries:  
pickle  
json  
numpy  

Install the dependencies using:
`pip install numpy`

## How to Use

Clone this GitHub repository to your local machine.

Ensure the models (*modele1.pkl* and *modele2.pkl*) are present in the project folder.

Run the main script using: `python main_Benayoun.py`

The program will ask you how many game you want to generate and will also prompt you to provide a file path for each match.  
When asked, provide the path to the JSON file containing the input data.  
Predictions are printed and saved as separate JSON files, named *generated_match_1.json*, *generated_match_2.json*, etc.

## Data Structure

Input data should be in the form of nested lists of dictionaries where each dictionary represents the acceleration norm and possibly the label associated with each gait. The label is not mandatory in the dictionary. The program is making predictions based solely on the norms.
