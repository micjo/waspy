from waspy.iba.file_handler import FileHandler
import glob
from pathlib import Path
import json
import threading
import logging
import time
import requests
from datetime import datetime, timedelta
from .field_issues import FieldIssue, WarningIssue, ErrorIssue
import itertools


class ExpectedFetchError(Exception):
    ...

def get_data_iteration(data: dict):
    if data == None:
        return []
    for key1, value1 in data.items():
        for key2, value2 in value1.items():
            if key2 == "color" or key2 == "column":
                continue
            identifier = key1 + '.' + key2
            yield key1, key2, identifier

def get_nested_value(dictionary, dotted_key):
    keys = dotted_key.split(".")
    value = dictionary
    for key in keys:
        value = value[key]
    return value

class DashboardHandler:
    FILESAVE_INTERVAL = 10*60 # seconds, so 10 minutes in total
    UPDATE_INTERVAL = 10 # seconds
    DAYBOOK_DATE_FORMAT = "%Y-%m-%d_%Hh"
    FILES_IN_HISTORY = 30*24 # How points to show in a plot (expressed in files)

    def __init__(self, file_handler):
        self._file_handler = file_handler
        self._cached_latest_dashboard = None
        self._cached_endpoints = None
        self._last_filesave: int = 0
        self.issues = {}
    
    def handle_dashboard_data(self, data):
        for key1, key2, identifier in get_data_iteration(data):
            if (not key1[0].isupper()) or (not key2[0].isupper()):
                self.add_warning(identifier, "It is advised to make the first letter of a field name an uppercase.")
            identifier = key1 + '.' + key2
            if identifier not in self.get_endpoints().keys():
                self.add_warning(identifier, "This field was not found in the endpoints file. Please add it in `wasp/daybook/endpoints.json`.")
                data[key1][key2].update({
                    "autoUpdateable": False,
                    "identifier": identifier,
                    "issues": self.get_json_issues(identifier)
                })
                continue
            auto_updateable = "auto-update" in self.get_endpoints()[identifier]
            data[key1][key2].update({
                "autoUpdateable": auto_updateable,
                "min": self.get_endpoints()[identifier]["min"],
                "max": self.get_endpoints()[identifier]["max"],
                "identifier": identifier,
                "issues": self.get_json_issues(identifier)
            })
        return data

    def start_update_thread(self):
        t1 = threading.Thread(target=self._update_loop, daemon=True)
        t1.start()
    
    def get_json_issues(self, identifier):
        return [issue.to_json() for issue in self.issues.get(identifier, []) if time.time() <= issue.alive_until]
    
    def add_error(self, identifier, message: str):
        self._add_issue(identifier, ErrorIssue(message))
    
    def add_warning(self, identifier, message: str):
        self._add_issue(identifier, WarningIssue(message))
    
    def _add_issue(self, identifier, issue: object):
        key1, key2 = identifier.split('.')
        issues = self.issues.get(identifier, [])

        if issue.message in [issue.message for issue in issues]:
            # already added, dont add
            # just reset the timer
            [_issue for _issue in issues if issue.message == _issue.message][0].revive()
            return 
        
        issues.append(issue)
        self.issues[identifier] = issues
        if not key1 in self._cached_latest_dashboard or not key2 in self._cached_latest_dashboard[key1]:
            # edge case: when a warning is added to a not yet existing field
            return
        
        self._cached_latest_dashboard[key1][key2].update({"issues": self.get_json_issues(identifier)})
    
    def _update_loop(self):
        while True:
            self.update()
            time.sleep(DashboardHandler.UPDATE_INTERVAL)
    
    def update(self):
        # Auto update fields
        DELTA_MINUTES = 2
        for key1, key2, identifier in get_data_iteration(self.get_dashboard()):
            if identifier in self.get_endpoints().keys() and "auto-update" in self.get_endpoints()[identifier]:
                try:
                    resp = requests.get(self.get_endpoints()[identifier]["auto-update"]["url"], timeout=1)
                    if resp.status_code != 200:
                        raise ExpectedFetchError(f"Dashboard update request error: server responded with status code {resp.status_code}.")
                    response_data = resp.json()
                    value = get_nested_value(response_data, self.get_endpoints()[identifier]["auto-update"]["key"])

                    self._cached_latest_dashboard[key1][key2].update({"value": value})
                
                except ExpectedFetchError as e:
                    self.add_error(identifier, str(e))
                    continue
                except Exception as e:
                    self.add_error(identifier, "An error occurred while updating this field: " + str(e))
                    logging.error(f"An unexpected error occurred while auto-updating a field {str(e)}.")
                    continue
        
        # check for file save
        if time.time() - self._last_filesave >= DashboardHandler.FILESAVE_INTERVAL:
            self._save_daybook_file()
            self._last_filesave = time.time()
        
        # update field issues
        for identifier, value in self.issues.items():
            for index, issue in enumerate(value):
                # kill issue
                self.issues[identifier] = [issue for issue in self.issues.get(identifier, []) if issue.alive_until >= time.time()]
            key1, key2 = identifier.split(".")
            self._cached_latest_dashboard[key1][key2]["issues"] = self.get_json_issues(identifier)

    def get_dashboard(self):
        if self._cached_latest_dashboard is not None:
            return self._cached_latest_dashboard
    
        dashboard_files = glob.glob(str(self._file_handler._remote / Path("entries/*.json")))
        if len(dashboard_files) == 0:
            raise FileNotFoundError()
        
        latest_file = max(dashboard_files)
        self._cached_latest_dashboard = self._file_handler.read_json_from_disk(latest_file)
        
        self._cached_latest_dashboard = self.handle_dashboard_data(self._cached_latest_dashboard)
            
        self.update()
        return self._cached_latest_dashboard

    def get_template_names(self):
        filenames = glob.glob(str(self._file_handler._remote / Path("templates/*.json")))
        return sorted([Path(filename).name for filename in filenames])

    def get_template(self, filename: str):
        with open(str(self._file_handler._remote / Path("templates/"+filename)), 'r') as f:
            data = json.load(f)
        data = self.handle_dashboard_data(data)
        return data
    
    def save_dashboard(self, dashboard_data: dict):
        self._cached_latest_dashboard = dashboard_data
        self._save_daybook_file()

    def _save_daybook_file(self):
        # Generate a unique, timestamped filename
        timestamp = datetime.now().strftime(DashboardHandler.DAYBOOK_DATE_FORMAT)
        filename = f"{timestamp}.json"

        with open(str(self._file_handler._remote / Path("entries/" + filename)), 'w+') as f:
            json.dump(self._cached_latest_dashboard, f)
    
    def add_to_favorites(self, data):
        # Generate a unique, timestamped filename
        filename = data["favoriteFileName"]

        with open(str(self._file_handler._remote / Path("favorites/" + filename+".json")), 'w+') as f:
            json.dump(data, f)
        
    def get_endpoints(self):
        if self._cached_endpoints is not None:
            return self._cached_endpoints
        
        with open(str(self._file_handler._remote / Path("endpoints.json")), 'r') as f:
            self._cached_endpoints = json.load(f)
            return self._cached_endpoints
    
    def get_history_by_id(self, identifier: str, start: int = None, end: int = None, limit: int = 100):
        """
        Returns entries of the given identifier filtered by optional start/end timestamps.
        
        Parameters:
            identifier: str in the format "key1.key2"
            start: int, optional, timestamp in milliseconds since epoch
            end: int, optional, timestamp in milliseconds since epoch
            limit: int, maximum number of entries to return (default 100)
        """
        keys = identifier.split('.')
        if len(keys) != 2:
            raise ValueError("Identifier did not follow the format `key1.key2`.")
        
        key1, key2 = keys
        output_data = []

        # Read all files in chronological order
        filenames = glob.glob(str(self._file_handler._remote / Path("entries/*.json")))
        daybook_files = sorted([filename for filename in filenames], key=lambda filename: Path(filename).name)

        for filename in daybook_files:
            if len(output_data) >= limit:
                break  # Stop once we have enough entries

            data = self._file_handler.read_json_from_disk(filename)
            if key1 in data and key2 in data[key1] and "value" in data[key1][key2]:
                # Extract the timestamp from filename
                date_str = Path(filename).name.split(".")[0]  # e.g. "2025-08-27_14h"
                dt = datetime.strptime(date_str, DashboardHandler.DAYBOOK_DATE_FORMAT)
                timestamp_ms = int(dt.timestamp() * 1000)  # milliseconds since epoch

                # Filter by start/end timestamps
                if start and timestamp_ms < start:
                    continue
                if end and timestamp_ms > end:
                    continue

                value = data[key1][key2]["value"]
                output_data.append({"value": value, "timestamp": timestamp_ms})

        # Return the latest entries first
        return output_data[-limit:]
