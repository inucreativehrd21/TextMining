# Python Textmining

A comprehensive tool for Textmining

## Features

- **PDF Text Extraction**: Extract and preprocess text from multiple PDF files
- **Korean NLP**: Extract Korean nouns using KoNLPy
- **Keyword Analysis**: Frequency analysis and advanced filtering
- **Co-occurrence Networks**: Build and analyze keyword relationships
- **Network Visualization**: Community detection and centrality analysis
- **Memory Optimization**: Batch processing for large documents

## Installation

1. Install required packages:
pip install -r requirements.txt

2. Install KoNLPy dependencies:
- For Windows: Install Java JDK
- For macOS: `brew install openjdk`
- For Ubuntu: `sudo apt-get install openjdk-8-jdk`

## Usage

**Basic Setup**:
from config import AnalysisConfig
from main import run_complete_analysis

## Configure your analysis

config = AnalysisConfig(
pdf_folder="./your_pdf_folder",
font_path="c:/Windows/Fonts/malgun.ttf", # Windows
font_path="/System/Library/Fonts/AppleGothic.ttf", # macOS
output_dir="./results"
)

## Run analysis
G, metrics, freq = run_complete_analysis(config)

**Run the main script**:
python main.py
 
## Project Structure

- TMconfig.py # Configuration management
- bing_pdf_crawler.py # Crawling pdf from bing(browser)
- keyword_pdf_kor.py # Keyword extraction & analysis
- cooccurrence_network.py # Network analysis & visualization
- main.py # Main execution script
- requirements.txt # Python dependencies
- README.md # Project documentation
- example_config_eng.py # example form of config(eng)
- example_config.py # example form of config(kor)
- .gitignore # Git ignore rules

## Configuration Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| `pdf_folder` | Path to PDF files | Required |
| `font_path` | Korean font path | System default |
| `min_word_freq` | Minimum word frequency | 3 |
| `window_size` | Co-occurrence window size | 5 |
| `min_edge_weight` | Minimum edge weight | 2 |
| `max_nodes_display` | Max nodes in visualization | 100 |

## Output Files

- `wordcloud.png` - Keyword word cloud
- `network_visualization.png` - Network visualization
- `network.gexf` - Network file (Gephi compatible)
- `nodes.json` - Node information
- `edges.json` - Edge information
- `metrics.json` - Network metrics
- `centrality/` - Centrality measures

## Advanced Usage

- Custom Stopwords
Create a text file with one stopword per line:
의
가
을
를
? <- you can add stopword to each line

- Memory Optimization
For large documents, adjust batch size:
config.batch_size = 5000 # Smaller for limited memory


## Network Analysis Features

- **Community Detection**: Louvain algorithm
- **Centrality Measures**: Betweenness, closeness, degree, eigenvector
- **Network Metrics**: Density, clustering coefficient
- **Visualization**: Dual-view (community & centrality)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Acknowledgments

- [KoNLPy](https://konlpy.org) for Korean natural language processing
- [NetworkX](https://networkx.org) for network analysis
- [python-louvain](https://github.com/taynaud/python-louvain) for community detection


##########################################################################################

# 한국어 PDF 키워드 분석 및 공동출현 네트워크 도구

한국어 PDF 문서에서 키워드를 추출하고 공동출현 네트워크를 분석하는 종합 도구입니다.

## 주요 기능

- **PDF 텍스트 추출**: 여러 PDF 파일에서 텍스트 추출 및 전처리
- **한국어 자연어처리**: KoNLPy를 활용한 한국어 명사 추출
- **키워드 분석**: 빈도 분석 및 고급 필터링
- **공동출현 네트워크**: 키워드 간 관계 분석 및 네트워크 구성
- **네트워크 시각화**: 커뮤니티 탐지 및 중심성 분석
- **메모리 최적화**: 대용량 문서를 위한 배치 처리

## 설치 방법

1. 필요 패키지 설치:
pip install -r requirements.txt

2. KoNLPy 설치:
- Windows: Java JDK 설치
- macOS: `brew install openjdk`
- Ubuntu: `sudo apt-get install openjdk-8-jdk`

## 사용 방법

**기본 설정**:
from config import AnalysisConfig
from main import run_complete_analysis

## 분석 설정

config = AnalysisConfig(
pdf_folder="./your_pdf_folder",
font_path="c:/Windows/Fonts/malgun.ttf", # Windows
font_path="/System/Library/Fonts/AppleGothic.ttf", # macOS
output_dir="./results"
)


## 분석 실행
G, metrics, freq = run_complete_analysis(config)

**메인 스크립트 실행**:
python main.py

## 프로젝트 구조
- TMconfig.py # 설정 관리
- bing_pdf_crawler.py # pdf 크롤링(bing 브라우저)
- keyword_pdf_kor.py # 키워드 추출 및 분석
- cooccurrence_network.py # 네트워크 분석 및 시각화
- main.py # 메인 실행 스크립트
- requirements.txt # 필요한 Python 라이브러리
- README.md # 프로젝트 문서
- example_config_eng.py # 설정 예시 파일(영문)
- example_config.py # 설정 예시 파일(한국어)
- .gitignore # Git 무시 규칙


## 설정 옵션

| 매개변수 | 설명 | 기본값 |
|---------|------|--------|
| `pdf_folder` | PDF 파일 경로 | 필수 |
| `font_path` | 한글 폰트 경로 | 시스템 기본값 |
| `min_word_freq` | 최소 단어 빈도 | 3 |
| `window_size` | 공동출현 윈도우 크기 | 5 |
| `min_edge_weight` | 최소 간선 가중치 | 2 |
| `max_nodes_display` | 시각화 최대 노드 수 | 100 |

## 출력 파일

- `wordcloud.png` - 키워드 워드클라우드
- `network_visualization.png` - 네트워크 시각화
- `network.gexf` - 네트워크 파일 (Gephi 호환)
- `nodes.json` - 노드 정보
- `edges.json` - 간선 정보
- `metrics.json` - 네트워크 메트릭
- `centrality/` - 중심성 지표들

## 고급 사용법

### 사용자 정의 불용어
한 줄에 하나씩 불용어를 작성한 텍스트 파일 생성:

의
가
을
를
? <- 줄마다 불용어 추가 가능

### 메모리 최적화
대용량 문서의 경우 배치 크기 조정:
config.batch_size = 5000 # 메모리가 부족한 경우 작게 조정


## 네트워크 분석 기능

- **커뮤니티 탐지**: Louvain 알고리즘
- **중심성 지표**: 매개 중심성, 근접 중심성, 연결 중심성, 고유벡터 중심성
- **네트워크 메트릭**: 밀도, 군집 계수
- **시각화**: 이중 뷰 (커뮤니티 & 중심성)

## 기여하기

1. 저장소 포크
2. 기능 브랜치 생성 (`git checkout -b feature/AmazingFeature`)
3. 변경사항 커밋 (`git commit -m 'Add some AmazingFeature'`)
4. 브랜치에 푸시 (`git push origin feature/AmazingFeature`)
5. Pull Request 생성


## 주요 출처

- 한국어 자연어처리를 위한 [KoNLPy](https://konlpy.org)
- 네트워크 분석을 위한 [NetworkX](https://networkx.org)
- 커뮤니티 탐지를 위한 [python-louvain](https://github.com/taynaud/python-louvain)
