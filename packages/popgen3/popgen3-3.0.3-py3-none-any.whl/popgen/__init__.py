from .project import popgen_run

__version__ = '3.0.3'

def run(config_path):
    """Run PopGen from Python."""
    popgen_run(config_path)


