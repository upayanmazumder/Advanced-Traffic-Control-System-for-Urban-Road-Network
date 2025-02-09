import Image from "next/image";
import Data from "../components/data/data"
import Map from "../components/map/map"
export default function Home() {
  return (
    <main>
      <h1>Map</h1>
      <Map />
      <h1>Data</h1>
      <Data />
    </main>
  );
}
