// components/Sidebar.tsx
import React, { useRef, useEffect } from "react";
import { Layout, Menu } from "antd";
import { useNavigate, useLocation } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import type { AppDispatch, RootState } from "@/app/store";
import { openSidebar } from "@/shared/features/sidebarSlice";
import sidebarItems from "@/shared/static/sidebarItems";

const { Sider } = Layout;

const Sidebar: React.FC<{ isMobile: boolean; setIsMobile: (val: boolean) => void }> = ({ isMobile, setIsMobile }) => {
  const collapsed = useSelector((state: RootState) => state.sidebar);
  const dispatch = useDispatch<AppDispatch>();
  const siderRef = useRef<HTMLDivElement>(null);
  const navigate = useNavigate();
  const location = useLocation();

  const siderStyle: React.CSSProperties = {
    overflow: "auto",
    height: "100vh",
    position: "sticky",
    insetInlineStart: 0,
    top: 0,
    bottom: 0,
    scrollbarWidth: "thin",
    scrollbarGutter: "stable",
  };
  const handleMenuClick = ({ key }: { key: string }) => {
    if (key.startsWith("/")) {
      navigate(key);
      if (isMobile) {
        dispatch(openSidebar(true));
      }
    }
  };

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (isMobile && !collapsed && siderRef.current && !siderRef.current.contains(event.target as Node)) {
        dispatch(openSidebar(true));
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [collapsed, isMobile]);

  return (
    <Sider
      style={siderStyle}
      ref={siderRef}
      collapsedWidth={0}
      collapsed={collapsed}
      breakpoint="lg"
      trigger={null}
      onBreakpoint={(broken) => {
        setIsMobile(broken);
        dispatch(openSidebar(broken));
      }}
    >
      <div className="demo-logo-vertical p-4 text-center">
        <h2 className="text-white font-bold">NeuraTask</h2>
      </div>
      <Menu
        theme="dark"
        mode="inline"
        selectedKeys={[location.pathname]}
        onClick={handleMenuClick}
        items={sidebarItems}
      />
    </Sider>
  );
};

export default Sidebar;
