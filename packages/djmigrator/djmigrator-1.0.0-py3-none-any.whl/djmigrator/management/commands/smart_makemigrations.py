from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection
from django.apps import apps
from django.db.migrations.loader import MigrationLoader
from django.db.migrations.recorder import MigrationRecorder
import sys

class Command(BaseCommand):
    help = "Smart DB sync: detects DB-model mismatch, generates required migrations, and applies only necessary changes."

    def add_arguments(self, parser):
        parser.add_argument('--repair', action='store_true', help="Attempt to auto-fix missing columns and tables via SQL and migration re-sync.")

    def handle(self, *args, **options):
        self.stdout.write("🔍 Starting smart DB intelligent sync...")

        missing_changes_detected = False
        missing_tables = set()
        columns_to_add = []

        with connection.cursor() as cursor:
            tables = connection.introspection.table_names()

            for model in apps.get_models():
                if not model._meta.managed:
                    continue

                table_name = model._meta.db_table

                if table_name not in tables:
                    self.stdout.write(self.style.ERROR(f"❌ Table missing in DB: {table_name}"))
                    missing_tables.add(model._meta.app_label)
                    missing_changes_detected = True
                    continue

                db_columns = connection.introspection.get_table_description(cursor, table_name)
                db_column_names = {col.name for col in db_columns}
                model_fields = [field for field in model._meta.fields if not getattr(field, 'auto_created', False)]

                model_field_names = {field.column for field in model_fields}
                missing_in_db = model_field_names - db_column_names
                extra_in_db = db_column_names - model_field_names

                if missing_in_db:
                    self.stdout.write(self.style.WARNING(f"⚠️ Missing columns in DB for `{table_name}`: {missing_in_db}"))
                    missing_changes_detected = True
                    for field in model_fields:
                        if field.column in missing_in_db:
                            columns_to_add.append((table_name, field))

                if extra_in_db:
                    self.stdout.write(self.style.NOTICE(f"ℹ️ Extra columns in DB (not affecting model sync): {extra_in_db}"))

        # 🔥 Repair missing columns
        if options['repair'] and columns_to_add:
            self.stdout.write(self.style.MIGRATE_HEADING("🔧 Repair mode: Adding missing columns..."))
            with connection.schema_editor() as schema_editor:
                for table_name, field in columns_to_add:
                    try:
                        model_class = apps.get_model(field.model._meta.app_label, field.model._meta.model_name)
                        schema_editor.add_field(model_class, field)
                        self.stdout.write(self.style.SUCCESS(f"✅ Added column `{field.column}` to `{table_name}`"))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"❌ Failed to add column `{field.column}` to `{table_name}`: {e}"))

        loader = MigrationLoader(connection, ignore_no_migrations=True)
        recorder = MigrationRecorder(connection)
        applied_migrations = set(recorder.applied_migrations())
        self.stdout.write(f"✅ Total migrations applied: {len(applied_migrations)}")

        # 🛠 Handle missing tables and migrations
        if missing_changes_detected or options['repair']:
            self.stdout.write("🛠️ Running makemigrations...")
            try:
                call_command('makemigrations', interactive=False)
            except Exception as e:
                if 'It is impossible to add a non-nullable field' in str(e):
                    self.stdout.write(self.style.WARNING("⚠️ Non-nullable field without default detected."))
                    for model in apps.get_models():
                        for field in model._meta.fields:
                            if not field.null and not field.has_default():
                                default_value = input(f"Enter default value for '{model._meta.model_name}.{field.name}': ")
                                field.default = default_value
                    call_command('makemigrations', interactive=False)

                elif 'is applied before its dependency' in str(e):
                    self.stdout.write(self.style.WARNING("⚠️ Broken migration history detected. Auto-fixing..."))
                    # ➡ Delete all migration records for involved apps
                    for app_label in missing_tables:
                        self.stdout.write(f"🧹 Cleaning migration records for: {app_label}")
                        recorder.Migration.objects.filter(app=app_label).delete()
                    # Retry makemigrations
                    call_command('makemigrations', interactive=False)

                else:
                    self.stdout.write(self.style.ERROR(f"❌ Error while making migrations: {e}"))
                    sys.exit(1)

            self.stdout.write("🚀 Applying migrations to database (smart mode)...")
            call_command('migrate', fake_initial=True)

        else:
            self.stdout.write(self.style.SUCCESS("✅ Database schema matches Django models. No migrations needed."))

        self.stdout.write(self.style.SUCCESS("🏁 Smart sync completed successfully!"))
