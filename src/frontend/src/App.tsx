import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import GraphEditor from './components/GraphEditor';
import RAGDashboard from './components/dashboard/RAGDashboard';
import MCPDashboard from './components/dashboard/MCPDashboard';
import FineTuneDashboard from './components/dashboard/FineTuneDashboard';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<GraphEditor />} />
          <Route path="rag" element={<RAGDashboard />} />
          <Route path="mcp" element={<MCPDashboard />} />
          <Route path="finetune" element={<FineTuneDashboard />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
