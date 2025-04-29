# pylint: disable=W0622
"""cubicweb-s3storage application packaging information"""


modname = "cubicweb_s3storage"
distname = "cubicweb-s3storage"

numversion = (4, 0, 2)
version = ".".join(str(num) for num in numversion)

license = "LGPL"
author = "LOGILAB S.A. (Paris, FRANCE)"
author_email = "contact@logilab.fr"
description = "A Cubicweb Storage that stores the data on S3"
web = f"https://forge.extranet.logilab.fr/cubicweb/cubes/{distname}"

__depends__ = {
    "cubicweb": ">= 4.0.0, < 5.0.0",
    "boto3": "< 1.36.0",
}
__recommends__ = {}

classifiers = [
    "Environment :: Web Environment",
    "Framework :: CubicWeb",
    "Programming Language :: Python",
    "Programming Language :: JavaScript",
]
