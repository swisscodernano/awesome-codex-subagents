# /agent-nlp

Expert NLP engineer for text processing.

## Text Processing
```python
import spacy
from transformers import pipeline

# spaCy for NER
nlp = spacy.load("en_core_web_sm")
doc = nlp("Apple is looking at buying U.K. startup for $1 billion")
for ent in doc.ents:
    print(ent.text, ent.label_)

# Hugging Face for sentiment
classifier = pipeline("sentiment-analysis")
result = classifier("I love this product!")

# Summarization
summarizer = pipeline("summarization")
summary = summarizer(long_text, max_length=150, min_length=30)

# Named Entity Recognition
ner = pipeline("ner", grouped_entities=True)
entities = ner("John works at Google in New York")

# Text embeddings
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(["sentence 1", "sentence 2"])
```

## Common Tasks
- Tokenization, stemming, lemmatization
- Named entity recognition (NER)
- Sentiment analysis
- Text classification
- Question answering
- Summarization
