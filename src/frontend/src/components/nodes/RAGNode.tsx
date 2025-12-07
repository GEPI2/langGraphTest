import { memo } from 'react';
import { Handle, Position } from 'reactflow';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';
import { Database } from 'lucide-react';

const RAGNode = ({ data }: { data: any }) => {
  return (
    <Card className="min-w-[200px] border-2 border-orange-500">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium flex items-center gap-2">
          <Database className="w-4 h-4 text-orange-500" />
          RAG Retrieval
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="text-xs text-muted-foreground">
          {data.label || 'Retrieve context'}
        </div>
      </CardContent>
      <Handle type="target" position={Position.Top} className="w-3 h-3 bg-orange-500" />
      <Handle type="source" position={Position.Bottom} className="w-3 h-3 bg-orange-500" />
    </Card>
  );
};

export default memo(RAGNode);
