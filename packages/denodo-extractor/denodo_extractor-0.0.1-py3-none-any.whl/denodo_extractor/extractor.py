from connector import connector
import pandas as pd
import math
from tqdm import tqdm


class extractor:
    HEADER = ['column_name', 'view_identifier', 'dependency_database_name', 'dependency_name',
              'dependency_column_name', 'dependency_identifier', 'expression', 'depth']

    def __init__(self, server_name, port, database, user_id, pwd):
        self.connector = connector(server_name, port, database, user_id, pwd)

    def get_fields(self, database, view):
        fields = []
        data_types = []
        # Query to be sent to the Denodo VDP Server
        query_field = f"SELECT column_name, column_vdp_type FROM GET_VIEW_COLUMNS() WHERE input_database_name = %s and input_view_name = %s"

        # Send the query to the server
        self.connector.cursor.execute(query_field, (database, view))

        # obtain all results from response
        results = self.connector.cursor.fetchall()

        # Save the field name and data type
        for i in results:
            fields.append(i[0])
            data_types.append(i[1])

        return fields, data_types

    def get_meta_data(self, database, view):
        """Obtain column dependency meta data for each field in the view. 
        The meta data is stored in a dictionary with the field name as key and the meta data as value.
        """
        fields, data_types = self.get_fields(database, view)
        meta_data = {}

        for f in tqdm(fields, desc="Loading meta data...", ncols=100):
            query_meta = "SELECT " + \
                ','.join(self.HEADER) + \
                f" FROM column_dependencies(%s, %s, %s)"
            self.connector.cursor.execute(query_meta, (database, view, f))
            results = self.connector.cursor.fetchall()
            meta_data[f] = pd.DataFrame(results, columns=self.HEADER)
        return fields, meta_data

    def get_transformations(self, database, view):
        fields, meta_data = self.get_meta_data(database, view)
        transformations = {}
        for field in tqdm(fields, desc="Loading transformations...", ncols=100):
            meta_data_field = meta_data[field]
            meta_data_field.sort_values(
                "dependency_identifier", inplace=True)
            table = meta_data_field[meta_data_field["depth"] == 1]
            start_id = meta_data_field.iloc[0]["view_identifier"]
            transformations[field] = self.parse_meta_data(table, start_id)

        return transformations

    def remove_nans(self, values):
        """Filter out NaN or None values from a list

        Args:
            values (list): list to filter

        Returns:
            list: filtered list
        """
        filtered_values = []
        for value in values:
            if type(value) == str:
                filtered_values.append(value)
            elif value is None or math.isnan(value):
                continue

        return filtered_values

    def parse_meta_data(self, table, start_id):
        # Stack data structure to traverse view identifiers in depth first manner
        stack = []
        stack.append(start_id)

        # SELECT and FROM statement
        transformations_string = ""

        # Depth first traversal
        while len(stack) > 0:
            id = stack.pop()
            unique_ids = table["view_identifier"].unique()

            if id in unique_ids:
                # Modularize values in separate variables for better readability
                rows_filtered_id = table[table["view_identifier"] == id]
                column_names = rows_filtered_id["column_name"].values[0]
                expression = rows_filtered_id["expression"].values
                kids = rows_filtered_id["dependency_identifier"].tolist()
                dependency_name = rows_filtered_id["dependency_name"].values
                dependency_column_name = rows_filtered_id["dependency_column_name"].values
                new_db = rows_filtered_id["dependency_database_name"].values

                # Remove <NULL> in table output
                expression = self.remove_nans(expression)
                dependency_name = self.remove_nans(dependency_name)
                new_db = self.remove_nans(new_db)

                # when you have no new column, you know you are at a leave of the tree, and hence you can continue traversing other parts of the data lineage tree
                if type(rows_filtered_id["dependency_column_name"].values[0]) != str or len(dependency_name) == 0 or dependency_name[0] == None:
                    continue

                new_col = rows_filtered_id["dependency_column_name"].values[0].split(
                    ',')

                # Account for empty expression (i.e. no transformation)
                column_name = ""
                if len(column_names.split(',')) > 1:
                    column_name = column_names.split(',')[1]
                else:
                    column_name = column_names.split(',')[0]

                expression_str = ""
                if len(expression) > 0:
                    expression_str = '"' + column_name + \
                        '"' + " = " + expression[0]
                else:
                    expression_str = '"' + column_name + '"' + " = " + '"' + \
                        dependency_name[0] + '"."' + \
                        dependency_column_name[0] + '"'

                transformations_string += expression_str + "\n"

                # In case of multiple variables used for creation of start_col, requery the tables for
                # these variables and append them to the original table. Also add the identifiers to the stack
                # to parse them later.
                if len(new_col) > 1:
                    for col in new_col:
                        self.connector.cursor.execute(
                            "SELECT " + ','.join(self.HEADER) + f" FROM column_dependencies(%s, %s, %s)", (new_db[0], dependency_name[0], col))
                        table_suppelement = pd.DataFrame(
                            self.connector.cursor.fetchall(), columns=self.HEADER)
                        max_id = max(table["dependency_identifier"].unique())
                        table_suppelement["dependency_identifier"] += max_id
                        table_suppelement["view_identifier"] += max_id
                        table_suppelement = table_suppelement[table_suppelement["depth"] == 1]
                        table_suppelement.sort_values(
                            "dependency_identifier", inplace=True)
                        stack.append(
                            int(table_suppelement.iloc[0]["view_identifier"]))
                        table = pd.concat(
                            [table, table_suppelement], ignore_index=True)
                else:
                    if len(kids) == 1:
                        stack.append(kids[0])  # 1:1 mapping
                    else:
                        for index, kid in rows_filtered_id.iterrows():
                            transformations_string += self.parse_meta_data(
                                table, kid["dependency_identifier"])

        return transformations_string

