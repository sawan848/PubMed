import requests
import xml.etree.ElementTree as ET
import pandas as pd


PUBMED_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"


COMPANY_KEYWORDS = ["Pharma", "Biotech", "Inc.", "Ltd.", "Corp.", "LLC", "Laboratories"]

def fetch_pubmed_papers(query: str, max_results: int = 20):
    """Fetches PubMed paper IDs matching a search query."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json"
    }
    response = requests.get(PUBMED_SEARCH_URL, params=params)
    response.raise_for_status()
    data = response.json()

    return data.get("esearchresult", {}).get("idlist", [])



def fetch_paper_details(paper_ids):
    """Fetches paper details including author affiliations using EFetch."""
    if not paper_ids:
        return []

    params = {
        "db": "pubmed",
        "id": ",".join(paper_ids),
        "retmode": "xml"
    }

    response = requests.get(PUBMED_FETCH_URL, params=params)
    response.raise_for_status()

    root = ET.fromstring(response.content)
    papers = []
    
    for article in root.findall(".//PubmedArticle"):
        pmid = article.find(".//PMID").text
        title = article.find(".//ArticleTitle").text if article.find(".//ArticleTitle") is not None else "N/A"
        pub_date = article.find(".//PubDate/Year")
        pub_date = pub_date.text if pub_date is not None else "N/A"

        authors = []
        company_authors = []
        company_affiliations = []

        for author in article.findall(".//Author"):
            last_name = author.find("LastName")
            fore_name = author.find("ForeName")
            affiliation = author.find(".//Affiliation")

            author_name = f"{fore_name.text if fore_name is not None else ''} {last_name.text if last_name is not None else ''}".strip()
            authors.append(author_name)
            
            if affiliation is not None and any(keyword in affiliation.text for keyword in COMPANY_KEYWORDS):
                company_authors.append(author_name)
                company_affiliations.append(affiliation.text)

        if company_authors:  # Keep only papers with at least one company author
            papers.append({
                "PubMed ID": pmid,
                "Title": title,
                "Publication Date": pub_date,
                "Authors": ", ".join(authors),
                "Company Authors": ", ".join(company_authors),
                "Company Affiliations": "; ".join(company_affiliations)
            })

    return papers

def save_to_csv(papers, filename="filtered_papers.csv"):
    df = pd.DataFrame(papers)
    df.to_csv(filename, index=False)
    print(f"Saved {len(papers)} papers to {filename}")


if __name__=="__main__":
    query='Cancer treatment'
    paper_ids = fetch_pubmed_papers(query)
    if paper_ids:
        papers = fetch_paper_details(paper_ids)
        if papers:
            save_to_csv(papers)
        else:
            print("No papers found with company-affiliated authors.")
    else:
        print("No PubMed papers found for this query.")
