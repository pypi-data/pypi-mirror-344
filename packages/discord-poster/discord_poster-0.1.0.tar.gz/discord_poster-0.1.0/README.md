# Discord Poster

A lightweight Python client to post messages to a Discord webhook.

## Setting up Webhooks

For information on creating Discord webhooks, see Discord's documentation [here](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks).

## Features
- Simple and lightweight
- Supports optional error logging and exception raising
- Custom exception class for better error handling
- Built-in request timeout (10 seconds)

## Installation

```bash
pip install discord-poster
```

## Usage

```python
from discord_poster import DiscordPoster

dp = DiscordPoster(webhook_url="my-webhook-url")
dp.post_to_discord(message="Hello from Discord Poster 😎")
```