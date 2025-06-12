import React from 'react';
import { Card, Badge, Typography, Space } from 'antd';
import type { KanbanColumnProps } from './Types';
import { getColumnIcon } from './Constants';
import TaskCard from './TaskCard';

const { Text } = Typography;

const KanbanColumn: React.FC<KanbanColumnProps> = ({ 
  column, 
  onMoveLeft, 
  onMoveRight, 
  onDelete 
}) => {
  return (
    <Card
      title={
        <div className="flex items-center justify-between">
          <Space>
            <span>{getColumnIcon(column.id)}</span>
            <Text strong>{column.title}</Text>
          </Space>
          <Badge count={column.tasks.length} style={{ backgroundColor: '#52c41a' }} />
        </div>
      }
      style={{ backgroundColor: column.color }}
      className="min-h-[600px]"
      bodyStyle={{ padding: '12px' }}
    >
      <div className="space-y-3">
        {column.tasks.map((task) => (
          <TaskCard
            key={task.id}
            task={task}
            onMoveLeft={onMoveLeft}
            onMoveRight={onMoveRight}
            onDelete={onDelete}
          />
        ))}
        
        {column.tasks.length === 0 && (
          <div className="text-center py-8 text-gray-400">
            <Text type="secondary">No hay tareas</Text>
          </div>
        )}
      </div>
    </Card>
  );
};

export default KanbanColumn;