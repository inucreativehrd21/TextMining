
"""
PDF 키워드 분석을 위한 예시 설정 파일입니다.
이 파일을 복사하여 환경에 맞게 경로를 수정하세요.
"""

from config import AnalysisConfig

# Windows 예시 설정
windows_config = AnalysisConfig(
    pdf_folder="./sample_pdfs",  # PDF 파일이 있는 폴더 경로
    font_path="c:/Windows/Fonts/malgun.ttf",  # Windows용 한글 폰트 경로
    stopwords_file="./stopwords.txt",  # 선택사항: 불용어 파일 경로
    output_dir="./analysis_results",
    
    # 텍스트 처리 매개변수
    char_limit=50000000,  # 처리할 최대 문자 수
    min_word_length=2,    # 최소 단어 길이
    max_word_length=15,   # 최대 단어 길이
    min_word_freq=3,      # 최소 단어 빈도
    batch_size=10000,     # 처리 배치 크기
    
    # 네트워크 분석 매개변수
    window_size=5,        # 공동출현 윈도우 크기
    min_edge_weight=2,    # 최소 간선 가중치
    
    # 시각화 매개변수
    max_nodes_display=50, # 표시할 최대 노드 수
    figure_size=(20, 10), # 그래프 크기
    dpi=300              # 이미지 해상도
)

# macOS 예시 설정
macos_config = AnalysisConfig(
    pdf_folder="./sample_pdfs",
    font_path="/System/Library/Fonts/AppleGothic.ttf",  # macOS용 한글 폰트
    stopwords_file="./stopwords.txt",
    output_dir="./analysis_results",
    min_word_freq=3,
    window_size=5,
    min_edge_weight=2,
    max_nodes_display=50
)

# Linux 예시 설정
linux_config = AnalysisConfig(
    pdf_folder="./sample_pdfs",
    font_path="/usr/share/fonts/truetype/nanum/NanumGothic.ttf",  # Linux용 한글 폰트
    stopwords_file="./stopwords.txt",
    output_dir="./analysis_results",
    min_word_freq=3,
    window_size=5,
    min_edge_weight=2,
    max_nodes_display=50
)

# 대용량 문서용 고성능 설정
large_doc_config = AnalysisConfig(
    pdf_folder="./large_pdfs",
    font_path="c:/Windows/Fonts/malgun.ttf",
    output_dir="./large_analysis_results",
    
    # 대용량 문서에 최적화
    char_limit=100000000,  # 더 많은 텍스트 처리
    min_word_freq=5,       # 높은 빈도 임계값
    batch_size=5000,       # 메모리 효율성을 위한 작은 배치
    window_size=3,         # 빠른 처리를 위한 작은 윈도우
    min_edge_weight=3,     # 높은 간선 가중치 임계값
    max_nodes_display=30   # 깔끔한 시각화를 위한 적은 노드 수
)
