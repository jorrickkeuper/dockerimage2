import logging
import os
import subprocess
import shutil
import socket

import backoff

from buildpack import util


NAMESPACE = "fluentbit"

CONF_FILENAME = f"{NAMESPACE}.conf"
FLUENTBIT_VERSION = "1.9.2"
FLUENTBIT_PACKAGE = f"fluent-bit-{FLUENTBIT_VERSION}.tar.gz"

LOGS_PORT = 5170


def stage(buildpack_dir, destination_path, cache_path):

    logging.info("Staging fluentbit ...")

    fluentbit_cdn_path = os.path.join(
        "/mx-buildpack", NAMESPACE, FLUENTBIT_PACKAGE
    )

    util.resolve_dependency(
        util.get_blobstore_url(fluentbit_cdn_path),
        # destination_path - DOT_LOCAL_LOCATION
        os.path.join(destination_path, NAMESPACE),
        buildpack_dir=buildpack_dir,
        cache_dir=cache_path,
    )

    shutil.copy(
        os.path.join(buildpack_dir, "etc", NAMESPACE, CONF_FILENAME),
        os.path.join(
            destination_path,
            NAMESPACE,
        ),
    )


def update_config(m2ee):

    util.upsert_logging_config(
        m2ee,
        {
            "type": "tcpjsonlines",
            "name": "FluentbitSubscriber",
            "autosubscribe": "INFO",
            "host": "localhost",
            "port": str(LOGS_PORT),
        },
    )


def run():
    fluentbit_dir = os.path.join(
        os.path.abspath(".local"),
        NAMESPACE,
    )

    fluentbit_bin_path = os.path.join(
        fluentbit_dir,
        "fluent-bit",
    )

    fluentbit_config_path = os.path.join(
        fluentbit_dir,
        CONF_FILENAME,
    )

    subprocess.Popen(
        (fluentbit_bin_path, "-c", fluentbit_config_path),
    )

    # The runtime does not handle a non-open logs endpoint socket
    # gracefully, so wait until it's up
    @backoff.on_predicate(backoff.expo, lambda x: x > 0, max_time=10)
    def _await_logging_endpoint():
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect_ex(
            ("localhost", LOGS_PORT)
        )

    logging.info("Awaiting fluentbit log subscriber...")
    if _await_logging_endpoint() == 0:
        logging.info("fluentbit log subscriber is ready")
    else:
        logging.error(
            "Fluentbit log subscriber was not initialized correctly."
            "Application logs will not be shipped to fluentbit."
        )
