import { useState, useEffect } from 'react'
import axios from 'axios'
import './index.css'
import RunsList from './components/RunsList'
import RunDetail from './components/RunDetail'
import NewRunModal from './components/NewRunModal'
import WelcomeScreen from './components/WelcomeScreen'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default function App() {
  const [runs, setRuns] = useState([])
  const [selectedRun, setSelectedRun] = useState(null)
  const [showNewRun, setShowNewRun] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const fetchRuns = async () => {
    try {
      const res = await axios.get(`${API}/itr/runs`)
      setRuns(res.data)
    } catch (e) {
      console.error('Failed to fetch runs', e)
    }
  }

  useEffect(() => {
    fetchRuns()
    const interval = setInterval(fetchRuns, 5000)
    return () => clearInterval(interval)
  }, [])

  const handleSelectRun = async (runId) => {
    try {
      const res = await axios.get(`${API}/itr/runs/${runId}`)
      setSelectedRun(res.data)
    } catch (e) {
      setError('Failed to load run details')
    }
  }

  const handleNewRun = async (payload, mode) => {
    setLoading(true)
    setError(null)
    try {
      const res = await axios.post(`${API}/itr/upload`, payload, {
        headers: { 'Content-Type': 'multipart/form-data' },
        timeout: 120000,
      })
      await fetchRuns()
      setSelectedRun(res.data)
      setShowNewRun(false)
    } catch (e) {
      const detail = e.response?.data?.detail
      const msg = Array.isArray(detail) ? detail.join(' ') : (detail || '')
      if (!e.response) {
        setError('Cannot connect to server. Start the backend: cd backend && python -m uvicorn main:app --reload')
      } else {
        setError(msg || `Filing failed (${e.response?.status || 'error'})`)
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-container">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <div className="logo">
            <div className="logo-icon">🤖</div>
            <div className="logo-text">
              <h1>ITR CoPilot</h1>
              <p>Agentic Tax Filing AI</p>
            </div>
          </div>
          <div className="logo-badge">🇮🇳 India AY 2025-26</div>
        </div>

        <div className="sidebar-actions">
          <button className="btn-primary" onClick={() => setShowNewRun(true)}>
            📂 Upload & File ITR
          </button>
        </div>

        <div className="runs-list">
          <h3>Recent Filings</h3>
          {error && <div className="error-box" style={{ margin: '0 4px 12px' }}>{error}</div>}
          <RunsList
            runs={runs}
            selectedId={selectedRun?.run_id}
            onSelect={handleSelectRun}
          />
        </div>
      </aside>

      {/* Main */}
      <main className="main-content">
        {showNewRun ? (
          <NewRunModal
            onSubmit={handleNewRun}
            onClose={() => setShowNewRun(false)}
            loading={loading}
            error={error}
          />
        ) : selectedRun ? (
          <RunDetail run={selectedRun} />
        ) : (
          <WelcomeScreen
            onNew={() => setShowNewRun(true)}
            loading={loading}
          />
        )}
      </main>
    </div>
  )
}
