---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces and mobile apps with high design quality. Use this skill when the user asks to build web components, Flutter apps, gamified UI, artifacts, or aesthetics (examples include websites, dashboards, gamified habit trackers, mobile layouts, or when styling/beautifying any UI). Generates creative, polished code, and UI design (Web & Flutter) that avoids generic AI aesthetics.
license: Complete terms in LICENSE.txt
---

This skill guides creation of distinctive, production-grade frontend interfaces (Web & Mobile) that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

The user provides requirements: a component, page, mobile/web app, or interface to build. They may include context about the purpose, audience, or technical constraints.

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian.
- **Constraints**: Technical requirements (Web/React vs. Mobile/Flutter, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision.

## General Aesthetic Guidelines

- **Typography**: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial, Roboto (unless requested), and Inter. Pair a distinctive display font with a refined body font.
- **Color & Theme**: Commit to a cohesive aesthetic. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Generous negative space OR controlled density.
- **Backgrounds**: Create atmosphere. Gradient meshes, noise textures, geometric patterns, layered transparencies, glassmorphism.

## Flutter & Mobile Gamification

For Flutter/Mobile requests, especially those inspired by gamified apps (Forest, Habitica, Flo), prioritize **"Juiciness"**—interfaces that feel alive, responsive, and rewarding.

### 1. Gamification Archetypes
Draw inspiration from specific industry patterns:
- **The "Organic Growth" (Forest-style)**:
    - **Metaphor**: Progress = Life. Use visual representations of growth (plants, buildings, creatures) that evolve with user action.
    - **Focus Mode**: deeply immersive "Isolation" screens that hide clutter to enforce focus.
    - **Loss Aversion**: Visual feedback for failure (withered plants, lost streaks) to encourage consistency.
- **The "RPG" (Habitica-style)**:
    - **Avatar-Centric**: The user *is* a character. prominent visualizations of HP, XP, and Level bars.
    - **Inventory/Rewards**: Grid layouts for collectables. Modal popups for "Loot Cords" with particle effects.
    - **Pixel/Stylized Art**: Don't be afraid of non-standard art styles (8-bit, hand-drawn) to distinguish from corporate apps.
- **The "Empathetic Dashboard" (Flo-style)**:
    - **Soft Personalization**: Use rounded corners, pastel/organic color palettes (soft pinks, sage greens), and approachable typography.
    - **Interactive "Stories"**: Use full-screen, tappable story cards for education or daily summaries.
    - **Data Storytelling**: Smooth, animated bezier curves for charts. Don't just show numbers; show trends with friendly visuals.

### 2. Flutter Implementation Details
- **Animations**: Crucial for gamification.
    - Use `flutter_animate` for declarative entrance/exit effects.
    - Use `Rive` or `Lottie` for complex, state-driven assets (e.g., a tree that actually grows, a chest that opens).
    - **Micro-interactions**: Everything must react. Buttons scale down on press. List items slide in. Confetti triggers on completion (`confetti` package).
- **Navigation**: Custom `PageRouteBuilder` transitions. Don't use default slide transitions; use scales, fades, or morphs that fit the game theme.
- **Haptics**: `HapticFeedback.lightImpact()` on tap; `mediumImpact()` on success; `heavyImpact()` on error/level-up.
- **Glassmorphism**: Use `BackdropFilter` with `ImageFilter.blur` for modern, layered UI depth.

## Web Aesthetic Details
- **Motion**: Prioritize CSS-only solutions. One well-orchestrated page load with staggered reveals creates delight.
- **Layout**: Grid-breaking elements. Asymmetry.
- **Visuals**: CSS gradients, `backdrop-filter`, box-shadow layering.

## Anti-Patterns (What to Avoid)
- **Generic AI Style**: Overused simple gradients (purple/blue), standard Material Design guidelines without customization, "Corporate Memphis" art styles.
- **Static Interfaces**: UI that doesn't react to touch/hover.
- **Placeholders**: Never use "Lorem Ipsum" or gray boxes. Generate thematic content.

Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations. Minimalist designs need restraint and precision.
