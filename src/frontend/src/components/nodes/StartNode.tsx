import { memo } from 'react';
import { Handle, Position, NodeProps } from 'reactflow';

const StartNode = () => {
  return (
    <div className="px-4 py-2 shadow-md rounded-md bg-white border-2 border-purple-500 w-32 flex justify-center items-center">
      <div className="font-bold text-sm text-purple-700">START</div>
      <Handle type="source" position={Position.Bottom} className="w-16 !bg-purple-500" />
    </div>
  );
};

export default memo(StartNode);
