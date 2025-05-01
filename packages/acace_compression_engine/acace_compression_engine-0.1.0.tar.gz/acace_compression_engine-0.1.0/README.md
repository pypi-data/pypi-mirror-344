# ACACE Compression Engine

A semantic text compression engine for the Adaptive Context-Aware Content Engine (ACACE).

## Features

- Token-based compression
- Semantic preservation
- Weight-based token filtering
- Configurable compression ratios

## Installation

```bash
pip install acace_compression_engine
```

## Usage

```python
from acace_compression_engine import compress_text
from acace_token_weightor import assign_weights
from acace_tokenizer import tokenize_text

# Prepare tokens with weights
tokens = tokenize_text("Your text to compress with important information.")
weighted_tokens = assign_weights(tokens)

# Compress text while preserving semantics
compressed_text = compress_text(weighted_tokens, compression_ratio=0.7)
print(compressed_text)
```

## License

MIT License 