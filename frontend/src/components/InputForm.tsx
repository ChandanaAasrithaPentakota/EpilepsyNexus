import { useState, FormEvent } from 'react'

type Props = {
  onSubmit: (mri: File, eeg: File, symptoms: string) => void
  loading: boolean
}

export default function InputForm({ onSubmit, loading }: Props) {
  const [mri, setMri] = useState<File | null>(null)
  const [eeg, setEeg] = useState<File | null>(null)
  const [symptoms, setSymptoms] = useState('')

  function handleSubmit(e: FormEvent) {
    e.preventDefault()
    if (!mri || !eeg || !symptoms.trim()) return
    onSubmit(mri, eeg, symptoms)
  }

  return (
    <form className="input-form" onSubmit={handleSubmit}>
      <div className="field">
        <label>MRI Image</label>
        <input
          type="file"
          accept="image/*"
          required
          onChange={e => setMri(e.target.files?.[0] ?? null)}
        />
        {mri && <span className="file-name">{mri.name}</span>}
      </div>

      <div className="field">
        <label>EEG File (.txt)</label>
        <input
          type="file"
          accept=".txt"
          required
          onChange={e => setEeg(e.target.files?.[0] ?? null)}
        />
        {eeg && <span className="file-name">{eeg.name}</span>}
      </div>

      <div className="field">
        <label>Symptoms</label>
        <textarea
          rows={4}
          required
          placeholder="Describe the patient's symptoms..."
          value={symptoms}
          onChange={e => setSymptoms(e.target.value)}
        />
      </div>

      <button type="submit" disabled={loading || !mri || !eeg || !symptoms.trim()}>
        {loading ? 'Analyzing...' : 'Run Analysis'}
      </button>
    </form>
  )
}
