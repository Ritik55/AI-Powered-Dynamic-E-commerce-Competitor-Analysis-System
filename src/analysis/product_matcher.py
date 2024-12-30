from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ProductMatcher:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def match_products(self, product_list):
        titles = [product['title'] for product in product_list]
        tfidf_matrix = self.vectorizer.fit_transform(titles)
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
        
        matches = []
        for i, product in enumerate(product_list):
            similar_indices = cosine_sim[i].argsort()[:-5:-1]
            similar_items = [
                {
                    "title": product_list[idx]['title'],
                    "platform": product_list[idx]['platform'],
                    "similarity": cosine_sim[i][idx]
                }
                for idx in similar_indices if idx != i
            ]
            matches.append({
                "product": product,
                "matches": similar_items
            })
        
        return matches
