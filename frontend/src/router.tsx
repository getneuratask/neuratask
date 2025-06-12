import { Route, BrowserRouter, Routes } from "react-router-dom";
import AppLayout from "./layouts/AppLayout";
import HomeView from "./views/HomeView";
import Kanban from "./components/KanbanTest/Kanban";

export default function Router() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppLayout />}>
          <Route path="/" element={<HomeView />} index />
          <Route path="/kanban" element={<Kanban />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
