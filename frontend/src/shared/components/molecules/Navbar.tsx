// components/Navbar.tsx
import React from "react";
import { Button, Layout, Space, Tooltip } from "antd";
import { LogoutOutlined, MenuOutlined } from "@ant-design/icons";
import { useSelector, useDispatch } from "react-redux";
import type { AppDispatch, RootState } from "@/app/store";
import { openSidebar } from "@/shared/features/sidebarSlice";

const { Header } = Layout;

const Navbar: React.FC<{ isMobile: boolean; colorBgContainer: string }> = ({ isMobile, colorBgContainer }) => {
  const collapsed = useSelector((state: RootState) => state.sidebar);
  const dispatch = useDispatch<AppDispatch>();

  const logout = () => {
    console.log("sesión cerrada");
  };

  const navbarStyle: React.CSSProperties = {
    position: "sticky",
    top: 0,
    zIndex: 1,
    width: "100%",
    display: "flex",
    alignItems: "center",
    background: colorBgContainer,
  };

  return (
    <Header
      style={navbarStyle}
      className={`px-0 py-4 flex items-center ${
        isMobile && collapsed ? "justify-between" : "justify-end"
      } bg-gray-200 dark:bg-black-900 shadow-md z-10`}
    >
      {isMobile && collapsed && (
        <Button icon={<MenuOutlined />} type="text" onClick={() => dispatch(openSidebar(false))} className="text-xl" />
      )}
      <Space>
        <div className="flex flex-col items-start"></div>
        <Tooltip placement="bottom" title="Cerrar sesión" arrow={true}>
          <Button shape="circle" type="text" icon={<LogoutOutlined />} onClick={logout} />
        </Tooltip>
      </Space>
    </Header>
  );
};

export default Navbar;
