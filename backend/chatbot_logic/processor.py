class QueryProcessor:
    def process_query(self, query: str) -> str:
        # Preprocess the input query (e.g., cleaning, normalization)
        processed_query = query.strip().lower()
        return processed_query

    def get_source_link(self, response: str) -> str:
        # Retrieve the source document link for the generated response
        # This is a placeholder implementation; actual logic will depend on how responses are generated
        source_link = "https://example.com/source"  # Replace with actual logic to find the source
        return source_link