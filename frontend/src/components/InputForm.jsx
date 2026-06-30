import { useState } from 'react'

const PLATFORMS = [
  { value: 'linkedin', label: 'LinkedIn' },
  { value: 'x', label: 'X / Twitter' },
  { value: 'facebook', label: 'Facebook' },
  { value: 'instagram', label: 'Instagram' },
]

export default function InputForm({ onAnalyze, loading }) {
  const [draft, setDraft] = useState('')
  const [platform, setPlatform] = useState('linkedin')
  const [showContext, setShowContext] = useState(false)
  const [audience, setAudience] = useState('')
  const [goal, setGoal] = useState('')
  const [brandTone, setBrandTone] = useState('')

  function handleSubmit(e) {
    e.preventDefault()
    if (!draft.trim()) return

    const context = {}
    if (audience.trim()) context.audience = audience.trim()
    if (goal.trim()) context.goal = goal.trim()
    if (brandTone.trim()) context.brandTone = brandTone.trim()

    onAnalyze({
      draft: draft.trim(),
      platform,
      context: Object.keys(context).length ? context : undefined,
    })
  }

  const charCount = draft.length

  return (
    <form className="input-form" onSubmit={handleSubmit}>
      <div className="form-section">
        <label className="form-label" htmlFor="draft">
          Your draft post
        </label>
        <textarea
          id="draft"
          className="draft-textarea"
          placeholder="Paste your draft post here…"
          value={draft}
          onChange={e => setDraft(e.target.value)}
          rows={8}
          disabled={loading}
        />
        <div className="char-count">{charCount} characters</div>
      </div>

      <div className="form-row">
        <div className="form-section form-section--platform">
          <label className="form-label" htmlFor="platform">
            Target platform
          </label>
          <div className="platform-select-wrapper">
            <select
              id="platform"
              className="platform-select"
              value={platform}
              onChange={e => setPlatform(e.target.value)}
              disabled={loading}
            >
              {PLATFORMS.map(p => (
                <option key={p.value} value={p.value}>{p.label}</option>
              ))}
            </select>
          </div>
        </div>

        <div className="form-section form-section--context-toggle">
          <label className="form-label">&nbsp;</label>
          <button
            type="button"
            className="toggle-context-btn"
            onClick={() => setShowContext(v => !v)}
            disabled={loading}
          >
            {showContext ? '− Hide context' : '+ Add context (optional)'}
          </button>
        </div>
      </div>

      {showContext && (
        <div className="context-fields">
          <div className="form-section">
            <label className="form-label" htmlFor="audience">Target audience</label>
            <input
              id="audience"
              type="text"
              className="context-input"
              placeholder="e.g. B2B SaaS founders"
              value={audience}
              onChange={e => setAudience(e.target.value)}
              disabled={loading}
            />
          </div>
          <div className="form-section">
            <label className="form-label" htmlFor="goal">Goal / CTA</label>
            <input
              id="goal"
              type="text"
              className="context-input"
              placeholder="e.g. drive demo signups"
              value={goal}
              onChange={e => setGoal(e.target.value)}
              disabled={loading}
            />
          </div>
          <div className="form-section">
            <label className="form-label" htmlFor="brandTone">Brand tone</label>
            <input
              id="brandTone"
              type="text"
              className="context-input"
              placeholder="e.g. confident but credible"
              value={brandTone}
              onChange={e => setBrandTone(e.target.value)}
              disabled={loading}
            />
          </div>
        </div>
      )}

      <button
        type="submit"
        className="analyze-btn"
        disabled={loading || !draft.trim()}
      >
        {loading ? 'Analyzing…' : '✈️ Run Preflight Check'}
      </button>
    </form>
  )
}
