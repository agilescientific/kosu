"""
Author: Agile Scientific
Licence: Apache 2.0
"""
import pathlib
import shutil
import zipfile
import os
import warnings
from urllib.request import urlretrieve
import inspect
import sys
import glob
import click

import requests
import click
import yaml
from jinja2 import Environment, FileSystemLoader

try:
    import boto3
    from botocore.exceptions import ClientError
    AWS_AVAILABLE = True
except:
    AWS_AVAILABLE = False

from .customize import process_notebook

env = Environment(loader=FileSystemLoader('templates'))

def get_script_dir(follow_symlinks=True):
    if getattr(sys, 'frozen', False):
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return pathlib.Path(os.path.dirname(path))


# Read the YAML control file, if present.
KOSU = {'path': get_script_dir()}
kosu = pathlib.Path(".kosu.yaml")
if kosu.is_file():
    with open(kosu, 'rt') as f:
        try:
            KOSU.update(yaml.safe_load(f))
        except yaml.YAMLError as e:
            print(e)

@click.group(context_settings=dict(help_option_names=['--help', '-h']))
def cli():
    pass


@cli.command()
@click.option('--yes', default=False, is_flag=True, help="Automatically confirm.")
def init(yes):
    """
    Initialize a course or group of courses.
    """
    message = "This will create a new course collection in the current directory. Are you sure?"
    if yes or click.confirm(message, default=False, abort=True):
        # Make folders for content.
        folders = ['prod', 'images', 'references', 'scripts', 'templates']
        for folder in folders:
            _ = pathlib.Path(folder).mkdir(exist_ok=True)

        # Make a sample course and other files.
        target = pathlib.Path('.').resolve()
        shutil.copyfile(KOSU['path'] / 'include' / 'example_course.yaml', target / 'example_course.yaml')
        shutil.copyfile(KOSU['path'] / 'include' / '.kosu.yaml', target / '.kosu.yaml')
        shutil.copyfile(KOSU['path'] / 'include' / 'environment.yaml', target / 'environment.yaml')
        shutil.copyfile(KOSU['path'] / 'include' / 'useful.pdf', target / 'references'/ 'useful.pdf')
        shutil.copyfile(KOSU['path'] / 'include' / 'README.md', target / 'templates' / 'README.md')
        shutil.copyfile(KOSU['path'] / 'include' / 'Interesting_notebook.ipynb', target / 'prod' / 'Interesting_notebook.ipynb')
        shutil.copyfile(KOSU['path'] / 'include' / 'Intro_to_Matplotlib.ipynb', target / 'prod' / 'Intro_to_Matplotlib.ipynb')
        shutil.copyfile(KOSU['path'] / 'include' / 'Intro_to_NumPy.ipynb', target / 'prod' / 'Intro_to_NumPy.ipynb')
        shutil.copyfile(KOSU['path'] / 'include' / 'Intro_to_Python.ipynb', target / 'prod' / 'Intro_to_Python.ipynb')
        shutil.copyfile(KOSU['path'] / 'include' / 'agile_logo.png', target / 'images' / 'agile_logo.png')
        shutil.copyfile(KOSU['path'] / 'include' / 'example.py', target / 'scripts' / 'example.py')
        click.secho("Created example course and config files.\n", fg="green", bold=True)
        click.secho("See .kosu.yaml for configuration options.", fg="cyan")

    return


@cli.command()
@click.argument('course', type=str, required=False)
@click.option('--all', is_flag=True, help="Cleans all courses listed in control file.")
def clean(course, all):
    """
    Clean COURSE builds from local storage.
    """
    courses = get_courses(course, all)

    for i, course in enumerate(courses):
        click.secho(f"Cleaning {course} ({i+1} of {len(courses)}).", fg="cyan")
        try:
            shutil.rmtree(pathlib.Path('build').joinpath(course))
        except FileNotFoundError:
            pass
        try:
            pathlib.Path(f'{course}.zip').unlink()
        except FileNotFoundError:
            pass
        try:
            if not any(pathlib.Path('build').iterdir()):
                click.secho(f"Removing build directory.", fg="red")
                shutil.rmtree(pathlib.Path('build'))
                break
        except:
            pass
    click.secho(f"Finished.\n", fg="green")

    return


@cli.command()
@click.argument('course', type=str, required=False)
@click.option('--all', is_flag=True, help="Publishes all courses listed in control file.")
def publish(course, all):
    """
    Publish COURSE to AWS.
    """
    courses = get_courses(course, all)

    for i, course in enumerate(courses):
        click.secho(f"Publishing {course} ({i+1}/{len(courses)}). Ctrl-C to abort.", fg="cyan")
        _ = build_course(course, clean=True, zip=True, upload=True, clobber=True)
    click.secho(f"Finished.\n", fg="green")

    return


@cli.command()
@click.argument('course', type=str, required=False)
@click.option('--all', is_flag=True, help="Tests all courses listed in control file.")
@click.option('--environment', is_flag=True, help="Build a global environment file for testing.")
def test(course, all, environment):
    """
    Test that COURSE builds without error.
    """
    courses = get_courses(course, all)

    envs = []
    for i, course in enumerate(courses):
        clean = 1 - environment  # Clean if we're not doing env.
        click.secho(f"Testing {course} ({i+1}/{len(courses)}). Ctrl-C to abort.", fg="cyan")
        env = build_course(course, clean=clean, zip=False, upload=False, clobber=True)
        envs.append(env)
    click.secho(f"Finished.\n", fg="green")

    if environment:
        # Build the combined environment.
        channels, conda, pip = set(), set(), set()
        for env in envs:
            channels.update(env['channels'])
            conda.update(env['dependencies'][:-1])  # All except pip.
            pip.update(env['dependencies'][-1]['pip'])
        env = {
            'name': 'kosu-all',
            'channels': list(channels),
            'dependencies': list(conda) + [{'pip': list(pip)}],
        }
        with open('environment-all.yml', 'w') as f:
            f.write(yaml.dump(env, default_flow_style=False, sort_keys=False))
        click.secho(f"Global environment file written.\n", fg="green")

    return


@cli.command()
@click.argument('course', type=str, required=False)
@click.option('--clean/--no-clean', default=True, help="Delete the build dir? Default: clean.")
@click.option('--zip/--no-zip', default=True, help="Make the zip file? Default: zip.")
@click.option('--upload/--no-upload', default=False, help="Upload the ZIP to S3? Default: no-upload.")
@click.option('--clobber/--no-clobber', default=False, help="Clobber existing files? Default: no-clobber.")
@click.option('--all', is_flag=True, help="Tests all courses listed in control file.")
def build(course, clean, zip, upload, clobber, all):
    """
    Build COURSE with various options.
    """
    courses = get_courses(course, all)

    for i, course in enumerate(courses):
        click.secho(f"Building {course} ({i+1}/{len(courses)}). Ctrl-C to abort.", fg="cyan")
        _ = build_course(course, clean, zip, upload, clobber)
    click.secho(f"Finished.\n", fg="green")

    return

# =============================================================================
def get_courses(course, all):
    """
    Returns the list of courses to process.
    """
    if (not all) and (course is None):
        message = "Missing argument 'COURSE', or use '--all'."
        raise click.UsageError(message)
    elif all and (course is not None):
        message = "'--all' cannot be used with 'COURSE'; use one or the other."
        raise click.BadOptionUsage('--all', message)
    elif all and (course is None):
        excl = ['environment.yaml']
        all_courses = [c.removesuffix('.yaml') for c in glob.glob("*.yaml") if c not in excl]
        courses = KOSU.get('all', all_courses)
    else:
        courses = [course.removesuffix('.yaml')]

    return courses


def build_course(course, clean, zip, upload, clobber):
    """
    Compiles the required files into a course repo, which
    will be zipped by default.

    Args:
        course (str): The course to build.
        clean (bool): Whether to remove the build files.
        zip (bool): Whether to create the zip file for the course repo (or to save it if uploading).
        upload (bool): Whether to attempt to upload the ZIP to AWS.
        clobber (bool): Whether to overwrite existing ZIP file and build directory.

    Returns:
        dict. Environment dictionary.
    """
    # Read the YAML control file.
    with open(f"{course.removesuffix('.yaml')}.yaml", 'rt') as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(e)
    config['course'] = course

    # Make a path to store everything.
    build_path = 'build'
    path = pathlib.Path(build_path).joinpath(course)
    if path.exists():
        message = "The target directory exists and will be overwritten. Are you sure?"
        if clobber or click.confirm(message, default=True, abort=True):
            shutil.rmtree(path)
    if pathlib.Path(f"{course}.zip").exists():
        message = "The ZIP file exists and will be overwritten. Are you sure?"
        if clobber or click.confirm(message, default=True, abort=True):
            pathlib.Path(f"{course}.zip").unlink()

    _ = path.mkdir(parents=True, exist_ok=True)

    # Build the notebooks; also deals with images.
    *paths, _, data_urls_to_check = build_notebooks(path, config)

    # Check the data files exist.
    click.secho('Checking and downloading data ', fg="cyan", nl=False)
    for url in data_urls_to_check:
        click.secho('.', fg="cyan", nl=False)
        if requests.head(url).status_code != 200:
            raise Exception(f"Missing data URL: {url}")

    # Make the data directory.
    build_data(path, config)
    click.secho()

    # Deal with scripts.
    if scripts := config.get('scripts'):
        for script in scripts:
            for p in paths:
                shutil.copyfile(pathlib.Path('scripts') / script, p / script)

    # Make the references folder.
    if refs := config.get('references'):
        ref_path = path.joinpath('references')
        ref_path.mkdir()
        for fname in refs:
            shutil.copyfile(pathlib.Path('references') / fname, ref_path / fname)

    # Make the environment.yaml file.
    env = build_environment(path, config)

    # Make the README.
    _ = build_readme(path, config)

    # Zip it.
    if zip or upload:
        zipped = shutil.make_archive(course, 'zip', root_dir=build_path, base_dir=course)
        click.secho(f"Created {zipped}", fg="green")

    # Upload to AWS.
    if upload:
        success = upload_zip(zipped)
        if success:
            click.secho(f"Uploaded {zipped}", fg="green")
            link  = f"https://{KOSU['s3-bucket']}.s3.amazonaws.com/"
            link += f"{course}.zip"
            click.secho(f"File link: {link}", fg="green")
        if not zip:
            pathlib.Path(f'{course}.zip').unlink()

    # Remove build.
    if clean:
        shutil.rmtree(path)
        click.secho(f"Removed build files.", fg="red")

    return env


def build_notebooks(path, config):
    """
    Process the notebook files. We'll look at three sections of the
    config: curriculum (which contains non-notebook items too),
    extras (which are listed in the README), and demos (which are not).
    """
    # Make the various directories.
    m_path = path.joinpath('master')
    m_path.mkdir()
    nb_path = path.joinpath('notebooks')
    nb_path.mkdir()
    if config.get('demos'):
        demo_path = path.joinpath('demos')
        demo_path.mkdir()
    else:
        demo_path = None

    all_items = [f for items in config['curriculum'].values() for f in items]
    notebooks = list(filter(lambda item: '.ipynb' in item, all_items))
    notebooks += config.get('extras', list())
    images_to_copy = []
    data_urls_to_check = []
    click.secho('Processing notebooks ',fg="cyan" , nl=False)
    for notebook in notebooks:
        infile = pathlib.Path('prod') / notebook
        outfile = nb_path / notebook
        images, data_urls = process_notebook(infile, outfile)
        images_to_copy.extend(images)
        data_urls_to_check.extend(data_urls)
        shutil.copyfile(infile, m_path / notebook)
        # Clear the outputs in the master file.
        _ = os.system("nbstripout {}".format(m_path / notebook))
        click.secho('+', fg="cyan", nl=False)
    notebooks = config.get('demos', list())
    for notebook in notebooks:
        infile = pathlib.Path('prod') / notebook
        outfile = demo_path / notebook
        images, data_urls = process_notebook(infile, outfile, demo=True)
        images_to_copy.extend(images)
        data_urls_to_check.extend(data_urls)
        shutil.copyfile(infile, m_path / notebook)
        # Clear the outputs in the master file.
        _ = os.system("nbstripout {}".format(m_path / notebook))
        click.secho('+', fg="cyan", nl=False)
    click.secho()
    if images_to_copy:
        img_path = path.joinpath('images')
        img_path.mkdir()
        for image in images_to_copy:
            shutil.copyfile(pathlib.Path('images') / image, img_path / image)

    return m_path, nb_path, demo_path, data_urls_to_check


def build_environment(path, config):
    """Construct the environment.yaml file for this course."""
    # Get the base environment.
    with open(f'environment.yaml', 'r') as f:
        try:
            deps = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(e)

    # Now add the course-specific stuff from the config.
    name = config.get('environment', config['course']).lower()
    conda = {'name': name}
    conda.update(deps)
    if isinstance(conda['dependencies'][-1], dict):
        pip = conda['dependencies'].pop()
    if p := config.get('pip'):
        pip['pip'].extend(p)
    if c := config.get('conda'):
        conda['dependencies'].extend(c)
    conda['dependencies'].append(pip)

    # Write the new environment file to the course directory.
    # Despite YAML recommended practice, we need to use .yml for conda.
    with open(path / 'environment.yml', 'w') as f:
        f.write(yaml.dump(conda, default_flow_style=False, sort_keys=False))
    return conda


def build_readme(path, config):
    """Build the README.md using Jinja2 templates. Note that there
    is a reasonable amount of magic happening at the template level,
    especially text formatting. So if you're looking to change
    something in the README.md, it's probably in there somewhere.
    """
    content = dict(env=config['course'],
                   title=config['title'],
                   curriculum=config.get('curriculum'),
                   extras=config.get('extras'),
                  )
    template = env.get_template('README.md')
    with open(path / 'README.md', 'w') as f:
        f.write(template.render(**content))
    return


def build_data(path, config):
    """Build the data directory. Files must exist in the given path
    of the bucket of AWS S3, per the control file.
    """
    data_path = path.joinpath('data')
    data_path.mkdir()

    s3path = KOSU.get('s3-path', '')
    s3bucket = KOSU.get('s3-bucket')
    data_url = config.get('data_url')
    if data_url is None:
        if s3bucket is None:
            raise TypeError("No data_url or s3-bucket specified.")
        data_url = f"https://{s3bucket}.s3.amazonaws.com/{s3path}{'/' if s3path else ''}"

    if datasets := config.get('data'):
        for fname in datasets:
            click.secho('+',fg="cyan", nl=False)
            fpath = data_path / fname
            if not fpath.exists():
                url = f"{data_url}{fname}"
                print(url)
                urlretrieve(url, fpath)
            if fpath.suffix == '.zip':
                # Inflate and delete the zip.
                with zipfile.ZipFile(fpath, 'r') as z:
                    z.extractall(data_path)
                fpath.unlink()
    else:
        data_path.joinpath('folder_should_be_empty.txt').touch()
    return


def upload_zip(file_name, bucket=None, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    if not AWS_AVAILABLE:
        m = "AWS upload is not available. You need to install boto3 and botocore, "
        m += "and set up AWS credentials."
        raise Exception(m)

    if bucket is None:
        bucket = KOSU['s3-bucket']

    # If S3 object_name was not specified, use file_name.
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file.
    s3_client = boto3.client('s3')
    try:
        args = {'ACL':'public-read'}
        _ = s3_client.upload_file(file_name, bucket, object_name, ExtraArgs=args)
    except ClientError as e:
        warnings.warn("Upload to S3 failed:", e)
        return False
    return True
