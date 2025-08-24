"""
Database connection and query helper functions.
Handles both MySQL and PostgreSQL connections via SQLAlchemy.
"""
import logging
from typing import Optional, Dict, List, Any
from sqlalchemy import create_engine, text, MetaData, Table, Column, String, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import pandas as pd

from config import DatabaseConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()

class DatabaseManager:
    """Manages database connections and provides query functionality."""
    
    def __init__(self):
        self.engine = None
        self.Session = None
        self.is_connected = False
        self._initialize_connection()
    
    def _initialize_connection(self):
        """Initialize database connection based on configuration."""
        connection_string = DatabaseConfig.get_connection_string()
        
        if not connection_string:
            logger.info("No database configured. Running in general chat mode only.")
            return
        
        try:
            self.engine = create_engine(connection_string, echo=False)
            self.Session = sessionmaker(bind=self.engine)
            
            # Test connection
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            self.is_connected = True
            logger.info(f"Successfully connected to {DatabaseConfig.DB_TYPE} database")
            
            # Create tables if they don't exist
            self._create_tables()
            
        except SQLAlchemyError as e:
            logger.error(f"Failed to connect to database: {e}")
            self.is_connected = False
    
    def _create_tables(self):
        """Create necessary tables if they don't exist."""
        try:
            Base.metadata.create_all(self.engine)
            logger.info("Database tables created/verified successfully")
        except SQLAlchemyError as e:
            logger.error(f"Failed to create tables: {e}")
    
    def execute_query(self, query: str, params: Optional[Dict] = None) -> Optional[List[Dict]]:
        """
        Execute a SQL query and return results.
        
        Args:
            query: SQL query string
            params: Optional parameters for the query
            
        Returns:
            List of dictionaries containing query results, or None if failed
        """
        if not self.is_connected:
            logger.warning("Database not connected. Cannot execute query.")
            return None
        
        try:
            with self.Session() as session:
                result = session.execute(text(query), params or {})
                
                if result.returns_rows:
                    # Convert to list of dictionaries
                    columns = result.keys()
                    rows = [dict(zip(columns, row)) for row in result.fetchall()]
                    return rows
                else:
                    session.commit()
                    return []
                    
        except SQLAlchemyError as e:
            logger.error(f"Query execution failed: {e}")
            return None
    
    def get_revenue_data(self, period: str = "last_quarter") -> Optional[Dict]:
        """
        Get revenue data for the specified period.
        
        Args:
            period: Time period ('last_quarter', 'last_year', 'current_month')
            
        Returns:
            Dictionary containing revenue data
        """
        if not self.is_connected:
            return None
        
        # Example revenue query - customize based on your database schema
        if period == "last_quarter":
            query = """
                SELECT 
                    SUM(amount) as total_revenue,
                    COUNT(*) as transaction_count,
                    AVG(amount) as average_transaction
                FROM transactions 
                WHERE created_at >= DATE_SUB(NOW(), INTERVAL 3 MONTH)
                AND created_at < NOW()
            """
        elif period == "last_year":
            query = """
                SELECT 
                    SUM(amount) as total_revenue,
                    COUNT(*) as transaction_count,
                    AVG(amount) as average_transaction
                FROM transactions 
                WHERE YEAR(created_at) = YEAR(NOW()) - 1
            """
        elif period == "current_month":
            query = """
                SELECT 
                    SUM(amount) as total_revenue,
                    COUNT(*) as transaction_count,
                    AVG(amount) as average_transaction
                FROM transactions 
                WHERE MONTH(created_at) = MONTH(NOW())
                AND YEAR(created_at) = YEAR(NOW())
            """
        else:
            return None
        
        try:
            results = self.execute_query(query)
            if results and len(results) > 0:
                return results[0]
        except Exception as e:
            logger.error(f"Failed to get revenue data: {e}")
        
        return None
    
    def get_customer_data(self, customer_id: Optional[str] = None) -> Optional[List[Dict]]:
        """
        Get customer data from the database.
        
        Args:
            customer_id: Optional customer ID to filter results
            
        Returns:
            List of customer dictionaries
        """
        if not self.is_connected:
            return None
        
        if customer_id:
            query = "SELECT * FROM customers WHERE customer_id = :customer_id"
            params = {"customer_id": customer_id}
        else:
            query = "SELECT * FROM customers LIMIT 100"
            params = {}
        
        return self.execute_query(query, params)
    
    def get_product_data(self, product_id: Optional[str] = None) -> Optional[List[Dict]]:
        """
        Get product data from the database.
        
        Args:
            product_id: Optional product ID to filter results
            
        Returns:
            List of product dictionaries
        """
        if not self.is_connected:
            return None
        
        if product_id:
            query = "SELECT * FROM products WHERE product_id = :product_id"
            params = {"product_id": product_id}
        else:
            query = "SELECT * FROM products LIMIT 100"
            params = {}
        
        return self.execute_query(query, params)
    
    def close_connection(self):
        """Close database connection."""
        if self.engine:
            self.engine.dispose()
            self.is_connected = False
            logger.info("Database connection closed")

# Example table definitions - customize based on your needs
class Transaction(Base):
    """Example transaction table."""
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True)
    customer_id = Column(String(50))
    product_id = Column(String(50))
    amount = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class Customer(Base):
    """Example customer table."""
    __tablename__ = 'customers'
    
    customer_id = Column(String(50), primary_key=True)
    name = Column(String(100))
    email = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

class Product(Base):
    """Example product table."""
    __tablename__ = 'products'
    
    product_id = Column(String(50), primary_key=True)
    name = Column(String(100))
    price = Column(Float)
    category = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

# Global database manager instance
db_manager = DatabaseManager()
