import json
import csv
import pandas as pd
from sqlalchemy import create_engine, Column, String, Float, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from typing import List, Dict
import os
from config.settings import Config

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Float)
    url = Column(String)
    description = Column(String)
    availability = Column(String)
    rating = Column(Float)
    scraped_at = Column(DateTime, default=datetime.utcnow)

class DataStorage:
    def __init__(self):
        self.config = Config()
        self.engine = None
        self.session = None
        
        if self.config.OUTPUT_FORMAT == 'database':
            self._setup_database()
    
    def _setup_database(self):
        """Initialize database connection"""
        self.engine = create_engine(self.config.DATABASE_URL)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def save_to_csv(self, data: List[Dict], filename: str):
        """Save data to CSV file"""
        if not data:
            return
        
        filepath = os.path.join(self.config.OUTPUT_PATH, f"{filename}.csv")
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        df = pd.DataFrame(data)
        df.to_csv(filepath, index=False)
        print(f"Data saved to {filepath}")
    
    def save_to_json(self, data: List[Dict], filename: str):
        """Save data to JSON file"""
        filepath = os.path.join(self.config.OUTPUT_PATH, f"{filename}.json")
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Data saved to {filepath}")
    
    def save_to_database(self, data: List[Dict]):
        """Save data to database"""
        if not self.session:
            raise Exception("Database not initialized")
        
        for item in data:
            product = Product(**item)
            self.session.add(product)
        
        self.session.commit()
        print(f"Saved {len(data)} items to database")
    
    def save(self, data: List[Dict], filename: str = "products"):
        """Save data based on configured format"""
        if self.config.OUTPUT_FORMAT == 'csv':
            self.save_to_csv(data, filename)
        elif self.config.OUTPUT_FORMAT == 'json':
            self.save_to_json(data, filename)
        elif self.config.OUTPUT_FORMAT == 'database':
            self.save_to_database(data)