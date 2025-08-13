import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from collections import Counter
from itertools import combinations
import community
import numpy as np
from typing import Dict, List, Tuple
import json
import os
import logging
from TMconfig import AnalysisConfig

class EnhancedCooccurrenceNetwork:
    def __init__(self, config: AnalysisConfig):
        self.config = config
    
    def build_cooccurrence_network(self, words: List[str]) -> nx.Graph:
        """향상된 공동출현 네트워크 생성"""
        frequencies = Counter(words)
        G = nx.Graph()
        
        # 빈도가 낮은 단어 미리 제거
        filtered_words = [word for word in words if frequencies[word] >= self.config.min_word_freq]
        
        # 노드 추가
        for word in set(filtered_words):
            G.add_node(word, freq=frequencies[word])
        
        # 공동출현 계산 (최적화된 버전)
        edge_weights = {}
        for i in range(len(filtered_words) - self.config.window_size + 1):
            window = set(filtered_words[i:i + self.config.window_size])
            for w1, w2 in combinations(window, 2):
                if w1 != w2:
                    edge = tuple(sorted([w1, w2]))
                    edge_weights[edge] = edge_weights.get(edge, 0) + 1
        
        # 간선 추가
        for (w1, w2), weight in edge_weights.items():
            if weight >= self.config.min_edge_weight:
                G.add_edge(w1, w2, weight=weight)
        
        # 고립된 노드 제거
        isolated_nodes = [node for node in G.nodes() if G.degree(node) == 0]
        G.remove_nodes_from(isolated_nodes)
        
        logging.info(f"Network created: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
        return G
    
    def calculate_network_metrics(self, G: nx.Graph) -> Dict:
        """네트워크 분석 메트릭 계산"""
        if G.number_of_nodes() == 0:
            return {}
        
        metrics = {
            'nodes': G.number_of_nodes(),
            'edges': G.number_of_edges(),
            'density': nx.density(G),
            'avg_clustering': nx.average_clustering(G) if G.number_of_edges() > 0 else 0,
        }
        
        if G.number_of_edges() > 0 and G.number_of_nodes() > 1:
            try:
                metrics['centrality'] = {
                    'betweenness': nx.betweenness_centrality(G),
                    'closeness': nx.closeness_centrality(G),
                    'degree': nx.degree_centrality(G),
                    'eigenvector': nx.eigenvector_centrality(G, max_iter=1000)
                }
            except:
                logging.warning("Could not calculate all centrality measures")
                metrics['centrality'] = {
                    'degree': nx.degree_centrality(G)
                }
        
        return metrics
    
    def save_network_results(self, G: nx.Graph, metrics: Dict, output_dir: str):
        """네트워크 분석 결과 저장"""
        os.makedirs(output_dir, exist_ok=True)
        
        # 그래프 저장
        nx.write_gexf(G, os.path.join(output_dir, "network.gexf"))
        
        # 노드 정보 저장
        nodes_data = []
        for node in G.nodes(data=True):
            node_info = {'name': node[0], 'freq': node[1].get('freq', 0)}
            nodes_data.append(node_info)
        
        with open(os.path.join(output_dir, "nodes.json"), 'w', encoding='utf-8') as f:
            json.dump(nodes_data, f, ensure_ascii=False, indent=2)
        
        # 간선 정보 저장
        edges_data = []
        for edge in G.edges(data=True):
            edge_info = {'source': edge[0], 'target': edge[1], 'weight': edge[2].get('weight', 0)}
            edges_data.append(edge_info)
        
        with open(os.path.join(output_dir, "edges.json"), 'w', encoding='utf-8') as f:
            json.dump(edges_data, f, ensure_ascii=False, indent=2)
        
        # 메트릭 저장
        save_metrics = metrics.copy()
        if 'centrality' in save_metrics:
            centrality_dir = os.path.join(output_dir, "centrality")
            os.makedirs(centrality_dir, exist_ok=True)
            for cent_type, cent_values in save_metrics['centrality'].items():
                with open(os.path.join(centrality_dir, f"{cent_type}.json"), 'w', encoding='utf-8') as cf:
                    json.dump(cent_values, cf, ensure_ascii=False, indent=2)
            del save_metrics['centrality']
        
        with open(os.path.join(output_dir, "metrics.json"), 'w', encoding='utf-8') as f:
            json.dump(save_metrics, f, ensure_ascii=False, indent=2)
    
    def draw_enhanced_network(self, G: nx.Graph, metrics: Dict = None, 
                             title: str = "키워드 공동출현 네트워크", 
                             output_path: str = None):
        """향상된 네트워크 시각화"""
        
        if G.number_of_nodes() == 0:
            logging.warning("Empty network - nothing to visualize")
            return
        
        # 노드 수가 너무 많으면 제한
        if G.number_of_nodes() > self.config.max_nodes_display:
            # 빈도가 높은 노드들만 선택
            freqs = nx.get_node_attributes(G, 'freq')
            top_nodes = sorted(freqs.keys(), key=lambda x: freqs[x], reverse=True)[:self.config.max_nodes_display]
            G = G.subgraph(top_nodes).copy()
            logging.info(f"Network reduced to top {len(top_nodes)} nodes")
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=self.config.figure_size)
        
        font_prop = fm.FontProperties(fname=self.config.font_path) if os.path.exists(self.config.font_path) else None
        
        if G.number_of_edges() > 0 and G.number_of_nodes() > 1:
            try:
                partition = community.best_partition(G)
                pos = nx.spring_layout(G, k=1, iterations=50)
            except:
                partition = {node: 0 for node in G.nodes()}
                pos = nx.circular_layout(G)
            
            # 왼쪽: 커뮤니티 기반 시각화
            communities = set(partition.values())
            colors = plt.cm.Set3.colors
            color_map = {com: colors[i % len(colors)] for i, com in enumerate(communities)}
            node_colors = [color_map[partition[node]] for node in G.nodes()]
            
            # 노드 크기 (빈도 기반)
            freqs = nx.get_node_attributes(G, 'freq')
            if freqs:
                max_freq = max(freqs.values())
                node_sizes = [300 + 1000 * (freqs.get(n, 1) / max_freq) for n in G.nodes()]
            else:
                node_sizes = [300 for _ in G.nodes()]
            
            # 간선 스타일
            weights = [G[u][v]['weight'] for u, v in G.edges()]
            if weights:
                max_weight = max(weights)
                edge_widths = [0.5 + 3 * (w / max_weight) for w in weights]
            else:
                edge_widths = [1.0 for _ in G.edges()]
            
            # 커뮤니티 시각화
            nx.draw_networkx(G, pos, ax=ax1, node_color=node_colors, 
                            node_size=node_sizes, width=edge_widths,
                            font_properties=font_prop, font_size=8, 
                            with_labels=True, edge_color='gray', alpha=0.7)
            ax1.set_title(f"{title} - 커뮤니티", fontsize=14)
            ax1.axis('off')
            
            # 오른쪽: 중심성 기반 시각화
            if metrics and 'centrality' in metrics and 'betweenness' in metrics['centrality']:
                centrality = metrics['centrality']['betweenness']
                if centrality:
                    max_centrality = max(centrality.values())
                    if max_centrality > 0:
                        centrality_colors = [centrality.get(n, 0) / max_centrality for n in G.nodes()]
                    else:
                        centrality_colors = [0.5 for _ in G.nodes()]
                else:
                    centrality_colors = [0.5 for _ in G.nodes()]
                
                nx.draw_networkx(G, pos, ax=ax2, node_color=centrality_colors, 
                               cmap=plt.cm.Reds, node_size=node_sizes, width=edge_widths,
                               font_properties=font_prop, font_size=8,
                               with_labels=True, edge_color='gray', alpha=0.7)
                ax2.set_title(f"{title} - 매개 중심성", fontsize=14)
            else:
                # 중심성 정보가 없으면 degree 기반으로
                degrees = dict(G.degree())
                max_degree = max(degrees.values()) if degrees else 1
                degree_colors = [degrees.get(n, 0) / max_degree for n in G.nodes()]
                
                nx.draw_networkx(G, pos, ax=ax2, node_color=degree_colors, 
                               cmap=plt.cm.Blues, node_size=node_sizes, width=edge_widths,
                               font_properties=font_prop, font_size=8,
                               with_labels=True, edge_color='gray', alpha=0.7)
                ax2.set_title(f"{title} - 연결 정도", fontsize=14)
            
            ax2.axis('off')
        
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=self.config.dpi, bbox_inches='tight')
            logging.info(f"Network visualization saved to {output_path}")
        
        plt.show()
