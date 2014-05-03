import logger
import time

def main():
    log_types = ['warning', 'error', 'info', 'ok', 'busy', 'bullshit']
    message = "This is a test message for the logger!!!!"
    
    for log_type in log_types:
        logger.log(log_type, message, time.strftime("%c"))
        
if __name__ == "__main__":
    main()
