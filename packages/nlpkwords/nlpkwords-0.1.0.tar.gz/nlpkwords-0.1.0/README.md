# NLPKWords

A Python package containing implementations of various AI/ML algorithms and NLP techniques for educational purposes.

## Features

- **NLP Processing**
  - Tokenization
  - Lemmatization
  - Bag of Words
  - TF-IDF
  - One-Hot Encoding

- **Neural Networks**
  - Sigmoid Activation
  - ReLU Activation
  - Tanh Activation
  - Simple MLP Implementation

- **Graph Algorithms**
  - BFS (Breadth-First Search)
  - DFS (Depth-First Search)
  - A* Search Algorithm
  - Best-First Search

- **Fuzzy Logic**
  - Fuzzy Set Operations
  - Complement Operations
  - Union and Intersection

- **Game Theory**
  - Nim Game Implementation

## Installation

```bash
pip install nlpkwords
```

## Usage

### NLP Processing
```python
from nlpkwords import tokenization, lemmatization

# Tokenization
tokens = tokenization.tokenize("Your text here")

# Lemmatization
lemmas = lemmatization.lemmatize("Your text here")
```

### Neural Networks
```python
from nlpkwords import sigmoid, relu, tanh

# Using different activation functions
output = sigmoid.forward(input_data)
output = relu.forward(input_data)
output = tanh.forward(input_data)
```

### Graph Algorithms
```python
from nlpkwords import bfs, dfs_recursive

# BFS Traversal
bfs.traverse(graph, start_node)

# DFS Traversal
dfs_recursive.traverse(graph, start_node)
```

## Requirements

- Python >= 3.6
- pandas >= 1.3.0
- nltk >= 3.6.0
- textblob >= 0.15.3
- scikit-learn >= 0.24.0
- numpy >= 1.20.0

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Rish Dias - rishrdias672004@gmail.com

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 