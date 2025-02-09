'use client'

import { useEffect, useState } from "react";

const TrafficSignalData = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("https://api.ibreakstuff.upayan.dev/traffic/signal-data")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((json) => {
        setData(json);
        setLoading(false);
      })
      .catch((error) => {
        setError(error.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold">Traffic Signal Data</h1>
      <p className="text-sm">Total Intersections: {data.intersections}</p>
      <div className="grid gap-4 mt-4">
        {Object.entries(data.data).map(([id, intersection]) => (
          <div key={id} className="border p-4 rounded-lg shadow">
            <h2 className="text-lg font-semibold">Intersection {id}</h2>
            <p>
              <strong>Location:</strong> {intersection.location.latitude.degrees}°
              {intersection.location.latitude.minutes}'
              {intersection.location.latitude.seconds}" {intersection.location.latitude.direction},
              {intersection.location.longitude.degrees}°
              {intersection.location.longitude.minutes}'
              {intersection.location.longitude.seconds}" {intersection.location.longitude.direction}
            </p>
            <p>
              <strong>Green Light Direction:</strong> {intersection.green.toUpperCase()}
            </p>
            <h3 className="font-medium mt-2">Vehicles</h3>
            <ul className="list-disc pl-5 text-sm">
              {Object.entries(intersection.vehicles).map(([direction, stats]) => (
                <li key={direction}>
                  <strong>{direction.toUpperCase()}:</strong> {stats.cars} cars, {stats.ambulances} ambulances, {stats.schoolbuses} school buses, {stats.accidents} accidents
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TrafficSignalData;
