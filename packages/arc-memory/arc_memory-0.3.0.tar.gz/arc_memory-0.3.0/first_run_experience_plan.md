# Arc Memory CLI First-Run Experience Plan

This document outlines a comprehensive first-run experience for Arc Memory CLI, designed to provide immediate value to users and create compelling visual material for screenshots and social proof.

## Design Inspiration

The first-run experience will draw inspiration from the VS Code extension's visual design:
- Clean, terminal-friendly UI with clear visual hierarchy
- Table-based decision trail presentation
- Graph-like visualization of related nodes
- Color-coding by entity type (PR, Issue, ADR, Commit)
- Command prompt integration

## Complete First-Run Flow

### 1. Authentication

```
$ arc auth gh

🔑 Authenticating with GitHub...

Please visit: https://github.com/login/device
And enter the code: ABCD-1234

[⏳ Waiting for authentication...]

✅ Authentication successful! Token stored in system keyring.

🔍 Arc Memory can now access GitHub data for your repositories.
```

### 2. Initial Build with Clear Expectations

```
$ arc build

📊 Building knowledge graph...

⏳ Analyzing Git repository...
  ✓ Processed 1,250 commits (25%)

⏳ Fetching GitHub data...
  ✓ Retrieved 150 PRs and 200 issues (60%)

⏳ Processing ADRs...
  ✓ Found 12 architecture decision records (85%)

⏳ Building relationships...
  ✓ Created 3,750 connections (100%)

✅ Build complete! Knowledge graph created with:
   • 1,250 nodes (commits, PRs, issues, files)
   • 3,750 connections between entities
   • 6 months of engineering history

🎉 Your knowledge graph is ready to explore!
```

### 3. First Insight - Decision Trail

```
┌─────────────────────────────────────────────────────────────┐
│ ✨ Welcome to Arc Memory! ✨                                 │
└─────────────────────────────────────────────────────────────┘

📂 Recently Modified: src/auth.py
   Last changed by: Jane Smith (2 days ago)

┌─────────────────────────── Decision Trail ──────────────────────────┐
│ Type   │ Title                        │ Date                        │
├────────┼──────────────────────────────┼─────────────────────────────┤
│ Commit │ Fix OAuth token rotation     │ Apr 28, 2025 (2 days ago)   │
├────────┼──────────────────────────────┼─────────────────────────────┤
│ PR     │ Decouple JWT rotation        │ Apr 28, 2025                │
├────────┼──────────────────────────────┼─────────────────────────────┤
│ Issue  │ BE-912 perf rewrite          │ Apr 25, 2025                │
├────────┼──────────────────────────────┼─────────────────────────────┤
│ ADR    │ Token cache strategy         │ Mar 15, 2025                │
└────────┴──────────────────────────────┴─────────────────────────────┘
                    (↓ expand, ↑ open in editor)

💡 This shows you the complete history behind this code - who wrote it,
   why it was created, and how it evolved over time.
```

### 4. Related Nodes Visualization

```
┌─────────────────────── Related Nodes ───────────────────────┐
│                                                             │
│                  ┌─────────────────┐                        │
│                  │  commit 9a8b3…  │                        │
│                  └────────┬────────┘                        │
│                           │                                 │
│                           ▼                                 │
│                  ┌─────────────────┐                        │
│                  │    PR #105      │                        │
│                  └────────┬────────┘                        │
│                           │                                 │
│              ┌────────────┴────────────┐                    │
│              │                         │                    │
│              ▼                         ▼                    │
│     ┌─────────────────┐      ┌─────────────────┐           │
│     │     PR #128     │      │    Issue #912   │           │
│     └─────────────────┘      └─────────────────┘           │
│                                                             │
└─────────────────────────────────────────────────────────────┘

🔍 This visualization shows how different entities are connected.
```

### 5. Interactive Command Prompt

```
arc> why src/auth.py:42

[Command output would appear here, similar to the decision trail above]

arc> relate node commit:9a8b3

[Command output would show related nodes, similar to the visualization above]
```

### 6. Guided Next Steps

```
🚀 What would you like to do next?

1. Explore another file
   arc why file <path> <line>

2. See what's related to an entity
   arc relate node <entity_id>

3. Serve the knowledge graph to AI assistants
   arc serve start

4. Learn more about Arc Memory
   arc help

💡 Pro tip: Run 'arc build --incremental' regularly to keep your
   knowledge graph up to date with minimal processing time.
```

## Implementation Approach

### 1. Leveraging Existing Functionality

- Use existing `arc why` and `arc relate` commands
- Capture and format their output for the first-run experience
- Use Git integration to identify recently modified files
- Use existing telemetry to track first-run completion

### 2. Terminal UI Enhancements

- Use Rich library's Tables, Panels, and formatting
- Create ASCII/Unicode-based graph visualization
- Use color coding consistent with VS Code extension
- Implement simple interactive elements

### 3. First-Run Detection

- Add a "first_run" flag in the configuration
- Show enhanced output only on first run
- Provide a way to replay the experience (`arc demo`)

### 4. Minimal Code Changes

- Focus on presentation layer, not core functionality
- Wrap existing commands rather than creating new ones
- Use existing data structures and models

## User Education Elements

1. **Contextual Explanations**: Brief explanations of what users are seeing
2. **Visual Cues**: Icons and formatting to highlight important information
3. **Command Examples**: Clear examples of how to use commands
4. **Progressive Disclosure**: Start simple, then introduce more complex features
5. **Pro Tips**: Sprinkled throughout to help users get the most value

## Social Proof and Marketing Materials

This first-run experience will provide excellent material for:

1. **Screenshots**: Clean, visually appealing terminal output
2. **GIFs**: The complete flow from auth to build to insights
3. **Video Demos**: Narrated walkthrough of the first-run experience
4. **Blog Posts**: "Getting started with Arc Memory in 5 minutes"
5. **Social Media**: Before/after comparisons of debugging with and without Arc

## Success Metrics

We'll measure the success of this first-run experience by tracking:

1. **Completion Rate**: % of users who complete the entire first-run flow
2. **Command Usage**: Which commands users try after the guided experience
3. **Retention**: % of users who run incremental builds after initial setup
4. **Time to Value**: How quickly users go from installation to first insight

## Next Steps

1. Implement the enhanced first-run experience
2. Create marketing materials using screenshots and recordings
3. Gather feedback from early users
4. Iterate based on telemetry and feedback
