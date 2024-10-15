/* @refresh reload */
import { render } from "solid-js/web";

import { Route, Router } from "@solidjs/router";
import BoardComponent from "./components/BoardComponent";
import { DisplayingFileContextProvider } from "./context/DisplayingFileContext";
import { OverlayContextProvider } from "./context/OverlayContext";
import { SidebarVisibleContextProvider } from "./context/SidebarVisibleContext";
import { UserContextProvider } from "./context/UserContext";
import "./index.css";
import Home from "./pages/homePage/homePage";
import LoginPage from "./pages/LoginPage/LoginPage";
import RegisterPage from "./pages/RegisterPage/RegisterPage";
import UploadPage from "./pages/UploadPage/UploadPage";

const root = document.getElementById("root");

if (import.meta.env.DEV && !(root instanceof HTMLElement)) {
  throw new Error(
    "Root element not found. Did you forget to add it to your index.html? Or maybe the id attribute got misspelled?"
  );
}

render(
  () => (
    <UserContextProvider>
      <OverlayContextProvider>
        <SidebarVisibleContextProvider>
          <DisplayingFileContextProvider>
            {/* <Navbar /> */}
            <Router>
              <Route path="/" component={Home} />
              <Route path="/upload" component={UploadPage} />
              <Route path="/board" component={BoardComponent} />
              <Route path="/login" component={LoginPage} />
              <Route path="/register" component={RegisterPage} />
            </Router>
            {/* <Footer /> */}
            {/* <Sidebar /> */}
          </DisplayingFileContextProvider>
        </SidebarVisibleContextProvider>
      </OverlayContextProvider>
    </UserContextProvider>
  ),
  root!
);
