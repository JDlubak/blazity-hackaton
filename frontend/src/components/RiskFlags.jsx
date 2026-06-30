const SEVERITY_CONFIG = {
  high: { label: 'HIGH', className: 'severity--high', icon: '🔴' },
  medium: { label: 'MED', className: 'severity--medium', icon: '🟡' },
  low: { label: 'LOW', className: 'severity--low', icon: '🟢' },
}

const CATEGORY_LABELS = {
  hate_discrimination: 'Hate / Discrimination',
  sensitive_politics_religion: 'Politics / Religion',
  profanity: 'Profanity',
  unverifiable_claim: 'Unverifiable Claim',
  legal_compliance: 'Legal / Compliance',
  brand_safety: 'Brand Safety',
}

function RiskCard({ risk }) {
  const sev = SEVERITY_CONFIG[risk.severity] || SEVERITY_CONFIG.low

  return (
    <div className={`risk-card ${sev.className}`}>
      <div className="risk-card-header">
        <span className="risk-severity-badge">
          {sev.icon} {sev.label}
        </span>
        <span className="risk-category">{CATEGORY_LABELS[risk.category] || risk.category}</span>
      </div>
      <blockquote className="risk-span">"{risk.span}"</blockquote>
      <p className="risk-reason">{risk.reason}</p>
      {risk.suggestion && (
        <p className="risk-suggestion">
          <strong>Fix:</strong> {risk.suggestion}
        </p>
      )}
    </div>
  )
}

export default function RiskFlags({ risks }) {
  if (!risks || risks.length === 0) {
    return (
      <div className="risk-flags">
        <h3 className="section-title">Risk Flags</h3>
        <div className="no-risks">
          <span>✅</span>
          <p>No risk flags detected. Looks clean!</p>
        </div>
      </div>
    )
  }

  const highCount = risks.filter(r => r.severity === 'high').length
  const medCount = risks.filter(r => r.severity === 'medium').length

  return (
    <div className="risk-flags">
      <h3 className="section-title">
        Risk Flags
        <span className="risk-count-summary">
          {highCount > 0 && <span className="badge-high">{highCount} high</span>}
          {medCount > 0 && <span className="badge-medium">{medCount} medium</span>}
        </span>
      </h3>
      <div className="risk-list">
        {risks.map((risk, i) => (
          <RiskCard key={i} risk={risk} />
        ))}
      </div>
    </div>
  )
}
