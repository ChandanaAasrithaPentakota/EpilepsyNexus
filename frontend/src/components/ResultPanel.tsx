import { AnalysisResult } from '../App'

type Props = { result: AnalysisResult }

const badge = (val: string | boolean | null) => {
  if (val === 'yes' || val === true) return 'badge badge-red'
  if (val === 'no' || val === false) return 'badge badge-green'
  return 'badge badge-yellow'
}

// Bold any line that looks like a heading (ends with ":" or is ALL CAPS)
function formatReport(text: string) {
  return text.split('\n').map((line, i) => {
    const trimmed = line.trim()
    const isHeading =
      (trimmed.endsWith(':') && trimmed.length < 60) ||
      (trimmed === trimmed.toUpperCase() && trimmed.length > 2 && /[A-Z]/.test(trimmed))
    return isHeading
      ? <p key={i} style={{ fontWeight: 700, color: '#e2e8f0', marginTop: '0.8rem' }}>{line}</p>
      : <p key={i} style={{ marginLeft: '0.5rem', color: '#cbd5e1' }}>{line}</p>
  })
}

export default function ResultPanel({ result }: Props) {
  return (
    <div className="result-panel">

      {/* Summary row */}
      <div className="summary-row">
        <div className="summary-card">
          <span className="label">Epilepsy Presence</span>
          <span className={badge(result.epilepsy_presence)}>{result.epilepsy_presence ?? '—'}</span>
        </div>
        <div className="summary-card">
          <span className="label">Seizure Type</span>
          <span className="badge badge-blue">{result.seizure_type ?? '—'}</span>
        </div>
        <div className="summary-card">
          <span className="label">Seizure Phase</span>
          <span className="badge badge-blue">{result.seizure_phase ?? '—'}</span>
        </div>
        <div className="summary-card">
          <span className="label">Safety Check</span>
          <span className={badge(result.safety_passed)}>{result.safety_passed ? 'Passed' : 'Failed'}</span>
        </div>
      </div>

      {/* Neurologist report */}
      <section>
        <h2>Neurologist Style Diagnostic Report</h2>
        <div className="report-body">{formatReport(result.neuro_diagnostic_report ?? '')}</div>
      </section>

      {/* Patient explanation */}
      <section>
        <h2>Patient Explanation</h2>
        <p>{result.patient_explanation}</p>
      </section>

      {/* Safety notes */}
      {result.safety_notes && (
        <section>
          <h2>Safety Notes</h2>
          <p>{result.safety_notes}</p>
        </section>
      )}
    </div>
  )
}
