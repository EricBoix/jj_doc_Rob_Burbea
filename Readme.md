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
docker build -t jejuneness:doc_Rob_Burbea https://github.com/EricBoix/jj_doc_Rob_Burbea.git#:DockerContext
docker run --rm jejuneness:doc_Rob_Burbea --help
```

Extracting the result out of the container requires local filesystem mount

```bash
docker run --rm  -v `pwd`/junk:/output jejuneness:doc_Rob_Burbea --output_directory /output
```

## Running the full data workflow

Fetch [jj_workflow_shell](https://github.com/EricBoix/jj_workflow_shell#fetch-the-workflow-utilities)

```bash
cd `git rev-parse --show-toplevel`         # Implicit from now on
git clone https://github.com/EricBoix/jj_workflow_shell.git
source jj_workflow_shell/init.bash
```

and [configure it](https://github.com/EricBoix/jj_workflow_shell#configure-the-shell-utilities) by editing the resulting `.env` file.

Define your target directories

```bash
set +a                                     # For vscode command runner execution
export RESULTS_DIR=`pwd`/result_data       # Syntactic sugar
export DATABASE_DIR=$RESULTS_DIR/database
\rm -fr $DATABASE_DIR                      # Clean slate from previous run
```

Note: no need for `pdf` conversion since the original data is here in a markdown format.

Prerequisite to Knowledge Graph (KG) extraction: launch a neo4j database

```bash
jj_neo4j_launch_db $RESULTS_DIR $NEO4J_PORT $NEO4J_USERNAME/$NEO4J_PASSWORD
```

Run the (Knowledge Graph) extraction

```bash
jj_extract_knowledge_graph `pwd`/original_data '--load_markdown_document 250_BCE_-_Dhammacakkappavattana_Sutta_Four_Noble_Truths_Wikipedia_translation.md' 
```

Dump the database content for later usage (optional)

```bash
jj_neo4j_dump_database $RESULTS_DIR neo4j.Four-Noble-Truths-Wikipedia-translation.Markdown.dump
```

In order to validate the dump, erase the database and restore it (out of the
previous dump)...

```bash
# WARNING: this DELETEs the existing database
jj_neo4j_restore_database $RESULTS_DIR neo4j.Four-Noble-Truths-Wikipedia-translation.Markdown.dump
```

Extract knowledge graph in [Turtle](https://en.wikipedia.org/wiki/Turtle_(syntax)) format:

```bash
jj_neo4j_launch_db $RESULTS_DIR $NEO4J_PORT $NEO4J_USERNAME/$NEO4J_PASSWORD
jj_dump_knowledge_graph_in_turtle $RESULTS_DIR Four-Noble-Truths-Wikipedia-translation-Markdown.ttl
```

Eventually turn the context off:

```bash
jj_neo4j_stop_db
```

## TODO

Other Rob Burbea talks and transcriptions are available on
[Hermesamara.org website](https://hermesamara.org/resources/audio).
Among them [this webpage focuses on the "Meditation on Emptiness" retreat](https://hermesamara.org/resources/all/retreat/Meditation%20on%20Emptiness%202010)
