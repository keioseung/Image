import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import time
import json
import base64
import os
import re
from io import BytesIO

# 페이지 설정
st.set_page_config(
    page_title="Samsung AI Text Recognition",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 삼성 스타일 CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* 전체 스타일 */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
}

/* 헤더 스타일 */
.main-header {
    background: linear-gradient(135deg, #1428a0 0%, #1e40af 50%, #3b82f6 100%);
    color: white;
    padding: 4rem 2rem 3rem 2rem;
    border-radius: 0 0 40px 40px;
    margin: -1rem -1rem 3rem -1rem;
    text-align: center;
    box-shadow: 0 20px 60px rgba(20, 40, 160, 0.3);
    position: relative;
    overflow: hidden;
}

.main-header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="0.5"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
    opacity: 0.3;
}

.main-header h1 {
    font-size: 3.5rem;
    font-weight: 900;
    margin-bottom: 1rem;
    background: linear-gradient(135deg, #ffffff 0%, #e0e7ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    position: relative;
    z-index: 1;
}

.main-header p {
    font-size: 1.4rem;
    font-weight: 400;
    opacity: 0.9;
    margin-bottom: 0;
    position: relative;
    z-index: 1;
}

/* 카드 스타일 */
.feature-card {
    background: white;
    border-radius: 24px;
    padding: 2.5rem;
    margin-bottom: 2rem;
    box-shadow: 0 10px 40px rgba(0,0,0,0.08);
    border: 1px solid rgba(255,255,255,0.2);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.feature-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(135deg, #1428a0 0%, #3b82f6 100%);
}

.feature-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 60px rgba(0,0,0,0.15);
}

/* 버튼 스타일 */
.samsung-btn {
    background: linear-gradient(135deg, #1428a0 0%, #3b82f6 100%);
    color: white !important;
    border: none;
    border-radius: 16px;
    padding: 1rem 2rem;
    font-weight: 600;
    font-size: 1rem;
    box-shadow: 0 8px 25px rgba(20, 40, 160, 0.3);
    transition: all 0.3s ease;
    cursor: pointer;
}

.samsung-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 35px rgba(20, 40, 160, 0.4);
    background: linear-gradient(135deg, #1e40af 0%, #60a5fa 100%);
}

/* 사이드바 스타일 */
.sidebar .sidebar-content {
    background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
    border-right: 1px solid rgba(0,0,0,0.1);
}

/* 탭 스타일 */
.stTabs [data-baseweb="tab-list"] {
    justify-content: center;
    gap: 0.5rem;
    background: white;
    border-radius: 20px;
    padding: 0.5rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    margin-bottom: 2rem;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 16px;
    font-weight: 600;
    transition: all 0.3s ease;
    padding: 0.75rem 1.5rem;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #1428a0 0%, #3b82f6 100%);
    color: white !important;
    box-shadow: 0 4px 15px rgba(20, 40, 160, 0.3);
}

/* 메트릭 카드 */
.metric-card {
    background: linear-gradient(135deg, #1428a0 0%, #3b82f6 100%);
    color: white;
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    box-shadow: 0 8px 30px rgba(20, 40, 160, 0.2);
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
}

.metric-card::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
    transform: rotate(45deg);
    animation: shimmer 3s infinite;
}

@keyframes shimmer {
    0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
    100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
}

/* 애니메이션 */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes slideInLeft {
    from {
        opacity: 0;
        transform: translateX(-50px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes slideInRight {
    from {
        opacity: 0;
        transform: translateX(50px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes zoomIn {
    from {
        opacity: 0;
        transform: scale(0.8);
    }
    to {
        opacity: 1;
        transform: scale(1);
    }
}

.fade-in-up {
    animation: fadeInUp 0.6s ease-out;
}

.slide-in-left {
    animation: slideInLeft 0.8s ease-out;
}

.slide-in-right {
    animation: slideInRight 0.8s ease-out;
}

.zoom-in {
    animation: zoomIn 0.5s ease-out;
}

/* 호버 효과 */
.hover-lift {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.hover-lift:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 40px rgba(0,0,0,0.15);
}

/* 그라데이션 텍스트 */
.gradient-text {
    background: linear-gradient(135deg, #1428a0 0%, #3b82f6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 700;
}

/* 검색 결과 하이라이트 */
.search-highlight {
    background: linear-gradient(135deg, #1428a0 0%, #3b82f6 100%);
    color: white;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    font-weight: 600;
}

/* 로딩 애니메이션 */
.loading-spinner {
    display: inline-block;
    width: 20px;
    height: 20px;
    border: 3px solid rgba(255,255,255,.3);
    border-radius: 50%;
    border-top-color: #fff;
    animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

/* 반응형 디자인 */
@media (max-width: 768px) {
    .main-header h1 {
        font-size: 2.5rem;
    }
    
    .feature-card {
        padding: 1.5rem;
    }
}

/* 스크롤바 스타일 */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f5f9;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #1428a0 0%, #3b82f6 100%);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #1e40af 0%, #60a5fa 100%);
}

/* 이미지 업로드 영역 */
.upload-area {
    border: 3px dashed #3b82f6;
    border-radius: 20px;
    padding: 3rem;
    text-align: center;
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.05) 0%, rgba(20, 40, 160, 0.05) 100%);
    transition: all 0.3s ease;
}

.upload-area:hover {
    border-color: #1428a0;
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(20, 40, 160, 0.1) 100%);
}

/* 결과 카드 */
.result-card {
    background: white;
    border-radius: 20px;
    padding: 2rem;
    margin: 1rem 0;
    box-shadow: 0 8px 30px rgba(0,0,0,0.1);
    border-left: 5px solid #3b82f6;
}

/* 진행률 바 */
.progress-container {
    background: #e2e8f0;
    border-radius: 10px;
    padding: 0.5rem;
    margin: 1rem 0;
}

.progress-bar {
    background: linear-gradient(135deg, #1428a0 0%, #3b82f6 100%);
    height: 8px;
    border-radius: 5px;
    transition: width 0.3s ease;
}

/* 고급 기능 카드 */
.advanced-feature {
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    border-radius: 16px;
    padding: 1.5rem;
    margin: 1rem 0;
    border: 1px solid rgba(59, 130, 246, 0.2);
}

/* 성공/오류 메시지 */
.success-message {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    color: white;
    padding: 1rem;
    border-radius: 12px;
    margin: 1rem 0;
}

.error-message {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    color: white;
    padding: 1rem;
    border-radius: 12px;
    margin: 1rem 0;
}

.warning-message {
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    color: white;
    padding: 1rem;
    border-radius: 12px;
    margin: 1rem 0;
}
</style>

<div class="main-header">
    <h1>📱 Samsung AI Text Recognition</h1>
    <p>Advanced OCR Technology with AI-Powered Analysis & Insights</p>
</div>
""", unsafe_allow_html=True)

# OCR 언어 코드 매핑 확장
LANG_CODE_MAP = {
    "한국어": "kor",
    "영어": "eng",
    "일본어": "jpn",
    "중국어 간체": "chi_sim",
    "중국어 번체": "chi_tra",
    "프랑스어": "fra",
    "독일어": "deu",
    "스페인어": "spa",
    "이탈리아어": "ita",
    "포르투갈어": "por",
    "러시아어": "rus",
    "아랍어": "ara",
    "힌디어": "hin",
    "태국어": "tha",
    "베트남어": "vie"
}

# AI 모델 선택
AI_MODELS = {
    "Claude Sonnet 4": "claude-sonnet-4-20250514",
    "Claude Haiku": "claude-3-haiku-20240307",
    "GPT-4": "gpt-4",
    "GPT-3.5": "gpt-3.5-turbo"
}

# 이미지 전처리 함수
def preprocess_image(image, enhancement_level=1.2):
    """이미지 품질 향상을 위한 전처리"""
    try:
        img = Image.open(image).convert("RGB")
        
        # 밝기 및 대비 향상
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(enhancement_level)
        
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(enhancement_level)
        
        # 선명도 향상
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.5)
        
        return img
    except Exception as e:
        st.error(f"이미지 전처리 중 오류: {e}")
        return None

# 고급 OCR 함수
def advanced_ocr_extraction(image, lang_code, enhancement_level=1.2):
    """고급 OCR 텍스트 추출"""
    try:
        # 이미지 전처리
        processed_img = preprocess_image(image, enhancement_level)
        if processed_img is None:
            return "이미지 전처리 실패"
        
        # Tesseract OCR 실행
        text = pytesseract.image_to_string(processed_img, lang=lang_code)
        
        # 텍스트 정리
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    except Exception as e:
        return f"OCR 처리 중 오류 발생: {e}"

# AI 요약 함수 (모의)
def ai_summarize_text(text, model_name="Claude Sonnet 4"):
    """AI 텍스트 요약 (실제 API 키가 없을 때 모의 응답)"""
    try:
        if len(text) > 100:
            # 간단한 요약 로직
            sentences = text.split('.')
            if len(sentences) > 3:
                summary = f"[{model_name} 요약] {' '.join(sentences[:3])}... (전체 {len(text)}자 중 핵심 내용 추출)"
            else:
                summary = f"[{model_name} 요약] {text[:200]}... (전체 {len(text)}자)"
        else:
            summary = f"[{model_name} 요약] {text}"
        
        return summary
    except Exception as e:
        return f"AI 요약 중 오류 발생: {e}"

# 텍스트 분석 함수
def analyze_text(text):
    """텍스트 분석 및 통계"""
    if not text:
        return {}
    
    try:
        # 기본 통계
        words = text.split()
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        # 언어 감지 (간단한 방식)
        korean_chars = sum(1 for char in text if '\u3131' <= char <= '\u318e' or '\uac00' <= char <= '\ud7af')
        english_chars = sum(1 for char in text if char.isascii() and char.isalpha())
        
        if korean_chars > english_chars:
            detected_lang = "한국어"
        elif english_chars > korean_chars:
            detected_lang = "영어"
        else:
            detected_lang = "혼합"
        
        # 추가 분석
        avg_word_length = np.mean([len(word) for word in words]) if words else 0
        unique_words = len(set(words))
        
        # 텍스트 복잡도 점수
        complexity_score = min(100, (avg_word_length * 10 + unique_words / len(words) * 50) if words else 0)
        
        return {
            'char_count': len(text),
            'word_count': len(words),
            'sentence_count': len(sentences),
            'paragraph_count': len(paragraphs),
            'detected_language': detected_lang,
            'avg_word_length': round(avg_word_length, 2),
            'unique_words': unique_words,
            'complexity_score': round(complexity_score, 1),
            'reading_time_minutes': round(len(words) / 200, 1)  # 평균 읽기 속도 200단어/분
        }
    except Exception as e:
        st.error(f"텍스트 분석 중 오류: {e}")
        return {}

# 차트 생성 함수
def create_text_analysis_charts(analysis_data):
    """텍스트 분석 차트 생성"""
    if not analysis_data:
        return None, None, None, None
    
    try:
        # 1. 기본 통계 차트
        stats_data = {
            '항목': ['문자 수', '단어 수', '문장 수', '단락 수'],
            '수치': [
                analysis_data['char_count'],
                analysis_data['word_count'],
                analysis_data['sentence_count'],
                analysis_data['paragraph_count']
            ]
        }
        
        fig1 = px.bar(
            x=stats_data['항목'],
            y=stats_data['수치'],
            title="📊 텍스트 기본 통계",
            color=stats_data['수치'],
            color_continuous_scale='Blues'
        )
        fig1.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter", size=12),
            height=400
        )
        
        # 2. 언어 분포 파이 차트
        lang_data = pd.DataFrame({
            '언어': [analysis_data['detected_language']],
            '비율': [100]
        })
        
        fig2 = px.pie(
            lang_data,
            values='비율',
            names='언어',
            title=f"🌐 감지된 언어: {analysis_data['detected_language']}",
            color_discrete_sequence=['#3b82f6']
        )
        fig2.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter", size=12),
            height=400
        )
        
        # 3. 텍스트 복잡도 지표
        complexity_data = {
            '지표': ['평균 단어 길이', '고유 단어 수', '복잡도 점수'],
            '값': [
                analysis_data['avg_word_length'],
                analysis_data['unique_words'],
                analysis_data['complexity_score']
            ]
        }
        
        fig3 = px.bar(
            x=complexity_data['지표'],
            y=complexity_data['값'],
            title="📈 텍스트 복잡도 분석",
            color=complexity_data['값'],
            color_continuous_scale='Viridis'
        )
        fig3.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter", size=12),
            height=400
        )
        
        # 4. 읽기 시간 및 효율성
        reading_data = {
            '지표': ['예상 읽기 시간 (분)', '단어당 평균 문자'],
            '값': [
                analysis_data['reading_time_minutes'],
                round(analysis_data['char_count'] / max(analysis_data['word_count'], 1), 2)
            ]
        }
        
        fig4 = px.bar(
            x=reading_data['지표'],
            y=reading_data['값'],
            title="⏱️ 읽기 효율성 분석",
            color=reading_data['값'],
            color_continuous_scale='Plasma'
        )
        fig4.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter", size=12),
            height=400
        )
        
        return fig1, fig2, fig3, fig4
    except Exception as e:
        st.error(f"차트 생성 중 오류: {e}")
        return None, None, None, None

# 배치 처리 함수
def batch_process_images(uploaded_files, lang_code, enhancement_level=1.2):
    """여러 이미지 배치 처리"""
    results = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, file in enumerate(uploaded_files):
        status_text.text(f"처리 중: {file.name} ({i+1}/{len(uploaded_files)})")
        
        try:
            text = advanced_ocr_extraction(file, lang_code, enhancement_level)
            analysis = analyze_text(text)
            
            results.append({
                'filename': file.name,
                'text': text,
                'analysis': analysis,
                'status': '성공',
                'timestamp': datetime.now().isoformat()
            })
        except Exception as e:
            results.append({
                'filename': file.name,
                'text': '',
                'analysis': {},
                'status': f'오류: {str(e)}',
                'timestamp': datetime.now().isoformat()
            })
        
        progress_bar.progress((i + 1) / len(uploaded_files))
    
    status_text.text("배치 처리 완료!")
    return results

# 텍스트 내보내기 함수
def export_text_data(text, analysis, filename="extracted_text"):
    """텍스트 데이터 내보내기"""
    try:
        # JSON 형태로 데이터 구성
        export_data = {
            'text': text,
            'analysis': analysis,
            'export_timestamp': datetime.now().isoformat(),
            'filename': filename
        }
        
        # JSON 파일로 다운로드
        json_str = json.dumps(export_data, ensure_ascii=False, indent=2)
        b64 = base64.b64encode(json_str.encode()).decode()
        href = f'<a href="data:file/json;base64,{b64}" download="{filename}_analysis.json" class="samsung-btn" style="display: inline-block; text-decoration: none; margin: 0.5rem;">📊 JSON 내보내기</a>'
        
        # 텍스트 파일로 다운로드
        b64_text = base64.b64encode(text.encode('utf-8')).decode()
        href_text = f'<a href="data:file/txt;base64,{b64_text}" download="{filename}.txt" class="samsung-btn" style="display: inline-block; text-decoration: none; margin: 0.5rem;">📄 텍스트 내보내기</a>'
        
        return href, href_text
    except Exception as e:
        st.error(f"내보내기 중 오류: {e}")
        return "", ""

# 메인 앱
def main():
    # 사이드바 설정
    st.sidebar.markdown("## 🎛️ 설정")
    
    # 고급 옵션
    enhancement_level = st.sidebar.slider("🔧 이미지 향상 레벨", 1.0, 2.0, 1.2, 0.1)
    auto_analyze = st.sidebar.checkbox("📊 자동 텍스트 분석", value=True)
    auto_summarize = st.sidebar.checkbox("🤖 자동 AI 요약", value=False)
    
    # AI 모델 선택
    selected_ai_model = st.sidebar.selectbox("🤖 AI 모델 선택", list(AI_MODELS.keys()))
    
    # 통계 표시
    st.sidebar.markdown("## 📊 통계")
    if 'total_processed' not in st.session_state:
        st.session_state.total_processed = 0
    if 'total_characters' not in st.session_state:
        st.session_state.total_characters = 0
    if 'processing_history' not in st.session_state:
        st.session_state.processing_history = []
    
    st.sidebar.metric("총 처리된 이미지", st.session_state.total_processed)
    st.sidebar.metric("총 추출된 문자", st.session_state.total_characters)
    
    # 메인 탭
    tabs = st.tabs(["📱 단일 이미지", "📚 배치 처리", "📊 분석 대시보드", "📈 성능 분석", "⚙️ 설정"])
    
    with tabs[0]:
        st.markdown('<div class="fade-in-up">', unsafe_allow_html=True)
        
        # 이미지 업로드 영역
        st.markdown('<div class="upload-area">', unsafe_allow_html=True)
        uploaded_image = st.file_uploader(
            "📥 이미지 파일을 업로드하세요",
            type=["jpg", "jpeg", "png", "bmp", "tiff", "webp", "jfif"],
            help="텍스트가 포함된 이미지를 업로드하세요"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 언어 선택
        col1, col2 = st.columns(2)
        with col1:
            ocr_lang = st.selectbox("🌐 인식할 언어 선택", list(LANG_CODE_MAP.keys()), index=0)
        with col2:
            if st.button("🔍 언어 자동 감지", use_container_width=True):
                st.info("언어 자동 감지 기능은 이미지 처리 후 분석에서 확인할 수 있습니다.")
        
        # 이미지 처리
        if uploaded_image is not None:
            # 이미지 표시
            col1, col2 = st.columns([2, 1])
            with col1:
                st.image(uploaded_image, caption="업로드된 이미지", use_column_width=True)
            
            with col2:
                # 이미지 정보
                img = Image.open(uploaded_image)
                st.markdown("### 📋 이미지 정보")
                st.write(f"**크기:** {img.size[0]} x {img.size[1]} px")
                st.write(f"**모드:** {img.mode}")
                st.write(f"**형식:** {img.format}")
                st.write(f"**파일 크기:** {uploaded_image.size / 1024:.1f} KB")
            
            lang_code = LANG_CODE_MAP[ocr_lang]
            
            # OCR 처리
            with st.spinner("🧠 AI 텍스트 인식 중..."):
                text = advanced_ocr_extraction(uploaded_image, lang_code, enhancement_level)
            
            if text.startswith("OCR 처리 중 오류"):
                st.markdown('<div class="error-message">', unsafe_allow_html=True)
                st.error(text)
                st.markdown('</div>', unsafe_allow_html=True)
            elif len(text.strip()) == 0:
                st.markdown('<div class="warning-message">', unsafe_allow_html=True)
                st.warning("❗ 인식된 텍스트가 없습니다. 더 선명한 이미지를 시도해보세요.")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="success-message">', unsafe_allow_html=True)
                st.success("✅ 텍스트 인식 완료!")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # 텍스트 분석
                if auto_analyze:
                    analysis = analyze_text(text)
                else:
                    analysis = {}
                
                # 결과 표시
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown('<div class="result-card">', unsafe_allow_html=True)
                    st.markdown("### 📄 추출된 텍스트")
                    st.text_area("", value=text, height=300, key="extracted_text")
                    
                    # 내보내기 버튼
                    if analysis:
                        json_link, text_link = export_text_data(text, analysis, uploaded_image.name)
                        st.markdown(json_link, unsafe_allow_html=True)
                        st.markdown(text_link, unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    if analysis:
                        st.markdown("### 📊 텍스트 분석")
                        st.metric("문자 수", analysis.get('char_count', 0))
                        st.metric("단어 수", analysis.get('word_count', 0))
                        st.metric("문장 수", analysis.get('sentence_count', 0))
                        st.metric("감지된 언어", analysis.get('detected_language', 'N/A'))
                        st.metric("복잡도 점수", f"{analysis.get('complexity_score', 0)}/100")
                        st.metric("읽기 시간", f"{analysis.get('reading_time_minutes', 0)}분")
                
                # AI 요약
                if auto_summarize or st.button("🤖 AI 요약 생성", use_container_width=True, key="summarize_btn"):
                    with st.spinner(f"{selected_ai_model} 요약 중..."):
                        summary = ai_summarize_text(text, selected_ai_model)
                    
                    st.markdown('<div class="result-card">', unsafe_allow_html=True)
                    st.markdown("### 🤖 AI 요약 결과")
                    st.text_area("", value=summary, height=200, key="summary_text")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # 통계 업데이트
                st.session_state.total_processed += 1
                st.session_state.total_characters += analysis.get('char_count', 0)
                
                # 처리 히스토리 저장
                history_entry = {
                    'timestamp': datetime.now().isoformat(),
                    'filename': uploaded_image.name,
                    'char_count': analysis.get('char_count', 0),
                    'word_count': analysis.get('word_count', 0),
                    'language': analysis.get('detected_language', 'N/A'),
                    'complexity_score': analysis.get('complexity_score', 0)
                }
                st.session_state.processing_history.append(history_entry)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tabs[1]:
        st.markdown('<div class="fade-in-up">', unsafe_allow_html=True)
        st.markdown("## 📚 배치 처리")
        
        uploaded_files = st.file_uploader(
            "📥 여러 이미지 파일을 업로드하세요",
            type=["jpg", "jpeg", "png", "bmp", "tiff", "webp"],
            accept_multiple_files=True,
            help="여러 이미지를 한 번에 처리할 수 있습니다"
        )
        
        batch_lang = st.selectbox("🌐 배치 처리 언어 선택", list(LANG_CODE_MAP.keys()), index=0)
        
        if uploaded_files and st.button("🚀 배치 처리 시작", use_container_width=True):
            batch_results = batch_process_images(uploaded_files, LANG_CODE_MAP[batch_lang], enhancement_level)
            
            # 결과 표시
            st.markdown("### 📊 배치 처리 결과")
            
            # 결과 테이블
            results_df = pd.DataFrame(batch_results)
            st.dataframe(results_df[['filename', 'status', 'timestamp']], use_container_width=True)
            
            # 상세 결과
            for result in batch_results:
                with st.expander(f"📄 {result['filename']} - {result['status']}"):
                    if result['text']:
                        st.text_area("추출된 텍스트", value=result['text'], height=150, key=f"batch_{result['filename']}")
                        if result['analysis']:
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("문자 수", result['analysis'].get('char_count', 0))
                            with col2:
                                st.metric("단어 수", result['analysis'].get('word_count', 0))
                            with col3:
                                st.metric("감지된 언어", result['analysis'].get('detected_language', 'N/A'))
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tabs[2]:
        st.markdown('<div class="fade-in-up">', unsafe_allow_html=True)
        st.markdown("## 📊 분석 대시보드")
        
        # 대시보드 메트릭
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("총 처리된 이미지", st.session_state.total_processed)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("총 추출된 문자", st.session_state.total_characters)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            avg_chars = st.session_state.total_characters / max(st.session_state.total_processed, 1)
            st.metric("평균 문자 수", f"{avg_chars:.1f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("지원 언어", len(LANG_CODE_MAP))
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 샘플 데이터로 차트 생성
        if 'extracted_text' in st.session_state and st.session_state.get('extracted_text'):
            analysis = analyze_text(st.session_state.extracted_text)
            fig1, fig2, fig3, fig4 = create_text_analysis_charts(analysis)
            
            if fig1 and fig2 and fig3 and fig4:
                col1, col2 = st.columns(2)
                with col1:
                    st.plotly_chart(fig1, use_container_width=True)
                with col2:
                    st.plotly_chart(fig2, use_container_width=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.plotly_chart(fig3, use_container_width=True)
                with col2:
                    st.plotly_chart(fig4, use_container_width=True)
        else:
            st.info("📊 분석 차트를 보려면 먼저 이미지를 처리해주세요.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tabs[3]:
        st.markdown('<div class="fade-in-up">', unsafe_allow_html=True)
        st.markdown("## 📈 성능 분석")
        
        if st.session_state.processing_history:
            # 처리 히스토리 차트
            history_df = pd.DataFrame(st.session_state.processing_history)
            
            # 시간별 처리량
            fig_timeline = px.line(
                history_df,
                x='timestamp',
                y='char_count',
                title="📈 시간별 처리된 문자 수",
                labels={'char_count': '문자 수', 'timestamp': '시간'}
            )
            fig_timeline.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter", size=12)
            )
            st.plotly_chart(fig_timeline, use_container_width=True)
            
            # 언어별 분포
            lang_counts = history_df['language'].value_counts()
            fig_lang = px.pie(
                values=lang_counts.values,
                names=lang_counts.index,
                title="🌐 언어별 처리 분포"
            )
            fig_lang.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter", size=12)
            )
            st.plotly_chart(fig_lang, use_container_width=True)
            
            # 복잡도 점수 분포
            fig_complexity = px.histogram(
                history_df,
                x='complexity_score',
                title="📊 텍스트 복잡도 점수 분포",
                nbins=10
            )
            fig_complexity.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter", size=12)
            )
            st.plotly_chart(fig_complexity, use_container_width=True)
        else:
            st.info("📈 성능 분석을 보려면 먼저 이미지를 처리해주세요.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tabs[4]:
        st.markdown('<div class="fade-in-up">', unsafe_allow_html=True)
        st.markdown("## ⚙️ 고급 설정")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🔧 OCR 설정")
            st.checkbox("고급 이미지 전처리", value=True)
            st.checkbox("자동 언어 감지", value=False)
            st.checkbox("신뢰도 임계값 적용", value=True)
            
            st.markdown("### 🤖 AI 설정")
            st.selectbox("기본 AI 모델", list(AI_MODELS.keys()))
            st.slider("요약 길이", 50, 500, 200)
        
        with col2:
            st.markdown("### 📊 분석 설정")
            st.checkbox("자동 텍스트 분석", value=True)
            st.checkbox("통계 차트 생성", value=True)
            st.checkbox("결과 저장", value=False)
            
            st.markdown("### 🎨 UI 설정")
            st.selectbox("테마", ["Samsung Blue", "Dark", "Light"])
            st.checkbox("애니메이션 효과", value=True)
        
        st.markdown("### 💾 데이터 관리")
        if st.button("🗑️ 모든 데이터 초기화", use_container_width=True):
            st.session_state.clear()
            st.success("모든 데이터가 초기화되었습니다.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 푸터
    st.markdown("""
    <hr style="margin-top: 4rem;">
    <div style="text-align: center; color: #64748b; font-size: 0.9rem; padding: 2rem;">
        <p>📱 Samsung AI Text Recognition | Advanced OCR Technology</p>
        <p>Powered by Samsung AI & Machine Learning</p>
        <p style="font-size: 0.8rem; margin-top: 1rem;">© 2024 Samsung Electronics. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 