## logstash2CSV

This is a Python client for exporting CSV files from logstash formatted data.

You cannot download any CSV Data from Kibana 3, so this library will be helpful for gathering data in CSV format.

### Version

0.1

### Requirements

* python 2.7+
* pip

### Dependencies

* elasticsearch
* pytest

### Features

* Supports configuration from Raw JSON or file
* Supports Setting the time range of search
* Simply select output fields and generate CSV files


## Example

    from logstash2csv import Logstash2CSV

    ls2csv = Logstash2CSV()

    # Configuration of connection
    ls2csv.set_connection(
        {
            "host": "log.example.org",
            "port": 443,
            "basic_auth: {
                "user": "user",
                "password": "password",
            },
            "use_ssl": True
        }
    )

    # Set a search query
    ls2csv.set_query({"query": "elasticsearch query"})

    # Set output fields in CSV file
    ls2csv.set_output_fields(["@timestamp", "_id"])

    # Execute search
    ls2csv.search()

    # Output CSV file
    csv = ls2csv.render_csv()


You can also configure settings with reading a file, using `Logstash2CSV.load_connection` or `Logstash2CSV.load_fields`.


## License

MPL2 license, see LICENSE file.
