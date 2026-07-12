from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
from supabase import create_client
import os

app = FastAPI()

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
supabase = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))

class SearchRequest(BaseModel):
    user_situation: str

@app.post("/api/search")
async def search_tax_law(request: SearchRequest):
    try:
        # 1. 사용자 질문을 벡터화 (새로운 키로 정상 작동)
        emb_res = genai.embed_content(
            model="models/text-embedding-004",
            content=request.user_situation
        )
        emb = emb_res['embedding']

        # 2. Supabase DB에서 유사 판례 3개 검색
        docs = supabase.rpc("match_documents", {
            "query_embedding": emb,
            "match_threshold": 0.3,
            "match_count": 3
        }).execute().data

        if not docs:
            return {"answer": "참고할 만한 비슷한 세법 해석 데이터를 찾지 못했습니다."}

        context = "\n\n".join([f"[{d['title']}]\n{d['content']}" for d in docs])

        # 3. Gemini 모델로 최종 답변 생성
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"전문가로서 제공된 참고 법령만을 바탕으로 의뢰인의 상황에 맞는 면밀한 해석과 실무적 주의점을 친절하게 답변하세요.\n\n사용자 상황:\n{request.user_situation}\n\n참고 법령:\n{context}"
        
        response = model.generate_content(prompt)
        
        return {"answer": response.text}
        
    except Exception as e:
        return {"answer": f"오류가 발생했습니다: {str(e)}"}