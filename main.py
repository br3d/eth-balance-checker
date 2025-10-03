import pyetherbalance
import schedule
import time
import requests
import logging
import json
import os
from datetime import datetime
from telegram import Bot
from dotenv import load_dotenv
from healthcheck import HealthCheckServer

# Load environment variables
load_dotenv()
healthcheck_status = {"eth_rpc_initialized": False, "telegram_bot_initialized": False, "eth_rpc_status": False}

# Load configuration
def load_config():
    """Load configuration from JSON file and environment variables."""
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        logger.error("config.json not found. Please create it with the required configuration.")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing config.json: {e}")
        raise
    
    # Load sensitive data from environment variables
    config['infura_url'] = os.getenv('INFURA_URL')
    config['bot_token'] = os.getenv('TELEGRAM_BOT_TOKEN')
    config['chat_id'] = os.getenv('TELEGRAM_CHAT_ID')
    
    # Validate required environment variables
    required_env_vars = ['INFURA_URL', 'TELEGRAM_BOT_TOKEN', 'TELEGRAM_CHAT_ID']
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        logger.error("Please create a .env file with the required variables. See env.example for reference.")
        raise ValueError(f"Missing environment variables: {', '.join(missing_vars)}")
    
    return config

# Load configuration
config = load_config()

# Configure logging
log_level = getattr(logging, config.get('log_level', 'INFO').upper())
logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Get configuration values
infura_url = config['infura_url']
ethereum_addresses = config['ethereum_addresses']
chat_id = config['chat_id']
bot_token = config['bot_token']
coins_list = config['coins_list']
checking_interval = config['checking_interval']
previous_balances = {}  # Dictionary to track previous balances for each address/coin combination

# Initialize services
bot = Bot(token=bot_token)  # Initialize the Telegram bot
try:
    ethbalance = pyetherbalance.PyEtherBalance(infura_url)  # Create an pyetherbalance object
    healthcheck_status["eth_rpc_initialized"] = True
except Exception as e:
    logger.error(f"Failed to initialize PyEtherBalance: {str(e)}")
    healthcheck_status["eth_rpc_initialized"] = False
    raise

# Initialize health check server
health_check_server = HealthCheckServer(healthcheck_status, port=8000)


def check_token_balance(coin, address):
    # if coin is None:
    #     return ethbalance.get_eth_balance(address)
    # else:
    try:
        result = ethbalance.get_token_balance(coin.upper(), address)
        
        # Check if result contains an error status
        if isinstance(result, dict) and result.get('status') == 'error':
            logger.error(f"Error getting token balance for {coin.upper()}: {result.get('description', 'Unknown error')}")
            healthcheck_status["eth_rpc_status"] = False
            return result
        
        # Extract just the balance value from the result
        if isinstance(result, dict) and 'balance' in result:
            healthcheck_status["eth_rpc_status"] = True
            return result['balance']
        
        healthcheck_status["eth_rpc_status"] = True
        return result
    except Exception as e:
        logger.error(f"Failed to get token balance for {coin.upper()}: {str(e)}")
        healthcheck_status["eth_rpc_status"] = False
        raise


def send_notification(message):
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}"
        response = requests.get(url).json()
        
        if response.get('ok') != True:
            logger.error(f"Failed to send Telegram message: {response.get('description')}")
            healthcheck_status["telegram_bot_initialized"] = False
            return False
            
        logger.info(f"Message sent: {message}")
        logger.debug(f"Telegram API response: {response}")
        healthcheck_status["telegram_bot_initialized"] = True
        return True
        
    except Exception as e:
        logger.error(f"Exception while sending Telegram message: {str(e)}")
        healthcheck_status["telegram_bot_initialized"] = False
        return False


def main_check():
    global previous_balances
    logger.info("Starting balance check cycle")
    
    # Check if this is the first run (previous_balances is empty)
    is_first_run = len(previous_balances) == 0
    
    if is_first_run:
        # Collect all initial balances first
        initial_balances = []
        for ethereum_address in ethereum_addresses:
            for coin in coins_list:
                logger.info(f"Checking {coin} balance for address: {ethereum_address}")
                current_balance = check_token_balance(coin, ethereum_address)
                logger.info(f"Current {coin} balance: {current_balance}")
                previous_balances[(ethereum_address, coin)] = current_balance
                initial_balances.append(f"{coin.upper()}: {current_balance}")
        
        # Send single "Bot is up!" message with all balances
        logger.info("Bot is starting up - sending initial notification")
        all_balances_text = "\n".join(initial_balances)
        send_notification(f"🤖 Bot is up!\nBalances:\n{all_balances_text}")
        
    else:
        # Normal balance checking for subsequent runs
        for ethereum_address in ethereum_addresses:
            for coin in coins_list:
                logger.info(f"Checking {coin} balance for address: {ethereum_address}")
                current_balance = check_token_balance(coin, ethereum_address)
                logger.info(f"Current {coin} balance: {current_balance}")
                
                if current_balance != previous_balances[(ethereum_address, coin)]:
                    logger.info(f"{coin} balance changed from {previous_balances[(ethereum_address, coin)]} to {current_balance}")
                    send_notification(
                        f"💰 {coin} Balance changed! New balance: {current_balance}"
                    )
                else:
                    logger.info(f"{coin} balance unchanged: {current_balance}")
                
                previous_balances[(ethereum_address, coin)] = current_balance
    
    logger.info("Balance check cycle completed")


def main():
    logger.info("Starting ETH balance monitoring bot")
    logger.info(f"Monitoring addresses: {ethereum_addresses}")
    logger.info(f"Monitoring coins: {coins_list}")
    logger.info(f"Check interval: {checking_interval} seconds")
    
    # Start healthcheck server in a separate thread
    health_check_server.start_in_thread()
    
    # Run initial balance check
    main_check()
    
    # Schedule regular balance checks
    schedule.every(checking_interval).seconds.do(main_check)
    logger.info("Scheduler configured - starting main loop")
    
    while True:
        schedule.run_pending()
        time.sleep(1)


main()
