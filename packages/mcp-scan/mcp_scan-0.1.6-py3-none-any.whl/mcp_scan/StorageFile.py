import json
import os
from datetime import datetime
from hashlib import md5
from typing import Any

import rich
from pydantic import ValidationError

from .models import Entity, ScannedEntities, ScannedEntity, entity_type_to_str
from .utils import upload_whitelist_entry


class StorageFile:
    def __init__(self, path: str):
        self.path = os.path.expanduser(path)
        # if path is a file
        self.scanned_entities: ScannedEntities = ScannedEntities({})
        self.whitelist: dict[str, str] = {}

        if os.path.isfile(path):
            rich.print(f"[bold]Legacy storage file detected at {path}, converting to new format[/bold]")
            # legacy format
            with open(path, "r") as f:
                legacy_data = json.load(f)
            if "__whitelist" in legacy_data:
                self.whitelist = legacy_data["__whitelist"]
                del legacy_data["__whitelist"]
            try:
                self.scanned_entities = ScannedEntities.model_validate(legacy_data)
            except ValidationError as e:
                rich.print(f"[bold red]Could not load legacy storage file {self.path}: {e}[/bold red]")
            os.remove(path)

        if os.path.exists(path) and os.path.isdir(path):
            scanned_entities_path = os.path.join(path, "scanned_entities.json")
            if os.path.exists(scanned_entities_path):
                with open(scanned_entities_path, "r") as f:
                    try:
                        self.scanned_entities = ScannedEntities.model_validate_json(f.read())
                    except ValidationError as e:
                        rich.print(
                            f"[bold red]Could not load scanned entities file {scanned_entities_path}: {e}[/bold red]"
                        )
            if os.path.exists(os.path.join(path, "whitelist.json")):
                with open(os.path.join(path, "whitelist.json"), "r") as f:
                    self.whitelist = json.load(f)

    def reset_whitelist(self) -> None:
        self.whitelist = {}
        self.save()

    def compute_hash(self, entity: Entity | None) -> str | None:
        if entity is None:
            return None
        if not hasattr(entity, "description") or entity.description is None:
            return None
        return md5((entity.description).encode()).hexdigest()

    def check_and_update(self, server_name: str, entity: Entity, verified: bool|None) -> tuple[bool, list[str]]:
        entity_type = entity_type_to_str(entity)
        key = f"{server_name}.{entity_type}.{entity.name}"
        hash = self.compute_hash(entity)
        new_data = ScannedEntity(
            hash=hash,
            type=entity_type,
            verified=verified,
            timestamp=datetime.now(),
            description=entity.description,
        )
        changed = False
        messages = []
        prev_data = None
        if key in self.scanned_entities.root:
            prev_data = self.scanned_entities.root[key]
            changed = prev_data.hash != new_data.hash
            if changed:
                messages.append(f"{entity_type} description changed since previous scan at " + prev_data.timestamp.strftime(
                    "%d/%m/%Y, %H:%M:%S"
                ))
                messages.append(prev_data.description)
        self.scanned_entities.root[key] = new_data
        return changed, messages

    def print_whitelist(self) -> None:
        whitelist_keys = sorted(self.whitelist.keys())
        for key in whitelist_keys:
            if "." in key:
                entity_type, name = key.split(".", 1)
            else:
                entity_type, name = "tool", key
            rich.print(entity_type, name, self.whitelist[key])
        rich.print(f"[bold]{len(whitelist_keys)} entries in whitelist[/bold]")

    def add_to_whitelist(self, entity_type: str, name: str, hash: str, base_url: str | None = None) -> None:
        key = f"{entity_type}.{name}"
        self.whitelist[key] = hash
        self.save()
        if base_url is not None:
            upload_whitelist_entry(name, hash, base_url)

    def is_whitelisted(self, entity: Entity) -> bool:
        hash = self.compute_hash(entity)
        return hash in self.whitelist.values()

    def save(self) -> None:
        os.makedirs(self.path, exist_ok=True)
        with open(os.path.join(self.path, "scanned_entities.json"), "w") as f:
            f.write(self.scanned_entities.model_dump_json())
        with open(os.path.join(self.path, "whitelist.json"), "w") as f:
            json.dump(self.whitelist, f)
