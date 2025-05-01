# Data Materialisation


## Getting started

Install `datmat` from PyPI:
```commandline
pip install datmat
```

In `datmat` you can interface with multiple data sources and storage solutions through a plugin system.
By linking together different plugins you can move data from one place to another.
A set of plugins is already installed when installing the package, but the program is set up to support development
of custom plugins. The plugins can be called by using a URL scheme to preface the path or URL to your file. For example,
by using `file:///home/user/file.txt` you can access the local file `/home/user/file.txt`, or by using
`xnat+https://xnat.health-ri.nl/projects/sandbox` you can access the XNAT project `sandbox` on `xnat.health-ri.nl` over HTTPS.

See below examples of various use cases.

## Downloading from XNAT into EUCAIM directory structure

Through the use of the `xnat+https://` plugin it is possible to download files from an XNAT instance.
The `eucaimdir://` plugin will store the files in the destination folder in the following nested folder structure:

```
/dest_folder/project_name/subject_label/experiment_label/{scan_id}_{scan_type}/file
```

The path `/dest_folder` needs to be supplied with the starting `/`, so the URL will be `eucaimdir:///dest_folder`.

### A complete project

```python
import datmat

datmat.materialize('xnat+https://xnat.health-ri.nl/projects/sandbox',
                   'eucaimdir:///dest_folder',
                   tempdir='/temp_directory')
```

**Note:** By default only the 'DICOM' resource is downloaded per scan. To download all
resources a query can be added to the input URL:

```python
import datmat

datmat.materialize('xnat+https://xnat.health-ri.nl/projects/sandbox?resources=*',
                   'eucaimresdir:///dest_folder',
                   tempdir='/temp_directory')
```

By using the `eucaimresdir:///` output URL scheme, a folder will be created for
each of the resources, like this:

```
/dest_folder/project_name/subject_label/experiment_label/{scan_id}_{scan_type}/resource_name/files/file
```


### A single subject
```python
import datmat

datmat.materialize('xnat+https://xnat.health-ri.nl/search?projects=sandbox&subjects=TEST01&resources=DICOM',
                   'eucaimdir:///dest_folder',
                   tempdir='/temp_directory')
```

The `datmat` package is based on the IOPlugin system of Fastr. See the documentation for the [XNATStorage IOPlugin](https://fastr.readthedocs.io/en/stable/_autogen/fastr.reference.html#xnatstorage)
for more information on querying XNAT.

# Other use cases
## Copy file to file
```python
import datmat

datmat.materialize('file:///input_file',
                   'file:///dest_file',
                   tempdir='/temp_directory')
```

## Developing your own plugin

You can connect your own data repository or define your own data structure by developing a custom plugin. Each plugin is a subclass of `IOPlugin` and uses a URL scheme (like `file://` or `xnat+https://`) to identify the data source or destination.

### Plugin Architecture Overview

Plugins in `datmat` serve two primary functions:
1. **Source plugins** - Pull data from external sources (e.g., XNAT)
2. **Sink plugins** - Push data to destinations in specific structures (e.g., EUCAIM directory)

Data is passed between plugins using two key data classes:
- `URLSample` - Contains source URLs and metadata
- `PathSample` - Contains file paths and metadata

### Creating a Basic Plugin

To create a custom plugin:

1. Subclass `IOPlugin` and define a unique URL scheme:
```python
class MyPlugin(IOPlugin):
    scheme = 'myplugin'  # URL scheme for your plugin
```

2. Override the necessary methods depending on whether your plugin is a source, sink, or both:

```python
def setup(self):
    """Optional initialization (e.g., connect to repository)"""
    pass
    
def cleanup(self):
    """Optional cleanup (e.g., disconnect from repository)"""
    pass
```

### Creating a Source Plugin

For a plugin that pulls data from a source, implement these methods:

```python
def expand_url(self, urlsample):
    """Convert a single URL entry point into multiple downloadable parts"""
    # Return either a single URLSample or a tuple of (id, URLSample) pairs
    
def fetch_url(self, inurlsample, outpath):
    """Download data based on URLSample to the specified path"""
    # Return a PathSample containing the downloaded data and metadata
```

### Creating a Sink Plugin

For a plugin that stores data in a specific structure, implement these methods:

```python
def put_url(self, sample, outurl):
    """Copy data from temporary location to final destination"""
    # Return True if successful, False otherwise
    
def url_to_path(self, url):
    """Convert plugin URL to filesystem path"""
    # Return the path as a string
```

### Creating a Custom Directory Structure

The easiest way to create a custom directory structure is to subclass `StructuredDirectory` and implement only the `_sample_to_outpath` method:

```python
class MyStructure(StructuredDirectory):
    scheme = 'mystructure'
    
    def _sample_to_outpath(self, url, sample):
        """Define your custom directory structure here"""
        return self.url_to_path(url / sample.project_name / f'{sample.subject_label}')
```

### Available Metadata Properties

The following properties are available in the `PathSample` object (if populated by your source plugin):

- `project_name` - Name of the project
- `subject_label` - Label of the subject
- `experiment_label` - Label of the experiment
- `experiment_date` - Date the experiment was acquired
- `scan_id` - ID of the scan
- `scan_type` - Type of the scan (e.g., T1w)
- `filename` - Filename (can be a partial path for subdirectories)
- `timepoint` - Label of the timepoint the data is from
- `data_path` - Path to the data on disk
