# CodePath AI201

CodePath AI201 코스의 주차별 랩 모음입니다.

## Labs

| Week | Lab | Description |
|------|-----|-------------|
| 2 | [PlantAdvisor](./lab2-plantadvisor) | Groq + Gradio 기반 AI 식물 관리 어시스턴트 에이전트 |

## 실행 방법 (각 랩 공통)

```bash
cd labN-name
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # 그 후 .env 에 본인 API 키 입력
python app.py
```
