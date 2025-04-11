# Generated by Django 5.1.7 on 2025-04-02 18:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_alter_answerchoice_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_number', models.IntegerField()),
                ('content', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='book_pages/')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pages', to='library.book')),
            ],
        ),
    ]
