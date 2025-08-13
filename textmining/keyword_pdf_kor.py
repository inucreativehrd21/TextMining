
import os
import fitz
from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
import logging
from typing import Set, List, Tuple
from TMconfig import AnalysisConfig

plt.rcParams['font.family'] = 'Malgun Gothic'  # 윈도우 기본 한글 폰트
plt.rcParams['axes.unicode_minus'] = False     # 마이너스 부호 깨짐 방지

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class EnhancedKeywordAnalyzer:
    def __init__(self, config: AnalysisConfig):
        self.config = config
        self.okt = Okt()
    
    def extract_text_from_pdfs_streaming(self, folder_path: str) -> str:
        """텍스트 추출"""
        text_chunks = []
        total_chars = 0
        
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(".pdf"):
                pdf_path = os.path.join(folder_path, filename)
                logging.info(f"Processing file: {filename}")
                
                try:
                    with fitz.open(pdf_path) as doc:
                        for page_num, page in enumerate(doc):
                            page_text = page.get_text()
                            if total_chars + len(page_text) > self.config.char_limit:
                                remaining = self.config.char_limit - total_chars
                                text_chunks.append(page_text[:remaining])
                                logging.info(f"Character limit {self.config.char_limit} reached.")
                                return ''.join(text_chunks)
                            
                            text_chunks.append(page_text)
                            total_chars += len(page_text)
                            
                except Exception as e:
                    logging.error(f"Error processing {filename}: {e}")
                    continue
        
        return ''.join(text_chunks)
    
    def enhanced_clean_text(self, text: str) -> str:
        """텍스트 전처리"""
        # URL 제거
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # 이메일 제거
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)
        
        # 연속된 특수문자 제거
        text = re.sub(r'[^\w\s가-힣]', ' ', text)
        
        # 숫자만으로 이루어진 단어 제거
        text = re.sub(r'\b\d+\b', '', text)
        
        # 다중 공백을 하나로
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def preprocess_and_extract_nouns_batch(self, text: str, stopwords: Set[str] = set()) -> List[str]:
        """배치 단위로 명사 추출하여 메모리 효율성 개선"""
        all_nouns = []
        
        # 텍스트를 배치 단위로 나누어 처리
        for i in range(0, len(text), self.config.batch_size):
            batch_text = text[i:i + self.config.batch_size]
            nouns = self.okt.nouns(batch_text)
            filtered = self.filter_nouns_advanced(nouns, stopwords)
            all_nouns.extend(filtered)
        
        logging.info(f"Extracted {len(all_nouns)} nouns after filtering.")
        return all_nouns
    
    def filter_nouns_advanced(self, nouns: List[str], stopwords: Set[str]) -> List[str]:
        """명사 필터링"""
        filtered = []
        
        for word in nouns:
            # 길이 조건
            if len(word) < self.config.min_word_length or len(word) > self.config.max_word_length:
                continue
                
            # 불용어 체크
            if word in stopwords:
                continue
                
            # 단일 문자 반복 제거 (예: "aaaa", "1111")
            if len(set(word)) == 1:
                continue
                
            # 의미없는 패턴 제거
            if re.match(r'^[가-힣]{1}[0-9]+$', word):  # "가1", "나123" 등
                continue
                
            filtered.append(word)
        
        return filtered
    
    def load_stopwords(self, stopwords_path: str) -> Set[str]:
        """불용어 로드"""
        stopwords = set()
        if stopwords_path and os.path.exists(stopwords_path):
            with open(stopwords_path, "r", encoding="utf-8") as f:
                stopwords = set(line.strip() for line in f if line.strip())
            logging.info(f"Loaded {len(stopwords)} stopwords.")
        else:
            logging.info("No stopwords file provided or file not found.")
        return stopwords
    
    def create_enhanced_wordcloud(self, freq_dict: dict, output_path: str = None):
        """워드클라우드 생성"""
        wc = WordCloud(
            font_path=self.config.font_path,
            width=800,
            height=600,
            background_color='white',
            max_words=200,
            relative_scaling=0.5,
            colormap='Dark2',
            prefer_horizontal=0.9,
            min_font_size=10
        )
        
        wc.generate_from_frequencies(freq_dict)
        
        plt.figure(figsize=(12, 8))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        plt.title('키워드 워드클라우드', fontsize=16, pad=20)
        plt.tight_layout()
        
        if output_path:
            wc.to_file(output_path)
            logging.info(f"Wordcloud saved to {output_path}")
        
        plt.show()
    
    def analyze(self) -> Tuple[List[str], Counter]:
        """전체 분석 실행"""
        # 1. PDF 텍스트 추출
        raw_text = self.extract_text_from_pdfs_streaming(self.config.pdf_folder)
        
        # 2. 텍스트 전처리
        cleaned_text = self.enhanced_clean_text(raw_text)
        
        # 3. 불용어 로드
        stopwords = self.load_stopwords(self.config.stopwords_file)
        
        # 4. 명사 추출
        nouns = self.preprocess_and_extract_nouns_batch(cleaned_text, stopwords)
        
        # 5. 빈도 계산
        freq = Counter(nouns)
        
        # 빈도가 낮은 단어 제거
        filtered_freq = Counter({word: count for word, count in freq.items() 
                               if count >= self.config.min_word_freq})
        
        logging.info(f"Top 10 keywords: {list(filtered_freq.most_common(10))}")
        
        return nouns, filtered_freq

def get_enhanced_nouns_and_freq(config: AnalysisConfig) -> Tuple[List[str], Counter]:
    """호출 API"""
    analyzer = EnhancedKeywordAnalyzer(config)
    return analyzer.analyze()

