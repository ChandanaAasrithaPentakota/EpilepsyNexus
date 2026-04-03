import { AnalysisResult } from '../App'

type Props = { result: AnalysisResult }

const badge = (val: string | boolean | null) => {
  if (val === 'yes' || val === true) return 'badge badge-red'
  if (val === 'no' || val === false) return 'badge badge-green'
  return 'badge badge-yellow'
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
          <span className="label">MRI Finding</span>
          <span className={badge(result.mri_epilepsy_label === 'epilepsy' ? 'yes' : 'no')}>
            {result.mri_epilepsy_label ?? '—'}
          </span>
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

      {/* Fusion explanation */}
      <section>
        <h2>Multimodal Fusion</h2>
        <p>{result.fusion_explanation}</p>
      </section>

      {/* Neurologist report */}
      <section>
        <h2>Neurologist Report</h2>
        <pre>{result.neuro_diagnostic_report}</pre>
      </section>

      {/* Patient explanation */}
      <section>
        <h2>Patient Explanation</h2>
        <p>{result.patient_explanation}</p>
      </section>

      {/* Medical context */}
      <section>
        <h2>Medical Context (RAG)</h2>
        <pre>{result.medical_context}</pre>
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
