import { memo } from 'react';
import { Handle, Position, NodeProps } from 'reactflow';

const EndNode = () => {
  return (
    <div className="px-4 py-2 shadow-md rounded-md bg-white border-2 border-red-500 w-32 flex justify-center items-center">
      <Handle type="target" position={Position.Top} className="w-16 !bg-red-500" />
      <div className="font-bold text-sm text-red-700">END</div>
    </div>
  );
};

export default memo(EndNode);
