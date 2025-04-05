import React from "react";
import { useTranslation } from "react-i18next";

export default function History() {
  const { t } = useTranslation();

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-100">
      <div className="w-full max-w-xl p-6 bg-white shadow-2xl rounded-2xl">
        <h2 className="text-3xl font-bold text-center mb-6">{t("history")}</h2>
        <div className="text-center text-gray-600">
          {t("No previous records found.")}
        </div>
      </div>
    </div>
  );
}
