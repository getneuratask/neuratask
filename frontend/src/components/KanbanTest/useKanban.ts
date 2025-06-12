import { useState, useCallback, useRef } from 'react';
import { message } from 'antd';
import { api, type Task, type Project } from '@/utils/api';
import type { Column, CreateTaskFormData } from './Types';
import { initialColumns, HARDCODED_PROJECT_ID, HARDCODED_USER_ID } from './Constants';

export const useKanban = () => {
  const [columns, setColumns] = useState<Column[]>(initialColumns);
  const [isLoading, setIsLoading] = useState(true);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [projectInfo, setProjectInfo] = useState<Project | null>(null);
  const loadingRef = useRef(false);

  // Load project information
  const loadProjectInfo = useCallback(async () => {
    try {
      const response = await api.projects.getById(HARDCODED_PROJECT_ID);
      setProjectInfo(response.data);
    } catch (err: any) {
      console.error('Error loading project info:', err);
      message.error('Error al cargar información del proyecto: ' + (err.response?.data?.detail || err.message));
    }
  }, []);

  // Load tasks from API
  const loadTasks = useCallback(async () => {
    // Prevent concurrent requests
    if (loadingRef.current) return;
    
    try {
      loadingRef.current = true;
      setIsLoading(true);
      
      // Load project info and tasks in parallel
      const [projectResponse, tasksResponse] = await Promise.all([
        api.projects.getById(HARDCODED_PROJECT_ID),
        api.tasks.getByProject(HARDCODED_PROJECT_ID)
      ]);
      
      setProjectInfo(projectResponse.data);
      const tasks: Task[] = tasksResponse.data;
      
      // Group tasks by status
      const updatedColumns = initialColumns.map(column => ({
        ...column,
        tasks: tasks.filter(task => task.status === column.id)
      }));
      
      setColumns(updatedColumns);
      message.success('Proyecto y tareas cargados correctamente');
    } catch (err: any) {
      console.error('Error loading tasks:', err);
      message.error('Error al cargar las tareas: ' + (err.response?.data?.detail || err.message));
    } finally {
      setIsLoading(false);
      loadingRef.current = false;
    }
  }, []);

  // Update local state without API call
  const updateLocalTaskStatus = useCallback((taskId: string, newStatus: 'TODO' | 'DOING' | 'DONE') => {
    setColumns(prevColumns => {
      // Find the task and remove it from current column
      let taskToMove: Task | null = null;
      const updatedColumns = prevColumns.map(column => ({
        ...column,
        tasks: column.tasks.filter(task => {
          if (task.id === taskId) {
            taskToMove = { ...task, status: newStatus };
            return false;
          }
          return true;
        })
      }));

      // Add task to new column if found
      if (taskToMove) {
        const targetColumn = updatedColumns.find(col => col.id === newStatus);
        if (targetColumn) {
          targetColumn.tasks.push(taskToMove);
        }
      }

      return updatedColumns;
    });
  }, []);

  // Update task status (optimistic update)
  const updateTaskStatus = useCallback(async (taskId: string, newStatus: 'TODO' | 'DOING' | 'DONE') => {
    try {
      // Optimistic update - update UI immediately
      updateLocalTaskStatus(taskId, newStatus);
      
      // Then update in backend
      await api.tasks.update(taskId, { status: newStatus });
      message.success('Tarea actualizada correctamente');
    } catch (err: any) {
      console.error('Error updating task:', err);
      message.error('Error al actualizar la tarea: ' + (err.response?.data?.detail || err.message));
      // Revert optimistic update by reloading
      await loadTasks();
    }
  }, [updateLocalTaskStatus, loadTasks]);

  // Create new task (optimistic update)
  const createTask = useCallback(async (values: CreateTaskFormData) => {
    try {
      const taskData: Partial<Task> = {
        title: values.title,
        description: values.description || undefined,
        project_id: HARDCODED_PROJECT_ID,
        priority: values.priority,
        status: values.status,
        created_by: HARDCODED_USER_ID
      };

      const response = await api.tasks.create(taskData);
      const newTask: Task = response.data;
      
      // Add new task to local state
      setColumns(prevColumns => 
        prevColumns.map(column => 
          column.id === newTask.status 
            ? { ...column, tasks: [...column.tasks, newTask] }
            : column
        )
      );
      
      message.success('Tarea creada correctamente');
      setIsModalVisible(false);
    } catch (err: any) {
      console.error('Error creating task:', err);
      message.error('Error al crear la tarea: ' + (err.response?.data?.detail || err.message));
    }
  }, []);

  // Delete task (optimistic update)
  const deleteTask = useCallback(async (taskId: string) => {
    try {
      // Optimistic update - remove from UI immediately
      setColumns(prevColumns => 
        prevColumns.map(column => ({
          ...column,
          tasks: column.tasks.filter(task => task.id !== taskId)
        }))
      );
      
      await api.tasks.delete(taskId);
      message.success('Tarea eliminada correctamente');
    } catch (err: any) {
      console.error('Error deleting task:', err);
      message.error('Error al eliminar la tarea: ' + (err.response?.data?.detail || err.message));
      // Revert optimistic update by reloading
      await loadTasks();
    }
  }, [loadTasks]);

  // Move task to previous column
  const moveTaskLeft = useCallback(async (task: Task) => {
    let newStatus: 'TODO' | 'DOING' | 'DONE';
    if (task.status === 'DONE') newStatus = 'DOING';
    else if (task.status === 'DOING') newStatus = 'TODO';
    else return;

    await updateTaskStatus(task.id, newStatus);
  }, [updateTaskStatus]);

  // Move task to next column
  const moveTaskRight = useCallback(async (task: Task) => {
    let newStatus: 'TODO' | 'DOING' | 'DONE';
    if (task.status === 'TODO') newStatus = 'DOING';
    else if (task.status === 'DOING') newStatus = 'DONE';
    else return;

    await updateTaskStatus(task.id, newStatus);
  }, [updateTaskStatus]);

  // Modal handlers
  const openModal = useCallback(() => setIsModalVisible(true), []);
  const closeModal = useCallback(() => setIsModalVisible(false), []);

  return {
    // State
    columns,
    isLoading,
    isModalVisible,
    projectInfo,
    
    // Actions
    loadTasks,
    loadProjectInfo,
    createTask,
    deleteTask,
    moveTaskLeft,
    moveTaskRight,
    openModal,
    closeModal
  };
};