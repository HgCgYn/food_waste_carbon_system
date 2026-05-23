import { useState } from "react";

/**
 * Button component with a ripple effect on click.
 * Wraps standard button props and styles.
 * @param {boolean} delayAction — 若為 true，onClick 會等到水波紋動畫結束後才觸發
 */
export default function Button({ children, style, onClick, delayAction, ...props }) {
  const [ripples, setRipples] = useState([]);

  /** 水波紋動畫時長（ms），與 CSS ripple-animation 的 duration 一致 */
  const RIPPLE_DURATION = 600;

  const handleClick = (e) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    // Calculate maximum distance to corners for perfect ripple size
    const width = rect.width;
    const height = rect.height;
    const maxRadius = Math.sqrt(Math.pow(width, 2) + Math.pow(height, 2));

    const newRipple = { x, y, size: maxRadius * 2, id: Date.now() };
    setRipples((prev) => [...prev, newRipple]);

    setTimeout(() => {
      setRipples((prev) => prev.filter((r) => r.id !== newRipple.id));
    }, RIPPLE_DURATION);

    if (onClick) {
      if (delayAction) {
        // NOTE: 等水波紋動畫完整播完後再觸發實際動作
        setTimeout(() => onClick(e), RIPPLE_DURATION);
      } else {
        onClick(e);
      }
    }
  };

  return (
    <button
      style={{
        position: "relative",
        overflow: "hidden",
        ...style,
      }}
      onClick={handleClick}
      {...props}
    >
      {children}
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
    </button>
  );
}
