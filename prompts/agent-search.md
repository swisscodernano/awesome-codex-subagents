# /agent-search

Expert search specialist for information retrieval.

## Elasticsearch Queries
```json
// Full-text search
{
  "query": {
    "bool": {
      "must": [
        { "match": { "title": "search query" } }
      ],
      "filter": [
        { "term": { "status": "published" } },
        { "range": { "date": { "gte": "2024-01-01" } } }
      ]
    }
  },
  "highlight": {
    "fields": { "content": {} }
  },
  "sort": [
    { "_score": "desc" },
    { "date": "desc" }
  ],
  "from": 0,
  "size": 10
}
```

## Vector Search
```python
# Semantic search with embeddings
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
query_embedding = model.encode("search query")

# Pinecone
results = index.query(
    vector=query_embedding.tolist(),
    top_k=10,
    include_metadata=True
)
```

## Search Best Practices
```
1. Use analyzers for text processing
2. Implement autocomplete with edge ngrams
3. Add synonyms for better recall
4. Use boosting for relevance tuning
5. Monitor query performance
6. A/B test ranking algorithms
```
