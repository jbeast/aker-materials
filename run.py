import os
import logging
import redis
from eve import Eve
from flask import g, request
from flask_bootstrap import Bootstrap
from eve_docs import eve_docs

SETTINGS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.py')

# Create redis binding
r = redis.StrictRedis(host='localhost', port=6379, db=0)

# Create the EVE app
app = Eve(settings=SETTINGS_PATH)

# Bootstrap the docs
Bootstrap(app)
app.register_blueprint(eve_docs, url_prefix='/docs')

# Event Hooks
# On Updated Biomaterial - Add/Remove it Sets
def after_materials_update(updates, original):
  material_id = str(request.view_args['_id'])

  updated_sets = set(updates.get('sets', []))
  original_sets = set(original.get('sets', []))

  added = updated_sets - original_sets
  removed = original_sets - updated_sets

  for set_id in added:
    r.sadd('aker.set.' + str(set_id) + '.materials', material_id)

  for set_id in removed:
    r.srem('aker.set.' + str(set_id) + '.materials', material_id)

app.on_updated_materials += after_materials_update

if __name__ == '__main__':

  # enable logging to 'app.log' file
  handler = logging.FileHandler('app.log')

  # set a custom log format, and add request
  # metadata to each log line
  handler.setFormatter(logging.Formatter(
      '%(asctime)s %(levelname)s: %(message)s '
      '[in %(filename)s:%(lineno)d] -- ip: %(clientip)s, '
      'url: %(url)s, method:%(method)s'))

  # the default log level is set to WARNING, so
  # we have to explictly set the logging level
  # to INFO to get our custom message logged.
  app.logger.setLevel(logging.INFO)

  # append the handler to the default application logger
  app.logger.addHandler(handler)

  app.run()