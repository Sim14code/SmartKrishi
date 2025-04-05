import React from "react";
import Sidebar from "./components/Sidebar";
import LanguageToggle from "./components/LanguageToggle";
import { Routes, Route } from "react-router-dom";
import Advisor from "./pages/Advisor";
import MarketPrediction from "./pages/MarketPrediction";
import History from "./pages/History";
import Login from "./pages/Login";
import { useTranslation } from "react-i18next";
import Weather from "./components/Weather";
import Register from "./pages/Register";
import CropGlossary from "./components/CropGlossary";

export default function App() {
  const { t } = useTranslation();

  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <div
        className="flex-1 p-4 bg-cover bg-center"
        style={{ backgroundImage: "url('/farmer-bg.jpg')" }}
      >
        {/* Language Toggle Button */}
        <div className="flex justify-end">
          <LanguageToggle />
        </div>

        {/* Page Routes */}
        <Routes>
          <Route path="/" element={<Login />} />

          <Route path="/crop-glossary" element={<CropGlossary />} />
          <Route path="/weather" element={<Weather />} />
          <Route path="/register" element={<Register />} />

          <Route path="/advisor" element={<Advisor />} />
          <Route path="/market" element={<MarketPrediction />} />
          <Route path="/history" element={<History />} />
        </Routes>
      </div>
    </div>
  );
}
