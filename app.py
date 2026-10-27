import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# .env 파일에서 OPENAI_API_KEY 불러오기
load_dotenv()

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

LANGUAGES = {
    "영어": "English",
    "일본어": "Japanese",
    "베트남어": "Vietnamese",
}


@st.cache_resource
def get_client():
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def translate(text: str, target_language: str) -> str:
    client = get_client()
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    f"You are a professional translator. Translate the user's text into {target_language}. "
                    "Output only the translation, without explanations or quotation marks."
                ),
            },
            {"role": "user", "content": text},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()


st.set_page_config(page_title="번역기", page_icon="🌐")
st.title("🌐 간단 번역기")

if not os.getenv("OPENAI_API_KEY"):
    st.error(".env 파일에 OPENAI_API_KEY를 설정해주세요.")
    st.stop()

text = st.text_area("번역할 글을 입력하세요", height=200)
language = st.radio("번역할 언어를 선택하세요", list(LANGUAGES.keys()), horizontal=True)

if st.button("번역하기", type="primary"):
    if not text.strip():
        st.warning("번역할 글을 입력해주세요.")
    else:
        with st.spinner(f"{language}로 번역 중..."):
            try:
                result = translate(text, LANGUAGES[language])
                st.subheader(f"번역 결과 ({language})")
                st.text_area("결과", value=result, height=200, label_visibility="collapsed")
            except Exception as e:
                st.error(f"번역 중 오류가 발생했습니다: {e}")
