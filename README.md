# Mystery Zebra Experimental Code and Corpus
This repository contains the experimental code used for the paper "Lexical Recall or Logical Reasoning: Probing the Limits of Reasoning Abilities in Large Language Models", published at the ACL2025 main conference. The following details, which part of the code belongs to which part of the paper.

[INSERT BIBLIOGRAPHIC INFO ONCE ITS THERE]

## Raw Puzzles
This directory contains the raw puzzles generated with a modified version of the puzzle generator in: https://github.com/quint-t/Puzzle-Generator-and-Solver Puzzles come in 42 sizes (2x1 to 7x7) and in 12 difficulty levels. Not all levels have the same set of sizes available due to restrictions imposed by the difficulty levels.

## Puzzles Natural Language
This directory contains all puzzles of the benchmark in the uniform natural language phrasing. The corpus directory is sourced from here. The files in here are in .txt format.

## Corpus
This directory contains the Mystery Zebra Corpus in .csv format and split into Part 1 and Part 2. This data is also available as a dataset on huggingface: https://huggingface.co/datasets/arg-tech/MysteryZebra

## Code
This directory contains the experimental code for all experiments reported in the paper. In addition, it contains the code used for evaluating the experimental results and for creating the obfuscated versions of the puzzles.

## Prompts
This directory contains the prompts used for Experiment 1 and the Q&A case-study. The files in this directory exemplify how the prompts look like for the different task setups (grid vs. Q&A).

## Model Testing
This directory contains the results from Experiment 1 and Experiment 2 for all models tested in the study.

## Correlation Analysis
This directory contains the results of the correlation analysis conducted for experiment 2.

## Error Analysis
This repository contains the results from the error analysis described in the paper, as well as the key for the error-source code used.
