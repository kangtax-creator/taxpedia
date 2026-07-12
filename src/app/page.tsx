'use client';
import { useState } from 'react';

export default function Home() {
  const [text, setText] = useState('');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!text) return;
    setLoading(true);
    setResult('');
    try {
      const res = await fetch('/api/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_situation: text }),
      });
      const data = await res.json();
      setResult(data.answer);
    } catch (e) {
      setResult('서버 통신 중 오류가 발생했습니다.');
    }
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: '700px', margin: '50px auto', padding: '20px', fontFamily: 'sans-serif' }}>
      <h2 style={{ color: '#1e3a8a', borderBottom: '2px solid #e5e7eb', paddingBottom: '10px' }}>세법해석 AI 검색기 (Gemini Free)</h2>
      <p style={{ color: '#6b7280', fontSize: '14px' }}>궁금하신 세무 상황을 자세하게 적어주세요. 무료 AI가 판례를 분석합니다.</p>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="예시: 외국인 투자기업이 설립 후 공장 부지를 매입할 때 취득세 감면 혜택을 받을 수 있는 요건이 어떻게 되나요?"
        style={{ width: '100%', minHeight: '140px', padding: '12px', border: '1px solid #d1d5db', borderRadius: '6px', marginTop: '10px', fontSize: '15px', lineHeight: '1.5' }}
      />
      <button
        onClick={handleSearch}
        disabled={loading}
        style={{ width: '100%', padding: '12px', backgroundColor: '#1e3a8a', color: 'white', border: 'none', borderRadius: '6px', fontSize: '16px', marginTop: '10px', cursor: 'pointer' }}
      >
        {loading ? 'AI가 관련 판례 및 세법 분석 중...' : '세법 해석 요청하기'}
      </button>
      {result && (
        <div style={{ marginTop: '25px', padding: '20px', backgroundColor: '#f9fafb', borderRadius: '8px', border: '1px solid #e5e7eb', whiteSpace: 'pre-wrap', lineHeight: '1.6' }}>
          <strong>📋 AI 세무 오피니언 결과:</strong><br/><br/>
          {result}
        </div>
      )}
    </div>
  );
}