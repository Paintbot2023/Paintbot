import praw
import time
import logging

# Reddit API credentials (replace these with your actual credentials)
reddit_client_id = '6J1-Q5HSqsZVcU5qNuKjqA'
reddit_client_secret = 'GWol_AJN7x0XbPbKkHmH-66kF1VzEg'
reddit_username = 'This-Picture2293'
reddit_password = 'vladimer1917'
user_agent = '<console:paintbot:1.0>'

# Subreddit to monitor
target_subreddit = 'place'  # r/place subreddit

# Color code for the pixel (you can change this to your desired color)
color_green = 4  # Green color (https://redd.it/61tjlj)

# Create a Reddit instance
reddit = praw.Reddit(
    client_id=reddit_client_id,
    client_secret=reddit_client_secret,
    username=reddit_username,
    password=reddit_password,
    user_agent=user_agent
)

def process_pixel_event(pixel):
    # Custom logic to process the pixel placement event
    # For simplicity, we'll just print the information here
    print(f"New pixel placed at (x={pixel['x']}, y={pixel['y']}) with color {pixel['color']}")

def place_pixel(x, y, color, submission_url):
    try:
        # Compose the comment body with the pixel placement information
        comment_body = f"Placed tile at {x} {y} {color}"

        # Get the submission object for the r/place canvas
        submission = reddit.submission(url=submission_url)

        # Post the comment to the submission (r/place canvas)
        submission.reply(comment_body)

        print(f"Pixel placed at (x={x}, y={y}) with color {color}")
    except praw.exceptions.RedditAPIException as e:
        # Handle Reddit API exceptions
        logging.error(f"Failed to place the pixel at (x={x}, y={y}): {e}")
    except Exception as e:
        # Handle other exceptions
        logging.error(f"Unexpected error while placing the pixel at (x={x}, y={y}): {e}")

def draw_line(x1, y1, x2, y2, submission_url):
    # Bresenham's line algorithm to draw a straight green line
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = -1 if x1 > x2 else 1
    sy = -1 if y1 > y2 else 1
    err = dx - dy

    while True:
        place_pixel(x1, y1, color_green, submission_url)

        if x1 == x2 and y1 == y2:
            break

        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy

        # Wait for five minutes (300 seconds) before placing the next pixel
        time.sleep(300)

def get_latest_submission_url():
    subreddit = reddit.subreddit(target_subreddit)
    latest_submission = subreddit.new(limit=1).__next__()
    return latest_submission.url

def main():
    # Get the URL of the latest "r/place" submission
    submission_url = get_latest_submission_url()

    # Draw a line on the "r/place" canvas
    draw_line(300, -200, 499, -200, submission_url)

if __name__ == "__main__":
    main()
