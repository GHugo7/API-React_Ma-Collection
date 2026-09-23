import { Route, Routes } from "react-router-dom";
import NotFound from './pages/NotFound';
import Register from "./pages/Register";
import Catalogue from "./pages/Catalogue";
import Navbar from "./pages/layout/Navbar";
import Login from "./pages/Login";
import ProtectedRoute from "./routes/ProtectedRoutes";

export default function App() {

  return(
    <Routes>
      <Route element={<Navbar />}>
        <Route path="/" element={<Catalogue />} />
        <Route path="/collection" element={<Catalogue />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />

        <Route element={<ProtectedRoute />} />

        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  )  
} 