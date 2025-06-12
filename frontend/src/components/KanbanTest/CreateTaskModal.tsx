import React from 'react';
import { Modal, Form, Input, Select, Button, Space, Row, Col } from 'antd';
import type { CreateTaskModalProps, CreateTaskFormData } from './Types';

const { TextArea } = Input;
const { Option } = Select;

const CreateTaskModal: React.FC<CreateTaskModalProps> = ({ 
  visible, 
  onCancel, 
  onCreate 
}) => {
  const [form] = Form.useForm();

  const handleSubmit = (values: CreateTaskFormData) => {
    onCreate(values);
  };

  const handleCancel = () => {
    form.resetFields();
    onCancel();
  };

  return (
    <Modal
      title="Nueva Tarea"
      open={visible}
      onCancel={handleCancel}
      footer={null}
      width={600}
    >
      <Form
        form={form}
        layout="vertical"
        onFinish={handleSubmit}
        initialValues={{ priority: 3, status: 'TODO' }}
      >
        <Form.Item
          label="Título"
          name="title"
          rules={[{ required: true, message: 'Por favor ingresa el título' }]}
        >
          <Input placeholder="Título de la tarea" />
        </Form.Item>

        <Form.Item
          label="Descripción"
          name="description"
        >
          <TextArea 
            rows={3} 
            placeholder="Descripción de la tarea (opcional)" 
          />
        </Form.Item>

        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              label="Estado"
              name="status"
            >
              <Select>
                <Option value="TODO">Por Hacer</Option>
                <Option value="DOING">En Progreso</Option>
                <Option value="DONE">Completado</Option>
              </Select>
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              label="Prioridad"
              name="priority"
            >
              <Select>
                <Option value={1}>Crítica</Option>
                <Option value={2}>Alta</Option>
                <Option value={3}>Media</Option>
                <Option value={4}>Baja</Option>
              </Select>
            </Form.Item>
          </Col>
        </Row>

        <Form.Item className="mb-0 text-right">
          <Space>
            <Button onClick={handleCancel}>
              Cancelar
            </Button>
            <Button type="primary" htmlType="submit">
              Crear Tarea
            </Button>
          </Space>
        </Form.Item>
      </Form>
    </Modal>
  );
};

export default CreateTaskModal;