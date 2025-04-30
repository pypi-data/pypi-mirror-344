import argparse
import os

from amapy_server.app import create_app
from amapy_server.configs import Configs
from amapy_server.configs.configs import ConfigModes
from amapy_server.run_gunicorn import StandaloneApplication

PORT = 5000
HOST = '0.0.0.0'


def get_app(mode: str = None):
    try:
        config_mode = ConfigModes[mode]
    except KeyError:
        config_mode = ConfigModes.DEV
    Configs.shared(mode=config_mode)  # default is DEV
    return create_app()


def parse_args():
    parser = argparse.ArgumentParser(description='Run the asset server')
    parser.add_argument('protocol', choices=['http', 'https'], nargs='?', default='http',
                        help='Protocol to use (http or https)')
    parser.add_argument('--debug', action='store_true',
                        help='Run the server in debug mode')
    return parser.parse_args()


def main():
    # Parse command line arguments
    args = parse_args()

    mode = os.getenv('ASSET_CONFIG_MODE')
    app = get_app(mode=mode)

    options = {
        'bind': '%s:%s' % (HOST, PORT),
        'workers': 2,
    }
    if args.protocol == 'https':
        options['certfile'] = os.environ.get('SSL_CERT')  # os.path.join(MOUNT_DIR, CERT)
        options['keyfile'] = os.environ.get('SSL_KEY')  # os.path.join(MOUNT_DIR, KEY)

    if args.debug:
        print('running in debug mode')
        app.run(debug=True)
    else:
        print(f'running on: {args.protocol}')
        StandaloneApplication(app, options).run()


if __name__ == '__main__':
    main()
