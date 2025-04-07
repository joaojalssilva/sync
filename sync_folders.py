import os
import shutil
import filecmp
import logging
import argparse
import time

def setup_logging(log_file_path):
    """Configures the logger to log messages both to console and to a log file."""
    logger = logging.getLogger("folder_sync")
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger

def sync_dirs(source, replica, logger):
    """Recursively synchronize the replica directory to match the source directory."""
    # Ensure both directories exist
    if not os.path.exists(source):
        logger.error(f"Source directory does not exist: {source}")
        raise FileNotFoundError(f"Source directory does not exist: {source}")
    
    # Create replica directory if it doesn't exist
    if not os.path.exists(replica):
        os.makedirs(replica)
        logger.info(f"Created directory: {replica}")
    
    # Compare the directories
    logger.info("Comparing directories...")
    dir_cmp = filecmp.dircmp(source, replica)
    
    # Copy files and directories that exist only in source
    for item in dir_cmp.left_only:
        src_path = os.path.join(source, item)
        dest_path = os.path.join(replica, item)
        try:
          if os.path.isdir(src_path):
              shutil.copytree(src_path, dest_path)
              logger.info(f"Directory copied: {src_path} -> {dest_path}")
          else:
              shutil.copy2(src_path, dest_path)
              logger.info(f"File copied: {src_path} -> {dest_path}")
        except Exception as e:
            logger.error(f"Error copying {src_path} to {dest_path}: {str(e)}")
    
    # Update files that are different
    for item in dir_cmp.diff_files:
        src_path = os.path.join(source, item)
        dest_path = os.path.join(replica, item)
        try:
          shutil.copy2(src_path, dest_path)
          logger.info(f"File updated: {src_path} -> {dest_path}")
        except Exception as e:
            logger.error(f"Error updating {dest_path}: {str(e)}")
    
    # Remove files and directories that exist only in replica
    for item in dir_cmp.right_only:
        dest_path = os.path.join(replica, item)
        try:
          if os.path.isdir(dest_path):
              shutil.rmtree(dest_path)
              logger.info(f"Directory removed: {dest_path}")
          else:
              os.remove(dest_path)
              logger.info(f"File removed: {dest_path}")
        except Exception as e:
            logger.error(f"Error removing {dest_path}: {str(e)}")
    
    # Recursively synchronize common subdirectories
    for common_dir in dir_cmp.common_dirs:
        sync_dirs(os.path.join(source, common_dir), os.path.join(replica, common_dir), logger)
        logger.info(f"Entering subdirectory: {common_dir}")

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Synchronizes two folders: source and replica. Maintains a full, identical copy of source folder at replica folder.')
    parser.add_argument('source', help='Path to source folder')
    parser.add_argument('replica', help='Path to replica folder')
    parser.add_argument('-i', '--interval', type=int, default=600, help='Time interval between syncs (in seconds)')
    parser.add_argument('-l', '--log_path', default="sync_log.txt", help='Path to the log file')
    
    args = parser.parse_args()

    # Setup logging
    logger = setup_logging(args.log_path)
    logger.info(f"Starting folder synchronization: {args.source} -> {args.replica}")
    logger.info(f"Sync interval: {args.interval} seconds")

    try:
        # Periodically synchronize
        while True:
            sync_dirs(args.source, args.replica, logger)
            logger.info("Synchronization complete. Waiting for next interval...")
            time.sleep(args.interval)
    except KeyboardInterrupt:
        logger.info("Synchronization stopped by user")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
