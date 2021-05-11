import flask
import dash
from dash.dependencies import Input, Output
import flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

from layouts import layout1, layout2, layout3


server = flask.Flask(__name__)

# dash app 1
dash_app = dash.Dash(__name__, server=server, url_base_pathname='/dashboard/')
dash_app.layout = layout1

# dash app 2
dash_app2 = dash.Dash(__name__, server=server, url_base_pathname='/secondary-dashboard/')
dash_app2.layout = layout2

# dash app 3
dash_app3 = dash.Dash(__name__, server=server, url_base_pathname='/interactive-dashboard/')
dash_app3.layout = layout3

@dash_app3.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='my-input', component_property='value')
)
def update_output_div(input_value):
    return 'Output: {}'.format(input_value)


# server routes
@server.route('/')
def render_default_page():
    return '/dashboard /secondary-dashboard /interactive-dashboard'


@server.route('/dashboard/')
def render_dashboard():
    return flask.redirect('/dash1')


@server.route('/secondary-dashboard/')
def render_secondary_dashboard():
    return flask.redirect('/dash2')


@server.route('/interactive-dashboard/')
def render_interactive_dashboard():
    return flask.redirect('/dash3')


application = DispatcherMiddleware(server, {'/dash1': dash_app.server,
                                            '/dash2': dash_app2.server,
                                            '/dash3': dash_app3.server
                                            })


if __name__ == '__main__':
    run_simple('127.0.0.1', 8080, application, use_reloader=True, use_debugger=True)

