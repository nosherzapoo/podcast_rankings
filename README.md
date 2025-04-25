# Podcast Rankings Scraper

This project automatically scrapes Apple Podcasts and Spotify top podcast rankings on a weekly basis, every Sunday.

## Features

- Scrapes Apple Podcasts top 100 rankings
- Scrapes Spotify Podcasts top 100 rankings
- Runs weekly as a GitHub Action (every Sunday)
- Emails results in CSV format
- Archives results as GitHub Actions artifacts

## Setup Instructions

To set up the automated scraper with email delivery:

1. Fork or clone this repository to your GitHub account
2. Navigate to your repository's Settings > Secrets and Variables > Actions
3. Add the following secrets for email configuration:

| Secret Name | Description |
|-------------|-------------|
| `MAIL_SERVER` | SMTP server address (e.g., smtp.gmail.com) |
| `MAIL_PORT` | SMTP server port (e.g., 587 for TLS) |
| `MAIL_USERNAME` | Email username/address to send from |
| `MAIL_PASSWORD` | Email password or app password |
| `EMAIL_TO` | Email address to send reports to |

### Email Provider Notes

**For Gmail**:
- Use `smtp.gmail.com` as server and port `587`
- You'll need to create an "App Password" instead of using your regular password
- Instructions: Google Account > Security > 2-Step Verification > App Passwords

**For Outlook/Office 365**:
- Use `smtp.office365.com` as server and port `587`

## Manual Trigger

You can manually trigger the workflow:

1. Go to the "Actions" tab in your repository
2. Select the "Weekly Podcast Rankings Scraper" workflow
3. Click "Run workflow"

## CSV Output Format

The workflow generates two CSV files:

1. `apple_podcast_rankings_YYYY-MM-DD.csv`
2. `spotify_podcast_rankings_YYYY-MM-DD.csv`

These files contain rankings, podcast titles, publishers, and additional metadata.

## Local Usage

To run the scrapers locally:

```bash
# Install dependencies
pip install requests pandas beautifulsoup4

# Run scrapers
python apple_scraper.py
python spotify_scraper.py
``` 