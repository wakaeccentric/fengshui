"""
風水相性診断アプリ
Feng Shui Compatibility App
"""

import streamlit as st
from PIL import Image
from datetime import datetime
import asyncio
import os
from fengshui_analyzer import (
    analyze_face_fengshui,
    generate_compatibility_report,
    calculate_zodiac,
    FIVE_ELEMENTS,
)

# ページ設定
st.set_page_config(
    page_title="風水相性診断",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# カスタムCSS - プレミアムデザイン
st.markdown(
    """
<style>
    /* メインカラーパレット */
    :root {
        --primary-color: #8B5CF6;
        --secondary-color: #EC4899;
        --accent-color: #F59E0B;
        --bg-dark: #1F2937;
        --bg-light: #F9FAFB;
        --text-light: #F3F4F6;
        --success-color: #10B981;
    }
    
    /* 背景グラデーション */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* ヘッダースタイル */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        background: linear-gradient(90deg, #FFD700, #FFA500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* カードスタイル */
    .card {
        background: #2d2d2d;
        color: #f5f5f5;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        backdrop-filter: blur(10px);
        margin: 1rem 0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 25px 70px rgba(0,0,0,0.4);
    }
    
    /* アップロードエリア */
    .upload-section {
        border: 3px dashed #8B5CF6;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        background: rgba(139, 92, 246, 0.05);
        transition: all 0.3s ease;
    }
    
    .upload-section:hover {
        border-color: #EC4899;
        background: rgba(236, 72, 153, 0.05);
    }
    
    /* 結果表示 */
    .result-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .score-circle {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        background: linear-gradient(135deg, #FFD700, #FFA500);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        font-weight: bold;
        margin: 0 auto;
        box-shadow: 0 10px 30px rgba(255, 215, 0, 0.4);
    }
    
    /* ボタンスタイル */
    .stButton>button {
        background: linear-gradient(90deg, #8B5CF6, #EC4899);
        color: white;
        font-size: 1.2rem;
        font-weight: 600;
        padding: 0.75rem 2rem;
        border-radius: 50px;
        border: none;
        box-shadow: 0 10px 30px rgba(139, 92, 246, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 40px rgba(139, 92, 246, 0.6);
    }
    
    /* スコアバッジ */
    .score-badge {
        display: inline-block;
        background: linear-gradient(90deg, #10B981, #059669);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        font-weight: 600;
        margin: 0.5rem;
        box-shadow: 0 5px 15px rgba(16, 185, 129, 0.3);
    }
    
    /* アニメーション */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animate-fade-in {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* サイドバー */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.95);
    }
    
    /* 入力フィールド */
    .stTextInput>div>div>input, .stDateInput>div>div>input {
        border-radius: 10px;
        border: 2px solid #8B5CF6;
        font-size: 1.1rem;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ヘッダー
st.markdown(
    """
<div class="main-header">
    <h1>🔮 風水相性診断アプリ</h1>
    <p style="font-size: 1.3rem; color: #FFD700;">顔相と五行で金運を見極める</p>
</div>
""",
    unsafe_allow_html=True,
)

# サイドバー - 男性の情報入力
with st.sidebar:
    st.markdown("### 👤 あなたの情報")

    man_age = st.number_input(
        "年齢",
        min_value=18,
        max_value=100,
        value=30,
        help="あなたの年齢を入力してください",
    )

    man_birthdate = st.date_input(
        "生年月日",
        value=datetime(1994, 1, 1),
        min_value=datetime(1920, 1, 1),
        max_value=datetime.now(),
        help="生年月日から干支と五行を計算します",
    )



    # .envファイルからAPIキーを読み込む
    api_key =st.secrets["google"]["api_key"]

    # 干支表示
    if man_birthdate:
        zodiac = calculate_zodiac(man_birthdate.year)
        st.markdown(
            f"""
        <div style="background: linear-gradient(135deg, #667eea, #764ba2); 
                    color: white; padding: 1rem; border-radius: 10px; margin-top: 1rem;">
            <div style="font-size: 1.1rem; font-weight: 600;">あなたの干支</div>
            <div style="font-size: 2rem; text-align: center; margin-top: 0.5rem;">
                {zodiac}
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

# メインエリア
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 👩 女性A の画像")
    woman1_image = st.file_uploader(
        "画像をアップロード",
        type=["jpg", "jpeg", "png"],
        key="woman1",
        help="顔がはっきり写っている画像を選択してください",
    )

    if woman1_image:
        image1 = Image.open(woman1_image)
        st.image(image1, caption="女性A", use_container_width=True)

with col2:
    st.markdown("### 👩 女性B の画像")
    woman2_image = st.file_uploader(
        "画像をアップロード",
        type=["jpg", "jpeg", "png"],
        key="woman2",
        help="顔がはっきり写っている画像を選択してください",
    )

    if woman2_image:
        image2 = Image.open(woman2_image)
        st.image(image2, caption="女性B", use_container_width=True)

# 分析ボタン
st.markdown("<br>", unsafe_allow_html=True)
analyze_button = st.button("🔮 風水診断を開始", use_container_width=True)

# 分析実行
if analyze_button:
    if not api_key:
        st.error("❌ Gemini APIキーを入力してください")
    elif not woman1_image or not woman2_image:
        st.error("❌ 両方の女性の画像をアップロードしてください")
    else:
        with st.spinner("🔮 風水分析中... しばらくお待ちください"):
            try:
                # 画像を開く
                img1 = Image.open(woman1_image)
                img2 = Image.open(woman2_image)

                # 非同期分析を同期的に実行
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                # 両方の画像を分析
                analysis1 = loop.run_until_complete(
                    analyze_face_fengshui(img1, api_key, "女性A")
                )
                analysis2 = loop.run_until_complete(
                    analyze_face_fengshui(img2, api_key, "女性B")
                )

                # 相性レポートの生成
                report = generate_compatibility_report(
                    man_age=man_age,
                    man_birthdate=man_birthdate,
                    woman1_analysis=analysis1,
                    woman2_analysis=analysis2,
                )

                st.markdown("## 📊 分析結果")

                # 総合スコア比較
                st.markdown("### 🏆 総合スコア比較")
                score_col1, score_col2 = st.columns(2)

                with score_col1:
                    st.markdown(
                        f"""
                    <div class="card animate-fade-in">
                        <h3 style="text-align: center; color: #8B5CF6;">女性A</h3>
                        <div class="score-circle">{report['woman1']['total_score']}</div>
                        <p style="text-align: center; margin-top: 1rem; font-size: 1.1rem;">
                            五行: <strong>{report['woman1']['element']}</strong><br>
                            相性: <strong>{report['woman1']['compatibility']['relationship']}</strong>
                        </p>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

                with score_col2:
                    st.markdown(
                        f"""
                    <div class="card animate-fade-in">
                        <h3 style="text-align: center; color: #EC4899;">女性B</h3>
                        <div class="score-circle">{report['woman2']['total_score']}</div>
                        <p style="text-align: center; margin-top: 1rem; font-size: 1.1rem;">
                            五行: <strong>{report['woman2']['element']}</strong><br>
                            相性: <strong>{report['woman2']['compatibility']['relationship']}</strong>
                        </p>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

                # おすすめ表示
                st.markdown(
                    f"""
                <div class="result-card animate-fade-in" style="text-align: center;">
                    <h2>✨ おすすめ: {report['recommendation']}</h2>
                    <p style="font-size: 1.2rem;">スコア差: {report['score_difference']}点</p>
                </div>
                """,
                    unsafe_allow_html=True,
                )

                # 詳細分析
                st.markdown("### 📋 詳細な顔相分析")

                detail_col1, detail_col2 = st.columns(2)

                with detail_col1:
                    st.markdown("#### 女性A の詳細")
                    with st.expander("🔍 顔相の詳細を見る", expanded=True):
                        st.write(f"**顔の形**: {analysis1.get('face_shape', 'N/A')}")
                        st.write(
                            f"**意味**: {analysis1.get('face_shape_meaning', 'N/A')}"
                        )
                        st.write(
                            f"**目の分析**: {analysis1.get('eyes_analysis', 'N/A')}"
                        )
                        st.write(
                            f"**鼻の分析**: {analysis1.get('nose_analysis', 'N/A')}"
                        )
                        st.write(
                            f"**口の分析**: {analysis1.get('mouth_analysis', 'N/A')}"
                        )

                        st.markdown("**💰 金運ポテンシャル**")
                        st.info(analysis1.get("wealth_potential", "N/A"))

                        st.markdown("**✨ 強み**")
                        for strength in analysis1.get("strengths", []):
                            st.success(f"✓ {strength}")

                with detail_col2:
                    st.markdown("#### 女性B の詳細")
                    with st.expander("🔍 顔相の詳細を見る", expanded=True):
                        st.write(f"**顔の形**: {analysis2.get('face_shape', 'N/A')}")
                        st.write(
                            f"**意味**: {analysis2.get('face_shape_meaning', 'N/A')}"
                        )
                        st.write(
                            f"**目の分析**: {analysis2.get('eyes_analysis', 'N/A')}"
                        )
                        st.write(
                            f"**鼻の分析**: {analysis2.get('nose_analysis', 'N/A')}"
                        )
                        st.write(
                            f"**口の分析**: {analysis2.get('mouth_analysis', 'N/A')}"
                        )

                        st.markdown("**💰 金運ポテンシャル**")
                        st.info(analysis2.get("wealth_potential", "N/A"))

                        st.markdown("**✨ 強み**")
                        for strength in analysis2.get("strengths", []):
                            st.success(f"✓ {strength}")

                # 五行相性の詳細
                st.markdown("### 🌟 五行相性の詳細")
                compat_col1, compat_col2 = st.columns(2)

                with compat_col1:
                    st.markdown(
                        f"""
                    <div class="card">
                        <h4>女性A との相性</h4>
                        <p><strong>関係性</strong>: {report['woman1']['compatibility']['relationship']}</p>
                        <p><strong>スコア</strong>: {report['woman1']['compatibility']['score']}/100</p>
                        <p>{report['woman1']['compatibility']['description']}</p>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

                with compat_col2:
                    st.markdown(
                        f"""
                    <div class="card">
                        <h4>女性B との相性</h4>
                        <p><strong>関係性</strong>: {report['woman2']['compatibility']['relationship']}</p>
                        <p><strong>スコア</strong>: {report['woman2']['compatibility']['score']}/100</p>
                        <p>{report['woman2']['compatibility']['description']}</p>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

            except Exception as e:
                import logging
                import traceback

                # エラーログに記録
                logging.basicConfig(
                    filename="c:/opt/data/ai/fengshui/error.log",
                    level=logging.ERROR,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    encoding="utf-8",
                )
                error_msg = f"Analysis failed: {str(e)}\n{traceback.format_exc()}"
                logging.error(error_msg)

                st.error(f"❌ エラーが発生しました: {str(e)}")
                st.info("💡 APIキーが正しいか、画像が適切か確認してください")
                st.warning("⚠️ 詳細なエラー情報は error.log ファイルに記録されました")

# フッター
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    """
<div style="text-align: center; color: white; padding: 2rem;">
    <p style="font-size: 0.9rem;">
        ⚠️ この診断は娯楽目的です。実際の人間関係の判断材料としてのみご利用ください。
    </p>
    <p style="font-size: 0.8rem; opacity: 0.8;">
        Powered by Google Gemini AI | 風水・五行思想に基づく分析
    </p>
</div>
""",
    unsafe_allow_html=True,
)
