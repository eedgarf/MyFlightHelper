## Synopsis
Flight Helper is a python3 command line utility to find the cheapest flight routes by parsing momondo.co.uk flight aggregator
results from the script.
## Motivation
Momondo, and many if not all other flight aggregators have a tendency to show somewhat skewed flight prices in their "Month"
view. This tool bypases that by pulling flight prices for a given day and destination explicitly. That is, we have an fully
automatized way of pulling the real flight price for a given day and destination.
## Installation
Pull the project.
Install python3 on your system. Plese consult python manual in regards to your operating system.
Intall selenium. `pip install selenium`
Install phantomjs. Consult your operating system manual. For Mac OS X have homebrew installed & `brew install phantomjs`
