# Arc Memory Revised Implementation Plan

This document outlines a focused, streamlined implementation plan for Arc Memory, prioritizing immediate value delivery with minimal friction.

## Strategic Vision

Arc's core value proposition is helping developers understand the "why" behind code changes by connecting code to its full context and history. This plan focuses on delivering this value in the simplest, most direct way possible.

## User Research Insights

Our user research has revealed several key insights that inform this implementation plan:

| Theme | Evidence | Impact on Implementation |
|-------|----------|--------------------------|
| **MTTR is the undisputed North-Star metric** | "Hours → minutes is the dream", mentioned ~10× in user interviews | Focus on measuring and improving MTTR; add timestamp capture in telemetry |
| **Manual log correlation is a pain point** | "Insane... slow... error-prone... bash scripts hitting multiple APIs" | Prioritize unified log-to-diff timeline in future phases |
| **Context is splintered across tools** | Out-of-date Notion runbooks, Slack threads, comments | Reinforce VS Code hover as key deliverable; plan for ADR + Slack integration |
| **Copilot doubled PR volume creating tech debt** | "PRs roughly double... people merge code they don't fully understand" | Position Arc as safety net for AI code surge |
| **Onboarding takes 3 months** | Pain acknowledged, secondary to MTTR | Secondary KPI: days-to-first-prod-merge |
| **Incidents cost ~$13k** | $13k direct ($10k spend + $3k eng-hours) for a mid-tier bug; MTTR=3h | Provides ROI calculation: "Arc aims to save 60% of that" |
| **Budget is $500-750k/yr** | Start with small squad pilot → expand | Validates land-and-expand strategy |
| **Adoption requires < 1 hour to value** | Minimal DevOps lift, RBAC, self-host/VPC, provenance/audit | Keep installation simple; document install <15 min |

## Implementation Priorities

### Phase 1: Core CLI Enhancements (1 week)

#### 1. `arc why` Command (2 days)
A user-friendly wrapper around the existing trace functionality with improved output formatting.

```python
@app.command()
def why(
    file_path_with_line: str = typer.Argument(..., help="Path to the file and line number (e.g., src/main.py:42)"),
    max_results: int = typer.Option(3, "--max-results", "-m", help="Maximum number of results to return"),
    max_hops: int = typer.Option(2, "--max-hops", "-h", help="Maximum number of hops in the graph traversal"),
    json_format: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    debug: bool = typer.Option(False, "--debug", help="Enable debug logging"),
) -> None:
    """Show the decision trail for a specific line in a file."""
    # Parse file path and line number
    try:
        file_path, line_number = file_path_with_line.rsplit(":", 1)
        line_number = int(line_number)
    except ValueError:
        console.print("[red]Invalid format. Use 'file_path:line_number' (e.g., src/main.py:42)[/red]")
        sys.exit(1)

    # Get trace data
    from arc_memory.trace import trace_history_for_file_line
    trace_data = trace_history_for_file_line(
        file_path=file_path,
        line_number=line_number,
        max_results=max_results,
        max_hops=max_hops
    )

    # If no results found, display a message and exit
    if not trace_data:
        console.print(f"[yellow]No decision trail found for {file_path}:{line_number}[/yellow]")
        sys.exit(0)

    # Format and display results
    if json_format:
        print(json.dumps(trace_data))
    else:
        display_why_results_rich(trace_data, file_path, line_number)

def display_why_results_rich(trace_data, file_path, line_number):
    """Display trace results in a rich, formatted way."""
    console.print(f"[bold]Decision Trail for [cyan]{file_path}:{line_number}[/cyan][/bold]\n")

    for i, event in enumerate(trace_data):
        event_type = event.get("type", "Unknown")
        title = event.get("title", "Untitled")
        id = event.get("id", "")
        date = event.get("date", "")
        author = event.get("author", "")
        url = event.get("url", "")

        # Determine icon and color based on event type
        icon, color = get_event_icon_and_color(event_type)

        # Print event header
        console.print(f"{i+1}. [{color}]{icon} {event_type}:[/{color}] [bold]{title}[/bold]")

        # Print metadata
        metadata = []
        if id:
            metadata.append(f"[dim]ID:[/dim] {id}")
        if date:
            metadata.append(f"[dim]Date:[/dim] {date}")
        if author:
            metadata.append(f"[dim]Author:[/dim] {author}")

        if metadata:
            console.print("   " + " | ".join(metadata))

        # Print URL if available
        if url:
            console.print(f"   [link={url}]{url}[/link]")

        # Print body if available
        body = event.get("body", "")
        if body:
            # Truncate and format body
            if len(body) > 200:
                body = body[:197] + "..."
            console.print(f"   [dim]{body}[/dim]")

        # Add separator between events
        if i < len(trace_data) - 1:
            console.print("")

def get_event_icon_and_color(event_type):
    """Get appropriate icon and color for event type."""
    event_type = event_type.lower()
    if "commit" in event_type:
        return "📝", "green"
    elif "pull" in event_type or "pr" in event_type:
        return "🔀", "blue"
    elif "issue" in event_type:
        return "🐛", "red"
    elif "adr" in event_type or "decision" in event_type:
        return "📋", "yellow"
    elif "comment" in event_type or "discussion" in event_type:
        return "💬", "purple"
    else:
        return "ℹ️", "cyan"
```

#### 2. `arc relate` Command (1 day)
Show nodes related to a specific entity with clear relationship information.

```python
@app.command()
def relate(
    entity_id: str = typer.Argument(..., help="Entity ID to find related nodes for"),
    max_results: int = typer.Option(5, "--max-results", "-m", help="Maximum number of results to return"),
    relationship_type: str = typer.Option(None, "--type", "-t", help="Filter by relationship type"),
    json_format: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    debug: bool = typer.Option(False, "--debug", help="Enable debug logging"),
) -> None:
    """Show nodes related to a specific entity."""
    configure_logging(debug=debug)

    try:
        # Get the database path
        from arc_memory.sql.db import ensure_arc_dir, get_connection
        arc_dir = ensure_arc_dir()
        db_path = arc_dir / "graph.db"

        # Get related nodes
        conn = get_connection(db_path)
        related_nodes = get_related_nodes(conn, entity_id, max_results, relationship_type)

        # Output based on format
        if json_format:
            print(json.dumps(related_nodes))
        else:
            # Display in a rich table
            table = Table(title=f"Nodes related to {entity_id}")
            table.add_column("Type", style="cyan")
            table.add_column("ID", style="green")
            table.add_column("Title", style="white")
            table.add_column("Relationship", style="yellow")

            for node in related_nodes:
                table.add_row(
                    node["type"],
                    node["id"],
                    node["title"],
                    node["relationship"]
                )

            console.print(table)

    except Exception as e:
        logger.exception("Error in relate command")
        error_msg = f"Error: {e}"
        if json_format:
            print(error_msg, file=sys.stderr)
        else:
            console.print(f"[red]{error_msg}[/red]")
        sys.exit(1)
```

#### 3. Simple `arc serve` Command (0.5 day)
A minimal wrapper around the existing MCP server.

```python
@app.command()
def serve(
    host: str = typer.Option("127.0.0.1", "--host", help="Host to bind the server to"),
    port: int = typer.Option(8000, "--port", "-p", help="Port to bind the server to"),
    stdio: bool = typer.Option(False, "--stdio", help="Use stdio mode instead of HTTP"),
    debug: bool = typer.Option(False, "--debug", help="Enable debug mode"),
) -> None:
    """Serve the knowledge graph via MCP protocol."""
    try:
        # Check if arc-mcp-server is installed
        import importlib.util
        has_mcp_server = importlib.util.find_spec("arc_mcp_server") is not None

        if not has_mcp_server:
            console.print("[yellow]arc-mcp-server not found. Installing...[/yellow]")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "arc-mcp-server"])

        # Build the command
        cmd = [sys.executable, "-m", "arc_mcp_server"]
        if host != "127.0.0.1":
            cmd.extend(["--host", host])
        if port != 8000:
            cmd.extend(["--port", str(port)])
        if stdio:
            cmd.append("--stdio")
        if debug:
            cmd.append("--debug")

        # Run the MCP server as a subprocess
        console.print(f"[green]Starting Arc MCP Server{'in stdio mode' if stdio else f'on {host}:{port}'}...[/green]")
        subprocess.run(cmd)

    except Exception as e:
        logger.exception("Error starting MCP server")
        console.print(f"[red]Error starting MCP server: {e}[/red]")
        sys.exit(1)
```

#### 4. MTTR-Focused Telemetry with PostHog (1 day)
Add opt-in telemetry to track command usage and measure MTTR improvements using PostHog.

```python
import time
import uuid
import threading
from typing import Dict, Any, Optional, Type

def track_command_usage(command_name: str, success: bool = True, error: Optional[Exception] = None,
                        session_id: Optional[str] = None, context: Optional[Dict[str, Any]] = None) -> None:
    """Track command usage if telemetry is enabled."""
    try:
        # Check if telemetry is enabled
        from arc_memory.config import get_config
        config = get_config()
        if not config.get("telemetry", {}).get("enabled", False):
            return

        # Get installation ID (anonymous)
        installation_id = config.get("telemetry", {}).get("installation_id", "unknown")

        # Get or create session ID for tracking investigation sessions (MTTR)
        if session_id is None:
            session_id = config.get("telemetry", {}).get("current_session_id")
            if session_id is None:
                # Create new session ID if none exists
                session_id = str(uuid.uuid4())
                # Store in config for future commands in this session
                config["telemetry"]["current_session_id"] = session_id
                config.save()

                # Track session start for MTTR calculation
                track_session_event("session_start", session_id)

        # Prepare properties
        properties = {
            "command": command_name,
            "success": success,
            "error_type": error.__class__.__name__ if error else None,
            "version": arc_memory.__version__,
            "session_id": session_id
        }

        # Add context if provided (file path, line number, etc.)
        if context:
            properties.update(context)

        # Send telemetry in background thread
        threading.Thread(
            target=send_posthog_event,
            args=(installation_id, f"command_{command_name}", properties),
            daemon=True
        ).start()
    except Exception:
        # Never let telemetry errors affect the user
        pass

def track_session_event(event_type: str, session_id: str) -> None:
    """Track session events for MTTR calculation."""
    try:
        from arc_memory.config import get_config
        config = get_config()
        installation_id = config.get("telemetry", {}).get("installation_id", "unknown")

        properties = {
            "session_id": session_id,
            "timestamp": time.time()
        }

        # Send telemetry in background thread
        threading.Thread(
            target=send_posthog_event,
            args=(installation_id, event_type, properties),
            daemon=True
        ).start()
    except Exception:
        pass

def send_posthog_event(distinct_id: str, event_name: str, properties: Dict[str, Any]) -> None:
    """Send telemetry event to PostHog."""
    try:
        # Lazy import PostHog to avoid dependency issues
        from posthog import Posthog

        # Initialize PostHog client
        # Project API key would be set via environment variable in production
        posthog = Posthog(
            project_api_key="phc_YOUR_PROJECT_KEY",
            host="https://app.posthog.com",  # Or your self-hosted instance
            disable_geoip=True  # Don't track server IP location
        )

        # Capture the event
        posthog.capture(
            distinct_id=distinct_id,
            event=event_name,
            properties=properties
        )

        # Ensure event is sent (important in serverless environments)
        posthog.flush()
    except Exception:
        # Silently ignore any errors
        pass

def end_investigation_session() -> None:
    """End the current investigation session for MTTR calculation."""
    try:
        from arc_memory.config import get_config
        config = get_config()
        session_id = config.get("telemetry", {}).get("current_session_id")

        if session_id:
            # Track session end for MTTR calculation
            track_session_event("session_end", session_id)

            # Clear session ID
            config["telemetry"]["current_session_id"] = None
            config.save()
    except Exception:
        pass
```

This telemetry implementation focuses on measuring MTTR by tracking investigation sessions from start to finish. It uses PostHog as the analytics platform, which provides powerful visualization and analysis capabilities with the following benefits:

1. **Simple Integration**: PostHog's Python SDK is easy to integrate and well-maintained
2. **Flexible Deployment**: Can use PostHog Cloud or self-host if needed
3. **Feature-Rich**: Includes event tracking, user identification, and feature flags
4. **Privacy-Focused**: Allows disabling GeoIP tracking and other privacy controls
5. **Open Source**: The entire PostHog platform is open source

#### 5. Documentation and Polish (1.5 days)
- Comprehensive documentation with examples
- Error handling improvements
- Installation guide optimization (<15 min to first output)
- README updates with ROI calculation example
- Dual installation options:
  - Standard pip install (primary method)
  - Docker container (for enterprise users)

### Phase 2: VS Code Extension Updates (1 week)

#### 1. Hover Card Enhancements (3 days)
- Update to use the new CLI commands
- Improve UI based on user feedback
- Optimize performance
- Focus on surfacing "decision diff" context
- Position as safety net for AI-generated code

#### 2. Testing and Reliability (2 days)
- End-to-end testing
- Error handling improvements
- Performance optimization

#### 3. Documentation and Examples (1 day)
- Update documentation
- Add GIFs and screenshots
- Create quickstart guide

### Phase 3: User Feedback & Iteration (Ongoing)
1. Collect user feedback on core functionality
2. Iterate based on feedback
3. Consider more advanced features based on user needs

## Success Metrics

### Primary Metric: MTTR Improvement

Our primary success metric is improvement in Mean Time To Resolution (MTTR) for incidents and investigations. Based on user research, reducing MTTR from hours to minutes is "the dream" and would justify investment in Arc.

| Current State | Target with Arc | Measurement Method |
|---------------|----------------|-------------------|
| MTTR = 3 hours | MTTR = 1-1.5 hours (50-60% reduction) | Telemetry session tracking + user interviews |

### Feature-Specific Success Signals

| Feature | Success Signal |
|---------|----------------|
| `arc why` | First design partner copies output into Slack during incident |
| `arc relate` | Used by VS Code hover to show "related ADR/PR" |
| `arc serve` | README quickstart works end-to-end |
| Documentation | New user <15 min to first output |
| Telemetry | See usage graph in Amplitude |

### Secondary Metrics

| Metric | Current State | Target with Arc |
|--------|--------------|----------------|
| Onboarding time | 3 months | 2 months (33% reduction) |
| Days to first prod merge | Varies | 20% reduction |
| Incident cost | ~$13k per incident | ~$5.2k per incident (60% reduction) |

## Deferred Features

These features are intentionally deferred until we have usage data and clear demand:

1. **LLM Integration**
   - Will be added as an opt-in feature after core functionality is solid
   - Initially will be a separate command (`arc ask`) rather than integrated into `why`

2. **Vector Search**
   - Will be added as an optional enhancement after we see how users interact with basic search

3. **Dashboard UI**
   - Will be considered based on user feedback and specific use cases

4. **Unified CLI/MCP Architecture**
   - Will be evaluated after we have telemetry on actual MCP usage

5. **Log Integration**
   - Integration with Datadog, Simulogic, and Redis logs
   - Unified log-to-diff timeline
   - Will be prioritized in next phase based on user research

6. **RBAC and Air-Gap Deployment**
   - Enterprise security features
   - Will be added to roadmap after initial adoption

## Rationale

This streamlined implementation plan:

1. **Focuses on MTTR Reduction**:
   - Directly addresses the #1 pain point from user research
   - Delivers verifiable provenance in one command and one hover
   - Prioritizes features that directly support the "why" behind code changes

2. **Minimizes Friction**:
   - Keeps the CLI pure local with no network dependencies
   - Ensures <1-hour to value for new users
   - Provides both pip and Docker installation options

3. **Separates Concerns**:
   - Maintains the CLI as a simple, direct interface to the knowledge graph
   - Keeps MCP as an opt-in power feature via `arc serve`
   - Avoids premature architecture complexity

4. **Enables Rapid Feedback**:
   - Gets the product in users' hands quickly
   - Provides clear success signals to validate the approach
   - Includes telemetry to measure MTTR improvement

5. **Addresses Real User Pain Points**:
   - Tackles context fragmentation with VS Code hover
   - Positions as safety net for AI-generated code
   - Provides ROI calculation based on incident cost reduction

6. **Preserves Future Options**:
   - Allows for more sophisticated features to be added based on real usage data
   - Doesn't commit to architectural decisions before we have evidence
   - Sets up clear path for enterprise features

## Conclusion

This revised plan focuses on delivering immediate value with minimal friction while directly addressing the key pain points identified in user research. By prioritizing a thin CLI that talks directly to the SQLite temporal knowledge graph, we can provide the "aha moment" for users within minutes of installation.

The implementation is laser-focused on reducing MTTR—the undisputed North Star metric from our research—with a clear path to demonstrating ROI through incident cost reduction. The VS Code extension builds on this foundation to provide contextual information directly in the editor, addressing the pain of fragmented context across tools.

By keeping the initial implementation simple and focused on core value, we can:
1. Get to market faster with our core value proposition
2. Collect user feedback on the most important features
3. Avoid overwhelming new users with complexity
4. Reduce maintenance burden and dependency issues
5. Make informed decisions about future features based on real usage data

This approach positions Arc as a critical tool for engineering teams, particularly in the era of AI-generated code where understanding the "why" behind changes is more important than ever.
