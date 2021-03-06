from flask_restful import Resource
from flask import request, g
from flocx_market.objects import offer


class Offer(Resource):

    @classmethod
    def get(cls, marketplace_offer_id=None):

        if marketplace_offer_id is None:
            return [x.to_dict() for x in offer.Offer.get_all(g.context)]

        a = offer.Offer.get(marketplace_offer_id, g.context)
        if a is None:
            return {'message': 'Offer not found'}, 404
        else:
            return a.to_dict()

    @classmethod
    def post(cls):

        data = request.get_json(force=True)
        return offer.Offer.create(data, g.context).to_dict(), 201

    @classmethod
    def delete(cls, marketplace_offer_id):

        o = offer.Offer.get(marketplace_offer_id)
        if o is None:
            return {'message': 'Offer not found.'}, 404
        o.destroy(g.context)
        return {'message': 'Offer deleted.'}

    @classmethod
    def put(cls, marketplace_offer_id):

        data = request.get_json(force=True)
        o = offer.Offer.get(marketplace_offer_id, g.context)
        if o is None:
            return {'message': 'Offer not found.'}, 404
        # we only allow status field to be modified
        if 'status' in data:
            o.status = data['status']
            return o.save(g.context).to_dict()
        return o.to_dict()
