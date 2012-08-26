trac-RecentReleasesMacro
========================

Fairly custom plugin that might not be useful for others since it assumes a particular page structure... but might be useful with modification.

Usage:
[[RecentReleases(prefix=server/releases,tag=upcoming)]] 

[[RecentReleases(prefix=server/releases,tag=upcoming,subset=2 1 3)]]

[[RecentReleases(prefix=server/releases,tag=upcoming,subset=2 1 3,limit=3)]]

What does it do?

Similar to the TitleIndex this plugin takes a prefix as the first
argument and iterates through the matching pages looking for ones that
have the specified tag. It then iterates through the pages and grabs
everything up to the first "----". 

There is an assumption being made about the pages being iterated which
is that they each begin with a title (= title =) followed by a table
(using Trac's || syntax) followed by a "----". It then extracts these
three parts and produces a new table with the following form:

||= Release =||= row 1 name =||= row 2 name =|| ... ||= row n name =||
||title||row value 1||row value 2||...||row value n||

There is an optional subset parameter to only the specified rows from
the table in the ingested pages. (i.e. subset=2 4 7) The subset can also
be used to reorder the rows (i.e. subset=2 1 5) Without the subset it
will grab all the rows.

There is another optional parameter limit which limits the number of
releases shown. This is useful for embedding the list in pages where
space is at a premium. And it's also useful to keep your tables from
getting out of hand as the number of releases you have gets large.

What do the ingested pages need to look like?

Sample:
= 1.0 Release =

||Branch||releases/1.0||
||Hash||2804365||

----

Other content goes here

We're managing these by using PageTemplates so all the pages are the
same to start.
