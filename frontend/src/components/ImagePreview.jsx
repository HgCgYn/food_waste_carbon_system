// Image preview card for View C — exact match for design 6.png.

const cardStyle = {
  background: "#f3f4f6", // Very light gray
  borderRadius: "24px",
  overflow: "hidden",
  display: "flex",
  flexDirection: "column",
};

const titleStyle = {
  padding: "24px 32px 16px",
  fontSize: "1.5rem",
  fontWeight: 900,
  color: "#111827",
  margin: 0,
};

const placeholderStyle = {
  width: "100%",
  aspectRatio: "4/3",
  display: "grid",
  placeItems: "center",
  color: "#6b7280",
  fontSize: "1.125rem",
  fontWeight: 700,
  background: "#e5e7eb",
};

/**
 * ImagePreview — displays a labelled image card.
 */
export default function ImagePreview({ title, imageBase64 }) {
  return (
    <div style={cardStyle}>
      <p style={titleStyle}>{title}</p>
      {imageBase64 ? (
        <img
          src={`data:image/jpeg;base64,${imageBase64}`}
          alt={title}
          style={{ display: "block", width: "100%", height: "auto", objectFit: "contain" }}
        />
      ) : (
        <div style={placeholderStyle}>尚無圖片</div>
      )}
    </div>
  );
}
