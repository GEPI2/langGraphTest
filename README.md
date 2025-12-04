# 자가 치유 코딩 에이전트 (Self-Correcting Coding Agent)

**LangGraph**와 **Google Gemini**를 활용하여 스스로 코드를 작성하고, 에러를 수정하며, 사람의 최종 승인을 받아 작업을 완료하는 지능형 코딩 에이전트입니다.

## ✨ 주요 기능

1. **자가 치유 (Self-Correction)**
    * 에이전트가 생성한 코드를 즉시 실행하여 검증합니다.
    * 에러 발생 시, 에러 로그를 분석하여 스스로 코드를 수정하고 재실행합니다. (최대 3회 시도)
2. **휴먼 인 더 루프 (Human-in-the-loop)**
    * 코드가 성공적으로 실행되더라도 즉시 종료하지 않습니다.
    * 사용자가 결과물을 검토하고 **승인(Approve)**하거나 **수정 요청(Reject)**할 수 있습니다.
3. **고성능 AI 모델**
    * Google의 최신 `gemini-2.0-flash` 모델을 사용하여 빠르고 정확하게 코드를 생성합니다.
4. **웹 UI 제공**
    * Streamlit 기반의 직관적인 채팅 인터페이스를 제공합니다.

## 🛠️ 기술 스택

* **Framework**: [LangGraph](https://langchain-ai.github.io/langgraph/), [LangChain](https://www.langchain.com/)
* **LLM**: Google Gemini (`gemini-2.0-flash`)
* **UI**: [Streamlit](https://streamlit.io/)
* **Language**: Python 3.10+

## 🚀 시작하기

### 1. 필수 조건

* Python 3.10 이상 설치
* Google Cloud API Key 발급 ([Google AI Studio](https://aistudio.google.com/))

### 2. 설치

프로젝트를 클론하고 의존성 패키지를 설치합니다.

```bash
git clone https://github.com/GEPI2/langGraphTest.git
cd langGraphTest
pip install -r requirements.txt
```

*(참고: `requirements.txt`가 없다면 다음 패키지를 설치하세요)*

```bash
pip install langgraph langchain-google-genai streamlit python-dotenv
```

### 3. 환경 변수 설정

`.env` 파일을 생성하고 API 키를 입력합니다.

```env
GOOGLE_API_KEY=your_api_key_here
```

### 4. 실행

Streamlit UI를 실행하여 에이전트와 대화합니다.

```bash
streamlit run src/ui/app.py
```

## 📂 프로젝트 구조 (Vibe Coding)

이 프로젝트는 **Feature-Sliced Lite** 구조를 따릅니다.

```text
src/
├── features/
│   └── coding_agent/       # 핵심 기능 모듈
│       ├── graph.py        # LangGraph 워크플로우 정의
│       ├── nodes.py        # 노드 (코드 생성, 실행, 검토) 구현
│       └── schema.py       # 상태(State) 스키마 정의
├── ui/
│   └── app.py              # Streamlit 웹 인터페이스
└── shared/                 # 공용 유틸리티 (현재 미사용)
```

## 🧪 테스트

터미널에서 에이전트의 로직만 빠르게 테스트하려면 다음 스크립트를 실행하세요.

```bash
python test_agent.py
```
