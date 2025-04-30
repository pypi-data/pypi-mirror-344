import os
import sys
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection, OperationalError
from django.apps import apps
from django.db.migrations.loader import MigrationLoader
from django.db.migrations.recorder import MigrationRecorder

class Command(BaseCommand):
    help = "Smart DB sync: Fully auto-fixes DB-model mismatches, missing tables, migrations, and ensures correct migration files."

    def add_arguments(self, parser):
        parser.add_argument('--repair', action='store_true', help="Auto-repair database schema, missing tables, and migrations.")

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("🔍 Starting Smart Database Intelligent Sync..."))

        missing_tables = set()
        missing_columns = []
        apps_to_rebuild = set()
        missing_changes_detected = False  # <-- You forgot this before

        with connection.cursor() as cursor:
            tables = connection.introspection.table_names()

            for model in apps.get_models():
                if not model._meta.managed:
                    continue
                table_name = model._meta.db_table

                if table_name not in tables:
                    self.stdout.write(self.style.ERROR(f"❌ Missing Table in Database: {table_name}"))
                    missing_tables.add(model._meta.app_label)
                    apps_to_rebuild.add(model._meta.app_label)
                    missing_changes_detected = True
                    continue

                db_columns = {col.name for col in connection.introspection.get_table_description(cursor, table_name)}
                model_field_names = {field.column for field in model._meta.fields if not getattr(field, 'auto_created', False)}

                missing_in_db = model_field_names - db_columns
                extra_in_db = db_columns - model_field_names

                if missing_in_db:
                    self.stdout.write(self.style.WARNING(f"⚠️ Missing Columns in `{table_name}`: {missing_in_db}"))
                    missing_columns.append((table_name, missing_in_db))
                    missing_changes_detected = True

                if extra_in_db:
                    self.stdout.write(self.style.NOTICE(f"ℹ️ Extra Columns in `{table_name}` (ignored): {extra_in_db}"))

        # 🔧 Auto-repair missing columns
        if options['repair'] and missing_columns:
            self.stdout.write(self.style.MIGRATE_LABEL("🔧 Repair Mode: Adding missing columns to database..."))
            with connection.schema_editor() as schema_editor:
                for table_name, fields in missing_columns:
                    model_class = self.get_model_from_table(table_name)
                    if model_class:
                        for field_name in fields:
                            field = next((f for f in model_class._meta.fields if f.column == field_name), None)
                            if field:
                                try:
                                    schema_editor.add_field(model_class, field)
                                    self.stdout.write(self.style.SUCCESS(f"✅ Added Column `{field_name}` to `{table_name}`"))
                                except Exception as e:
                                    self.stdout.write(self.style.ERROR(f"❌ Could not add `{field_name}` to `{table_name}`: {e}"))

        loader = MigrationLoader(connection, ignore_no_migrations=True)
        recorder = MigrationRecorder(connection)
        applied_migrations = set(recorder.applied_migrations())

        self.stdout.write(self.style.MIGRATE_HEADING(f"✅ Current Applied Migrations: {len(applied_migrations)}"))

        # 🛠 If missing tables detected —> force makemigrations for their apps
        if missing_tables:
            self.stdout.write(self.style.WARNING(f"⚡ Missing tables detected for apps: {missing_tables}. Forcing makemigrations..."))
            for app_label in apps_to_rebuild:
                try:
                    call_command('makemigrations', app_label, interactive=False)
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"❌ Failed makemigrations for {app_label}: {e}"))

        # 🛠 Always try general makemigrations
        if missing_changes_detected or options['repair']:
            self.stdout.write(self.style.MIGRATE_HEADING("🛠️ Running makemigrations..."))
            try:
                call_command('makemigrations', interactive=False)
            except Exception as e:
                if 'It is impossible to add a non-nullable field' in str(e):
                    self.stdout.write(self.style.WARNING("⚠️ Non-Nullable Field Error Detected. Asking for default values..."))
                    for model in apps.get_models():
                        for field in model._meta.fields:
                            if not field.null and not field.has_default():
                                default_value = input(f"🔹 Enter default value for '{model._meta.model_name}.{field.name}': ")
                                field.default = default_value
                    self.stdout.write(self.style.MIGRATE_HEADING("🔁 Retrying makemigrations after setting defaults..."))
                    call_command('makemigrations', interactive=False)
                elif 'is applied before its dependency' in str(e):
                    self.stdout.write(self.style.WARNING("⚠️ Broken Migration History Detected. Cleaning up..."))
                    loader = MigrationLoader(connection, ignore_no_migrations=True)
                    broken_apps = set()
                    for (app_label, migration_name), migration in loader.disk_migrations.items():
                        for dependency in migration.dependencies:
                            if dependency not in loader.applied_migrations:
                                broken_apps.add(app_label)
                                broken_apps.add(dependency[0])

                    for app_label in broken_apps:
                        self.stdout.write(self.style.WARNING(f"🧹 Removing migration records and files for: {app_label}"))
                        recorder.Migration.objects.filter(app=app_label).delete()

                        try:
                            app_config = apps.get_app_config(app_label)
                            migrations_path = os.path.join(app_config.path, 'migrations')
                            if os.path.exists(migrations_path):
                                for filename in os.listdir(migrations_path):
                                    if filename != "__init__.py" and filename.endswith(".py"):
                                        os.remove(os.path.join(migrations_path, filename))
                                self.stdout.write(self.style.SUCCESS(f"🧹 Deleted migration files for `{app_label}`"))
                        except Exception as cleanup_error:
                            self.stdout.write(self.style.ERROR(f"❌ Failed to delete migration files for `{app_label}`: {cleanup_error}"))

                    self.stdout.write(self.style.MIGRATE_HEADING(f"🔁 Retrying makemigrations after cleaning: {broken_apps}"))
                    call_command('makemigrations', interactive=False)
                else:
                    self.stdout.write(self.style.ERROR(f"❌ makemigrations failed unexpectedly: {e}"))
                    sys.exit(1)

            # 🛠 Final migrate step
            self.stdout.write(self.style.MIGRATE_HEADING("🚀 Applying Migrations (fake_initial=True)..."))
            try:
                call_command('migrate', fake_initial=True)
            except OperationalError as migrate_error:
                if 'already exists' in str(migrate_error):
                    self.stdout.write(self.style.WARNING("⚠️ Table already exists. Marking migrations as applied..."))
                    loader = MigrationLoader(connection, ignore_no_migrations=True)
                    for (app_label, migration_name), migration in loader.disk_migrations.items():
                        recorder.record_applied(app_label, migration_name)
                    self.stdout.write(self.style.MIGRATE_HEADING("🔁 Retrying migrate after marking migrations as applied..."))
                    call_command('migrate', fake_initial=True)
                else:
                    self.stdout.write(self.style.ERROR(f"❌ Migration failed: {migrate_error}"))
                    sys.exit(1)
        else:
            self.stdout.write(self.style.SUCCESS("✅ Database schema is fully synchronized with Django models."))

        self.stdout.write(self.style.SUCCESS("🏁 Smart Database Intelligent Sync completed successfully!"))

    def get_model_from_table(self, table_name):
        for model in apps.get_models():
            if model._meta.db_table == table_name:
                return model
        return None
