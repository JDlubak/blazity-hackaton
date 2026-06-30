import { useState } from 'react'
import InputForm from './components/InputForm'
import ResultsDashboard from './components/ResultsDashboard'
import './App.css'

const MOCK_RESPONSE = {
  "platform": "linkedin",
  "risks": [
    {
      "span": "10x your output overnight, guaranteed",
      "category": "unverifiable_claim",
      "severity": "high",
      "reason": "Absolute performance guarantee with no evidence; reads as misleading and erodes credibility.",
      "suggestion": "Soften to a realistic, evidence-backed claim, e.g. 'helped teams cut drafting time by ~40%'."
    },
    {
      "span": "literally the best thing ever",
      "category": "brand_safety",
      "severity": "medium",
      "reason": "Hyperbole undercuts a credible B2B tone.",
      "suggestion": "Replace with a specific, concrete differentiator."
    }
  ],
  "fit": {
    "verdict": "needs_work",
    "overallScore": 54,
    "dimensions": [
      { "key": "length", "label": "Length & format", "score": 40, "comment": "Too short for LinkedIn; no structure or line breaks.", "suggestion": "Expand to 3-5 short paragraphs with a clear takeaway." },
      { "key": "tone", "label": "Tone", "score": 50, "comment": "Hype-heavy, low credibility for a B2B audience.", "suggestion": "Lead with a concrete result or insight." },
      { "key": "hook", "label": "Hook / opening", "score": 60, "comment": "Opening states the action but gives no reason to keep reading.", "suggestion": "Open with the problem it solves or a surprising stat." },
      { "key": "hashtags_emoji", "label": "Hashtags & emoji", "score": 55, "comment": "No hashtags; LinkedIn rewards 3-5 relevant ones.", "suggestion": "Add #AI #SaaS and 1-2 niche tags." },
      { "key": "cta", "label": "Call to action", "score": 65, "comment": "'DM me' is weak and high-friction.", "suggestion": "Use a clearer, lower-friction CTA." },
      { "key": "readability", "label": "Readability", "score": 55, "comment": "One dense block, hard to skim on mobile.", "suggestion": "Break into short lines." }
    ]
  },
  "rewrite": {
    "text": "We just shipped our new AI tool — and the early numbers surprised even us.\n\nTeams using it cut their content drafting time by ~40% in the first two weeks.\n\nNo magic, no overnight 10x. Just fewer hours lost to the blank page.\n\nCurious how it'd fit your workflow? Link in the comments. 👇\n\n#AI #SaaS #ContentMarketing",
    "summary": "Replaced hype and unverifiable guarantees with a concrete result, added structure, a credible CTA, and relevant hashtags for LinkedIn."
  }
}

const USE_MOCK = false

export default function App() {
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [originalDraft, setOriginalDraft] = useState('')

  async function handleAnalyze({ draft, platform, context }) {
    setLoading(true)
    setError(null)
    setResult(null)
    setOriginalDraft(draft)

    if (USE_MOCK) {
      await new Promise(r => setTimeout(r, 800))
      setResult(MOCK_RESPONSE)
      setLoading(false)
      return
    }

    try {
      const res = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ draft, platform, context }),
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.error || 'Analysis failed')
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-inner">
          <div className="logo">
            <span className="logo-icon">✈️</span>
            <span className="logo-text">Post Preflight</span>
          </div>
          <p className="tagline">Is your post ready to publish?</p>
        </div>
      </header>

      <main className="app-main">
        <InputForm onAnalyze={handleAnalyze} loading={loading} />

        {error && (
          <div className="error-banner">
            <span>⚠️</span> {error}
          </div>
        )}

        {loading && (
          <div className="loading-state">
            <div className="spinner" />
            <p>Analyzing your post…</p>
          </div>
        )}

        {result && !loading && (
          <ResultsDashboard result={result} originalDraft={originalDraft} />
        )}
      </main>
    </div>
  )
}
