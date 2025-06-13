import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import Router from "./router";

import "./assets/css/index.css";
import { Provider } from "react-redux";
import store from "./app/store";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <Provider store={store}>
      <Router />
    </Provider>
  </StrictMode>
);
