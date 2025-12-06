from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from chat.models import ChatMessage


class Command(BaseCommand):
    help = 'Delete chat messages older than 1 year'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting',
        )

    def handle(self, *args, **options):
        # Calculate date 1 year ago
        one_year_ago = timezone.now() - timedelta(days=365)
        
        # Get old messages
        old_messages = ChatMessage.objects.filter(timestamp__lt=one_year_ago)
        count = old_messages.count()
        
        if options['dry_run']:
            self.stdout.write(
                self.style.WARNING(
                    f'DRY RUN: Would delete {count} messages older than {one_year_ago.strftime("%Y-%m-%d")}'
                )
            )
            
            # Show sample of messages that would be deleted
            if count > 0:
                self.stdout.write('\nSample of messages to be deleted:')
                for msg in old_messages[:5]:
                    self.stdout.write(
                        f'  - [{msg.timestamp}] {msg.user.username} in {msg.room.name}: {msg.content[:50]}'
                    )
                if count > 5:
                    self.stdout.write(f'  ... and {count - 5} more')
        else:
            # Actually delete the messages
            deleted_count, _ = old_messages.delete()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully deleted {deleted_count} messages older than {one_year_ago.strftime("%Y-%m-%d")}'
                )
            )
