import xml.etree.ElementTree as ET
from defusedxml.ElementTree import fromstring as safe_fromstring


        
def  parse_paper_data(xml_data):
        try:
            root = safe_fromstring(xml_data)
        except ET.ParseError as e:
            print(f"XML Parse Error: {e}")
            raise
        
        papers = []
        
        COMPANY_KEYWORDS = ["Pharma", "Biotech", "Inc.", "Ltd.", "Corp.", "LLC", "Laboratories"]


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

            if company_authors:  
                papers.append({
                    "PubMed ID": pmid,
                    "Title": title,
                    "Publication Date": pub_date,
                    "Authors": ", ".join(authors),
                    "Company Authors": ", ".join(company_authors),
                    "Company Affiliations": "; ".join(company_affiliations)
                })

        return papers
