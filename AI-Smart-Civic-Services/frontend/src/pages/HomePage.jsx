import { useEffect, useState } from 'react'
import api from '../lib/api'

export default function HomePage() {
  const [complaints, setComplaints] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/complaints/public')
      .then((response) => setComplaints(response.data))
      .finally(() => setLoading(false))
  }, [])

  return (
    <div>
      <section className="mb-8 rounded-xl bg-white p-6 shadow-sm">
        <h2 className="text-2xl font-semibold">Latest complaints</h2>
        <p className="mt-2 text-slate-600">Review the most recent citizen reports and AI-suggested priority.</p>
      </section>
      <section className="grid gap-4">
        {loading ? (
          <div className="rounded-xl bg-slate-100 p-6 text-center">Loading complaints...</div>
        ) : complaints.length === 0 ? (
          <div className="rounded-xl bg-slate-100 p-6 text-center">No complaints submitted yet.</div>
        ) : (
          complaints.map((complaint) => (
            <div key={complaint.id} className="rounded-xl bg-white p-6 shadow-sm">
              <div className="flex items-center justify-between gap-4">
                <div>
                  <h3 className="text-lg font-semibold">{complaint.category}</h3>
                  <p className="text-slate-500">{complaint.address || 'Unknown address'}</p>
                </div>
                <span className="rounded-full bg-slate-100 px-3 py-1 text-sm text-slate-700">{complaint.priority}</span>
              </div>
              <p className="mt-4 text-slate-700">{complaint.description}</p>
            </div>
          ))
        )}
      </section>
    </div>
  )
}
