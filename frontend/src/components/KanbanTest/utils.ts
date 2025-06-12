export const getPriorityColor = (priority?: number): string => {
  switch (priority) {
    case 1: return 'red';     // Crítica
    case 2: return 'orange';  // Alta
    case 3: return 'yellow';  // Media
    case 4: return 'green';   // Baja
    default: return 'default';
  }
};

export const getPriorityText = (priority?: number): string => {
  switch (priority) {
    case 1: return 'Crítica';
    case 2: return 'Alta';
    case 3: return 'Media';
    case 4: return 'Baja';
    default: return 'Normal';
  }
};

export const formatDate = (dateString?: string): string => {
  if (!dateString) return 'No definida';
  try {
    return new Date(dateString).toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  } catch {
    return 'Fecha inválida';
  }
};

export const formatDateTime = (dateString?: string): string => {
  if (!dateString) return 'No definida';
  try {
    return new Date(dateString).toLocaleString('es-ES', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  } catch {
    return 'Fecha inválida';
  }
};

export const isTaskOverdue = (dueDate?: string, status?: string): boolean => {
  if (!dueDate || status === 'DONE') return false;
  return new Date(dueDate) < new Date();
};