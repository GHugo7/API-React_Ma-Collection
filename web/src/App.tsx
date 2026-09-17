import { Route, Routes } from "react-router-dom";
import NotFound from './pages/notfound';
import Register from "./pages/register";
import Home from "./pages/home";

export default function App() {

  return(
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/register" element={<Register />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  )  
} 