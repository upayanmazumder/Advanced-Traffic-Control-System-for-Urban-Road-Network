'use client';

import { useEffect, useState } from 'react';
import styles from './map.module.css';
import { BiSolidBusSchool } from "react-icons/bi";
import { FaCarCrash, FaAmbulance, FaCarSide  } from "react-icons/fa";

export default function MapGrid() {
  const cols = 5;
  const rows = 4;
  const totalCells = rows * cols;

  const [grid, setGrid] = useState([]);
  const [trafficData, setTrafficData] = useState({});

  useEffect(() => {
    setGrid(Array.from({ length: totalCells }, (_, index) => index));

    fetch('https://api.ibreakstuff.upayan.dev/traffic/signal-data')
      .then((res) => res.json())
      .then((data) => setTrafficData(data.data || {}))
      .catch((err) => console.error('Error fetching traffic data:', err));
  }, []);

  const isBoundary = (index) => {
    const row = Math.floor(index / cols);
    const col = index % cols;
    return row === 0 || row === rows - 1 || col === 0 || col === cols - 1;
  };

  return (
    <div className={styles.gridContainer}>
      {grid.map((index) => {
        if (isBoundary(index)) return <div key={index} className={styles.emptyCell} />;

        const intersectionNumber = index < 9 ? index - 5 : index - 7;
        const intersectionData = trafficData[intersectionNumber];

        const borderColor = intersectionData?.green === "n-s" ? "red" : "green";

        return (
          <div key={index} className={styles.gridItem}>
            <button 
              className={styles.gridButton} 
              style={{ borderColor }}
            >
              <div className={styles.innerGrid}>
                <div className={styles.cell}></div>
                <div className={styles.cell}>
                  <p>
                    {intersectionData?.vehicles?.north?.cars} <FaCarSide /> {intersectionData?.vehicles?.north?.accidents} <FaCarCrash/><br />
                    {intersectionData?.vehicles?.north?.ambulances} <FaAmbulance/> {intersectionData?.vehicles?.north?.schoolbuses} <BiSolidBusSchool/>
                  </p>
                </div>
                <div className={styles.cell}></div>
                <div className={styles.cell}>
                  <p>
                    {intersectionData?.vehicles?.west?.cars} <FaCarSide /> {intersectionData?.vehicles?.west?.accidents} <FaCarCrash/><br />
                    {intersectionData?.vehicles?.west?.ambulances} <FaAmbulance/> {intersectionData?.vehicles?.west?.schoolbuses} <BiSolidBusSchool/>
                  </p>
                </div>
                <div className={styles.centerCell}>{intersectionNumber}</div>
                <div className={styles.cell}>
                  <p>
                    {intersectionData?.vehicles?.east?.cars} <FaCarSide /> {intersectionData?.vehicles?.east?.accidents} <FaCarCrash/><br />
                    {intersectionData?.vehicles?.east?.ambulances} <FaAmbulance/> {intersectionData?.vehicles?.east?.schoolbuses} <BiSolidBusSchool/>
                  </p>
                </div>
                <div className={styles.cell}></div>
                <div className={styles.cell}>
                  <p>
                    {intersectionData?.vehicles?.south?.cars} <FaCarSide /> {intersectionData?.vehicles?.south?.accidents} <FaCarCrash/><br />
                    {intersectionData?.vehicles?.south?.ambulances} <FaAmbulance/> {intersectionData?.vehicles?.south?.schoolbuses} <BiSolidBusSchool/>
                  </p>
                </div>
                <div className={styles.cell}></div>
              </div>
            </button>
          </div>
        );
        
      })}
    </div>
  );
}
