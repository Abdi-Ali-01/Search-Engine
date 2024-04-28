import requests
from bs4 import BeautifulSoup
import sqlite3
from time import sleep
from urllib.parse import urlparse

# Absolute path for the database
db_path = 'C:/Users/mrabd/OneDrive/Documents/Search engine/2.web spidering/job_listings.db'

def is_allowed_by_robots(url):
    parsed_url = urlparse(url)
    robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
    try:
        robots_response = requests.get(robots_url, timeout=10)
        if robots_response.status_code == 200:
            return not any(agent == '*' or agent == 'job_crawler' for agent, _ in parse_robots(robots_response.text))
        else:
            return True
    except requests.RequestException as e:
        print(f"Error fetching robots.txt for {url}: {e}")
        return True

def parse_robots(robots_content):
    lines = robots_content.splitlines()
    agent = None
    rules = []
    for line in lines:
        if line.startswith('User-agent:'):
            if agent is not None:
                yield (agent, rules)
            agent = line.split(':')[1].strip()
            rules = []
        elif line.startswith('Disallow:') and agent is not None:
            path = line.split(':')[1].strip()
            rules.append(path)
    if agent is not None:
        yield (agent, rules)

def job_crawler(start_urls, max_pages=50):
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE,
                title TEXT,
                description TEXT,
                location TEXT
            )
        ''')

        url_frontier = list(start_urls)
        visited_pages = set()

        while url_frontier and len(visited_pages) < max_pages:
            url = url_frontier.pop(0)
            if url not in visited_pages and is_allowed_by_robots(url):
                visited_pages.add(url)
                try:
                    response = requests.get(url, timeout=10)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    job_articles = soup.find_all('article', class_='job_listing')
                    for job in job_articles:
                        job_title = job.find('h2').text.strip()
                        job_description = job.find('p', class_='description').text.strip()
                        job_location = job.find('span', class_='location').text.strip()
                        job_url = job.find('a', href=True)['href']
                        
                        c.execute('''
                            INSERT OR IGNORE INTO jobs (url, title, description, location)
                            VALUES (?, ?, ?, ?)
                        ''', (job_url, job_title, job_description, job_location))

                    links = soup.find_all('a', href=True)
                    for link in links:
                        href = link.get("href")
                        if href.startswith('http') and href not in visited_pages:
                            url_frontier.append(href)
                    
                    print(f"Processed {url}")
                    sleep(1)  # Respectful crawling by waiting between requests
                except requests.RequestException as e:
                    print(f"Error fetching {url}: {e}")
            else:
                print(f"Skipping {url} due to robots.txt restriction")

    print('Crawling complete.')

# Example usage with multiple start URLs
start_urls = [
    'https://www.it-jobs.co.uk/',
    'https://uk.indeed.com/?r=us',
    'https://www.glassdoor.co.uk',
    'https://www.fish4.co.uk',
    'https://www.linkedin.com',
    'https://www.cv-library.co.uk',
    'https://www.monster.co.uk',
    'https://www.reed.co.uk'
]
job_crawler(start_urls, 50)
