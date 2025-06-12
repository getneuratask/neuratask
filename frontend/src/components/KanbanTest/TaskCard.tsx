import React from 'react';
import { Card, Button, Tag, Typography, Tooltip, Popconfirm } from 'antd';
import { 
  ArrowLeftOutlined, 
  ArrowRightOutlined, 
  DeleteOutlined,
  ExclamationCircleOutlined 
} from '@ant-design/icons';
import type { TaskCardProps } from './Types';
import { getPriorityColor, getPriorityText, formatDate, formatDateTime, isTaskOverdue } from './utils';

const { Text } = Typography;

const TaskCard: React.FC<TaskCardProps> = ({ task, onMoveLeft, onMoveRight, onDelete }) => {
  return (
    <Card
      size="small"
      className="shadow-sm hover:shadow-md transition-shadow cursor-pointer border"
      bodyStyle={{ padding: '12px' }}
      actions={[
        <Tooltip title="Mover a la izquierda">
          <Button
            type="text"
            icon={<ArrowLeftOutlined />}
            onClick={() => onMoveLeft(task)}
            disabled={task.status === 'TODO'}
            size="small"
          />
        </Tooltip>,
        <Tooltip title="Mover a la derecha">
          <Button
            type="text"
            icon={<ArrowRightOutlined />}
            onClick={() => onMoveRight(task)}
            disabled={task.status === 'DONE'}
            size="small"
          />
        </Tooltip>,
        <Popconfirm
          title="¿Eliminar tarea?"
          description="¿Estás seguro de que quieres eliminar esta tarea?"
          onConfirm={() => onDelete(task.id)}
          okText="Sí"
          cancelText="No"
          icon={<ExclamationCircleOutlined style={{ color: 'red' }} />}
        >
          <Button
            type="text"
            danger
            icon={<DeleteOutlined />}
            size="small"
          />
        </Popconfirm>
      ]}
    >
      {/* Task Title */}
      <div className="mb-2">
        <Text strong className="text-sm leading-tight block">
          {task.title}
        </Text>
        {task.parent_task_id && (
          <Tag color="blue" className="mt-1">
            Subtarea
          </Tag>
        )}
      </div>
      
      {/* Task Description */}
      {task.description && (
        <div className="mb-3">
          <Text type="secondary" className="text-xs">
            {task.description.length > 80 
              ? `${task.description.substring(0, 80)}...` 
              : task.description
            }
          </Text>
        </div>
      )}

      {/* Priority and Status Tags */}
      <div className="flex items-center justify-between mb-2">
        <Tag color={getPriorityColor(task.priority)} className="text-xs">
          {getPriorityText(task.priority)}
        </Tag>
        {task.is_recurring && (
          <Tag color="purple" className="text-xs">
            🔄 Recurrente
          </Tag>
        )}
      </div>

      {/* Dates Information */}
      <div className="mb-2 text-xs">
        {task.start_date && (
          <div className="flex justify-between items-center mb-1">
            <span className="text-gray-500">Inicio:</span>
            <span>{formatDate(task.start_date)}</span>
          </div>
        )}
        {task.due_date && (
          <div className="flex justify-between items-center mb-1">
            <span className="text-gray-500">Vencimiento:</span>
            <span className={
              isTaskOverdue(task.due_date, task.status)
                ? 'text-red-500 font-bold'
                : 'text-gray-700'
            }>
              {formatDate(task.due_date)}
            </span>
          </div>
        )}
        {task.completed_at && (
          <div className="flex justify-between items-center mb-1">
            <span className="text-gray-500">Completada:</span>
            <span className="text-green-600">{formatDateTime(task.completed_at)}</span>
          </div>
        )}
      </div>

      {/* Assignment and Creation Info */}
      <div className="mb-2 text-xs">
        {task.assigned_to && (
          <div className="flex justify-between items-center mb-1">
            <span className="text-gray-500">Asignada a:</span>
            <Tag color="geekblue">
              {task.assigned_to.slice(0, 8)}...
            </Tag>
          </div>
        )}
        {task.created_by && (
          <div className="flex justify-between items-center mb-1">
            <span className="text-gray-500">Creada por:</span>
            <Tag color="cyan">
              {task.created_by.slice(0, 8)}...
            </Tag>
          </div>
        )}
      </div>

      {/* Recurrence Rule */}
      {task.recurrence_rule && (
        <div className="mb-2">
          <Tooltip title={task.recurrence_rule}>
            <Tag color="purple" className="text-xs w-full text-center">
              Regla: {task.recurrence_rule.length > 20 
                ? `${task.recurrence_rule.substring(0, 20)}...` 
                : task.recurrence_rule
              }
            </Tag>
          </Tooltip>
        </div>
      )}

      {/* Creation and Update Timestamps */}
      <div className="text-xs text-gray-400 border-t pt-2 mt-2">
        <div className="flex justify-between items-center mb-1">
          <span>Creada:</span>
          <span>{formatDateTime(task.created_at)}</span>
        </div>
        {task.updated_at && task.updated_at !== task.created_at && (
          <div className="flex justify-between items-center mb-1">
            <span>Actualizada:</span>
            <span>{formatDateTime(task.updated_at)}</span>
          </div>
        )}
        <div className="text-center mt-1">
          <Text type="secondary" className="text-xs">
            ID: {task.id.slice(0, 8)}...
          </Text>
        </div>
      </div>
    </Card>
  );
};

export default TaskCard;