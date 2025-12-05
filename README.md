# Dynamic LangGraph Agent Service

## 📖 프로젝트 개요 (Project Overview)
**Dynamic LangGraph Agent Service**는 복잡한 LLM 에이전트 워크플로우를 시각적으로 설계하고 실행할 수 있는 플랫폼입니다. 사용자는 직관적인 드래그 앤 드롭 인터페이스(React Flow)를 통해 에이전트 그래프를 구성하고, 강력한 백엔드 엔진(LangGraph)을 통해 이를 동적으로 실행할 수 있습니다.

이 프로젝트의 핵심 혁신은 **MetaAgent** 기능에 있습니다. 사용자가 자연어로 의도를 설명하기만 하면, AI가 자동으로 필요한 Python 노드 로직을 생성하여 그래프에 적용합니다.

## 🚀 핵심 기능 (Key Features)
- **Visual Graph Builder**: React Flow 기반의 직관적인 UI로 노드와 엣지를 손쉽게 생성 및 연결할 수 있습니다.
- **Dynamic Graph Compilation**: JSON 형태의 그래프 설정을 런타임에 실행 가능한 LangGraph `StateGraph` 객체로 즉시 변환합니다.
- **AI-Assisted Node Generation**: "MetaAgent"가 사용자의 프롬프트를 분석하여 커스텀 노드용 Python 코드를 자동 생성합니다.
- **State Persistence**: 단계별 실행 상태를 유지하여, 장기 실행 워크플로우에서도 데이터의 연속성을 보장합니다.
- **Secure Execution**: 동적 코드 실행을 위한 샌드박스 환경을 제공하여 보안성을 강화했습니다.

## 🛠️ 기술 스택 (Tech Stack)
### Backend
- **Framework**: FastAPI (Python 3.10+)
- **Agent Engine**: LangGraph, LangChain
- **Validation**: Pydantic
- **Testing**: Pytest

### Frontend
- **Framework**: React (Vite)
- **Visualization**: React Flow
- **State Management**: Zustand
- **Styling**: TailwindCSS
- **Icons**: Lucide React

## 📂 프로젝트 구조 (Project Structure)
```
src/
├── backend/
│   ├── engine/             # 동적 그래프 코어 로직
│   │   ├── builder.py      # 그래프 컴파일 및 빌드 로직
│   │   ├── node_factory.py # 노드 인스턴스화 및 코드 생성
│   │   └── schema.py       # 데이터 모델 (GraphConfig, NodeConfig)
│   ├── main.py             # FastAPI 엔트리 포인트
│   └── ...
├── frontend/               # React 애플리케이션
│   ├── src/
│   │   ├── components/     # UI 컴포넌트 (GraphEditor, Sidebar)
│   │   ├── store/          # Zustand 상태 관리
│   │   └── ...
│   └── ...
tests/                      # 테스트 스위트
├── unit/                   # 코어 로직 단위 테스트
├── integration/            # API 흐름 통합 테스트
└── debug/                  # 엣지 케이스 시나리오 (루프, 에러 등)
```

## ⚡ 시작하기 (Getting Started)

### 사전 요구사항 (Prerequisites)
- Python 3.10 이상
- Node.js 18 이상
- OpenAI API Key (MetaAgent 기능 사용 시 필요)

### 1. 백엔드 설정 (Backend Setup)
```bash
# 레포지토리 클론
git clone <repository-url>
cd langGraphTest

# Python 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
# .env 파일을 생성하고 API 키를 추가하세요
echo "OPENAI_API_KEY=your_api_key_here" > .env

# 백엔드 서버 실행
# 참고: 포트 충돌 방지를 위해 8001 포트를 사용합니다
uvicorn src.backend.main:app --host 0.0.0.0 --port 8001 --reload
```

### 2. 프론트엔드 설정 (Frontend Setup)
```bash
# 프론트엔드 디렉토리로 이동
cd src/frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

### 3. Docker로 실행하기 (Run with Docker)
간편하게 전체 시스템을 실행하려면 Docker를 사용하세요.
```bash
# 프로젝트 루트에서 실행
docker-compose up --build
```
- Frontend: http://localhost:80
- Backend: http://localhost:8001

### 4. 테스트 실행 (Running Tests)
단위, 통합, 디버그 시나리오를 포함한 포괄적인 테스트 스위트가 준비되어 있습니다.
```bash
# 전체 테스트 실행
pytest tests/
```

## 🧪 테스트 전략 (Testing Strategy)
- **Unit Tests**: `NodeFactory`와 `GraphBuilder`의 로직이 의도대로 동작하는지 개별적으로 검증합니다.
- **Integration Tests**: 그래프 생성부터 실행까지의 전체 API 흐름이 정상적으로 이어지는지 확인합니다.
- **Debug Scenarios**: 무한 루프나 런타임 에러 같은 예외 상황에서도 시스템이 안정적으로 대응하는지 검증합니다.

## 📝 라이선스 (License)
이 프로젝트는 MIT 라이선스를 따릅니다.
