# Generated by Django 4.1.4 on 2023-01-16 07:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0011_notificatiions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificatiions',
            name='users',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='student.student'),
        ),
    ]