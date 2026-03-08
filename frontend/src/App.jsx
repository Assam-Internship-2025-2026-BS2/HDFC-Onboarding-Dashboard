import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Layout from "./ui/Layout";
import Dashboard from "./pages/Dashboard";
import Products from "./pages/Products";
import CustomerInsights from "./pages/CustomerInsights";
import Analysis from "./pages/Analysis";

export default function App(){
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="products" element={<Products />} />
          <Route path="insights" element={<CustomerInsights />} />
          <Route path="analysis" element={<Analysis />} />
        </Route>
      </Routes>
    </Router>
  );
}
