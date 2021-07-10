#!/bin/bash

for entry in "$test"/*
do
  python -m unittest $entry
done
