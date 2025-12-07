import { memo } from 'react';
import { Handle, Position } from 'reactflow';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';
import { Wrench } from 'lucide-react';

const ToolNode = ({ data }: { data: any }) => {
  return (
    <Card className="min-w-[200px] border-2 border-purple-500">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium flex items-center gap-2">
          <Wrench className="w-4 h-4 text-purple-500" />
          MCP Tool
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="text-xs font-bold mb-1">{data.toolName || 'Select Tool'}</div>
        <div className="text-xs text-muted-foreground">
          {data.serverName ? `@${data.serverName}` : 'No server selected'}
        </div>
      </CardContent>
      <Handle type="target" position={Position.Top} className="w-3 h-3 bg-purple-500" />
      <Handle type="source" position={Position.Bottom} className="w-3 h-3 bg-purple-500" />
    </Card>
  );
};

export default memo(ToolNode);
