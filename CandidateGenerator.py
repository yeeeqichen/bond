import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from Config import config


# 返回候选集，若相似度大于一定阈值，直接给出链接结果
def get_candidates(mention_embedding, kind_idx):
    # 在对应债券种类集合中选取相似度top k
    if kind_idx == -1 or len(config.bond_clusters[kind_idx]) == 0:
        sim_matrix = cosine_similarity(mention_embedding, config.full_embeddings)
        top_k = min(config.top_k, len(sim_matrix[0]))
        top_n = []
        temp_idx = np.argpartition(sim_matrix[0], -top_k)[-top_k:]
        for idx in temp_idx:
            top_n.append((idx, sim_matrix[0][idx]))
    else:
        sim_matrix = cosine_similarity(mention_embedding, config.bond_clusters[kind_idx])
        top_k = min(config.top_k, len(sim_matrix[0]))
        temp_idx = np.argpartition(sim_matrix[0], -top_k)[-top_k:]
        # 转化为债券名库(去除了英文债券)中的索引,原索引是在sim_matrix中的索引，即对应cluster内的索引
        top_n = []
        for idx in temp_idx:
            top_n.append((config.cluster_to_id[kind_idx][idx], sim_matrix[0][idx]))
        # 返回索引以及对应的相似度得分
    return top_n



