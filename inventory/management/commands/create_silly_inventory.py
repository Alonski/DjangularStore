from django.core.management.base import BaseCommand
import silly

from inventory.models import Product, Category


class Command(BaseCommand):
    help = "Create silly inventory items."

    def handle(self, *args, **options):
        # Product.objects.all().delete()

        for i in range(5):
            parent_title = "{} {}".format(silly.adjective(), silly.noun())
            parent_desc = silly.paragraph(length=2) + "\n" + silly.paragraph(length=2)

            parent = Category.objects.create(
                title=parent_title,
                description=parent_desc,
            )

            for j in range(5):
                title = "{} {}".format(silly.adjective(), silly.noun())
                desc = silly.paragraph(length=2) + "\n" + silly.paragraph(length=2)
                price = silly.number() + silly.number() / 10
                image_url = silly.image();
                Category.objects.create(
                    title=title,
                    description=desc,
                    price=price,
                    image_url=image_url,
                    parent=parent
                )

                # for i in range(100):
                #         title = "{} {}".format(silly.adjective(), silly.noun())
                #         desc = silly.paragraph(length=2) + "\n" + silly.paragraph(length=2)
                #         price = silly.number() + silly.number() / 10
                #
                #         Product.objects.create(
                #             title=title,
                #             description=desc,
                #             price=price,
                #             image_url=silly.image(),
                #         )
                #
                #     print("OK")
