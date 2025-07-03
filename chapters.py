import logging
from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def group_sentences(captions: List[Tuple[str, float]], group_size: int) -> List[Tuple[str, float]]:
    grouped_captions = []
    for i in range(0, len(captions), group_size):
        grouped_text = ' '.join(text for text, _ in captions[i:i+group_size])
        start_time = captions[i][1]
        grouped_captions.append((grouped_text, start_time))
    return grouped_captions

def split_into_chapters_by_topic(captions: List[Tuple[str, float]], group_size: int = 10, threshold: float = 0.1) -> List[List[Tuple[str, float]]]:
    if not captions:
        logging.warning("No captions provided for chapter segmentation.")
        return []
    grouped_captions = group_sentences(captions, group_size)
    vectorizer = TfidfVectorizer()
    texts = [text for text, _ in grouped_captions]
    X = vectorizer.fit_transform(texts)
    sim_matrix = cosine_similarity(X)
    breakpoints = [0]
    for i in range(1, len(sim_matrix)):
        if sim_matrix[i-1][i] < threshold:
            breakpoints.append(i)
    breakpoints.append(len(sim_matrix))
    chapters = [grouped_captions[breakpoints[i]:breakpoints[i+1]] for i in range(len(breakpoints)-1)]
    return chapters 