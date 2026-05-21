// Main React screen for image upload, weight input, and waste carbon analysis output.

import { useState } from "react";
import UploadForm from "./components/UploadForm";
import ImagePreview from "./components/ImagePreview";
import ResultTable from "./components/ResultTable";
import CarbonSummary from "./components/CarbonSummary";

const loadingKeyframes = `
  @keyframes analysisPulse {
    0%,
    100% {
      opacity: 0.45;
      transform: scale(0.92);
    }
    50% {
      opacity: 1;
      transform: scale(1);
    }
  }

  @keyframes analysisShimmer {
    0% {
      background-position: 200% 0;
    }
    100% {
      background-position: -200% 0;
    }
  }

  @keyframes overlayFloat {
    0%,
    100% {
      transform: translateY(0);
    }
    50% {
      transform: translateY(-6px);
    }
  }
`;

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

const overlayStyle = {
  position: "fixed",
  inset: 0,
  background: "rgba(22, 34, 26, 0.42)",
  backdropFilter: "blur(10px)",
  display: "grid",
  placeItems: "center",
  zIndex: 1000,
  padding: "24px",
};

const overlayCardStyle = {
  width: "min(440px, 100%)",
  background: "rgba(255,255,255,0.92)",
  borderRadius: "28px",
  padding: "28px 24px",
  boxShadow: "0 30px 80px rgba(25, 41, 30, 0.22)",
  display: "grid",
  gap: "18px",
  textAlign: "center",
};

const overlaySpinnerStyle = {
  width: "72px",
  height: "72px",
  margin: "0 auto",
  borderRadius: "22px",
  background:
    "linear-gradient(135deg, rgba(45,106,79,0.16), rgba(160,196,163,0.42), rgba(45,106,79,0.16))",
  display: "grid",
  placeItems: "center",
  animation: "analysisShimmer 2.2s linear infinite, overlayFloat 1.6s ease-in-out infinite",
};

const overlayDotsStyle = {
  display: "flex",
  justifyContent: "center",
  gap: "10px",
};

const overlayDotStyle = (delay) => ({
  width: "12px",
  height: "12px",
  borderRadius: "999px",
  background: "#2d6a4f",
  animation: "analysisPulse 1s ease-in-out infinite",
  animationDelay: delay,
});

export default function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  return (
    <main style={appStyle}>
      <style>{loadingKeyframes}</style>
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
      {loading ? (
        <div style={overlayStyle} role="status" aria-live="polite" aria-busy="true">
          <div style={overlayCardStyle}>
            <div style={overlaySpinnerStyle}>
              <div style={overlayDotsStyle} aria-hidden="true">
                <span style={overlayDotStyle("0s")} />
                <span style={overlayDotStyle("0.18s")} />
                <span style={overlayDotStyle("0.36s")} />
              </div>
            </div>
            <div style={{ display: "grid", gap: "8px" }}>
              <strong style={{ fontSize: "1.2rem" }}>正在分析中</strong>
              <div style={{ color: "#4b5d51", lineHeight: 1.6 }}>
                系統正在辨識餐盤內容、估算重量，並生成偵測結果圖片。
              </div>
            </div>
          </div>
        </div>
      ) : null}
    </main>
  );
}
