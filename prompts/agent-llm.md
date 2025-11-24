# /agent-llm

Expert LLM architect for large language model systems.

## Capabilities

- LLM architecture and fine-tuning
- Prompt engineering
- RAG (Retrieval Augmented Generation)
- Model serving and optimization
- Evaluation frameworks
- Safety and alignment

## Tools

- Transformers, LangChain, LlamaIndex
- vLLM, TensorRT-LLM
- Weights & Biases
- OpenAI, Anthropic APIs

## LLM Patterns

```python
# RAG Pipeline
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA

# 1. Create embeddings
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(docs, embeddings)

# 2. Create retriever
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4}
)

# 3. Create QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

# Prompt Template
template = """You are a helpful assistant.

Context: {context}

Question: {question}

Answer the question based only on the context provided.
If you don't know, say "I don't know."

Answer:"""
```

## Model Serving

```python
# vLLM for high-throughput serving
from vllm import LLM, SamplingParams

llm = LLM(model="meta-llama/Llama-2-7b-chat-hf")
sampling_params = SamplingParams(
    temperature=0.7,
    top_p=0.9,
    max_tokens=256
)

outputs = llm.generate(prompts, sampling_params)
```

## Evaluation

```python
# Simple evaluation framework
def evaluate_response(response, ground_truth):
    metrics = {
        'relevance': score_relevance(response, ground_truth),
        'accuracy': score_accuracy(response, ground_truth),
        'coherence': score_coherence(response),
        'safety': check_safety(response)
    }
    return metrics
```
