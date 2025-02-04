# SDE Intern Assignment - Deepsolv

## Overview
This project is a **Facebook Insights Microservice** that allows users to fetch and store insights of a given Facebook Page username. The service scrapes Facebook data, stores it in a database, and provides RESTful APIs to retrieve the stored information.

## Tech Stack
- **Backend Framework:** FastAPI
- **Database:** MySQL
- **Scraping Library:** BeautifulSoup/Selenium/Scrapy
- **Deployment:** Docker 


## Features

### Mandatory Features
1. **Scraping Service**
   - Extracts the following details from a given Facebook Page username:
     - Page Name, URL, ID, Profile Picture, Email, Website, Category, Followers, Likes, Creation Date.
     - Stores 25-40 recent posts.
     - Fetches comments and followers/following details.
   - Saves all data into the database with appropriate relationships.

2. **API Endpoints**
   - `GET /page/{username}`: Fetches details of a page from the DB. If not found, scrapes it in real time.
   - `GET /pages?followers_min=20000&followers_max=40000` - Fetches pages by follower count range.
   - `GET /pages?name=xyz` - Fetches pages with a similar name.
   - `GET /pages?category=xyz` - Fetches pages by category.
   - `GET /page/{username}/followers` - Retrieves the followers of a page.
   - `GET /page/{username}/following` - Retrieves the following list of a page.
   - `GET /page/{username}/posts` - Fetches 10-15 recent posts.
   - **Pagination Support** for GET requests.


## Project Structure
```
facebook_insights/
├── src/
│   ├── models.py         # Database models (Page, Post, User, etc.)
│   ├── scraper.py        # Scraping logic
│   ├── api.py            # API endpoints
│   ├── database.py       # Database connection
│   ├── main.py           # Entry point
├── requirements.txt      # Dependencies
├── README.md             # Documentation
├── postman_collection.json # Postman API collection (optional)
├── Dockerfile            # Containerization (optional)
```

## Installation & Setup
```bash
# Clone the repository
git clone https://github.com/Aayushi1111/fb_insights.git
cd fb_insights

# Install dependencies
pip install -r requirements.txt

# Setup Database
python src/database.py --init

# Run the server
python src/main.py
```

## API Documentation
### Fetch Page Details
```http
GET /page/{username}
```
**Response:**
```json
{
  "page_name": "Boat Lifestyle",
  "followers": 500000,
  "likes": 450000,
  "posts": [
    {"id": 1, "content": "New Launch!", "likes": 5000}
  ]
}
```

## Deployment

```bash
docker build -t fb-insights .
docker run -p 8000:8000 fb-insights
```

