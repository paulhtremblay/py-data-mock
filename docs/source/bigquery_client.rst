BigQuery Client
================

Imagine we have a function that queries BigQuery, and aggregates 
minutes. If no rows are returned, the result should be 0. Otherwise, return
the sum divided by a (60 * 24) to get days.

The example code is below. 

To test the code without actually connecting to BQ, mock the call. 
Create a class and subclass `data_mock.gcp.client`. In the first class,
the value of minutes is set to 6686876 by a tuple. This casues the call 
to BQ mock a value of one row with the value of 6686876. 

In the second case, we set no values at all. This results in now iteration,
as if BigQuery found no data, the desired test.

.. literalinclude:: ../../examples/bq_with_class.py

