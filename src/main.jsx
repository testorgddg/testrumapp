import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { datadogRum } from '@datadog/browser-rum'

// Initialize Datadog RUM
datadogRum.init({
  applicationId: '6a95f9f6-a637-4977-a5da-9738a40fe887',
  clientToken: 'pub39026c483a155e18a6d3091d05004edf',
  site: 'datad0g.com',
  service: 'test-rum-app',
  env: 'development',
  version: '1.0.0',
  sessionSampleRate: 100,
  sessionReplaySampleRate: 100,
  trackUserInteractions: true,
  trackResources: true,
  trackLongTasks: true,
  defaultPrivacyLevel: 'mask-user-input'
})

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
