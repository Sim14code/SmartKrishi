import React from "react";
import { useTranslation } from "react-i18next";

const CropGlossary = () => {
  const { t } = useTranslation();

  const glossaryItems = [
    { key: "market_price" },
    { key: "demand_index" },
    { key: "supply_index" },
    { key: "competitor_price" },
    { key: "economic_indicator" },
    { key: "weather_impact_score" },
    { key: "seasonal_factors" },
    { key: "consumer_trend_index" },
  ];

  return (
    <div className="p-6 max-w-3xl mx-auto bg-green rounded-xl shadow-md space-y-6">
      <h1 className="text-2xl font-bold text-center">
        {t("definitions_heading")}
      </h1>
      <ul className="space-y-4">
        {glossaryItems.map((item) => (
          <li
            key={item.key}
            className="border p-4 rounded shadow-sm bg-gray-50"
          >
            <p className="text-lg font-semibold text-green-700">
              {t(item.key)}
            </p>
            <p className="text-gray-700 mt-2">{t(`${item.key}_definition`)}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CropGlossary;
