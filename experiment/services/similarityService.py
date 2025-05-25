from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine_similarity
from openai import OpenAI
from django.conf import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def cosine_similarity(text1, text2):
    if not isinstance(text1, str) or not isinstance(text2, str):
        return {"error": "Inputs must be strings"}, 400
    
    text1 = text1.strip()
    text2 = text2.strip()
    
    if not text1 or not text2:
        return {"error": "Texts cannot be empty"}, 400
    
    try:
        response = client.embeddings.create(
            input=[text1, text2],
            model="text-embedding-3-small"
        )
        emb1 = response.data[0].embedding
        emb2 = response.data[1].embedding
        
        similarity_score = sklearn_cosine_similarity([emb1], [emb2])[0][0]
        return {"similarity": round(float(similarity_score), 4)}, 200
    
    except Exception as e:
        return {"error": f"OpenAI API Error: {str(e)}"}, 500