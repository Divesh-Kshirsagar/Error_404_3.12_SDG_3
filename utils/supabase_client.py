"""
Supabase Database Client

Handles all database operations:
- Patient records
- Visit records
- Queue state management
- Real-time sync between kiosk and dashboard
"""

import os
from supabase import create_client, Client


_supabase_client = None


def get_supabase() -> Client:
    """
    Get or create Supabase client instance (singleton pattern)
    
    Returns:
        Client: Supabase client instance
        
    Raises:
        ValueError: If SUPABASE_URL or SUPABASE_KEY not set in environment
    """
    global _supabase_client
    
    if _supabase_client is None:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        
        if not url or not key:
            raise ValueError(
                "Missing Supabase credentials. "
                "Set SUPABASE_URL and SUPABASE_KEY environment variables."
            )
        
        _supabase_client = create_client(url, key)
    
    return _supabase_client

