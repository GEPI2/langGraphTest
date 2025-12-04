# SYSTEM_LOG.md

# SYSTEM_LOG.md

## 3. 알려진 버그/이슈

1. **Gemini API 연동 관련**
    - [x] 라이브러리 설치 & 코드 수정
    - [x] API Key 설정 (.env)

- [ ] **UI 개발 (Streamlit)**
  - [ ] Streamlit 설치
  - [ ] 채팅 인터페이스 구현
  - [ ] Human-in-the-loop 연동 (승인/거절 버튼)

## 4. AI 작업 가이드 (Workflow)

1. **Coding Agent 개발** (Self-Correcting + HITL)
    - [x] Schema 정의
    - [x] Node 구현 (Gen, Exec, Review)
    - [x] Graph 구성
2. **Context Sync**: 작업 시작 전 이 파일을 읽고 현재 상태 파악.
3. **Feature Coding**: `/src/features` 내에 기능 단위로 작업.
4. **Verify & Log**: 작업 종료 전 에러 확인 및 이 파일 업데이트.
