from fastapi import APIRouter
from PubMed.controllers.pubmed_controller import PubMedController

router = APIRouter()
pubmed_controller = PubMedController()

    
@router.get("/pubmed")
def  get_filtered_articles(query: str, max_results: int = 10):
    """API endpoint to fetch and filter PubMed articles."""
    return  pubmed_controller.get_filtered_papers(query, max_results)
