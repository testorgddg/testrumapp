# Test React App with Datadog RUM

A simple React application instrumented with Datadog Real User Monitoring (RUM) SDK.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Configure Datadog RUM:
   - Open `src/main.jsx`
   - Replace `YOUR_APPLICATION_ID` with your Datadog Application ID
   - Replace `YOUR_CLIENT_TOKEN` with your Datadog Client Token
   - Update the `site` value if needed (e.g., 'datadoghq.eu', 'us3.datadoghq.com', etc.)

## Getting Datadog Credentials

1. Log in to your Datadog account
2. Navigate to UX Monitoring > RUM Applications
3. Create a new application or select an existing one
4. Copy the Application ID and Client Token from the instrumentation page

## Running the App

```bash
npm run dev
```

The app will be available at `http://localhost:5173`

## Datadog RUM Features Enabled

- Session Recording (100% sample rate)
- User Interaction Tracking
- Resource Tracking
- Long Task Tracking
- Privacy Level: mask-user-input

## Learn More

- [Datadog RUM Documentation](https://docs.datadoghq.com/real_user_monitoring/)
- [Vite Documentation](https://vitejs.dev/)
- [React Documentation](https://react.dev/)
