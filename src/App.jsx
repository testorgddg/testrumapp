import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { datadogRum } from '@datadog/browser-rum'

function App() {
  const [count, setCount] = useState(0)
  const [loading, setLoading] = useState(false)

  const handleClick = () => {
    setCount((count) => count + 1)
    datadogRum.addAction('button_click', { count: count + 1 })
  }

  const simulateApiCall = async () => {
    setLoading(true)
    datadogRum.addAction('api_call_started')

    try {
      await fetch('https://jsonplaceholder.typicode.com/posts/1')
      datadogRum.addAction('api_call_success')
    } catch (error) {
      datadogRum.addError(error)
    } finally {
      setLoading(false)
    }
  }

  const triggerCustomError = () => {
    datadogRum.addError(
      new Error('This is a test error for RUM tracking'),
      { context: 'user_triggered' }
    )
  }

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React + Datadog RUM</h1>
      <div className="card">
        <button onClick={handleClick}>
          count is {count}
        </button>
        <button onClick={simulateApiCall} disabled={loading}>
          {loading ? 'Loading...' : 'Test API Call'}
        </button>
        <button onClick={triggerCustomError}>
          Trigger Test Error
        </button>
        <p>
          This app is instrumented with Datadog RUM SDK.
          All user interactions, resources, and errors are being tracked.
        </p>
      </div>
      <p className="read-the-docs">
        Configure your Datadog credentials in <code>src/main.jsx</code>
      </p>
    </>
  )
}

export default App
