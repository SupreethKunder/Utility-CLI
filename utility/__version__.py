VERSION = (0, 1, 0)
PRERELEASE = None  # alpha, beta or rc
REVISION = None


def generate_version(version, prerelease=None, revision=None):
    version_parts = [".".join(map(str, version))]
    if prerelease is not None:
        version_parts.append("-{}".format(prerelease))
    if revision is not None:
        version_parts.append(".{}".format(revision))
    return "".join(version_parts)


__title__ = "utility"
__description__ = "Utility Functions for Automation"
__url__ = "https://github.com/SupreethKunder/Utility-CLI.git"
__version__ = generate_version(VERSION, prerelease=PRERELEASE, revision=REVISION)
__author__ = "utility"
__author_email__ = "kundersupreeth@gmail.com"
__license__ = "MIT"
