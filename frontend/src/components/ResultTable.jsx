// Result table component for View C — lists detected foods, weights, and carbon emissions.
// Supports sorting on numeric columns; default: confidence descending.

import { useMemo, useState } from "react";

// ─── Styles ───────────────────────────────────────────────────────────────────

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

/** Base th style for all columns */
const thBaseStyle = {
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
  justifyContent: "center",
  textAlign: "center",
  padding: "6px 14px",
  borderRadius: "999px",
  fontSize: "0.875rem",
  fontWeight: 900,
  color: matched ? "#065f46" : "#92400e",
  background: matched ? "#d1fae5" : "#fef3c7",
});

// ─── Sortable column definitions ──────────────────────────────────────────────

/**
 * Columns that support sorting.
 * key: corresponds to item field name (or custom accessor defined in sortValue).
 */
const SORTABLE_KEYS = new Set([
  "confidence",
  "area",
  "density_factor",
  "estimated_weight_g",
  "carbon_factor",
  "carbon_emission_kg",
]);

/** Fallback value for fields that may be null/undefined (treated as -Infinity so they sink to bottom) */
const sortValue = (item, key) => {
  const raw = item[key];
  const n = Number(raw);
  return isNaN(n) ? -Infinity : n;
};

// ─── SortArrow sub-component ──────────────────────────────────────────────────

/**
 * Renders an up/down chevron icon.
 * - Visible when the column is the active sort key, OR when the user is hovering.
 * - Direction: active sort direction if active, otherwise defaults to "desc" (down).
 *
 * @param {{ isActive: boolean, isHovered: boolean, dir: "asc"|"desc" }} props
 */
function SortArrow({ isActive, isHovered, dir }) {
  const visible = isActive || isHovered;
  // When hovered but not active, show the default "down" hint
  const displayDir = isActive ? dir : "desc";

  return (
    <span
      aria-hidden="true"
      style={{
        display: "inline-flex",
        alignItems: "center",
        marginLeft: "5px",
        // NOTE: 用 opacity + scale 做平滑的淡入淡出，避免 layout shift
        opacity: visible ? 1 : 0,
        transform: visible ? "scale(1)" : "scale(0.6)",
        transition: "opacity 0.18s ease, transform 0.18s ease",
        pointerEvents: "none",
        verticalAlign: "middle",
        position: "relative",
        zIndex: 1,
      }}
    >
      {displayDir === "desc" ? (
        // Down chevron
        <svg width="13" height="13" viewBox="0 0 13 13" fill="none">
          <path d="M2.5 4.5L6.5 8.5L10.5 4.5" stroke="#111827" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      ) : (
        // Up chevron
        <svg width="13" height="13" viewBox="0 0 13 13" fill="none">
          <path d="M2.5 8.5L6.5 4.5L10.5 8.5" stroke="#111827" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      )}
    </span>
  );
}

// ─── SortableTh sub-component ─────────────────────────────────────────────────

/**
 * A <th> that shows a sort arrow on hover/active.
 * Clicking toggles between desc → asc → desc.
 * Includes ripple effect and prevents rapid clicks on the same column.
 *
 * @param {{ colKey: string, label: string, sortKey: string, sortDir: "asc"|"desc", onSort: (key: string) => void }} props
 */
function SortableTh({ colKey, label, sortKey, sortDir, onSort }) {
  const [hovered, setHovered] = useState(false);
  const [ripples, setRipples] = useState([]);
  const [isAnimating, setIsAnimating] = useState(false);

  const isActive = sortKey === colKey;
  const RIPPLE_DURATION = 600;

  const handleClick = (e) => {
    // NOTE: 若點擊的是目前正在排序的欄位，且水波紋尚未結束，則忽略此次點擊
    if (isActive && isAnimating) return;

    const rect = e.currentTarget.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const width = rect.width;
    const height = rect.height;
    const maxRadius = Math.sqrt(Math.pow(width, 2) + Math.pow(height, 2));

    const newRipple = { x, y, size: maxRadius * 2, id: Date.now() };
    setRipples((prev) => [...prev, newRipple]);
    setIsAnimating(true);

    setTimeout(() => {
      setRipples((prev) => prev.filter((r) => r.id !== newRipple.id));
      setIsAnimating(false);
    }, RIPPLE_DURATION);

    // NOTE: 點擊後立即觸發排序，不需等待動畫結束
    onSort(colKey);
  };

  return (
    <th
      style={{
        ...thBaseStyle,
        padding: "8px 0", // 減少外層 th 的 padding，將空間轉移給內層膠囊
      }}
    >
      <div
        style={{
          display: "inline-flex",
          alignItems: "center",
          padding: "8px 12px",
          borderRadius: "24px",
          cursor: "pointer",
          userSelect: "none",
          position: "relative",
          overflow: "hidden",
          // NOTE: 有 active sort 或 hover 時稍微加深背景做視覺回饋
          background: isActive || hovered ? "rgba(0,0,0,0.06)" : "transparent",
          transition: "background 0.15s ease",
          animation: isAnimating ? "morphShape 0.6s ease-in-out" : "none",
        }}
        onClick={handleClick}
        onMouseEnter={() => setHovered(true)}
        onMouseLeave={() => setHovered(false)}
      >
        <span style={{ position: "relative", zIndex: 1 }}>{label}</span>
        <SortArrow isActive={isActive} isHovered={hovered} dir={sortDir} />
        
        {ripples.map((r) => (
          <span
            key={r.id}
            className="ripple-effect"
            style={{
              left: r.x,
              top: r.y,
              width: r.size,
              height: r.size,
            }}
          />
        ))}
      </div>
    </th>
  );
}

// ─── Main component ───────────────────────────────────────────────────────────

/**
 * ResultTable — recognition result table shown in View C.
 * Default sort: confidence descending.
 */
export default function ResultTable({ items }) {
  const [sortKey, setSortKey] = useState("confidence");
  const [sortDir, setSortDir] = useState("desc");

  /** Toggle sort: same column flips direction; new column resets to desc. */
  const handleSort = (key) => {
    if (!SORTABLE_KEYS.has(key)) return;
    if (sortKey === key) {
      setSortDir(sortDir === "desc" ? "asc" : "desc");
    } else {
      setSortKey(key);
      setSortDir("desc");
    }
  };

  const sortedItems = useMemo(() => {
    if (!items?.length) return [];
    return [...items].sort((a, b) => {
      const va = sortValue(a, sortKey);
      const vb = sortValue(b, sortKey);
      return sortDir === "desc" ? vb - va : va - vb;
    });
  }, [items, sortKey, sortDir]);

  /** Shared props passed to every SortableTh */
  const sortProps = { sortKey, sortDir, onSort: handleSort };

  return (
    <div style={wrapperStyle}>
      <style>{`
        @keyframes morphShape {
          0% { border-radius: 24px; transform: scale(1); }
          50% { border-radius: 8px; transform: scale(0.95); }
          100% { border-radius: 24px; transform: scale(1); }
        }
      `}</style>
      <h2 style={{ marginBottom: "24px", fontSize: "1.5rem", fontWeight: 900, color: "#111827" }}>
        辨識結果
      </h2>
      <table style={tableStyle}>
        <thead>
          <tr>
            {/* Non-sortable columns */}
            <th style={thBaseStyle}>食物</th>
            <th style={thBaseStyle}>YOLO Label</th>
            <th style={thBaseStyle}>碳排狀態</th>
            {/* Sortable columns */}
            <SortableTh colKey="confidence"        label="信心值"         {...sortProps} />
            <SortableTh colKey="area"              label="面積"           {...sortProps} />
            <SortableTh colKey="density_factor"    label="密度係數"       {...sortProps} />
            <SortableTh colKey="estimated_weight_g" label="推估重量 (g)"  {...sortProps} />
            <SortableTh colKey="carbon_factor"     label="碳排係數"       {...sortProps} />
            <SortableTh colKey="carbon_emission_kg" label="碳排量 (kg)"   {...sortProps} />
          </tr>
        </thead>
        <tbody>
          {sortedItems.length === 0 ? (
            <tr>
              <td style={{ ...tdStyle, color: "#9ca3af", textAlign: "center" }} colSpan={9}>
                尚無分析結果。
              </td>
            </tr>
          ) : (
            sortedItems.map((item, index) => (
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
