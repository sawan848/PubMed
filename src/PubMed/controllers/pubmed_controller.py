from PubMed.services.pubmed_service import PubMedService
import pandas as pd
from PubMed.utils.common import save_to_csv

class PubMedController:
    def __init__(self):
        self.pubmed_service = PubMedService()

    def get_filtered_papers(self, query: str, max_results: int = 10):
        article_ids = self.pubmed_service.fetch_pubmed_articles(query, max_results)
        articles = self.pubmed_service.fetch_article_details(article_ids)
        df = pd.DataFrame(articles)
        save_to_csv(pd.DataFrame(articles))
        
        return df.to_dict()
