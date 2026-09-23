from sklearn.cluster import KMeans

def cluster_documents(embeddings_array, metadata_list, num_clusters=3):
    if len(embeddings_array) < num_clusters:
        return [{"cluster": 0, "metadata": m} for m in metadata_list]
        
    kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init='auto')
    labels = kmeans.fit_predict(embeddings_array)
    
    results = []
    for i, label in enumerate(labels):
        results.append({
            "cluster": int(label),
            "metadata": metadata_list[i]
        })
        
    return results

def group_papers_by_cluster(doc_clusters):
    clusters_map = {}
    for item in doc_clusters:
        c_id = item["cluster"]
        if c_id not in clusters_map:
            clusters_map[c_id] = []
        clusters_map[c_id].append(item["metadata"])
        
    return clusters_map
