// KhanalChess bishop mark. Drawn as plain SVG shapes, so it is original
// artwork, renders the same on every device, and takes its colours from CSS:
//   fill        -> currentColor (the .logo colour, amber in style.css)
//   cross hole  -> .logo-cut    (set to the page background in style.css)
export default function Logo({ className = "logo", title }) {
  return (
    <svg
      className={className}
      viewBox="25 12 150 332"
      role={title ? "img" : undefined}
      aria-label={title}
      aria-hidden={title ? undefined : "true"}
      focusable="false"
    >
      <g fill="currentColor">
        <circle cx="100" cy="30" r="11" />
        <path d="M100 42C128 58 150 82 150 108C150 130 128 148 100 152C72 148 50 130 50 108C50 82 72 58 100 42Z" />
        <rect x="72" y="153" width="56" height="8" rx="3" />
        <rect x="62" y="165" width="76" height="12" rx="6" />
        <path d="M80 182L120 182C117 226 123 264 146 286L54 286C77 264 83 226 80 182Z" />
        <rect x="52" y="286" width="96" height="4" rx="1.5" />
        <path d="M41 316C41 302 52 294 64 294L136 294C148 294 159 302 159 316Z" />
        <rect x="33" y="321" width="134" height="16" rx="5" />
      </g>

      {/* soft shade on the right half */}
      <g fill="#000" opacity="0.13">
        <path d="M100 19A11 11 0 0 1 100 41Z" />
        <path d="M100 42C128 58 150 82 150 108C150 130 128 148 100 152Z" />
        <path d="M100 153H125A3 3 0 0 1 128 156V158A3 3 0 0 1 125 161H100Z" />
        <path d="M100 165H132A6 6 0 0 1 132 177H100Z" />
        <path d="M100 182H120C117 226 123 264 146 286H100Z" />
        <path d="M100 286H146.5A1.5 1.5 0 0 1 148 287.5V288.5A1.5 1.5 0 0 1 146.5 290H100Z" />
        <path d="M100 294H136C148 294 159 302 159 316H100Z" />
        <path d="M100 321H162A5 5 0 0 1 167 326V332A5 5 0 0 1 162 337H100Z" />
      </g>

      {/* highlights on the left */}
      <g fill="none" stroke="#fff" strokeLinecap="round" opacity="0.32">
        <path d="M64 106C64 90 72 76 84 66" strokeWidth="3.5" />
        <path d="M89 194C89 224 86 246 76 268" strokeWidth="3" />
      </g>

      {/* cross cut-out */}
      <g className="logo-cut">
        <rect x="95" y="64" width="10" height="52" />
        <rect x="80" y="80" width="40" height="10" />
      </g>
    </svg>
  );
}