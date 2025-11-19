"""
Database Schemas for Favor International

Each Pydantic model maps to a MongoDB collection whose name is the lowercase of the class name.
Example: Story -> "story" collection

These schemas are used for validation before inserting into the database.
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date, datetime

# Content & Impact
class Story(BaseModel):
    id: Optional[str] = Field(None, description="Document ID")
    title: str = Field(..., description="Story title")
    content: str = Field(..., description="Full story text")
    image_url: Optional[str] = Field(None, description="Primary image URL")
    author_name: Optional[str] = Field(None, description="Author name")
    published_date: Optional[date] = Field(None, description="Publish date")

class Program(BaseModel):
    id: Optional[str] = Field(None, description="Document ID")
    name: str = Field(..., description="Program name")
    description: str = Field(..., description="Program description")
    region: Optional[str] = Field(None, description="Geographic region")
    image_url: Optional[str] = Field(None, description="Representative image URL")

# Engagement
class Volunteer(BaseModel):
    id: Optional[str] = Field(None, description="Document ID")
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    message: Optional[str] = Field(None, description="Message or motivation")
    signup_date: Optional[date] = Field(None, description="Signup date")

class Donation(BaseModel):
    id: Optional[str] = Field(None, description="Document ID")
    full_name: str = Field(..., description="Donor full name")
    email: EmailStr = Field(..., description="Donor email")
    amount: float = Field(..., gt=0, description="Donation amount in USD")
    donation_date: Optional[datetime] = Field(None, description="Donation timestamp")

class NewsletterSubscriber(BaseModel):
    id: Optional[str] = Field(None, description="Document ID")
    email: EmailStr = Field(..., description="Subscriber email")
    subscribed_date: Optional[datetime] = Field(None, description="Subscription timestamp")
