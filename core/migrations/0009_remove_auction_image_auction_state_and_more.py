# Generated by Django 4.2.11 on 2024-06-27 23:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0008_auction_category"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="auction",
            name="image",
        ),
        migrations.AddField(
            model_name="auction",
            name="state",
            field=models.IntegerField(
                choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")],
                default=1,
                help_text="Auction State",
            ),
        ),
        migrations.AlterField(
            model_name="auction",
            name="category",
            field=models.CharField(
                blank=True, help_text="Auction category", max_length=50
            ),
        ),
        migrations.CreateModel(
            name="AuctionImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(help_text="Auction image", upload_to="auctions/"),
                ),
                (
                    "uploaded_at",
                    models.DateTimeField(
                        auto_now_add=True, help_text="Image upload date"
                    ),
                ),
                (
                    "auction",
                    models.ForeignKey(
                        help_text="Auction related",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.auction",
                    ),
                ),
            ],
        ),
    ]
