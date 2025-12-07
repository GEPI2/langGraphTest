# 시스템 로그 (SYSTEM LOG)

## 프로젝트 개요
**목수**: 컨텍스트 보존을 위해 모든 주요 작업 또는 세션이 끝날 때마다 이 로그를 업데이트합니다.

## 최근 변경 사항 (2025-12-07)

### 1. 그래프 실행 에러 해결 (Failed to execute graph)
- **이슈**: `StartNode` 부재로 인한 LangGraph 유효성 검사 실패 (No entry point).
- **조치 (Backend)**: `GraphBuilder`에 Fallback 로직 추가 (StartNode 없을 시 첫 번째 노드 자동 연결).
- **조치 (Frontend)**: `StartNode`, `EndNode` 컴포넌트 추가 및 사이드바 등록.
- **결과**: `TC011` 테스트 통과, 프론트엔드 정상 실행 확인.

### 2. 프론트엔드 개발 환경 개선
- **이슈**: Docker 환경에서 코드 수정 시 브라우저 반영 안 됨.
- **조치**: `Dockerfile.dev` 생성 및 `vite.config.ts`에 `usePolling: true` 설정 추가.
- **결과**: Hot Reload 정상 작동 확인.

### 3. 테스트 및 검증 (진행 중)
- **계획**: 테스트 시나리오 문서화, UI/LLM 노드 검증, 사용자 가이드 작성.
