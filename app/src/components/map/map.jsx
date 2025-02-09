'use client';

import { useEffect, useState } from 'react';
import styles from './map.module.css';

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

        return (
          <div key={index} className={styles.gridItem}>
            <button className={styles.gridButton}>
              <div className={styles.innerGrid}>
                <div className={styles.cell}></div>
                <div className={styles.cell}>
                  {intersectionData?.vehicles?.north?.cars} 🚗<br />
                  {intersectionData?.vehicles?.north?.accidents} ⚠️<br />
                  {intersectionData?.vehicles?.north?.ambulances} 🚑<br />
                  {intersectionData?.vehicles?.north?.schoolbuses} 🚌
                </div>
                <div className={styles.cell}></div>
                <div className={styles.cell}>
                  {intersectionData?.vehicles?.west?.cars} 🚗<br />
                  {intersectionData?.vehicles?.west?.accidents} ⚠️<br />
                  {intersectionData?.vehicles?.west?.ambulances} 🚑<br />
                  {intersectionData?.vehicles?.west?.schoolbuses} 🚌
                </div>
                <div className={styles.centerCell}>{intersectionNumber}</div>
                <div className={styles.cell}>
                  {intersectionData?.vehicles?.east?.cars} 🚗<br />
                  {intersectionData?.vehicles?.east?.accidents} ⚠️<br />
                  {intersectionData?.vehicles?.east?.ambulances} 🚑<br />
                  {intersectionData?.vehicles?.east?.schoolbuses} 🚌
                </div>
                <div className={styles.cell}></div>
                <div className={styles.cell}>
                  {intersectionData?.vehicles?.south?.cars} 🚗<br />
                  {intersectionData?.vehicles?.south?.accidents} ⚠️<br />
                  {intersectionData?.vehicles?.south?.ambulances} 🚑<br />
                  {intersectionData?.vehicles?.south?.schoolbuses} 🚌
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
