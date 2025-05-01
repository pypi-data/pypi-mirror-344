The Cantus Library
==================

This is a design document for the Cantus Python library, proposed during
the DACT Chant Analytics team meeting during Workshop 18 on April 6 2024
in Halifax, CA. (Kate Helsen, Tim Eipert, Jan Hajič and Jennifer Bain were there.)

The Cantus library is envisioned as a Python API to the Cantus family of databases
that makes it easy to use this data for computational processing. Primarily we intend
this to be used for research in digital chant scholarship, but of course it can
be used to build chant-centric apps, new websites, extract data for comparative
studies across different repertoires, study liturgy, etc.

This document lays out the specification for the library, the reasoning behind
the specification, and policies for how the library should develop further.
It should be a result of discussion, primarily within the Chant Analytics team,
but we will seek input from the broader DACT community as well.

We work downstream of Cantus DB and Cantus Index policies.
That means we are not getting into discussions about e.g. how vernacular
Cantus IDs are assigned. We take what is catalogued in the databases
and run with that. (That doesn't mean the concerns of chant analytics
cannot be a part of the upstream discussions, but those are separate
discussions.)


Data model
----------

At the heart of the library is the Cantus Database and Cantus Index data model.
The two elementary objects in this model are a `Chant`, and a `Source`. 

A `Source` is a physical manuscript or print that contains Gregorian chant.
Primarily, this will be a liturgical book such as an antiphonary, gradual,
or other sources. Fragments are, in principle, also sources.
(Note: tonaries may get special handling.)

A `Chant` is one instance of a chant in a source. Typically it has a text,
a melody (which is not necessarily transcribed), and a Cantus ID assigned,
and it should link to a source in which it is found.

...What else?


Data formats
------------

CantusCorpus-style CSV

For sources...?

Feast, office and genre IDs like CantusCorpus, or use raw field values?


Downloading the Cantus network data
-----------------------------------

Django pipeline: we need Cantus DB and other django-fied databases
to just give us a database dump (django's manage.py script supports that).

Drupal/backup Drupal databases: we have a front-end scraping set based on BeautifulSoup.

Sources: again: scraping based on BeautifulSoup with scrapers for a subset of the databases
implemented.


Disseminating the data
----------------------

We run a release of the entire Cantus database network at least once a year.

We provide the following output sets, in ascending degree of curation:

- Raw data dump with everything
- Major Mass and Office genres
- ...? Other levels such as discarding fragments, discarding too unusual Cantus IDs, etc.
  We have to talk to others about options.
- High-quality catalogued sources only (complete, sufficiently large,
  with Cantus DB experts signing off on the quality)

Each of these datasets has its own well-defined preprocesing pipeline that
anyone can run themselves.

For each dataset, we also compute some elementary statistics:

- No. of chants, no. of chants with full melodies
- No. of sources, no. of sources with full provenance data and geocoding,
  sources with at least X chants (or: list of sources ordered by no. of chants), etc.
- Breakdown by component database, growth reports
- Mode stats, differentia stats

We shouldn't, however, go overboard. The idea is to provide some basics,
not to pre-compute anything that "people" might be interested in knowing.
(ChantLab can then finally have a reasonable dashboard to implement.)


Discussion points:

- Doing these releases makes it really convenient for other computer science-y people
  to work with our data. This means: citations! Street cred! Building out the field!
- By doing different "levels of quality", we make it easy for people to jsut go for
  the high-quality one and therefore not come up with silly things and/or bullshit.
- It's fully customizable for anyone who wants to get into it, but by providing
  reasonable defaults, we make it easy for people to not have to get into it.


Preprocessing and data cleaning
-------------------------------

Dataset: implements everything that we need to make the releases described above.

Most difficult part: "Trusted" status. Should be derived from something upstream
that the actual musicologists mark in the database.

Melody preprocessing.
Differentia cleaning, completeness checks, syllabyfication checks (optional).
Transposition warnings?


Analytics
---------

In general, we do not implement a method just because we can.
Each analytical method should have a paper, or at least a preprint,
that acts as the method's documentation.
Kind of like scikit-learn.

What do we try to do w.r.t. Cantus Analysis Tool?