import { useState } from 'react'
import InputForm from './components/InputForm'
import ResultPanel from './components/ResultPanel'
import './App.css'

export type AnalysisResult = {
  symptoms_text: string
  mri_epilepsy_label: string
  seizure_phase: string
  seizure_type: string
  epilepsy_presence: string
  fusion_explanation: string
  medical_context: string
  neuro_diagnostic_report: string
  patient_explanation: string
  safety_passed: boolean
  safety_notes: string
}

export default function App() {
  const [result, setResult] = useState<AnalysisResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit(mri: File, eeg: File, symptoms: string) {
    setLoading(true)
    setError(null)
    setResult(null)

    const form = new FormData()
    form.append('mri', mri)
    form.append('eeg', eeg)
    form.append('symptoms', symptoms)

    try {
      const res = await fetch('/analyze', { method: 'POST', body: form })
      if (!res.ok) {
        const err = await res.json()
        throw new Error(err.detail || 'Server error')
      }
      setResult(await res.json())
    } catch (e: any) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header>
        <h1>EpilepsyNexus</h1>
        <p>Multimodal AI-assisted epilepsy screening</p>
      </header>
      <main>
        <InputForm onSubmit={handleSubmit} loading={loading} />
        {error && <div className="error-banner">{error}</div>}
        {result && <ResultPanel result={result} />}
      </main>
    </div>
  )
}
