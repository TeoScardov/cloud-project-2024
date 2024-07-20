from botocore.client import Config
import boto3
import os
import logging
import subprocess

# Setup the logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
    
def lambda_handler(event, context):
    # S3 and database details
    s3_bucket = os.getenv('S3_BUCKET')
    s3_key = os.getenv('S3_KEY')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT', '5432')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_name = os.getenv('DB_NAME')
    
    # Download the dump file from S3
    logger.info("Downloading dump file")
    try:
        config = Config(connect_timeout=5, retries={'max_attempts': 0})
        s3 = boto3.client('s3', config=config)
        dump_file_path = "/tmp/" + s3_key
        s3.download_file(s3_bucket, s3_key, dump_file_path)
        logger.info("Dump file successfully downloaded")
    except Exception as e:
        logger.error(f"Error downloading database dump: {str(e)}")
        return {
            'statusCode': 500,
            'body': f'Error downloading database dump: {str(e)}'
        }

    # Restore the dump file into the database using pg_restore
    logger.info("Restoring dump file into the database using pg_restore")
    try:
        command = [
            '/opt/bin/psql',
            '--host', db_host,
            '--port', db_port,
            '--username', db_user,
            '--dbname', db_name,
            '-f', dump_file_path
        ]

        # Set the PGPASSWORD environment variable for authentication
        env = os.environ.copy()
        env['PGPASSWORD'] = db_password

        result = subprocess.run(command, env=env, check=True, text=True, capture_output=True)
        logger.info("Restore output: %s", result.stdout)
        if result.stderr:
            logger.error("Restore error output: %s", result.stderr)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error during restore: {e.stderr}")
        return {
            'statusCode': 500,
            'body': f'Error loading database dump into db: {str(e)}'
        }

    return {
        'statusCode': 200,
        'body': 'Database loaded successfully!'
    }
