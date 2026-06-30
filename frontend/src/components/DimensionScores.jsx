import { useState } from 'react'

function scoreColor(score) {
  if (score >= 75) return '#22c55e'
  if (score >= 50) return '#f59e0b'
  return '#ef4444'
}

function DimensionRow({ dim }) {
  const [expanded, setExpanded] = useState(false)
  const color = scoreColor(dim.score)

  return (
    <div className="dimension-row">
      <button
        className="dimension-header"
        onClick={() => setExpanded(v => !v)}
        type="button"
      >
        <span className="dimension-label">{dim.label}</span>
        <div className="dimension-bar-wrap">
          <div className="dimension-bar-bg">
            <div
              className="dimension-bar-fill"
              style={{ width: `${dim.score}%`, background: color }}
            />
          </div>
          <span className="dimension-score" style={{ color }}>{dim.score}</span>
        </div>
        <span className="dimension-chevron">{expanded ? '▲' : '▼'}</span>
      </button>
      {expanded && (
        <div className="dimension-detail">
          <p className="dimension-comment">{dim.comment}</p>
          {dim.suggestion && (
            <p className="dimension-suggestion">
              <strong>Suggestion:</strong> {dim.suggestion}
            </p>
          )}
        </div>
      )}
    </div>
  )
}

export default function DimensionScores({ dimensions }) {
  return (
    <div className="dimension-scores">
      <h3 className="section-title">Platform Fit — Dimensions</h3>
      <div className="dimensions-list">
        {dimensions.map(dim => (
          <DimensionRow key={dim.key} dim={dim} />
        ))}
      </div>
      <p className="dimension-hint">Click a dimension to see details and suggestions.</p>
    </div>
  )
}
