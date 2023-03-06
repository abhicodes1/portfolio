# Generated by Django 4.1.4 on 2023-01-06 05:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_alter_student_fee_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
                ('is_present', models.CharField(blank=True, choices=[('1', 'Present'), ('2', 'absent')], max_length=20, null=True)),
                ('name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student.student')),
            ],
        ),
    ]