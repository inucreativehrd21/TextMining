
import os
import fitz  # PyMuPDF
from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
import logging

# 로깅 설정 (디버그 및 문제 해결에 도움)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def extract_text_from_pdfs(folder_path, char_limit=50000000):
    """
    지정된 폴더 내 PDF 파일을 모두 읽어 텍스트를 추출하고,
    전체 텍스트 길이가 char_limit을 넘으면 제한합니다.
    """
    text = ""
    try:
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(".pdf"):
                pdf_path = os.path.join(folder_path, filename)
                logging.info(f"Processing file: {filename}")
                with fitz.open(pdf_path) as doc:
                    for page in doc:
                        text += page.get_text()
                        if len(text) >= char_limit:
                            logging.info(f"Character limit {char_limit} reached, stopping text extraction.")
                            return text[:char_limit]
    except Exception as e:
        logging.error(f"Error during PDF text extraction: {e}")
    return text[:char_limit]

def clean_text(text):
    """
    텍스트 전처리 함수:
    - 불필요한 공백 및 특수문자 제거
    - 알파벳과 한글, 숫자만 남김
    - 소문자 변환 불필요 (한국어는 의미 없음)
    """
    text = re.sub(r'\s+', ' ', text)  # 다중 공백 하나로 축소
    text = re.sub(r'[^가-힣a-zA-Z0-9\s]', '', text)  # 한글, 영어, 숫자, 공백 제외 제거
    return text

def preprocess_and_extract_nouns(text, stopwords=set()):
    """
    KoNLPy Okt를 사용해 명사만 추출하고, 2자 이상 및 불용어를 걸러냅니다.
    """
    okt = Okt()
    nouns = okt.nouns(text)
    filtered_nouns = [word for word in nouns if len(word) > 1 and word not in stopwords]
    logging.info(f"Extracted {len(filtered_nouns)} nouns after filtering.")
    return filtered_nouns

def create_wordcloud(freq_dict, font_path, output_filename=None):
    """
    키워드 빈도 기반 워드클라우드 생성 및 화면 출력,
    output_filename 지정 시 이미지 파일로 저장.
    """
    wc = WordCloud(
        font_path=font_path,
        width=800,
        height=600,
        background_color='white',
        max_words=200,
        relative_scaling=0.5,
        colormap='Dark2'
    )
    wc.generate_from_frequencies(freq_dict)
    
    plt.figure(figsize=(12, 8))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout()
    
    if output_filename:
        wc.to_file(output_filename)
        logging.info(f"Wordcloud saved to {output_filename}")
    plt.show()

def main(pdf_folder, font_path, stopwords_path=None):
    # 1. PDF 텍스트 추출
    raw_text = extract_text_from_pdfs(pdf_folder)
    
    # 2. 텍스트 클린징
    cleaned_text = clean_text(raw_text)
    
    # 3. 불용어 목록 불러오기 (파일이 있으면)
    stopwords = set()
    if stopwords_path and os.path.exists(stopwords_path):
        with open(stopwords_path, "r", encoding="utf-8") as f:
            stopwords = set(line.strip() for line in f if line.strip())
        logging.info(f"Loaded {len(stopwords)} stopwords.")
    else:
        logging.info("No stopwords file provided or file not found. Proceeding without stopwords.")
    
    # 4. 명사 추출 및 불용어 제거
    nouns = preprocess_and_extract_nouns(cleaned_text, stopwords)
    
    # 5. 빈도수 계산
    freq = Counter(nouns)
    most_common = dict(freq.most_common(100))
    logging.info(f"Most common keywords: {list(most_common.items())[:10]}")
    
    # 6. 워드클라우드 생성 및 시각화
    create_wordcloud(most_common, font_path, output_filename="wordcloud.png")

if __name__ == "__main__":
    # 작업 경로 및 폰트 경로 설정 (윈도우 예시)
    pdf_folder = r"your_pdf_folder_path"  # PDF가 모여있는 폴더 경로
    font_path = "c:/Windows/Fonts/malgun.ttf"  # 한글 폰트 경로
    stopwords_file = r"your_stopwords_file_path"  # 한글 불용어 리스트 파일 (선택)

    main(pdf_folder, font_path, stopwords_file)
