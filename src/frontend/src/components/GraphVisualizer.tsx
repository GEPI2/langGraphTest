import { useCallback } from 'react';
import ReactFlow, {
    Background,
    Controls,
    Node,
    Edge,
    useNodesState,
    useEdgesState,
    MarkerType,
} from 'reactflow';
import 'reactflow/dist/style.css';

// LangGraph 구조에 맞게 노드 정의
const initialNodes: Node[] = [
    {
        id: 'start',
        position: { x: 50, y: 250 },
        data: { label: 'Start' },
        type: 'input',
        style: { background: '#6b7280', color: 'white', border: 'none', borderRadius: '50%', width: 50, height: 50, display: 'flex', alignItems: 'center', justifyContent: 'center' }
    },
    {
        id: 'general_chat',
        position: { x: 250, y: 100 },
        data: { label: 'General Chat' },
        style: { background: '#1f2937', color: 'white', border: '1px solid #374151', padding: '10px', borderRadius: '8px' }
    },
    {
        id: 'generate_code',
        position: { x: 250, y: 400 },
        data: { label: 'Generate Code' },
        style: { background: '#1f2937', color: 'white', border: '1px solid #374151', padding: '10px', borderRadius: '8px' }
    },
    {
        id: 'execute_code',
        position: { x: 500, y: 400 },
        data: { label: 'Execute Code' },
        style: { background: '#1f2937', color: 'white', border: '1px solid #374151', padding: '10px', borderRadius: '8px' }
    },
    {
        id: 'human_review',
        position: { x: 750, y: 400 },
        data: { label: 'Human Review' },
        style: { background: '#c2410c', color: 'white', border: '1px solid #ea580c', padding: '10px', borderRadius: '8px' }
    },
    {
        id: 'end',
        position: { x: 1000, y: 250 },
        data: { label: 'End' },
        type: 'output',
        style: { background: '#6b7280', color: 'white', border: 'none', borderRadius: '50%', width: 50, height: 50, display: 'flex', alignItems: 'center', justifyContent: 'center' }
    },
];

const initialEdges: Edge[] = [
    { id: 'e1-1', source: 'start', target: 'general_chat', animated: true },
    { id: 'e1-2', source: 'start', target: 'generate_code', animated: true },
    { id: 'e2-1', source: 'general_chat', target: 'end' },
    { id: 'e3-1', source: 'generate_code', target: 'execute_code' },
    { id: 'e4-1', source: 'execute_code', target: 'generate_code', label: 'Error / Retry', markerEnd: { type: MarkerType.ArrowClosed } },
    { id: 'e4-2', source: 'execute_code', target: 'human_review', label: 'Success' },
    { id: 'e4-3', source: 'execute_code', target: 'end', label: 'Max Retries' },
    { id: 'e5-1', source: 'human_review', target: 'end', label: 'Approve' },
    { id: 'e5-2', source: 'human_review', target: 'generate_code', label: 'Reject' },
];

interface GraphVisualizerProps {
    threadId: string;
    currentNode: string | null;
    selectedHistory: any;
}

export default function GraphVisualizer({ currentNode }: GraphVisualizerProps) {
    const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
    const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

    // 현재 실행 중인 노드 하이라이트
    if (currentNode) {
        setNodes((nds) =>
            nds.map((node) => {
                if (node.id === currentNode) {
                    return {
                        ...node,
                        style: { ...node.style, background: '#2563eb', borderColor: '#3b82f6', boxShadow: '0 0 10px #3b82f6' },
                    };
                }
                return {
                    ...node,
                    style: {
                        ...node.style,
                        background: node.id === 'start' || node.id === 'end' ? '#6b7280' :
                            node.id === 'human_review' ? '#c2410c' : '#1f2937',
                        borderColor: '#374151',
                        boxShadow: 'none'
                    }
                };
            })
        );
    }

    return (
        <div className="w-full h-full bg-gray-900">
            <div className="absolute top-4 left-4 z-10 bg-gray-800 p-2 rounded shadow text-xs text-gray-300">
                <p>🔵 Active Node</p>
                <p>🟠 Human Review</p>
                <p>⚫ Inactive Node</p>
            </div>
            <ReactFlow
                nodes={nodes}
                edges={edges}
                onNodesChange={onNodesChange}
                onEdgesChange={onEdgesChange}
                fitView
                attributionPosition="bottom-left"
            >
                <Background color="#374151" gap={16} />
                <Controls />
            </ReactFlow>
        </div>
    );
}
