# Extracting (some) Knowledge Graph out of Rob Burbea's teachings<!-- omit from toc -->

## Table of contents<!-- omit from toc -->

- [Introduction](#introduction)
- [Running the converter](#running-the-converter)
- [Running the PDF conversion with docker](#running-the-pdf-conversion-with-docker)
- [Running the full data workflow](#running-the-full-data-workflow)
- [TODO](#todo)

## Introduction

This repository holds some teachings, mostly talks given during retreats, given by [Rob Burbea](https://hermesamara.org/rob-burbea).

### Concerning the Meditation on Emptiness retreat content (copyrights)

The original recordings of the "Meditation on Emptiness" (27 days) retreat, that was held in  2010 at [Gaia House](https://gaiahouse.co.uk/) are available at [Dharamseed.org](https://dharmaseed.org/retreats/1044/) with a [Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License (CC BY-NC-ND 4.0)](https://creativecommons.org/licenses/by-nc-nd/4.0/).

The markdown transcriptions were extracted out of [the Hermes Amāra Foundation webpages focusing on the "Meditation on Emptiness" retreat](https://hermesamara.org/resources/all/retreat/Meditation%20on%20Emptiness%202010), that redistributes the original talk but also provides their transcriptions.

## Running the converter

```bash
cd `git rev-parse --show-toplevel`/Convert
python3.10 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Running the PDF conversion with docker

```bash
docker build -t jejuneness:doc_Rob_Burbea https://github.com/EricBoix/jejune_doc_Rob_Burbea.git#:DockerContext
docker run --rm jejuneness:doc_Rob_Burbea --help
```

Extracting the result out of the container requires local filesystem mount

```bash
docker run --rm  -v `pwd`/junk:/output jejuneness:doc_Rob_Burbea --output_directory /output
```

## Running the full data workflow

Install and configure [`jejune_cli`](https://github.com/EricBoix/jejune_cli), then run `jejune doctor` to verify the configuration. This boils down to

```bash
uv tool install git+https://github.com/EricBoix/jejune_cli
jejune configuration init     
# Proceed with the configuration of the files located in .jejune/ dir
echo "CONVERT_DOC_DIR=." >> .jejune/env-config
jejune doctor
```

Define a convenience variable for the results directory:

```bash
export RESULTS_DIR=`pwd`/result_data
```

Run the converter to sanitize original document:

```bash
jejune convert run --output-dir $RESULTS_DIR
```

Run the (Knowledge Graph) extraction (launching a clean slate neo4j database is a prerequisite)

```bash
jejune neo4j delete $RESULTS_DIR
jejune neo4j stats --assert 0/0
jejune graph extract $RESULTS_DIR \
  --load_markdown_document \
  2010_01_20_-_Rob_Burbea_-_Meditation_on_emptiness_Retreat_-_Opening_talk_Orienting_and_relating_to_the_emptiness_retreat_-_local_converter.md \
  --load_json_document \
  2010_01_20_-_Rob_Burbea_-_Meditation_on_emptiness_Retreat_-_Opening_talk_Orienting_and_relating_to_the_emptiness_retreat_-_Sentences_as_LangChain_Document.json
jejune neo4j stats --assert 537/871
```

Dump the database content for later usage (optional)

```bash
jejune neo4j stop
jejune neo4j dump $RESULTS_DIR \
  neo4j.Rob-Burbea-Meditation-On-Emptiness-Opening-talk.MarkdownAndSentences.dump
```

Extract knowledge graph in [Turtle](https://en.wikipedia.org/wiki/Turtle_(syntax)) format (initial restoration validates the previous dump):

```bash
# WARNING: restoring DELETEs the existing database
jejune neo4j restore $RESULTS_DIR \
  neo4j.Rob-Burbea-Meditation-On-Emptiness-Opening-talk.MarkdownAndSentences.dump
jejune neo4j start $RESULTS_DIR
jejune neo4j stats --assert 537/871.  # Just making sure
jejune neo4j dump-turtle $RESULTS_DIR \
  Rob-Burbea-Meditation-On-Emptiness-Opening-talk.MarkdownAndSentences.ttl
jejune neo4j stop
```

## TODO

Other Rob Burbea talks and transcriptions are available on
[Hermesamara.org website](https://hermesamara.org/resources/audio).
Among them [this webpage focuses on the "Meditation on Emptiness" retreat](https://hermesamara.org/resources/all/retreat/Meditation%20on%20Emptiness%202010)
