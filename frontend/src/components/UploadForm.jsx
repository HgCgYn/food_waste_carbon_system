// Upload form component that sends image and total plate weight to the backend API.

import { useEffect, useState } from "react";
import { detectWaste } from "../api/wasteApi";

const panelStyle = {
  background: "rgba(255,255,255,0.78)",
  backdropFilter: "blur(12px)",
  borderRadius: "24px",
  padding: "24px",
  boxShadow: "0 20px 50px rgba(53, 78, 55, 0.12)",
  display: "grid",
  gap: "16px",
};

const fieldStyle = {
  display: "grid",
  gap: "8px",
};

const labelStyle = {
  fontWeight: 600,
};

const inputStyle = {
  width: "100%",
  padding: "14px 16px",
  borderRadius: "14px",
  border: "1px solid #b6c4b2",
  fontSize: "1rem",
  background: "#fffdf8",
  boxSizing: "border-box",
};

const modeRowStyle = {
  display: "flex",
  gap: "10px",
  flexWrap: "wrap",
};

const modeButtonStyle = (active) => ({
  border: active ? "1px solid #2d6a4f" : "1px solid #b6c4b2",
  borderRadius: "999px",
  padding: "10px 16px",
  background: active ? "#dff2e8" : "#fffdf8",
  color: "#1f2933",
  fontWeight: 700,
  cursor: "pointer",
});

const hiddenInputStyle = {
  display: "none",
};

const pickerStyle = {
  border: "1px solid #b6c4b2",
  borderRadius: "18px",
  padding: "14px",
  background: "#fffdf8",
  display: "grid",
  gap: "12px",
};

const pickerButtonStyle = {
  display: "inline-flex",
  alignItems: "center",
  justifyContent: "center",
  border: 0,
  borderRadius: "14px",
  padding: "12px 16px",
  background: "#eff5ef",
  color: "#1f2933",
  fontWeight: 700,
  cursor: "pointer",
  width: "fit-content",
};

const previewFrameStyle = {
  borderRadius: "18px",
  overflow: "hidden",
  border: "1px solid #d7e1d3",
  background: "#f5f7f2",
};

const buttonStyle = (disabled) => ({
  border: 0,
  borderRadius: "999px",
  padding: "14px 22px",
  background: disabled ? "#98a39a" : "#2d6a4f",
  color: "#ffffff",
  fontSize: "1rem",
  fontWeight: 700,
  cursor: disabled ? "not-allowed" : "pointer",
});

export default function UploadForm({
  loading,
  onSubmitResult,
  onLoadingChange,
  onErrorChange,
}) {
  const [file, setFile] = useState(null);
  const [weight, setWeight] = useState("");
  const [inputMode, setInputMode] = useState("upload");
  const [previewUrl, setPreviewUrl] = useState("");

  useEffect(() => {
    if (!file) {
      setPreviewUrl("");
      return undefined;
    }

    const url = URL.createObjectURL(file);
    setPreviewUrl(url);
    return () => URL.revokeObjectURL(url);
  }, [file]);

  const handleFileChange = (event) => {
    setFile(event.target.files?.[0] ?? null);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!file) {
      onErrorChange("請先選擇圖片。");
      return;
    }

    onLoadingChange(true);
    onErrorChange("");

    try {
      const result = await detectWaste(file, weight);
      onSubmitResult(result);
    } catch (error) {
      onErrorChange(error.message || "分析失敗，請稍後再試。");
      onSubmitResult(null);
    } finally {
      onLoadingChange(false);
    }
  };

  return (
    <section style={panelStyle}>
      <h2 style={{ margin: 0 }}>分析輸入</h2>
      <form onSubmit={handleSubmit} style={{ display: "grid", gap: "16px" }}>
        <div style={fieldStyle}>
          <span style={labelStyle}>
            餐盤圖片
          </span>
          <div style={modeRowStyle}>
            <button
              type="button"
              style={modeButtonStyle(inputMode === "upload")}
              onClick={() => setInputMode("upload")}
            >
              上傳照片
            </button>
            <button
              type="button"
              style={modeButtonStyle(inputMode === "camera")}
              onClick={() => setInputMode("camera")}
            >
              直接拍照
            </button>
          </div>

          <div style={pickerStyle}>
            {inputMode === "upload" ? (
              <>
                <label htmlFor="upload-file" style={pickerButtonStyle}>
                  選擇照片
                </label>
                <input
                  id="upload-file"
                  type="file"
                  accept="image/*"
                  onChange={handleFileChange}
                  style={hiddenInputStyle}
                />
              </>
            ) : (
              <>
                <label htmlFor="camera-file" style={pickerButtonStyle}>
                  開啟相機
                </label>
                <input
                  id="camera-file"
                  type="file"
                  accept="image/*"
                  capture="environment"
                  onChange={handleFileChange}
                  style={hiddenInputStyle}
                />
              </>
            )}

            <div style={{ color: "#5b6b61" }}>
              {file ? `已選擇：${file.name}` : inputMode === "camera" ? "拍攝完成後會自動帶入圖片。" : "支援從裝置選擇既有圖片。"}
            </div>

            {previewUrl ? (
              <div style={previewFrameStyle}>
                <img
                  src={previewUrl}
                  alt="餐盤預覽"
                  style={{ display: "block", width: "100%", maxHeight: "260px", objectFit: "cover" }}
                />
              </div>
            ) : (
              <div
                style={{
                  ...inputStyle,
                  minHeight: "140px",
                  display: "grid",
                  placeItems: "center",
                  color: "#5b6b61",
                  borderStyle: "dashed",
                }}
              >
                尚未選擇圖片
              </div>
            )}
          </div>
        </div>

        <div style={fieldStyle}>
          <label htmlFor="weight" style={labelStyle}>
            整盤廚餘重量（g）
          </label>
          <input
            id="weight"
            type="number"
            min="0"
            step="0.01"
            value={weight}
            onChange={(event) => setWeight(event.target.value)}
            placeholder="例如 350"
            style={inputStyle}
          />
        </div>

        <button type="submit" disabled={loading} style={buttonStyle(loading)}>
          {loading ? "分析中..." : "開始分析"}
        </button>
      </form>
    </section>
  );
}
