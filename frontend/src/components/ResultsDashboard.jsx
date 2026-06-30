import VerdictBadge from './VerdictBadge'
import DimensionScores from './DimensionScores'
import RiskFlags from './RiskFlags'
import RewritePanel from './RewritePanel'

const PLATFORM_LABELS = {
  linkedin: 'LinkedIn',
  x: 'X / Twitter',
  facebook: 'Facebook',
  instagram: 'Instagram',
}

export default function ResultsDashboard({ result, originalDraft }) {
  const { platform, risks, fit, rewrite } = result

  return (
    <div className="results-dashboard">
      <div className="results-header">
        <h2 className="results-title">Preflight Report</h2>
        <span className="results-platform">{PLATFORM_LABELS[platform] || platform}</span>
      </div>

      <VerdictBadge verdict={fit.verdict} overallScore={fit.overallScore} />

      <div className="results-grid">
        <div className="results-col">
          <RiskFlags risks={risks} />
          <DimensionScores dimensions={fit.dimensions} />
        </div>
        <div className="results-col">
          <RewritePanel rewrite={rewrite} originalDraft={originalDraft} />
        </div>
      </div>
    </div>
  )
}
