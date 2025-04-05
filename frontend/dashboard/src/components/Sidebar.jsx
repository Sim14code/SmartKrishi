import { useTranslation } from "react-i18next";
import { Link, useNavigate } from "react-router-dom";
import {
  User,
  Home,
  BarChart2,
  Calendar,
  MessageSquare,
  Settings,
  ChevronLeft,
} from "lucide-react";
import { useEffect } from "react";

export default function Sidebar() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const isLoggedIn = localStorage.getItem("loggedIn") === "true";
  const name = localStorage.getItem("loggedInName");

  useEffect(() => {
    const privateRoutes = ["/advisor", "/market", "/history", "/weather"];
    if (!isLoggedIn && privateRoutes.includes(window.location.pathname)) {
      navigate("/");
    }
  }, [isLoggedIn, navigate]);

  const handleLogout = () => {
    localStorage.removeItem("loggedIn");
    localStorage.removeItem("loggedInName");
    navigate("/");
  };

  return (
    <div className="bg-green-800 text-white w-64 h-screen flex flex-col shadow-lg">
      {/* Header */}
      <div className="flex justify-between items-center px-4 py-3 bg-green-900">
        <h1 className="font-bold text-lg">SmartKrishi</h1>
        <button className="p-1 hover:bg-green-700 rounded-full transition-colors">
          <ChevronLeft size={18} />
        </button>
      </div>

      {/* User Profile */}
      {isLoggedIn && (
        <div className="p-4 border-b border-green-700 flex items-center space-x-3">
          <div className="w-12 h-12 rounded-full bg-green-600 flex items-center justify-center border-2 border-green-400 hover:border-white transition-colors">
            <User size={200} />
          </div>
          <div>
            <h3 className="font-medium text-sm">{name}</h3>
            <div className="flex items-center mt-1">
              <div className="w-2 h-2 rounded-full bg-emerald-400 mr-1.5"></div>
              <div className="w-2 h-2 rounded-full bg-emerald-400 mr-1.5"></div>
              <div className="w-2 h-2 rounded-full bg-emerald-400 mr-1.5"></div>
              <div className="w-2 h-2 rounded-full bg-emerald-400 mr-1.5"></div>
              <div className="w-2 h-2 rounded-full bg-emerald-400 mr-1.5"></div>
            </div>
          </div>
        </div>
      )}

      {/* Navigation */}
      <nav className="flex-grow py-4 px-2">
        <div className="space-y-1">
          <Link
            to="/"
            className="flex items-center w-full px-3 py-2.5 rounded-lg hover:bg-green-700 transition duration-200"
          >
            <Home size={18} className="mr-3 text-green-300" />
            {t("Weather")}
          </Link>

          <Link
            to="/advisor"
            className="flex items-center w-full px-3 py-2.5 rounded-lg hover:bg-green-700 transition duration-200"
          >
            <Calendar size={18} className="mr-3 text-green-300" />
            {t("crop_glossary")}
          </Link>

          <Link
            to="/history"
            className="flex items-center w-full px-3 py-2.5 rounded-lg hover:bg-green-700 transition duration-200"
          >
            <BarChart2 size={18} className="mr-3 text-green-300" />
            {t("history")}
          </Link>

          <Link
            to="/advisor"
            className="flex items-center w-full px-3 py-2.5 rounded-lg hover:bg-green-700 transition duration-200"
          >
            <Calendar size={18} className="mr-3 text-green-300" />
            {t("advisor")}
          </Link>

          <Link
            to="/market"
            className="flex items-center w-full px-3 py-2.5 rounded-lg hover:bg-green-700 transition duration-200"
          >
            <MessageSquare size={18} className="mr-3 text-green-300" />
            {t("market")}
          </Link>
        </div>

        <div className="mt-8 pt-4 border-t border-green-700">
          <button className="flex items-center w-full px-3 py-2.5 rounded-lg hover:bg-green-700 transition duration-200 text-green-100">
            <Settings size={18} className="mr-3 text-green-300" />
            {t("settings")}
          </button>
        </div>
      </nav>

      {/* Footer */}
      {isLoggedIn && (
        <div className="p-4 text-xs bg-green-900 flex items-center justify-between">
          <button
            onClick={handleLogout}
            className="bg-green-600 hover:bg-green-500 px-3 py-1.5 rounded text-xs font-medium transition-colors"
          >
            {t("Logout")}
          </button>
        </div>
      )}
    </div>
  );
}
