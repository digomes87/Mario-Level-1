#!/usr/bin/env python
__author__ = "justinarmstrong"

"""
This is an attempt to recreate the first level of
Super Mario Bros for the NES.
"""

import cProfile
import sys
import logging
import traceback
from datetime import datetime

import pygame as pg

from data.main import main

# Configure logging system
def setup_logging():
    """Setup logging configuration to capture errors and debug info"""
    log_filename = f"mario_debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler(sys.stdout)  # Also print to console
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("=== Mario Game Debug Session Started ===")
    logger.info(f"Log file: {log_filename}")
    return logger

if __name__ == "__main__":
    logger = setup_logging()
    
    try:
        logger.info("Starting Mario game...")
        main()
        logger.info("Game ended normally")
    except Exception as e:
        logger.error("CRITICAL ERROR occurred during game execution!")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Error message: {str(e)}")
        logger.error("Full traceback:")
        logger.error(traceback.format_exc())
        
        # Print error to console as well
        print("\n" + "="*50)
        print("ERRO CAPTURADO!")
        print("="*50)
        print(f"Tipo do erro: {type(e).__name__}")
        print(f"Mensagem: {str(e)}")
        print("\nTraceback completo:")
        print(traceback.format_exc())
        print("="*50)
        
    finally:
        logger.info("Cleaning up and exiting...")
        pg.quit()
        sys.exit()
