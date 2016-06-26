from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.base import View, logger

from inventory.models import Product, Category


class StoreView(TemplateView):
    template_name = "store/store.html"


class InventoryJsonView(View):
    def get(self, request):
        qs = Category.objects.filter(parent=None)
        payload = [
            {
                'id': d.id,
                'title': d.title,
                'description': d.description,
                'img': d.image_url,
                'inventory': [
                    {
                        'id': p.id,
                        'title': p.title,
                        'description': p.description,
                        'price': p.price,
                        'img': p.image_url,
                        'parent': p.parent.id,
                    } for p in d.get_children().all()],
            } for d in qs]

        return JsonResponse(payload, safe=False)
        # qs = Category.objects.all()
        # payload = []
        # for p in qs:
        #     # logger.error("For p in qs {}".format(p.id))
        #     # logger.error("For p in qs {}".format(p))
        #     if p.parent is None:
        #         # logger.error("Parent = None: {}".format(p.id))
        #         payload.append(
        #             {
        #                 'id': p.id,
        #                 'title': p.title,
        #                 'description': p.description,
        #                 'price': p.price,
        #                 'img': p.image_url,
        #                 'inventory': [],
        #             }
        #         )
        #     else:
        #         # logger.error("Parent = Parent: {}".format(p.id))
        #         # if(!payload[-1]['inventory']):
        #         #     payload[-1]['inventory'] = []
        #         payload[-1]['inventory'].append(
        #             {
        #                 'id': p.id,
        #                 'title': p.title,
        #                 'description': p.description,
        #                 'price': p.price,
        #                 'img': p.image_url,
        #                 'parent': p.parent.id,
        #             }
        #         )
        # payload = [{
        #                'id': p.id,
        #                'title': p.title,
        #                'description': p.description,
        #                'price': p.price,
        #                'image_url': p.image_url,
        #                 'parent': p.parent.id,
        #            } for p in qs]

        # return JsonResponse({'items':payload})
