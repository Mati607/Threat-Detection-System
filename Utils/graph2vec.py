from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
import networkx as nx
import hashlib
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from joblib import Parallel, delayed

# Function to hash a feature vector to a string
def hash_vector(vector):
    return hashlib.sha256(str(vector).encode()).hexdigest()

# Function for one round of Weisfeiler-Lehman hashing (feature update)
def wl_hash_with_features(graph, feature_vectors):
    new_feature_vectors = {}
    for node in graph.nodes():
        neighbors = list(graph.neighbors(node))
        neighbor_vectors = [feature_vectors[neighbor] for neighbor in neighbors]
        aggregated_vectors = np.sum(neighbor_vectors, axis=0) if neighbor_vectors else np.zeros_like(feature_vectors[node])
        concatenated_vectors = np.concatenate([feature_vectors[node], aggregated_vectors])
        new_feature_vectors[node] = concatenated_vectors
    return new_feature_vectors

# Function to prepare 'documents' for Doc2Vec
def prepare_documents(graph):
    feature_vectors = {}
    for node in graph.nodes():
        degree = graph.degree(node)
        color = graph.nodes[node]['color']
        feature_vector = np.array([degree, color], dtype=np.float32)
        feature_vectors[node] = feature_vector
    for iteration in range(3):
        feature_vectors = wl_hash_with_features(graph, feature_vectors)
    features = {node: hash_vector(vec) for node, vec in feature_vectors.items()}
    document = list(features.values())
    return document

# Create example graphs with node attributes (color: 1 or 2)
G1 = nx.cycle_graph(5)
nx.set_node_attributes(G1, {0: 1, 1: 2, 2: 1, 3: 2, 4: 1}, 'color')
G2 = nx.path_graph(5)
nx.set_node_attributes(G2, {0: 1, 1: 1, 2: 2, 3: 2, 4: 1}, 'color')

graphs = [G1, G2]

# Prepare data for Doc2Vec in parallel for optimization
documents = Parallel(n_jobs=-1)(delayed(prepare_documents)(graph) for graph in graphs)

# Add tags to documents
documents = [TaggedDocument(words=doc, tags=[str(i)]) for i, doc in enumerate(documents)]

# Train Doc2Vec model
model = Doc2Vec(documents, vector_size=5, window=2, min_count=1, workers=4, epochs=100)

# Extract graph embeddings
embeddings = np.array([model.dv[str(i)] for i in range(len(graphs))])

# Visualize using PCA
pca = PCA(n_components=2)
embeddings_2d = pca.fit_transform(embeddings)
plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1])
for i, txt in enumerate(["G1", "G2"]):
    plt.annotate(txt, (embeddings_2d[i, 0], embeddings_2d[i, 1]))
plt.title('Graph Embeddings')
plt.show()
