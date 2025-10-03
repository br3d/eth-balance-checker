# ETH Balance Checker

A Python-based monitoring bot that tracks Ethereum token balances and sends notifications via Telegram when balances change. Includes comprehensive health monitoring and Docker support.

## 🚀 Features

- **Real-time Balance Monitoring**: Track multiple Ethereum addresses and tokens
- **Telegram Notifications**: Get instant alerts when balances change
- **Health Monitoring**: Built-in health check system with web endpoints
- **Docker Support**: Easy deployment with Docker containers
- **Configurable**: Flexible configuration for addresses, tokens, and intervals
- **Error Handling**: Robust error handling with detailed logging

## 📋 Prerequisites

- Python 3.11+
- Infura API key
- Telegram Bot Token
- Docker (optional)

## 🛠️ Installation

### Method 1: Local Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/br3d/eth-balance-checker.git
   cd eth-balance-checker
   ```

2. **Install dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your actual values
   ```

4. **Configure the bot**
   ```bash
   # Edit config.json with your addresses and settings
   ```

5. **Run the bot**
   ```bash
   python main.py
   ```

### Method 2: Docker Installation

1. **Build the Docker image**
   ```bash
   docker build -t eth-balance-checker .
   ```

2. **Run the container**
   ```bash
   docker run -d \
     --name eth-balance-checker \
     -e INFURA_URL="https://mainnet.infura.io/v3/YOUR_API_KEY" \
     -e TELEGRAM_BOT_TOKEN="YOUR_BOT_TOKEN" \
     -e TELEGRAM_CHAT_ID="YOUR_CHAT_ID" \
     -p 8000:8000 \
     eth-balance-checker
   ```

## ⚙️ Configuration

### Environment Variables (.env)

Create a `.env` file with the following variables:

```env
# Infura API configuration
INFURA_URL=https://mainnet.infura.io/v3/YOUR_INFURA_API_KEY

# Telegram Bot configuration
TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID=YOUR_TELEGRAM_CHAT_ID
```

### Configuration File (config.json)

```json
{
  "ethereum_addresses": [
    "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
  ],
  "coins_list": ["usdt", "usdc", "dai"],
  "checking_interval": 600,
  "log_level": "INFO"
}
```

#### Configuration Options

- **ethereum_addresses**: Array of Ethereum addresses to monitor
- **coins_list**: Array of token symbols to check (e.g., "usdt", "usdc", "dai")
- **checking_interval**: Balance check interval in seconds (default: 600 = 10 minutes)
- **log_level**: Logging level ("DEBUG", "INFO", "ERROR")

## 🔧 Setup Guide

### 1. Get Infura API Key

1. Visit [Infura.io](https://infura.io/)
2. Create an account and new project
3. Copy your project's API endpoint URL

### 2. Create Telegram Bot

1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Use `/newbot` command and follow instructions
3. Save the bot token
4. Get your chat ID by messaging [@userinfobot](https://t.me/userinfobot)

### 3. Configure Addresses and Tokens

Edit `config.json` to add:
- Your Ethereum addresses
- Token symbols you want to monitor
- Check interval (in seconds)

## 🏥 Health Monitoring

The bot includes a built-in health monitoring system accessible via HTTP endpoints.

### Health Check Endpoints

- **GET /** - Main health check endpoint
  - Returns HTTP 200 if all systems are healthy
  - Returns HTTP 500 if any system is unhealthy
  - Response includes all health status items and timestamp

### Example Health Check Response

**Healthy (HTTP 200):**
```json
{
  "eth_rpc_initialized": true,
  "telegram_bot_initialized": true,
  "eth_rpc_status": true,
  "timestamp": "2024-01-15T14:30:00.123456"
}
```

**Unhealthy (HTTP 500):**
```json
{
  "eth_rpc_initialized": true,
  "telegram_bot_initialized": false,
  "eth_rpc_status": true,
  "timestamp": "2024-01-15T14:30:00.123456"
}
```

### Health Check Usage

```bash
# Check health status
curl http://localhost:8000/

# Using Docker
curl http://localhost:8000/
```

## 📊 Monitoring

### Logs

The bot provides detailed logging for:
- Balance check cycles
- Health status changes
- Error conditions
- Telegram notifications

### Health Status Items

- **eth_rpc_initialized**: Infura connection established
- **telegram_bot_initialized**: Telegram bot working
- **eth_rpc_status**: Recent API calls successful

## 🐳 Docker

### Dockerfile Features

- Python 3.11 slim base image
- Non-root user for security
- Health check integration
- Port 8000 exposed for health monitoring

### Docker Commands

```bash
# Build image
docker build -t eth-balance-checker .

# Run container
docker run -d --name eth-balance-checker \
  -e INFURA_URL="your_url" \
  -e TELEGRAM_BOT_TOKEN="your_token" \
  -e TELEGRAM_CHAT_ID="your_chat_id" \
  -p 8000:8000 \
  eth-balance-checker

# View logs
docker logs eth-balance-checker

# Check health
curl http://localhost:8000/
```

## 🧪 Testing

### Test Health Check

```bash
python test_healthcheck.py
```

This will start a test health check server and demonstrate the functionality.

## 📁 Project Structure

```
eth-balance-checker/
├── main.py                 # Main application
├── healthcheck.py          # Health monitoring module
├── test_healthcheck.py     # Health check testing
├── config.json            # Configuration file
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── env.example          # Environment variables template
├── .env                 # Your environment variables (create this)
└── README.md           # This file
```

## 🔍 Troubleshooting

### Common Issues

1. **"Failed to initialize PyEtherBalance"**
   - Check your Infura URL in `.env`
   - Verify your Infura API key is valid

2. **"Failed to send Telegram message"**
   - Verify your bot token and chat ID
   - Ensure the bot is not blocked

3. **Health check returns 500**
   - Check the logs for specific error messages
   - Verify all environment variables are set correctly

4. **"No module named 'flask'"**
   - Install dependencies: `pip install -r requirements.txt`

### Logs

Check logs for detailed error information:
```bash
# Local
python main.py

# Docker
docker logs eth-balance-checker
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues:

1. Check the troubleshooting section
2. Review the logs for error messages
3. Verify your configuration
4. Open an issue on GitHub

## 🔄 Updates

The bot will:
- Send notifications when balances change
- Log all activities
- Provide health status via HTTP endpoints
- Handle errors gracefully

Monitor the health endpoint to ensure the bot is running properly!