from googleapiclient.discovery import build
from urllib.parse import urlparse, parse_qs

# -----------------------------
# CONFIGURATION
# -----------------------------

API_KEY = "YOUR_YOUTUBE_API_KEY"

# Estimated revenue per subscriber (example: $0.05 per subscriber)
REVENUE_PER_SUBSCRIBER = 0.05

YOUTUBE_URLS = [
    "https://www.youtube.com/@Google",
    "https://www.youtube.com/@OpenAI"
]

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------

def extract_channel_identifier(url):
    """
    Extracts a channel identifier from a YouTube URL.
    Supports:
    - /@handle
    - /channel/CHANNEL_ID
    """
    parsed = urlparse(url)
    path_parts = parsed.path.strip("/").split("/")

    if path_parts[0].startswith("@"):
        return ("forHandle", path_parts[0][1:])
    elif path_parts[0] == "channel":
        return ("id", path_parts[1])
    else:
        raise ValueError(f"Unsupported URL format: {url}")


def get_subscriber_count(youtube, identifier_type, identifier_value):
    """
    Fetches subscriber count using the YouTube Data API.
    """
    if identifier_type == "id":
        request = youtube.channels().list(
            part="statistics",
            id=identifier_value
        )
    else:
        request = youtube.channels().list(
            part="statistics",
            forHandle=identifier_value
        )

    response = request.execute()

    if not response["items"]:
        return None

    return int(response["items"][0]["statistics"]["subscriberCount"])


# -----------------------------
# MAIN LOGIC
# -----------------------------

def main():
    youtube = build("youtube", "v3", developerKey=API_KEY)

    for url in YOUTUBE_URLS:
        try:
            identifier_type, identifier_value = extract_channel_identifier(url)
            subscribers = get_subscriber_count(
                youtube,
                identifier_type,
                identifier_value
            )

            if subscribers is None:
                print(f"Could not fetch data for {url}")
                continue

            # Revenue estimation logic
            estimated_revenue = subscribers * REVENUE_PER_SUBSCRIBER

            print(f"Channel: {url}")
            print(f"Subscribers: {subscribers:,}")
            print(f"Estimated Revenue: ${estimated_revenue:,.2f}")
            print("-" * 40)

        except Exception as e:
            print(f"Error processing {url}: {e}")


if __name__ == "__main__":
    main()
