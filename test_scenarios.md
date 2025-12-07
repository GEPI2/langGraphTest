# 테스트 시나리오 및 결과 (Test Scenarios & Results)

## 1. 테스트 범위 (Test Scope)
본 문서는 LangGraph 기반 에이전트 플랫폼의 핵심 기능에 대한 테스트 시나리오와 결과를 정의합니다.

### 포함 범위 (In Scope)
- **그래프 에디터**: 노드 추가/삭제/연결, 그래프 저장.
- **그래프 실행**: 백엔드 API를 통한 그래프 실행 및 결과 반환.
- **노드 유형**: `StartNode`, `EndNode`, `LLMNode`, `CodeNode`.
- **예외 처리**: 잘못된 입력, 필수 노드 누락 시 동작.

### 제외 범위 (Out of Scope)
- **MCP 연동 심화 테스트**: 외부 MCP 서버와의 실제 통신 (Mocking으로 대체 가능하나 현재는 제외).
- **대규모 부하 테스트**: 성능 테스트는 추후 진행.
- **복잡한 RAG 파이프라인**: 기본적인 RAG 노드 동작만 확인.

---

## 2. 상세 테스트 시나리오 (Detailed Test Scenarios)

| ID | 테스트명 | 테스트 데이터/조건 | 테스트 방법 | 예상 결과 | 실제 결과 | 비고 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC001** | 그래프 에디터 기능 (Drag & Drop) | `LLMNode`, `RAGNode` 추가/연결 | `/graphs` API로 그래프 설정 저장 및 수정 시뮬레이션 | 그래프가 정상적으로 저장되고 수정되어야 함 | **PASS** | `TC001_test_graph_editor_node_drag_and_drop.py` |
| **TC002** | 그래프 실행 (Execution) | `StartNode` -> `CodeNode` | `/graphs/{id}/execute` API 호출 | CodeNode의 실행 결과가 반환되어야 함 | **PASS** | `TC002_test_graph_execution_trigger.py` |
| **TC009** | 그래프 저장 및 로드 (Save/Load) | 복잡한 노드/엣지 구성 | `/graphs` 저장 후 GET으로 조회하여 비교 | 저장된 설정과 로드된 설정이 일치해야 함 | **PASS** | `TC009_test_backend_api_graph_saving_and_loading.py` |
| **TC010** | 에러 핸들링 (Error Handling) | 잘못된 경로, 잘못된 바디 | 유효하지 않은 요청 전송 | 404 또는 422 에러 코드를 반환해야 함 | **PASS** | `TC010_test_backend_api_error_handling_for_invalid_inputs.py` |
| **TC011** | StartNode 누락 시 Fallback | `StartNode` 없이 `CodeNode`만 존재 | 그래프 생성 및 실행 | 자동으로 첫 번째 노드를 시작점으로 잡아 실행 성공 | **PASS** | `TC011_test_missing_start_node.py` |
| **TC012** | LLM 노드 실행 (LLM Node Run) | `StartNode` -> `LLMNode` | 실제 LLM 모델(Mock/Real) 호출 | LLM 응답이 포함된 결과 반환 | **PARTIAL** | API Quota Exhausted (Backend tried to call Gemini) |

---

## 3. 테스트 불가 범위 및 사유 (Limitations)

| 항목 | 사유 | 해결 방안 |
| :--- | :--- | :--- |
| **실제 LLM 비용** | 테스트 반복 시 API 비용 발생 가능 | Mock LLM 사용 또는 로컬 LLM(Ollama 등) 연동 권장 |
| **브라우저 UI 인터랙션** | 현재 테스트 스크립트는 API 위주 | Playwright/Selenium 등을 도입하여 E2E 테스트 구성 필요 |

---

## 4. 추가 의견 (Comments)
- `SYSTEM_LOG.md` 인코딩 문제는 UTF-8로 재생성하여 해결함.
- 프론트엔드 Hot Reload 설정으로 개발 생산성 향상됨.
