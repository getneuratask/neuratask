import axios from 'axios';

// Variables de entorno para Vite (VITE_ prefix)
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080/api/v1';
const AI_SERVICES_URL = import.meta.env.VITE_AI_SERVICES_URL || 'http://localhost:8000';

// Función auxiliar para generar UUID simple (sin dependencia externa)
const generateUUID = () => {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0;
    const v = c === 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
};

export const api = {
  // ==================== AI SERVICES ====================
  chatbot: async (message) => {
    try {
      const url = `${AI_SERVICES_URL}/chat`;
      const uuid = generateUUID();

      const response = await axios({
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
      if (axios.isAxiosError?.(error)) {
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

  get: async (endpoint, params = {}) => {
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
      if (axios.isAxiosError?.(error)) {
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

  post: async (endpoint, data) => {
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
      if (axios.isAxiosError?.(error)) {
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

  update: async (endpoint, data) => {
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
      if (axios.isAxiosError?.(error)) {
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

  delete: async (endpoint) => {
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
      if (axios.isAxiosError?.(error)) {
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
    getAll: () => api.get('/users'),
    getById: (id) => api.get(`/users/${id}`),
    create: (userData) => api.post('/users', userData),
    update: (id, userData) => api.update(`/users/${id}`, userData),
    delete: (id) => api.delete(`/users/${id}`),
  },

  // Workspaces
  workspaces: {
    getAll: () => api.get('/workspaces'),
    getById: (id) => api.get(`/workspaces/${id}`),
    create: (workspaceData) => api.post('/workspaces', workspaceData),
    update: (id, workspaceData) => api.update(`/workspaces/${id}`, workspaceData),
    delete: (id) => api.delete(`/workspaces/${id}`),
    getProjects: (id) => api.get(`/workspaces/${id}/projects`),
  },

  // Projects
  projects: {
    getAll: () => api.get('/projects'),
    getById: (id) => api.get(`/projects/${id}`),
    create: (projectData) => api.post('/projects', projectData),
    update: (id, projectData) => api.update(`/projects/${id}`, projectData),
    delete: (id) => api.delete(`/projects/${id}`),
    getTasks: (id) => api.get(`/projects/${id}/tasks`),
  },

  // Tasks
  tasks: {
    getAll: () => api.get('/tasks'),
    getById: (id) => api.get(`/tasks/${id}`),
    create: (taskData) => api.post('/tasks', taskData),
    update: (id, taskData) => api.update(`/tasks/${id}`, taskData),
    delete: (id) => api.delete(`/tasks/${id}`),
    updateStatus: (id, status) => api.update(`/tasks/${id}/status`, { status }),
    getComments: (id) => api.get(`/tasks/${id}/comments`),
    addComment: (id, commentData) => api.post(`/tasks/${id}/comments`, commentData),
  },

  // Labels
  labels: {
    getAll: () => api.get('/labels'),
    getById: (id) => api.get(`/labels/${id}`),
    create: (labelData) => api.post('/labels', labelData),
    update: (id, labelData) => api.update(`/labels/${id}`, labelData),
    delete: (id) => api.delete(`/labels/${id}`),
  },

  // Comments
  comments: {
    getAll: () => api.get('/comments'),
    getById: (id) => api.get(`/comments/${id}`),
    create: (commentData) => api.post('/comments', commentData),
    update: (id, commentData) => api.update(`/comments/${id}`, commentData),
    delete: (id) => api.delete(`/comments/${id}`),
  },

  // Reminders
  reminders: {
    getAll: () => api.get('/reminders'),
    getById: (id) => api.get(`/reminders/${id}`),
    create: (reminderData) => api.post('/reminders', reminderData),
    update: (id, reminderData) => api.update(`/reminders/${id}`, reminderData),
    delete: (id) => api.delete(`/reminders/${id}`),
  },

  // Activity Logs
  activityLogs: {
    getAll: () => api.get('/activity-logs'),
    getById: (id) => api.get(`/activity-logs/${id}`),
    getByTask: (taskId) => api.get(`/activity-logs/task/${taskId}`),
    getByUser: (userId) => api.get(`/activity-logs/user/${userId}`),
  },

  // ==================== HEALTH CHECK ====================
  health: {
    check: () => api.get('/health'),
    root: () => api.get('/'),
  },
};