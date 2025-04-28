"""
Example usage for the AI Data SDK
"""

from .client import AIDataClient

def embedding_example(api_key: str, base_url: str = None) -> None:
    """
    Example of generating embeddings
    """
    client = AIDataClient(api_key, base_url)
    
    texts = [
        "AI Data SDK helps standardize data for AI applications.",
        "The embedding module converts text into vector representations."
    ]
    
    result = client.create_embeddings(texts)
    print(f"Generated {len(result['embeddings'])} embeddings")
    print(f"Model used: {result['model']}")
    print(f"Dimension: {result['dimension']}")
    
    # Just show the first 5 dimensions of the first embedding
    first_embedding_preview = [f"{x:.4f}" for x in result['embeddings'][0][:5]]
    print(f"First embedding (first 5 dimensions): {first_embedding_preview}...")


def search_example(api_key: str, base_url: str = None) -> None:
    """
    Example of semantic search
    """
    client = AIDataClient(api_key, base_url)
    
    # Basic search
    result = client.search(query_text="How do machines learn from data?", top_k=3)
    print(f"Found {result['count']} similar documents")
    
    for i, item in enumerate(result['results'], 1):
        print(f"{i}. {item['metadata'].get('title', 'Untitled')} (score: {item['score']:.2f})")
    
    # Advanced search with filters
    filters = {
        "category": "technology",
        "rating": {"$gt": 4.5}
    }
    
    result = client.search(
        query_text="neural networks",
        filters=filters,
        hybrid_search_text="deep learning",
        hybrid_alpha=0.3
    )
    
    print(f"\nAdvanced search found {result['count']} documents")
    for i, item in enumerate(result['results'], 1):
        print(f"{i}. {item['metadata'].get('title', 'Untitled')} (score: {item['score']:.2f})")


def pii_detection_example(api_key: str, base_url: str = None) -> None:
    """
    Example of PII detection and masking
    """
    client = AIDataClient(api_key, base_url)
    
    # Basic PII detection
    text = "My email is john.doe@example.com and my phone is 555-123-4567."
    result = client.detect_pii(text, pii_types=["email", "phone"], mask=True)
    
    print("Original text:", result['original_text'])
    print("Processed text:", result['processed_text'])
    print(f"PII instances found: {len(result['pii_instances'])}")
    
    # Advanced anonymization
    result = client.detect_pii(
        text,
        advanced_anonymize=True,
        consistent_replacements=True
    )
    
    print("\nAdvanced anonymization:")
    print("Processed text:", result['processed_text'])


def main() -> None:
    """
    Run all examples
    """
    # Replace with your API key
    api_key = "your_api_key_here"
    # Optional base URL if not using the default
    base_url = "https://api.example.com"
    
    print("=== Embedding Example ===")
    embedding_example(api_key, base_url)
    
    print("\n=== Search Example ===")
    search_example(api_key, base_url)
    
    print("\n=== PII Detection Example ===")
    pii_detection_example(api_key, base_url)


if __name__ == "__main__":
    main()
