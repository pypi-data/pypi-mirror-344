"""
Mock implementation of EventBus for testing.
"""

import logging
from typing import Dict, Any, List, Callable, Optional, Awaitable
from datetime import datetime, UTC

from events.event_bus import EventBus

logger = logging.getLogger(__name__)

class MockEventBus(EventBus):
    """
    Mock implementation of EventBus for testing.
    
    This class simulates the behavior of the EventBus without using Kafka.
    It stores events and handlers in memory for testing purposes.
    """
    
    def __init__(self):
        """Initialize the mock event bus."""
        self.handlers: Dict[str, List[Callable[[Dict[str, Any]], Awaitable[None]]]] = {}
        self.events: List[Dict[str, Any]] = []
        self._is_running = False
        
    async def initialize(self) -> None:
        """Initialize the mock event bus."""
        try:
            self._is_running = True
            logger.info("Mock event bus initialized")
            
        except Exception as e:
            logger.error(f"Error initializing mock event bus: {e}")
            raise
            
    async def publish(self, topic: str, data: Dict[str, Any]) -> None:
        """
        Publish an event to a topic.
        
        Args:
            topic (str): Topic to publish to
            data (Dict[str, Any]): Event data
        """
        try:
            # Add timestamp
            event = {
                "topic": topic,
                "data": data,
                "timestamp": datetime.now(UTC).isoformat()
            }
            
            # Store event
            self.events.append(event)
            
            # Call handlers
            if topic in self.handlers:
                for handler in self.handlers[topic]:
                    await handler(data)
                    
            logger.info(f"Published event to topic {topic}")
            
        except Exception as e:
            logger.error(f"Error publishing event: {e}")
            raise
            
    async def consume(self, topic: str, callback: Callable) -> None:
        """
        Register a callback for a topic.
        
        Args:
            topic (str): Topic to consume from
            callback (Callable): Callback function
        """
        try:
            if topic not in self.handlers:
                self.handlers[topic] = []
                
            self.handlers[topic].append(callback)
            logger.info(f"Registered handler for topic {topic}")
            
        except Exception as e:
            logger.error(f"Error registering handler: {e}")
            raise
            
    def start(self) -> None:
        """Start the mock event bus."""
        self._is_running = True
        logger.info("Mock event bus started")
        
    def stop(self) -> None:
        """Stop the mock event bus."""
        self._is_running = False
        logger.info("Mock event bus stopped")
        
    def clear(self) -> None:
        """Clear all events and handlers."""
        self.handlers.clear()
        self.events.clear()
        logger.info("Mock event bus cleared")
        
    @property
    def is_running(self) -> bool:
        """Check if the event bus is running."""
        return self._is_running 

    async def register_handler(
        self,
        event_type: str,
        handler: Callable[[Dict[str, Any]], Awaitable[None]]
    ) -> None:
        """Register an event handler."""
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)
        logger.info(f"Registered handler for event type: {event_type}")
        
    async def emit(self, event_type: str, event_data: Dict[str, Any]) -> None:
        """Emit an event."""
        event = {
            "type": event_type,
            "data": event_data,
            "timestamp": datetime.now().isoformat()
        }
        self.events.append(event)
        
        if event_type in self.handlers:
            for handler in self.handlers[event_type]:
                try:
                    await handler(event_data)
                except Exception as e:
                    logger.error(f"Error in event handler: {str(e)}")
                    
        logger.info(f"Emitted event: {event_type}")
        
    def get_events(self) -> List[Dict[str, Any]]:
        """Get all emitted events."""
        return self.events
        
    def clear_events(self) -> None:
        """Clear all emitted events."""
        self.events = []
        logger.info("Cleared all events")
        
    async def __aenter__(self):
        """Async context manager entry."""
        await self.initialize()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        self._is_running = False 