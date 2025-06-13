import { configureStore } from "@reduxjs/toolkit";
import sidebarReducer from "@/shared/features/sidebarSlice";

const store = configureStore({
  reducer: {
    sidebar: sidebarReducer,
  },
});

// Tipos exportables para usar en todo el proyecto
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

export default store;
