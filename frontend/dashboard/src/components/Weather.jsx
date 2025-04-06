import React, { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import {
  Sun,
  Cloud,
  CloudRain,
  CloudSnow,
  CloudFog,
  CloudLightning,
  Wind,
  Thermometer,
  Droplets,
  Wind as WindIcon,
  MapPin,
} from "lucide-react";

export default function Weather() {
  const { t } = useTranslation();
  const [weather, setWeather] = useState(null);
  const [forecast, setForecast] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [unit, setUnit] = useState("metric"); // metric or imperial
  const [animateTemp, setAnimateTemp] = useState(false);

  const apiKey = "c616e7c90fb5944ead097362caa0be95"; // Your OpenWeather API Key

  const getWeatherIcon = (condition, size = 36) => {
    switch (condition) {
      case "Clear":
        return <Sun className="text-yellow-500 animate-pulse" size={size} />;
      case "Rain":
        return (
          <CloudRain className="text-blue-500 animate-bounce" size={size} />
        );
      case "Clouds":
        return <Cloud className="text-gray-500" size={size} />;
      case "Thunderstorm":
        return (
          <CloudLightning
            className="text-purple-500 animate-pulse"
            size={size}
          />
        );
      case "Drizzle":
        return <CloudRain className="text-blue-400" size={size} />;
      case "Snow":
        return (
          <CloudSnow className="text-blue-200 animate-pulse" size={size} />
        );
      case "Mist":
      case "Haze":
      case "Fog":
        return <CloudFog className="text-gray-400" size={size} />;
      default:
        return <Wind className="text-gray-600" size={size} />;
    }
  };

  const getTemperature = (temp) => {
    return unit === "metric"
      ? `${temp}°C`
      : `${((temp * 9) / 5 + 32).toFixed(1)}°F`;
  };

  const getBackgroundGradient = (temp) => {
    if (!temp) return "bg-gradient-to-br from-blue-400 to-blue-600";

    if (unit === "imperial") {
      temp = ((temp - 32) * 5) / 9; // Convert back to Celsius for gradient calculation
    }

    if (temp > 30) return "bg-gradient-to-br from-orange-400 to-red-600";
    if (temp > 20) return "bg-gradient-to-br from-yellow-300 to-orange-500";
    if (temp > 10) return "bg-gradient-to-br from-green-300 to-blue-400";
    if (temp > 0) return "bg-gradient-to-br from-blue-300 to-blue-500";
    return "bg-gradient-to-br from-blue-400 to-blue-700";
  };

  const groupForecastByDate = (list) => {
    const grouped = {};

    list.forEach((item) => {
      const date = item.dt_txt.split(" ")[0];

      if (!grouped[date]) {
        grouped[date] = {
          temps: [],
          conditions: [],
        };
      }

      grouped[date].temps.push(item.main.temp);
      grouped[date].conditions.push(item.weather[0].main);
    });

    return Object.keys(grouped).map((date) => {
      const temps = grouped[date].temps;
      const conditions = grouped[date].conditions;
      const mainCondition = conditions
        .sort(
          (a, b) =>
            conditions.filter((v) => v === a).length -
            conditions.filter((v) => v === b).length
        )
        .pop();

      return {
        date,
        minTemp: Math.min(...temps),
        maxTemp: Math.max(...temps),
        condition: mainCondition,
      };
    });
  };

  const toggleUnit = () => {
    setUnit((prev) => (prev === "metric" ? "imperial" : "metric"));
    setAnimateTemp(true);
    setTimeout(() => setAnimateTemp(false), 500);
  };

  useEffect(() => {
    if (!navigator.geolocation) {
      setError(t("Geolocation is not supported by your browser."));
      setLoading(false);
      return;
    }

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const { latitude, longitude } = position.coords;
        try {
          const [weatherRes, forecastRes] = await Promise.all([
            fetch(
              `https://api.openweathermap.org/data/2.5/weather?lat=${latitude}&lon=${longitude}&appid=${apiKey}&units=metric`
            ),
            fetch(
              `https://api.openweathermap.org/data/2.5/forecast?lat=${latitude}&lon=${longitude}&appid=${apiKey}&units=metric`
            ),
          ]);

          const weatherData = await weatherRes.json();
          const forecastData = await forecastRes.json();

          if (weatherData.cod !== 200) throw new Error(weatherData.message);
          if (forecastData.cod !== "200") throw new Error(forecastData.message);

          setWeather(weatherData);
          const groupedForecast = groupForecastByDate(forecastData.list).slice(
            1,
            6
          );
          setForecast(groupedForecast);
        } catch {
          setError(t("Failed to fetch weather data."));
        } finally {
          setLoading(false);
        }
      },
      () => {
        setError(t("Location permission denied or unavailable."));
        setLoading(false);
      }
    );
  }, [t, apiKey]);

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8 bg-gradient-to-br from-blue-400 to-blue-600 min-h-screen w-full text-white">
        <div className="animate-spin rounded-full h-16 w-16 border-4 border-white border-t-transparent"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-8 bg-gradient-to-br from-red-400 to-red-600 min-h-screen w-full text-white flex items-center justify-center">
        <div className="text-center max-w-md">
          <div className="mb-4 text-6xl">⚠️</div>
          <div className="font-bold text-xl">{error}</div>
        </div>
      </div>
    );
  }

  const currDate = new Date().toLocaleDateString(undefined, {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  });

  return (
    <div
      className={`min-h-screen w-full overflow-x-hidden transition-all duration-500 ${getBackgroundGradient(
        weather?.main?.temp
      )}`}
    >
      <div className="container mx-auto px-4 py-8 max-w-full">
        <div className="flex flex-wrap justify-between items-center mb-8">
          <div className="flex items-center mb-4 sm:mb-0">
            <MapPin className="text-white mr-2" size={24} />
            <h1 className="font-bold text-2xl md:text-3xl text-white">
              {weather?.name}
            </h1>
          </div>
          <button
            onClick={toggleUnit}
            className="bg-white bg-opacity-30 hover:bg-opacity-40 text-white font-semibold px-4 py-2 rounded-lg transition-all duration-300"
          >
            {unit === "metric" ? "Switch to °F" : "Switch to °C"}
          </button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Current Weather Card */}
          <div className="bg-white bg-opacity-20 backdrop-blur-sm p-4 md:p-6 rounded-xl shadow-lg">
            <h2 className="text-white text-xl mb-4 font-semibold">
              {t("Current Weather")}
            </h2>
            <p className="text-white opacity-80 text-sm md:text-base">
              {currDate}
            </p>

            <div className="flex items-center justify-between mt-6">
              <div>
                <p
                  className={`font-bold text-4xl md:text-6xl text-white transition-all duration-300 ${
                    animateTemp ? "scale-110" : "scale-100"
                  }`}
                >
                  {getTemperature(weather?.main?.temp)}
                </p>
                <p className="text-white text-base md:text-lg mt-1">
                  {t("feelsLike")} {getTemperature(weather?.main?.feels_like)}
                </p>
                <p className="capitalize text-white text-base md:text-lg mt-4 flex items-center">
                  {weather?.weather[0]?.main}
                </p>
              </div>
              <div className="text-6xl md:text-8xl">
                {getWeatherIcon(weather?.weather[0]?.main, 72)}
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3 mt-8">
              <div className="bg-white bg-opacity-20 p-3 rounded-lg">
                <div className="flex items-center text-white mb-2">
                  <Thermometer size={16} className="mr-2" />
                  <span className="opacity-80 text-sm">{t("minMax")}</span>
                </div>
                <p className="text-white text-sm md:text-base">
                  {getTemperature(weather?.main?.temp_min)} /{" "}
                  {getTemperature(weather?.main?.temp_max)}
                </p>
              </div>
              <div className="bg-white bg-opacity-20 p-3 rounded-lg">
                <div className="flex items-center text-white mb-2">
                  <Droplets size={16} className="mr-2" />
                  <span className="opacity-80 text-sm">{t("humidity")}</span>
                </div>
                <p className="text-white text-sm md:text-base">
                  {weather?.main?.humidity}%
                </p>
              </div>
              <div className="bg-white bg-opacity-20 p-3 rounded-lg">
                <div className="flex items-center text-white mb-2">
                  <WindIcon size={16} className="mr-2" />
                  <span className="opacity-80 text-sm">{t("wind")}</span>
                </div>
                <p className="text-white text-sm md:text-base">
                  {weather?.wind?.speed} m/s
                </p>
              </div>
              <div className="bg-white bg-opacity-20 p-3 rounded-lg">
                <div className="flex items-center text-white mb-2">
                  <Cloud size={16} className="mr-2" />
                  <span className="opacity-80 text-sm">{t("pressure")}</span>
                </div>
                <p className="text-white text-sm md:text-base">
                  {weather?.main?.pressure} hPa
                </p>
              </div>
            </div>
          </div>

          {/* 5-Day Forecast */}
          <div className="lg:col-span-2 bg-white bg-opacity-20 backdrop-blur-sm p-4 md:p-6 rounded-xl shadow-lg">
            <h2 className="text-white text-xl mb-6 font-semibold">
              {t("forecast")}
            </h2>
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-3">
              {forecast.map((item, index) => (
                <div
                  key={index}
                  className="bg-white bg-opacity-20 p-3 rounded-lg hover:bg-opacity-30 transition-all duration-300 flex flex-col items-center"
                >
                  <p className="text-white font-medium mb-2 text-sm">
                    {new Date(item.date).toLocaleDateString(undefined, {
                      weekday: "short",
                    })}
                  </p>
                  <div className="my-2">
                    {getWeatherIcon(item.condition, 36)}
                  </div>
                  <p className="text-white font-medium text-base">
                    {getTemperature(item.maxTemp)}
                  </p>
                  <p className="text-white opacity-80 text-sm">
                    {getTemperature(item.minTemp)}
                  </p>
                  <p className="text-white text-xs mt-1">{item.condition}</p>
                </div>
              ))}
            </div>

            {/* Weather Details */}
            <div className="mt-6 md:mt-8">
              <h2 className="text-white text-xl mb-4 font-semibold">
                {t("weatherdetails")}
              </h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="bg-white bg-opacity-20 p-3 md:p-4 rounded-lg">
                  <h3 className="text-white font-medium mb-2 text-sm md:text-base">
                    {t("sunrisesunset")}
                  </h3>
                  <div className="flex flex-wrap justify-between">
                    <div className="flex items-center mb-2 md:mb-0">
                      <Sun size={20} className="text-yellow-400 mr-2" />
                      <div>
                        <p className="text-white opacity-80 text-xs">
                          {t("sunrise")}
                        </p>
                        <p className="text-white text-sm">
                          {new Date(
                            weather?.sys?.sunrise * 1000
                          ).toLocaleTimeString([], {
                            hour: "2-digit",
                            minute: "2-digit",
                          })}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center">
                      <Sun size={20} className="text-orange-400 mr-2" />
                      <div>
                        <p className="text-white opacity-80 text-xs">
                          {t("sunset")}
                        </p>
                        <p className="text-white text-sm">
                          {new Date(
                            weather?.sys?.sunset * 1000
                          ).toLocaleTimeString([], {
                            hour: "2-digit",
                            minute: "2-digit",
                          })}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
                <div className="bg-white bg-opacity-20 p-3 md:p-4 rounded-lg">
                  <h3 className="text-white font-medium mb-2 text-sm md:text-base">
                    {t("visibilityclouds")}
                  </h3>
                  <div className="flex justify-between">
                    <div>
                      <p className="text-white opacity-80 text-xs">
                        {t("visibility")}
                      </p>
                      <p className="text-white text-sm">
                        {(weather?.visibility / 1000).toFixed(1)} km
                      </p>
                    </div>
                    <div>
                      <p className="text-white opacity-80 text-xs">
                        {t("cloudiness")}
                      </p>
                      <p className="text-white text-sm">
                        {weather?.clouds?.all}%
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
