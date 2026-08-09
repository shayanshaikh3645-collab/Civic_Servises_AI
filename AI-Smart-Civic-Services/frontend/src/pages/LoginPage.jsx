import { useState } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import api from '../lib/api'
import { setToken, setUser } from '../lib/auth'
import Toast from '../components/Toast'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState(null)
  const location = useLocation()
  const navigate = useNavigate()
  const [redirectMessage, setRedirectMessage] = useState(location.state?.message || null)

  const handleSubmit = async (event) => {
    event.preventDefault()
    setError(null)

    try {
      const response = await api.post('/auth/token', new URLSearchParams({ username: email, password }).toString(), {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      })
      setToken(response.data.access_token)

      const userResponse = await api.get('/auth/me')
      setUser(userResponse.data)
      navigate('/dashboard')
    } catch (err) {
      setError(err.response?.data?.detail || 'Unable to login.')
    }
  }

  return (
    <div className="mx-auto max-w-xl rounded-xl bg-white p-6 shadow-sm">
      <h2 className="text-2xl font-semibold">Login</h2>
      <p className="mt-2 text-slate-600">Sign in to manage your complaints and view dashboard updates.</p>
      <Toast message={redirectMessage} type="warning" onClose={() => setRedirectMessage(null)} />
      <form onSubmit={handleSubmit} className="mt-6 space-y-4">
        <div>
          <label className="block text-sm font-medium text-slate-700">Email</label>
          <input
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            required
            className="mt-1 w-full rounded-xl border border-slate-300 bg-slate-50 p-3 focus:border-slate-500 focus:outline-none"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-700">Password</label>
          <input
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            required
            className="mt-1 w-full rounded-xl border border-slate-300 bg-slate-50 p-3 focus:border-slate-500 focus:outline-none"
          />
        </div>
        <button type="submit" className="rounded-xl bg-slate-900 px-5 py-3 text-white hover:bg-slate-700">
          Sign In
        </button>
        {error && <p className="text-sm text-red-700">{error}</p>}
      </form>
    </div>
  )
}
