'use client';

import { useEffect, useState } from "react";
import styles from "./data.module.css";
import { BiSolidBusSchool } from "react-icons/bi";
import { FaCarCrash, FaAmbulance, FaCarSide  } from "react-icons/fa";

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

  if (loading) return <p className={styles.loading}>Loading...</p>;
  if (error) return <p className={styles.error}>Error: {error}</p>;

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Traffic Signal Data</h1>
      <p className={styles.subtitle}>Total Intersections: {data.intersections}</p>
      <div className={styles.grid}>
        {Object.entries(data.data).map(([id, intersection]) => {
          let totalCars = 0, totalAmbulances = 0, totalSchoolBuses = 0, totalAccidents = 0;

          Object.values(intersection.vehicles).forEach(({ cars, ambulances, schoolbuses, accidents }) => {
            totalCars += cars;
            totalAmbulances += ambulances;
            totalSchoolBuses += schoolbuses;
            totalAccidents += accidents;
          });

          return (
            <details key={id} className={styles.intersection}>
              <summary className={styles.summary}>
                <span className={styles.arrow}>▶</span> Intersection {id} - {totalCars} <FaCarSide />, {totalAmbulances} <FaAmbulance />, {totalSchoolBuses} <BiSolidBusSchool />, {totalAccidents} <FaCarCrash />
              </summary>
              <div className={styles.detailsContent}>
                <p className={styles.location}>
                  {intersection.location.latitude.degrees}°
                  {intersection.location.latitude.minutes}'
                  {intersection.location.latitude.seconds}" {intersection.location.latitude.direction}, 
                  {intersection.location.longitude.degrees}°
                  {intersection.location.longitude.minutes}'
                  {intersection.location.longitude.seconds}" {intersection.location.longitude.direction}
                </p>
                <p>
                  <strong>Green Light:</strong> {intersection.green.toUpperCase()}
                </p>
                <h3 className={styles.sectionTitle}>Vehicles</h3>
                <ul className={styles.vehicleList}>
                  {Object.entries(intersection.vehicles).map(([direction, stats]) => (
                    <li key={direction} className={styles.vehicleItem}>
                      <strong>{direction.toUpperCase()}:</strong> {stats.cars} cars, {stats.ambulances} ambulances, {stats.schoolbuses} , {stats.accidents} accidents
                    </li>
                  ))}
                </ul>
              </div>
            </details>
          );
        })}
      </div>
    </div>
  );
};

export default TrafficSignalData;
