import requests
import xml.etree.ElementTree as ET
import csv
import argparse

# PubMed API base URL
PUBMED_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

# Function to fetch PubMed article IDs based on user query
def fetch_pubmed_ids(query):
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "xml",
        "retmax": 20  # Adjust as needed
    }
    response = requests.get(PUBMED_API_URL, params=params)
    if response.status_code != 200:
        print("Error fetching data from PubMed")
        return []
    
    root = ET.fromstring(response.text)
    return [id_elem.text for id_elem in root.findall(".//Id")]

# Function to fetch article details from PubMed
def fetch_article_details(article_ids):
    if not article_ids:
        return []
    
    params = {
        "db": "pubmed",
        "id": ",".join(article_ids),
        "retmode": "xml"
    }
    response = requests.get(PUBMED_FETCH_URL, params=params)
    
    if response.status_code != 200:
        print("Error fetching article details from PubMed")
        return []
    
    return ET.fromstring(response.text)

# Function to extract relevant data from XML response
def extract_research_papers(xml_data, debug=False):
    papers = []
    
    for article in xml_data.findall(".//PubmedArticle"):
        paper_id = article.find(".//PMID").text
        title_elem = article.find(".//ArticleTitle")
        title = title_elem.text if title_elem is not None else "N/A"
        date_elem = article.find(".//PubDate/Year")
        date = date_elem.text if date_elem is not None else "N/A"

        authors_data = []
        for author in article.findall(".//Author"):
            last_name = author.find("LastName")
            fore_name = author.find("ForeName")
            email_elem = author.find("AffiliationInfo/Affiliation")
            affiliation = email_elem.text if email_elem is not None else "N/A"
            
            if affiliation and ("pharmaceutical" in affiliation.lower() or "biotech" in affiliation.lower()):
                authors_data.append({
                    "Name": f"{fore_name.text if fore_name is not None else ''} {last_name.text if last_name is not None else ''}".strip(),
                    "Affiliation": affiliation,
                    "Email": email_elem.text if email_elem is not None else "N/A"
                })
        
        if authors_data:
            papers.append({
                "Paper ID": paper_id,
                "Title": title,
                "Publication Date": date,
                "Authors": ", ".join([author["Name"] for author in authors_data]),
                "Pharma/Biotech Company": ", ".join(set([author["Affiliation"] for author in authors_data])),
                "Author Emails": ", ".join([author["Email"] for author in authors_data])
            })
    
    if debug:
        print(f"Extracted {len(papers)} papers with pharmaceutical/biotech affiliations")
    
    return papers

# Function to save results to CSV
def save_to_csv(papers, filename="research_papers.csv"):
    if not papers:
        print("No relevant research papers found.")
        return
    
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=papers[0].keys())
        writer.writeheader()
        writer.writerows(papers)
    
    print(f"Results saved to {filename}")

# Command-line argument parsing
def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed based on a query and filter by pharmaceutical/biotech author affiliations.")
    parser.add_argument("query", help="Search query for fetching research papers")
    parser.add_argument("--debug", action="store_true", help="Print debug information during execution")
    parser.add_argument("--file", type=str, default="research_papers.csv", help="Specify the filename to save the results")
    
    args = parser.parse_args()
    
    if args.debug:
        print(f"Fetching papers for query: {args.query}")
    
    article_ids = fetch_pubmed_ids(args.query)
    xml_data = fetch_article_details(article_ids)
    papers = extract_research_papers(xml_data, args.debug)
    save_to_csv(papers, args.file)

if __name__ == "__main__":
    main()
