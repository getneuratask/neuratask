import {
  DesktopOutlined,
  FileOutlined,
  PieChartOutlined,
  TeamOutlined,
  UserOutlined,
  ProjectOutlined,
} from "@ant-design/icons";
import type { MenuProps } from "antd";
type MenuItem = Required<MenuProps>["items"][number];

function getItem(label: React.ReactNode, key: React.Key, icon?: React.ReactNode, children?: MenuItem[]): MenuItem {
  return {
    key,
    icon,
    children,
    label,
  } as MenuItem;
}

const sidebarItems: MenuItem[] = [
  getItem("Dashboard", "/", <PieChartOutlined />),
  getItem("Kanban Board", "/kanban", <ProjectOutlined />),
  getItem("Proyectos", "projects", <DesktopOutlined />),
  getItem("Usuarios", "sub1", <UserOutlined />, [getItem("Lista", "users"), getItem("Perfil", "profile")]),
  getItem("Equipos", "sub2", <TeamOutlined />, [
    getItem("Mi Equipo", "my-team"),
    getItem("Todos los Equipos", "all-teams"),
  ]),
  getItem("Archivos", "files", <FileOutlined />),
];

export default sidebarItems;
