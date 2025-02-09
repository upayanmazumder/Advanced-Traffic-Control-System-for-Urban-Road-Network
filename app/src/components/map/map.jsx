'use client';

import { useEffect, useState } from 'react';
import styles from './map.module.css';

export default function MapGrid() {
  const cols = 5;
  const rows = 4;
  const totalCells = rows * cols;

  const [grid, setGrid] = useState([]);

  useEffect(() => {
    setGrid(Array.from({ length: totalCells }, (_, index) => index));
  }, []);

  // Function to check if a button is on the boundary
  const isBoundary = (index) => {
    const row = Math.floor(index / cols);
    const col = index % cols;
    return row === 0 || row === rows - 1 || col === 0 || col === cols - 1;
  };

  return (
    <div className={styles.gridContainer}>
      {grid.map((index) => {
        const row = Math.floor(index / cols);
        const col = index % cols;

        const rightIndex = index + 1;
        const downIndex = index + cols;

        const hasRightNeighbor = col < cols - 1 && !isBoundary(index) && !isBoundary(rightIndex);
        const hasDownNeighbor = row < rows - 1 && !isBoundary(index) && !isBoundary(downIndex);

        return (
          <div key={index} className={styles.gridItem}>
            {/* Button (Hidden if boundary) */}
            <button className={`${styles.gridButton} ${isBoundary(index) ? styles.hiddenButton : ''}`}>
              {isBoundary(index) ? '' : index + 1}
            </button>

            {/* Horizontal Line (Only if both buttons are visible) */}
            {hasRightNeighbor && <div className={styles.horizontalLine} />}

            {/* Vertical Line (Only if both buttons are visible) */}
            {hasDownNeighbor && <div className={styles.verticalLine} />}
          </div>
        );
      })}
    </div>
  );
}
