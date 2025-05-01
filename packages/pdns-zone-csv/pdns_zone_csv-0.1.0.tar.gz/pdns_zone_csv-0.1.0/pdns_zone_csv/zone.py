import json
import typing
import csv
import io


class Zone:
    def __init__(self, zone_json: str) -> None:
        json_dict: typing.Dict = json.loads(zone_json)

        self.rr_sets: typing.List[RRSet] = []

        for rr_set in json_dict["rrsets"]:
            self.rr_sets.append(RRSet(rr_set))

        return

    def csv(self) -> str:
        buffer = io.StringIO()

        writer: csv.Writer = csv.writer(buffer)

        for rr_set in self.rr_sets:
            writer.writerows(rr_set.csv_rows())

        return buffer.getvalue().strip()


class RRSet:
    def __init__(self, json_dict: typing.Dict) -> None:
        name: str = json_dict["name"]

        ttl: int = json_dict["ttl"]

        rr_type: str = json_dict["type"]

        self.records: typing.List[RR] = []

        for record in json_dict["records"]:
            rr = RR(name, ttl, rr_type, record)

            self.records.append(rr)

        return

    def csv_rows(self) -> typing.List[typing.List[str]]:
        rows: typing.List[typing.List[str]] = []

        for record in self.records:
            row: typing.List[str] = record.csv_row()

            if len(row) > 0:
                rows.append(row)

        return rows


class RR:
    CLASS = "IN"

    def __init__(
        self, name: str, ttl: int, rr_type: str, json_dict: typing.Dict
    ) -> None:
        self.name: str = name

        self.ttl: int = ttl

        self.type: str = rr_type

        self.content: str = json_dict["content"]

        self.disabled: bool = json_dict["disabled"]

        return

    def csv_row(self) -> typing.List[str]:
        if self.disabled:
            return []

        return [self.name, str(self.ttl), self.CLASS, self.type, self.content]
