import Image from "next/image";
import Data from "../components/data/data"
import Map from "../components/map/map"
export default function Home() {
  return (
    <>
      <Map />
      <main>
        <Data />
      </main>
    </>
  );
}
