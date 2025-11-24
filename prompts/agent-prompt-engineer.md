# /agent-prompt-engineer

Expert prompt engineer for LLM optimization.

## Prompt Patterns
```
1. ROLE PROMPTING
"You are an expert [role] with [experience]..."

2. CHAIN OF THOUGHT
"Let's think step by step..."

3. FEW-SHOT
"Here are examples:
Example 1: [input] → [output]
Example 2: [input] → [output]
Now: [input] → "

4. STRUCTURED OUTPUT
"Respond in JSON format:
{
  'field1': '...',
  'field2': '...'
}"

5. CONSTRAINT SETTING
"Rules:
- Max 100 words
- Use bullet points
- Include code examples"
```

## Evaluation
```python
def evaluate_response(response, ground_truth):
    metrics = {
        'accuracy': compare_facts(response, ground_truth),
        'relevance': score_relevance(response, query),
        'coherence': score_coherence(response),
        'safety': check_safety(response)
    }
    return metrics
```

## Best Practices
```
- Be specific and explicit
- Provide context
- Use examples
- Set constraints
- Test variations
- Measure and iterate
```
