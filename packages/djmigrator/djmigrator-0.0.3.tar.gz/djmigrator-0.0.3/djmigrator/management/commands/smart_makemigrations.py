from django.core.management.base import BaseCommand
from django.db import connection
from django.apps import apps
from django.db.migrations.loader import MigrationLoader


class Command(BaseCommand):
    help = "Smart DB sync check: compares DB schema with models."

    def handle(self, *args, **options):
        self.stdout.write("🔍 Starting smart DB schema check...")

        with connection.cursor() as cursor:
            tables = connection.introspection.table_names()

            for model in apps.get_models():
                table_name = model._meta.db_table

                if table_name not in tables:
                    self.stdout.write(self.style.ERROR(f"❌ Table missing in DB: {table_name}"))
                    continue

                db_columns = connection.introspection.get_table_description(cursor, table_name)
                db_column_names = {col.name for col in db_columns}

                model_field_names = {field.column for field in model._meta.fields}

                missing_in_db = model_field_names - db_column_names
                extra_in_db = db_column_names - model_field_names

                if missing_in_db:
                    self.stdout.write(self.style.WARNING(f"⚠️ Missing columns in DB for table `{table_name}`: {missing_in_db}"))
                if extra_in_db:
                    self.stdout.write(self.style.WARNING(f"⚠️ Extra columns in DB not in model `{table_name}`: {extra_in_db}"))

        # Optional: Show migration history
        loader = MigrationLoader(connection)
        applied = loader.applied_migrations
        self.stdout.write(f"✅ Applied migrations: {len(applied)} total.")
