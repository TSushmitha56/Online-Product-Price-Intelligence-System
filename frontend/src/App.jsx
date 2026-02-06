import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [backendMessage, setBackendMessage] = useState('')
  const [backendStatus, setBackendStatus] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    // Fetch data from backend Hello World endpoint
    fetch('http://localhost:8000/api/hello/')
      .then(response => {
        if (!response.ok) throw new Error('Backend not reachable')
        return response.json()
      })
      .then(data => {
        setBackendMessage(data.message)
        setBackendStatus(data.status)
        setError('')
      })
      .catch(err => {
        setError(`Backend Error: ${err.message}`)
        setBackendMessage('Backend not available')
        setBackendStatus('offline')
      })
      .finally(() => setLoading(false))
  }, [])

  return (
    <div className="container">
      <h1>🚀 Internship Project</h1>
      <div className="content">
        <h2>Frontend (React + Vite)</h2>
        <p>✅ Frontend is running!</p>
        
        <h2>Backend Status</h2>
        {loading && <p>⏳ Checking backend...</p>}
        {!loading && !error && (
          <div className="success">
            <p>✅ {backendMessage}</p>
            <p>Status: {backendStatus}</p>
          </div>
        )}
        {error && (
          <div className="error">
            <p>❌ {error}</p>
            <p>Make sure to run: <code>python manage.py runserver</code></p>
          </div>
        )}
        
        <div className="links">
          <a href="http://localhost:8000/api/hello/" target="_blank">Backend Hello World API</a>
          <a href="http://localhost:8000/api/health/" target="_blank">Health Check Endpoint</a>
        </div>
      </div>
    </div>
  )
}

export default App
