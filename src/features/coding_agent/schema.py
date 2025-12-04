from typing import TypedDict, Optional, List, Annotated
import operator

class AgentState(TypedDict):
    messages: Annotated[List[dict], operator.add]  # 채팅 기록 (Chat history)
    code: Optional[str]  # 생성된 파이썬 코드
    execution_output: Optional[str]  # 코드 실행 결과
    error: Optional[str]  # 실행 중 발생한 에러 메시지
    iterations: int  # 무한 루프 방지용 카운터
    human_feedback: Optional[str]  # 사람의 피드백 (승인/거절/수정요청)
