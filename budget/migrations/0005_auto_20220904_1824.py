# Generated by Django 3.2.15 on 2022-09-04 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0004_alter_budgetitem_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='budgetitem',
            name='cost',
        ),
        migrations.AddField(
            model_name='budgetitem',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0.0, help_text='The amount value of the budget item.', max_digits=9, verbose_name='Amount'),
        ),
        migrations.AddField(
            model_name='budgetitem',
            name='type',
            field=models.CharField(choices=[('INCOME', 'INCOME'), ('EXPENSE', 'EXPENSE')], default='EXPENSE', help_text='The type of budget item.', max_length=7),
        ),
        migrations.AlterField(
            model_name='budgetitem',
            name='quantity',
            field=models.PositiveSmallIntegerField(blank=True, default=0, help_text='If quantity is more than 1, specify the quality of the budget item. Defaults to 1. Quantity is required if `type` is `EXPENSE`.', null=True),
        ),
    ]