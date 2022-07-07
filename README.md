# Transform files

## Purpose

You must implement a conversion system from CSV format to JSON.


## Task

You must write a program that takes csv files as input and transform it to structured JSON. 

Given the following two sample files: ``items.csv`` and ``groups.csv`` where records in the data file are linked to the groups through the group_id you must generate a structured JSON file.

The resulting JSON It should have the following structure where UPPERCASE refers to the header line in the csv.

```python
{
   “UUID_title”:{
      "string”:”TITLE”
   },

   “UUID_description”:{
      "string”:”DESCRIPTION”,
      "context”:”GROUP”
   }
 }
 ```

Example:

```python
{
   “f19c962e-eec0-455f-baa9-c0ba6986d01b_title”:{
      "string”: ”autem deserunt quo quaerat deleniti”
   },
   “f19c962e-eec0-455f-baa9-c0ba6986d01b_description”:{
      "string”: ”aut soluta repudiandae numquam accusantium pariatur culpa fugiat ducimus laudantium consequatur quam rerum dolorem beatae cum eius magni in architecto nihil similique odit été distinctio eligendi alias optio asperiores incidunt unde quaerat dolor a animi sapiente vel saepe ad iusto doloribus libero voluptates voluptate explicabo velit officiis praesentium accusamus possimus”,
      "context”: ”nesciunt quidem iure”
   }
 }
```

When run as a CLI command it must accept a filename that may be either csv or json and transform from one format to the other.

It will be run similar to the following example:

```# python3 main.py items.csv groups.csv -o output.json```

The CLI should also output a help when called with:

```# python3 main.py -h```


### Notes

The delimiter used is the comma with a pipe as the quoting character for the CSV.

Please note your program will be run using different input files to check the validity.

More info on structured JSON https://docs.transifex.com/formats/json/structured-json

This exercise should not take you more than 3 hours. Please reach out if you have difficulty so we can discuss next steps. Do not spend days trying to craft a solution to impress, this is not the goal.
