# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "typer",
#     "httpx",
#     "rich",
#     "pydantic",
# ]
# ///

import importlib.metadata
import json
import os
from enum import Enum
from pathlib import Path
from typing import Annotated, Any, Dict, Optional

import httpx
import typer
from pydantic import BaseModel, Field
from rich.console import Console


class Config(BaseModel):
    browserless_url: Optional[str] = Field(None, description="URL of the browserless instance")
    token: Optional[str] = Field(None, description="Auth token for browserless")
    cf_client_id: Optional[str] = Field(None, description="Cloudflare Access client ID")
    cf_client_secret: Optional[str] = Field(None, description="Cloudflare Access client secret")


class ScreenshotFormat(str, Enum):
    PNG = "png"
    JPEG = "jpeg"
    WEBP = "webp"


app = typer.Typer(
    help="A CLI tool to capture HTML or screenshots using browserless",
    rich_markup_mode="rich",
)


def version_callback(value: bool):
    if value:
        try:
            __version__ = importlib.metadata.version("page-scoop")
        except importlib.metadata.PackageNotFoundError:
            __version__ = "dev"
        print(__version__)
        raise typer.Exit()


@app.callback()
def main(
    _: Annotated[Optional[bool], typer.Option("--version", callback=version_callback)] = None,
): ...


console = Console()


def load_config() -> Config:
    """Load config from ~/.config/page-scoop/config.json if it exists."""
    config_path = Path.home() / ".config" / "page-scoop" / "config.json"
    if config_path.exists():
        try:
            with open(config_path, "r") as f:
                config_data = json.load(f)
            return Config(**config_data)
        except (json.JSONDecodeError, IOError) as e:
            console.print(f"[yellow]Warning: Failed to load config file: {e}[/yellow]")
    return Config()


def get_setting(cli_value: Optional[str], env_var: str, config_value: Optional[str]) -> Optional[str]:
    """Get a setting value from CLI argument, environment variable, or config file in that order."""
    if cli_value is not None:
        return cli_value
    env_value = os.environ.get(env_var)
    if env_value:
        return env_value
    return config_value


def make_browserless_request(
    endpoint: str,
    url: str,
    browserless_url: str,
    token: Optional[str] = None,
    cf_client_id: Optional[str] = None,
    cf_client_secret: Optional[str] = None,
    timeout: int = 30,
    **kwargs,
) -> httpx.Response:
    """Make a request to browserless service."""
    headers = {
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
    }
    params = {}

    # Add token as query param if provided
    if token:
        params["token"] = token

    # Add Cloudflare Access headers if provided
    if cf_client_id and cf_client_secret:
        headers["CF-Access-Client-Id"] = cf_client_id
        headers["CF-Access-Client-Secret"] = cf_client_secret

    # Construct the JSON payload
    payload = {"url": url, **kwargs}

    # Make the request
    with httpx.Client(timeout=timeout, follow_redirects=True) as client:
        return client.post(
            f"{browserless_url.rstrip('/')}/{endpoint}",
            json=payload,
            headers=headers,
            params=params,
        )


@app.command("html")
def get_html(
    url: Annotated[str, typer.Argument(help="URL to capture HTML from")],
    browserless_url: Annotated[Optional[str], typer.Option(help="Browserless instance URL")] = None,
    token: Annotated[Optional[str], typer.Option(help="Auth token for browserless")] = None,
    cf_client_id: Annotated[Optional[str], typer.Option(help="Cloudflare Access client ID")] = None,
    cf_client_secret: Annotated[Optional[str], typer.Option(help="Cloudflare Access client secret")] = None,
    output: Annotated[Optional[Path], typer.Option(help="Save HTML to file instead of stdout")] = None,
    timeout: Annotated[int, typer.Option(help="HTTP request timeout in seconds")] = 30,
    wait_for: Annotated[Optional[str], typer.Option(help="Wait for selector to appear before capture")] = None,
    wait_time: Annotated[int, typer.Option(help="Wait time in milliseconds before capture")] = 0,
):
    """Capture HTML content from a URL using browserless."""
    config = load_config()

    # Get settings from CLI args, env vars, or config file
    browserless_url = get_setting(browserless_url, "BROWSERLESS_URL", config.browserless_url)
    token = get_setting(token, "BROWSERLESS_TOKEN", config.token)
    cf_client_id = get_setting(cf_client_id, "CF_CLIENT_ID", config.cf_client_id)
    cf_client_secret = get_setting(cf_client_secret, "CF_CLIENT_SECRET", config.cf_client_secret)

    if not browserless_url:
        console.print("[bold red]Error: Browserless URL is required[/bold red]")
        raise typer.Exit(1)

    try:
        payload: Dict[str, Any] = {}
        if wait_for:
            payload["waitForSelector"] = wait_for
        if wait_time > 0:
            payload["waitTime"] = wait_time

        response = make_browserless_request(
            "content",
            url,
            browserless_url,
            token,
            cf_client_id,
            cf_client_secret,
            timeout,
            **payload,
        )
        response.raise_for_status()

        html_content = response.text

        if output:
            output.parent.mkdir(parents=True, exist_ok=True)
            with open(output, "w", encoding="utf-8") as f:
                f.write(html_content)
            console.print(f"[green]HTML saved to [bold]{output}[/bold][/green]")
        else:
            print(html_content)

    except httpx.HTTPStatusError as e:
        console.print(f"[bold red]HTTP Error: {e.response.status_code} - {e.response.text}[/bold red]")
        raise typer.Exit(1)
    except httpx.RequestError as e:
        console.print(f"[bold red]Request Error: {e}[/bold red]")
        raise typer.Exit(1)


@app.command("screenshot")
def take_screenshot(
    url: Annotated[str, typer.Argument(help="URL to screenshot")],
    browserless_url: Annotated[Optional[str], typer.Option(help="Browserless instance URL")] = None,
    token: Annotated[Optional[str], typer.Option(help="Auth token for browserless")] = None,
    cf_client_id: Annotated[Optional[str], typer.Option(help="Cloudflare Access client ID")] = None,
    cf_client_secret: Annotated[Optional[str], typer.Option(help="Cloudflare Access client secret")] = None,
    output: Annotated[Path, typer.Option(help="Path to save screenshot file")] = Path("screenshot.png"),
    timeout: Annotated[int, typer.Option(help="HTTP request timeout in seconds")] = 30,
    width: Annotated[int, typer.Option(help="Viewport width")] = 1280,
    height: Annotated[int, typer.Option(help="Viewport height")] = 800,
    full_page: Annotated[bool, typer.Option(help="Capture full page height")] = False,
    format: Annotated[ScreenshotFormat, typer.Option(help="Screenshot format")] = ScreenshotFormat.PNG,
    quality: Annotated[int, typer.Option(min=0, max=100, help="Image quality (for JPEG/WEBP)")] = 80,
    wait_for: Annotated[Optional[str], typer.Option(help="Wait for selector to appear before capture")] = None,
    wait_time: Annotated[int, typer.Option(help="Wait time in milliseconds before capture")] = 0,
    overwrite: Annotated[bool, typer.Option(help="Overwrite existing file if it exists")] = False,
):
    """Capture a screenshot of a URL using browserless."""
    config = load_config()

    # Get settings from CLI args, env vars, or config file
    browserless_url = get_setting(browserless_url, "BROWSERLESS_URL", config.browserless_url)
    token = get_setting(token, "BROWSERLESS_TOKEN", config.token)
    cf_client_id = get_setting(cf_client_id, "CF_CLIENT_ID", config.cf_client_id)
    cf_client_secret = get_setting(cf_client_secret, "CF_CLIENT_SECRET", config.cf_client_secret)

    if not browserless_url:
        console.print("[bold red]Error: Browserless URL is required[/bold red]")
        raise typer.Exit(1)

    try:
        payload = {
            "options": {
                "fullPage": full_page,
                "type": format,
                "quality": quality if format != ScreenshotFormat.PNG else None,
            },
            "viewport": {
                "width": width,
                "height": height,
            },
        }

        if wait_for:
            payload["waitForSelector"] = wait_for
        if wait_time > 0:
            payload["waitTime"] = wait_time

        response = make_browserless_request(
            "screenshot",
            url,
            browserless_url,
            token,
            cf_client_id,
            cf_client_secret,
            timeout,
            **payload,
        )
        response.raise_for_status()

        # Check if file exists and handle accordingly
        if output.exists() and not overwrite:
            console.print(
                f"[bold red]Error: File [bold]{output}[/bold] already exists. Use --overwrite to overwrite it.[/bold red]"
            )
            raise typer.Exit(1)

        # Save the image data directly
        output.parent.mkdir(parents=True, exist_ok=True)
        with open(output, "wb") as f:
            f.write(response.content)

        console.print(f"[green]Screenshot saved to [bold]{output}[/bold][/green]")

    except httpx.HTTPStatusError as e:
        console.print(f"[bold red]HTTP Error: {e.response.status_code} - {e.response.text}[/bold red]")
        raise typer.Exit(1)
    except httpx.RequestError as e:
        console.print(f"[bold red]Request Error: {e}[/bold red]")
        raise typer.Exit(1)


@app.command("config")
def create_config(
    browserless_url: Annotated[Optional[str], typer.Option(help="Browserless instance URL")] = None,
    token: Annotated[Optional[str], typer.Option(help="Auth token for browserless")] = None,
    cf_client_id: Annotated[Optional[str], typer.Option(help="Cloudflare Access client ID")] = None,
    cf_client_secret: Annotated[Optional[str], typer.Option(help="Cloudflare Access client secret")] = None,
    update: Annotated[bool, typer.Option(help="Update existing config file")] = False,
):
    """Create or update the config file with browserless settings."""
    config_path = Path.home() / ".config" / "page-scoop" / "config.json"

    # Check if config exists
    if config_path.exists() and not update:
        console.print("[yellow]Config file already exists. Use --update to modify it.[/yellow]")
        raise typer.Exit(1)

    # Create config directory if it doesn't exist
    config_path.parent.mkdir(parents=True, exist_ok=True)

    # Load existing config if updating
    existing_config = {}
    if config_path.exists() and update:
        try:
            with open(config_path, "r") as f:
                existing_config = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            console.print(f"[yellow]Warning: Failed to load existing config: {e}[/yellow]")

    # Update config with new values
    config_data = {
        **existing_config,
        **{
            k: v
            for k, v in {
                "browserless_url": browserless_url,
                "token": token,
                "cf_client_id": cf_client_id,
                "cf_client_secret": cf_client_secret,
            }.items()
            if v is not None
        },
    }

    # Save config
    try:
        with open(config_path, "w") as f:
            json.dump(config_data, f, indent=2)
        console.print(f"[green]Config saved to [bold]{config_path}[/bold][/green]")
    except IOError as e:
        console.print(f"[bold red]Error saving config: {e}[/bold red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
