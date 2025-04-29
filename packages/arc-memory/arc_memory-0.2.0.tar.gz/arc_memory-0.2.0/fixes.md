# Arc Memory SDK - Implementation Plan for Issue #6

This document outlines the implementation plan to address the issues reported in [GitHub Issue #6](https://github.com/Arc-Computer/arc-memory/issues/6).

## 1. Hyperspecific Root Causes Identified

After a detailed code review, we've identified the exact locations and causes of the issues:

### 1.1 GitHub Authentication Issues

- **Root Cause**: In `arc_memory/auth/github.py`, the default GitHub OAuth client ID (`Iv23liNmVnxkNuRfG8tr`) in `arc_memory/auth/default_credentials.py` may be invalid or revoked.
- **Error Handling Gap**: In `get_github_token()` (line 220-258), there's no fallback mechanism when authentication fails.
- **Missing Validation**: The `start_device_flow()` function (line 261-299) doesn't validate the client ID before making the API request.
- **Error Message Issue**: When authentication fails, the error message in line 257 doesn't provide clear guidance on how to resolve the issue.

### 1.2 Database Connection Handling Issues

- **Inconsistent Parameter Types**:
  - Functions in `arc_memory/sql/db.py` like `get_node_by_id()` (line 730), `get_edges_by_src()` (line 782), and `get_edges_by_dst()` (line 849) expect a connection object.
  - Meanwhile, `trace_history_for_file_line()` in `arc_memory/trace.py` (line 377) accepts a file path.

- **Type Validation Missing**:
  - No validation in database functions to check if the input is a connection object or a path.
  - When a `Path` object is passed to functions expecting a connection, the error `'PosixPath' object has no attribute 'execute'` occurs.

- **Connection Management**:
  - `trace_history_for_file_line()` (line 377-411) opens and closes a connection, but other functions expect an already open connection.
  - No consistent pattern for connection management across the codebase.

### 1.3 Inconsistent API Design

- **Parameter Naming Inconsistency**:
  - `db_path` in `trace_history_for_file_line()` (line 378)
  - `conn` in `get_node_by_id()` (line 730), `get_edges_by_src()` (line 782), etc.
  - No standardized naming convention for database connection parameters.

- **Function Signature Inconsistency**:
  - Some functions return dictionaries (`get_node_by_id()` line 730)
  - Others return model objects (`get_node_by_id()` in `trace.py` line 159)
  - No consistent return type pattern across similar functions.

### 1.4 Limited Documentation on Function Parameters

- **Docstring Issues**:
  - Docstrings in `arc_memory/sql/db.py` don't clearly specify that `conn` must be a connection object, not a path.
  - Examples in `docs/examples/sdk-usage.md` don't show how to properly handle connections.

- **Missing API Documentation**:
  - No dedicated API documentation for database functions (no `docs/api/db.md` file).
  - Existing examples don't demonstrate proper error handling.

### 1.5 ADR Processing Issues

- **Date Parsing Problems**:
  - In `arc_memory/ingest/adr.py` (line 184-214), the date parsing logic tries multiple formats but doesn't provide clear error messages when parsing fails.
  - The warning on line 212 (`Could not parse date: {date_str}`) doesn't suggest how to fix the issue.

- **Validation Gaps**:
  - Limited validation for ADR file formats in `parse_adr_frontmatter()` (line 20-72).
  - No schema validation for expected ADR structure.

### 1.6 Lack of Clear Error Messages

- **Generic Error Messages**:
  - Error messages like `Failed to get node by ID: {e}` (line 773) don't provide context about what went wrong.
  - The database connection error (`'PosixPath' object has no attribute 'execute'`) doesn't explain that a connection object is needed.

- **Missing Troubleshooting Guidance**:
  - Error messages don't include suggestions for how to fix common issues.
  - No centralized troubleshooting guide for common errors.

## 2. Implementation Plan

### 2.1 Standardize Database Connection Handling

#### 2.1.1 Create a Simple Connection Wrapper Function in `arc_memory/sql/db.py`

```python
def ensure_connection(conn_or_path: Union[Any, Path, str]) -> sqlite3.Connection:
    """Ensure we have a valid database connection.

    This function accepts either:
    - An existing database connection object
    - A path to a database file (as Path or string)

    It returns a valid database connection in all cases, opening a new
    connection if a path was provided.

    Args:
        conn_or_path: Either a database connection object or a path to a database file.

    Returns:
        A valid database connection.

    Raises:
        DatabaseError: If the input is neither a valid connection nor a valid path.
    """
    from arc_memory.errors import DatabaseError

    # Case 1: Already a connection object
    if hasattr(conn_or_path, 'execute') or hasattr(conn_or_path, 'cursor'):
        return conn_or_path

    # Case 2: A Path object or string path
    if isinstance(conn_or_path, (Path, str)):
        path = Path(conn_or_path) if isinstance(conn_or_path, str) else conn_or_path
        return get_connection(path)

    # Case 3: Invalid input
    raise DatabaseError(
        f"Expected a database connection or path, got {type(conn_or_path).__name__}",
        details={
            "type": type(conn_or_path).__name__,
            "value": str(conn_or_path),
            "hint": "Pass either a database connection object or a Path to the database file."
        }
    )
```

#### 2.1.2 Update Most Frequently Used Database Functions

Rather than modifying all functions at once, focus on the most commonly used ones that are causing issues:

1. First priority (functions directly mentioned in the issue):
   - `get_node_by_id()` (line 730)
   - `get_edges_by_src()` (line 782)
   - `get_edges_by_dst()` (line 849)

2. Second priority (other commonly used functions):
   - `get_node_count()` (line 586)
   - `get_edge_count()` (line 618)

Example update for `get_node_by_id()`:

```python
def get_node_by_id(conn_or_path: Union[Any, Path, str], node_id: str) -> Optional[Dict[str, Any]]:
    """Get a node by its ID.

    Args:
        conn_or_path: Either a database connection object or a path to a database file.
        node_id: The ID of the node.

    Returns:
        The node, or None if it doesn't exist.

    Raises:
        GraphQueryError: If getting the node fails.
    """
    # Get a valid connection
    conn = ensure_connection(conn_or_path)

    # Check if we're using a test database
    if hasattr(conn, 'nodes') and hasattr(conn, 'edges'):
        try:
            from arc_memory.sql.test_db import get_test_node_by_id
            return get_test_node_by_id(conn, node_id)
        except ImportError as e:
            logger.error(f"Failed to import test database module: {e}")
            raise GraphQueryError(f"Failed to get node by ID in test mode: {e}")

    try:
        cursor = conn.execute(
            """
            SELECT id, type, title, body, extra
            FROM nodes
            WHERE id = ?
            """,
            (node_id,),
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return {
            "id": row[0],
            "type": row[1],
            "title": row[2],
            "body": row[3],
            "extra": json.loads(row[4]) if row[4] else {},
        }
    except Exception as e:
        logger.error(f"Failed to get node by ID: {e}")
        raise GraphQueryError(
            f"Failed to get node by ID '{node_id}': {e}",
            details={
                "node_id": node_id,
                "error": str(e),
                "hint": "Make sure you're passing a valid database connection or path."
            }
        )
```

This approach:
1. Makes minimal changes to the existing codebase
2. Focuses on the functions that are causing the most issues
3. Maintains backward compatibility
4. Provides clear error messages

### 2.2 Fix GitHub Authentication

#### 2.2.1 Verify and Update Default Client ID in `arc_memory/auth/default_credentials.py`

```python
# Default GitHub OAuth Client ID for the Arc organizational account
# This is embedded in the package to allow users to authenticate directly
# from the CLI without needing to provide their own OAuth credentials.
DEFAULT_GITHUB_CLIENT_ID = "updated-client-id-here"  # Update with valid client ID
```

#### 2.2.2 Add Fallback Mechanism in `arc_memory/auth/github.py`

Modify `get_github_token()` to include a fallback parameter:

```python
def get_github_token(token: Optional[str] = None, owner: Optional[str] = None, repo: Optional[str] = None, allow_failure: bool = False) -> Optional[str]:
    """Get a GitHub token from various sources.

    Args:
        token: An explicit token to use. If None, tries to find a token from other sources.
        owner: The repository owner. Used for GitHub App installation tokens.
        repo: The repository name. Used for GitHub App installation tokens.
        allow_failure: If True, returns None instead of raising an error when no token is found.

    Returns:
        A GitHub token, or None if allow_failure is True and no token could be found.

    Raises:
        GitHubAuthError: If no token could be found and allow_failure is False.
    """
    # [existing code]

    # No token found
    if allow_failure:
        logger.warning("No GitHub token found. GitHub data will not be included in the graph.")
        return None
    else:
        raise GitHubAuthError(
            "No GitHub token found. Please run 'arc auth gh' to authenticate."
        )
```

#### 2.2.3 Improve Client ID Validation in `arc_memory/cli/auth.py`

Add better validation for the client ID:

```python
def validate_client_id(client_id: str) -> bool:
    """Validate that a GitHub OAuth client ID is properly formatted.

    Args:
        client_id: The client ID to validate.

    Returns:
        True if the client ID is valid, False otherwise.
    """
    # GitHub client IDs are typically 20 characters
    if not client_id or len(client_id) < 10:
        return False

    # Add additional validation if needed
    return True
```

### 2.3 Improve API Consistency

#### 2.3.1 Standardize Parameter Names

Create a style guide for parameter naming:
- Use `conn_or_path` for functions that accept either a connection or path
- Use `conn` for functions that only accept a connection
- Use `db_path` for functions that only accept a path

#### 2.3.2 Update Existing Functions Instead of Creating New API Layer

Rather than creating a new API layer that might add complexity, update the existing functions to be more flexible:

```python
# Update existing function in arc_memory/sql/db.py
def get_node_by_id(conn_or_path: Union[Any, Path, str], node_id: str) -> Optional[Dict[str, Any]]:
    """Get a node by its ID.

    Args:
        conn_or_path: Either a database connection object or a path to a database file.
        node_id: The ID of the node.

    Returns:
        The node, or None if it doesn't exist.
    """
    with db_connection(conn_or_path) as conn:
        # Original implementation using the connection
        try:
            cursor = conn.execute(
                """
                SELECT id, type, title, body, extra
                FROM nodes
                WHERE id = ?
                """,
                (node_id,),
            )
            # Rest of the implementation...
        except Exception as e:
            # Improved error message
            logger.error(f"Failed to get node by ID: {e}")
            raise GraphQueryError(
                f"Failed to get node by ID '{node_id}': {e}",
                details={
                    "node_id": node_id,
                    "error": str(e),
                    "hint": "Make sure the database contains this node ID."
                }
            )
```

This approach:
1. Maintains backward compatibility
2. Improves the developer experience without adding a new layer of abstraction
3. Keeps the API surface area smaller and more manageable

### 2.4 Enhance Documentation

#### 2.4.1 Create `docs/api/db.md` with Clear Examples

```markdown
# Database API

The Database API provides functions for interacting with the Arc Memory knowledge graph database.

## Connection Management

### `get_connection(db_path: Optional[Path] = None, check_exists: bool = True) -> sqlite3.Connection`

Get a connection to the database.

```python
from arc_memory.sql.db import get_connection
from pathlib import Path

# Connect to the default database
conn = get_connection()

# Connect to a specific database
conn = get_connection(Path("./my-graph.db"))

# Don't check if the file exists (useful for new databases)
conn = get_connection(Path("./new-graph.db"), check_exists=False)
```

### `ensure_connection(conn_or_path: Union[Any, Path, str]) -> sqlite3.Connection`

Ensure we have a valid database connection. This function accepts either an existing connection or a path.

```python
from arc_memory.sql.db import ensure_connection
from pathlib import Path

# From an existing connection
conn = ensure_connection(existing_conn)

# From a path
conn = ensure_connection(Path("./my-graph.db"))

# From a string path
conn = ensure_connection("./my-graph.db")
```
```

#### 2.4.2 Create a Troubleshooting Guide in `docs/guides/troubleshooting.md`

Add a section specifically for database connection issues:

```markdown
## Database Connection Issues

### PosixPath object has no attribute 'execute'

**Problem**: You're passing a Path object to a function that expects a database connection.

**Solution**:
1. Use `get_connection()` to get a connection from a path:
   ```python
   from arc_memory.sql.db import get_connection

   # Get a connection
   conn = get_connection(db_path)

   # Now use functions that expect a connection
   node = get_node_by_id(conn, "node:123")
   ```

2. Or use the new `ensure_connection()` function:
   ```python
   from arc_memory.sql.db import ensure_connection

   # This works with either a connection or a path
   conn = ensure_connection(db_path_or_conn)
   ```

3. Or use the high-level API functions that accept either:
   ```python
   from arc_memory.api import get_node

   # This works with either a connection or a path
   node = get_node(db_path_or_conn, "node:123")
   ```
```

### 2.5 Fix ADR Processing

#### 2.5.1 Improve Date Handling in `arc_memory/ingest/adr.py`

Enhance the date parsing logic (line 184-214):

```python
def parse_date(date_str: Any) -> Optional[datetime]:
    """Parse a date string into a datetime object.

    Args:
        date_str: The date string to parse.

    Returns:
        A datetime object, or None if parsing failed.
    """
    if not date_str:
        return None

    if not isinstance(date_str, str):
        logger.warning(f"Date is not a string: {date_str} (type: {type(date_str).__name__})")
        return None

    # Try different date formats
    date_formats = [
        "%Y-%m-%d",  # ISO format: 2023-11-15
        "%Y-%m-%dT%H:%M:%S",  # ISO format with time: 2023-11-15T14:30:00
        "%Y-%m-%dT%H:%M:%S.%f",  # ISO format with microseconds: 2023-11-15T14:30:00.123456
        "%Y/%m/%d",  # Slash format: 2023/11/15
        "%d-%m-%Y",  # European format: 15-11-2023
        "%d/%m/%Y",  # European slash format: 15/11/2023
        "%B %d, %Y",  # Month name format: November 15, 2023
        "%b %d, %Y",  # Abbreviated month format: Nov 15, 2023
    ]

    for date_format in date_formats:
        try:
            return datetime.strptime(date_str, date_format)
        except ValueError:
            continue

    # Try fromisoformat as a last resort
    try:
        return datetime.fromisoformat(date_str)
    except ValueError:
        logger.warning(
            f"Could not parse date: '{date_str}'. "
            f"Expected formats: YYYY-MM-DD, YYYY/MM/DD, DD-MM-YYYY, etc."
        )
        return None
```

### 2.6 Improve Error Messages

#### 2.6.1 Enhance Error Messages in `arc_memory/sql/db.py`

Update error messages to be more descriptive and actionable:

```python
# Example for get_node_by_id
except Exception as e:
    logger.error(f"Failed to get node by ID: {e}")
    raise GraphQueryError(
        f"Failed to get node by ID '{node_id}': {e}",
        details={
            "node_id": node_id,
            "error": str(e),
            "hint": "Make sure you're passing a valid database connection object, not a path."
        }
    )
```

## 3. Testing Plan

### 3.1 Unit Tests

Add the following tests:
- `tests/sql/test_connection_handling.py` - Test the new connection wrapper functions
- `tests/auth/test_github_fallback.py` - Test the GitHub authentication fallback mechanism
- `tests/ingest/test_adr_date_parsing.py` - Test the improved ADR date parsing

### 3.2 Integration Tests

Add integration tests that verify the entire workflow:
- `tests/integration/test_api_consistency.py` - Test the new API functions
- `tests/integration/test_error_messages.py` - Test that error messages are clear and actionable

## 4. Version Update

### 4.1 Update Version Number

Update to version 0.2.0 in:
- `pyproject.toml`
- `arc_memory/__init__.py`

### 4.2 Update CHANGELOG.md

```markdown
## [0.2.0] - 2025-05-01

### Added
- New `ensure_connection()` function to handle both connection objects and paths
- Database connection context manager for safer connection handling
- Fallback mechanism for GitHub authentication
- Comprehensive troubleshooting guide for common issues

### Fixed
- Inconsistent API design across database functions
- GitHub authentication issues with default client ID
- ADR date parsing problems
- Unclear error messages
- Documentation gaps for database connection handling
```

## 5. Developer Experience Considerations

When implementing these fixes, we need to prioritize the developer experience while maintaining the simplicity of the SDK. Here are the key principles to follow:

### 5.1 Prioritize Simplicity and Intuitiveness

- **Minimize Cognitive Load**: Developers shouldn't need to remember which functions take paths vs. connections
- **Consistent Patterns**: Use consistent patterns across the API to make the SDK predictable
- **Progressive Disclosure**: Simple use cases should be simple, complex use cases should be possible

### 5.2 Graceful Degradation

- **Core Functionality First**: Ensure the core functionality (Git-based knowledge graph) works even when optional features fail
- **Clear Fallbacks**: When GitHub authentication fails, provide a clear path forward
- **Informative Warnings**: Use warnings to inform users about limitations without blocking their workflow

### 5.3 Balanced Approach

Since Arc Memory SDK is still in beta and validating its concept, we should:

- **Fix Critical Issues**: Address the issues that block users from successfully using the SDK
- **Avoid Overengineering**: Don't introduce complex abstractions that might be hard to change later
- **Focus on Validation**: Make it easy for users to validate the core value proposition

## 6. Implementation Order

1. **Standardize Database Connection Handling** (Highest Priority)
   - Add `ensure_connection()` function to accept both paths and connections
   - Update core database query functions to use this wrapper
   - This addresses the most common error users encounter

2. **Fix GitHub Authentication with Graceful Fallback** (High Priority)
   - Verify and update default client ID
   - Add fallback mechanism to build graphs with just Git data
   - Add clear warnings when GitHub data is unavailable
   - This ensures users can still build useful knowledge graphs even without GitHub auth

3. **Improve Error Messages** (High Priority)
   - Make error messages more descriptive and actionable
   - Add troubleshooting hints to common errors
   - This helps users resolve issues without needing to read extensive documentation

4. **Enhance Documentation with Examples** (Medium Priority)
   - Update examples to show proper connection handling
   - Add troubleshooting section for common issues
   - This helps users understand how to use the SDK correctly

5. **Fix ADR Processing** (Medium Priority)
   - Improve date parsing with better error messages
   - This ensures ADRs are properly integrated into the knowledge graph

6. **Add Targeted Tests** (Medium Priority)
   - Focus on testing the new connection handling
   - Test the GitHub fallback mechanism
   - This ensures the fixes work as expected

7. **Update Version Number** (Low Priority)
   - Update version in pyproject.toml and __init__.py
   - Add entry to CHANGELOG.md
   - This communicates the improvements to users

This implementation plan addresses all the issues reported in GitHub Issue #6 with a focus on creating an ideal developer experience while maintaining the simplicity of the SDK. It prioritizes the most critical issues that block users from successfully using the SDK, while avoiding overengineering.
