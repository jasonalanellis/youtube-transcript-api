# YouTube Indexsy Daily Summarizer

Automatically summarizes new videos from [Indexsy](https://www.youtube.com/@indexsy) and emails you the insights.

## Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ n8n         │───▶│ YouTube     │───▶│ Transcript  │───▶│ Claude API  │───▶ Email
│ (Schedule)  │    │ RSS Feed    │    │ API (local) │    │             │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

## Setup

### 1. Start the Transcript API

```bash
cd ~/youtube-summarizer
pip install -r requirements.txt
python transcript_api.py
```

Test it works:
```bash
curl http://localhost:5111/health
curl http://localhost:5111/transcript/dQw4w9WgXcQ  # Test with any video ID
```

For production, run with gunicorn:
```bash
gunicorn -w 2 -b 0.0.0.0:5111 transcript_api:app
```

### 2. Import the n8n Workflow

1. Open n8n
2. Go to Workflows → Import from File
3. Select `n8n-workflow.json`
4. Update credentials:
   - **Anthropic API Key**: Create HTTP Header Auth credential with `x-api-key` header
   - **Gmail**: Connect your Gmail OAuth2 credential
5. Update email recipient in "Send Email Summary" node
6. Activate the workflow

### 3. Keep Transcript API Running

Option A - tmux/screen:
```bash
tmux new -s transcript-api
python transcript_api.py
# Ctrl+B, D to detach
```

Option B - systemd service (Linux):
```bash
# Create /etc/systemd/system/transcript-api.service
sudo systemctl enable transcript-api
sudo systemctl start transcript-api
```

Option C - launchd (macOS):
See `com.youtube.transcript-api.plist` if created

## Configuration

### Change the YouTube Channel

Edit `n8n-workflow.json` and replace the channel ID in the RSS URL:
```
https://www.youtube.com/feeds/videos.xml?channel_id=YOUR_CHANNEL_ID
```

To find a channel ID: Go to channel page → View Source → Search for "channelId"

### Adjust Time Window

In the "Parse RSS & Filter Recent" node, change `7` to your preferred number of days:
```javascript
const sevenDaysAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);
```

## Files

- `transcript_api.py` - Flask API for fetching YouTube transcripts
- `requirements.txt` - Python dependencies
- `n8n-workflow.json` - Importable n8n workflow
- `README.md` - This file

## Channel Info

- **Channel**: Indexsy (Jacky Chou)
- **Channel ID**: UCS1LT_WoYAIHW5KcUNxXYEw
- **RSS Feed**: https://www.youtube.com/feeds/videos.xml?channel_id=UCS1LT_WoYAIHW5KcUNxXYEw
