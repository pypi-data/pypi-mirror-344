# Streamlit tldraw

A Streamlit component that integrates the tldraw whiteboard library for creating diagrams, system designs, ER diagrams and more. This component uses the latest tldraw v2 API.

![Streamlit tldraw Demo](https://raw.githubusercontent.com/Mr-Dark-debug/streamlit-tldraw/main/demo.png)

## Installation

```bash
pip install streamlit-tldraw
```

## Quick Start

```python
import streamlit as st
from streamlit_tldraw import st_tldraw

st.title("tldraw in Streamlit")

# Basic usage
result = st_tldraw(key="my_canvas")

# Display the result
if result:
    st.write("Canvas data:", result)
```

## Usage

```python
import streamlit as st
from streamlit_tldraw import st_tldraw

st.title("tldraw in Streamlit")

# Basic usage
result = st_tldraw(key="my_canvas")

# Advanced usage with options
result = st_tldraw(
    key="advanced_canvas",
    width=800,
    height=600,
    read_only=False,
    dark_mode=True,
    show_ui=True,
)

# Display the result
if result:
    st.write("Canvas data:", result)
```

## Parameters

- `key` (str, optional): A unique key for the component instance.
- `width` (int, optional): The width of the canvas in pixels. Defaults to container width.
- `height` (int, default 600): The height of the canvas in pixels.
- `read_only` (bool, default False): Whether the canvas should be in read-only mode.
- `dark_mode` (bool, default False): Whether to use dark mode.
- `show_ui` (bool, default True): Whether to show the UI elements (toolbar, menu).
- `initial_data` (dict, optional): Initial data to load into the canvas.

## Return Value

The component returns a dictionary containing:

- `snapshot`: The current state of the canvas
- `type`: The type of event ('mounted' or 'document_change')

## Features

- **Infinite Canvas**: Create diagrams on an infinite canvas with pan and zoom.
- **Rich Tools**: Draw shapes, add text, create arrows, and more.
- **Styling Options**: Customize colors, line styles, and text formatting.
- **Real-time Data**: All changes are sent back to Streamlit in real-time.
- **Dark Mode**: Switch between light and dark themes.
- **Read-only Mode**: Display diagrams without allowing edits.
- **UI Visibility Control**: Show or hide the toolbar and menu.
- **Initial Data Loading**: Load pre-existing diagrams.

## What's New in v0.1.3

- Fixed issue with updates not being sent back to Streamlit
- Improved dark mode implementation
- Enhanced read-only mode functionality
- Fixed UI visibility toggle
- Better error handling and debugging
- Improved initial data loading

## Examples

Check out the included example.py for a full demonstration:

```bash
streamlit run path/to/streamlit_tldraw/example.py
```

Or try the simple test.py:

```bash
streamlit run path/to/streamlit_tldraw/test.py
```

## Development

For development instructions, see [DEV_README.md](DEV_README.md).

## License

MIT