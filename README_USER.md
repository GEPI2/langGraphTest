# LangGraph Agent Platform - 사용자 가이드

## 1. 시작하기 (Getting Started)

### 필수 요구사항
- Docker & Docker Compose
- Python 3.10+ (로컬 테스트 시)

### 실행 방법
1. 프로젝트 루트 디렉토리에서 터미널을 엽니다.
2. 다음 명령어로 서비스를 실행합니다:
   ```bash
   docker-compose up -d --build
   ```
3. 브라우저에서 `http://localhost` 로 접속합니다.

---

## 2. 사용 방법 (How to Use)

### 그래프 생성
1. 왼쪽 사이드바에서 노드를 드래그하여 캔버스에 놓습니다.
   - **Start Node**: 그래프의 시작점 (필수).
   - **LLM Node**: AI 모델이 응답을 생성하는 노드.
   - **End Node**: 그래프의 종료점 (필수).
2. 노드의 핸들(점)을 클릭하고 드래그하여 다른 노드와 연결합니다.
3. `LLM Node`를 클릭하여 프롬프트나 모델 설정을 변경할 수 있습니다.

### 그래프 실행
1. 우측 상단의 **Run** 버튼을 클릭합니다.
2. 실행 결과가 하단 로그 패널이나 결과 창에 표시됩니다.

---

## 3. 문제 해결 (Troubleshooting)

- **"Failed to execute graph" 에러**:
  - `Start Node`가 그래프에 포함되어 있는지 확인하세요.
  - 모든 노드가 올바르게 연결되어 있는지 확인하세요.

- **브라우저 접속 불가**:
  - Docker 컨테이너가 실행 중인지 확인하세요 (`docker ps`).
  - `http://localhost:80` 포트가 다른 프로그램에 의해 사용 중인지 확인하세요.

---

## 4. 개발자 가이드 (Developer Guide)
- **Frontend**: `src/frontend` (React + Vite)
  - Hot Reload가 활성화되어 있어, 코드 수정 시 브라우저에 즉시 반영됩니다.
- **Backend**: `src/backend` (FastAPI + LangGraph)
  - `http://localhost:8001/docs` 에서 API 문서를 확인할 수 있습니다.
