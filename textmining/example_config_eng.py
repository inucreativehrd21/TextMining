
"""
Example configuration file for PDF keyword analysis.
Copy this file and modify the paths according to your environment.
"""

from config import AnalysisConfig

# Windows example configuration
windows_config = AnalysisConfig(
    pdf_folder="./sample_pdfs",  # Path to folder containing PDF files
    font_path="c:/Windows/Fonts/malgun.ttf",  # Korean font path for Windows
    stopwords_file="./stopwords.txt",  # Optional: stopwords file path
    output_dir="./analysis_results",
    
    # Text processing parameters
    char_limit=50000000,  # Maximum characters to process
    min_word_length=2,    # Minimum word length
    max_word_length=15,   # Maximum word length
    min_word_freq=3,      # Minimum word frequency
    batch_size=10000,     # Batch size for processing
    
    # Network analysis parameters
    window_size=5,        # Co-occurrence window size
    min_edge_weight=2,    # Minimum edge weight
    
    # Visualization parameters
    max_nodes_display=50, # Maximum nodes to display
    figure_size=(20, 10), # Figure size for plots
    dpi=300              # Image resolution
)

# macOS example configuration
macos_config = AnalysisConfig(
    pdf_folder="./sample_pdfs",
    font_path="/System/Library/Fonts/AppleGothic.ttf",  # Korean font for macOS
    stopwords_file="./stopwords.txt",
    output_dir="./analysis_results",
    min_word_freq=3,
    window_size=5,
    min_edge_weight=2,
    max_nodes_display=50
)

# Linux example configuration
linux_config = AnalysisConfig(
    pdf_folder="./sample_pdfs",
    font_path="/usr/share/fonts/truetype/nanum/NanumGothic.ttf",  # Korean font for Linux
    stopwords_file="./stopwords.txt",
    output_dir="./analysis_results",
    min_word_freq=3,
    window_size=5,
    min_edge_weight=2,
    max_nodes_display=50
)

# High-performance configuration for large documents
large_doc_config = AnalysisConfig(
    pdf_folder="./large_pdfs",
    font_path="c:/Windows/Fonts/malgun.ttf",
    output_dir="./large_analysis_results",
    
    # Optimized for large documents
    char_limit=100000000,  # Process more text
    min_word_freq=5,       # Higher frequency threshold
    batch_size=5000,       # Smaller batches for memory efficiency
    window_size=3,         # Smaller window for faster processing
    min_edge_weight=3,     # Higher edge weight threshold
    max_nodes_display=30   # Fewer nodes for cleaner visualization
)
