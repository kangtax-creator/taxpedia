import requests
import xml.etree.ElementTree as ET
import google.generativeai as genai
from supabase import create_client

# ⚠️ 본인의 정보로 정확히 변경하세요
LAW_API_KEY = "kang1980" 
GEMINI_KEY = "이제안씀"
SUPABASE_URL = "https://oslbpdnpnsdcvgmvhlmh.supabase.co"
SUPABASE_KEY = "이제안씀"

genai.configure(api_key=GEMINI_KEY)
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 예시: 국가법령 API에서 '조세특례제한법' 관련 판례 가져오기
url = f"http://www.law.go.kr/DRF/lawSearch.do?OC={LAW_API_KEY}&target=prec&query=조세특례제한법&type=XML"
res = requests.get(url)
root = ET.fromstring(res.content)

for item in root.findall('.//prec'):
    title = item.find('사건명').text if item.find('사건명') is not None else "제목 없음"
    content = item.find('판시사항').text if item.find('판시사항') is not None else ""

    if not content: continue

    # 구글 제미나이 무료 임베딩 모델 사용 (768차원 변환)
    emb_res = genai.embed_content(
        model="models/embedding-001",
        content=content
    )
    embedding = emb_res['embedding']

    # 데이터베이스에 저장
    supabase.table("tax_documents").insert({
        "title": title,
        "content": content,
        "embedding": embedding
    }).execute()

print("구글 제미나이 기준 세법 데이터 무료 구축 완료!")