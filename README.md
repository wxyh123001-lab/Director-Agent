# Director Agent

A fully automated multi-agent pipeline that turns a single sentence into a complete film production package — script, shooting style recommendations, AI image/video prompts, and formatted documents.

## What It Does

You type one sentence. The system does the rest:

```
"A cyberpunk love story set in neon-lit rain-soaked streets"
```

→ **Characters** with appearance, costume, and emotional state  
→ **Script** with scenes, dialogue, and action  
→ **Scene environments** with lighting, weather, time of day, and props  
→ **Shooting style** with camera directions, editing techniques, and filter recommendations  
→ **Three output files**: a structured JSON of AI prompts, a Markdown storyboard, and a Word document  

---

## Pipeline Architecture

The system uses [LangGraph](https://github.com/langchain-ai/langgraph) to orchestrate five agents as a directed acyclic graph. After the story is analyzed, the script and scene agents run **in parallel** to save time.

```
User Input (one sentence)
        │
        ▼
   [B Agent] Story Recognition
        │
        ├──────────────────────┐
        ▼                      ▼
  [C Agent]              [D Agent]
  Characters             Scenes &
  & Script               Environment
  (parallel)             (parallel)
        │                      │
        └──────────┬───────────┘
                   ▼
           [A Agent] Shooting Style
                   │
                   ▼
           [E Agent] Output Generation
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
   prompts.json  storyboard  storyboard
                   .md         .docx
```

---

## Agents

### B Agent — Story Recognition (`agents/b_story.py`)

Analyzes the user's input and extracts the foundational story elements that all other agents build on.

**Output:**
- `story_type` — Genre (romance, sci-fi, thriller, drama, etc.)
- `tone` — Emotional tone (warm, tense, melancholic, epic, etc.)
- `conflict` — Core conflict in one sentence
- `perspective` — Narrative point of view (first person, third person, multi-POV)

---

### C Agent — Characters & Script (`agents/c_script.py`)

Creates detailed character profiles and a full scene-by-scene script, receiving the story analysis from B Agent.

**Character output (per character):**
- `name` — Character name
- `background` — One-sentence backstory
- `appearance` — Physical description
- `costume` — Specific, visualizable clothing description
- `state` — Current emotional and physical condition

**Scene output (per scene):**
- `scene_id` — Scene number
- `title` — Scene title
- `characters` — List of characters present
- `dialogue` — Line-by-line dialogue with speaker attribution
- `action` — Stage directions and movement

---

### D Agent — Scenes & Environment (`agents/d_scene.py`)

Designs the physical world each scene takes place in. Runs in parallel with C Agent since both only depend on B Agent's output.

**Output (per scene):**
- `location` — Location name
- `background` — Detailed visual description of surroundings
- `time` — Time of day (dawn, noon, dusk, late night, etc.)
- `weather` — Atmosphere and weather conditions
- `lighting` — Lighting characteristics (color, direction, quality)
- `props` — Key props present in the scene

---

### A Agent — Shooting Style (`agents/a_style.py`)

After the script and scenes are both complete, this agent recommends how to shoot each scene. It reads from both C and D Agent outputs.

**Output:**
- `global_style` — Overall cinematographic style in one sentence
- Per scene:
  - `camera` — Shot type and camera movement (e.g., "low-angle tracking shot")
  - `editing_technique` — Cut style and pacing (e.g., "slow cuts synced to rain rhythm")
  - `filter_style` — Color grade and tone (e.g., "cold blue-teal, high contrast, light grain")

---

### E Agent — Output Generation (`agents/e_output.py`)

Collects all outputs and writes three files to `output/{timestamp}/`.

**`prompts.json`** — Structured data for AI generation tools:
```json
{
  "project": "...",
  "global_style_prompt": "...",
  "characters": [
    {
      "name": "Chen Ming",
      "prompt": "tall and lean, worn leather jacket with holographic goggles, state: exhausted but determined"
    }
  ],
  "scenes": [
    {
      "scene_id": 1,
      "description": "Neon street",
      "prompt": "neon street, dense high-rises with holographic billboards, late night, drizzle, cold blue light, camera: low-angle upward shot",
      "editing_technique": "slow cuts matching rain rhythm",
      "filter_style": "cold blue-teal, high contrast, light grain"
    }
  ]
}
```

**`storyboard.md`** — Full storyboard document with all scenes, dialogue, and shooting notes in Markdown.

**`storyboard.docx`** — Same content as Word document for sharing or printing.

---

## Installation

```bash
# Clone or navigate to the project
cd director_agent

# Install dependencies
pip install -r requirements.txt
```

**Requirements:**
- Python 3.10+
- `langgraph >= 0.2.0`
- `anthropic >= 0.40.0`
- `python-docx >= 1.1.0`

---

## Usage

**Set your Anthropic API key:**
```bash
export ANTHROPIC_API_KEY=your_api_key_here   # macOS / Linux
set ANTHROPIC_API_KEY=your_api_key_here      # Windows CMD
```

**Run with a custom prompt:**
```bash
python main.py "A cyberpunk love story in neon-lit rain-soaked streets"
```

**Run with the default prompt:**
```bash
python main.py
```

**Output:**
```
Starting: A cyberpunk love story in neon-lit rain-soaked streets

Generation complete! Files saved to:
  JSON : output/20260409_143021/prompts.json
  MD   : output/20260409_143021/storyboard.md
  DOCX : output/20260409_143021/storyboard.docx
```

---

## Use the Prompts

The `prompts.json` output is designed to feed directly into AI generation tools:

- **Character prompts** → Use in Midjourney, DALL-E, Stable Diffusion for consistent character images
- **Scene prompts** → Use in Runway, Kling, Sora for video generation
- **`editing_technique`** → Guide your editing software (cut timing, transitions)
- **`filter_style`** → Apply as a LUT or color grade in DaVinci Resolve / Premiere
- **`global_style_prompt`** → Use as the overarching style seed for the entire project

---

## Project Structure

```
director_agent/
├── main.py              # Entry point
├── graph.py             # LangGraph pipeline definition
├── state.py             # Shared state type (DirectorState)
├── requirements.txt
├── agents/
│   ├── b_story.py       # Story recognition
│   ├── c_script.py      # Characters and script
│   ├── d_scene.py       # Scene environments
│   ├── a_style.py       # Shooting style
│   ├── e_output.py      # File generation
│   └── utils.py         # JSON parsing utility
├── tests/               # Unit tests (22 tests, all passing)
└── output/              # Generated files (created at runtime)
```

---
