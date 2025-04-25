import os
import csv
import re
from bs4 import BeautifulSoup

def extract_top_podcasts(html_file_path):
    """
    Extract top podcast data from Podscribe HTML file and save as CSV.
    
    Args:
        html_file_path (str): Path to the Podscribe HTML file
    """
    # Check if file exists
    if not os.path.exists(html_file_path):
        print(f"Error: File {html_file_path} not found.")
        return
    
    # Read the HTML file
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Based on the HTML structure, podcasts are likely in rows with class jss589
    # Each row contains podcast information in a structured format
    podcast_rows = soup.select('.jss589')
    
    # Prepare data for CSV
    podcast_data = []
    
    if not podcast_rows:
        print("No podcast data found with expected class. The HTML structure might have changed.")
        return
    
    rank = 1  # Initialize rank counter
    
    for row in podcast_rows:
        try:
            # The podcast title is likely in a heading element or div with specific classes
            title_element = row.select_one('h3, .jss590, .MuiTypography-root')
            
            # The listeners count might be in a specific element or format
            # Look for elements that contain numeric data with K or M suffix
            text_elements = row.find_all(text=True)
            listeners_text = "N/A"
            
            for text in text_elements:
                # Look for text that matches pattern of numbers possibly followed by K or M
                if re.search(r'\d+(\.\d+)?[KMkm]?', text.strip()):
                    # Exclude short numbers that might be ranks
                    if len(text.strip()) > 1 and 'K' in text or 'M' in text or '.' in text:
                        listeners_text = text.strip()
                        break
            
            # Clean up the text
            title_text = title_element.get_text().strip() if title_element else "Unknown"
            
            # Add to dataset
            podcast_data.append({
                'Rank': str(rank),
                'Podcast Title': title_text,
                'Monthly Listeners': listeners_text
            })
            
            rank += 1
            
        except Exception as e:
            print(f"Error extracting podcast data: {e}")
    
    if not podcast_data:
        print("Could not extract structured podcast data.")
        return
    
    # Save to CSV
    output_file = 'top_podcasts.csv'
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Rank', 'Podcast Title', 'Monthly Listeners']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for podcast in podcast_data:
            writer.writerow(podcast)
    
    print(f"Successfully extracted {len(podcast_data)} podcasts to {output_file}")

if __name__ == "__main__":
    # Adjust the path to your HTML file
    html_file = "Podcast transcripts, sponsors, and audience data - Podscribe.html"
    extract_top_podcasts(html_file)
