from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models import Page, Post, Follower
from scraper import scrape_facebook_page
from typing import List, Optional

app = FastAPI()

# Home endpoint
@app.get("/")
def home():
    return {"message": "Facebook Insights API"}

# Get page details by username
@app.get("/page/{username}")
def get_page(username: str, db: Session = Depends(get_db)):
    # Check if the page already exists in the database
    page = db.query(Page).filter(Page.username == username).first()
    
    if not page:
        # If not, scrape the page data
        scraped_data = scrape_facebook_page(username)
        print("Scraped Data:", scraped_data)  # Debugging line
        if not scraped_data["page_name"]:
            raise HTTPException(status_code=404, detail="Page not found")

        # Filter out invalid keys
        valid_keys = {"username", "page_name", "followers_count", "category", "url"}  # Add valid keys here
        filtered_data = {k: v for k, v in scraped_data.items() if k in valid_keys}

        # Save the filtered data to the database
        new_page = Page(**filtered_data)
        db.add(new_page)
        db.commit()
        db.refresh(new_page)
        return new_page

    return page

# Filter pages by follower count and category
@app.get("/pages/")
def filter_pages(
    min_followers: Optional[int] = Query(0, description="Minimum number of followers"),
    max_followers: Optional[int] = Query(10000000, description="Maximum number of followers"),
    category: Optional[str] = Query(None, description="Page category"),
    db: Session = Depends(get_db)
):
    query = db.query(Page)
    
    # Apply follower count filter
    if min_followers is not None and max_followers is not None:
        query = query.filter(Page.followers.between(min_followers, max_followers))
    
    # Apply category filter
    if category:
        query = query.filter(Page.category == category)
    
    return query.all()

# Get followers of a page
@app.get("/page/{username}/followers")
def get_followers(username: str, db: Session = Depends(get_db)):
    # Find the page
    page = db.query(Page).filter(Page.username == username).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    
    # Fetch followers
    followers = db.query(Follower).filter(Follower.page_id == page.id).all()
    return followers

# Get recent posts of a page (with pagination)
@app.get("/page/{username}/posts")
def get_posts(
    username: str,
    limit: int = Query(10, description="Number of posts to return"),
    skip: int = Query(0, description="Number of posts to skip"),
    db: Session = Depends(get_db)
):
    # Find the page
    page = db.query(Page).filter(Page.username == username).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    
    # Fetch posts with pagination
    posts = db.query(Post).filter(Post.page_id == page.id).offset(skip).limit(limit).all()
    return posts