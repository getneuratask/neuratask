import React, { useState } from "react";
import { Outlet, useNavigate, useLocation } from "react-router-dom";
import { DesktopOutlined, FileOutlined, PieChartOutlined, TeamOutlined, UserOutlined, ProjectOutlined } from "@ant-design/icons";
import type { MenuProps } from "antd";
import { Breadcrumb, Layout, Menu, theme } from "antd";

const { Header, Content, Footer, Sider } = Layout;

type MenuItem = Required<MenuProps>["items"][number];

function getItem(label: React.ReactNode, key: React.Key, icon?: React.ReactNode, children?: MenuItem[]): MenuItem {
  return {
    key,
    icon,
    children,
    label,
  } as MenuItem;
}

const AppLayout: React.FC = () => {
  const [collapsed, setCollapsed] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();

  const items: MenuItem[] = [
    getItem("Dashboard", "/", <PieChartOutlined />),
    getItem("Kanban Board", "/kanban", <ProjectOutlined />),
    getItem("Proyectos", "projects", <DesktopOutlined />),
    getItem("Usuarios", "sub1", <UserOutlined />, [
      getItem("Lista", "users"), 
      getItem("Perfil", "profile")
    ]),
    getItem("Equipos", "sub2", <TeamOutlined />, [
      getItem("Mi Equipo", "my-team"), 
      getItem("Todos los Equipos", "all-teams")
    ]),
    getItem("Archivos", "files", <FileOutlined />),
  ];

  const handleMenuClick = (e: any) => {
    if (e.key.startsWith('/')) {
      navigate(e.key);
    }
  };

  const getCurrentSelectedKeys = () => {
    return [location.pathname];
  };

  return (
    <Layout style={{ minHeight: "100vh" }}>
      <Sider collapsible collapsed={collapsed} onCollapse={(value) => setCollapsed(value)}>
        <div className="demo-logo-vertical p-4 text-center">
          <h2 className="text-white font-bold">NeuraTask</h2>
        </div>
        <Menu 
          theme="dark" 
          selectedKeys={getCurrentSelectedKeys()} 
          mode="inline" 
          items={items}
          onClick={handleMenuClick}
        />
      </Sider>
      <Layout>
        <Header style={{ padding: 0, background: colorBgContainer }} />
        <Content style={{ margin: "0 16px" }}>
          <Breadcrumb style={{ margin: "16px 0" }} items={[
            { title: "NeuraTask" }, 
            { title: location.pathname === "/" ? "Dashboard" : location.pathname.replace("/", "") }
          ]} />
          <div
            style={{
                padding: 24,
                minHeight: 360,
                background: colorBgContainer,
                borderRadius: borderRadiusLG,
            }}
          >
            <Outlet />
          </div>
        </Content>
        <Footer style={{ textAlign: "center" }}>NeuraTask ©{new Date().getFullYear()} Created by NeuraTask Corp</Footer>
      </Layout>
    </Layout>
  );
};

export default AppLayout;
