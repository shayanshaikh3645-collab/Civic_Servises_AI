import { useEffect, useState } from 'react'
import { Routes, Route, Link, useNavigate, Navigate } from 'react-router-dom'
import HomePage from './pages/HomePage'
import ComplaintPage from './pages/ComplaintPage'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import DashboardPage from './pages/DashboardPage'
import { getUser, isAuthenticated, logout } from './lib/auth'

function ProtectedRoute({ children }) {
  if (!isAuthenticated()) {
    return <Navigate to="/login" replace state={{ message: 'Please sign in to continue.' }} />
  }
  return children
}

function RedirectIfAuthenticated({ children }) {
  if (isAuthenticated()) {
    return <Navigate to="/dashboard" replace state={{ message: 'You are already signed in.' }} />
  }
  return children
}

function App() {
  const [user, setUser] = useState(getUser())
  const navigate = useNavigate()

  useEffect(() => {
    const handleAuthChange = () => setUser(getUser())
    window.addEventListener('auth-change', handleAuthChange)
    return () => window.removeEventListener('auth-change', handleAuthChange)
  }, [])

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <header className="border-b bg-white/90 py-4 shadow-sm">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-4">
          <div>
            <h1 className="text-xl font-semibold">AI Smart Civic Services</h1>
            <p className="text-sm text-slate-600">Submit complaints and track service response.</p>
          </div>
          <nav className="flex items-center gap-4 text-sm">
            <Link className="text-slate-700 hover:text-slate-900" to="/">Home</Link>
            <Link className="text-slate-700 hover:text-slate-900" to="/complaint">Submit</Link>
            {user ? (
              <>
                <Link className="text-slate-700 hover:text-slate-900" to="/dashboard">Dashboard</Link>
                <button onClick={handleLogout} className="rounded-lg bg-slate-900 px-4 py-2 text-white hover:bg-slate-700">
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link className="text-slate-700 hover:text-slate-900" to="/login">Login</Link>
                <Link className="text-slate-700 hover:text-slate-900" to="/register">Register</Link>
              </>
            )}
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-6xl px-4 py-8">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/complaint" element={<ProtectedRoute><ComplaintPage /></ProtectedRoute>} />
          <Route path="/login" element={<RedirectIfAuthenticated><LoginPage /></RedirectIfAuthenticated>} />
          <Route path="/register" element={<RedirectIfAuthenticated><RegisterPage /></RedirectIfAuthenticated>} />
          <Route path="/dashboard" element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
        </Routes>
      </main>
    </div>
  )
}

export default App
