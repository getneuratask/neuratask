// layouts/AppLayout.tsx
import React, { useState } from "react";
import { Layout, Breadcrumb, theme } from "antd";
import { Outlet, useLocation } from "react-router-dom";
import { Sidebar, Navbar } from "@/shared/components/molecules";

const { Content, Footer } = Layout;

const AppLayout: React.FC = () => {
  const [isMobile, setIsMobile] = useState(false);
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();

  const location = useLocation();

  const getBreadcrumbTitle = () => {
    const path = location.pathname;
    if (path === "/") return "Dashboard";
    return path
      .slice(1)
      .replace(/-/g, " ")
      .replace(/^\w/, (c) => c.toUpperCase());
  };

  return (
    <Layout style={{ minHeight: "100h" }}>
      <Sidebar isMobile={isMobile} setIsMobile={setIsMobile} />

      <Layout>
        <Navbar isMobile={isMobile} colorBgContainer={colorBgContainer} />

        <Content style={{ margin: "24px 16px 0" }}>
          <Breadcrumb style={{ margin: "16px 0" }} items={[{ title: "NeuraTask" }, { title: getBreadcrumbTitle() }]} />
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

        <Footer style={{ textAlign: "center", position: "sticky" }}>
          NeuraTask ©{new Date().getFullYear()} Created by NeuraTask Corp
        </Footer>
      </Layout>
    </Layout>
  );
};

export default AppLayout;
