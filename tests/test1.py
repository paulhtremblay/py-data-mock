import unittest
import google

from google.cloud import bigquery

def get_sql():
        return """
            /*
            py-bigquery-mock-register: bikeshare-name-status-address

            */
        SELECT
      name, status, address
    FROM
      `bigquery-public-data.austin_bikeshare.bikeshare_stations`
      order by name, status, address
    LIMIT
      2
        """

class TestResults(unittest.TestCase):

    def test_items_first_result_returns_3_correct_name_values(self):
        client = bigquery.Client(project= 'some-project')
        sql = get_sql() 
        row_iter = client.query(sql).result()
        self.assertEqual(row_iter.total_rows, 2)
        final = []
        for i in row_iter:
            temp = []
            for j in i.items():
                self.assertTrue(isinstance(j, tuple))
                temp.append(j)
            final.append(temp)

        needed = [[('name', '10th & Red River'), ('status', 'active'), ('address', '699 East 10th Street')], [('name', '11th & Salina'), ('status', 'active'), ('address', '1705 E 11th St')]]
        self.assertEqual(final, needed)

if __name__ == '__main__':
    unittest.main()
