import requests
# from PubMed.utils.common import load_config
# from PubMed.constants import BASE_URL
from PubMed.exceptions import PubMedAPIException
from PubMed.services.paper_processor import parse_paper_data


class PubMedService:
    def __init__(self):
        pass
       
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"


    def fetch_pubmed_articles(self, query: str, max_results: int = 10):
        """Fetch PubMed articles based on a search query."""
    
        try:
            params = {
                "db": "pubmed",
                "term": query,
                "retmode": "json",
                "retmax": max_results
            }
            response = requests.get(f"{self.BASE_URL}esearch.fcgi", params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("esearchresult", {}).get("idlist", [])
        except requests.RequestException as e:
            raise PubMedAPIException(f"Error fetching PubMed articles: {e}")

    def fetch_article_details(self, article_ids: list):
        """Fetch details of specific PubMed articles."""
        try:
            if not article_ids:
                return []
            
            response = requests.get(f"{self.BASE_URL}efetch.fcgi", params={"db": "pubmed", "id": ",".join(article_ids), "retmode": "xml"})
            response.raise_for_status()
            # processor=PaperProcessor()
            papers=parse_paper_data(response.content)
            return papers
            
        except requests.RequestException as e:
            raise PubMedAPIException(f"Error fetching PubMed article details: {e}")
