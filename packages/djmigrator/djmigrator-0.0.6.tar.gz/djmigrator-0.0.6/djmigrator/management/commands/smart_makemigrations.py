from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection
from django.apps import apps
from django.db.migrations.loader import MigrationLoader

class Command(BaseCommand):
    help = "Smart DB sync: detects DB-model mismatch, generates required migrations, and applies only necessary changes."

    def handle(self, *args, **options):
        self.stdout.write("🔍 Starting smart DB intelligent sync...")

        missing_changes_detected = False

        with connection.cursor() as cursor:
            tables = connection.introspection.table_names()

            for model in apps.get_models():
                table_name = model._meta.db_table

                if table_name not in tables:
                    self.stdout.write(self.style.ERROR(f"❌ Table missing in DB: {table_name}"))
                    missing_changes_detected = True
                    continue

                # Existing table — check columns
                db_columns = connection.introspection.get_table_description(cursor, table_name)
                db_column_names = {col.name for col in db_columns}

                model_field_names = {field.column for field in model._meta.fields if not getattr(field, 'auto_created', False)}

                missing_in_db = model_field_names - db_column_names
                extra_in_db = db_column_names - model_field_names

                if missing_in_db:
                    self.stdout.write(self.style.WARNING(f"⚠️ Missing columns in DB for table `{table_name}`: {missing_in_db}"))
                    missing_changes_detected = True

                # Extra columns generally we don't drop automatically
                if extra_in_db:
                    self.stdout.write(self.style.NOTICE(f"ℹ️ Extra columns in DB (not affecting model sync): {extra_in_db}"))

        # Check if any migrations exist
        loader = MigrationLoader(connection)
        applied = loader.applied_migrations
        self.stdout.write(f"✅ Total migrations applied: {len(applied)}")

        if missing_changes_detected:
            self.stdout.write("🛠️ Missing things detected. Running makemigrations...")
            try:
                call_command('makemigrations', interactive=False)
                self.stdout.write("🚀 Applying migrations to database (smart mode)...")

                # Apply migrations, using fake-initial to avoid 'already exists' errors
                call_command('migrate', fake_initial=True)

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Error while migrating: {e}"))
        else:
            self.stdout.write(self.style.SUCCESS("✅ Database schema matches Django models. No migrations needed."))

