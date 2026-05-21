// Main React screen for image upload, weight input, and waste carbon analysis output.

import { useState } from "react";
import UploadForm from "./components/UploadForm";
import ImagePreview from "./components/ImagePreview";
import ResultTable from "./components/ResultTable";
import CarbonSummary from "./components/CarbonSummary";

const appStyle = {
  minHeight: "100vh",
  padding: "32px 20px 48px",
  background:
    "radial-gradient(circle at top left, #f5d0a9 0%, #f7efe4 30%, #dce7d5 100%)",
  color: "#1f2933",
  fontFamily: '"Avenir Next", "Noto Sans TC", sans-serif',
};

const shellStyle = {
  maxWidth: "1200px",
  margin: "0 auto",
  display: "grid",
  gap: "24px",
};

const headerStyle = {
  display: "grid",
  gap: "8px",
};

const titleStyle = {
  margin: 0,
  fontSize: "clamp(2rem, 4vw, 3.5rem)",
  fontWeight: 700,
};

const subtitleStyle = {
  margin: 0,
  maxWidth: "720px",
  lineHeight: 1.6,
};

const twoColumnStyle = {
  display: "grid",
  gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))",
  gap: "24px",
  alignItems: "start",
};

export default function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  return (
    <main style={appStyle}>
      <div style={shellStyle}>
        <header style={headerStyle}>
          <p style={{ margin: 0, letterSpacing: "0.18em", textTransform: "uppercase" }}>
            Food Waste Carbon System
          </p>
          <h1 style={titleStyle}>廚餘碳排放估算系統</h1>
          <p style={subtitleStyle}>
            上傳餐盤照片並輸入整盤廚餘重量，系統會使用 YOLOv11 辨識食物殘渣，
            依據資料庫中的密度係數與碳排係數推估每項食物重量與碳排量。
            如果某個辨識食物尚未建立碳排對應，系統會保留辨識與重量結果，但不會把它計入總碳排。
          </p>
        </header>

        <div style={twoColumnStyle}>
          <UploadForm
            loading={loading}
            onSubmitResult={setResult}
            onLoadingChange={setLoading}
            onErrorChange={setError}
          />
          <CarbonSummary result={result} loading={loading} error={error} />
        </div>

        <div style={twoColumnStyle}>
          <ImagePreview title="偵測結果" imageBase64={result?.image_base64} />
          <ImagePreview title="分群視圖" imageBase64={result?.clustering_image_base64} />
        </div>

        <ResultTable items={result?.objects ?? []} />
      </div>
    </main>
  );
}
