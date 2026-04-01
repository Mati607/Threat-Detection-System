# 🛡️ Decentralized Intrusion Detection

<div align="center">

![Privacy-Preserving ML](https://img.shields.io/badge/Privacy--Preserving-ML-blue?style=for-the-badge&logo=shield)
![PyTorch](https://img.shields.io/badge/PyTorch-2.5.0-red?style=for-the-badge&logo=pytorch)
![Federated Learning](https://img.shields.io/badge/Federated-Learning-green?style=for-the-badge&logo=network)
![Graph Neural Networks](https://img.shields.io/badge/Graph-Neural%20Networks-purple?style=for-badge&logo=graph)

**A cutting-edge machine learning system for intrusion detection that balances security effectiveness with privacy preservation**

[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat&logo=python)](https://python.org)
[![Jupyter](https://img.shields.io/badge/Jupyter-Lab-orange?style=flat&logo=jupyter)](https://jupyter.org)
[![DARPA](https://img.shields.io/badge/DARPA-Datasets-red?style=flat)](https://www.darpa.mil)

</div>

---

## 🌟 Overview

This system implements state-of-the-art approaches to intrusion detection that balance security effectiveness with privacy preservation. It analyzes system logs and network activity while minimizing exposure of sensitive information using advanced techniques like federated learning, differential privacy, and cryptographic approaches.

### ✨ Key Features

- 🛡️ **Privacy-by-Design**: Integrates privacy-preserving techniques without sacrificing utility
- ⚙️ **End-to-End System**: Complete pipeline from raw data parsing to evaluation and reporting
- 🧩 **Modular Architecture**: Plug-and-play components for feature extraction and models
- 🔁 **Reproducible Research**: Deterministic pipelines with pre-trained weights
- 🗂️ **Multi-Dataset Support**: Evaluated across multiple DARPA datasets and scenarios
- 🚀 **Production Ready**: Docker containerization and scalable infrastructure
- 📊 **Comprehensive Evaluation**: Standardized metrics and experiment tracking

### 🔄 System Flow

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data          │    │   Feature       │    │   Model         │
│   Ingestion     │    │   Engineering   │    │   Training      │
│   & Parsing     │    │   & Privacy     │    │   & Inference   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Evaluation    │
                    │   & Reporting   │
                    └─────────────────┘
```

In the training phase, the system builds local provenance graphs for each client and trains an ensemble of GNN models. Prior to this, Word2vec models are harmonized in a privacy-preserving manner using encryption and dual-server architecture for semantic encoding. The local GNN models participate in federated learning to develop a global model, which is then utilized for anomaly detection.

## 🛠️ Tech Stack

### 🧠 Core ML/AI Frameworks
- **PyTorch 2.5.0** - Deep learning framework with CUDA support
- **PyTorch Geometric 2.6.1** - Graph neural networks (GCN, SAGE, GAT)
- **Gensim 4.3.0** - Word2Vec, Doc2Vec embeddings
- **scikit-learn 1.1.1** - Traditional ML algorithms and preprocessing
- **XGBoost 0.90** - Gradient boosting for classification

### 🔒 Privacy & Security
- **Cryptography (Fernet)** - Symmetric encryption for model privacy
- **Differential Privacy** - Mathematical privacy guarantees
- **Federated Learning** - Distributed training without data sharing
- **Dual-Server Architecture** - Secure multi-party computation

### 🧪 Advanced ML Techniques
- **Graph Neural Networks** - SAGEConv, GATConv for graph-structured data
- **Word Embeddings** - Cryptographic Word2Vec with privacy preservation
- **Graph2Vec** - Graph representation learning
- **Weisfeiler-Lehman Hashing** - Graph isomorphism testing
- **Procrustes Analysis** - Embedding alignment and harmonization

### 📊 Data Processing & Analysis
- **Pandas 1.3.5** - Data manipulation and analysis
- **NumPy 1.23.1** - Numerical computing
- **SciPy 1.9.3** - Scientific computing
- **NetworkX 3.0** - Graph analysis and algorithms
- **Matplotlib** - Data visualization and plotting

### 🏗️ Data Engineering & Infrastructure
- **Docker** - Containerization and deployment
- **Jupyter Lab** - Interactive development environment
- **Elasticsearch** - Search and analytics engine
- **JSON/JSONL** - Data serialization and storage
- **Regular Expressions** - Pattern matching and data extraction

### ⚡ Performance & Optimization
- **Joblib** - Parallel processing and caching
- **Multiprocessing** - CPU parallelization
- **Concurrent.futures** - Asynchronous execution
- **xxHash** - Fast hashing algorithms
- **tqdm** - Progress tracking and monitoring

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Jupyter Lab environment
- CUDA-compatible GPU (recommended for optimal performance)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/privacy-preserving-intrusion-detection.git
   cd privacy-preserving-intrusion-detection
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch Jupyter Lab**
   ```bash
   jupyter lab
   ```

4. **Run evaluation notebooks**
   - Open a notebook under `system/` (e.g., `DARPA_E3.ipynb`, `DARPA_E5_CADETS.ipynb`)
   - Review the parameters section to configure components
   - Run all cells to see results

### 🎯 Quick Demo

```bash
# Start with a simple evaluation
jupyter lab system/DARPA_E3.ipynb

# Or run the Docker setup
chmod +x docker_setup.sh
./docker_setup.sh
```

## ⚙️ Configuration

Each notebook exposes a parameters cell to configure:

- **📁 Dataset Settings**: Paths and sampling configurations
- **🔧 Feature Extractors**: Choice between word2vec, graph2vec, or cryptographic word2vec
- **🤖 Model Options**: Centralized vs federated training, differential privacy settings
- **📊 Evaluation Metrics**: Customizable metrics and output paths
- **🧰 Pre-trained Weights**: Available under `Utils/weights/` for quick benchmarking

## 🗂️ Supported Datasets

This project is evaluated on open-source datasets from DARPA and the research community.

| Dataset | Description | Access | Size |
|---------|-------------|--------|------|
| **DARPA OpTC** | Operational Technology Cybersecurity dataset | [GitHub](https://github.com/FiveDirections/OpTC-data) | ~50GB |
| **DARPA E3** | Enterprise Email Exfiltration dataset | [Google Drive](https://drive.google.com/drive/folders/1fOCY3ERsEmXmvDekG-LUUSjfWs6TRdp) | ~20GB |
| **DARPA E5** | Multi-scenario email exfiltration dataset | [Google Drive](https://drive.google.com/drive/folders/1okt4AYElyBohW4XiOBqmsvjwXsnUjLVf) | ~30GB |

### 📊 Dataset Features

- **🔍 Real-world Scenarios**: Authentic attack patterns and system behaviors
- **📈 Multi-modal Data**: System logs, network traffic, and user activities
- **🏷️ Ground Truth Labels**: Expert-annotated attack classifications
- **⚖️ Balanced Classes**: Representative samples of normal and malicious activities

## 📁 Project Structure

```
privacy-preserving-intrusion-detection/
├── 📁 system/                     # Main evaluation notebooks
│   ├── 📄 DARPA_E3.ipynb         # E3 dataset evaluation
│   ├── 📄 DARPA_E5_CADETS.ipynb  # E5 CADETS scenario
│   ├── 📄 DARPA_E5_CLEARSCOPE.ipynb # E5 CLEARSCOPE scenario
│   ├── 📄 DARPA_E5_THEIA.ipynb   # E5 THEIA scenario
│   ├── 📄 DARPA_OPTC.ipynb       # OpTC dataset evaluation
│   └── 📄 Ablation_Studies_Modules.ipynb # Modular components
├── 📁 Utils/                      # Utilities and tools
│   ├── 📄 graph2vec.py           # Graph representation learning
│   ├── 📄 cryptographic_word2vec.ipynb # Privacy-preserving embeddings
│   ├── 📄 combine_word2vecs.ipynb # Embedding harmonization
│   ├── 📄 privacy_analysis.ipynb # Privacy metrics and analysis
│   ├── 📁 artifacts/             # Generated artifacts
│   └── 📁 weights/               # Pre-trained model weights
├── 📄 docker_setup.sh            # Docker environment setup
├── 📄 requirements.txt           # Python dependencies
├── 📄 architecture.png           # System architecture diagram
└── 📄 README.md                  # This file
```

### 🧪 Evaluation Scripts
- **Location**: `system/` directory
- **Purpose**: Dedicated Jupyter notebooks for each dataset evaluation
- **Features**: 
  - Integrated data parsers for each dataset
  - Automated downloading, parsing, and evaluation pipelines
  - Pre-trained model weights for immediate evaluation
  - Configurable parameters for different system components

### 🔬 Ablation Studies
- **File**: `Ablation_Studies_Modules.ipynb`
- **Purpose**: Modular components for conducting ablation studies
- **Features**: Plug-and-play components that can be combined with base evaluation scripts

### 🧰 Utilities
- **Location**: `Utils/` directory
- **Contents**: 
  - Cryptographic word2vec implementations
  - Graph2vec utilities
  - Privacy analysis tools
  - Pre-trained model weights and artifacts

## 📊 Reproducibility & Results

### 🔬 Research Standards
- **🎲 Deterministic Seeds**: Set within notebooks for reproducible results
- **🧰 Pre-trained Weights**: Available for quick validation and benchmarking
- **📈 Standardized Metrics**: Consistent evaluation across all datasets
- **📋 Detailed Results**: Comprehensive metrics at the end of each notebook

### 📝 Important Notes
- **📦 Large Datasets**: Hosted externally; see dataset links above for access
- **🔧 Path Configuration**: Some notebooks may require local dataset path updates
- **⚡ GPU Recommended**: CUDA support for optimal performance

## 🚀 Deployment

### Docker Setup
```bash
# Quick start with Docker
chmod +x docker_setup.sh
./docker_setup.sh
```

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Launch Jupyter Lab
jupyter lab

# Run specific evaluation
jupyter lab system/DARPA_E3.ipynb
```



---


