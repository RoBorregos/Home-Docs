"""Read-only access to a GitHub Projects v2 board."""

import json
import urllib.request
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta

API = "https://api.github.com/graphql"

FIELDS_QUERY = """
query($org: String!, $number: Int!) {
  organization(login: $org) {
    projectV2(number: $number) {
      url
      fields(first: 50) {
        nodes {
          ... on ProjectV2IterationField {
            name
            configuration {
              iterations { title startDate duration }
              completedIterations { title startDate duration }
            }
          }
        }
      }
    }
  }
}
"""

ITEMS_QUERY = """
query($org: String!, $number: Int!, $cursor: String) {
  organization(login: $org) {
    projectV2(number: $number) {
      items(first: 100, after: $cursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          fieldValues(first: 30) {
            nodes {
              ... on ProjectV2ItemFieldSingleSelectValue {
                name
                field { ... on ProjectV2FieldCommon { name } }
              }
              ... on ProjectV2ItemFieldIterationValue {
                startDate
                field { ... on ProjectV2FieldCommon { name } }
              }
            }
          }
          content {
            __typename
            ... on Issue {
              number title url state closedAt
              assignees(first: 10) { nodes { login name } }
              comments(last: 20) {
                nodes { createdAt body author { __typename login } }
              }
            }
          }
        }
      }
    }
  }
}
"""


@dataclass(frozen=True)
class Sprint:
    title: str
    start: date
    duration: int

    @property
    def end(self) -> date:
        # Exclusive: first day after the sprint
        return self.start + timedelta(days=self.duration)


@dataclass
class Comment:
    author: str
    created: datetime
    body: str


@dataclass
class Item:
    number: int
    title: str
    url: str
    state: str
    closed_at: datetime | None
    assignees: list[tuple[str, str | None]]
    values: dict[str, str]
    sprint_start: date | None
    comments: list[Comment] = field(default_factory=list)


def graphql(token: str, query: str, variables: dict) -> dict:
    request = urllib.request.Request(
        API,
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        payload = json.load(response)
    if payload.get("errors"):
        raise RuntimeError(f"GraphQL error: {payload['errors']}")
    return payload["data"]


def parse_timestamp(value: str | None) -> datetime | None:
    return datetime.fromisoformat(value.replace("Z", "+00:00")) if value else None


def parse_sprints(field_nodes: list[dict], sprint_field: str) -> list[Sprint]:
    for node in field_nodes:
        if node.get("name") != sprint_field:
            continue
        config = node["configuration"]
        raw = config["iterations"] + config["completedIterations"]
        sprints = {
            Sprint(it["title"], date.fromisoformat(it["startDate"]), it["duration"]) for it in raw
        }
        return sorted(sprints, key=lambda s: s.start)
    raise ValueError(f"Iteration field '{sprint_field}' not found on the board")


def parse_items(nodes: list[dict], sprint_field: str) -> list[Item]:
    items = []
    for node in nodes:
        content = node.get("content") or {}
        # Draft issues and pull requests are not tracked as tasks
        if content.get("__typename") != "Issue":
            continue

        values, sprint_start = {}, None
        for value in node["fieldValues"]["nodes"]:
            name = (value.get("field") or {}).get("name")
            if not name:
                continue
            if name == sprint_field and value.get("startDate"):
                sprint_start = date.fromisoformat(value["startDate"])
            elif value.get("name"):
                values[name] = value["name"]

        comments = [
            Comment(c["author"]["login"], parse_timestamp(c["createdAt"]), c["body"])
            for c in content["comments"]["nodes"]
            if c.get("author") and c["author"]["__typename"] != "Bot"
        ]
        items.append(Item(
            number=content["number"],
            title=content["title"],
            url=content["url"],
            state=content["state"],
            closed_at=parse_timestamp(content.get("closedAt")),
            assignees=[(a["login"], a.get("name")) for a in content["assignees"]["nodes"]],
            values=values,
            sprint_start=sprint_start,
            comments=comments,
        ))
    return items


def fetch(token: str, org: str, number: int, sprint_field: str) -> tuple[str, list[Sprint], list[Item]]:
    variables = {"org": org, "number": number}
    board = graphql(token, FIELDS_QUERY, variables)["organization"]["projectV2"]
    sprints = parse_sprints(board["fields"]["nodes"], sprint_field)

    nodes, cursor = [], None
    while True:
        page = graphql(token, ITEMS_QUERY, {**variables, "cursor": cursor})
        items = page["organization"]["projectV2"]["items"]
        nodes += items["nodes"]
        if not items["pageInfo"]["hasNextPage"]:
            break
        cursor = items["pageInfo"]["endCursor"]

    return board["url"], sprints, parse_items(nodes, sprint_field)
