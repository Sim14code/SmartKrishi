// import React from "react";
// import { useTranslation } from "react-i18next";

// export default function LanguageToggle() {
//   const { i18n } = useTranslation();

//   const toggleLanguage = () => {
//     i18n.changeLanguage(i18n.language === "en" ? "hi" : "en");
//   };

//   return (
//     <button
//       onClick={toggleLanguage}
//       className="mb-4 bg-blue-500 text-white px-4 py-2 rounded"
//     >
//       {i18n.language === "en" ? "Switch to Hindi" : "अंग्रेज़ी में स्विच करें"}
//     </button>
//   );
// }

import React from "react";
import { useTranslation } from "react-i18next";

export default function LanguageToggle() {
  const { i18n } = useTranslation();

  const toggleLanguage = () => {
    const newLang = i18n.language === "en" ? "hi" : "en";
    i18n.changeLanguage(newLang);
    localStorage.setItem("i18nextLng", newLang); // Persist language manually
  };

  return (
    <button
      onClick={toggleLanguage}
      className="mb-4 bg-blue-500 text-white px-4 py-2 rounded"
    >
      {i18n.language === "en" ? "Switch to Hindi" : "अंग्रेज़ी में स्विच करें"}
    </button>
  );
}
