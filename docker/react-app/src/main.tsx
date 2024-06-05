import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import { BackendProvider } from "./services/backendService";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
    <React.StrictMode>
        <BackendProvider>
            <App />
        </BackendProvider>
    </React.StrictMode>
);
