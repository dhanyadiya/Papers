# Papers
# Overview:

This script fetches research papers from the PubMed database based on a user-provided query. It extracts relevant details from the articles, including title, publication date, author names, affiliations, and emails (if available). The extracted data is filtered to include only authors affiliated with pharmaceutical or biotech companies. The final results are saved in a CSV file.

# Project Structure:

├── cs.py  # Main script
├── README.md                   # Documentation file
└── requirements.txt            # Dependencies file

Dependencies:

1. requests (for making API calls to PubMed)

2. xml.etree.ElementTree (for parsing XML responses)

3. csv (for saving extracted data to a CSV file)

4. argparse (for handling command-line arguments)

5. re (for extracting emails using regular expressions)

# Installation:

1. Clone the repository or download the script::
git clone <repository-url>
cd <repository-folder>
2. Install required dependencies:
pip install -r requirements.txt

# Execution:

1. To fetch research papers from PubMed, run the script with a search query:  python cs.py "Mathematics"
2. Optional Arguments:
    a. -h: Display usage instructions.
    b. --debug:Printdebug information during execution.
    c. --file:Specifythe filename to save the results. 
python research_paper_fetcher.py "COVID-19 vaccine" --debug --file output.csv


# Tools & Resources Used:

1. PubMed API: Used to fetch research paper metadata.
2. Python Libraries:
    a. requests
    b. xml.etree.ElementTree
    c. argparse
3. LLM Tools:
    a. Chatgpt
    b. Gemini

# Output:
1. The script outputs a CSV file:
   
    Paper ID,Title,Publication Date,Authors,Pharma/Biotech Company,Author Emails
    40071493,Boosting Non-Radiative Decay of Boron Difluoride Formazanate Dendrimers for NIR-II Photothermal Theranostics.,2025,Peng Chen,"Nanyang Technological University, School of Chemistry, Chemical         
    Engineering and Biotechnology, SINGAPORE.","Nanyang Technological University, School of Chemistry, Chemical Engineering and Biotechnology, SINGAPORE."
