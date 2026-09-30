"""Durable member/client identity registry for the Member AI Gateway."""
from dataclasses import dataclass
from typing import Dict, FrozenSet

class IdentityError(PermissionError):
    pass

@dataclass(frozen=True)
class MemberRecord:
    member_id: str
    display_name: str
    membership_status: str
    roles: FrozenSet[str]

@dataclass(frozen=True)
class ClientRecord:
    client_id: str
    member_id: str
    status: str
    scopes: FrozenSet[str]

MEMBERS: Dict[str, MemberRecord] = {
    "jake": MemberRecord("jake", "Jake", "ACTIVE", frozenset({"commissioner","league_member"})),
    "pitts": MemberRecord("pitts", "Pitts", "ACTIVE", frozenset({"league_member"})),
}

CLIENTS: Dict[str, ClientRecord] = {
    "jake-chatgpt": ClientRecord("jake-chatgpt","jake","ACTIVE",frozenset({
        "capabilities.read","league.read","history.read","identity.read","pittys_book.inputs"
    })),
    "pitts-chatgpt": ClientRecord("pitts-chatgpt","pitts","ACTIVE",frozenset({
        "capabilities.read","league.read","history.read","identity.read","pittys_book.inputs"
    })),
}

def resolve_client(client_id: str) -> tuple[MemberRecord, ClientRecord]:
    client = CLIENTS.get(client_id)
    if client is None:
        raise IdentityError("CLIENT_UNKNOWN")
    if client.status != "ACTIVE":
        raise IdentityError("CLIENT_REVOKED")
    member = MEMBERS.get(client.member_id)
    if member is None or member.membership_status != "ACTIVE":
        raise IdentityError("MEMBERSHIP_INACTIVE")
    return member, client

def revoke_client(client_id: str) -> None:
    current = CLIENTS.get(client_id)
    if current is None:
        raise IdentityError("CLIENT_UNKNOWN")
    CLIENTS[client_id] = ClientRecord(current.client_id,current.member_id,"REVOKED",current.scopes)

def rotate_client(old_client_id: str, new_client_id: str) -> ClientRecord:
    member, old = resolve_client(old_client_id)
    revoke_client(old_client_id)
    new = ClientRecord(new_client_id,member.member_id,"ACTIVE",old.scopes)
    CLIENTS[new_client_id] = new
    return new
