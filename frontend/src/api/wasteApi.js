// Frontend API client that submits multipart form data to the FastAPI detect endpoint.

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export async function detectWaste(file, totalWeightG) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("total_weight_g", totalWeightG);

  const response = await fetch(`${API_BASE_URL}/api/detect`, {
    method: "POST",
    body: formData,
  });

  const payload = await response.json();
  if (!response.ok) {
    throw new Error(extractErrorMessage(payload));
  }

  return payload;
}

function extractErrorMessage(payload) {
  if (!payload) {
    return "Request failed";
  }

  if (typeof payload.detail === "string" && payload.detail) {
    return payload.detail;
  }

  if (Array.isArray(payload.detail) && payload.detail.length > 0) {
    const first = payload.detail[0];
    if (typeof first === "string") {
      return first;
    }
    if (first?.msg) {
      return first.msg;
    }
  }

  if (typeof payload.error === "string" && payload.error) {
    return payload.error;
  }

  return "分析失敗，請檢查圖片與輸入欄位。";
}
