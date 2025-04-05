import React, { useState } from "react";
import { useTranslation } from "react-i18next";

export default function Advisor() {
  const { t } = useTranslation();

  const [crop, setCrop] = useState("");
  const [area, setArea] = useState("");
  const [goal, setGoal] = useState("");
  const [result, setResult] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setIsSubmitting(true);
  };

  return (
    <div className="max-w-xl mx-auto mt-8 p-6 bg-gradient-to-b from-green-100 to-green-200 shadow-lg rounded-2xl">
      <h2 className="text-2xl font-bold text-green-800 mb-4 text-center">
        {t("market")}
      </h2>

      <form
        onSubmit={handleSubmit}
        className="flex flex-col gap-4 bg-white p-6 rounded-lg shadow-md border border-green-100"
      >
        <input
          type="text"
          placeholder={t("crop_name")}
          value={crop}
          onChange={(e) => setCrop(e.target.value)}
          className="p-3 border border-green-200 rounded bg-green-50 focus:outline-none focus:ring-2 focus:ring-green-500"
        />

        <input
          type="text"
          placeholder={t("area")}
          value={area}
          onChange={(e) => setArea(e.target.value)}
          className="p-3 border border-green-200 rounded bg-green-50 focus:outline-none focus:ring-2 focus:ring-green-500"
        />

        <input
          type="text"
          placeholder={t("financial_goal")}
          value={goal}
          onChange={(e) => setGoal(e.target.value)}
          className="p-3 border border-green-200 rounded bg-green-50 focus:outline-none focus:ring-2 focus:ring-green-500"
        />

        <button
          type="submit"
          disabled={isSubmitting}
          className="bg-green-600 text-white py-2 rounded-lg hover:bg-green-700 transition"
        >
          {isSubmitting ? t("processing") : t("submit")}
        </button>
      </form>

      {result && (
        <div className="mt-6 bg-white p-4 rounded-lg shadow border border-green-100 animate-fadeIn">
          <h3 className="font-semibold text-green-700 mb-2">{t("result")}</h3>

          <p className="text-green-800">{result.recommendation}</p>

          <div className="grid grid-cols-2 gap-4 mt-4">
            <div className="bg-green-50 p-3 rounded">
              <p className="text-green-600">{t("yield")}</p>
              <p className="font-bold text-green-800">{result.yield}</p>
            </div>
            <div className="bg-green-50 p-3 rounded">
              <p className="text-green-600">{t("waterNeeded")}</p>
              <p className="font-bold text-green-800">{result.waterNeeded}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
