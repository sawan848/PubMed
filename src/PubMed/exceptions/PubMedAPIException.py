class PubMedAPIException(Exception):
    def __init__(self, message):
        super().__init__(f"PubMed API Error: {message}")
