// Result table component for View C — lists detected foods, weights, and carbon emissions.

const wrapperStyle = {
  background: "#f3f4f6",
  borderRadius: "24px",
  padding: "32px 40px",
  overflowX: "auto",
};

const tableStyle = {
  width: "100%",
  borderCollapse: "collapse",
};

const thStyle = {
  textAlign: "left",
  padding: "16px 12px",
  borderBottom: "2px solid #d1d5db",
  fontSize: "1.125rem",
  fontWeight: 900,
  color: "#111827",
  whiteSpace: "nowrap",
};

const tdStyle = {
  textAlign: "left",
  padding: "16px 12px",
  borderBottom: "1px solid #e5e7eb",
  fontSize: "1.125rem",
  color: "#374151",
  fontWeight: 600,
};

const statusStyle = (matched) => ({
  display: "inline-flex",
  alignItems: "center",
  padding: "6px 14px",
  borderRadius: "999px",
  fontSize: "0.875rem",
  fontWeight: 900,
  color: matched ? "#065f46" : "#92400e",
  background: matched ? "#d1fae5" : "#fef3c7",
});

/**
 * ResultTable — recognition result table shown in View C.
 */
export default function ResultTable({ items }) {
  return (
    <div style={wrapperStyle}>
      <h2 style={{ marginBottom: "24px", fontSize: "1.5rem", fontWeight: 900, color: "#111827" }}>
        辨識結果
      </h2>
      <table style={tableStyle}>
        <thead>
          <tr>
            <th style={thStyle}>食物</th>
            <th style={thStyle}>YOLO Label</th>
            <th style={thStyle}>碳排狀態</th>
            <th style={thStyle}>信心值</th>
            <th style={thStyle}>面積</th>
            <th style={thStyle}>密度係數</th>
            <th style={thStyle}>推估重量 (g)</th>
            <th style={thStyle}>碳排係數</th>
            <th style={thStyle}>碳排量 (kg)</th>
          </tr>
        </thead>
        <tbody>
          {items.length === 0 ? (
            <tr>
              <td style={{ ...tdStyle, color: "#9ca3af", textAlign: "center" }} colSpan={9}>
                尚無分析結果。
              </td>
            </tr>
          ) : (
            items.map((item, index) => (
              <tr key={`${item.yolo_label}-${index}`}>
                <td style={{ ...tdStyle, fontWeight: 900, color: "#111827" }}>{item.food_name_zh}</td>
                <td style={tdStyle}>{item.label_name}</td>
                <td style={tdStyle}>
                  <span style={statusStyle(item.has_carbon_data)}>
                    {item.has_carbon_data ? "已對應碳排" : "無碳排資料"}
                  </span>
                </td>
                <td style={tdStyle}>{Number(item.confidence).toFixed(3)}</td>
                <td style={tdStyle}>{Number(item.area).toFixed(2)}</td>
                <td style={tdStyle}>{Number(item.density_factor).toFixed(3)}</td>
                <td style={tdStyle}>{Number(item.estimated_weight_g).toFixed(2)}</td>
                <td style={tdStyle}>
                  {item.has_carbon_data ? Number(item.carbon_factor).toFixed(3) : "—"}
                </td>
                <td style={{ ...tdStyle, color: item.has_carbon_data ? "#065f46" : "#374151" }}>
                  {item.has_carbon_data ? Number(item.carbon_emission_kg).toFixed(6) : "—"}
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}
