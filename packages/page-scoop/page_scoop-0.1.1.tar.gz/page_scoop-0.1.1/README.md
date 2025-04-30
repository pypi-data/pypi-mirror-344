# Page Scoop

A command-line tool for capturing HTML content and screenshots from web pages using browserless.

## Features

- Capture HTML content from any URL
- Take screenshots with customizable options:
  - Multiple formats (PNG, JPEG, WEBP)
  - Adjustable viewport size
  - Full-page capture
  - Image quality control
- Configurable through:
  - Command-line arguments
  - Environment variables
  - Configuration file

## Installation

```bash
uv tool install page-scoop
```

## Requirements

- Python 3.10 or higher
- A browserless instance (self-hosted or cloud service)

## Configuration

You can configure page-scoop using one of these methods:

1. Command-line arguments
2. Environment variables
3. Configuration file

### Configuration File

Create a configuration file (`~/.config/page-scoop/config.json`) with the following structure:

```json
{
    "browserless_url": "your-browserless-url",
    "token": "your-auth-token",
    "cf_client_id": "your-cloudflare-client-id",
    "cf_client_secret": "your-cloudflare-client-secret"
}
```

## Usage

### Capture HTML

```bash
page-scoop html https://example.com
```

Options:
- `--browserless-url`: Browserless instance URL
- `--token`: Auth token for browserless
- `--output`: Save HTML to file instead of stdout
- `--timeout`: HTTP request timeout in seconds
- `--wait-for`: Wait for selector to appear before capture
- `--wait-time`: Wait time in milliseconds before capture

### Take Screenshot

```bash
page-scoop screenshot https://example.com --output screenshot.png
```

Options:
- `--browserless-url`: Browserless instance URL
- `--token`: Auth token for browserless
- `--output`: Path to save screenshot file
- `--timeout`: HTTP request timeout in seconds
- `--width`: Viewport width
- `--height`: Viewport height
- `--full-page`: Capture full page height
- `--format`: Screenshot format (png, jpeg, webp)
- `--quality`: Image quality (for JPEG/WEBP)
- `--wait-for`: Wait for selector to appear before capture
- `--wait-time`: Wait time in milliseconds before capture
- `--overwrite`: Overwrite existing file if it exists

### Create/Update Configuration

```bash
page-scoop config --browserless-url your-url --token your-token
```

Options:
- `--browserless-url`: Browserless instance URL
- `--token`: Auth token for browserless
- `--cf-client-id`: Cloudflare Access client ID
- `--cf-client-secret`: Cloudflare Access client secret
- `--update`: Update existing config file

## Environment Variables

- `BROWSERLESS_URL`: Browserless instance URL
- `BROWSERLESS_TOKEN`: Auth token for browserless
- `CF_CLIENT_ID`: Cloudflare Access client ID
- `CF_CLIENT_SECRET`: Cloudflare Access client secret
