"use client";

import dynamic from "next/dynamic";
import Webcam from "react-webcam";

export default function Home() {
  return (
    <main className="flex flex-col items-center justify-center min-h-screen bg-black text-white">
      <h1 className="text-4xl font-bold mb-4">AwakenedFit</h1>
      <Webcam className="rounded-xl border-4 border-indigo-500" />
    </main>
  );
}

