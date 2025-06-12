import React from 'react';
import { Card, Tag, Typography, Space, Descriptions, Skeleton } from 'antd';
import { ProjectOutlined, CalendarOutlined, UserOutlined } from '@ant-design/icons';
import type { Project } from '@/utils/api';
import { formatDateTime } from './utils';

const { Title, Text } = Typography;

interface ProjectInfoProps {
  project: Project | null;
  isLoading: boolean;
}

const ProjectInfo: React.FC<ProjectInfoProps> = ({ project, isLoading }) => {
    if (isLoading) {
        return (
            <div className="mb-6 bg-white shadow rounded p-4">
                <Skeleton active paragraph={{ rows: 3 }} />
            </div>
        );
    }

    if (!project) {
        return (
            <div className="mb-6 bg-white shadow rounded p-4">
                <Text type="secondary">No se pudo cargar la información del proyecto</Text>
            </div>
        );
    }

    return (
        <div 
            className={`mb-6 shadow rounded p-4 ${project.color ? '' : 'bg-white'}`}
            style={{ backgroundColor: project.color || '#ffffff' }}
        >
            <div className="flex items-start justify-between">
                <div className="flex-1">
                    <div className="flex flex-col space-y-2 w-full">
                        <div className="flex items-center space-x-3">
                            <ProjectOutlined className="text-xl" />
                            <Title level={3} className="mb-0">
                                {project.name}
                            </Title>
                            {project.is_archived && (
                                <Tag color="orange">Archivado</Tag>
                            )}
                        </div>

                        <div className="mt-4 grid grid-cols-2 gap-y-2 text-sm">
                            <div className="col-span-2 font-bold text-gray-600 flex items-center">
                                <ProjectOutlined className="mr-2" /> ID del Proyecto:
                                <Text code className="ml-2">{project.id}</Text>
                            </div>

                            {project.workspace_id && (
                                <div className="col-span-2 font-bold text-gray-600 flex items-center">
                                    <UserOutlined className="mr-2" /> Workspace ID:
                                    <Text code className="ml-2">{project.workspace_id}</Text>
                                </div>
                            )}

                            <div className="font-bold text-gray-600 flex items-center">
                                <CalendarOutlined className="mr-2" /> Creado:
                                <span className="ml-2">{formatDateTime(project.created_at)}</span>
                            </div>

                            {project.updated_at && project.updated_at !== project.created_at && (
                                <div className="font-bold text-gray-600 flex items-center">
                                    <CalendarOutlined className="mr-2" /> Actualizado:
                                    <span className="ml-2">{formatDateTime(project.updated_at)}</span>
                                </div>
                            )}

                            {project.sort_order !== undefined && (
                                <div className="font-bold text-gray-600">
                                    Orden:
                                    <span className="ml-2">{project.sort_order}</span>
                                </div>
                            )}

                            {project.color && (
                                <div className="font-bold text-gray-600 flex items-center">
                                    Color:
                                    <div 
                                        className="w-4 h-4 rounded border ml-2"
                                        style={{ backgroundColor: project.color }}
                                    ></div>
                                    <Text code className="ml-2">{project.color}</Text>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ProjectInfo;