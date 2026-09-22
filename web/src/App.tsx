import { Route, Routes } from "react-router-dom";
import NotFound from './pages/notfound';
import Register from "./pages/register";
import Catalogue from "./pages/catalogue";
import Navbar from "./pages/navbar";
import Login from "./pages/login";
import ProtectedRoute from "./routes/ProtectedRoutes";

export default function App() {

  return(
    <Routes>
      <Route element={<Navbar />}>
        <Route path="/" element={<Catalogue />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />

        <Route element={<ProtectedRoute />} />

        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  )  
} 