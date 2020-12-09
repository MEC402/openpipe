from flask import Flask
from flask_marshmallow import Marshmallow
from flask_restful import Api

from FlaskEndpoints.services.FolderContent import FolderContent
from FlaskEndpoints.services.Assets import Asset
from FlaskEndpoints.services.Assets import Assets
from FlaskEndpoints.services.Folders import Folders, Folder

app = Flask(__name__)
ma = Marshmallow(app)

api = Api(app, prefix="/api/v1")

api.add_resource(Assets, '/assets')
api.add_resource(Asset, '/asset/<int:id>')

api.add_resource(Folders, '/folders')
api.add_resource(Folder, '/folder/<int:id>')

api.add_resource(FolderContent, '/foldercontent/<int:id>')


if __name__ == '__main__':
    app.run(debug=True)
