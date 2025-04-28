# AI Data SDK by Zeebee

A comprehensive SDK for standardizing, processing, embedding, and retrieving data for AI applications.

## Features

- Data ingestion from various sources
- Data validation and quality checks
- Metadata management for AI data
- Text embedding generation
- PII detection and masking
- Vector database connectors
- Drift detection and user feedback

## Installation

```bash
pip install ai-data-sdk-zeebee
```

## Usage

```python
from ai_data_sdk import ingestion, embedding, vector_db

# Ingest data
data = ingestion.load_from_json("data.json")

# Generate embeddings
embeddings = embedding.create_embeddings(data)

# Store in vector DB
vector_db.store_vectors(embeddings)
```

## Documentation

For full documentation, visit [https://ai-data-sdk.readthedocs.io/](https://ai-data-sdk.readthedocs.io/)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
