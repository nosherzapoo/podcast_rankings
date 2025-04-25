import os
import requests
import json
import pandas as pd
from datetime import datetime

def scrape_apple_podcast_rankings():
    """
    Scrape top podcast rankings from Apple Podcasts using their API and save as CSV.
    
    Returns:
        str: Path to the saved CSV file and displays DataFrame
    """
    # Apple Podcasts API endpoint for top podcasts
    api_url = "https://itunes.apple.com/us/rss/toppodcasts/limit=100/json"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/json",
    }
    
    print(f"Fetching data from Apple Podcasts API: {api_url}")
    
    try:
        # Make the API request
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        # Parse the JSON response
        data = response.json()
        
        # Debug the response structure
        print(f"API Response structure: {list(data.keys())}")
        
        # Extract the podcast entries from the feed
        entries = data.get('feed', {}).get('entry', [])
        
        if not entries:
            print("Error: No podcast data found in the API response.")
            return None
        
        # Debug the first entry
        print(f"First podcast entry structure: {json.dumps(entries[0], indent=2)[:500]}..." if entries else "None")
        
        # Prepare data for DataFrame
        podcast_data = []
        
        for i, entry in enumerate(entries, 1):
            try:
                # Extract data from the entry
                title = entry.get('title', {}).get('label', 'Unknown')
                artist = entry.get('im:artist', {}).get('label', 'Unknown')
                
                # Extract image URL (get the highest resolution available)
                images = entry.get('im:image', [])
                image_url = images[-1].get('label', 'N/A') if images else 'N/A'
                
                # Extract podcast URL
                podcast_url = entry.get('id', {}).get('label', 'N/A')
                
                # Extract category
                category = 'N/A'
                category_data = entry.get('category', {}).get('attributes', {})
                if category_data:
                    category = category_data.get('label', 'N/A')
                
                # Extract release date
                release_date = entry.get('im:releaseDate', {}).get('label', 'N/A')
                
                # Extract summary
                summary = entry.get('summary', {}).get('label', 'N/A')
                
                # Add to dataset
                podcast_data.append({
                    'Rank': str(i),
                    'Podcast Title': title,
                    'Publisher': artist,
                    'Category': category,
                    'Image URL': image_url,
                    'Apple URL': podcast_url,
                    'Release Date': release_date,
                    'Summary': summary
                })
                
                # Debug first few entries
                if i <= 3:
                    print(f"Podcast {i}: {title} by {artist}")
                
            except Exception as e:
                print(f"Error extracting podcast at index {i}: {e}")
        
        if not podcast_data:
            print("Error: No podcast data could be extracted.")
            return None
        
        # Create DataFrame
        df = pd.DataFrame(podcast_data)
        
        # Display the DataFrame
        print("\nApple Podcasts Rankings:")
        print(df[['Rank', 'Podcast Title', 'Publisher', 'Category']])  # Show limited columns for display
        
        # Generate filename with date
        today = datetime.now().strftime('%Y-%m-%d')
        output_file = f'apple_podcast_rankings_{today}.csv'
        
        # Save to CSV
        df.to_csv(output_file, index=False)
        
        print(f"Successfully extracted {len(podcast_data)} podcasts to {output_file}")
        return output_file
        
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        
        # Try alternative API endpoint if the first one fails
        try:
            fallback_url = "https://itunes.apple.com/us/rss/toppodcasts/genre=1310/limit=100/json"
            print(f"Trying fallback API: {fallback_url}")
            
            response = requests.get(fallback_url, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract the podcast entries from the feed
            entries = data.get('feed', {}).get('entry', [])
            
            if not entries:
                print("Error: No podcast data found in the fallback API response.")
                return None
            
            # Process data as before
            podcast_data = []
            for i, entry in enumerate(entries, 1):
                try:
                    title = entry.get('title', {}).get('label', 'Unknown')
                    artist = entry.get('im:artist', {}).get('label', 'Unknown')
                    
                    images = entry.get('im:image', [])
                    image_url = images[-1].get('label', 'N/A') if images else 'N/A'
                    
                    podcast_url = entry.get('id', {}).get('label', 'N/A')
                    
                    category = 'N/A'
                    category_data = entry.get('category', {}).get('attributes', {})
                    if category_data:
                        category = category_data.get('label', 'N/A')
                    
                    podcast_data.append({
                        'Rank': str(i),
                        'Podcast Title': title,
                        'Publisher': artist,
                        'Category': category,
                        'Image URL': image_url,
                        'Apple URL': podcast_url
                    })
                    
                except Exception as e:
                    print(f"Error extracting podcast at index {i}: {e}")
            
            if not podcast_data:
                print("Error: No podcast data could be extracted from fallback API.")
                return None
            
            # Create DataFrame for fallback data
            df = pd.DataFrame(podcast_data)
            
            # Display the DataFrame
            print("\nApple Podcasts Rankings (from genre API):")
            print(df[['Rank', 'Podcast Title', 'Publisher', 'Category']])
            
            today = datetime.now().strftime('%Y-%m-%d')
            output_file = f'apple_podcast_rankings_genre_{today}.csv'
            
            # Save to CSV
            df.to_csv(output_file, index=False)
            
            print(f"Successfully extracted {len(podcast_data)} podcasts to {output_file}")
            return output_file
            
        except Exception as e2:
            print(f"Error with fallback API: {e2}")
            return None
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

if __name__ == "__main__":
    scrape_apple_podcast_rankings()

