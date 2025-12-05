# 시스템 로그 (SYSTEM LOG)

## 프로토콜
**필수**: 컨텍스트 보존을 위해 모든 주요 작업 또는 대화 세션이 끝날 때마다 이 파일을 업데이트해야 합니다.
**형식**: 날짜 - 이벤트/결정 - 상세 내용

## 로그
- **2025-12-05**: 프로젝트 전환 시작 (Project Pivot Initiated).
    - **이전 상태**: 자가 치유 에이전트 (자율 오류 수정에 중점).
    - **새로운 목표**: 동적 랭그래프 에이전트 서비스 (노/로우 코드 그래프 빌더).
    - **주요 기능**:
        - 비주얼 노드 에디터 (React Flow).
        - LLM 보조 노드 코드 생성.
        - 실시간 실행 시각화.
        - 재귀적/순환적 그래프 지원.
        - RAG 통합.
    - **아키텍처 전략**:
        - 백엔드: FastAPI + LangGraph (설정으로부터 동적 그래프 구성).
        - 프론트엔드: React + React Flow.

- **2025-12-05**: ������Ʈ ���� ������ (Project Structure Reorganization).
    - **����� ��û**: ���ϰ� ���丮�� ü�������� �����ϰ� �������� �� ���� �̵����� ����.
    - **���� ����**:
        - scripts/ ����: ��Ʈ�� ��ƿ��Ƽ ��ũ��Ʈ(debug_stream.py, gen_graph.py ��) �� deploy.sh �̵�.
        - docs/artifacts/ ����: ���̾�׷�(*.mermaid) �� �̹���, �ؽ�Ʈ ���� �̵�.
        - data/ ����: ���� DB ����(checkpoints.sqlite*) �̵�.
        - legacy/ ����: ��Ʈ Dockerfile (Streamlit��) �� src/ui (Streamlit �ڵ�) �̵�.
    - **���**: ������Ʈ ��Ʈ�� src, docs, scripts, data, legacy �� �ʼ� ���� ���Ϸ� ����ϰ� ������.
