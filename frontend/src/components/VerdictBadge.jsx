const VERDICT_CONFIG = {
  ready: { label: 'Ready to Publish', emoji: '🟢', className: 'verdict--ready' },
  needs_work: { label: 'Needs Work', emoji: '🟡', className: 'verdict--needs-work' },
  risky: { label: 'Risky', emoji: '🔴', className: 'verdict--risky' },
}

export default function VerdictBadge({ verdict, overallScore }) {
  const config = VERDICT_CONFIG[verdict] || VERDICT_CONFIG.needs_work

  return (
    <div className={`verdict-badge ${config.className}`}>
      <div className="verdict-left">
        <span className="verdict-emoji">{config.emoji}</span>
        <div>
          <div className="verdict-label">{config.label}</div>
          <div className="verdict-sub">Overall platform fit</div>
        </div>
      </div>
      <div className="verdict-score">
        <span className="score-number">{overallScore}</span>
        <span className="score-max">/100</span>
      </div>
    </div>
  )
}
