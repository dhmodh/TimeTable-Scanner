# Generated by Django 3.1.6 on 2021-02-20 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TimeTable', '0004_auto_20210220_0847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scantimetablemodel',
            name='image',
            field=models.ImageField(default='image/White_thumb.png', upload_to='TimeTable/image/', verbose_name='Timetable Image'),
        ),
    ]