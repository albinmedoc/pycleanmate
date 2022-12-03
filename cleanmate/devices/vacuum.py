"""A Cleanmate vacuum."""

from ..connection import Connection
from ..enums import WorkMode, WorkState, MopMode


class CleanmateVacuum(Connection):
    """A Cleanmate vacuum."""
    battery_level: int = None
    version: str = None
    work_mode: WorkMode = None
    work_state: WorkState = None
    mop_mode: MopMode = None
    volume: int = None

    def __init__(self, host: str, auth_code: str) -> None:
        super().__init__(host, auth_code)
    
    def update_state(self, state_data):
        self.battery_level = state_data["value"]["battery"]
        self.version = state_data["value"]["version"]
        self.work_mode = state_data["value"]["workMode"]
        self.work_state = state_data["value"]["workState"]
        self.mop_mode = state_data["value"]["waterTank"]

    def send_request_and_update_state(self, data):
        self.send_request(data)
        state_data = self.read_data()
        self.update_state(state_data)

    def poll_state(self) -> None:
        """Poll state of the vacuum."""
        data = {
            "state": "",
            "transitCmd": "98"
        }
        self.send_request(data)
        state_data = self.read_data()
        self.update_state(state_data)
        return state_data

    def poll_map(self) -> None:
        """Poll map of the vacuum."""
        data = {
            "mapWidth": "0",
            "centerPoint": "0",
            "mapHeight": "0",
            "trackNum": "AAA=",
            "mapSign": "AAA=",
            "transitCmd": "133",
        }
        return self.send_request(data)

    def start(self, work_mode: WorkMode = None) -> None:
        """Start cleaning."""
        if(work_mode == None):
            data = {
                "start": "1",
                "transitCmd": "100",
            }
        else:
            data = {
                "mode": str(work_mode),
                "transitCmd": "106",
            }
        self.send_request_and_update_state(data)

    def pause(self) -> None:
        """Pause cleaning."""
        data = {
            "pause": "1",
            "isStop": "0",
            "transitCmd": "102",
        }
        self.send_request_and_update_state(data)

    def charge(self) -> None:
        """Go to charging station."""
        data = {
            "charge": "1",
            "transitCmd": "104",
        }
        self.send_request_and_update_state(data)

    def set_mop_mode(self, mop_mode: MopMode) -> None:
        """Set mop mode of the vacuum."""
        data = {
            "waterTank": str(mop_mode),
            "transitCmd": "145",
        }
        self.send_request_and_update_state(data)

    def set_volume(self, volume: int) -> None:
        """Set volume of the vacuum."""
        vol = 1 + round((volume/100) * 10) / 10
        data = {
            "volume": str(vol),
            "voice": "",
            "transitCmd": "123",
        }
        self.send_request_and_update_state(data)

    def clean_rooms(self, room_ids: list[int]) -> None:
        """Clean specific rooms"""
        unique_sorted_ids = list(dict.fromkeys(room_ids)).sort()
        clean_blocks = map(lambda room_id: {"cleanNum": "1", "blockNum": str(room_id)}, unique_sorted_ids)
        data = {
            'opCmd': "cleanBlocks",
            "cleanBlocks": clean_blocks,
        }
        self.send_request_and_update_state(data)

    def find(self) -> None:
        """Announce vacuum's location"""
        data = {
            "find": "",
            "transitCmd": "143",
        }
        self.send_request_and_update_state(data)

    def __str__(self):
       return f"Cleanmate {self.host}"
