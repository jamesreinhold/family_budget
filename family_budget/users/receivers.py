import logging

from django.contrib.auth import get_user_model
from django.db import transaction as db_transaction
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from budget.choices import ModelChoices
from budget.models import BudgetItem

User = get_user_model()
logger = logging.getLogger(__name__) 


@receiver(post_save, sender=BudgetItem)
def on_budget_item_created(sender, instance, created, *args, **kwargs):
    logger.info(f"{__name__}: Handling post_save signal...")
    if created:
        with db_transaction.atomic():
            user = User.objects.select_for_update().get(id=instance.user.id)
            if instance.item_type == ModelChoices.BUDGET_ITEM_TYPE_INCOME:
                logger.info(f"{__name__}: Updating income.. <> {instance.total}")
                user.income += instance.total
            else:
                logger.info(f"{__name__}: Updating expenses..  <> {instance.total}")
                user.expenses += instance.total
            user.save()
            logger.info(f"{__name__}: User profile updated on post_save")
            logger.info(f"{__name__}: INCOME: {user.income}, EXPENSES: {user.expenses}")
    
    logger.info(f"{__name__}: Successfully handled post_save signal")



@receiver(pre_delete, sender=BudgetItem)
def on_budget_item_deleted(sender, instance, *args, **kwargs):
    logger.info(f"{__name__}: Handling pre_delete signal...")
    with db_transaction.atomic():
        user = User.objects.select_for_update().get(id=instance.user.id)
        if instance.item_type == ModelChoices.BUDGET_ITEM_TYPE_INCOME:
            logger.info(f"{__name__}: Updating income...")
            user.income -= instance.total
        else:
            logger.info(f"{__name__}: Updating expenses...")
            user.expenses -= instance.total
        user.save()
        logger.info(f"{__name__}: User profile updated on post_save")
    
    logger.info(f"{__name__}: Successfully handled pre_delete signal")
