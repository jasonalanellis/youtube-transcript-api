"""
Minimal YouTube Transcript API
Serves transcripts for n8n workflow consumption.

Run: python transcript_api.py
Endpoint: GET /transcript/<video_id>
"""

from flask import Flask, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

app = Flask(__name__)

# Initialize the API client (v1.x style)
yt_api = YouTubeTranscriptApi()

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/transcript/<video_id>")
def get_transcript(video_id):
    try:
        # v1.x API: use instance.fetch() method
        try:
            transcript = yt_api.fetch(video_id, languages=['en'])
        except NoTranscriptFound:
            transcript = yt_api.fetch(video_id)

        # Convert transcript snippets to plain text
        text = " ".join([entry.text for entry in transcript])

        return jsonify({
            "success": True,
            "video_id": video_id,
            "transcript": text,
            "word_count": len(text.split())
        })

    except TranscriptsDisabled:
        return jsonify({
            "success": False,
            "video_id": video_id,
            "error": "Transcripts are disabled for this video"
        }), 404

    except NoTranscriptFound:
        return jsonify({
            "success": False,
            "video_id": video_id,
            "error": "No transcript found for this video"
        }), 404

    except Exception as e:
        return jsonify({
            "success": False,
            "video_id": video_id,
            "error": str(e)
        }), 500

if __name__ == "__main__":
    print("Starting YouTube Transcript API on http://localhost:5111")
    print("Test with: curl http://localhost:5111/transcript/VIDEO_ID")
    app.run(host="0.0.0.0", port=5111)
