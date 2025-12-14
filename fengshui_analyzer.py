"""
風水相性分析モジュール
Feng Shui compatibility analyzer using Google Gemini API
"""

import google.generativeai as genai
from datetime import datetime
from PIL import Image
import io
"""
風水相性分析モジュール
Feng Shui compatibility analyzer using Google Gemini API
"""

import google.generativeai as genai
from datetime import datetime
from PIL import Image
import io
import base64
import logging
import traceback
import hashlib

# ロギング設定
logging.basicConfig(
    filename="c:/opt/data/ai/fengshui/error.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
)

# 十二支の計算
ZODIAC_ANIMALS = [
    "子(鼠)",
    "丑(牛)",
    "寅(虎)",
    "卯(兎)",
    "辰(龍)",
    "巳(蛇)",
    "午(馬)",
    "未(羊)",
    "申(猿)",
    "酉(鶏)",
    "戌(犬)",
    "亥(猪)",
]

# 五行の対応関係
FIVE_ELEMENTS = {
    "木": {"color": "緑", "direction": "東", "season": "春"},
    "火": {"color": "赤", "direction": "南", "season": "夏"},
    "土": {"color": "黄", "direction": "中央", "season": "土用"},
    "金": {"color": "白", "direction": "西", "season": "秋"},
    "水": {"color": "黒", "direction": "北", "season": "冬"},
}


def calculate_zodiac(birth_year: int) -> str:
    """生年から干支を計算"""
    base_year = 1924
    index = (birth_year - base_year) % 12
    return ZODIAC_ANIMALS[index]


def get_element_from_zodiac(zodiac: str) -> str:
    """干支から五行を判定"""
    element_map = {
        "子(鼠)": "水",
        "亥(猪)": "水",
        "寅(虎)": "木",
        "卯(兎)": "木",
        "巳(蛇)": "火",
        "午(馬)": "火",
        "申(猿)": "金",
        "酉(鶏)": "金",
        "丑(牛)": "土",
        "辰(龍)": "土",
        "未(羊)": "土",
        "戌(犬)": "土",
    }
    return element_map.get(zodiac, "土")


def calculate_element_compatibility(element1: str, element2: str) -> dict:
    """五行の相性を計算"""
    generating_cycle = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
    overcoming_cycle = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}

    if (
        generating_cycle.get(element1) == element2
        or generating_cycle.get(element2) == element1
    ):
        return {
            "relationship": "相生",
            "score": 90,
            "description": "お互いを助け合う良い相性です",
        }
    elif overcoming_cycle.get(element1) == element2:
        return {
            "relationship": "相克",
            "score": 40,
            "description": "一方が他方を抑制する関係です",
        }
    elif overcoming_cycle.get(element2) == element1:
        return {
            "relationship": "被克",
            "score": 45,
            "description": "抑制される関係ですが、成長の機会にもなります",
        }
    elif element1 == element2:
        return {
            "relationship": "同気",
            "score": 70,
            "description": "同じ気を持つ安定した関係です",
        }
    else:
        return {"relationship": "平和", "score": 65, "description": "穏やかな関係です"}


async def analyze_face_fengshui(
    image: Image.Image, api_key: str, person_name: str = "女性"
) -> dict:
    """Gemini APIを使用して顔相を分析"""
    genai.configure(api_key=api_key)

    models_to_try = [
        "models/gemini-2.5-flash",
        "models/gemini-flash-latest",
        "models/gemini-2.0-flash",
        "models/gemini-pro-latest",
        "models/gemini-2.5-pro",
    ]

    prompt = f"""
この{person_name}の顔写真を風水・人相学の観点から分析してください。以下の要素を考慮してください：

1. **顔の輪郭**: 丸顔、面長、四角、卵型などの形状とその風水的意味
2. **目**: 大きさ、形、位置、輝きから見る運勢（特に金運との関連）
3. **鼻**: 高さ、大きさ、形から見る財運
4. **口**: 形、大きさから見る対人運と金運
5. **額**: 広さ、形から見る知恵と晩年運
6. **耳**: 大きさ、形から見る福運
7. **顔色・肌**: 明るさ、血色から見る健康運と金運
8. **全体的な印象**: 調和、バランスから見る総合運

特に**金運（財運）**に関する分析を重点的にお願いします。

分析結果は以下のJSON形式で返してください：
{
  "face_shape": "顔の形（例：丸顔）",
  "face_shape_meaning": "顔の形の風水的意味",
  "eyes_analysis": "目の分析結果",
  "nose_analysis": "鼻の分析結果（財運との関連を含む）",
  "mouth_analysis": "口の分析結果",
  "forehead_analysis": "額の分析結果",
  "ears_analysis": "耳の分析結果",
  "complexion_analysis": "顔色・肌の分析結果",
  "fortune_score": 85,
  "wealth_fortune_score": 80,
  "overall_impression": "全体的な印象と総合評価",
  "strengths": ["強み1", "強み2", "強み3"],
  "wealth_potential": "金運のポテンシャルについての詳細な説明"
}

必ずJSON形式で返答してください。
"""

    last_error = None

    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content([prompt, image])

            import json
            import re

            response_text = response.text
            json_match = re.search(r"```json\s*(.*?)\s*```", response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                json_str = response_text

            analysis_result = json.loads(json_str)
            return analysis_result

        except Exception as e:
            error_msg = f"Model {model_name} failed: {str(e)}\n{traceback.format_exc()}"
            logging.error(error_msg)
            last_error = e
            continue

    final_error_msg = (
        f"All models failed. Last error: {str(last_error)}\n{traceback.format_exc()}"
    )
    logging.error(final_error_msg)

    return {
        "face_shape": "分析失敗",
        "face_shape_meaning": "モデルエラー",
        "eyes_analysis": f"エラー: {str(last_error)}",
        "nose_analysis": "分析できませんでした",
        "mouth_analysis": "分析できませんでした",
        "forehead_analysis": "分析できませんでした",
        "ears_analysis": "分析できませんでした",
        "complexion_analysis": "分析できませんでした",
        "fortune_score": 50,
        "wealth_fortune_score": 50,
        "overall_impression": "利用可能なモデルが見つかりませんでした",
        "strengths": ["APIキーまたはモデル設定を確認してください"],
        "wealth_potential": "分析できませんでした",
    }


def generate_compatibility_report(
    man_age: int,
    man_birthdate: datetime,
    woman1_analysis: dict,
    woman2_analysis: dict,
    woman1_name: str = "女性A",
    woman2_name: str = "女性B",
    woman1_image: Image.Image = None,
    woman2_image: Image.Image = None,
) -> dict:
    """総合的な相性レポートを生成"""
    man_zodiac = calculate_zodiac(man_birthdate.year)
    man_element = get_element_from_zodiac(man_zodiac)

    # 画像ハッシュで五行を判定（確実に異なる値にする）
    def get_element_from_image(image: Image.Image) -> str:
        """画像ハッシュから五行を判定"""
        try:
            img_bytes = io.BytesIO()
            image.save(img_bytes, format="PNG")
            image_hash = int(hashlib.md5(img_bytes.getvalue()).hexdigest()[:8], 16)
            elements = ["金", "水", "木", "火", "土"]
            element = elements[image_hash % 5]
            logging.info(f"Image hash: {image_hash}, Element: {element}")
            return element
        except:
            return "土"

    woman1_element = get_element_from_image(woman1_image) if woman1_image else "土"
    woman2_element = get_element_from_image(woman2_image) if woman2_image else "金"

    compatibility1 = calculate_element_compatibility(man_element, woman1_element)
    compatibility2 = calculate_element_compatibility(man_element, woman2_element)

    total_score1 = (
        woman1_analysis.get("fortune_score", 50) * 0.3
        + woman1_analysis.get("wealth_fortune_score", 50) * 0.4
        + compatibility1["score"] * 0.3
    )

    total_score2 = (
        woman2_analysis.get("fortune_score", 50) * 0.3
        + woman2_analysis.get("wealth_fortune_score", 50) * 0.4
        + compatibility2["score"] * 0.3
    )

    return {
        "man_info": {"age": man_age, "zodiac": man_zodiac, "element": man_element},
        "woman1": {
            "name": woman1_name,
            "element": woman1_element,
            "face_analysis": woman1_analysis,
            "compatibility": compatibility1,
            "total_score": round(total_score1, 1),
        },
        "woman2": {
            "name": woman2_name,
            "element": woman2_element,
            "face_analysis": woman2_analysis,
            "compatibility": compatibility2,
            "total_score": round(total_score2, 1),
        },
        "recommendation": woman1_name if total_score1 > total_score2 else woman2_name,
        "score_difference": abs(round(total_score1 - total_score2, 1)),
    }
