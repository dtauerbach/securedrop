# -*- coding: utf-8 -*-

# This file is for utilities that depend on db

import config
import crypto_util
from db import db_session, Source, Submission

RETRY_LIMIT = 10000
NONPENDING_SOURCES_SOFT_LIMIT = max(3000, config.SUPERHEROES_LENGTH)

def create_source_display_name(retry_limit=None):
    """Creates a new unique low entropy display name for a source.

    Args:
      (optional) retry_limit (int): how many tries we make to avoid
      collisions.

    Returns:
      source_name (str): the display name for a source.

    Raises:
      SourceException: if we cannot get a unique display name.
    """
    if not retry_limit: retry_limit = RETRY_LIMIT
    candidate_name = crypto_util.superhero_display_id()
    source_names = [source.filesystem_id 
                    for source in Source.query.filter_by(pending=None)]
    num_tries = 0
    # If there is a name collision with our randomly chosen name, we need
    # to retry.
    print "Source names are %s" % str(source_names)
    while candidate_name in source_names and num_tries < retry_limit:
        num_tries += 1
        if num_tries == RETRY_LIMIT:
            raise crypto_util.SourceException, "Could not generate a code for this source"
        if len(source_names) > NONPENDING_SOURCES_SOFT_LIMIT / 2:
            candidate_name = crypto_util.superhero_with_adjective_display_id()
        else:
            candidate_name = crypto_util.superhero_display_id()
        print "trying candidate name %s..." % candidate_name

    return candidate_name
