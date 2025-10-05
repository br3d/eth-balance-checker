"""
Prometheus metrics module for ETH balance checker application.
Provides comprehensive monitoring and observability metrics.
"""

import time
import psutil
import logging
from prometheus_client import Counter, Gauge, Histogram, Info, generate_latest, CONTENT_TYPE_LATEST
from flask import Response

logger = logging.getLogger(__name__)

class PrometheusMetrics:
    """Prometheus metrics collector for ETH balance checker application."""
    
    def __init__(self):
        """Initialize all Prometheus metrics."""
        self._init_balance_metrics()
        self._init_health_metrics()
        self._init_performance_metrics()
        self._init_error_metrics()
        self._init_resource_metrics()
        self._init_scheduling_metrics()
        
    def _init_balance_metrics(self):
        """Initialize balance tracking metrics."""
        # Current balance for each address/coin combination
        self.balance_current = Gauge(
            'eth_balance_current',
            'Current balance for each address/coin combination',
            ['address', 'coin']
        )
        
        # Balance change detection counter
        self.balance_change_detected_total = Counter(
            'eth_balance_change_detected_total',
            'Total number of balance changes detected',
            ['address', 'coin']
        )
        
        # Balance check duration histogram
        self.balance_check_duration_seconds = Histogram(
            'eth_balance_check_duration_seconds',
            'Duration of balance check operations',
            ['address', 'coin'],
            buckets=(0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0, float('inf'))
        )
        
        # Balance check total counter
        self.balance_check_total = Counter(
            'eth_balance_check_total',
            'Total number of balance checks performed',
            ['address', 'coin', 'status']
        )
    
    def _init_health_metrics(self):
        """Initialize health status metrics."""
        # RPC health status
        self.eth_rpc_health_status = Gauge(
            'eth_rpc_health_status',
            'Ethereum RPC connection health status (1=healthy, 0=unhealthy)'
        )
        
        # Telegram bot health status
        self.telegram_bot_health_status = Gauge(
            'telegram_bot_health_status',
            'Telegram bot health status (1=healthy, 0=unhealthy)'
        )
        
        # Overall application health
        self.application_health_status = Gauge(
            'application_health_status',
            'Overall application health status (1=healthy, 0=unhealthy)'
        )
        
        # Application info
        self.application_info = Info(
            'application_info',
            'Application information'
        )
        self.application_info.info({
            'name': 'eth-balance-checker',
            'version': '1.0.0',
            'description': 'Ethereum balance monitoring application'
        })
    
    def _init_performance_metrics(self):
        """Initialize performance monitoring metrics."""
        # RPC request duration
        self.eth_rpc_request_duration_seconds = Histogram(
            'eth_rpc_request_duration_seconds',
            'Duration of Ethereum RPC requests',
            ['method'],
            buckets=(0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0, float('inf'))
        )
        
        # RPC request total counter
        self.eth_rpc_request_total = Counter(
            'eth_rpc_request_total',
            'Total number of Ethereum RPC requests',
            ['method', 'status']
        )
        
        # Telegram notification duration
        self.telegram_notification_duration_seconds = Histogram(
            'telegram_notification_duration_seconds',
            'Duration of Telegram notification sending',
            buckets=(0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0, float('inf'))
        )
        
        # Telegram notification total counter
        self.telegram_notification_total = Counter(
            'telegram_notification_total',
            'Total number of Telegram notifications sent',
            ['status']
        )
    
    def _init_error_metrics(self):
        """Initialize error tracking metrics."""
        # RPC errors
        self.eth_rpc_errors_total = Counter(
            'eth_rpc_errors_total',
            'Total number of Ethereum RPC errors',
            ['error_type']
        )
        
        # Telegram errors
        self.telegram_errors_total = Counter(
            'telegram_errors_total',
            'Total number of Telegram API errors',
            ['error_type']
        )
        
        # Balance check errors
        self.balance_check_errors_total = Counter(
            'balance_check_errors_total',
            'Total number of balance check errors',
            ['address', 'coin', 'error_type']
        )
        
        # General application errors
        self.application_errors_total = Counter(
            'application_errors_total',
            'Total number of application errors',
            ['error_type', 'component']
        )
    
    def _init_resource_metrics(self):
        """Initialize resource usage metrics."""
        # Memory usage
        self.memory_usage_bytes = Gauge(
            'memory_usage_bytes',
            'Memory usage in bytes'
        )
        
        # CPU usage percentage
        self.cpu_usage_percent = Gauge(
            'cpu_usage_percent',
            'CPU usage percentage'
        )
        
        # Process uptime
        self.process_uptime_seconds = Gauge(
            'process_uptime_seconds',
            'Process uptime in seconds'
        )
    
    def _init_scheduling_metrics(self):
        """Initialize scheduling metrics."""
        # Balance check cycle counter
        self.balance_check_cycle_total = Counter(
            'balance_check_cycle_total',
            'Total number of balance check cycles completed'
        )
        
        # Balance check cycle duration
        self.balance_check_cycle_duration_seconds = Histogram(
            'balance_check_cycle_duration_seconds',
            'Duration of balance check cycles',
            buckets=(1.0, 5.0, 10.0, 30.0, 60.0, 120.0, 300.0, 600.0, float('inf'))
        )
        
        # Scheduler uptime
        self.scheduler_uptime_seconds = Gauge(
            'scheduler_uptime_seconds',
            'Scheduler uptime in seconds'
        )
    
    def update_balance_metrics(self, address, coin, current_balance, previous_balance=None, duration=None, status='success'):
        """Update balance-related metrics."""
        # Update current balance
        self.balance_current.labels(address=address, coin=coin).set(current_balance)
        
        # Update balance check counter
        self.balance_check_total.labels(address=address, coin=coin, status=status).inc()
        
        # Update duration if provided
        if duration is not None:
            self.balance_check_duration_seconds.labels(address=address, coin=coin).observe(duration)
        
        # Check for balance change
        if previous_balance is not None and current_balance != previous_balance:
            self.balance_change_detected_total.labels(address=address, coin=coin).inc()
            logger.info(f"Balance change detected for {address}/{coin}: {previous_balance} -> {current_balance}")
    
    def update_health_status(self, rpc_healthy, telegram_healthy, overall_healthy):
        """Update health status metrics."""
        self.eth_rpc_health_status.set(1 if rpc_healthy else 0)
        self.telegram_bot_health_status.set(1 if telegram_healthy else 0)
        self.application_health_status.set(1 if overall_healthy else 0)
    
    def record_rpc_request(self, method, duration, success=True):
        """Record RPC request metrics."""
        status = 'success' if success else 'error'
        self.eth_rpc_request_total.labels(method=method, status=status).inc()
        self.eth_rpc_request_duration_seconds.labels(method=method).observe(duration)
    
    def record_telegram_notification(self, duration, success=True):
        """Record Telegram notification metrics."""
        status = 'success' if success else 'error'
        self.telegram_notification_total.labels(status=status).inc()
        self.telegram_notification_duration_seconds.observe(duration)
    
    def record_error(self, error_type, component='general', address=None, coin=None):
        """Record error metrics."""
        if component == 'rpc':
            self.eth_rpc_errors_total.labels(error_type=error_type).inc()
        elif component == 'telegram':
            self.telegram_errors_total.labels(error_type=error_type).inc()
        elif component == 'balance_check' and address and coin:
            self.balance_check_errors_total.labels(address=address, coin=coin, error_type=error_type).inc()
        else:
            self.application_errors_total.labels(error_type=error_type, component=component).inc()
    
    def record_balance_check_cycle(self, duration):
        """Record balance check cycle metrics."""
        self.balance_check_cycle_total.inc()
        self.balance_check_cycle_duration_seconds.observe(duration)
    
    def update_resource_metrics(self):
        """Update resource usage metrics."""
        try:
            # Memory usage
            process = psutil.Process()
            memory_info = process.memory_info()
            self.memory_usage_bytes.set(memory_info.rss)
            
            # CPU usage
            cpu_percent = process.cpu_percent()
            self.cpu_usage_percent.set(cpu_percent)
            
            # Process uptime
            uptime = time.time() - process.create_time()
            self.process_uptime_seconds.set(uptime)
            
        except Exception as e:
            logger.error(f"Failed to update resource metrics: {e}")
    
    def update_scheduler_uptime(self, start_time):
        """Update scheduler uptime."""
        uptime = time.time() - start_time
        self.scheduler_uptime_seconds.set(uptime)
    
    def get_metrics_response(self):
        """Get Prometheus metrics response."""
        try:
            # Update resource metrics before generating response
            self.update_resource_metrics()
            
            # Generate metrics
            metrics_data = generate_latest()
            return Response(metrics_data, mimetype=CONTENT_TYPE_LATEST)
        except Exception as e:
            logger.error(f"Failed to generate metrics: {e}")
            return Response(f"Error generating metrics: {e}", status=500, mimetype='text/plain')

# Global metrics instance
metrics = PrometheusMetrics()
