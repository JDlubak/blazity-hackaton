import { useMemo } from 'react'
import * as Diff from 'diff'

function buildHighlightedRewrite(original, rewritten) {
  const changes = Diff.diffWords(original, rewritten)
  return changes.map((part, i) => {
    if (part.added) {
      return <mark key={i} className="diff-added">{part.value}</mark>
    }
    if (part.removed) {
      return null
    }
    return <span key={i}>{part.value}</span>
  })
}

export default function RewritePanel({ rewrite, originalDraft }) {
  const highlighted = useMemo(
    () => buildHighlightedRewrite(originalDraft, rewrite.text),
    [originalDraft, rewrite.text]
  )

  return (
    <div className="rewrite-panel">
      <h3 className="section-title">✍️ Rewrite Proposal</h3>

      {rewrite.summary && (
        <p className="rewrite-summary">{rewrite.summary}</p>
      )}

      <div className="diff-legend">
        <span className="legend-item">
          <mark className="diff-added legend-swatch">highlighted</mark>
          = changed or added text
        </span>
      </div>

      <div className="rewrite-text">
        {highlighted}
      </div>

      <button
        className="copy-btn"
        type="button"
        onClick={() => navigator.clipboard.writeText(rewrite.text)}
      >
        📋 Copy rewrite
      </button>
    </div>
  )
}
