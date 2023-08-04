import Home from "../pages/Home";
import Login from "../pages/Login";

const appRouter = {
  "/login": <Login />,
  "*": <Home />,
};

export default appRouter;
