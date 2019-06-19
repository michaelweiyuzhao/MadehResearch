# SQL Auto Query - Used with MSSQL on Road Maintenance Data
Michael Zhao University of Toronto
Last updated: May, 2017

This utility script is set up for a query of a specific format and can be adapted later to work for more queries.


## Program Description

This program was originally written to run a few queries that were exactly the same save a few word replacements, however depending on how the settings files are defined, it can run any query the user specifies. Prewritten queries can be placed into queries.txt with certain keywords specified by the user to be replaced between every iteration and the replacement values can be specified in keyword\_replacements.txt. The number of iterations is specified by the number of times the keywords repeat in keyword\_replacements.txt.


## File Descriptions (files can be found in program directory)

- auto\_query.py: Python script file to automate repeated, similar queries. Run with settings.txt, queries.txt and keyword\_replacements.txt in the same directory

- config.txt: Settings file that defines certain options such as connection details for the database being queried and other options such as custom set up flags.

- queries.txt: Settings file that auto\_query.py pulls queries from. These are the queries the program runs. This file is in a csv format where each line run consecutively. The delimiter for this file is '|'. Keywords in the format {KEYWORD} can be defined in this file and are replaced with words defined in keyword\_replacements.txt to allow for adjustability between queries. The user can write their own queries in this format and the program will run it according to the values in keyword\_replacements.txt.

- keyword\_replacements.txt: Settings file that holds replacement {KEYWORD} values for queries.txt. Information in this file is represented as key-value pairs, the key being the {KEYWORD} and the value being the value to replace {KEYWORD} with. {KEYWORDS} and values can be user defined by changing this file. The delimiter for this file is ','.


## Examples

- example queries.txt file:
select * from dbo.PCI{YEAR1}{POSTFIX1} where ...
select * from dbo.PCI{YEAR2}...

- example keyword\_replacements.txt file:
{YEAR1},1999
{YEAR2},2001
{POSTFIX1},all\_T
...
{YEAR1},2000
{YEAR2},2002
...

- program will replace all instances of {KEYWORD} in queries.txt with its value from keyword\_replacements.txt during runtime:
select * from dbo.PCI1999all\_T where ...
select * from dbo.PCI2001...
...
select * from dbo.PCI2000all\_T where ...
select * from dbo.PCI2002...

## Change Log

May 9, 2017:
- First implementation of program done. Runs perfectly for original intended use.
- Settings files implemented to allow for more customization.
- Bugs:
	- pyodbc doesn't handle long queries very well. The query will execute but pyodbc will not be able to get the output unless it's structured in a certain way. Need to do more research into T-SQL to be able to figure this out.
	- does not yet write to excel sheets in output
