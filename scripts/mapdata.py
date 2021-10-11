import sys

if sys.version_info[0] < 3 or sys.version_info[1] < 5:  # 3.5+
    raise ImportError("Only Python 3.5+ is supported.")

import json
import re
from typing import Dict, Union

quote_keys_pattern = re.compile(
    r"([\{ ])([a-z]+):"
)  # e.g. room: "Portable 1" → "room": "Portable 1"


def fix_json_key(line: str) -> str:
    """
    Fix unquoted JSON-like keys in line.
    :param line: single line from data.txt
    :return: fixed line
    """
    return quote_keys_pattern.sub(r'\1"\2":', line)


def strip(line: str) -> str:
    """
    Cleans up the line: remove any trailing commas and whitespace.
    :param line: single line from data.txt
    :return: cleaned line
    """
    return line.strip().strip(",")


def to_feature(data: Dict[str, Union[float, str]]) -> Dict:
    """
    Converts the data from data.txt in dict format to geojson feature format (in a dict).
    :param data: data from data.txt
    :return: geojson feature
    """
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [
                data["longitude"],
                data["latitude"],
            ],
        },
        "properties": {
            "title": data["room"],
            "floor": data["floor"],
        },
    }


def process_line(line: str) -> Dict:
    # operations spread over muliple statements over nesting because makes it easier to add/remove steps
    # clean input
    line = strip(line)
    line = fix_json_key(line)

    # read data
    raw_data = json.loads(line)

    # convert data
    return to_feature(raw_data)


def main(input_path: str = "data.txt", output_path: str = "data.geojson") -> None:
    """
    Runs the main program: use the data form input_path, convert it to a geojson format and save it to output_path
    """
    with open(input_path) as input_file:
        # usually points to metropolis/core/static/core/js/map/data.txt
        with open(output_path, "w") as output_file:
            # open both files at the same time to show that they are both being used
            data = {
                "type": "FeatureCollection",
                "features": list(map(process_line, input_file)),
            }
            json.dump(data, output_file)


if __name__ == "__main__":
    main()
