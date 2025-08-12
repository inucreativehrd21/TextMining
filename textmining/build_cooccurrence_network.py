
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
from itertools import combinations
import community
import matplotlib.font_manager as fm

def build_cooccurrence_network(words, window_size=5, min_edge_weight=2):
    G = nx.Graph()
    for word in set(words):
        G.add_node(word)
    for i in range(len(words) - window_size + 1):
        window = words[i:i + window_size]
        for w1, w2 in combinations(set(window), 2):
            if G.has_edge(w1, w2):
                G[w1][w2]['weight'] += 1
            else:
                G.add_edge(w1, w2, weight=1)
    # 가중치 적은 간선 제거
    edges_to_remove = [(u, v) for u, v, d in G.edges(data=True) if d['weight'] < min_edge_weight]
    G.remove_edges_from(edges_to_remove)
    return G

def draw_cooccurrence_network(G, title="키워드 공동출현 네트워크", font_path=None):
    plt.figure(figsize=(15, 15))
    # 한글 폰트 설정
    if font_path:
        font_prop = fm.FontProperties(fname=font_path)
    else:
        font_prop = None

    # 커뮤니티 탐지 (Louvain)
    partition = community.best_partition(G)
    
    # 노드 컬러 맵 생성
    communities = set(partition.values())
    colors = plt.cm.tab20.colors  # 최대 20개 색상
    color_map = {com: colors[i % len(colors)] for i, com in enumerate(communities)}
    node_colors = [color_map[partition[node]] for node in G.nodes()]

    # 레이아웃 (Kamada-Kawai)
    pos = nx.kamada_kawai_layout(G)

    # 노드 크기: 연결 수에 비례 (최솟값 설정)
    degrees = dict(G.degree())
    node_sizes = [max(100, degrees[node] * 200) for node in G.nodes()]

    # 간선 두께 및 투명도 - 가중치에 비례
    weights = [G[u][v]['weight'] for u, v in G.edges()]
    max_weight = max(weights) if weights else 1
    edge_widths = [2 * (w / max_weight) for w in weights]
    edge_alphas = [0.6 * (w / max_weight) + 0.4 for w in weights]

    # 간선 그리기 (투명도 개별 적용 위해 반복)
    ax = plt.gca()
    for (u, v), w, alpha, width in zip(G.edges(), weights, edge_alphas, edge_widths):
        ax.plot(
            [pos[u][0], pos[v][0]],
            [pos[u][1], pos[v][1]],
            color='gray', alpha=alpha, linewidth=width
        )

    # 노드 그리기
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.9)

    # 레이블 표시 (노드 수가 많으면 일부만 표시하는 옵션 고려 가능)
    nx.draw_networkx_labels(G, pos, font_properties=font_prop, font_size=12)

    plt.title(title, fontsize=20)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

# 사용
keywords = [
    'keyword', 'keyword1'
]

G = build_cooccurrence_network(keywords, window_size=5, min_edge_weight=2)

# 윈도우 환경 한글 폰트
font_path = "c:/Windows/Fonts/malgun.ttf"

draw_cooccurrence_network(G, font_path=font_path)
