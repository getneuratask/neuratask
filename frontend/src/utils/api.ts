import axios from 'axios';
import type { AxiosResponse } from 'axios';

// Variables de entorno para Vite (VITE_ prefix)
const API_BASE_URL = 'http://localhost:8000/api/v1';
const AI_SERVICES_URL = 'http://localhost:47337';


// Función auxiliar para generar UUID simple (sin dependencia externa)
const generateUUID = (): string => {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0;
    const v = c === 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
};

export const api = {
  // ==================== AI SERVICES ====================
  chatbot: async (message: string): Promise<ChatbotResponse> => {
    try {
      const url = `${AI_SERVICES_URL}/chat`;
      const uuid = generateUUID();

      const response: AxiosResponse<ChatbotResponse> = await axios({
        method: 'POST',
        url: url,
        data: { 
          message,
          uuid 
        },
        headers: {
          'Content-Type': 'application/json',
        },
      });

      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        console.error('Chatbot API Error:', {
          message: error.message,
          status: error.response?.status,
          data: error.response?.data,
        });
      } else {
        console.error('Unexpected error:', error);
      }
      throw error;
    }
  },

  // ==================== GENERIC HTTP METHODS ====================

  get: async <T = any>(endpoint: string, params: Record<string, any> = {}): Promise<AxiosResponse<T>> => {
    try {
      const url = `${API_BASE_URL}${endpoint}`;

      const response = await axios({
        method: 'GET',
        url: url,
        params: params,
        headers: {
          'Content-Type': 'application/json',
        },
      });

      return response;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        console.error('API Error:', {
          message: error.message,
          status: error.response?.status,
          data: error.response?.data,
        });
      } else {
        console.error('Unexpected error:', error);
      }
      throw error;
    }
  },

  post: async <T = any>(endpoint: string, data: any): Promise<AxiosResponse<T>> => {
    try {
      const url = `${API_BASE_URL}${endpoint}`;

      const response = await axios({
        method: 'POST',
        url: url,
        data: data,
        headers: {
          'Content-Type': 'application/json',
        },
      });

      return response;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        console.error('API Error:', {
          message: error.message,
          status: error.response?.status,
          data: error.response?.data,
        });
      } else {
        console.error('Unexpected error:', error);
      }
      throw error;
    }
  },

  update: async <T = any>(endpoint: string, data: any): Promise<AxiosResponse<T>> => {
    try {
      const url = `${API_BASE_URL}${endpoint}`;

      const response = await axios({
        method: 'PUT',
        url: url,
        data: data,
        headers: {
          'Content-Type': 'application/json',
        },
      });

      return response;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        console.error('API Error:', {
          message: error.message,
          status: error.response?.status,
          data: error.response?.data,
        });
      } else {
        console.error('Unexpected error:', error);
      }
      throw error;
    }
  },

  delete: async <T = any>(endpoint: string): Promise<AxiosResponse<T>> => {
    try {
      const url = `${API_BASE_URL}${endpoint}`;

      const response = await axios({
        method: 'DELETE',
        url: url,
        headers: {
          'Content-Type': 'application/json',
        },
      });

      return response;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        console.error('API Error:', {
          message: error.message,
          status: error.response?.status,
          data: error.response?.data,
        });
      } else {
        console.error('Unexpected error:', error);
      }
      throw error;
    }
  },

  // ==================== NEURATASK SPECIFIC ENDPOINTS ====================

  // Users
  users: {
    getAll: (): Promise<AxiosResponse<User[]>> => api.get<User[]>('/users'),
    getById: (id: string | number): Promise<AxiosResponse<User>> => api.get<User>(`/users/${id}`),
    create: (userData: Partial<User>): Promise<AxiosResponse<User>> => api.post<User>('/users', userData),
    update: (id: string | number, userData: Partial<User>): Promise<AxiosResponse<User>> => api.update<User>(`/users/${id}`, userData),
    delete: (id: string | number): Promise<AxiosResponse<void>> => api.delete<void>(`/users/${id}`),
  },

  // Workspaces
  workspaces: {
    getAll: (): Promise<AxiosResponse<Workspace[]>> => api.get<Workspace[]>('/workspaces'),
    getById: (id: string | number): Promise<AxiosResponse<Workspace>> => api.get<Workspace>(`/workspaces/${id}`),
    create: (workspaceData: Partial<Workspace>): Promise<AxiosResponse<Workspace>> => api.post<Workspace>('/workspaces', workspaceData),
    update: (id: string | number, workspaceData: Partial<Workspace>): Promise<AxiosResponse<Workspace>> => api.update<Workspace>(`/workspaces/${id}`, workspaceData),
    delete: (id: string | number): Promise<AxiosResponse<void>> => api.delete<void>(`/workspaces/${id}`),
    getProjects: (id: string | number): Promise<AxiosResponse<Project[]>> => api.get<Project[]>(`/workspaces/${id}/projects`),
  },

  // Projects
  projects: {
    getAll: (): Promise<AxiosResponse<Project[]>> => api.get<Project[]>('/projects'),
    getById: (id: string | number): Promise<AxiosResponse<Project>> => api.get<Project>(`/projects/${id}`),
    create: (projectData: Partial<Project>): Promise<AxiosResponse<Project>> => api.post<Project>('/projects', projectData),
    update: (id: string | number, projectData: Partial<Project>): Promise<AxiosResponse<Project>> => api.update<Project>(`/projects/${id}`, projectData),
    delete: (id: string | number): Promise<AxiosResponse<void>> => api.delete<void>(`/projects/${id}`),
    getTasks: (id: string | number): Promise<AxiosResponse<Task[]>> => api.get<Task[]>(`/workspaces/${id}/tasks`),
  },

  // Tasks
  tasks: {
    getAll: (): Promise<AxiosResponse<Task[]>> => api.get<Task[]>('/tasks'),
    getById: (id: string | number): Promise<AxiosResponse<Task>> => api.get<Task>(`/tasks/${id}`),
    getByProject: (projectId: string | number): Promise<AxiosResponse<Task[]>> => api.get<Task[]>(`/tasks/project/${projectId}`),
    create: (taskData: Partial<Task>): Promise<AxiosResponse<Task>> => api.post<Task>('/tasks', taskData),
    update: (id: string | number, taskData: Partial<Task>): Promise<AxiosResponse<Task>> => api.update<Task>(`/tasks/${id}`, taskData),
    delete: (id: string | number): Promise<AxiosResponse<void>> => api.delete<void>(`/tasks/${id}`),
    updateStatus: (id: string | number, status: string): Promise<AxiosResponse<Task>> => api.update<Task>(`/tasks/${id}/status`, { status }),
    getComments: (id: string | number): Promise<AxiosResponse<Comment[]>> => api.get<Comment[]>(`/tasks/${id}/comments`),
    addComment: (id: string | number, commentData: Partial<Comment>): Promise<AxiosResponse<Comment>> => api.post<Comment>(`/tasks/${id}/comments`, commentData),
  },

  // Labels
  labels: {
    getAll: (): Promise<AxiosResponse<Label[]>> => api.get<Label[]>('/labels'),
    getById: (id: string | number): Promise<AxiosResponse<Label>> => api.get<Label>(`/labels/${id}`),
    create: (labelData: Partial<Label>): Promise<AxiosResponse<Label>> => api.post<Label>('/labels', labelData),
    update: (id: string | number, labelData: Partial<Label>): Promise<AxiosResponse<Label>> => api.update<Label>(`/labels/${id}`, labelData),
    delete: (id: string | number): Promise<AxiosResponse<void>> => api.delete<void>(`/labels/${id}`),
  },

  // Comments
  comments: {
    getAll: (): Promise<AxiosResponse<Comment[]>> => api.get<Comment[]>('/comments'),
    getById: (id: string | number): Promise<AxiosResponse<Comment>> => api.get<Comment>(`/comments/${id}`),
    create: (commentData: Partial<Comment>): Promise<AxiosResponse<Comment>> => api.post<Comment>('/comments', commentData),
    update: (id: string | number, commentData: Partial<Comment>): Promise<AxiosResponse<Comment>> => api.update<Comment>(`/comments/${id}`, commentData),
    delete: (id: string | number): Promise<AxiosResponse<void>> => api.delete<void>(`/comments/${id}`),
  },

  // Reminders
  reminders: {
    getAll: (): Promise<AxiosResponse<Reminder[]>> => api.get<Reminder[]>('/reminders'),
    getById: (id: string | number): Promise<AxiosResponse<Reminder>> => api.get<Reminder>(`/reminders/${id}`),
    create: (reminderData: Partial<Reminder>): Promise<AxiosResponse<Reminder>> => api.post<Reminder>('/reminders', reminderData),
    update: (id: string | number, reminderData: Partial<Reminder>): Promise<AxiosResponse<Reminder>> => api.update<Reminder>(`/reminders/${id}`, reminderData),
    delete: (id: string | number): Promise<AxiosResponse<void>> => api.delete<void>(`/reminders/${id}`),
  },

  // Activity Logs
  activityLogs: {
    getAll: (): Promise<AxiosResponse<ActivityLog[]>> => api.get<ActivityLog[]>('/activity-logs'),
    getById: (id: string | number): Promise<AxiosResponse<ActivityLog>> => api.get<ActivityLog>(`/activity-logs/${id}`),
    getByTask: (taskId: string | number): Promise<AxiosResponse<ActivityLog[]>> => api.get<ActivityLog[]>(`/activity-logs/task/${taskId}`),
    getByUser: (userId: string | number): Promise<AxiosResponse<ActivityLog[]>> => api.get<ActivityLog[]>(`/activity-logs/user/${userId}`),
  },

  // ==================== HEALTH CHECK ====================
  health: {
    check: (): Promise<AxiosResponse<{ status: string }>> => api.get<{ status: string }>('/health'),
    root: (): Promise<AxiosResponse<{ message: string }>> => api.get<{ message: string }>('/'),
  },
};

// Interfaces para tipos de datos
export interface User {
  id: string;
  auth0_sub: string;
  name: string;
  email?: string;
  avatar_url?: string;
  created_at?: string;
  updated_at?: string;
}

export interface Workspace {
  id: string;
  owner_id?: string;
  name: string;
  created_at?: string;
}

export interface Project {
  id: string;
  workspace_id?: string;
  name: string;
  color?: string;
  sort_order?: number;
  is_archived?: boolean;
  created_at?: string;
  updated_at?: string;
}

export interface Task {
  id: string;
  project_id?: string;
  parent_task_id?: string;
  title: string;
  description?: string;
  status?: 'TODO' | 'DOING' | 'DONE';
  priority?: number; // 1-4 where 1 is highest priority
  due_date?: string;
  start_date?: string;
  completed_at?: string;
  created_by?: string;
  assigned_to?: string;
  is_recurring?: boolean;
  recurrence_rule?: string;
  created_at?: string;
  updated_at?: string;
}

export interface Comment {
  id: string;
  task_id?: string;
  author_id?: string;
  body: string;
  created_at?: string;
  edited_at?: string;
}

export interface Label {
  id: string;
  workspace_id?: string;
  name: string;
  color?: string;
}

export interface Reminder {
  id: string;
  task_id?: string;
  user_id?: string;
  remind_at: string;
  channel?: 'PUSH' | 'EMAIL' | 'WEB';
}

export interface ActivityLog {
  id: string;
  entity_type: string;
  entity_id: string;
  action: string;
  actor_id?: string;
  payload?: any;
  created_at?: string;
}

export interface TaskLabel {
  task_id: string;
  label_id: string;
}

export interface ChatbotResponse {
  response: string;
  uuid: string;
  timestamp?: string;
}

export interface ApiResponse<T = any> {
  data: T;
  message?: string;
  status?: string;
}

