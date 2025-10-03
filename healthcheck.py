import logging
import threading
from datetime import datetime
from flask import Flask, jsonify

logger = logging.getLogger(__name__)

class HealthCheckServer:
    """Health check server that provides web endpoints for monitoring system health."""
    
    def __init__(self, healthcheck_status, port=8000):
        """
        Initialize the health check server.
        
        Args:
            healthcheck_status (dict): Dictionary containing health status of various components
            port (int): Port number to run the server on (default: 8000)
        """
        self.healthcheck_status = healthcheck_status
        self.port = port
        self.app = Flask(__name__)
        self._setup_routes()
    
    def _setup_routes(self):
        """Set up Flask routes for health check endpoints."""
        
        @self.app.route('/')
        def healthcheck():
            """Health check endpoint that returns status based on healthcheck_status."""
            # Check if all items in healthcheck_status are True
            all_healthy = all(self.healthcheck_status.values())
            
            # Prepare response data with all healthcheck_status items and timestamp
            response_data = self.healthcheck_status.copy()
            response_data['timestamp'] = datetime.now().isoformat()
            
            # Return appropriate HTTP status code
            # 200 if all items are True, 500 if any item is False
            status_code = 200 if all_healthy else 500
            
            return jsonify(response_data), status_code

    def start_server(self):
        """Start the health check server in a separate thread."""
        try:
            logger.info(f"Starting healthcheck server on port {self.port}")
            self.app.run(host='127.0.0.1', port=self.port, debug=False, use_reloader=False, threaded=True)
        except Exception as e:
            logger.error(f"Failed to start healthcheck server: {str(e)}")

    def start_in_thread(self):
        """Start the health check server in a daemon thread."""
        healthcheck_thread = threading.Thread(target=self.start_server, daemon=True)
        healthcheck_thread.start()
        logger.info(f"Healthcheck server started on port {self.port}")
        return healthcheck_thread

    def update_health_status(self, new_status):
        """Update the health status dictionary."""
        self.healthcheck_status.update(new_status)

    def get_health_summary(self):
        """Get a summary of the current health status."""
        all_healthy = all(self.healthcheck_status.values())
        return {
            "overall_status": "healthy" if all_healthy else "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "checks": self.healthcheck_status,
            "healthy_count": sum(1 for status in self.healthcheck_status.values() if status),
            "total_count": len(self.healthcheck_status)
        }
