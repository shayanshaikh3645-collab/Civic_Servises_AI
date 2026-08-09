import { useState } from 'react'
import api from '../lib/api'

export default function ComplaintPage() {
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [address, setAddress] = useState('')
  const [message, setMessage] = useState(null)
  const [error, setError] = useState(null)

  const handleSubmit = async (event) => {
    event.preventDefault()
    setMessage(null)
    setError(null)

    try {
      await api.post('/complaints', { title, description, address })
      setMessage('Complaint submitted successfully.')
      setTitle('')
      setDescription('')
      setAddress('')
    } catch (err) {
      setError(err.response?.data?.detail || 'Unable to submit complaint.')
    }
  }

  return (
    <div className="max-w-2xl rounded-xl bg-white p-6 shadow-sm">
      <h2 className="text-2xl font-semibold">Submit a complaint</h2>
      <p className="mt-2 text-slate-600">Describe the issue and the location so the right department can respond.</p>

      <form className="mt-6 space-y-4" onSubmit={handleSubmit}>
        <div>
          <label className="block text-sm font-medium text-slate-700">Issue title</label>
          <input
            value={title}
            onChange={(event) => setTitle(event.target.value)}
            className="mt-1 w-full rounded-xl border border-slate-300 bg-slate-50 p-3 focus:border-slate-500 focus:outline-none"
            placeholder="e.g. Pothole near bus stop"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700">Description</label>
          <textarea
            value={description}
            onChange={(event) => setDescription(event.target.value)}
            className="mt-1 w-full rounded-xl border border-slate-300 bg-slate-50 p-3 focus:border-slate-500 focus:outline-none"
            rows="4"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700">Address</label>
          <input
            value={address}
            onChange={(event) => setAddress(event.target.value)}
            className="mt-1 w-full rounded-xl border border-slate-300 bg-slate-50 p-3 focus:border-slate-500 focus:outline-none"
            placeholder="Optional address or landmark"
          />
        </div>

        <button
          type="submit"
          className="rounded-xl bg-slate-900 px-5 py-3 text-white transition hover:bg-slate-700"
        >
          Submit Complaint
        </button>

        {message && <p className="text-sm text-green-700">{message}</p>}
        {error && <p className="text-sm text-red-700">{error}</p>}
      </form>
    </div>
  )
}
