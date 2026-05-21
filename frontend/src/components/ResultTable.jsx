// Result table component that lists detected foods, weights, and carbon emissions.

const wrapperStyle = {
  background: "rgba(255,255,255,0.82)",
  borderRadius: "24px",
  padding: "24px",
  boxShadow: "0 20px 50px rgba(53, 78, 55, 0.12)",
  overflowX: "auto",
};

const tableStyle = {
  width: "100%",
  borderCollapse: "collapse",
};

const cellStyle = {
  textAlign: "left",
  padding: "12px 10px",
  borderBottom: "1px solid #d7e1d3",
  fontSize: "0.95rem",
};

const statusStyle = (matched) => ({
  display: "inline-flex",
  alignItems: "center",
  padding: "4px 10px",
  borderRadius: "999px",
  fontSize: "0.8rem",
  fontWeight: 700,
  color: matched ? "#0f5132" : "#8a4b08",
  background: matched ? "#d9f2e3" : "#f8e2bf",
});

export default function ResultTable({ items }) {
  return (
    <section style={wrapperStyle}>
      <h2 style={{ marginTop: 0 }}>辨識結果</h2>
      <table style={tableStyle}>
        <thead>
          <tr>
            <th style={cellStyle}>食物</th>
            <th style={cellStyle}>YOLO Label</th>
            <th style={cellStyle}>碳排狀態</th>
            <th style={cellStyle}>信心值</th>
            <th style={cellStyle}>面積</th>
            <th style={cellStyle}>密度係數</th>
            <th style={cellStyle}>推估重量(g)</th>
            <th style={cellStyle}>碳排係數</th>
            <th style={cellStyle}>碳排量(kg)</th>
          </tr>
        </thead>
        <tbody>
          {items.length === 0 ? (
            <tr>
              <td style={cellStyle} colSpan={9}>
                尚無分析結果。
              </td>
            </tr>
          ) : (
            items.map((item, index) => (
              <tr key={`${item.yolo_label}-${index}`}>
                <td style={cellStyle}>{item.food_name_zh}</td>
                <td style={cellStyle}>{item.label_name}</td>
                <td style={cellStyle}>
                  <span style={statusStyle(item.has_carbon_data)}>
                    {item.has_carbon_data ? "已對應碳排" : "無碳排資料"}
                  </span>
                </td>
                <td style={cellStyle}>{Number(item.confidence).toFixed(3)}</td>
                <td style={cellStyle}>{Number(item.area).toFixed(2)}</td>
                <td style={cellStyle}>{Number(item.density_factor).toFixed(3)}</td>
                <td style={cellStyle}>{Number(item.estimated_weight_g).toFixed(2)}</td>
                <td style={cellStyle}>
                  {item.has_carbon_data ? Number(item.carbon_factor).toFixed(3) : "-"}
                </td>
                <td style={cellStyle}>
                  {item.has_carbon_data ? Number(item.carbon_emission_kg).toFixed(6) : "-"}
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </section>
  );
}
