import { useEffect, useState } from 'react'
import api from '../lib/api'

export default function DashboardPage() {
  const [stats, setStats] = useState(null)
  const [notifications, setNotifications] = useState([])
  const [error, setError] = useState(null)

  useEffect(() => {
    async function loadData() {
      try {
        const [statsResponse, notificationsResponse] = await Promise.all([
          api.get('/stats'),
          api.get('/notifications'),
        ])
        setStats(statsResponse.data)
        setNotifications(notificationsResponse.data)
      } catch (err) {
        setError(err.response?.data?.detail || 'Unable to load dashboard data.')
      }
    }

    loadData()
  }, [])

  return (
    <div className="space-y-6">
      <section className="rounded-xl bg-white p-6 shadow-sm">
        <h2 className="text-2xl font-semibold">Dashboard</h2>
        <p className="mt-2 text-slate-600">View complaint analytics and your latest notifications.</p>
      </section>

      {error && <div className="rounded-xl bg-rose-50 p-4 text-rose-700">{error}</div>}

      <section className="grid gap-4 md:grid-cols-2">
        <div className="rounded-xl bg-white p-6 shadow-sm">
          <h3 className="text-lg font-semibold">Complaint metrics</h3>
          {stats ? (
            <div className="mt-4 space-y-3 text-sm text-slate-700">
              <div>Total complaints: {stats.total_complaints}</div>
              <div>Status counts:</div>
              <ul className="ml-4 list-disc">
                {Object.entries(stats.status_counts || {}).map(([status, count]) => (
                  <li key={status}>{status}: {count}</li>
                ))}
              </ul>
              <div>Priority counts:</div>
              <ul className="ml-4 list-disc">
                {Object.entries(stats.priority_counts || {}).map(([priority, count]) => (
                  <li key={priority}>{priority}: {count}</li>
                ))}
              </ul>
            </div>
          ) : (
            <div className="mt-4 text-slate-500">Loading analytics...</div>
          )}
        </div>

        <div className="rounded-xl bg-white p-6 shadow-sm">
          <h3 className="text-lg font-semibold">Notifications</h3>
          {notifications.length === 0 ? (
            <p className="mt-4 text-slate-500">No notifications yet.</p>
          ) : (
            <ul className="mt-4 space-y-3 text-sm text-slate-700">
              {notifications.map((item) => (
                <li key={item.id} className="rounded-2xl border border-slate-200 p-3">
                  <div>{item.message}</div>
                  <div className="mt-1 text-xs text-slate-500">{new Date(item.created_at).toLocaleString()}</div>
                </li>
              ))}
            </ul>
          )}
        </div>
      </section>
    </div>
  )
}
