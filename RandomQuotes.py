#Dataset link = https://www.kaggle.com/datasets/manann/quotes-500k?resource=download

import csv
import random
from BioUpdater import update_facebook_bio
import time

def get_quotes(csv_file_path, max_length=100, max_attempts=100):
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        if not rows:
            print("Error: CSV file is empty")
            return None
        
        for attempt in range(max_attempts):
            row = random.choice(rows)
            quote = row.get('quote', '').strip()
            author = row.get('author', '').strip()
            
            result = f"{quote} -{author}"
            
            if len(result) <= max_length:
                return result
        
        print(f"Error: Could not find quote under {max_length} characters after {max_attempts} attempts")
        return None
        
    except FileNotFoundError:
        print(f"Error: File not found at {csv_file_path}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    
if __name__ == "__main__":
    quote = get_quotes('quotes.csv')
    while True:
        if quote:
            print(quote)
            update_facebook_bio(quote, publish_story=False)
        
        time.sleep(120)