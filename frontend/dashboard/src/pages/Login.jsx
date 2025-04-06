import React, { useState } from "react";
import { useTranslation } from "react-i18next";
import { useNavigate } from "react-router-dom";
import axios from "axios";

export default function Login() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const form = new URLSearchParams();
      form.append("username", name);
      form.append("password", password);

      await axios.post("http://localhost:5000/login", form);
      localStorage.setItem("loggedIn", "true");
      localStorage.setItem("loggedInName", name);
      navigate("/weather");
    } catch (err) {
      alert(err.response?.data?.error || "Login failed");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <h2 className="text-2xl font-bold mb-4">{t("login")}</h2>
      <form
        onSubmit={handleLogin}
        className="bg-white p-6 rounded shadow-md w-full max-w-sm"
      >
        <label className="block mb-2">{t("name")}</label>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="w-full mb-4 p-2 border rounded"
          required
        />

        <label className="block mb-2">{t("password")}</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full mb-4 p-2 border rounded"
          required
        />

        <button
          type="submit"
          className="w-full bg-blue-500 text-white p-2 rounded"
        >
          {t("login")}
        </button>
        <button
          type="button"
          onClick={() => navigate("/register")}
          className="w-full bg-green-500 text-white p-2 rounded mt-2"
        >
          {t("signup")}
        </button>
      </form>
    </div>
  );
}
