import type { Task } from '@/utils/api';

export interface Column {
  id: string;
  title: string;
  color: string;
  tasks: Task[];
}

export interface CreateTaskFormData {
  title: string;
  description?: string;
  status: 'TODO' | 'DOING' | 'DONE';
  priority: number;
}

export interface KanbanState {
  columns: Column[];
  isLoading: boolean;
  isModalVisible: boolean;
}

export interface TaskCardProps {
  task: Task;
  onMoveLeft: (task: Task) => void;
  onMoveRight: (task: Task) => void;
  onDelete: (taskId: string) => void;
}

export interface CreateTaskModalProps {
  visible: boolean;
  onCancel: () => void;
  onCreate: (values: CreateTaskFormData) => void;
}

export interface KanbanColumnProps {
  column: Column;
  onMoveLeft: (task: Task) => void;
  onMoveRight: (task: Task) => void;
  onDelete: (taskId: string) => void;
}