# server.py
import sys
import os
import json
from typing import Dict, List, Optional, Any, Union
import httpx
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Linear MCP")

# Environment variables for Linear configuration
LINEAR_API_KEY = os.environ.get("LINEAR_API_KEY")
LINEAR_BASE_URL = os.environ.get("LINEAR_BASE_URL", "https://api.linear.app/graphql")

# Check if environment variables are set
if not LINEAR_API_KEY:
    print("Warning: Linear environment variables not fully configured. Set LINEAR_API_KEY.", file=sys.stderr)

# Helper function for GraphQL API requests
async def make_linear_graphql_request(query: str, variables: Dict = None) -> Dict:
    """
    Make a GraphQL request to the Linear API.
    
    Args:
        query: GraphQL query string
        variables: Variables for the GraphQL query
    
    Returns:
        Response from Linear API as dictionary
    """
    url = LINEAR_BASE_URL
    headers = {
        "Authorization": LINEAR_API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    payload = {
        "query": query,
        "variables": variables or {}
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        
        if response.status_code >= 400:
            return {
                "error": True,
                "status_code": response.status_code,
                "message": response.text
            }
            
        result = response.json()
        
        # Check if there are any GraphQL errors
        if "errors" in result:
            return {
                "error": True,
                "message": result["errors"][0]["message"],
                "errors": result["errors"]
            }
            
        return result

# === TOOLS ===

@mcp.tool()
async def get_issue(issue_id: str) -> str:
    """
    Get details of a specific Linear issue.
    
    Args:
        issue_id: The Linear issue ID (e.g., "ABC-123")
    """
    query = """
    query Issue($id: String!) {
        issue(id: $id) {
            id
            identifier
            title
            description
            state {
                id
                name
                color
            }
            assignee {
                id
                name
                email
            }
            team {
                id
                name
            }
            priority
            estimate
            createdAt
            updatedAt
            comments {
                nodes {
                    id
                    body
                    user {
                        name
                    }
                    createdAt
                }
            }
        }
    }
    """
    
    result = await make_linear_graphql_request(query, {"id": issue_id})
    
    if "error" in result:
        return f"Error retrieving issue: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result["data"], indent=2)

@mcp.tool()
async def create_issue(team_id: str, title: str, description: str = "", assignee_id: str = None, priority: int = 0) -> str:
    """
    Create a new issue in Linear.
    
    Args:
        team_id: The ID of the team to create the issue in
        title: The title of the issue
        description: The description of the issue
        assignee_id: The ID of the user to assign the issue to (optional)
        priority: The priority of the issue (0-4, 0 is no priority, 4 is urgent)
    """
    query = """
    mutation CreateIssue($input: IssueCreateInput!) {
        issueCreate(input: $input) {
            success
            issue {
                id
                identifier
                title
                url
            }
        }
    }
    """
    
    variables = {
        "input": {
            "teamId": team_id,
            "title": title,
            "description": description,
        }
    }
    
    if assignee_id:
        variables["input"]["assigneeId"] = assignee_id
    
    if priority:
        variables["input"]["priority"] = priority
    
    result = await make_linear_graphql_request(query, variables)
    
    if "error" in result:
        return f"Error creating issue: {result.get('message', 'Unknown error')}"
    
    issue_data = result["data"]["issueCreate"]["issue"]
    return f"Issue created successfully: {issue_data['identifier']} - {issue_data['title']}\nURL: {issue_data['url']}"

@mcp.tool()
async def update_issue(issue_id: str, title: str = None, description: str = None, state_id: str = None, assignee_id: str = None, priority: int = None) -> str:
    """
    Update an existing issue in Linear.
    
    Args:
        issue_id: The ID of the issue to update
        title: The new title of the issue (optional)
        description: The new description of the issue (optional)
        state_id: The ID of the new state (optional)
        assignee_id: The ID of the user to assign the issue to (optional)
        priority: The new priority of the issue (0-4, 0 is no priority, 4 is urgent) (optional)
    """
    query = """
    mutation UpdateIssue($id: String!, $input: IssueUpdateInput!) {
        issueUpdate(id: $id, input: $input) {
            success
            issue {
                id
                identifier
                title
                url
            }
        }
    }
    """
    
    input_vars = {}
    
    if title is not None:
        input_vars["title"] = title
    
    if description is not None:
        input_vars["description"] = description
    
    if state_id is not None:
        input_vars["stateId"] = state_id
    
    if assignee_id is not None:
        input_vars["assigneeId"] = assignee_id
    
    if priority is not None:
        input_vars["priority"] = priority
    
    if not input_vars:
        return "Error: No update parameters provided."
    
    variables = {
        "id": issue_id,
        "input": input_vars
    }
    
    result = await make_linear_graphql_request(query, variables)
    
    if "error" in result:
        return f"Error updating issue: {result.get('message', 'Unknown error')}"
    
    issue_data = result["data"]["issueUpdate"]["issue"]
    return f"Issue updated successfully: {issue_data['identifier']} - {issue_data['title']}\nURL: {issue_data['url']}"

@mcp.tool()
async def add_comment(issue_id: str, body: str) -> str:
    """
    Add a comment to an issue in Linear.
    
    Args:
        issue_id: The ID of the issue to comment on
        body: The body of the comment
    """
    query = """
    mutation CommentCreate($input: CommentCreateInput!) {
        commentCreate(input: $input) {
            success
            comment {
                id
                body
            }
        }
    }
    """
    
    variables = {
        "input": {
            "issueId": issue_id,
            "body": body
        }
    }
    
    result = await make_linear_graphql_request(query, variables)
    
    if "error" in result:
        return f"Error adding comment: {result.get('message', 'Unknown error')}"
    
    return "Comment added successfully."

@mcp.tool()
async def search_issues(term: str, team_ids: str = None) -> str:
    """
    Search for issues in Linear.
    
    Args:
        term: The search term
        team_ids: Comma-separated list of team IDs to search within (optional)
    """
    query = """
    query IssueSearch($filter: IssueFilter, $first: Int!) {
        issues(filter: $filter, first: $first) {
            nodes {
                id
                identifier
                title
                state {
                    name
                }
                assignee {
                    name
                }
                team {
                    name
                }
                priority
                createdAt
            }
        }
    }
    """
    
    filter_params = {}
    
    # Add search term
    filter_params["search"] = term
    
    # Add team IDs if provided
    if team_ids:
        team_id_list = team_ids.split(",")
        filter_params["team"] = {
            "id": {
                "in": team_id_list
            }
        }
    
    variables = {
        "filter": filter_params,
        "first": 10  # Limit to 10 results
    }
    
    result = await make_linear_graphql_request(query, variables)
    
    if "error" in result:
        return f"Error searching issues: {result.get('message', 'Unknown error')}"
    
    issues = result["data"]["issues"]["nodes"]
    
    if not issues:
        return "No issues found matching the search term."
    
    formatted_issues = []
    for issue in issues:
        formatted_issue = {
            "id": issue["id"],
            "identifier": issue["identifier"],
            "title": issue["title"],
            "state": issue["state"]["name"] if issue["state"] else "No state",
            "assignee": issue["assignee"]["name"] if issue["assignee"] else "Unassigned",
            "team": issue["team"]["name"] if issue["team"] else "No team",
            "priority": issue["priority"],
            "created_at": issue["createdAt"]
        }
        formatted_issues.append(formatted_issue)
    
    return json.dumps(formatted_issues, indent=2)

@mcp.tool()
async def list_teams() -> str:
    """
    List all teams in Linear.
    """
    query = """
    query Teams {
        teams {
            nodes {
                id
                name
                key
                description
                states {
                    nodes {
                        id
                        name
                        color
                    }
                }
            }
        }
    }
    """
    
    result = await make_linear_graphql_request(query)
    
    if "error" in result:
        return f"Error listing teams: {result.get('message', 'Unknown error')}"
    
    teams = result["data"]["teams"]["nodes"]
    
    if not teams:
        return "No teams found."
    
    formatted_teams = []
    for team in teams:
        states = team["states"]["nodes"] if "states" in team and "nodes" in team["states"] else []
        formatted_team = {
            "id": team["id"],
            "name": team["name"],
            "key": team["key"],
            "description": team["description"],
            "states": [{"id": state["id"], "name": state["name"], "color": state["color"]} for state in states]
        }
        formatted_teams.append(formatted_team)
    
    return json.dumps(formatted_teams, indent=2)

@mcp.tool()
async def list_projects(team_id: str = None) -> str:
    """
    List projects in Linear.
    
    Args:
        team_id: The ID of the team to list projects for (optional)
    """
    query = """
    query Projects($filter: ProjectFilter) {
        projects(filter: $filter) {
            nodes {
                id
                name
                description
                state
                team {
                    id
                    name
                }
                creator {
                    name
                }
                lead {
                    name
                }
                startDate
                targetDate
            }
        }
    }
    """
    
    variables = {}
    
    if team_id:
        variables["filter"] = {
            "team": {
                "id": {
                    "eq": team_id
                }
            }
        }
    
    result = await make_linear_graphql_request(query, variables)
    
    if "error" in result:
        return f"Error listing projects: {result.get('message', 'Unknown error')}"
    
    projects = result["data"]["projects"]["nodes"]
    
    if not projects:
        return "No projects found."
    
    formatted_projects = []
    for project in projects:
        formatted_project = {
            "id": project["id"],
            "name": project["name"],
            "description": project["description"],
            "state": project["state"],
            "team": project["team"]["name"] if project["team"] else "No team",
            "creator": project["creator"]["name"] if project["creator"] else "Unknown",
            "lead": project["lead"]["name"] if project["lead"] else "No lead",
            "start_date": project["startDate"],
            "target_date": project["targetDate"]
        }
        formatted_projects.append(formatted_project)
    
    return json.dumps(formatted_projects, indent=2)

@mcp.tool()
async def list_issue_states(team_id: str) -> str:
    """
    List all issue states for a team in Linear.
    
    Args:
        team_id: The ID of the team to list states for
    """
    query = """
    query TeamStates($teamId: String!) {
        team(id: $teamId) {
            id
            name
            states {
                nodes {
                    id
                    name
                    color
                    type
                    description
                }
            }
        }
    }
    """
    
    variables = {
        "teamId": team_id
    }
    
    result = await make_linear_graphql_request(query, variables)
    
    if "error" in result:
        return f"Error listing issue states: {result.get('message', 'Unknown error')}"
    
    if not result["data"] or not result["data"]["team"]:
        return f"Team with ID {team_id} not found."
    
    team_data = result["data"]["team"]
    states = team_data["states"]["nodes"]
    
    if not states:
        return f"No states found for team {team_data['name']}."
    
    formatted_states = []
    for state in states:
        formatted_state = {
            "id": state["id"],
            "name": state["name"],
            "color": state["color"],
            "type": state["type"],
            "description": state["description"]
        }
        formatted_states.append(formatted_state)
    
    return json.dumps(formatted_states, indent=2)

# === RESOURCES ===

@mcp.resource("linear://issues")
async def get_issues() -> str:
    """Get a list of all issues in Linear."""
    query = """
    query Issues($first: Int!) {
        issues(first: $first) {
            nodes {
                id
                identifier
                title
                state {
                    name
                }
                assignee {
                    name
                }
                team {
                    name
                }
                priority
                createdAt
            }
        }
    }
    """
    
    variables = {
        "first": 100  # Limit to 100 issues
    }
    
    result = await make_linear_graphql_request(query, variables)
    
    if "error" in result:
        return f"Error retrieving issues: {result.get('message', 'Unknown error')}"
    
    return json.dumps(result["data"], indent=2)

@mcp.resource("linear://teams")
async def get_all_teams() -> str:
    """Get a list of all teams in Linear."""
    query = """
    query Teams {
        teams {
            nodes {
                id
                name
                key
                description
            }
        }
    }
    """
    
    result = await make_linear_graphql_request(query)
    
    if "error" in result:
        return f"Error retrieving teams: {result.get('message', 'Unknown error')}"
    
    return json.dumps(result["data"], indent=2)

@mcp.resource("linear://projects")
async def get_all_projects() -> str:
    """Get a list of all projects in Linear."""
    query = """
    query Projects {
        projects {
            nodes {
                id
                name
                description
                state
                team {
                    name
                }
                startDate
                targetDate
            }
        }
    }
    """
    
    result = await make_linear_graphql_request(query)
    
    if "error" in result:
        return f"Error retrieving projects: {result.get('message', 'Unknown error')}"
    
    return json.dumps(result["data"], indent=2)

@mcp.resource("linear://user")
async def get_user_info() -> str:
    """Get information about the authenticated user."""
    query = """
    query Viewer {
        viewer {
            id
            name
            email
            displayName
            admin
            organizationId
            teams {
                nodes {
                    id
                    name
                }
            }
        }
    }
    """
    
    result = await make_linear_graphql_request(query)
    
    if "error" in result:
        return f"Error retrieving user information: {result.get('message', 'Unknown error')}"
    
    return json.dumps(result["data"], indent=2)

# === PROMPTS ===

@mcp.prompt("create_issue_prompt")
def create_issue_prompt(title: str = None, description: str = None, team_key: str = None) -> str:
    """
    A prompt template for creating a new issue in Linear.
    
    Args:
        title: Title of the issue
        description: Description of the issue
        team_key: Key of the team to create the issue in (e.g., "ENG")
    """
    prompt_text = "I need to create a new issue in Linear."
    
    if all([title, description, team_key]):
        prompt_text += f"\n\nTitle: {title}\nDescription: {description}\nTeam: {team_key}"
    elif any([title, description, team_key]):
        prompt_text += "\n\nI have the following details so far:"
        if title:
            prompt_text += f"\nTitle: {title}"
        if description:
            prompt_text += f"\nDescription: {description}"
        if team_key:
            prompt_text += f"\nTeam: {team_key}"
    
    return prompt_text

@mcp.prompt("search_issues_prompt")
def search_issues_prompt(query: str = None, team_key: str = None) -> str:
    """
    A prompt template for searching issues in Linear.
    
    Args:
        query: Search query
        team_key: Team key to limit search to (e.g., "ENG")
    """
    prompt_text = "I need to search for issues in Linear."
    
    if query:
        prompt_text += f"\n\nSearch query: {query}"
    
    if team_key:
        prompt_text += f"\nTeam: {team_key}"
    
    return prompt_text

@mcp.prompt("update_issue_prompt")
def update_issue_prompt(issue_id: str = None, title: str = None, description: str = None, state: str = None, assignee: str = None) -> str:
    """
    A prompt template for updating an issue in Linear.
    
    Args:
        issue_id: ID of the issue to update (e.g., "ENG-123")
        title: New title for the issue
        description: New description for the issue
        state: New state for the issue
        assignee: New assignee for the issue
    """
    prompt_text = "I need to update an issue in Linear."
    
    if issue_id:
        prompt_text += f"\n\nIssue ID: {issue_id}"
    
    if any([title, description, state, assignee]):
        prompt_text += "\n\nI want to update the following:"
        if title:
            prompt_text += f"\nTitle: {title}"
        if description:
            prompt_text += f"\nDescription: {description}"
        if state:
            prompt_text += f"\nState: {state}"
        if assignee:
            prompt_text += f"\nAssignee: {assignee}"
    
    return prompt_text

if __name__ == "__main__":
    print("Starting Linear MCP server...", file=sys.stderr)
    mcp.run()
