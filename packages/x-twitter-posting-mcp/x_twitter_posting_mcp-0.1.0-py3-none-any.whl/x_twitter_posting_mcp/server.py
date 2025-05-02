import os
import tweepy
import asyncio
from typing import List, Optional
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP, Context

# Load environment variables from .env file
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("x-twitter-posting-mcp")

# --- Twitter API Client Setup ---

def get_twitter_client() -> Optional[tweepy.Client]:
    """Initializes and returns a Tweepy Client using environment variables."""
    consumer_key = os.getenv("TWITTER_API_KEY")
    consumer_secret = os.getenv("TWITTER_API_KEY_SECRET")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

    if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
        print("Error: Twitter API credentials not found in environment variables.")
        print("Please set TWITTER_API_KEY, TWITTER_API_KEY_SECRET, TWITTER_ACCESS_TOKEN, and TWITTER_ACCESS_TOKEN_SECRET.")
        # In a real MCP server, you might want to raise an error or handle this differently
        return None

    try:
        client = tweepy.Client(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )
        # Verify credentials (optional but recommended)
        # client.get_me() # This call confirms authentication works
        return client
    except Exception as e:
        print(f"Error initializing Tweepy client: {e}")
        return None

# --- MCP Tools ---

@mcp.tool()
def post_tweet(text: str) -> str:
    """
    Posts a single tweet to X (Twitter).

    Args:
        text: The content of the tweet (max 280 characters).
    """
    client = get_twitter_client()
    if not client:
        return "Error: Twitter client not initialized. Check credentials."

    if len(text) > 280:
        return "Error: Tweet text exceeds 280 characters."
    if not text:
        return "Error: Tweet text cannot be empty."

    try:
        response = client.create_tweet(text=text)
        tweet_id = response.data.get('id')
        return f"Tweet posted successfully! ID: {tweet_id}"
    except tweepy.errors.TweepyException as e:
        return f"Error posting tweet: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

@mcp.tool()
async def post_thread(tweets: List[str]) -> str:
    """
    Posts a thread of tweets to X (Twitter).
    The first item in the list is the head tweet, subsequent items are replies.

    Args:
        tweets: A list of strings, where each string is the content of a tweet in the thread.
    """
    if not tweets:
        return "Error: No tweets provided for the thread."

    client = get_twitter_client()
    if not client:
        return "Error: Twitter client not initialized. Check credentials."

    last_tweet_id = None
    posted_ids = []

    try:
        # Post the first tweet
        first_tweet_text = tweets[0]
        if len(first_tweet_text) > 280:
             return f"Error: First tweet exceeds 280 characters."
        if not first_tweet_text:
            return f"Error: First tweet cannot be empty."

        response = client.create_tweet(text=first_tweet_text)
        last_tweet_id = response.data.get('id')
        posted_ids.append(last_tweet_id)
        print(f"Posted first tweet: {last_tweet_id}") # Log progress

        # Post subsequent tweets as replies
        for i, tweet_text in enumerate(tweets[1:], start=1):
            if len(tweet_text) > 280:
                return f"Error: Tweet {i+1} exceeds 280 characters. Thread partially posted up to tweet ID {last_tweet_id}."
            if not tweet_text:
                 return f"Error: Tweet {i+1} cannot be empty. Thread partially posted up to tweet ID {last_tweet_id}."

            # Add a small delay to avoid rate limiting issues (optional, adjust as needed)
            await asyncio.sleep(1)

            response = client.create_tweet(
                text=tweet_text,
                in_reply_to_tweet_id=last_tweet_id
            )
            last_tweet_id = response.data.get('id')
            posted_ids.append(last_tweet_id)
            print(f"Posted reply tweet {i+1}: {last_tweet_id}") # Log progress

        return f"Thread posted successfully! Tweet IDs: {', '.join(posted_ids)}"

    except tweepy.errors.TweepyException as e:
        return f"Error posting thread (partially posted: {', '.join(posted_ids)}): {e}"
    except Exception as e:
        return f"An unexpected error occurred (partially posted: {', '.join(posted_ids)}): {e}"


# --- Main Entry Point ---

def main():
    """Runs the MCP server."""
    # Check credentials on startup (optional but good practice)
    if not get_twitter_client():
         print("Server startup failed: Could not initialize Twitter client. Check credentials.")
         # Depending on requirements, you might exit here or let it run without functionality
         # exit(1) # Uncomment to exit if credentials fail
    else:
        print("Twitter client initialized successfully.")

    print("Starting x-twitter-posting-mcp server...")
    mcp.run(transport='stdio') # Default transport

if __name__ == "__main__":
    main()