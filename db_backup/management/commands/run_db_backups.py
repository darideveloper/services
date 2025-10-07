import os
import subprocess
from django.core.files.uploadedfile import SimpleUploadedFile

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings

from db_backup import models


BASE_FILE = os.path.basename(__file__)


class Command(BaseCommand):
    help = "Save all databases backups"

    def handle(self, *args, **kwargs):

        def backup_database(host, port, database, user, password, backup_dir):
            """
            Backup a PostgreSQL database using pg_dump.

            Args:
                host (str): Database host
                port (int): Database port
                database (str): Database name
                user (str): Database user
                password (str): Database password
                backup_dir (str): Directory to save backup file

            Returns:
                str: Path to the backup file
            """
            # Create backup directory if it doesn't exist
            os.makedirs(backup_dir, exist_ok=True)

            # Generate backup filename with timestamp
            timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(backup_dir, f"backup_{timestamp}.sql")

            # Set password as environment variable (pg_dump reads from PGPASSWORD)
            env = os.environ.copy()
            env["PGPASSWORD"] = password

            # Build pg_dump command
            cmd = [
                "pg_dump",
                "-h",
                host,
                "-p",
                str(port),
                "-U",
                user,
                "-d",
                database,
                "-F",
                "p",  # plain text SQL format
                "-f",
                backup_file,
            ]

            try:
                print(f"Starting backup of database '{database}'...")
                subprocess.run(cmd, env=env, check=True, capture_output=True)
                print(f"Backup completed successfully: {backup_file}")
            except subprocess.CalledProcessError as e:
                print(f"Backup failed: {e.stderr.decode()}")
                raise

            return backup_file

        backup_dir = os.path.join(settings.BASE_DIR, "backups")

        # Create temp backup folder if not exists
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        # Access to each db porgressl credential
        credentials = models.Credentials.objects.filter(enabled=True)

        for credential in credentials:

            print(f"Backing up database {credential}...")

            # Run the backup command
            backup_file = backup_database(
                credential.host,
                credential.port,
                credential.database,
                credential.username,
                credential.password,
                backup_dir,
            )

            # Create a backup of the database
            print("Uploading backup to AWS S3...")
            file = SimpleUploadedFile(backup_file, open(backup_file, "rb").read())
            models.Backup.objects.create(credentials=credential, backup_file=file)

            # Delete older backups
            print("Deleting older backups...")
            backups = models.Backup.objects.filter(credentials=credential).order_by(
                "-created_at"
            )
            backups_to_keep = credential.backups_to_keep
            backups_to_delete = backups[backups_to_keep:]
            print(f"Deleting {len(backups_to_delete)} backups...")
            for backup in backups_to_delete:
                backup.delete()

            print("Old backups deleted successfully")
            print("Done")
            print("--------------------------------")