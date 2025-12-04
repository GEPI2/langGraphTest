import { useState, useRef, useEffect } from 'react'
import { Send, User, Bot, RefreshCw } from 'lucide-react'
import { RemoteRunnable } from "@langchain/core/runnables/remote";
import ReactMarkdown from 'react-markdown';

interface Message {
    role: 'user' | 'assistant';
    content: string;
}

interface ChatInterfaceProps {
    threadId: string;
    onNodeStart: (node: string) => void;
    onNodeEnd: () => void;
    onHistorySelect: (history: any) => void;
}

export default function ChatInterface({ threadId, onNodeStart, onNodeEnd }: ChatInterfaceProps) {
    const [messages, setMessages] = useState<Message[]>([])
    const [input, setInput] = useState('')
    const [isLoading, setIsLoading] = useState(false)
    const messagesEndRef = useRef<HTMLDivElement>(null)

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
    }

    useEffect(scrollToBottom, [messages])

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        if (!input.trim() || isLoading) return

        const userMessage = input
        setInput('')
        setMessages(prev => [...prev, { role: 'user', content: userMessage }])
        setIsLoading(true)

        try {
            const response = await fetch('/api/agent/stream_events', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Thread-Id': threadId,
                },
                body: JSON.stringify({
                    input: { messages: [{ role: 'user', content: userMessage }] },
                    config: { configurable: { thread_id: threadId } },
                    version: "v2"
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const reader = response.body?.getReader();
            const decoder = new TextDecoder();
            let assistantMessage = ""
            setMessages(prev => [...prev, { role: 'assistant', content: "" }])

            if (reader) {
                while (true) {
                    const { done, value } = await reader.read();
                    if (done) break;

                    const chunk = decoder.decode(value, { stream: true });
                    
                    const lines = chunk.split('\n');
                    for (const line of lines) {
                        if (line.startsWith('event: data')) continue;
                        if (line.startsWith('data: ')) {
                            try {
                                const data = JSON.parse(line.slice(6));
                                const event = data;

                                if (event.event === "on_chain_start" && event.name !== "LangGraph") {
                                    onNodeStart(event.name)
                                }
                                if (event.event === "on_chain_end" && event.name !== "LangGraph") {
                                    onNodeEnd()
                                }

                                if (event.event === "on_chat_model_stream") {
                                    const chunkContent = event.data.chunk?.content;
                                    if (chunkContent) {
                                        assistantMessage += chunkContent
                                        setMessages(prev => {
                                            const newMessages = [...prev]
                                            newMessages[newMessages.length - 1].content = assistantMessage
                                            return newMessages
                                        })
                                    }
                                }
                            } catch (e) {
                                // ignore parse errors
                            }
                        }
                    }
                }
            }

        } catch (error) {
            console.error("Error:", error)
            setMessages(prev => [...prev, { role: 'assistant', content: `Error: ${error}` }])
        } finally {
            setIsLoading(false)
            onNodeEnd()
        }
    }

    return (
        <div className="flex flex-col h-full">
            <div className="p-4 border-b border-gray-700 flex justify-between items-center bg-gray-800">
                <h2 className="text-lg font-semibold">Chat</h2>
                <button
                    onClick={() => window.location.reload()}
                    className="p-2 hover:bg-gray-700 rounded-full transition-colors"
                    title="New Chat (Refresh)"
                >
                    <RefreshCw size={20} />
                </button>
            </div>

            <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.map((msg, idx) => (
                    <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`flex max-w-[80%] ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'} items-start gap-2`}>
                            <div className={`p-2 rounded-full ${msg.role === 'user' ? 'bg-blue-600' : 'bg-green-600'}`}>
                                {msg.role === 'user' ? <User size={20} /> : <Bot size={20} />}
                            </div>
                            <div className={`p-3 rounded-lg ${msg.role === 'user' ? 'bg-blue-600' : 'bg-gray-700'}`}>
                                <ReactMarkdown>{msg.content}</ReactMarkdown>
                            </div>
                        </div>
                    </div>
                ))}
                {isLoading && (
                    <div className="flex justify-start">
                        <div className="flex items-center gap-2 text-gray-400 text-sm ml-12">
                            <span className="animate-pulse">Thinking...</span>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            <form onSubmit={handleSubmit} className="p-4 border-t border-gray-700 bg-gray-800">
                <div className="flex gap-2">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Type a message..."
                        className="flex-1 bg-gray-700 text-white rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        disabled={isLoading}
                    />
                    <button
                        type="submit"
                        disabled={isLoading}
                        className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white p-2 rounded-lg transition-colors"
                    >
                        <Send size={20} />
                    </button>
                </div>
            </form>
        </div>
    )
}
