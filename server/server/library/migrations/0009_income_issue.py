# Generated by Django 4.2.7 on 2023-12-10 22:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0008_alter_bookissue_due_date_alter_bookissue_issue_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='income',
            name='issue',
            field=models.OneToOneField(default=7, on_delete=django.db.models.deletion.CASCADE, related_name='receipt', to='library.bookissue'),
        ),
    ]
