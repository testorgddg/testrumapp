#!/usr/bin/env bash
set -euo pipefail

export DATADOG_SITE="${DATADOG_SITE:-datad0g.com}"
SERVICE="${DATADOG_SERVICE:-test-rum-app}"
ENV="${DATADOG_ENV:-development}"
VERSION="${DATADOG_VERSION:-1.0.0}"
BUILD_DIR="dist"
MIN_JS_URL="${MIN_JS_URL:-/}"
REMOVE_SOURCEMAPS_AFTER_UPLOAD="${REMOVE_SOURCEMAPS_AFTER_UPLOAD:-true}"

if [ -z "${DATADOG_API_KEY:-}" ]; then
  echo "ERROR: DATADOG_API_KEY environment variable is required."
  echo ""
  echo "Usage:"
  echo "  DATADOG_API_KEY=<your-api-key> $0"
  echo ""
  echo "Optional environment variables:"
  echo "  DATADOG_SITE                     Datadog site (default: datad0g.com)"
  echo "  DATADOG_SERVICE                  Service name (default: test-rum-app)"
  echo "  DATADOG_ENV                      Environment (default: development)"
  echo "  DATADOG_VERSION                  Release version (default: 1.0.0)"
  echo "  MIN_JS_URL                       URL prefix where JS files are served (default: /)"
  echo "  REMOVE_SOURCEMAPS_AFTER_UPLOAD   Remove .map files after upload (default: true)"
  exit 1
fi

echo "==> Building application with sourcemaps..."
npx vite build

if [ ! -d "$BUILD_DIR" ]; then
  echo "ERROR: Build directory '$BUILD_DIR' not found. Build may have failed."
  exit 1
fi

JS_FILE_COUNT=$(find "$BUILD_DIR" -name '*.js.map' | wc -l | tr -d ' ')
if [ "$JS_FILE_COUNT" -eq 0 ]; then
  echo "ERROR: No sourcemap files found in '$BUILD_DIR'. Ensure sourcemaps are enabled in vite.config.js."
  exit 1
fi

echo "==> Found $JS_FILE_COUNT sourcemap file(s). Uploading to Datadog..."

npx datadog-ci sourcemaps upload "$BUILD_DIR" \
  --service="$SERVICE" \
  --release-version="$VERSION" \
  --minified-path-prefix="$MIN_JS_URL" \
  --project-path="./"

echo "==> Sourcemaps uploaded successfully."

if [ "$REMOVE_SOURCEMAPS_AFTER_UPLOAD" = "true" ]; then
  echo "==> Removing sourcemap files from build output..."
  find "$BUILD_DIR" -name '*.map' -delete
  echo "==> Sourcemap files removed."
fi

echo "==> Done. service=$SERVICE env=$ENV version=$VERSION site=$DATADOG_SITE"
