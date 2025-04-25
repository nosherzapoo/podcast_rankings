import os
import csv
import requests
import json
import pandas as pd
from datetime import datetime

def scrape_spotify_podcast_rankings():
    """
    Scrape top podcast rankings from Spotify Podcast Charts and display as DataFrame.
    Uses the API endpoint that the website calls rather than Selenium.
    
    Returns:
        str: Path to the saved CSV file and displays DataFrame
    """
    # The website uses this API endpoint to fetch the data
    api_url = "https://podcastcharts.byspotify.com/api/charts/top?country=us&date=latest&limit=100"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/json",
        "Referer": "https://podcastcharts.byspotify.com/"
    }
    
    print(f"Fetching data from API: {api_url}")
    
    try:
        # Make the API request
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        # Parse the JSON response
        data = response.json()
        
        # Debug the response
        print(f"API Response: {json.dumps(data, indent=2)[:500]}...")  # Print first 500 chars of response
        
        # Check if data is a list (API structure has changed)
        if isinstance(data, list):
            podcasts = data  # The data itself is a list of podcasts
        else:
            # Original expected structure - dictionary with 'podcasts' key
            podcasts = data.get('podcasts', [])
        
        if not podcasts:
            print("Error: No podcast data found in the API response.")
            return None
        
        # Debug the podcasts data
        print(f"First podcast entry: {json.dumps(podcasts[0], indent=2) if podcasts else 'None'}")
        
        # Prepare data for DataFrame
        podcast_data = []
        
        for i, podcast in enumerate(podcasts, 1):
            # Safely extract data using get() only for dictionaries
            if isinstance(podcast, dict):
                # Print the structure of the first few podcasts to debug
                if i <= 3:
                    print(f"Podcast {i} structure: {json.dumps(podcast, indent=2)}")
                
                # Extract data based on the actual API structure
                podcast_data.append({
                    'Rank': str(i),
                    'Podcast Title': podcast.get('showName', podcast.get('name', 'Unknown')),
                    'Publisher': podcast.get('showPublisher', podcast.get('publisher', 'Unknown')),
                    'Spotify ID': podcast.get('showUri', podcast.get('id', 'N/A')).replace('spotify:show:', '') if podcast.get('showUri') else podcast.get('id', 'N/A'),
                    'Image URL': podcast.get('showImageUrl', podcast.get('imageUrl', 'N/A')),
                    'Description': podcast.get('showDescription', podcast.get('description', 'N/A')),
                    'Rank Movement': podcast.get('chartRankMove', 'N/A')
                })
            else:
                # Handle unexpected podcast format
                print(f"Warning: Unexpected podcast data format at index {i}: {type(podcast)}")
                print(f"Content: {podcast}")
        
        # Create DataFrame
        df = pd.DataFrame(podcast_data)
        
        # Display the DataFrame
        print("\nSpotify Podcast Rankings:")
        print(df)
        
        # Generate filename with date
        today = datetime.now().strftime('%Y-%m-%d')
        output_file = f'spotify_podcast_rankings_{today}.csv'
        
        # Save to CSV
        df.to_csv(output_file, index=False)
        
        print(f"Successfully extracted {len(podcast_data)} podcasts to {output_file}")
        
        # Check if the API might have changed structure
        if all(p.get('Podcast Title') == 'Unknown' for p in podcast_data):
            print("WARNING: All podcast titles are 'Unknown'. The API structure may have changed.")
            print("Dumping raw data to 'api_response_debug.json' for inspection")
            with open('api_response_debug.json', 'w') as f:
                json.dump(data, f, indent=2)
        
        return output_file
        
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        
        # Fallback to alternative API endpoint if the first one fails
        try:
            fallback_url = "https://podcastcharts.byspotify.com/api/charts/trending?country=us&date=latest&limit=50"
            print(f"Trying fallback API: {fallback_url}")
            
            response = requests.get(fallback_url, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            print(f"Fallback API Response: {json.dumps(data, indent=2)[:500]}...")  # Debug output
            
            podcasts = data.get('podcasts', [])
            
            if not podcasts:
                print("Error: No podcast data found in the fallback API response.")
                return None
            
            # Process data as before
            podcast_data = []
            for i, podcast in enumerate(podcasts, 1):
                if i <= 3:  # Debug first few entries
                    print(f"Fallback podcast {i} structure: {json.dumps(podcast, indent=2)}")
                
                podcast_data.append({
                    'Rank': str(i),
                    'Podcast Title': podcast.get('showName', podcast.get('name', 'Unknown')),
                    'Publisher': podcast.get('showPublisher', podcast.get('publisher', 'Unknown')),
                    'Spotify ID': podcast.get('showUri', podcast.get('id', 'N/A')).replace('spotify:show:', '') if podcast.get('showUri') else podcast.get('id', 'N/A'),
                    'Image URL': podcast.get('showImageUrl', podcast.get('imageUrl', 'N/A')),
                    'Description': podcast.get('showDescription', podcast.get('description', 'N/A')),
                    'Rank Movement': podcast.get('chartRankMove', 'N/A')
                })
            
            # Create DataFrame for fallback data
            df = pd.DataFrame(podcast_data)
            
            # Display the DataFrame
            print("\nSpotify Trending Podcast Rankings:")
            print(df)
            
            today = datetime.now().strftime('%Y-%m-%d')
            output_file = f'spotify_podcast_rankings_trending_{today}.csv'
            
            # Save to CSV
            df.to_csv(output_file, index=False)
            
            print(f"Successfully extracted {len(podcast_data)} trending podcasts to {output_file}")
            return output_file
            
        except Exception as e2:
            print(f"Error with fallback API: {e2}")
            return None
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

if __name__ == "__main__":
    scrape_spotify_podcast_rankings()
