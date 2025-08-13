
from dataclasses import dataclass
from typing import Optional, Tuple

@dataclass
class AnalysisConfig:
    """분석 설정을 관리하는 클래스"""
    pdf_folder: str
    font_path: str = "c:/Windows/Fonts/malgun.ttf"
    stopwords_file: Optional[str] = None
    output_dir: str = "./results"
    
    # 텍스트 처리 설정
    char_limit: int = 50000000
    min_word_length: int = 2
    max_word_length: int = 15
    min_word_freq: int = 3
    batch_size: int = 10000
    
    # 네트워크 설정
    window_size: int = 5
    min_edge_weight: int = 2
    
    # 시각화 설정
    max_nodes_display: int = 100
    figure_size: Tuple[int, int] = (20, 10)
    dpi: int = 300
