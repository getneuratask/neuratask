import type { Column } from './Types';

// Hardcoded project ID for testing
export const HARDCODED_PROJECT_ID = 'c41b801f-e307-4100-b108-6b8d3a70efd9';
export const HARDCODED_USER_ID = '90f77778-257a-4597-a2df-6a29cbf6aa6c';

export const initialColumns: Column[] = [
  {
    id: 'TODO',
    title: 'Por Hacer',
    color: '#f0f0f0',
    tasks: []
  },
  {
    id: 'DOING',
    title: 'En Progreso',
    color: '#e6f4ff',
    tasks: []
  },
  {
    id: 'DONE',
    title: 'Completado',
    color: '#f6ffed',
    tasks: []
  }
];

export const getColumnIcon = (columnId: string): string => {
  switch (columnId) {
    case 'TODO': return '📝';
    case 'DOING': return '⚡';
    case 'DONE': return '✅';
    default: return '📋';
  }
};