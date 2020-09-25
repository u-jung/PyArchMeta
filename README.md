# PyArchMeta

This is work in progress

The main objective is to create a python package which will aid to fetch archival meta data from various repositories, to process and to store them. 
One focus is to provide a the handling of more than one language within on record while still using the ISAD (G) - International Standard Archival Description (General).

## What's working by now ? ##

The package reads EAD3 xml files and give them out as csv. The parent child relationship will be represented via a parent_id column. An example of how it works is shown in the test file. 
