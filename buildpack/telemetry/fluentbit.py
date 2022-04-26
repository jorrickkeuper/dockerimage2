import logging
import os
import subprocess
import shutil

from buildpack import util


NAMESPACE = "fluentbit"

CONF_FILENAME = f"{NAMESPACE}.conf"
FLUENTBIT_VERSION = "1.9.2"
FLUENTBIT_PACKAGE = f"fluent-bit-{FLUENTBIT_VERSION}.tar.gz"

LOGS_PORT = 9032


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
