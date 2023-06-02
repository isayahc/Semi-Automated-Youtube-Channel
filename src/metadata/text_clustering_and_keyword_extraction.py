from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# Assume descriptions contains the text data of the video descriptions
descriptions = ["Python tutorial", "How to bake a cake", "Machine learning basics", "..."]

# Number of clusters
num_clusters = 3

# Vectorize the descriptions using TF-IDF
vectorizer = TfidfVectorizer(max_features=10000)
tfidf = vectorizer.fit_transform(descriptions)

# Perform KMeans clustering
kmeans = KMeans(n_clusters=num_clusters)
kmeans.fit(tfidf)

# For each cluster, print the top keywords
for i in range(num_clusters):
    print(f"Niche #{i + 1}:")
    
    # Get the descriptions in this cluster
    cluster_descriptions = tfidf[kmeans.labels_ == i]
    
    # Sum the TF-IDF scores for each keyword
    sum_tfidf = cluster_descriptions.sum(axis=0)

    # Get the top 10 keywords in this cluster
    top_keywords_indices = sum_tfidf.argsort()[0, ::-1][:10]
    top_keywords = [vectorizer.get_feature_names_out()[index] for index in top_keywords_indices.flat]
    
    print(top_keywords)
