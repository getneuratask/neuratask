import React, { useEffect } from 'react';
import { Button, Typography, Space, Row, Col } from 'antd';
import { PlusOutlined, ReloadOutlined } from '@ant-design/icons';
import { useKanban } from './useKanban';
import KanbanColumn from './KanbanColumn';
import CreateTaskModal from './CreateTaskModal';
import ProjectInfo from './ProjectInfo';

const { Title } = Typography;

const Kanban: React.FC = () => {
  const {
    columns,
    isLoading,
    isModalVisible,
    projectInfo,
    loadTasks,
    createTask,
    deleteTask,
    moveTaskLeft,
    moveTaskRight,
    openModal,
    closeModal
  } = useKanban();

  useEffect(() => {
    loadTasks();
  }, [loadTasks]);

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-6">
          <Title level={2}>Kanban Board</Title>
          
          <div className="mt-4">
            <Space>
              <Button 
                type="primary" 
                icon={<PlusOutlined />}
                onClick={openModal}
                size="large"
              >
                Nueva Tarea
              </Button>
              
              <Button 
                icon={<ReloadOutlined />}
                onClick={loadTasks}
                loading={isLoading}
                size="large"
              >
                Recargar
              </Button>
            </Space>
          </div>
        </div>

        {/* Project Information */}
        <ProjectInfo project={projectInfo} isLoading={isLoading} />

        {/* Kanban Board */}
        <Row gutter={[16, 16]}>
          {columns.map((column) => (
            <Col key={column.id} xs={24} md={8}>
              <KanbanColumn
                column={column}
                onMoveLeft={moveTaskLeft}
                onMoveRight={moveTaskRight}
                onDelete={deleteTask}
              />
            </Col>
          ))}
        </Row>

        {/* Create Task Modal */}
        <CreateTaskModal
          visible={isModalVisible}
          onCancel={closeModal}
          onCreate={createTask}
        />
      </div>
    </div>
  );
};

export default Kanban;