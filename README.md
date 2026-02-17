# Test RUM App - Datadog APM Instrumented Python App

A plug-and-play Flask application fully instrumented with Datadog APM, running alongside the Datadog Agent via Docker Compose.

## Quick Start

1. **Copy the environment file and add your Datadog API key:**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` and set `DD_API_KEY` to your actual Datadog API key.

2. **Start everything:**

   ```bash
   docker compose up --build
   ```

3. **Visit the app:**

   Open [http://localhost:8080](http://localhost:8080) to see all available endpoints.

4. **View traces in Datadog:**

   Go to [APM > Traces](https://app.datadoghq.com/apm/traces) in your Datadog account.

## Endpoints

| Endpoint    | Description                                                  |
|-------------|--------------------------------------------------------------|
| `/`         | Lists all available endpoints                                |
| `/hello`    | Simple traced endpoint                                       |
| `/slow`     | Simulates a slow request (0.5–2s delay)                      |
| `/external` | Makes an outbound HTTP call to httpbin.org                   |
| `/chain`    | Chains multiple custom-traced operations with nested spans   |
| `/error`    | Triggers an exception (`?type=value\|runtime\|zero`)         |
| `/health`   | Health check                                                 |

## What Gets Traced

- **Flask HTTP requests** — automatic instrumentation via `ddtrace-run`
- **Outbound HTTP calls** — automatic instrumentation of the `requests` library
- **Custom spans** — manual spans in the `/chain` endpoint
- **Errors** — error tracking with span tags on the `/error` endpoint
- **Profiling** — continuous profiling enabled via `DD_PROFILING_ENABLED`

## Configuration

All configuration is via environment variables in `.env`:

| Variable     | Default            | Description                     |
|-------------|--------------------|---------------------------------|
| `DD_API_KEY` | (required)         | Your Datadog API key            |
| `DD_SITE`    | `datadoghq.com`    | Datadog site (e.g. `datadoghq.eu`) |
| `DD_ENV`     | `dev`              | Environment tag for traces      |

## Stopping

```bash
docker compose down
```
