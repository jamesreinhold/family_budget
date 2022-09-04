# Generated by Django 3.2.15 on 2022-09-04 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='expenses',
            field=models.DecimalField(decimal_places=2, default=0.0, help_text='The total amount of expenses of the user.', max_digits=9, verbose_name='Expenses'),
        ),
        migrations.AddField(
            model_name='user',
            name='income',
            field=models.DecimalField(decimal_places=2, default=0.0, help_text='The total amount of income of the user', max_digits=9, verbose_name='Income'),
        ),
    ]
