# Generated by Django 2.1.4 on 2019-02-23 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20190104_1227'),
    ]

    operations = [
        migrations.CreateModel(
            name='PDF_Files',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.CharField(max_length=100)),
                ('Description', models.CharField(max_length=100)),
                ('pdf', models.FileField(upload_to='handout_pdf')),
            ],
        ),
    ]
