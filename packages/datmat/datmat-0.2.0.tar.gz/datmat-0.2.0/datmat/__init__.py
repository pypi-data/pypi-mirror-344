import uuid
from pathlib import Path

from yarl import URL

# Import one plugin from the plugins to trigger the whole sub-package to be loaded
from . import plugins, helpers
from .exceptions import DatmatMaterializeError
from .ioplugin import IOPlugin
from .models import BaseSample
from .typehints import urllike, pathlike

__version__ = "0.2.0"

PLUGINS = IOPlugin.PLUGIN_MAP


def materialize(inurl: urllike, outurl: urllike, tempdir: pathlike):
    """
    Materialize data from one place to another.

    :param inurl: URL to where the data is stored
    :type inurl: urllike
    :param outurl: URL to where the data needs to end up
    :type outurl: urllike
    :param tempdir: Temporary directory where the data will be downloaded to
    :type tempdir: pathlike
    :return: Sample information for the materialized data
    :rtype: BaseSample
    :raises DatmatMaterializeError: If materialization fails
    """
    tempdir = Path(tempdir)
    in_samples = pull_source_data(inurl, tempdir, str(uuid.uuid4()))
    out_samples = []
    for key, value in in_samples.items():
        # TODO: In the future: return sample list, with succes boolean. To be aggregated in a report.
        result, out_sample = push_sink_data(sample=value[0], outurl=outurl)
        if not result:
            # If any of the results fail, all of them fail. Raise an exception.
            raise DatmatMaterializeError()
        out_samples.append(out_sample)
        helpers.remove_file_dir(value[0].data_path)

    return out_samples[0]


def pull_source_data(url: urllike,
                     outdir: pathlike,
                     sample_id):
    """
    Retrieve data from an external source. This function checks the url scheme and
    selects the correct IOPlugin to retrieve the data.

    :param url: URL to pull data from
    :type url: urllike
    :param outdir: The directory to write the data to
    :type outdir: pathlike
    :param sample_id: Unique identifier for the sample being pulled
    :type sample_id: str
    :return: Dictionary of retrieved samples
    :rtype: dict
    """
    url = URL(url)
    outdir = Path(outdir)

    plugin_cls = IOPlugin.PLUGIN_MAP[url.scheme]

    with plugin_cls() as plugin:
        return plugin.pull_source_data(url, outdir, sample_id)


def push_sink_data(sample: BaseSample,
                   outurl: urllike):
    """
    Send data to an external source. This function checks the url scheme and
    selects the correct IOPlugin to push the data to.

    :param sample: Sample data to be pushed
    :type sample: BaseSample
    :param outurl: The URL to write the data to
    :type outurl: urllike
    :return: Tuple containing success status and the output sample
    :rtype: tuple
    """
    outurl = URL(outurl)
    plugin_cls = IOPlugin.PLUGIN_MAP[outurl.scheme]
    with plugin_cls() as plugin:
        return plugin.push_sink_data(sample=sample,
                                     outurl=outurl)
