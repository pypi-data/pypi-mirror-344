# AI Data SDK by Zeebee

A comprehensive SDK for standardizing, processing, embedding, and retrieving data for AI applications.

## Features

- Text embedding generation
- Semantic search with filtering and hybrid search
- PII detection and masking
- User feedback submission
- IP allowlist management (admin only)

## Installation

```bash
pip install ai-data-sdk-zeebee==0.1.2
```

## Usage

### Initialize Client

```python
from ai_data_sdk import AIDataClient

# Initialize with your API key
client = AIDataClient(api_key="your_api_key_here")
```

### Generate Embeddings

```python
# Generate embeddings for a list of texts
texts = [
    "AI Data SDK helps standardize data for AI applications.",
    "The embedding module converts text into vector representations."
]

result = client.create_embeddings(texts)
```

### Search for Similar Documents

```python
# Basic search
search_result = client.search(query_text="How do machines learn from data?")

# Advanced search with filters
filters = {
    "category": "technology",
    "rating": {"$gt": 4.5}
}

search_result = client.search(
    query_text="neural networks",
    filters=filters,
    hybrid_search_text="deep learning",
    hybrid_alpha=0.3
)
```

### Detect and Mask PII

```python
# Basic PII detection
text = "My email is john.doe@example.com and my phone is 555-123-4567."
result = client.detect_pii(text, pii_types=["email", "phone"], mask=True)

# Advanced anonymization
result = client.detect_pii(
    text,
    advanced_anonymize=True,
    consistent_replacements=True
)
```

### Submit Feedback

```python
feedback = client.submit_feedback(
    query_id="q_12345",
    result_id="doc_1",
    rating=4,
    comments="Very relevant result, but missing some details."
)
```

## Error Handling

```python
from ai_data_sdk import APIError, AuthenticationError, InvalidRequestError, RateLimitError

try:
    result = client.create_embeddings(texts)
except AuthenticationError:
    print("Authentication failed. Check your API key.")
except InvalidRequestError as e:
    print(f"Invalid request: {e}")
except RateLimitError:
    print("Rate limit exceeded. Please try again later.")
except APIError as e:
    print(f"API error: {e}")
```

## Documentation

For full documentation, visit [https://ai-data-sdk.readthedocs.io/](https://ai-data-sdk.readthedocs.io/)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
