# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-07 09:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


SUBSCRIPTION_TO_BILLINGTYPE = {
    "DL-Budget": "Engineering Budget",
    "SLA Störungsbehebung": "SLA Incident Management",
    "Software Maintenance Abonnement": "Software Maintenance",
    "SySupport-Premium": "SSA Premium",
    "SySupport-Standard": "SSA Standard",
}


def migrate_packages(apps, schema_editor):
    """Map package subscription to billing type."""
    Package = apps.get_model("subscription", "Package")
    BillingType = apps.get_model("projects", "BillingType")

    for subscription, billing_type in SUBSCRIPTION_TO_BILLINGTYPE.items():
        pkgs = Package.objects.filter(subscription__name=subscription)
        if pkgs.exists():
            billing_type, _ = BillingType.objects.get_or_create(name=billing_type)
            pkgs.update(billing_type=billing_type)

    # delete all obsolete packages
    Package.objects.filter(billing_type__isnull=True).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0005_auto_20170907_0938"),
        ("subscription", "0002_auto_20170808_1729"),
    ]

    operations = [
        migrations.RemoveField(model_name="subscriptionproject", name="project"),
        migrations.RemoveField(model_name="subscriptionproject", name="subscription"),
        migrations.AddField(
            model_name="package",
            name="billing_type",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="projects.BillingType",
                related_name="packages",
            ),
            preserve_default=False,
        ),
        migrations.RunPython(migrate_packages),
        migrations.RemoveField(model_name="package", name="subscription"),
        migrations.DeleteModel(name="Subscription"),
        migrations.DeleteModel(name="SubscriptionProject"),
    ]
