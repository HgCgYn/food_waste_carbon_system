// Image preview component for showing base64-encoded detection and clustering outputs.

const wrapperStyle = {
  background: "rgba(255,255,255,0.82)",
  borderRadius: "24px",
  padding: "24px",
  boxShadow: "0 20px 50px rgba(53, 78, 55, 0.12)",
  display: "grid",
  gap: "16px",
};

export default function ImagePreview({ title, imageBase64 }) {
  const src = imageBase64 ? `data:image/jpeg;base64,${imageBase64}` : "";

  return (
    <section style={wrapperStyle}>
      <h2 style={{ margin: 0 }}>{title}</h2>
      {src ? (
        <img
          src={src}
          alt={title}
          style={{
            width: "100%",
            borderRadius: "18px",
            objectFit: "cover",
            minHeight: "260px",
            maxHeight: "520px",
          }}
        />
      ) : (
        <div
          style={{
            minHeight: "260px",
            borderRadius: "18px",
            border: "1px dashed #b5c4b3",
            display: "grid",
            placeItems: "center",
            color: "#5b6b61",
          }}
        >
          尚無圖片
        </div>
      )}
    </section>
  );
}
