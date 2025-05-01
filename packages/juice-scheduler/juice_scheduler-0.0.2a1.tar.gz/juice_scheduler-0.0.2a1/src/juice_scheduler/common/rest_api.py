from __future__ import annotations

import json

from requests import session

SUCCES_RESPONSE = 200

class RestApiConnector:
    def __init__(self, server_url: str):
        self.session = session()
        self.server_url = server_url

    def __get_json(self, endpoint: str):
        response = self.session.get(self.server_url + endpoint)
        if response.status_code != SUCCES_RESPONSE:
            raise RestApiError(response.text)
        return response.json()

    def __get_file(self, file_path: str):
        response = self.session.get(file_path)
        if response.status_code != SUCCES_RESPONSE:
            raise RestApiError(file_path)
        return response.text

    def get_segment_definitions(self, trajectory: str):
        return self.__get_json(f"trajectory/{trajectory}/segment_definition")

    def get_file(self, file_path: str):
        return self.__get_file(file_path)

    def get_events(self,
                  start: str, end: str, trajectory: str, mnemonics: list[str]):
        body = {
            "start": start,
            "end": end,
            "trajectory": trajectory,
            "mnemonics": mnemonics}

        endpoint = f"events/?body={json.dumps(body)}"
        return self.__get_json(endpoint)

    def get_trajectory(self, trajectory: str):
        endpoint = f"trajectory/{trajectory}"
        return self.__get_json(endpoint)



class RestApiError(Exception):
    pass
