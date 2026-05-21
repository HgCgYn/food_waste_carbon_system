// Summary card component that highlights total weight, waste ratio, and total carbon.

const cardStyle = {
  background: "#203a2a",
  color: "#f4f1e8",
  borderRadius: "24px",
  padding: "24px",
  display: "grid",
  gap: "16px",
  boxShadow: "0 20px 50px rgba(32, 58, 42, 0.22)",
};

const metricGridStyle = {
  display: "grid",
  gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))",
  gap: "12px",
};

const metricStyle = {
  background: "rgba(255,255,255,0.08)",
  borderRadius: "18px",
  padding: "16px",
};

export default function CarbonSummary({ result, loading, error }) {
  return (
    <section style={cardStyle}>
      <h2 style={{ margin: 0 }}>分析摘要</h2>
      <p style={{ margin: 0, lineHeight: 1.6 }}>
        {error
          ? error
          : loading
            ? "模型正在辨識食物與估算碳排。"
            : "分析完成後，這裡會顯示總重量、廚餘比例與總碳排放量。"}
      </p>
      <div style={metricGridStyle}>
        <div style={metricStyle}>
          <div>整盤重量</div>
          <strong>{Number(result?.total_weight_g ?? 0).toFixed(2)} g</strong>
        </div>
        <div style={metricStyle}>
          <div>廚餘比例</div>
          <strong>{Number(result?.waste_percentage ?? 0).toFixed(2)} %</strong>
        </div>
        <div style={metricStyle}>
          <div>總碳排量</div>
          <strong>{Number(result?.total_carbon_emission_kg ?? 0).toFixed(6)} kg</strong>
        </div>
        <div style={metricStyle}>
          <div>已對應項目</div>
          <strong>{Number(result?.matched_item_count ?? 0)}</strong>
        </div>
        <div style={metricStyle}>
          <div>未對應項目</div>
          <strong>{Number(result?.unmatched_item_count ?? 0)}</strong>
        </div>
      </div>
      <div style={metricGridStyle}>
        <div style={metricStyle}>
          <div>Food Area</div>
          <strong>{Number(result?.food_area ?? 0).toFixed(2)}</strong>
        </div>
        <div style={metricStyle}>
          <div>Garbage Area</div>
          <strong>{Number(result?.garbage_area ?? 0).toFixed(2)}</strong>
        </div>
        <div style={metricStyle}>
          <div>Plate Area</div>
          <strong>{Number(result?.plate_area ?? 0).toFixed(2)}</strong>
        </div>
      </div>
      {result ? (
        <p style={{ margin: 0, fontSize: "0.9rem", lineHeight: 1.6, color: "#dbe7d8" }}>
          未對應碳排資料的食物仍會被辨識並分配重量，但不會被計入總碳排。
        </p>
      ) : null}
    </section>
  );
}
