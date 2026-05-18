from django.db import migrations


def populate_categoria_from_feria(apps, schema_editor):
    # El cambio de tipo de campo y la migración de datos ya se realizaron en 0002.
    # Este migration file permanece para completar la cadena de migraciones sin acción adicional.
    return


def reverse_populate_categoria_from_feria(apps, schema_editor):
    # No safe reverse operation for this automatic population.
    return


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0002_categoria_alter_feria_categoria_sector"),
    ]

    operations = [
        migrations.RunPython(populate_categoria_from_feria, reverse_populate_categoria_from_feria),
    ]
