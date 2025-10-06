# Prometheus Metrics Documentation

This document describes the Prometheus metrics available in the ETH Balance Checker application.

## Overview

The application exposes comprehensive metrics for monitoring balance changes, health status, performance, errors, and resource usage. All metrics are available at the `/metrics` endpoint on port 8000.

## Available Metrics

### 1. Balance Tracking Metrics

#### `eth_balance_current{address, coin}`
- **Type**: Gauge
- **Description**: Current balance for each address/coin combination
- **Labels**: 
  - `address`: Ethereum address being monitored
  - `coin`: Token symbol (e.g., usdt, usdc, dai)

#### `eth_balance_change_detected_total{address, coin}`
- **Type**: Counter
- **Description**: Total number of balance changes detected
- **Labels**: 
  - `address`: Ethereum address
  - `coin`: Token symbol

#### `eth_balance_check_duration_seconds{address, coin}`
- **Type**: Histogram
- **Description**: Duration of balance check operations
- **Labels**: 
  - `address`: Ethereum address
  - `coin`: Token symbol
- **Buckets**: 0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0, +Inf

#### `eth_balance_check_total{address, coin, status}`
- **Type**: Counter
- **Description**: Total number of balance checks performed
- **Labels**: 
  - `address`: Ethereum address
  - `coin`: Token symbol
  - `status`: success or error

### 2. Health Status Metrics

#### `eth_rpc_health_status`
- **Type**: Gauge
- **Description**: Ethereum RPC connection health (1=healthy, 0=unhealthy)

#### `telegram_bot_health_status`
- **Type**: Gauge
- **Description**: Telegram bot health (1=healthy, 0=unhealthy)

#### `application_health_status`
- **Type**: Gauge
- **Description**: Overall application health (1=healthy, 0=unhealthy)

#### `application_info`
- **Type**: Info
- **Description**: Application information
- **Labels**: name, version, description

### 3. Performance Metrics

#### `eth_rpc_request_duration_seconds{method}`
- **Type**: Histogram
- **Description**: Duration of Ethereum RPC requests
- **Labels**: 
  - `method`: RPC method name (e.g., get_token_balance)
- **Buckets**: 0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0, +Inf

#### `eth_rpc_request_total{method, status}`
- **Type**: Counter
- **Description**: Total number of Ethereum RPC requests
- **Labels**: 
  - `method`: RPC method name
  - `status`: success or error

#### `telegram_notification_duration_seconds`
- **Type**: Histogram
- **Description**: Duration of Telegram notification sending
- **Buckets**: 0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0, +Inf

#### `telegram_notification_total{status}`
- **Type**: Counter
- **Description**: Total number of Telegram notifications sent
- **Labels**: 
  - `status`: success or error

### 4. Error Tracking Metrics

#### `eth_rpc_errors_total{error_type}`
- **Type**: Counter
- **Description**: Total number of Ethereum RPC errors
- **Labels**: 
  - `error_type`: Type of error (e.g., rpc_error, rpc_exception)

#### `telegram_errors_total{error_type}`
- **Type**: Counter
- **Description**: Total number of Telegram API errors
- **Labels**: 
  - `error_type`: Type of error (e.g., telegram_api_error, telegram_exception)

#### `balance_check_errors_total{address, coin, error_type}`
- **Type**: Counter
- **Description**: Total number of balance check errors
- **Labels**: 
  - `address`: Ethereum address
  - `coin`: Token symbol
  - `error_type`: Type of error

#### `application_errors_total{error_type, component}`
- **Type**: Counter
- **Description**: Total number of application errors
- **Labels**: 
  - `error_type`: Type of error
  - `component`: Component where error occurred

### 5. Resource Usage Metrics

#### `memory_usage_bytes`
- **Type**: Gauge
- **Description**: Memory usage in bytes

#### `cpu_usage_percent`
- **Type**: Gauge
- **Description**: CPU usage percentage

#### `process_uptime_seconds`
- **Type**: Gauge
- **Description**: Process uptime in seconds

### 6. Scheduling Metrics

#### `balance_check_cycle_total`
- **Type**: Counter
- **Description**: Total number of balance check cycles completed

#### `balance_check_cycle_duration_seconds`
- **Type**: Histogram
- **Description**: Duration of balance check cycles
- **Buckets**: 1.0, 5.0, 10.0, 30.0, 60.0, 120.0, 300.0, 600.0, +Inf

#### `scheduler_uptime_seconds`
- **Type**: Gauge
- **Description**: Scheduler uptime in seconds

## Usage

### Accessing Metrics

Metrics are available at: `http://localhost:8000/metrics`

### Health Check

Health status is available at: `http://localhost:8000/`

### Sample Prometheus Queries

```promql
# Alert when RPC is down
eth_rpc_health_status == 0

# Track balance change frequency
rate(eth_balance_change_detected_total[5m])

# Monitor check cycle performance
histogram_quantile(0.95, rate(balance_check_cycle_duration_seconds_bucket[5m]))

# Track error rates
rate(eth_rpc_errors_total[5m])

# Monitor memory usage
memory_usage_bytes

# Track notification success rate
rate(telegram_notification_total{status="success"}[5m]) / rate(telegram_notification_total[5m])

# Monitor balance check duration
histogram_quantile(0.95, rate(eth_balance_check_duration_seconds_bucket[5m]))
```

### Alerting Rules

Example Prometheus alerting rules:

```yaml
groups:
  - name: eth-balance-checker
    rules:
      - alert: RPCDown
        expr: eth_rpc_health_status == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Ethereum RPC is down"
          
      - alert: TelegramDown
        expr: telegram_bot_health_status == 0
        for: 1m
        labels:
          severity: warning
        annotations:
          summary: "Telegram bot is down"
          
      - alert: HighErrorRate
        expr: rate(eth_rpc_errors_total[5m]) > 0.1
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "High RPC error rate"
          
      - alert: BalanceCheckSlow
        expr: histogram_quantile(0.95, rate(eth_balance_check_duration_seconds_bucket[5m])) > 10
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Balance checks are slow"
```

## Testing

Run the test script to verify metrics are working:

```bash
python test_metrics.py
```

This will test all metric types and generate sample output.

## Dependencies

The metrics implementation requires:
- `prometheus_client==0.20.0`
- `psutil==5.9.8`

These are automatically included in the updated `requirements.txt`.
