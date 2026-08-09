import { useEffect } from 'react'

export default function Toast({ message, onClose, type = 'info' }) {
  useEffect(() => {
    if (!message) return
    const timer = setTimeout(() => onClose?.(), 5000)
    return () => clearTimeout(timer)
  }, [message, onClose])

  if (!message) return null

  const colors = {
    info: 'bg-sky-50 text-sky-900 border-sky-200',
    success: 'bg-emerald-50 text-emerald-900 border-emerald-200',
    warning: 'bg-amber-50 text-amber-900 border-amber-200',
    error: 'bg-rose-50 text-rose-900 border-rose-200',
  }

  return (
    <div className={`relative rounded-xl border p-4 text-sm shadow-sm ${colors[type]}`}>
      <button
        type="button"
        onClick={() => onClose?.()}
        className="absolute right-3 top-3 rounded-full p-1 text-slate-500 hover:bg-slate-200 hover:text-slate-900"
        aria-label="Close notification"
      >
        ×
      </button>
      <p>{message}</p>
    </div>
  )
}
