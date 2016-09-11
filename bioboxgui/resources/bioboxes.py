import os

from flask import abort
from flask_restful import marshal, Resource, fields, reqparse
from bioboxgui.api import auth, roles_accepted

from bioboxgui import models
from config import FOLDERS

regular_image = {
    'dockerhub': fields.String,
    'repo': fields.String,
    'source': fields.String
}

helper_interface = {
    'name': fields.String
}

regular_task = {
    'name': fields.String,
    'interface': fields.Nested(helper_interface)
}

regular_source = {
    'name': fields.String,
    'url': fields.String
}

regular_biobox = {
    'title': fields.String,
    'pmid': fields.Integer,
    'description': fields.String,
    'image': fields.Nested(regular_image),
    'homepage': fields.String,
    'mailing_list': fields.String,
    'tasks': fields.List(fields.Nested(regular_task)),
    'source': fields.Nested(regular_source)
}

regular_file = {
    'name': fields.String
}

class InputFiles(Resource):
    """Accessing all the input files."""
    @auth.login_required
    @roles_accepted('common', 'trusted', 'admin')
    def get(self):
        """
        Fetches all the input files' names.

        :return: json formatted list of file names.
        """
        files = [{'name': file} for file in os.listdir(FOLDERS['files'])]
        return marshal(files, regular_file, envelope="files");



class BioboxesAll(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'interface',
            type=str,
            required=False,
            location='args'
        )

    def get(self):
        """
        queries a list of available bioboxes.

        will be empty when no bioboxes are stored.
        :return: json formatted bioboxes.
        """
        args = self.reqparse.parse_args()
        interface = args.get('interface')
        if not interface:
            return get_all_bioboxes()
        else:
            result = models.get_bioboxes(interface)
            if not result:
                abort(404)
            return marshal(result, regular_biobox, envelope='bioboxes')

    @auth.login_required
    @roles_accepted('trusted', 'admin')
    def put(self):
        """
        updates the stored bioboxes.

        :return: json formatted bioboxes.
        """
        models.refresh()
        return get_all_bioboxes()


class BioboxId(Resource):
    def get(self, biobox_id):
        """
        fetches a single biobox with the given id.

        :param biobox_id: the pmid of the biobox.
        :return: a json formatted biobox.
        """
        result = models.Biobox.query.get(biobox_id)
        if not result:
            abort(404)
        return marshal(result, regular_biobox, envelope='biobox')


class BioboxName(Resource):
    def get(self, biobox_name):
        """
        fetches a single biobox with the given id.

        :param biobox_id: the pmid of the biobox.
        :return: a json formatted biobox.
        """
        result = models.Biobox.query.filter_by(
            title=biobox_name
        ).first()
        if not result:
            abort(404)
        return marshal(result, regular_biobox, envelope='biobox')


def get_all_bioboxes():
    bioboxes = models.Biobox.query.order_by(models.Biobox.title).all()
    return marshal(bioboxes, regular_biobox, envelope='bioboxes')
