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
    throw new Error(payload.detail || payload.error || "Request failed");
  }

  return payload;
}
