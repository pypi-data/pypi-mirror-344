from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection, transaction
from django.apps import apps
from django.db.migrations.loader import MigrationLoader
from django.db.migrations.recorder import MigrationRecorder
from django.db import models

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
                # 🔥 Skip unmanaged models
                if not model._meta.managed:
                    continue

                table_name = model._meta.db_table

                if table_name not in tables:
                    self.stdout.write(self.style.ERROR(f"❌ Table missing in DB: {table_name}"))
                    missing_tables.add(table_name)
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

        # ----------------------
        # 🔥 Repair missing columns
        # ----------------------
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

        # ----------------------
        # 🔥 Handling missing tables
        # ----------------------
        if missing_changes_detected:
            self.stdout.write("🛠️ Missing things detected. Running makemigrations...")
            try:
                call_command('makemigrations', interactive=False)

                self.stdout.write("🚀 Applying migrations to database (smart mode)...")
                fake_apps = set()

                for model in apps.get_models():
                    if not model._meta.managed:
                        continue
                    if model._meta.db_table in missing_tables:
                        fake_apps.add(model._meta.app_label)

                # Handle apps needing reinitialization
                for app_label in fake_apps:
                    initial_key = (app_label, "0001_initial")
                    if initial_key in loader.disk_migrations:
                        if any(m[0] == app_label for m in applied_migrations):
                            self.stdout.write(f"🔁 Unapplying all applied migrations for: {app_label}")
                            recorder.Migration.objects.filter(app=app_label).delete()

                        self.stdout.write(f"🛠️ Applying initial migration for: {app_label}")
                        try:
                            call_command('migrate', app_label, fake_initial=True)
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f"❌ Error while applying {app_label} initial migration: {e}"))

                    else:
                        self.stdout.write(self.style.WARNING(f"⚠️ No initial migration found for app: {app_label}. Manual intervention may be required."))

                # Apply remaining migrations normally
                call_command('migrate')

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Error while migrating: {e}"))

        else:
            self.stdout.write(self.style.SUCCESS("✅ Database schema matches Django models. No migrations needed."))

        self.stdout.write(self.style.SUCCESS("🏁 Smart sync completed successfully!"))
