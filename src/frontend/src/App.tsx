import { useState } from 'react'
import ChatInterface from './components/ChatInterface'
import GraphVisualizer from './components/GraphVisualizer'

function App() {
    // 현재 선택된 스레드 ID (기본값은 랜덤 생성)
    const [threadId, setThreadId] = useState(() => crypto.randomUUID())

    // 현재 실행 중인 노드 정보 (하이라이트용)
    const [currentNode, setCurrentNode] = useState<string | null>(null)

    // 사이드바에서 선택한 과거 실행 이력 (선택 시 해당 시점의 그래프 보여줌)
    const [selectedHistory, setSelectedHistory] = useState<any>(null)

    return (
        <div className="flex h-screen bg-gray-900 text-white">
            {/* 왼쪽: 그래프 시각화 영역 */}
            <div className="w-2/3 border-r border-gray-700 relative">
                <GraphVisualizer
                    threadId={threadId}
                    currentNode={currentNode}
                    selectedHistory={selectedHistory}
                />
            </div>

            {/* 오른쪽: 채팅 인터페이스 */}
            <div className="w-1/3 flex flex-col">
                <ChatInterface
                    threadId={threadId}
                    onNodeStart={(node) => setCurrentNode(node)}
                    onNodeEnd={() => setCurrentNode(null)}
                    onHistorySelect={(history) => setSelectedHistory(history)}
                />
            </div>
        </div>
    )
}

export default App
