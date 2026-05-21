// Upload form component that supports file upload or live camera capture before analysis.

import { useEffect, useRef, useState } from "react";
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

const errorInputStyle = {
  border: "2px solid #d14343",
  boxShadow: "0 0 0 3px rgba(209, 67, 67, 0.12)",
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
  background: "#2d6a4f",
  color: "#ffffff",
  fontWeight: 700,
  cursor: "pointer",
  width: "fit-content",
  boxShadow: "0 10px 24px rgba(45, 106, 79, 0.18)",
};

const previewFrameStyle = {
  borderRadius: "18px",
  overflow: "hidden",
  border: "1px solid #d7e1d3",
  background: "#f5f7f2",
};

const cameraPanelStyle = {
  border: "1px solid #d7e1d3",
  borderRadius: "18px",
  padding: "14px",
  background: "#f5f7f2",
  display: "grid",
  gap: "12px",
};

const secondaryButtonStyle = {
  border: "1px solid #c7d3c4",
  borderRadius: "14px",
  padding: "12px 16px",
  background: "#ffffff",
  color: "#1f2933",
  fontWeight: 700,
  cursor: "pointer",
};

const disabledButtonStyle = {
  opacity: 0.45,
  cursor: "not-allowed",
  boxShadow: "none",
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
  const [fileTouched, setFileTouched] = useState(false);
  const [weight, setWeight] = useState("");
  const [weightTouched, setWeightTouched] = useState(false);
  const [inputMode, setInputMode] = useState("upload");
  const [previewUrl, setPreviewUrl] = useState("");
  const [cameraActive, setCameraActive] = useState(false);
  const [cameraReady, setCameraReady] = useState(false);
  const [cameraStarting, setCameraStarting] = useState(false);
  const [cameraError, setCameraError] = useState("");
  const [cameraStream, setCameraStream] = useState(null);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  useEffect(() => {
    const video = videoRef.current;
    if (!cameraActive || !video || !cameraStream) {
      return;
    }

    const attachStream = async () => {
      try {
        video.srcObject = cameraStream;
        video.muted = true;
        video.playsInline = true;
        video.autoplay = true;
        await video.play();
        await waitForVideoReady(video);
        setCameraReady(true);
        setCameraStarting(false);
        setCameraError("");
      } catch {
        setCameraError("相機已啟動，但預覽載入失敗，請重新開啟相機。");
      }
    };

    attachStream();
  }, [cameraActive, cameraStream]);

  useEffect(() => {
    if (!file) {
      setPreviewUrl("");
      return undefined;
    }

    const url = URL.createObjectURL(file);
    setPreviewUrl(url);
    return () => URL.revokeObjectURL(url);
  }, [file]);

  useEffect(() => {
    return () => {
      stopCamera();
    };
  }, []);

  const handleFileChange = (event) => {
    setFile(event.target.files?.[0] ?? null);
    setFileTouched(true);
    setCameraError("");
  };

  const stopCamera = () => {
    if (cameraStream) {
      cameraStream.getTracks().forEach((track) => track.stop());
    }
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
    setCameraStream(null);
    setCameraActive(false);
    setCameraReady(false);
    setCameraStarting(false);
  };

  const startCamera = async () => {
    if (!navigator.mediaDevices?.getUserMedia) {
      setCameraError("目前瀏覽器不支援直接開啟相機。");
      return;
    }

    stopCamera();
    setCameraError("");
    setCameraStarting(true);
    setCameraActive(true);
    setCameraReady(false);

    try {
      let stream;
      try {
        stream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: { ideal: "environment" } },
          audio: false,
        });
      } catch {
        stream = await navigator.mediaDevices.getUserMedia({
          video: true,
          audio: false,
        });
      }
      setCameraStream(stream);
    } catch (error) {
      stopCamera();
      setCameraError("無法開啟相機，請確認已允許瀏覽器使用攝影機。");
    }
  };

  const capturePhoto = async () => {
    if (!videoRef.current || !canvasRef.current || !cameraReady) {
      setCameraError("相機畫面尚未準備完成，請稍候再拍照。");
      return;
    }

    const video = videoRef.current;
    const canvas = canvasRef.current;
    canvas.width = video.videoWidth || 1280;
    canvas.height = video.videoHeight || 720;

    const context = canvas.getContext("2d");
    if (!context) {
      setCameraError("無法擷取相機畫面。");
      return;
    }

    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    const blob = await new Promise((resolve) => canvas.toBlob(resolve, "image/jpeg", 0.92));
    if (!blob) {
      setCameraError("拍照失敗，請再試一次。");
      return;
    }

    const capturedFile = new File([blob], `camera-capture-${Date.now()}.jpg`, {
      type: "image/jpeg",
    });
    setFile(capturedFile);
    setFileTouched(true);
    stopCamera();
  };

  const handleVideoReady = () => {
    if (videoRef.current?.videoWidth && videoRef.current?.videoHeight) {
      setCameraReady(true);
      setCameraStarting(false);
      setCameraError("");
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!file) {
      setFileTouched(true);
      onErrorChange("請先選擇圖片。");
      return;
    }

    if (!weight || Number(weight) <= 0) {
      setWeightTouched(true);
      onErrorChange("請輸入大於 0 的整盤廚餘重量。");
      return;
    }

    onLoadingChange(true);
    onErrorChange("");
    onSubmitResult(null);

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

  const fileHasError = fileTouched && !file;
  const weightHasError = weightTouched && (!weight || Number(weight) <= 0);

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
              onClick={() => {
                setInputMode("upload");
                stopCamera();
              }}
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

          <div style={fileHasError ? { ...pickerStyle, ...errorInputStyle } : pickerStyle}>
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
              <div style={cameraPanelStyle}>
                <div style={{ display: "flex", gap: "10px", flexWrap: "wrap" }}>
                  {cameraActive ? (
                    <button type="button" style={secondaryButtonStyle} onClick={stopCamera}>
                      關閉相機
                    </button>
                  ) : (
                    <button type="button" style={pickerButtonStyle} onClick={startCamera}>
                      {cameraStarting ? "啟動相機中..." : "開啟相機"}
                    </button>
                  )}
                  <button
                    type="button"
                    style={{
                      ...pickerButtonStyle,
                      ...(cameraReady ? {} : disabledButtonStyle),
                    }}
                    onClick={capturePhoto}
                    disabled={!cameraReady}
                  >
                    拍照並使用
                  </button>
                </div>

                {cameraError ? (
                  <div style={{ color: "#b45309", lineHeight: 1.6 }}>{cameraError}</div>
                ) : null}

                <div style={previewFrameStyle}>
                  {cameraActive ? (
                    <video
                      ref={videoRef}
                      autoPlay
                      playsInline
                      muted
                      onLoadedData={handleVideoReady}
                      style={{
                        display: "block",
                        width: "100%",
                        maxHeight: "260px",
                        minHeight: "220px",
                        objectFit: "cover",
                        background: "#0f1720",
                      }}
                    />
                  ) : (
                    <div
                      style={{
                        minHeight: "220px",
                        display: "grid",
                        placeItems: "center",
                        color: "#5b6b61",
                        lineHeight: 1.6,
                        padding: "0 18px",
                        textAlign: "center",
                      }}
                    >
                      桌機會直接使用瀏覽器攝影機。手機瀏覽器也可以直接拍照。
                    </div>
                  )}
                </div>

                <canvas ref={canvasRef} style={{ display: "none" }} />
              </div>
            )}

            <div style={{ color: "#5b6b61" }}>
              {file ? `已選擇：${file.name}` : inputMode === "camera" ? "拍照完成後會自動帶入圖片。" : "支援從裝置選擇既有圖片。"}
            </div>

            {previewUrl ? (
              <div style={previewFrameStyle}>
                <img
                  src={previewUrl}
                  alt="餐盤預覽"
                  style={{ display: "block", width: "100%", maxHeight: "300px", objectFit: "cover" }}
                />
              </div>
            ) : (
              <div
                style={{
                  ...inputStyle,
                  ...(fileHasError ? errorInputStyle : {}),
                  minHeight: "96px",
                  display: "grid",
                  placeItems: "center",
                  color: "#5b6b61",
                  borderStyle: "dashed",
                }}
              >
                尚未選擇圖片
              </div>
            )}
            {fileHasError ? (
              <div style={{ color: "#d14343", fontSize: "0.9rem", fontWeight: 600 }}>
                請先選擇圖片。
              </div>
            ) : null}
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
            onChange={(event) => {
              setWeight(event.target.value);
              setWeightTouched(true);
              if (event.target.value && Number(event.target.value) > 0) {
                onErrorChange("");
              }
            }}
            onBlur={() => setWeightTouched(true)}
            placeholder="例如 350"
            style={weightHasError ? { ...inputStyle, ...errorInputStyle } : inputStyle}
          />
          {weightHasError ? (
            <div style={{ color: "#d14343", fontSize: "0.9rem", fontWeight: 600 }}>
              請輸入大於 0 的整盤廚餘重量。
            </div>
          ) : null}
        </div>

        <button type="submit" disabled={loading} style={buttonStyle(loading)}>
          {loading ? "分析中..." : "開始分析"}
        </button>
      </form>
    </section>
  );
}

function waitForVideoReady(video) {
  if (video.readyState >= 2 && video.videoWidth > 0 && video.videoHeight > 0 && video.currentTime > 0) {
    return Promise.resolve();
  }

  return new Promise((resolve) => {
    const onReady = () => {
      if (!(video.videoWidth > 0 && video.videoHeight > 0 && video.currentTime > 0)) {
        return;
      }
      video.removeEventListener("loadeddata", onReady);
      video.removeEventListener("playing", onReady);
      resolve();
    };
    video.addEventListener("loadeddata", onReady);
    video.addEventListener("playing", onReady);
  });
}
