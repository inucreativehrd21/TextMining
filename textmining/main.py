
import os
import logging
from TMconfig import AnalysisConfig
from keyword_pdf_kor import EnhancedKeywordAnalyzer
from build_cooccurrence_network import EnhancedCooccurrenceNetwork

def run_complete_analysis(config: AnalysisConfig):
    """전체 분석 파이프라인 실행"""
    
    # 출력 디렉토리 생성
    os.makedirs(config.output_dir, exist_ok=True)
    
    logging.info("=== 키워드 분석 및 공동출현 네트워크 분석 시작 ===")
    
    try:
        # 1. 키워드 분석
        logging.info("1. 키워드 추출 중...")
        analyzer = EnhancedKeywordAnalyzer(config)
        nouns, freq = analyzer.analyze()
        
        # 워드클라우드 생성
        if freq:
            wordcloud_path = os.path.join(config.output_dir, "wordcloud.png")
            analyzer.create_enhanced_wordcloud(dict(freq.most_common(100)), wordcloud_path)
        
        # 2. 네트워크 분석
        logging.info("2. 공동출현 네트워크 생성 중...")
        network_analyzer = EnhancedCooccurrenceNetwork(config)
        G = network_analyzer.build_cooccurrence_network(nouns)
        
        # 3. 네트워크 메트릭 계산
        logging.info("3. 네트워크 분석 중...")
        metrics = network_analyzer.calculate_network_metrics(G)
        
        # 4. 결과 저장
        logging.info("4. 결과 저장 중...")
        network_analyzer.save_network_results(G, metrics, config.output_dir)
        
        # 5. 시각화
        logging.info("5. 네트워크 시각화 중...")
        viz_path = os.path.join(config.output_dir, "network_visualization.png")
        network_analyzer.draw_enhanced_network(G, metrics, output_path=viz_path)
        
        # 6. 결과 요약 출력
        print("\n=== 분석 결과 요약 ===")
        print(f"총 추출된 키워드 수: {len(nouns)}")
        print(f"고유 키워드 수: {len(freq)}")
        print(f"네트워크 노드 수: {metrics.get('nodes', 0)}")
        print(f"네트워크 간선 수: {metrics.get('edges', 0)}")
        print(f"네트워크 밀도: {metrics.get('density', 0):.4f}")
        
        if freq:
            print(f"\n상위 10개 키워드:")
            for i, (word, count) in enumerate(freq.most_common(10), 1):
                print(f"  {i}. {word}: {count}회")
        
        print(f"\n결과 파일들이 '{config.output_dir}' 폴더에 저장되었습니다.")
        
        logging.info("=== 분석 완료 ===")
        return G, metrics, freq
        
    except Exception as e:
        logging.error(f"분석 중 오류 발생: {e}")
        raise

if __name__ == "__main__":
    # 실제 경로로 수정
    config = AnalysisConfig(
        pdf_folder=r"your_pdf_folder_path",  # PDF 파일들이 있는 폴더 경로
        font_path=r"c:/Windows/Fonts/malgun.ttf",  # 한글 폰트 경로
        stopwords_file=r"your_stopwords_file_path",  # 불용어 파일 경로 (선택사항)
        output_dir="./analysis_results",
        
        # 분석 파라미터 조정
        min_word_freq=3,  # 최소 단어 빈도
        window_size=5,    # 공동출현 윈도우 크기
        min_edge_weight=2, # 최소 간선 가중치
        max_nodes_display=50  # 시각화할 최대 노드 수
    )
    
    # 전체 분석 실행
    try:
        G, metrics, freq = run_complete_analysis(config)
        
        # 추가 분석이 필요하면 여기서 진행
        # 예: 특정 키워드 중심의 서브네트워크 분석 등
        
    except Exception as e:
        print(f"분석 실행 중 오류: {e}")
