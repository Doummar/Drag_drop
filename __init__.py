# Drag Drop
# Created by Adel Aitah
# GitHub: https://github.com/Doummar/Drag_drop
# Copyright (c) 2026 Adel Aitah — All rights reserved

"""
Drag Drop — Anki visual labeling & category sorting addon
Interactive drag-and-drop image labeling and category sorting with visual placement studio,
clean feedback, light/dark mode support, and minimalistic design.
"""

import os
import re
from typing import List, Dict, Optional, Tuple

from anki.hooks import addHook
from aqt import mw, gui_hooks
from aqt.qt import *
from aqt.utils import showInfo, tooltip
from aqt.editor import Editor

ADDON_NAME = "Drag Drop"
ADDON_AUTHOR = "Adel Aitah"
ADDON_VERSION = "1.3.0"
ADDON_URL = "https://github.com/Doummar/Drag_drop"

# Note Type 1: Image Labeling
NOTE_TYPE_NAME = "Drag drop Image"
LEGACY_NAMES = ["Drag & Drop Image (DDI)", "DragDrop Image", "Drag & Drop Image"]
FIELDS = ["Title", "Question", "Image", "Labels", "Zones", "Layout", "Extra", "Front Audio", "Back Audio", "Front Image", "Back Image"]

BASE_CSS = """:root {
  --bg: #ffffff;
  --fg: #1c1c1c;
  --muted: #8e8e93;
  --border: #e2e8f0;
  --surf: #f8fafc;
  --ok: #059669;
  --err: #dc2626;
  --warn: #d97706;
  --accent: #2563eb;
  --font: -apple-system, BlinkMacSystemFont, \"Segoe UI\", Roboto, Helvetica, Arial, sans-serif;
  --r: 8px;
}

/* Explicit Light Mode in Anki */
/* ==========================================================================
   THEME VARIABLES & ADAPTIVE STYLES
   ========================================================================== */

:root,
html:not(.night_mode):not(.nightMode),
body:not(.night_mode):not(.nightMode),
.card:not(.night_mode):not(.nightMode) {
  --bg: #ffffff;
  --fg: #1c1c1c;
  --muted: #8e8e93;
  --border: #e2e8f0;
  --surf: #f8fafc;
  --ok: #059669;
  --err: #dc2626;
  --warn: #d97706;
  --accent: #2563eb;
  
  /* Adaptive Chips: Light Mode (Clean Minimal Default) */
  --chip-placed-bg: #ffffff;
  --chip-placed-fg: #0f172a;
  --chip-placed-border: #94a3b8;
  --chip-ok-bg: #ffffff;
  --chip-ok-fg: #0f172a;
  --chip-ok-border: #94a3b8;
  --chip-err-bg: #ffffff;
  --chip-err-fg: #0f172a;
  --chip-err-border: #94a3b8;
  --chip-miss-bg: #ffffff;
  --chip-miss-fg: #15803d;
  --chip-miss-border: #94a3b8;
  --chip-wrong-strike: #64748b;
  --chip-correct-fg: #15803d;
  --dz-empty-border: rgba(148, 163, 184, 0.75);
  --dz-empty-bg: rgba(255, 255, 255, 0.6);
}

/* Automatic Anki Dark/Night Mode Detection */
html.night_mode,
html.nightMode,
html[data-theme=\"dark\"],
html[data-night-mode=\"true\"],
.night_mode,
.nightMode,
.night_mode #qa,
.nightMode #qa,
body.night_mode,
body.nightMode,
:root.night_mode,
:root.nightMode,
.card.night_mode,
.card.nightMode {
  --bg: #18181b !important;
  --fg: #f4f4f5 !important;
  --muted: #a1a1aa !important;
  --border: #27272a !important;
  --surf: #27272a !important;
  --ok: #10b981 !important;
  --err: #ef4444 !important;
  --warn: #f59e0b !important;
  --accent: #3b82f6 !important;

  /* Adaptive Chips: Dark Mode (Clean Minimal Default) */
  --chip-placed-bg: #22242a !important;
  --chip-placed-fg: #f1f5f9 !important;
  --chip-placed-border: #3f3f46 !important;
  --chip-ok-bg: #22242a !important;
  --chip-ok-fg: #f1f5f9 !important;
  --chip-ok-border: #3f3f46 !important;
  --chip-err-bg: #22242a !important;
  --chip-err-fg: #f1f5f9 !important;
  --chip-err-border: #3f3f46 !important;
  --chip-miss-bg: #22242a !important;
  --chip-miss-fg: #4ade80 !important;
  --chip-miss-border: #52525b !important;
  --chip-wrong-strike: #94a3b8 !important;
  --chip-correct-fg: #4ade80 !important;
  --dz-empty-border: rgba(113, 113, 122, 0.7) !important;
  --dz-empty-bg: rgba(0, 0, 0, 0.4) !important;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html, body {
  height: auto !important;
  min-height: 100% !important;
  margin: 0 !important;
  padding: 0 !important;
  display: block !important;
  overflow-y: auto !important;
  background: var(--bg);
  color: var(--fg);
}

.card {
  min-height: 100vh !important;
  height: auto !important;
  display: flex !important;
  flex-direction: column !important;
  justify-content: flex-start !important;
  align-items: center !important;
  padding-top: 24px !important;
  margin: 0 !important;
  box-sizing: border-box !important;
  font-family: var(--font);
  background: var(--bg);
  color: var(--fg);
  font-size: 15px;
  line-height: 1.55;
  width: 100%;
}

/* Midcenter mode: Visually centered on screen with stable top anchor to prevent vertical jump */
body.midcenter,
html.midcenter,
.card.midcenter {
  min-height: 100vh !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: flex-start !important;
  padding-top: max(24px, calc(48vh - 330px)) !important;
  padding-bottom: 48px !important;
}

.ddi-wrap {
  width: 100%;
  max-width: 920px;
  margin: 0 auto;
  padding: 0 16px 48px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  text-align: center;
  box-sizing: border-box;
}

.upper-locked {
  width: 100% !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: flex-start !important;
  flex-shrink: 0 !important;
  flex-grow: 0 !important;
  contain: layout paint !important;
  position: relative !important;
  box-sizing: border-box !important;
}

.lower-flexible {
  width: 100% !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: flex-start !important;
  flex-grow: 1 !important;
  flex-shrink: 0 !important;
  position: relative !important;
  box-sizing: border-box !important;
  contain: layout !important;
}

.meta {
  width: 100%;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.09em;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 6px;
  text-align: center;
}

.question {
  width: 100%;
  font-size: 22px;
  font-weight: 700;
  margin-bottom: 18px;
  line-height: 1.3;
  text-align: center;
}

.img-arena {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 16px;
  flex-shrink: 0;
  box-sizing: border-box;
  contain: layout;
}

.img-box {
  position: relative;
  display: inline-block;
  width: auto;
  max-width: 100%;
  max-height: 65vh;
  line-height: 0;
  border-radius: var(--r);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  background: rgba(0,0,0,0.03);
  margin: 0 auto;
  flex-shrink: 0;
  box-sizing: border-box;
}

#main-img-wrap, #extra-img-wrap, .cat-swapped-img-arena {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cat-swapped-img-arena {
  max-width: 820px;
  margin: 0 auto 16px;
}

.img-box img, #extra-img-wrap img, .cat-swapped-img-arena img {
  display: block;
  max-width: 100%;
  max-height: 65vh;
  width: auto;
  height: auto;
  margin: 0 auto;
  border-radius: var(--r);
  object-fit: contain;
  user-select: none;
  pointer-events: none;
}

#zones {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.dz {
  position: absolute;
  transform: translate(-50%, -50%);
  min-width: 76px;
  min-height: 30px;
  border: 1.5px dashed var(--dz-empty-border);
  border-radius: 8px;
  background: var(--dz-empty-bg);
  backdrop-filter: blur(2px);
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: all;
  transition: border-color 0.15s, background 0.15s, transform 0.15s;
  padding: 2px;
  z-index: 10;
  box-sizing: border-box;
}

.dz-hover {
  border-color: var(--accent) !important;
  background: rgba(37, 99, 235, 0.25) !important;
  transform: translate(-50%, -50%) scale(1.05);
}

.dz-ok,
.dz-err {
  border-color: transparent !important;
  background: transparent !important;
}

/* Zone Target Visual Cues during Click-to-Place */
.has-selected-chip .dz:not(.dz-ok):not(.dz-err) {
  cursor: pointer !important;
}

.has-selected-chip .dz.dz-cue-target {
  border-color: var(--accent) !important;
  background: rgba(37, 99, 235, 0.12) !important;
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.25) !important;
}

.dz-empty-cue {
  font-size: 10px;
  font-family: var(--font);
  font-weight: 600;
  color: var(--accent);
  letter-spacing: 0.02em;
  pointer-events: none;
  user-select: none;
  text-transform: lowercase;
}

/* Minimal Empty States */
.empty-state-badge {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 6px 14px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
  color: var(--muted);
  background: var(--surf);
  border: 1px solid var(--border);
  pointer-events: none;
  user-select: none;
  white-space: nowrap;
  z-index: 20;
}

.empty-pool-msg {
  width: 100%;
  text-align: center;
  font-size: 12px;
  color: var(--muted);
  font-weight: 500;
  padding: 6px 0;
  user-select: none;
}

.label-pool {
  width: 100% !important;
  box-sizing: border-box !important;
  display: flex !important;
  flex-wrap: wrap !important;
  justify-content: center !important;
  align-items: center !important;
  gap: 8px !important;
  padding: 12px 16px !important;
  background: var(--surf);
  border-radius: var(--r);
  border: 1px solid var(--border);
  min-height: 96px !important;
  margin-bottom: 8px !important;
  flex-shrink: 0 !important;
}

.chip {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 5px 12px;
  border-radius: 6px;
  border: 1.5px solid var(--border);
  background: var(--bg);
  color: var(--fg);
  font-size: 13px !important;
  line-height: 1.4 !important;
  font-weight: 500;
  cursor: grab;
  user-select: none;
  touch-action: none;
  white-space: nowrap;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.07);
  transition: transform 0.1s, box-shadow 0.1s;
}

.chip:active {
  cursor: grabbing;
  transform: scale(0.98);
}

.chip.chip-selected {
  outline: 2px solid var(--accent);
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.35);
  transform: scale(1.04);
}

/* ==========================================================================
   THEME-ADAPTIVE PLACED CHIPS (LIGHT & DARK MODE)
   ========================================================================== */

/* 1. Normal Placed Label (Front card - Clean Neutral Border) */
.dz .chip,
.drop-zone .chip {
  background: var(--chip-placed-bg) !important;
  background-color: var(--chip-placed-bg) !important;
  border: 1.5px solid var(--chip-placed-border) !important;
  color: var(--chip-placed-fg) !important;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.06) !important;
  font-size: 13px !important;
  line-height: 1.4 !important;
  font-weight: 500 !important;
  padding: 4px 11px !important;
  border-radius: 6px !important;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
  text-shadow: none !important;
}

/* 2. Correct Placed Label (Back card - Clean Minimal Default) */
.c-ok {
  background: var(--chip-ok-bg) !important;
  background-color: var(--chip-ok-bg) !important;
  color: var(--chip-ok-fg) !important;
  border: 1.5px solid var(--chip-ok-border) !important;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
  font-size: 13px !important;
  line-height: 1.4 !important;
  font-weight: 500 !important;
  border-radius: 6px !important;
  padding: 4px 11px !important;
  cursor: default;
  text-shadow: none !important;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
}

/* 3. Wrong Placed Label (Back card - Clean Minimal Default) */
.c-err {
  background: var(--chip-err-bg) !important;
  background-color: var(--chip-err-bg) !important;
  color: var(--chip-err-fg) !important;
  border: 1.5px solid var(--chip-err-border) !important;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
  font-size: 13px !important;
  line-height: 1.4 !important;
  font-weight: 500 !important;
  border-radius: 6px !important;
  padding: 4px 11px !important;
  cursor: default;
  text-shadow: none !important;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
}

/* 4. Missed Label (Back card - Clean Minimal Default) */
.c-miss {
  background: var(--chip-miss-bg) !important;
  background-color: var(--chip-miss-bg) !important;
  color: var(--chip-miss-fg) !important;
  border: 1.5px dashed var(--chip-miss-border) !important;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
  font-size: 13px !important;
  line-height: 1.4 !important;
  font-weight: 500 !important;
  border-radius: 6px !important;
  padding: 4px 11px !important;
  cursor: default;
  font-style: normal;
  text-shadow: none !important;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
}

/* Strikethrough & Target spans for clean feedback */
.chip-wrong {
  text-decoration: line-through;
  opacity: 0.65;
  margin-right: 6px;
  color: var(--chip-wrong-strike) !important;
  font-weight: 400 !important;
}

.chip-correct {
  font-weight: 600;
  color: var(--chip-correct-fg) !important;
}

/* ==========================================================================
   OPTIONAL: CALM COLORED FEEDBACK (WHEN ENABLED IN SETTINGS)
   ========================================================================== */
.colored-feedback .c-ok {
  background: #f0fdf4 !important;
  background-color: #f0fdf4 !important;
  color: #166534 !important;
  border: 1.5px solid #86efac !important;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04) !important;
}

.colored-feedback .c-err {
  background: #fef2f2 !important;
  background-color: #fef2f2 !important;
  color: #991b1b !important;
  border: 1.5px solid #fca5a5 !important;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04) !important;
}

.colored-feedback .c-miss {
  background: #f0fdf4 !important;
  background-color: #f0fdf4 !important;
  color: #166534 !important;
  border: 1.5px dashed #86efac !important;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04) !important;
}

.colored-feedback .chip-correct {
  color: #166534 !important;
}

/* Dark mode overrides for calm colored feedback */
html.night_mode .colored-feedback .c-ok,
html.nightMode .colored-feedback .c-ok,
.night_mode .colored-feedback .c-ok,
.nightMode .colored-feedback .c-ok,
body.night_mode .colored-feedback .c-ok,
body.nightMode .colored-feedback .c-ok,
.card.night_mode .colored-feedback .c-ok,
.card.nightMode .colored-feedback .c-ok {
  background: #14291f !important;
  background-color: #14291f !important;
  color: #86efac !important;
  border: 1.5px solid #166534 !important;
  box-shadow: none !important;
}

html.night_mode .colored-feedback .c-err,
html.nightMode .colored-feedback .c-err,
.night_mode .colored-feedback .c-err,
.nightMode .colored-feedback .c-err,
body.night_mode .colored-feedback .c-err,
body.nightMode .colored-feedback .c-err,
.card.night_mode .colored-feedback .c-err,
.card.nightMode .colored-feedback .c-err {
  background: #2b171a !important;
  background-color: #2b171a !important;
  color: #fca5a5 !important;
  border: 1.5px solid #7f1d1d !important;
  box-shadow: none !important;
}

html.night_mode .colored-feedback .c-miss,
html.nightMode .colored-feedback .c-miss,
.night_mode .colored-feedback .c-miss,
.nightMode .colored-feedback .c-miss,
body.night_mode .colored-feedback .c-miss,
body.nightMode .colored-feedback .c-miss,
.card.night_mode .colored-feedback .c-miss,
.card.nightMode .colored-feedback .c-miss {
  background: #14291f !important;
  background-color: #14291f !important;
  color: #86efac !important;
  border: 1.5px dashed #166534 !important;
  box-shadow: none !important;
}

html.night_mode .colored-feedback .chip-correct,
html.nightMode .colored-feedback .chip-correct,
.night_mode .colored-feedback .chip-correct,
.nightMode .colored-feedback .chip-correct,
body.night_mode .colored-feedback .chip-correct,
body.nightMode .colored-feedback .chip-correct,
.card.night_mode .colored-feedback .chip-correct,
.card.nightMode .colored-feedback .chip-correct {
  color: #86efac !important;
}

.colored-feedback .dz-ok,
.colored-feedback .dz-err {
  border-color: transparent !important;
  background: transparent !important;
}

.back-body {
  width: 100%;
  box-sizing: border-box;
  margin-top: 14px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  flex-shrink: 0;
  contain: layout;
}

.back-fade {
  opacity: 0;
  transform: translateY(5px);
  transition: opacity 0.25s, transform 0.25s;
}

.back-fade-in {
  opacity: 1;
  transform: translateY(0);
}

.section-label {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--muted);
  padding-top: 14px;
  border-top: 1px solid var(--border);
  margin-bottom: 10px;
  width: 100%;
  text-align: center;
}

.score {
  display: inline-block;
  font-size: 15px;
  font-weight: 700;
  padding: 8px 16px;
  border-radius: var(--r);
  border-left: 4px solid;
  background: var(--surf);
}

.s-ok {
  border-color: var(--ok);
  color: var(--ok);
}

.s-mid {
  border-color: var(--warn);
  color: var(--warn);
}

.s-bad {
  border-color: var(--err);
  color: var(--err);
}

.top-toolbar {
  position: fixed;
  top: 10px;
  right: 14px;
  z-index: 300;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 5px;
}

/* Anki Native Audio / Sound Play Button - Clean icon without square borders */
.audio-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: transparent !important;
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
  padding: 0 !important;
  margin: 0 !important;
}

.audio-btn a,
.audio-btn button,
.replay-button,
.replaybutton,
a.replay-button,
a.replaybutton,
a.soundLink,
button.soundLink,
.soundLink {
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  background: transparent !important;
  background-color: transparent !important;
  border: none !important;
  border-width: 0 !important;
  outline: none !important;
  box-shadow: none !important;
  padding: 0 !important;
  margin: 0 !important;
  border-radius: 0 !important;
  text-decoration: none !important;
  cursor: pointer !important;
}

.audio-btn svg,
.replay-button svg,
.replaybutton svg,
a.replay-button svg,
a.replaybutton svg,
a.soundLink svg,
.soundLink svg,
svg.playImage,
.playImage {
  border: none !important;
  border-width: 0 !important;
  outline: none !important;
  box-shadow: none !important;
  background: transparent !important;
  background-color: transparent !important;
}

.audio-btn svg circle,
.replay-button svg circle,
.replaybutton svg circle,
.playImage circle {
  border: none !important;
}

/* CONTROLS (Top-Right Vertical Stack) */
.ctrl {
  position: fixed;
  top: 14px;
  right: 14px;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 4px;
  z-index: 100;
}

/* BUTTONS – Minimalistic Text */
.ibtn {
  min-width: auto;
  height: 22px;
  padding: 0 6px;
  border-radius: 5px;
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 11px;
  font-weight: 500;
  color: #aaa;
  opacity: 0.65;
  transition: all 0.15s ease;
  line-height: 1;
}

.ibtn:hover {
  opacity: 1;
  color: #666;
  background: rgba(0, 0, 0, 0.04);
}

.ibtn.active {
  opacity: 1;
  color: #222;
  font-weight: 600;
  background: rgba(0, 0, 0, 0.06);
}

/* HIDDEN UTILITY */
.ms { display: none !important; }

/* EXTRA AREA (Text notes & images revealed by Extra/Image button) */
.extra-area {
  max-width: 940px;
  width: 94vw;
  margin: 22px auto 0;
  padding: 0 16px;
  font-size: 1.05rem;
  line-height: 1.55;
  color: #555;
  text-align: center;
  opacity: 0;
  max-height: 0;
  overflow: hidden;
  transition: opacity 0.2s ease, max-height 0.25s ease;
  box-sizing: border-box;
}

.extra-area.show {
  opacity: 1;
  max-height: 1000px;
}

.extra-area img {
  max-width: 100%;
  max-height: 60vh;
  height: auto;
  object-fit: contain;
  margin: 0 auto;
  border-radius: 6px;
  display: block;
}

/* Extra position: Above */
.extra-area.extra-above,
.extra-above .extra-area,
.extra-pos-above .extra-area {
  position: absolute !important;
  top: 48px !important;
  left: 50% !important;
  transform: translateX(-50%) !important;
  z-index: 90 !important;
  width: 92% !important;
  max-width: 820px !important;
  background: var(--surf) !important;
  border: 1px solid var(--border) !important;
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.25) !important;
  margin: 0 !important;
}

html.night_mode .extra-area.extra-above,
html.nightMode .extra-area.extra-above,
.night_mode .extra-area.extra-above,
.nightMode .extra-area.extra-above,
body.night_mode .extra-area.extra-above,
.card.night_mode .extra-area.extra-above {
  background: #202024 !important;
  border-color: #3f3f46 !important;
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.5) !important;
}

/* NIGHT MODE */
.nightMode .ibtn, .night_mode .ibtn, html.nightMode .ibtn, html.night_mode .ibtn { color: #777; opacity: 0.55; }
.nightMode .ibtn:hover, .night_mode .ibtn:hover, html.nightMode .ibtn:hover, html.night_mode .ibtn:hover { opacity: 0.9; color: #ccc; background: rgba(255,255,255,0.06); }
.nightMode .ibtn.active, .night_mode .ibtn.active, html.nightMode .ibtn.active, html.night_mode .ibtn.active { opacity: 1; color: #eee; background: rgba(255,255,255,0.1); }
.nightMode .extra-area, .night_mode .extra-area, html.nightMode .extra-area, html.night_mode .extra-area { color: #bbb; }

.toolbar-btn {
  background: var(--surf);
  border: 1px solid var(--border);
  border-radius: 50%;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  cursor: pointer;
  padding: 0;
  color: var(--fg);
}

.ddi-reveal-btn {
  background: var(--surf) !important;
  border: 1px solid var(--border) !important;
  border-radius: 6px !important;
  width: auto !important;
  height: auto !important;
  padding: 4px 10px !important;
  display: inline-flex !important;
  align-items: center !important;
  gap: 5px !important;
  font-size: 11px !important;
  font-weight: 500 !important;
  color: var(--fg) !important;
  cursor: pointer !important;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
  line-height: 1.3 !important;
  text-decoration: none !important;
}

.ddi-reveal-btn:hover {
  background: var(--bg) !important;
  border-color: var(--muted) !important;
}

.ddi-reveal-btn .reveal-chevron {
  font-size: 8px !important;
  opacity: 0.75;
}

.panel {
  width: 100%;
  max-width: 640px;
  margin: 12px auto 0;
  box-sizing: border-box;
  text-align: left;
  flex-shrink: 0;
  contain: content;
}

.img-panel {
  width: 100%;
  max-width: 640px;
  margin: 12px auto 0;
  text-align: center;
  box-sizing: border-box;
}

.panel-img-box {
  display: inline-block;
  max-width: 100%;
  border-radius: var(--r);
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border: 1px solid var(--border);
  background: var(--surf);
}

.panel-img-box img {
  display: block;
  max-width: 100%;
  max-height: 48vh;
  height: auto;
  margin: 0 auto;
  object-fit: contain;
}

.panel-body {
  padding: 12px 14px;
  font-size: 13px;
  line-height: 1.6;
  background: var(--surf);
  border-left: 3px solid var(--border);
  border-radius: var(--r);
}

.hint-bar {
  width: 100%;
  margin-top: 10px;
  font-size: 11px;
  color: var(--muted);
  text-align: center;
}

.hint-bar kbd {
  display: inline-block;
  padding: 1px 5px;
  border: 1px solid var(--border);
  border-radius: 4px;
  font-size: 10px;
  background: var(--surf);
  font-family: inherit;
}

/* Horizontal vs Vertical Layout Variations for Image Cards */
.ddi-wrap.layout-vertical,
.layout-vertical .ddi-wrap,
.layout-vertical.ddi-wrap {
  max-width: 1100px !important;
  flex-direction: row !important;
  align-items: flex-start !important;
  justify-content: center !important;
  gap: 24px !important;
}
.ddi-wrap.layout-vertical .upper-locked,
.layout-vertical .upper-locked {
  flex: 1 1 auto !important;
  min-width: 0 !important;
  align-items: center !important;
}
.ddi-wrap.layout-vertical .lower-flexible,
.layout-vertical .lower-flexible {
  width: 260px !important;
  max-width: 300px !important;
  flex-shrink: 0 !important;
  flex-grow: 0 !important;
  margin-top: 44px !important;
  align-items: stretch !important;
}
.ddi-wrap.layout-vertical .label-pool,
.layout-vertical .label-pool {
  flex-direction: column !important;
  align-items: stretch !important;
  max-height: 65vh !important;
  overflow-y: auto !important;
  gap: 8px !important;
  width: 100% !important;
}
.ddi-wrap.layout-vertical .back-body,
.layout-vertical .back-body {
  width: 100% !important;
}
@media (max-width: 768px) {
  .ddi-wrap.layout-vertical,
  .layout-vertical .ddi-wrap {
    flex-direction: column !important;
    align-items: center !important;
  }
  .ddi-wrap.layout-vertical .lower-flexible,
  .layout-vertical .lower-flexible {
    width: 100% !important;
    max-width: 100% !important;
    margin-top: 16px !important;
  }
  .ddi-wrap.layout-vertical .label-pool,
  .layout-vertical .label-pool {
    flex-direction: row !important;
    flex-wrap: wrap !important;
    max-height: none !important;
  }
}
"""
FRONT_TEMPLATE = """<script>
function toggleImage(btn){
  var main = document.getElementById('main-img-wrap');
  var extra = document.getElementById('extra-img-wrap');
  var zones = document.getElementById('zones');
  if(!main || !extra) return;
  var isSwapped = extra.style.display !== 'none';
  if(isSwapped){
    main.style.display = '';
    extra.style.display = 'none';
    if(zones) zones.style.display = '';
    if(btn) btn.classList.remove('active');
  } else {
    main.style.display = 'none';
    extra.style.display = 'flex';
    if(zones) zones.style.display = 'none';
    if(btn) btn.classList.add('active');
  }
}
function toggleExtra(btn){
  var source = document.getElementById('extra-src');
  var area = document.getElementById('extra-area');
  if(!source || !area) return;
  var isActive = area.classList.contains('show');
  if(isActive){
    area.innerHTML = '';
    area.classList.remove('show');
    if(btn) btn.classList.remove('active');
  } else {
    area.innerHTML = '<div class=\"extra-body\">' + source.innerHTML + '</div>';
    area.classList.add('show');
    if(btn) btn.classList.add('active');
  }
}
function toggle(id, btn){
  if(id === 'fimg' || id === 'bimg') toggleImage(btn);
  else toggleExtra(btn);
}
</script>
<div class=\"vp\">
  {{#Front Image}}<div id=\"fimg\" class=\"ms\">{{Front Image}}</div>{{/Front Image}}
  {{#Extra}}<div id=\"extra-src\" class=\"ms\">{{Extra}}</div>{{/Extra}}

  <div class=\"ctrl\">
    {{#Front Audio}}<div class=\"audio-btn\">{{Front Audio}}</div>{{/Front Audio}}
    <button type=\"button\" id=\"ddi-undo-btn\" class=\"ibtn ddi-undo-btn\" style=\"display:none;\" onclick=\"_ddiUndo(event)\" title=\"Undo last placement (Ctrl+Z / ⌘Z)\">undo</button>
    {{#Front Image}}
    <button type=\"button\" class=\"ibtn\" data-label=\"image\" onclick=\"toggleImage(this)\" title=\"Image\">image</button>
    {{/Front Image}}
    {{#Extra}}
    <button type=\"button\" class=\"ibtn\" data-label=\"extra\" onclick=\"toggleExtra(this)\" title=\"Extra\">extra</button>
    {{/Extra}}
  </div>

  <span id=\"ddi-labels\" style=\"display:none\">{{Labels}}</span>
  <span id=\"ddi-zones\" style=\"display:none\">{{Zones}}</span>
  <div class=\"ddi-wrap {{#Layout}}layout-{{Layout}}{{/Layout}}\">
    <div class=\"upper-locked\">
      <div class=\"meta\">{{Title}}</div>
      <h1 class=\"question\">{{Question}}</h1>
      <div class=\"img-arena\">
        <div class=\"img-box\" id=\"imgBox\">
          <div id=\"main-img-wrap\">{{#Image}}{{Image}}{{/Image}}</div>
          {{#Front Image}}<div id=\"extra-img-wrap\" style=\"display:none;\">{{Front Image}}</div>{{/Front Image}}
          <div id=\"zones\"></div>
        </div>
      </div>
    </div>
    <div class=\"lower-flexible\">
      <div class=\"label-pool\" id=\"pool\"></div>
    </div>
  </div>

  <div id=\"extra-area\" class=\"extra-area\"></div>
</div>
<script>
function _ddiInit(){
// Synchronize Anki theme
try {
  var isDark = document.body.classList.contains('night_mode') || 
               document.body.classList.contains('nightMode') || 
               document.documentElement.classList.contains('night_mode') || 
               document.documentElement.classList.contains('nightMode');
  if (!isDark && window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    document.documentElement.setAttribute('data-anki-light', 'true');
  }
} catch(e){}

function decodeEntities(str){
var d=document.createElement('div');
d.innerHTML=str;
return d.textContent||d.innerText||str;
}
function stripTags(str){
var d=document.createElement('div');
d.innerHTML=str;
return d.textContent||d.innerText||'';
}
function splitField(str){
// Split on pipe - handle both raw | and HTML entity &#124;
str = decodeEntities(str);
str = stripTags(str);
var parts = str.split('|');
if(parts.length <= 1) parts = str.split('&#124;');
return parts.map(function(s){
  var clean = s.trim();
  var eq = clean.indexOf('=');
  if (eq > 0) {
    var after = clean.slice(eq + 1).trim();
    if (/^[\d\.\,%\s]+$/.test(after)) {
      clean = clean.slice(0, eq).trim();
    }
  }
  return clean;
}).filter(Boolean);
}
function parseZones(str){
str = decodeEntities(str);
str = stripTags(str);
var parts = str.split('|');
if(parts.length <= 1) parts = str.split('&#124;');
var z=[];
parts.forEach(function(p){
p=p.trim();
var idx=p.indexOf('='); if(idx<0)return;
var lbl=p.slice(0,idx).trim(), xy=p.slice(idx+1).trim().split(',');
if(xy.length===2){var x=parseFloat(xy[0]),y=parseFloat(xy[1]);if(!isNaN(x)&&!isNaN(y))z.push({label:lbl,x:x,y:y});}
});
return z;
}

// Lock image dimensions to permanently freeze layout
function lockImageDimensions(){
  var img = document.querySelector('#imgBox img') || document.querySelector('.img-box img');
  var box = document.getElementById('imgBox') || document.querySelector('.img-box');
  var arena = document.querySelector('.img-arena');
  if(!img || !box || !arena) return;

  function applyLock(){
    var rect = img.getBoundingClientRect();
    if(rect.height > 10 && rect.width > 10){
      var h = Math.round(rect.height) + 'px';
      var w = Math.round(rect.width) + 'px';
      box.style.height = h;
      box.style.width = w;
      box.style.minHeight = h;
      box.style.maxHeight = h;
      arena.style.height = h;
      arena.style.minHeight = h;
    }
  }

  if(img.complete && img.naturalHeight > 0){
    applyLock();
  } else {
    img.addEventListener('load', applyLock, { once: true });
  }
}
lockImageDimensions();

var CARD_KEY = (\"ddi_{{Title}}_{{Question}}\").slice(0,60);
// Read from DOM spans - most reliable, Anki always renders span content correctly
var _labelsEl = document.getElementById(\"ddi-labels\");
var _zonesEl = document.getElementById(\"ddi-zones\");
var LABELS = _labelsEl ? splitField(_labelsEl.innerHTML) : [];
var zones = _zonesEl ? parseZones(_zonesEl.innerHTML) : [];

// Restore previously-placed items if Anki redrew this same question (e.g.
// after Mark Note or another note-text change elsewhere) using the same
// {key, placed} data save() already writes below. Falls back to
// sessionStorage. Leftover data from a different card (or no data at all)
// is ignored and the hash cleared, exactly as before.
var restoredPlaced = {};
try{
var _raw = '';
if(location.hash.startsWith('#ddi=')){
  _raw = decodeURIComponent(location.hash.slice(5));
} else {
  try{ _raw = sessionStorage.getItem('ddi') || ''; }catch(e){}
}
if(_raw){
  var old = JSON.parse(_raw);
  if(old.key === CARD_KEY){
    restoredPlaced = old.placed || {};
  } else {
    location.hash = '';
  }
} else {
  location.hash = '';
}
}catch(e){ location.hash=''; restoredPlaced = {}; }

function shuffle(a){
a=a.slice();
for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1)),t=a[i];a[i]=a[j];a[j]=t;}
return a;
}

var zc=document.getElementById('zones');
if(zones.length === 0){
  var emptyZ=document.createElement('div');
  emptyZ.className='empty-state-badge';
  emptyZ.textContent='No drop zones';
  zc.appendChild(emptyZ);
} else {
  zones.forEach(function(z){
  var dz=document.createElement('div');
  dz.className='dz'; dz.dataset.label=z.label;
  dz.style.left=z.x+'%'; dz.style.top=z.y+'%';
  var cue=document.createElement('span');
  cue.className='dz-empty-cue';
  dz.appendChild(cue);
  var restoredVal=restoredPlaced[z.label];
  if(restoredVal){
    var rc=document.createElement('div');
    rc.className='chip'; rc.draggable=true; rc.dataset.v=restoredVal; rc.textContent=restoredVal;
    dz.appendChild(rc);
  }
  zc.appendChild(dz);
  });
}

var pool=document.getElementById('pool');
var _restoredCounts={};
Object.keys(restoredPlaced).forEach(function(k){
var v=restoredPlaced[k];
_restoredCounts[v]=(_restoredCounts[v]||0)+1;
});
shuffle(LABELS).forEach(function(v){
if(_restoredCounts[v] > 0){
  _restoredCounts[v]--;
  return;
}
var c=document.createElement('div');
c.className='chip'; c.draggable=true; c.dataset.v=v; c.textContent=v;
pool.appendChild(c);
});

function updatePoolEmptyState(){
  if(!pool) return;
  var remaining = pool.querySelectorAll('.chip').length;
  var emptyMsg = pool.querySelector('.empty-pool-msg');
  if(remaining === 0){
    if(!emptyMsg){
      emptyMsg = document.createElement('div');
      emptyMsg.className = 'empty-pool-msg';
      emptyMsg.textContent = LABELS.length === 0 ? 'No labels' : 'No labels in pool';
      pool.appendChild(emptyMsg);
    }
  } else {
    if(emptyMsg) emptyMsg.remove();
  }
}
updatePoolEmptyState();

// Undo History Management
var historyStack = [];
function pushHistory(){
  var snapshot = [];
  document.querySelectorAll('.chip').forEach(function(c){
    snapshot.push({ el: c, parent: c.parentElement });
  });
  historyStack.push(snapshot);
  updateUndoBtn();
}

window._ddiUndo = function(e){
  if(e && e.preventDefault) e.preventDefault();
  undo();
};

function undo(){
  if(historyStack.length === 0) return;
  var snapshot = historyStack.pop();
  snapshot.forEach(function(item){
    item.parent.appendChild(item.el);
    item.el.classList.remove('chip-selected');
  });
  if(selectedChip){
    selectedChip.classList.remove('chip-selected');
    selectedChip = null;
  }
  updateZoneVisualCues();
  updatePoolEmptyState();
  updateUndoBtn();
  save();
}

function updateUndoBtn(){
  var btn = document.getElementById('ddi-undo-btn');
  if(btn){
    btn.style.display = historyStack.length > 0 ? 'inline-flex' : 'none';
  }
}

function save(){
var state={key:CARD_KEY,placed:{}};
document.querySelectorAll('.dz').forEach(function(d){
var c=d.querySelector('.chip'); if(c) state.placed[d.dataset.label]=c.dataset.v;
});
try{ location.hash='ddi='+encodeURIComponent(JSON.stringify(state)); }catch(e){}
try{ sessionStorage.setItem('ddi',JSON.stringify(state)); }catch(e){}
}

var hov=null;
document.addEventListener('dragover',function(e){
e.preventDefault();
var dz=e.target.closest('.dz');
if(dz!==hov){ if(hov)hov.classList.remove('dz-hover'); hov=dz; if(hov)hov.classList.add('dz-hover'); }
});
document.addEventListener('dragleave',function(e){
if(hov&&!hov.contains(e.relatedTarget)){hov.classList.remove('dz-hover');hov=null;}
});

var drag=null;
document.addEventListener('dragstart',function(e){
if(!e.target.classList.contains('chip'))return;
drag=e.target; setTimeout(function(){if(drag)drag.style.opacity='.3';},0);
});
document.addEventListener('dragend',function(e){
if(e.target.classList.contains('chip'))e.target.style.opacity='1';
if(hov){hov.classList.remove('dz-hover');hov=null;}
});

// Drop event with clean swapping & history recording
document.addEventListener('drop',function(e){
e.preventDefault();
if(hov){hov.classList.remove('dz-hover');hov=null;}
var t=e.target.closest('.dz,#pool');
if(!t||!drag)return;
if(drag.parentElement === t) return;

pushHistory();
var fromDz=drag.closest('.dz');
if(t.classList.contains('dz')){
  var ex=t.querySelector('.chip');
  if(ex && ex !== drag){
    ex.style.opacity='1';
    ex.classList.remove('chip-selected');
    if(fromDz){
      // Clean swap: target chip moves to origin zone
      fromDz.appendChild(ex);
    } else {
      // Came from pool: displaced chip returns to pool
      pool.appendChild(ex);
    }
  }
}
t.appendChild(drag);
if(selectedChip){
  selectedChip.classList.remove('chip-selected');
  selectedChip=null;
}
updateZoneVisualCues();
updatePoolEmptyState();
save();
});

// Click-to-place support with clear selection feedback & zone cues
var selectedChip=null;

function updateZoneVisualCues(){
  var zc = document.getElementById('zones');
  if(!zc) return;
  if(selectedChip){
    zc.classList.add('has-selected-chip');
    document.querySelectorAll('.dz').forEach(function(d){
      var c = d.querySelector('.chip');
      var cue = d.querySelector('.dz-empty-cue');
      if(!c){
        d.classList.add('dz-cue-target');
        if(cue) cue.textContent = 'place here';
      } else {
        d.classList.remove('dz-cue-target');
        if(cue) cue.textContent = '';
      }
    });
  } else {
    zc.classList.remove('has-selected-chip');
    document.querySelectorAll('.dz').forEach(function(d){
      d.classList.remove('dz-cue-target');
      var cue = d.querySelector('.dz-empty-cue');
      if(cue) cue.textContent = '';
    });
  }
}

document.addEventListener('click',function(e){
var chip=e.target.closest('.chip');
var dz=e.target.closest('.dz,#pool');

if(chip){
  var parentDz=chip.closest('.dz');
  if(selectedChip && selectedChip !== chip){
    if(parentDz){
      // User clicked on an occupied zone while a chip is selected -> place and swap!
      pushHistory();
      var fromDz=selectedChip.closest('.dz');
      var ex=chip;
      ex.style.opacity='1';
      ex.classList.remove('chip-selected');
      if(fromDz){
        fromDz.appendChild(ex);
      } else {
        pool.appendChild(ex);
      }
      parentDz.appendChild(selectedChip);
      selectedChip.classList.remove('chip-selected');
      selectedChip=null;
      updateZoneVisualCues();
      updatePoolEmptyState();
      save();
      return;
    }
    // Clicked another chip in the pool -> switch selection
    selectedChip.classList.remove('chip-selected');
    selectedChip=chip;
    chip.classList.add('chip-selected');
    updateZoneVisualCues();
    return;
  }
  if(parentDz && !selectedChip){
    // Clicking a placed chip in a zone selects it to move
    selectedChip=chip;
    chip.classList.add('chip-selected');
    updateZoneVisualCues();
    return;
  }
  // Clicking a chip in the pool toggles selection
  if(selectedChip===chip){
    chip.classList.remove('chip-selected');
    selectedChip=null;
  } else {
    if(selectedChip) selectedChip.classList.remove('chip-selected');
    selectedChip=chip;
    chip.classList.add('chip-selected');
  }
  updateZoneVisualCues();
  return;
}

if(dz && selectedChip){
  var fromContainer=selectedChip.parentElement;
  if(dz.id==='pool'||dz.classList.contains('label-pool')){
    if(fromContainer !== pool){
      pushHistory();
      selectedChip.style.opacity='1';
      selectedChip.classList.remove('chip-selected');
      pool.appendChild(selectedChip);
      selectedChip=null;
      updateZoneVisualCues();
      updatePoolEmptyState();
      save();
    } else {
      selectedChip.classList.remove('chip-selected');
      selectedChip=null;
      updateZoneVisualCues();
    }
    return;
  }
  if(dz.classList.contains('dz')){
    if(fromContainer !== dz){
      pushHistory();
      var fromDz=selectedChip.closest('.dz');
      var ex=dz.querySelector('.chip');
      if(ex && ex !== selectedChip){
        ex.style.opacity='1';
        ex.classList.remove('chip-selected');
        if(fromDz){
          fromDz.appendChild(ex);
        } else {
          pool.appendChild(ex);
        }
      }
      dz.appendChild(selectedChip);
      selectedChip.classList.remove('chip-selected');
      selectedChip=null;
      updateZoneVisualCues();
      updatePoolEmptyState();
      save();
    } else {
      selectedChip.classList.remove('chip-selected');
      selectedChip=null;
      updateZoneVisualCues();
    }
    return;
  }
}
});

var ti=null,tc=null;
document.addEventListener('touchstart',function(e){
var item=e.target.closest('.chip'); if(!item)return;
ti=item; var r=item.getBoundingClientRect();
tc=item.cloneNode(true);
tc.style.cssText='position:fixed;z-index:9999;pointer-events:none;opacity:.85;left:'+r.left+'px;top:'+r.top+'px;width:'+r.width+'px;margin:0;';
document.body.appendChild(tc); item.style.opacity='.3';
},{passive:true});
document.addEventListener('touchmove',function(e){
if(!tc)return; e.preventDefault();
var t=e.touches[0];
tc.style.left=(t.clientX-tc.offsetWidth/2)+'px';
tc.style.top=(t.clientY-tc.offsetHeight/2)+'px';
tc.style.display='none';
var hit=document.elementFromPoint(t.clientX,t.clientY);
tc.style.display='';
document.querySelectorAll('.dz').forEach(function(d){d.classList.remove('dz-hover');});
var dz=hit&&hit.closest('.dz'); if(dz)dz.classList.add('dz-hover');
},{passive:false});
document.addEventListener('touchend',function(e){
if(!ti||!tc)return;
var t=e.changedTouches[0];
tc.style.display='none';
var hit=document.elementFromPoint(t.clientX,t.clientY);
tc.remove();tc=null;ti.style.opacity='1';
document.querySelectorAll('.dz').forEach(function(d){d.classList.remove('dz-hover');});
var dz=hit&&hit.closest('.dz,#pool');
if(dz){
var fromContainer = ti.parentElement;
if(fromContainer !== dz){
  pushHistory();
  var fromDz=ti.closest('.dz');
  if(dz.classList.contains('dz')){
    var ex=dz.querySelector('.chip');
    if(ex && ex !== ti){
      ex.style.opacity='1';
      ex.classList.remove('chip-selected');
      if(fromDz){
        fromDz.appendChild(ex);
      } else {
        pool.appendChild(ex);
      }
    }
  }
  dz.appendChild(ti);
  if(selectedChip){
    selectedChip.classList.remove('chip-selected');
    selectedChip=null;
  }
  updateZoneVisualCues();
  updatePoolEmptyState();
  save();
}
}
ti=null;
});

// Keyboard listener for Space (flip) and Ctrl+Z / Cmd+Z (undo)
document.addEventListener('keydown',function(e){
if((e.ctrlKey || e.metaKey) && (e.key === 'z' || e.key === 'Z' || e.code === 'KeyZ')){
  e.preventDefault();
  undo();
  return;
}
if(e.code==='Space'||e.key===' '){
  e.preventDefault();
  var btn=document.querySelector('#answer,.btn-primary,[id*=\"answer\"]');
  if(btn)btn.click();
  else document.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',code:'Enter',keyCode:13,bubbles:true}));
}
});
}
_ddiInit();
</script>"""
BACK_TEMPLATE = """<script>
function toggleImage(btn){
  var main = document.getElementById('main-img-wrap');
  var extra = document.getElementById('extra-img-wrap');
  var zones = document.getElementById('zones');
  if(!main || !extra) return;
  var isSwapped = extra.style.display !== 'none';
  if(isSwapped){
    main.style.display = '';
    extra.style.display = 'none';
    if(zones) zones.style.display = '';
    if(btn) btn.classList.remove('active');
  } else {
    main.style.display = 'none';
    extra.style.display = 'flex';
    if(zones) zones.style.display = 'none';
    if(btn) btn.classList.add('active');
  }
}
function toggleExtra(btn){
  var source = document.getElementById('extra-src');
  var area = document.getElementById('extra-area');
  if(!source || !area) return;
  var isActive = area.classList.contains('show');
  if(isActive){
    area.innerHTML = '';
    area.classList.remove('show');
    if(btn) btn.classList.remove('active');
  } else {
    area.innerHTML = '<div class=\"extra-body\">' + source.innerHTML + '</div>';
    area.classList.add('show');
    if(btn) btn.classList.add('active');
  }
}
function toggle(id, btn){
  if(id === 'fimg' || id === 'bimg') toggleImage(btn);
  else toggleExtra(btn);
}
</script>
<div class=\"vp\">
  {{#Back Image}}<div id=\"bimg\" class=\"ms\">{{Back Image}}</div>{{/Back Image}}
  {{#Extra}}<div id=\"extra-src\" class=\"ms\">{{Extra}}</div>{{/Extra}}

  <div class=\"ctrl\">
    {{#Back Audio}}<div class=\"audio-btn\">{{Back Audio}}</div>{{/Back Audio}}
    {{#Back Image}}
    <button type=\"button\" class=\"ibtn\" data-label=\"image\" onclick=\"toggleImage(this)\" title=\"Image\">image</button>
    {{/Back Image}}
    {{#Extra}}
    <button type=\"button\" class=\"ibtn\" data-label=\"extra\" onclick=\"toggleExtra(this)\" title=\"Extra\">extra</button>
    {{/Extra}}
  </div>

  <span id=\"ddi-labels\" style=\"display:none\">{{Labels}}</span>
  <span id=\"ddi-zones\" style=\"display:none\">{{Zones}}</span>
  <div class=\"ddi-wrap {{#Layout}}layout-{{Layout}}{{/Layout}}\">
    <div class=\"upper-locked\">
      <div class=\"meta\">{{Title}}</div>
      <h1 class=\"question\">{{Question}}</h1>
      <div class=\"img-arena\">
        <div class=\"img-box\" id=\"imgBox\">
          <div id=\"main-img-wrap\">{{#Image}}{{Image}}{{/Image}}</div>
          {{#Back Image}}<div id=\"extra-img-wrap\" style=\"display:none;\">{{Back Image}}</div>{{/Back Image}}
          <div id=\"zones\"></div>
        </div>
      </div>
    </div>
    <div class=\"lower-flexible\">
      <div class=\"label-pool\" id=\"pool\"></div>
      <div class=\"back-body\">
        <div class=\"section-label\">Resultat</div>
        <div id=\"scoreBox\"></div>
      </div>
    </div>
  </div>

  <div id=\"extra-area\" class=\"extra-area\"></div>
</div>
<script>
(function(){
// Synchronize Anki theme
try {
  var isDark = document.body.classList.contains('night_mode') || 
               document.body.classList.contains('nightMode') || 
               document.documentElement.classList.contains('night_mode') || 
               document.documentElement.classList.contains('nightMode');
  if (!isDark && window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    // If OS prefers dark but Anki's body does NOT have night_mode, force light mode tag
    document.documentElement.setAttribute('data-anki-light', 'true');
  }
} catch(e){}

function decodeEntities(str){
var d=document.createElement('div'); d.innerHTML=str;
return d.textContent||d.innerText||str;
}
function stripTags(str){
var d=document.createElement('div'); d.innerHTML=str;
return d.textContent||d.innerText||'';
}
function splitField(str){
str=decodeEntities(str); str=stripTags(str);
var parts=str.split('|');
if(parts.length<=1) parts=str.split('&#124;');
return parts.map(function(s){return s.trim();}).filter(Boolean);
}
function parseZones(str){
str=decodeEntities(str); str=stripTags(str);
var parts=str.split('|');
if(parts.length<=1) parts=str.split('&#124;');
var z=[];
parts.forEach(function(p){
p=p.trim();
var idx=p.indexOf('='); if(idx<0)return;
var lbl=p.slice(0,idx).trim(), xy=p.slice(idx+1).trim().split(',');
if(xy.length===2){var x=parseFloat(xy[0]),y=parseFloat(xy[1]);if(!isNaN(x)&&!isNaN(y))z.push({label:lbl,x:x,y:y});}
});
return z;
}

var _lEl=document.getElementById(\"ddi-labels\");
var _zEl=document.getElementById(\"ddi-zones\");
var LABELS=_lEl ? splitField(_lEl.innerHTML) : [];
var zones =_zEl ? parseZones(_zEl.innerHTML) : [];

var placed={};
var raw='';

// Lock image dimensions to permanently freeze layout
function lockImageDimensions(){
  var img = document.querySelector('#imgBox img') || document.querySelector('.img-box img');
  var box = document.getElementById('imgBox') || document.querySelector('.img-box');
  var arena = document.querySelector('.img-arena');
  if(!img || !box || !arena) return;

  function applyLock(){
    var rect = img.getBoundingClientRect();
    if(rect.height > 10 && rect.width > 10){
      var h = Math.round(rect.height) + 'px';
      var w = Math.round(rect.width) + 'px';
      box.style.height = h;
      box.style.width = w;
      box.style.minHeight = h;
      box.style.maxHeight = h;
      arena.style.height = h;
      arena.style.minHeight = h;
    }
  }

  if(img.complete && img.naturalHeight > 0){
    applyLock();
  } else {
    img.addEventListener('load', applyLock, { once: true });
  }
}
lockImageDimensions();
try{ var h=location.hash; if(h&&h.indexOf('ddi=')>=0)raw=decodeURIComponent(h.slice(h.indexOf('ddi=')+4)); }catch(e){}
if(!raw){ try{ raw=sessionStorage.getItem('ddi')||''; }catch(e){} }
try{ if(raw){ var parsed=JSON.parse(raw); placed=parsed.placed||{}; } }catch(e){ placed={}; }
try{ location.hash=''; }catch(e){}
try{ sessionStorage.removeItem('ddi'); }catch(e){}

var zc=document.getElementById('zones');
var pool=document.getElementById('pool');
var total=0,got=0;

if(zones.length === 0){
  var emptyZ = document.createElement('div');
  emptyZ.className = 'empty-state-badge';
  emptyZ.textContent = 'No drop zones';
  zc.appendChild(emptyZ);
} else {
  zones.forEach(function(z){
  var dz=document.createElement('div');
  dz.className='dz'; dz.style.left=z.x+'%'; dz.style.top=z.y+'%';
  var userVal=placed[z.label]||'';
  var ok=(userVal===z.label);
  total++; if(ok)got++;
  var chip=document.createElement('div');
  if(userVal){
  if(ok){
  chip.className='chip c-ok';
  chip.textContent=userVal;
  dz.classList.add('dz-ok');
  } else {
  chip.className='chip c-err';
  chip.innerHTML='<span class=\"chip-wrong\">'+userVal+'</span> <span class=\"chip-correct\">'+z.label+'</span>';
  dz.classList.add('dz-err');
  }
  } else {
  chip.className='chip c-miss';
  chip.innerHTML='<span class=\"chip-correct\">'+z.label+'</span>';
  dz.classList.add('dz-err');
  }
  dz.appendChild(chip);
  zc.appendChild(dz);
  });
}

var allPlaced=Object.values(placed);
if(pool){
var unplacedCount = 0;
LABELS.forEach(function(v){
if(allPlaced.indexOf(v)<0){
unplacedCount++;
var c=document.createElement('div');c.className='chip';c.textContent=v;pool.appendChild(c);
}
});
if(unplacedCount === 0){
  var emptyMsg = document.createElement('div');
  emptyMsg.className = 'empty-pool-msg';
  emptyMsg.textContent = LABELS.length === 0 ? 'No labels' : 'No labels in pool';
  pool.appendChild(emptyMsg);
}
}

var pct=total?Math.round(got/total*100):0;
var scls=pct===100?'s-ok':pct>=50?'s-mid':'s-bad';
var sb=document.getElementById('scoreBox');
if(sb) sb.innerHTML='<div class=\"score '+scls+'\">'+got+' / '+total+' korrekte ('+pct+'%)</div>';

setTimeout(function(){
document.querySelectorAll('.back-fade').forEach(function(el){el.classList.add('back-fade-in');});
},20);
document.addEventListener('keydown',function(e){if(e.code==='Space'||e.key===' ')e.preventDefault();});
}());
</script>"""

# Note Type 2: Category Sorting
CAT_NOTE_TYPE_NAME = "DragDrop"
CAT_LEGACY_NAMES = ["Drag & Drop Category", "Category Sorting", "DragDrop Sorting"]
CAT_FIELDS = ["Title", "Question", "Categories", "Items", "Distractors", "Layout", "Extra", "Front Audio", "Back Audio", "Front Image", "Back Image"]

CAT_BASE_CSS = """:root {
  --bg: #ffffff;
  --fg: #1c1c1c;
  --muted: #8e8e93;
  --border: #e2e8f0;
  --surf: #f8fafc;
  --ok: #059669;
  --err: #dc2626;
  --warn: #d97706;
  --accent: #2563eb;
  --font: -apple-system, BlinkMacSystemFont, \"Segoe UI\", Roboto, Helvetica, Arial, sans-serif;
  --r: 8px;
}

/* Explicit Light Mode in Anki */
/* ==========================================================================
   THEME VARIABLES & ADAPTIVE STYLES
   ========================================================================== */

:root,
html:not(.night_mode):not(.nightMode),
body:not(.night_mode):not(.nightMode),
.card:not(.night_mode):not(.nightMode) {
  --bg: #ffffff;
  --fg: #1c1c1c;
  --muted: #8e8e93;
  --border: #e2e8f0;
  --surf: #f8fafc;
  --ok: #059669;
  --err: #dc2626;
  --warn: #d97706;
  --accent: #2563eb;
  
  /* Adaptive Chips: Light Mode (Clean Minimal Default) */
  --chip-placed-bg: #ffffff;
  --chip-placed-fg: #0f172a;
  --chip-placed-border: #94a3b8;
  --chip-ok-bg: #ffffff;
  --chip-ok-fg: #0f172a;
  --chip-ok-border: #94a3b8;
  --chip-err-bg: #ffffff;
  --chip-err-fg: #0f172a;
  --chip-err-border: #94a3b8;
  --chip-miss-bg: #ffffff;
  --chip-miss-fg: #15803d;
  --chip-miss-border: #94a3b8;
  --chip-wrong-strike: #64748b;
  --chip-correct-fg: #15803d;
  --dz-empty-border: rgba(148, 163, 184, 0.75);
  --dz-empty-bg: rgba(255, 255, 255, 0.6);
}

/* Automatic Anki Dark/Night Mode Detection */
html.night_mode,
html.nightMode,
html[data-theme=\"dark\"],
html[data-night-mode=\"true\"],
.night_mode,
.nightMode,
.night_mode #qa,
.nightMode #qa,
body.night_mode,
body.nightMode,
:root.night_mode,
:root.nightMode,
.card.night_mode,
.card.nightMode {
  --bg: #18181b !important;
  --fg: #f4f4f5 !important;
  --muted: #a1a1aa !important;
  --border: #27272a !important;
  --surf: #27272a !important;
  --ok: #10b981 !important;
  --err: #ef4444 !important;
  --warn: #f59e0b !important;
  --accent: #3b82f6 !important;

  /* Adaptive Chips: Dark Mode (Clean Minimal Default) */
  --chip-placed-bg: #22242a !important;
  --chip-placed-fg: #f1f5f9 !important;
  --chip-placed-border: #3f3f46 !important;
  --chip-ok-bg: #22242a !important;
  --chip-ok-fg: #f1f5f9 !important;
  --chip-ok-border: #3f3f46 !important;
  --chip-err-bg: #22242a !important;
  --chip-err-fg: #f1f5f9 !important;
  --chip-err-border: #3f3f46 !important;
  --chip-miss-bg: #22242a !important;
  --chip-miss-fg: #4ade80 !important;
  --chip-miss-border: #52525b !important;
  --chip-wrong-strike: #94a3b8 !important;
  --chip-correct-fg: #4ade80 !important;
  --dz-empty-border: rgba(113, 113, 122, 0.7) !important;
  --dz-empty-bg: rgba(0, 0, 0, 0.4) !important;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html, body {
  height: auto !important;
  min-height: 100% !important;
  margin: 0 !important;
  padding: 0 !important;
  display: block !important;
  overflow-y: auto !important;
  background: var(--bg);
  color: var(--fg);
}

.card {
  min-height: 100vh !important;
  height: auto !important;
  display: flex !important;
  flex-direction: column !important;
  justify-content: flex-start !important;
  align-items: center !important;
  padding-top: 24px !important;
  margin: 0 !important;
  box-sizing: border-box !important;
  font-family: var(--font);
  background: var(--bg);
  color: var(--fg);
  font-size: 15px;
  line-height: 1.55;
  width: 100%;
}

/* Midcenter mode: Visually centered on screen with stable top anchor to prevent vertical jump */
body.midcenter,
html.midcenter,
.card.midcenter {
  min-height: 100vh !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: flex-start !important;
  padding-top: max(24px, calc(48vh - 330px)) !important;
  padding-bottom: 48px !important;
}

.ddi-wrap {
  width: 100%;
  max-width: 920px;
  margin: 0 auto;
  padding: 0 16px 48px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  text-align: center;
  box-sizing: border-box;
}

.upper-locked {
  width: 100% !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: flex-start !important;
  flex-shrink: 0 !important;
  flex-grow: 0 !important;
  contain: layout paint !important;
  position: relative !important;
  box-sizing: border-box !important;
}

.lower-flexible {
  width: 100% !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: flex-start !important;
  flex-grow: 1 !important;
  flex-shrink: 0 !important;
  position: relative !important;
  box-sizing: border-box !important;
  contain: layout !important;
}

.meta {
  width: 100%;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.09em;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 6px;
  text-align: center;
}

.question {
  width: 100%;
  font-size: 22px;
  font-weight: 700;
  margin-bottom: 18px;
  line-height: 1.3;
  text-align: center;
}

.img-arena {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 16px;
  flex-shrink: 0;
  box-sizing: border-box;
  contain: layout;
}

.img-box {
  position: relative;
  display: inline-block;
  width: auto;
  max-width: 100%;
  max-height: 65vh;
  line-height: 0;
  border-radius: var(--r);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  background: rgba(0,0,0,0.03);
  margin: 0 auto;
  flex-shrink: 0;
  box-sizing: border-box;
}

#main-img-wrap, #extra-img-wrap, .cat-swapped-img-arena {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cat-swapped-img-arena {
  max-width: 820px;
  margin: 0 auto 16px;
}

.img-box img, #extra-img-wrap img, .cat-swapped-img-arena img {
  display: block;
  max-width: 100%;
  max-height: 65vh;
  width: auto;
  height: auto;
  margin: 0 auto;
  border-radius: var(--r);
  object-fit: contain;
  user-select: none;
  pointer-events: none;
}

#zones {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.dz {
  position: absolute;
  transform: translate(-50%, -50%);
  min-width: 76px;
  min-height: 30px;
  border: 1.5px dashed var(--dz-empty-border);
  border-radius: 8px;
  background: var(--dz-empty-bg);
  backdrop-filter: blur(2px);
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: all;
  transition: border-color 0.15s, background 0.15s, transform 0.15s;
  padding: 2px;
  z-index: 10;
  box-sizing: border-box;
}

.dz-hover {
  border-color: var(--accent) !important;
  background: rgba(37, 99, 235, 0.25) !important;
  transform: translate(-50%, -50%) scale(1.05);
}

.dz-ok,
.dz-err {
  border-color: transparent !important;
  background: transparent !important;
}

/* Zone Target Visual Cues during Click-to-Place */
.has-selected-chip .dz:not(.dz-ok):not(.dz-err) {
  cursor: pointer !important;
}

.has-selected-chip .dz.dz-cue-target {
  border-color: var(--accent) !important;
  background: rgba(37, 99, 235, 0.12) !important;
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.25) !important;
}

.dz-empty-cue {
  font-size: 10px;
  font-family: var(--font);
  font-weight: 600;
  color: var(--accent);
  letter-spacing: 0.02em;
  pointer-events: none;
  user-select: none;
  text-transform: lowercase;
}

/* Minimal Empty States */
.empty-state-badge {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 6px 14px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
  color: var(--muted);
  background: var(--surf);
  border: 1px solid var(--border);
  pointer-events: none;
  user-select: none;
  white-space: nowrap;
  z-index: 20;
}

.empty-pool-msg {
  width: 100%;
  text-align: center;
  font-size: 12px;
  color: var(--muted);
  font-weight: 500;
  padding: 6px 0;
  user-select: none;
}

.label-pool {
  width: 100% !important;
  box-sizing: border-box !important;
  display: flex !important;
  flex-wrap: wrap !important;
  justify-content: center !important;
  align-items: center !important;
  gap: 8px !important;
  padding: 12px 16px !important;
  background: var(--surf);
  border-radius: var(--r);
  border: 1px solid var(--border);
  min-height: 96px !important;
  margin-bottom: 8px !important;
  flex-shrink: 0 !important;
}

.chip {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 5px 12px;
  border-radius: 6px;
  border: 1.5px solid var(--border);
  background: var(--bg);
  color: var(--fg);
  font-size: 13px !important;
  line-height: 1.4 !important;
  font-weight: 500;
  cursor: grab;
  user-select: none;
  touch-action: none;
  white-space: nowrap;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.07);
  transition: transform 0.1s, box-shadow 0.1s;
}

.chip:active {
  cursor: grabbing;
  transform: scale(0.98);
}

.chip.chip-selected {
  outline: 2px solid var(--accent);
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.35);
  transform: scale(1.04);
}

/* ==========================================================================
   THEME-ADAPTIVE PLACED CHIPS (LIGHT & DARK MODE)
   ========================================================================== */

/* 1. Normal Placed Label (Front card - Clean Neutral Border) */
.dz .chip,
.drop-zone .chip {
  background: var(--chip-placed-bg) !important;
  background-color: var(--chip-placed-bg) !important;
  border: 1.5px solid var(--chip-placed-border) !important;
  color: var(--chip-placed-fg) !important;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.06) !important;
  font-size: 13px !important;
  line-height: 1.4 !important;
  font-weight: 500 !important;
  padding: 4px 11px !important;
  border-radius: 6px !important;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
  text-shadow: none !important;
}

/* 2. Correct Placed Label (Back card - Clean Minimal Default) */
.c-ok {
  background: var(--chip-ok-bg) !important;
  background-color: var(--chip-ok-bg) !important;
  color: var(--chip-ok-fg) !important;
  border: 1.5px solid var(--chip-ok-border) !important;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
  font-size: 13px !important;
  line-height: 1.4 !important;
  font-weight: 500 !important;
  border-radius: 6px !important;
  padding: 4px 11px !important;
  cursor: default;
  text-shadow: none !important;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
}

/* 3. Wrong Placed Label (Back card - Clean Minimal Default) */
.c-err {
  background: var(--chip-err-bg) !important;
  background-color: var(--chip-err-bg) !important;
  color: var(--chip-err-fg) !important;
  border: 1.5px solid var(--chip-err-border) !important;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
  font-size: 13px !important;
  line-height: 1.4 !important;
  font-weight: 500 !important;
  border-radius: 6px !important;
  padding: 4px 11px !important;
  cursor: default;
  text-shadow: none !important;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
}

/* 4. Missed Label (Back card - Clean Minimal Default) */
.c-miss {
  background: var(--chip-miss-bg) !important;
  background-color: var(--chip-miss-bg) !important;
  color: var(--chip-miss-fg) !important;
  border: 1.5px dashed var(--chip-miss-border) !important;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
  font-size: 13px !important;
  line-height: 1.4 !important;
  font-weight: 500 !important;
  border-radius: 6px !important;
  padding: 4px 11px !important;
  cursor: default;
  font-style: normal;
  text-shadow: none !important;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
}

/* Strikethrough & Target spans for clean feedback */
.chip-wrong {
  text-decoration: line-through;
  opacity: 0.65;
  margin-right: 6px;
  color: var(--chip-wrong-strike) !important;
  font-weight: 400 !important;
}

.chip-correct {
  font-weight: 600;
  color: var(--chip-correct-fg) !important;
}

/* ==========================================================================
   OPTIONAL: CALM COLORED FEEDBACK (WHEN ENABLED IN SETTINGS)
   ========================================================================== */
.colored-feedback .c-ok {
  background: #f0fdf4 !important;
  background-color: #f0fdf4 !important;
  color: #166534 !important;
  border: 1.5px solid #86efac !important;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04) !important;
}

.colored-feedback .c-err {
  background: #fef2f2 !important;
  background-color: #fef2f2 !important;
  color: #991b1b !important;
  border: 1.5px solid #fca5a5 !important;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04) !important;
}

.colored-feedback .c-miss {
  background: #f0fdf4 !important;
  background-color: #f0fdf4 !important;
  color: #166534 !important;
  border: 1.5px dashed #86efac !important;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04) !important;
}

.colored-feedback .chip-correct {
  color: #166534 !important;
}

/* Dark mode overrides for calm colored feedback */
html.night_mode .colored-feedback .c-ok,
html.nightMode .colored-feedback .c-ok,
.night_mode .colored-feedback .c-ok,
.nightMode .colored-feedback .c-ok,
body.night_mode .colored-feedback .c-ok,
body.nightMode .colored-feedback .c-ok,
.card.night_mode .colored-feedback .c-ok,
.card.nightMode .colored-feedback .c-ok {
  background: #14291f !important;
  background-color: #14291f !important;
  color: #86efac !important;
  border: 1.5px solid #166534 !important;
  box-shadow: none !important;
}

html.night_mode .colored-feedback .c-err,
html.nightMode .colored-feedback .c-err,
.night_mode .colored-feedback .c-err,
.nightMode .colored-feedback .c-err,
body.night_mode .colored-feedback .c-err,
body.nightMode .colored-feedback .c-err,
.card.night_mode .colored-feedback .c-err,
.card.nightMode .colored-feedback .c-err {
  background: #2b171a !important;
  background-color: #2b171a !important;
  color: #fca5a5 !important;
  border: 1.5px solid #7f1d1d !important;
  box-shadow: none !important;
}

html.night_mode .colored-feedback .c-miss,
html.nightMode .colored-feedback .c-miss,
.night_mode .colored-feedback .c-miss,
.nightMode .colored-feedback .c-miss,
body.night_mode .colored-feedback .c-miss,
body.nightMode .colored-feedback .c-miss,
.card.night_mode .colored-feedback .c-miss,
.card.nightMode .colored-feedback .c-miss {
  background: #14291f !important;
  background-color: #14291f !important;
  color: #86efac !important;
  border: 1.5px dashed #166534 !important;
  box-shadow: none !important;
}

html.night_mode .colored-feedback .chip-correct,
html.nightMode .colored-feedback .chip-correct,
.night_mode .colored-feedback .chip-correct,
.nightMode .colored-feedback .chip-correct,
body.night_mode .colored-feedback .chip-correct,
body.nightMode .colored-feedback .chip-correct,
.card.night_mode .colored-feedback .chip-correct,
.card.nightMode .colored-feedback .chip-correct {
  color: #86efac !important;
}

.colored-feedback .dz-ok,
.colored-feedback .dz-err {
  border-color: transparent !important;
  background: transparent !important;
}

.back-body {
  width: 100%;
  box-sizing: border-box;
  margin-top: 14px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  flex-shrink: 0;
  contain: layout;
}

.back-fade {
  opacity: 0;
  transform: translateY(5px);
  transition: opacity 0.25s, transform 0.25s;
}

.back-fade-in {
  opacity: 1;
  transform: translateY(0);
}

.section-label {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--muted);
  padding-top: 14px;
  border-top: 1px solid var(--border);
  margin-bottom: 10px;
  width: 100%;
  text-align: center;
}

.score {
  display: inline-block;
  font-size: 15px;
  font-weight: 700;
  padding: 8px 16px;
  border-radius: var(--r);
  border-left: 4px solid;
  background: var(--surf);
}

.s-ok {
  border-color: var(--ok);
  color: var(--ok);
}

.s-mid {
  border-color: var(--warn);
  color: var(--warn);
}

.s-bad {
  border-color: var(--err);
  color: var(--err);
}

.top-toolbar {
  position: fixed;
  top: 10px;
  right: 14px;
  z-index: 300;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 5px;
}

/* Anki Native Audio / Sound Play Button - Clean icon without square borders */
.audio-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: transparent !important;
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
  padding: 0 !important;
  margin: 0 !important;
}

.audio-btn a,
.audio-btn button,
.replay-button,
.replaybutton,
a.replay-button,
a.replaybutton,
a.soundLink,
button.soundLink,
.soundLink {
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  background: transparent !important;
  background-color: transparent !important;
  border: none !important;
  border-width: 0 !important;
  outline: none !important;
  box-shadow: none !important;
  padding: 0 !important;
  margin: 0 !important;
  border-radius: 0 !important;
  text-decoration: none !important;
  cursor: pointer !important;
}

.audio-btn svg,
.replay-button svg,
.replaybutton svg,
a.replay-button svg,
a.replaybutton svg,
a.soundLink svg,
.soundLink svg,
svg.playImage,
.playImage {
  border: none !important;
  border-width: 0 !important;
  outline: none !important;
  box-shadow: none !important;
  background: transparent !important;
  background-color: transparent !important;
}

.audio-btn svg circle,
.replay-button svg circle,
.replaybutton svg circle,
.playImage circle {
  border: none !important;
}

/* CONTROLS (Top-Right Vertical Stack) */
.ctrl {
  position: fixed;
  top: 14px;
  right: 14px;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 4px;
  z-index: 100;
}

/* BUTTONS – Minimalistic Text */
.ibtn {
  min-width: auto;
  height: 22px;
  padding: 0 6px;
  border-radius: 5px;
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 11px;
  font-weight: 500;
  color: #aaa;
  opacity: 0.65;
  transition: all 0.15s ease;
  line-height: 1;
}

.ibtn:hover {
  opacity: 1;
  color: #666;
  background: rgba(0, 0, 0, 0.04);
}

.ibtn.active {
  opacity: 1;
  color: #222;
  font-weight: 600;
  background: rgba(0, 0, 0, 0.06);
}

/* HIDDEN UTILITY */
.ms { display: none !important; }

/* EXTRA AREA (Text notes & images revealed by Extra/Image button) */
.extra-area {
  max-width: 940px;
  width: 94vw;
  margin: 22px auto 0;
  padding: 0 16px;
  font-size: 1.05rem;
  line-height: 1.55;
  color: #555;
  text-align: center;
  opacity: 0;
  max-height: 0;
  overflow: hidden;
  transition: opacity 0.2s ease, max-height 0.25s ease;
  box-sizing: border-box;
}

.extra-area.show {
  opacity: 1;
  max-height: 1000px;
}

.extra-area img {
  max-width: 100%;
  max-height: 60vh;
  height: auto;
  object-fit: contain;
  margin: 0 auto;
  border-radius: 6px;
  display: block;
}

/* Extra position: Above */
.extra-area.extra-above,
.extra-above .extra-area,
.extra-pos-above .extra-area {
  position: absolute !important;
  top: 48px !important;
  left: 50% !important;
  transform: translateX(-50%) !important;
  z-index: 90 !important;
  width: 92% !important;
  max-width: 820px !important;
  background: var(--surf) !important;
  border: 1px solid var(--border) !important;
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.25) !important;
  margin: 0 !important;
}

html.night_mode .extra-area.extra-above,
html.nightMode .extra-area.extra-above,
.night_mode .extra-area.extra-above,
.nightMode .extra-area.extra-above,
body.night_mode .extra-area.extra-above,
.card.night_mode .extra-area.extra-above {
  background: #202024 !important;
  border-color: #3f3f46 !important;
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.5) !important;
}

/* NIGHT MODE */
.nightMode .ibtn, .night_mode .ibtn, html.nightMode .ibtn, html.night_mode .ibtn { color: #777; opacity: 0.55; }
.nightMode .ibtn:hover, .night_mode .ibtn:hover, html.nightMode .ibtn:hover, html.night_mode .ibtn:hover { opacity: 0.9; color: #ccc; background: rgba(255,255,255,0.06); }
.nightMode .ibtn.active, .night_mode .ibtn.active, html.nightMode .ibtn.active, html.night_mode .ibtn.active { opacity: 1; color: #eee; background: rgba(255,255,255,0.1); }
.nightMode .extra-area, .night_mode .extra-area, html.nightMode .extra-area, html.night_mode .extra-area { color: #bbb; }

.toolbar-btn {
  background: var(--surf);
  border: 1px solid var(--border);
  border-radius: 50%;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  cursor: pointer;
  padding: 0;
  color: var(--fg);
}

.ddi-reveal-btn {
  background: var(--surf) !important;
  border: 1px solid var(--border) !important;
  border-radius: 6px !important;
  width: auto !important;
  height: auto !important;
  padding: 4px 10px !important;
  display: inline-flex !important;
  align-items: center !important;
  gap: 5px !important;
  font-size: 11px !important;
  font-weight: 500 !important;
  color: var(--fg) !important;
  cursor: pointer !important;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
  line-height: 1.3 !important;
  text-decoration: none !important;
}

.ddi-reveal-btn:hover {
  background: var(--bg) !important;
  border-color: var(--muted) !important;
}

.ddi-reveal-btn .reveal-chevron {
  font-size: 8px !important;
  opacity: 0.75;
}

.panel {
  width: 100%;
  max-width: 640px;
  margin: 12px auto 0;
  box-sizing: border-box;
  text-align: left;
  flex-shrink: 0;
  contain: content;
}

.img-panel {
  width: 100%;
  max-width: 640px;
  margin: 12px auto 0;
  text-align: center;
  box-sizing: border-box;
}

.panel-img-box {
  display: inline-block;
  max-width: 100%;
  border-radius: var(--r);
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border: 1px solid var(--border);
  background: var(--surf);
}

.panel-img-box img {
  display: block;
  max-width: 100%;
  max-height: 48vh;
  height: auto;
  margin: 0 auto;
  object-fit: contain;
}

.panel-body {
  padding: 12px 14px;
  font-size: 13px;
  line-height: 1.6;
  background: var(--surf);
  border-left: 3px solid var(--border);
  border-radius: var(--r);
}

.hint-bar {
  width: 100%;
  margin-top: 10px;
  font-size: 11px;
  color: var(--muted);
  text-align: center;
}

.hint-bar kbd {
  display: inline-block;
  padding: 1px 5px;
  border: 1px solid var(--border);
  border-radius: 4px;
  font-size: 10px;
  background: var(--surf);
  font-family: inherit;
}

/* Horizontal vs Vertical Layout Variations for Image Cards */
.ddi-wrap.layout-vertical,
.layout-vertical .ddi-wrap,
.layout-vertical.ddi-wrap {
  max-width: 1100px !important;
  flex-direction: row !important;
  align-items: flex-start !important;
  justify-content: center !important;
  gap: 24px !important;
}
.ddi-wrap.layout-vertical .upper-locked,
.layout-vertical .upper-locked {
  flex: 1 1 auto !important;
  min-width: 0 !important;
  align-items: center !important;
}
.ddi-wrap.layout-vertical .lower-flexible,
.layout-vertical .lower-flexible {
  width: 260px !important;
  max-width: 300px !important;
  flex-shrink: 0 !important;
  flex-grow: 0 !important;
  margin-top: 44px !important;
  align-items: stretch !important;
}
.ddi-wrap.layout-vertical .label-pool,
.layout-vertical .label-pool {
  flex-direction: column !important;
  align-items: stretch !important;
  max-height: 65vh !important;
  overflow-y: auto !important;
  gap: 8px !important;
  width: 100% !important;
}
.ddi-wrap.layout-vertical .back-body,
.layout-vertical .back-body {
  width: 100% !important;
}
@media (max-width: 768px) {
  .ddi-wrap.layout-vertical,
  .layout-vertical .ddi-wrap {
    flex-direction: column !important;
    align-items: center !important;
  }
  .ddi-wrap.layout-vertical .lower-flexible,
  .layout-vertical .lower-flexible {
    width: 100% !important;
    max-width: 100% !important;
    margin-top: 16px !important;
  }
  .ddi-wrap.layout-vertical .label-pool,
  .layout-vertical .label-pool {
    flex-direction: row !important;
    flex-wrap: wrap !important;
    max-height: none !important;
  }
}


/* Category Sorting Specific Layouts */
.cat-wrap {
  width: 100%;
  max-width: 920px;
  margin: 0 auto;
}

.categories-arena {
  width: 100%;
  box-sizing: border-box;
  margin-bottom: 16px;
}

.cat-arena-horizontal {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  grid-auto-rows: 1fr;
  align-items: stretch;
  gap: 12px;
  width: 100%;
  box-sizing: border-box;
}

.cat-arena-vertical {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
  box-sizing: border-box;
}

.cat-box {
  background: var(--surf);
  border: 1.5px solid var(--border);
  border-radius: var(--r);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 120px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
  box-sizing: border-box;
  transition: min-height 0.15s ease;
}

.cat-header {
  padding: 8px 12px;
  font-weight: 700;
  font-size: 13px;
  background: rgba(0, 0, 0, 0.03);
  border-bottom: 1px solid var(--border);
  color: var(--fg);
  text-align: center;
  letter-spacing: 0.02em;
  flex-shrink: 0;
}

.cat-drop-area {
  padding: 10px;
  min-height: 90px;
  flex: 1 1 auto;
  display: flex;
  flex-wrap: wrap;
  align-items: flex-start;
  align-content: flex-start;
  gap: 6px;
  transition: background-color 0.15s, border-color 0.15s, box-shadow 0.15s;
  box-sizing: border-box;
}

.cat-drop-cue {
  background: rgba(37, 99, 235, 0.04);
  box-shadow: inset 0 0 0 1.5px rgba(37, 99, 235, 0.25);
  cursor: pointer;
}

.cat-drop-hover {
  background: rgba(37, 99, 235, 0.12) !important;
  box-shadow: inset 0 0 0 2px var(--accent) !important;
}

/* Category Vertical Layout Adaptation */
.cat-wrap.layout-vertical,
.layout-vertical .cat-wrap {
  max-width: 1000px !important;
}

.cat-wrap.layout-vertical .cat-arena-vertical .cat-box {
  flex-direction: column;
}

@media (min-width: 769px) {
  .cat-wrap.layout-vertical .categories-arena {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
}
"""
CAT_FRONT_TEMPLATE = """<script>
function toggleImage(btn){
  var arena = document.getElementById('catArena');
  var extra = document.getElementById('cat-extra-img-wrap');
  if(!arena || !extra) return;
  var isSwapped = extra.style.display !== 'none';
  if(isSwapped){
    arena.style.display = '';
    extra.style.display = 'none';
    if(btn) btn.classList.remove('active');
  } else {
    arena.style.display = 'none';
    extra.style.display = 'flex';
    if(btn) btn.classList.add('active');
  }
}
function toggleExtra(btn){
  var source = document.getElementById('extra-src');
  var area = document.getElementById('extra-area');
  if(!source || !area) return;
  var isActive = area.classList.contains('show');
  if(isActive){
    area.innerHTML = '';
    area.classList.remove('show');
    if(btn) btn.classList.remove('active');
  } else {
    area.innerHTML = '<div class=\"extra-body\">' + source.innerHTML + '</div>';
    area.classList.add('show');
    if(btn) btn.classList.add('active');
  }
}
function toggle(id, btn){
  if(id === 'fimg' || id === 'bimg') toggleImage(btn);
  else toggleExtra(btn);
}
</script>
<div class=\"vp\">
  {{#Front Image}}<div id=\"fimg\" class=\"ms\">{{Front Image}}</div>{{/Front Image}}
  {{#Extra}}<div id=\"extra-src\" class=\"ms\">{{Extra}}</div>{{/Extra}}

  <div class=\"ctrl\">
    {{#Front Audio}}<div class=\"audio-btn\">{{Front Audio}}</div>{{/Front Audio}}
    <button type=\"button\" id=\"cat-undo-btn\" class=\"ibtn\" style=\"display:none;\" onclick=\"_catUndo(event)\" title=\"Undo last placement (Ctrl+Z / ⌘Z)\">undo</button>
    {{#Front Image}}
    <button type=\"button\" class=\"ibtn\" data-label=\"image\" onclick=\"toggleImage(this)\" title=\"Image\">image</button>
    {{/Front Image}}
    {{#Extra}}
    <button type=\"button\" class=\"ibtn\" data-label=\"extra\" onclick=\"toggleExtra(this)\" title=\"Extra\">extra</button>
    {{/Extra}}
  </div>

  <span id=\"cat-categories\" style=\"display:none\">{{Categories}}</span>
  <span id=\"cat-items\" style=\"display:none\">{{Items}}</span>
  <span id=\"cat-distractors\" style=\"display:none\">{{Distractors}}</span>
  <span id=\"cat-layout\" style=\"display:none\">{{Layout}}</span>

  <div class=\"ddi-wrap cat-wrap {{#Layout}}layout-{{Layout}}{{/Layout}}\">
    <div class=\"upper-locked\">
      <div class=\"meta\">{{Title}}</div>
      <h1 class=\"question\">{{Question}}</h1>
      <div class=\"categories-arena\" id=\"catArena\"></div>
      {{#Front Image}}<div id=\"cat-extra-img-wrap\" class=\"cat-swapped-img-arena\" style=\"display:none;\">{{Front Image}}</div>{{/Front Image}}
    </div>
    <div class=\"lower-flexible\">
      <div class=\"label-pool\" id=\"catPool\"></div>
    </div>
  </div>

  <div id=\"extra-area\" class=\"extra-area\"></div>
</div>

<script>
function _catInit(){
  try {
    var isDark = document.body.classList.contains('night_mode') || 
                 document.body.classList.contains('nightMode') || 
                 document.documentElement.classList.contains('night_mode') || 
                 document.documentElement.classList.contains('nightMode');
    if (!isDark && window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      document.documentElement.setAttribute('data-anki-light', 'true');
    }
  } catch(e){}

  function decodeEntities(str){
    var d = document.createElement('div');
    d.innerHTML = str;
    return d.textContent || d.innerText || str;
  }
  function stripTags(str){
    var d = document.createElement('div');
    d.innerHTML = str;
    return d.textContent || d.innerText || '';
  }
  function splitField(str){
    str = decodeEntities(str); str = stripTags(str);
    var parts = str.split('|');
    if(parts.length <= 1) parts = str.split('&#124;');
    return parts.map(function(s){ return s.trim(); }).filter(Boolean);
  }
  function parseItems(str){
    str = decodeEntities(str); str = stripTags(str);
    var parts = str.split('|');
    if(parts.length <= 1) parts = str.split('&#124;');
    var result = [];
    parts.forEach(function(p){
      p = p.trim();
      if(!p) return;
      var eq = p.indexOf('=');
      if(eq > 0){
        result.push({ item: p.slice(0, eq).trim(), category: p.slice(eq + 1).trim() });
      }
    });
    return result;
  }

  var CARD_KEY = (\"{{Title}}_{{Question}}\").replace(/[^a-zA-Z0-9]/g, '_');

  // Restore previously-placed items if Anki redrew this same question (e.g.
  // after Mark Note or another note-text change elsewhere), using the same
  // {key, placed} data saveState() already writes below. Mirrors the read
  // pattern category_back.html uses, but only restores when the stored key
  // matches this exact card, so a different/new card never inherits it.
  var restoredPlaced = {};
  try {
    var _raw = '';
    var _h = location.hash;
    if(_h && _h.indexOf('ddcat=') >= 0) _raw = decodeURIComponent(_h.slice(_h.indexOf('ddcat=') + 6));
    else if(_h && _h.indexOf('ddi=') >= 0) _raw = decodeURIComponent(_h.slice(_h.indexOf('ddi=') + 4));
    if(!_raw){
      try { _raw = sessionStorage.getItem('ddcat_' + CARD_KEY) || sessionStorage.getItem('ddcat') || sessionStorage.getItem('ddi') || ''; } catch(e){}
    }
    if(_raw){
      var _parsed = JSON.parse(_raw);
      if(_parsed.key === CARD_KEY) restoredPlaced = _parsed.placed || {};
    }
  } catch(e){ restoredPlaced = {}; }
  var categories = splitField(document.getElementById('cat-categories')?.innerHTML || '');
  var items = parseItems(document.getElementById('cat-items')?.innerHTML || '');
  var distractors = splitField(document.getElementById('cat-distractors')?.innerHTML || '');
  var rawLayout = (decodeEntities(stripTags(document.getElementById('cat-layout')?.innerHTML || '')) || 'horizontal').trim().toLowerCase();

  var poolLabels = items.map(function(i){ return i.item; }).concat(distractors);

  // Shuffle pool labels
  for (var i = poolLabels.length - 1; i > 0; i--) {
    var j = Math.floor(Math.random() * (i + 1));
    var temp = poolLabels[i];
    poolLabels[i] = poolLabels[j];
    poolLabels[j] = temp;
  }

  var arena = document.getElementById('catArena');
  var pool = document.getElementById('catPool');
  if(!arena || !pool) return;
  arena.innerHTML = '';
  pool.innerHTML = '';

  if(rawLayout === 'vertical'){
    arena.className = 'categories-arena cat-arena-vertical';
  } else {
    arena.className = 'categories-arena cat-arena-horizontal';
  }

  var placedState = restoredPlaced;
  var history = [];
  var selectedChip = null;
  var draggedItem = null;

  categories.forEach(function(cat){
    var box = document.createElement('div');
    box.className = 'cat-box';
    box.setAttribute('data-category', cat);

    var header = document.createElement('div');
    header.className = 'cat-header';
    header.textContent = cat;
    box.appendChild(header);

    var dropArea = document.createElement('div');
    dropArea.className = 'cat-drop-area';
    dropArea.setAttribute('data-category', cat);

    dropArea.addEventListener('dragover', function(e){ 
      e.preventDefault(); 
      dropArea.classList.add('cat-drop-hover'); 
    });
    dropArea.addEventListener('dragleave', function(e){ 
      if(!dropArea.contains(e.relatedTarget)){
        dropArea.classList.remove('cat-drop-hover');
      }
    });
    dropArea.addEventListener('drop', function(e){
      e.preventDefault();
      dropArea.classList.remove('cat-drop-hover');
      var itemText = e.dataTransfer.getData('text/plain') || draggedItem;
      if(itemText) placeItem(itemText, cat);
      draggedItem = null;
    });

    dropArea.addEventListener('click', function(e){
      if(selectedChip){
        var itemText = selectedChip.getAttribute('data-item');
        if(itemText) placeItem(itemText, cat);
        selectedChip.classList.remove('chip-selected');
        selectedChip = null;
        updateCues();
      }
    });

    box.appendChild(dropArea);
    arena.appendChild(box);
  });

  function updateUndoBtn(){
    var undoBtn = document.getElementById('cat-undo-btn');
    if(undoBtn) undoBtn.style.display = history.length > 0 ? 'inline-flex' : 'none';
  }

  function saveState(){
    var state = { key: CARD_KEY, placed: placedState };
    try { location.hash = 'ddcat=' + encodeURIComponent(JSON.stringify(state)); } catch(e){}
    try { sessionStorage.setItem('ddcat', JSON.stringify(state)); } catch(e){}
    try { sessionStorage.setItem('ddcat_' + CARD_KEY, JSON.stringify(state)); } catch(e){}
    try { sessionStorage.setItem('ddi', JSON.stringify(state)); } catch(e){}
    updateUndoBtn();
  }

  function placeItem(itemText, cat){
    if(placedState[itemText] === cat) return;
    history.push({ item: itemText, from: placedState[itemText] || null, to: cat });
    placedState[itemText] = cat;
    renderAll();
    saveState();
  }

  function unplaceItem(itemText){
    if(placedState[itemText]){
      history.push({ item: itemText, from: placedState[itemText], to: null });
      delete placedState[itemText];
      renderAll();
      saveState();
    }
  }

  window._catUndo = function(e){
    if(e && e.stopPropagation) e.stopPropagation();
    var last = history.pop();
    if(!last) return;
    if(last.from){
      placedState[last.item] = last.from;
    } else {
      delete placedState[last.item];
    }
    selectedChip = null;
    renderAll();
    saveState();
  };

  function updateCues(){
    var hasSel = !!selectedChip;
    document.querySelectorAll('.cat-drop-area').forEach(function(da){
      if(hasSel){
        da.classList.add('cat-drop-cue');
      } else {
        da.classList.remove('cat-drop-cue');
      }
    });
  }

  function renderAll(){
    pool.innerHTML = '';
    document.querySelectorAll('.cat-drop-area').forEach(function(da){ da.innerHTML = ''; });

    var unplacedCount = 0;
    poolLabels.forEach(function(label){
      var placedCat = placedState[label];
      var chip = document.createElement('div');
      chip.className = 'chip';
      chip.textContent = label;
      chip.setAttribute('data-item', label);
      chip.setAttribute('draggable', 'true');

      chip.addEventListener('dragstart', function(e){
        draggedItem = label;
        e.dataTransfer.setData('text/plain', label);
        setTimeout(function(){ chip.style.opacity = '.3'; }, 0);
      });
      chip.addEventListener('dragend', function(){
        chip.style.opacity = '1';
        draggedItem = null;
      });

      chip.addEventListener('click', function(e){
        e.stopPropagation();
        if(placedCat){
          // Clicking placed chip: if another chip is selected, place that one; else return this one to pool
          if(selectedChip && selectedChip !== chip){
            var itemText = selectedChip.getAttribute('data-item');
            if(itemText) placeItem(itemText, placedCat);
            selectedChip.classList.remove('chip-selected');
            selectedChip = null;
            updateCues();
            return;
          }
          unplaceItem(label);
        } else {
          // In pool: toggle selection
          if(selectedChip === chip){
            chip.classList.remove('chip-selected');
            selectedChip = null;
          } else {
            if(selectedChip) selectedChip.classList.remove('chip-selected');
            selectedChip = chip;
            chip.classList.add('chip-selected');
          }
        }
        updateCues();
      });

      if(placedCat){
        var targetArea = null;
        document.querySelectorAll('.cat-drop-area').forEach(function(da){
          if(da.getAttribute('data-category') === placedCat) targetArea = da;
        });
        if(targetArea) targetArea.appendChild(chip);
      } else {
        unplacedCount++;
        pool.appendChild(chip);
      }
    });

    if(unplacedCount === 0){
      var emptyMsg = document.createElement('div');
      emptyMsg.className = 'empty-pool-msg';
      emptyMsg.textContent = poolLabels.length === 0 ? 'No items' : 'All items placed · Press Space to check answers';
      pool.appendChild(emptyMsg);
    }

    equalizeBoxHeights();
  }

  function equalizeBoxHeights(){
    var boxes = document.querySelectorAll('.cat-box');
    if(!boxes.length) return;
    var maxH = 120;
    boxes.forEach(function(b){ b.style.minHeight = ''; });
    boxes.forEach(function(b){
      var h = b.getBoundingClientRect().height;
      if(h > maxH) maxH = h;
    });
    boxes.forEach(function(b){ b.style.minHeight = maxH + 'px'; });
  }

  window.addEventListener('resize', equalizeBoxHeights);

  // Pool drag & drop back
  pool.addEventListener('dragover', function(e){ 
    e.preventDefault(); 
    pool.classList.add('cat-drop-hover');
  });
  pool.addEventListener('dragleave', function(e){ 
    if(!pool.contains(e.relatedTarget)){
      pool.classList.remove('cat-drop-hover');
    }
  });
  pool.addEventListener('drop', function(e){
    e.preventDefault();
    pool.classList.remove('cat-drop-hover');
    var itemText = e.dataTransfer.getData('text/plain') || draggedItem;
    if(itemText) unplaceItem(itemText);
    draggedItem = null;
  });

  pool.addEventListener('click', function(e){
    if(e.target === pool && selectedChip){
      var itemText = selectedChip.getAttribute('data-item');
      if(itemText) unplaceItem(itemText);
      selectedChip.classList.remove('chip-selected');
      selectedChip = null;
      updateCues();
    }
  });

  // Touch handlers for mobile devices
  var ti = null, tc = null;
  document.addEventListener('touchstart', function(e){
    var item = e.target.closest('.chip');
    if(!item) return;
    ti = item;
    var r = item.getBoundingClientRect();
    tc = item.cloneNode(true);
    tc.style.cssText = 'position:fixed;z-index:9999;pointer-events:none;opacity:.85;left:' + r.left + 'px;top:' + r.top + 'px;width:' + r.width + 'px;margin:0;';
    document.body.appendChild(tc);
    item.style.opacity = '.3';
  }, { passive: true });

  document.addEventListener('touchmove', function(e){
    if(!tc) return;
    e.preventDefault();
    var t = e.touches[0];
    tc.style.left = (t.clientX - tc.offsetWidth / 2) + 'px';
    tc.style.top = (t.clientY - tc.offsetHeight / 2) + 'px';
    tc.style.display = 'none';
    var hit = document.elementFromPoint(t.clientX, t.clientY);
    tc.style.display = '';
    document.querySelectorAll('.cat-drop-area, #catPool').forEach(function(d){ d.classList.remove('cat-drop-hover'); });
    var da = hit && hit.closest('.cat-drop-area, #catPool');
    if(da) da.classList.add('cat-drop-hover');
  }, { passive: false });

  document.addEventListener('touchend', function(e){
    if(!ti || !tc) return;
    var t = e.changedTouches[0];
    tc.style.display = 'none';
    var hit = document.elementFromPoint(t.clientX, t.clientY);
    tc.remove(); tc = null; ti.style.opacity = '1';
    document.querySelectorAll('.cat-drop-area, #catPool').forEach(function(d){ d.classList.remove('cat-drop-hover'); });
    var da = hit && hit.closest('.cat-drop-area, #catPool');
    var label = ti.getAttribute('data-item');
    if(da && label){
      if(da.id === 'catPool' || da.classList.contains('label-pool')){
        unplaceItem(label);
      } else {
        var cat = da.getAttribute('data-category');
        if(cat) placeItem(label, cat);
      }
    }
    ti = null;
  });

  // Keyboard shortcut listener
  document.addEventListener('keydown', function(e){
    if((e.ctrlKey || e.metaKey) && (e.key === 'z' || e.key === 'Z' || e.code === 'KeyZ')){
      e.preventDefault();
      window._catUndo();
      return;
    }
    if(e.code === 'Space' || e.key === ' '){
      e.preventDefault();
      var btn = document.querySelector('#answer, .btn-primary, [id*=\"answer\"]');
      if(btn) btn.click();
      else document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', keyCode: 13, bubbles: true }));
    }
  });

  renderAll();
  saveState();
}

if(document.readyState === 'loading'){
  document.addEventListener('DOMContentLoaded', _catInit);
} else {
  _catInit();
}
</script>"""
CAT_BACK_TEMPLATE = """<script>
function toggleImage(btn){
  var arena = document.getElementById('catArena');
  var extra = document.getElementById('cat-extra-img-wrap');
  if(!arena || !extra) return;
  var isSwapped = extra.style.display !== 'none';
  if(isSwapped){
    arena.style.display = '';
    extra.style.display = 'none';
    if(btn) btn.classList.remove('active');
  } else {
    arena.style.display = 'none';
    extra.style.display = 'flex';
    if(btn) btn.classList.add('active');
  }
}
function toggleExtra(btn){
  var source = document.getElementById('extra-src');
  var area = document.getElementById('extra-area');
  if(!source || !area) return;
  var isActive = area.classList.contains('show');
  if(isActive){
    area.innerHTML = '';
    area.classList.remove('show');
    if(btn) btn.classList.remove('active');
  } else {
    area.innerHTML = '<div class=\"extra-body\">' + source.innerHTML + '</div>';
    area.classList.add('show');
    if(btn) btn.classList.add('active');
  }
}
function toggle(id, btn){
  if(id === 'fimg' || id === 'bimg') toggleImage(btn);
  else toggleExtra(btn);
}
</script>
<div class=\"vp\">
  {{#Back Image}}<div id=\"bimg\" class=\"ms\">{{Back Image}}</div>{{/Back Image}}
  {{#Extra}}<div id=\"extra-src\" class=\"ms\">{{Extra}}</div>{{/Extra}}

  <div class=\"ctrl\">
    {{#Back Audio}}<div class=\"audio-btn\">{{Back Audio}}</div>{{/Back Audio}}
    {{#Back Image}}
    <button type=\"button\" class=\"ibtn\" data-label=\"image\" onclick=\"toggleImage(this)\" title=\"Image\">image</button>
    {{/Back Image}}
    {{#Extra}}
    <button type=\"button\" class=\"ibtn\" data-label=\"extra\" onclick=\"toggleExtra(this)\" title=\"Extra\">extra</button>
    {{/Extra}}
  </div>

  <span id=\"cat-categories\" style=\"display:none\">{{Categories}}</span>
  <span id=\"cat-items\" style=\"display:none\">{{Items}}</span>
  <span id=\"cat-distractors\" style=\"display:none\">{{Distractors}}</span>
  <span id=\"cat-layout\" style=\"display:none\">{{Layout}}</span>

  <div class=\"ddi-wrap cat-wrap {{#Layout}}layout-{{Layout}}{{/Layout}}\">
    <div class=\"upper-locked\">
      <div class=\"meta\">{{Title}}</div>
      <h1 class=\"question\">{{Question}}</h1>
      <div class=\"categories-arena\" id=\"catArena\"></div>
      {{#Back Image}}<div id=\"cat-extra-img-wrap\" class=\"cat-swapped-img-arena\" style=\"display:none;\">{{Back Image}}</div>{{/Back Image}}
    </div>
    <div class=\"lower-flexible\">
      <div class=\"label-pool\" id=\"catPool\"></div>
      <div class=\"back-body\">
        <div class=\"section-label\">Resultat</div>
        <div id=\"catScoreBox\"></div>
      </div>
    </div>
  </div>

  <div id=\"extra-area\" class=\"extra-area\"></div>
</div>

<script>
(function(){
  try {
    var isDark = document.body.classList.contains('night_mode') || 
                 document.body.classList.contains('nightMode') || 
                 document.documentElement.classList.contains('night_mode') || 
                 document.documentElement.classList.contains('nightMode');
    if (!isDark && window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      document.documentElement.setAttribute('data-anki-light', 'true');
    }
  } catch(e){}

  function decodeEntities(str){
    var d = document.createElement('div');
    d.innerHTML = str;
    return d.textContent || d.innerText || str;
  }
  function stripTags(str){
    var d = document.createElement('div');
    d.innerHTML = str;
    return d.textContent || d.innerText || '';
  }
  function splitField(str){
    str = decodeEntities(str); str = stripTags(str);
    var parts = str.split('|');
    if(parts.length <= 1) parts = str.split('&#124;');
    return parts.map(function(s){ return s.trim(); }).filter(Boolean);
  }
  function parseItems(str){
    str = decodeEntities(str); str = stripTags(str);
    var parts = str.split('|');
    if(parts.length <= 1) parts = str.split('&#124;');
    var result = [];
    parts.forEach(function(p){
      p = p.trim();
      if(!p) return;
      var eq = p.indexOf('=');
      if(eq > 0){
        result.push({ item: p.slice(0, eq).trim(), category: p.slice(eq + 1).trim() });
      }
    });
    return result;
  }

  var CARD_KEY = (\"{{Title}}_{{Question}}\").replace(/[^a-zA-Z0-9]/g, '_');
  var categories = splitField(document.getElementById('cat-categories')?.innerHTML || '');
  var items = parseItems(document.getElementById('cat-items')?.innerHTML || '');
  var distractors = splitField(document.getElementById('cat-distractors')?.innerHTML || '');
  var rawLayout = (decodeEntities(stripTags(document.getElementById('cat-layout')?.innerHTML || '')) || 'horizontal').trim().toLowerCase();

  var expectedMap = {};
  var allValidItems = [];
  items.forEach(function(pair){
    expectedMap[pair.item] = pair.category;
    allValidItems.push(pair.item);
  });

  var placed = {};
  var raw = '';
  try {
    var h = location.hash;
    if(h && h.indexOf('ddcat=') >= 0) raw = decodeURIComponent(h.slice(h.indexOf('ddcat=') + 6));
    else if(h && h.indexOf('ddi=') >= 0) raw = decodeURIComponent(h.slice(h.indexOf('ddi=') + 4));
  } catch(e){}
  if(!raw){
    try { raw = sessionStorage.getItem('ddcat_' + CARD_KEY) || sessionStorage.getItem('ddcat') || sessionStorage.getItem('ddi') || ''; } catch(e){}
  }
  try {
    if(raw){
      var parsed = JSON.parse(raw);
      placed = parsed.placed || parsed;
    }
  } catch(e){ placed = {}; }

  var arena = document.getElementById('catArena');
  var pool = document.getElementById('catPool');
  if(!arena || !pool) return;
  arena.innerHTML = '';
  pool.innerHTML = '';

  if(rawLayout === 'vertical'){
    arena.className = 'categories-arena cat-arena-vertical';
  } else {
    arena.className = 'categories-arena cat-arena-horizontal';
  }

  var total = allValidItems.length;
  var got = 0;

  // Build each category on the back with evaluated answers
  categories.forEach(function(cat){
    var box = document.createElement('div');
    box.className = 'cat-box';

    var header = document.createElement('div');
    header.className = 'cat-header';
    header.textContent = cat;
    box.appendChild(header);

    var dropArea = document.createElement('div');
    dropArea.className = 'cat-drop-area';
    dropArea.setAttribute('data-category', cat);

    // 1. Check all items placed by user in this category
    Object.keys(placed).forEach(function(item){
      if(placed[item] === cat){
        var isOk = (expectedMap[item] === cat);
        var chip = document.createElement('div');
        if(isOk){
          got++;
          chip.className = 'chip c-ok';
          chip.textContent = item;
        } else {
          chip.className = 'chip c-err';
          var correctCat = expectedMap[item];
          if(correctCat){
            chip.innerHTML = '<span class=\"chip-wrong\">' + item + '</span> <span class=\"chip-correct\">' + correctCat + '</span>';
          } else {
            chip.innerHTML = '<span class=\"chip-wrong\">' + item + '</span> <span class=\"chip-correct\">Decoy</span>';
          }
        }
        dropArea.appendChild(chip);
      }
    });

    // 2. Add missed items that should have been in this category but were not placed in this category
    allValidItems.forEach(function(item){
      if(expectedMap[item] === cat && placed[item] !== cat){
        var missChip = document.createElement('div');
        missChip.className = 'chip c-miss';
        missChip.innerHTML = '<span class=\"chip-correct\">' + item + '</span>';
        dropArea.appendChild(missChip);
      }
    });

    box.appendChild(dropArea);
    arena.appendChild(box);
  });

  function equalizeBoxHeights(){
    var boxes = document.querySelectorAll('.cat-box');
    if(!boxes.length) return;
    var maxH = 120;
    boxes.forEach(function(b){ b.style.minHeight = ''; });
    boxes.forEach(function(b){
      var h = b.getBoundingClientRect().height;
      if(h > maxH) maxH = h;
    });
    boxes.forEach(function(b){ b.style.minHeight = maxH + 'px'; });
  }
  equalizeBoxHeights();
  window.addEventListener('resize', equalizeBoxHeights);

  // Pool: show unplaced items/distractors
  var allPoolLabels = allValidItems.concat(distractors);
  var unplacedInPool = 0;
  allPoolLabels.forEach(function(item){
    if(!placed[item]){
      unplacedInPool++;
      var c = document.createElement('div');
      c.className = 'chip';
      c.style.opacity = '.6';
      c.textContent = item;
      pool.appendChild(c);
    }
  });

  if(unplacedInPool === 0){
    var emptyMsg = document.createElement('div');
    emptyMsg.className = 'empty-pool-msg';
    emptyMsg.textContent = allPoolLabels.length === 0 ? 'No items' : 'All items placed';
    pool.appendChild(emptyMsg);
  }

  // Score Box evaluation
  var pct = total ? Math.round(got / total * 100) : 0;
  var scls = pct === 100 ? 's-ok' : (pct >= 50 ? 's-mid' : 's-bad');
  var sb = document.getElementById('catScoreBox');
  if(sb){
    sb.innerHTML = '<div class=\"score ' + scls + '\">' + got + ' / ' + total + ' korrekte (' + pct + '%)</div>';
  }

  document.addEventListener('keydown', function(e){
    if(e.code === 'Space' || e.key === ' ') e.preventDefault();
  });
}());
</script>"""



def is_anki_dark_mode() -> bool:
    """Detects if Anki is currently in Dark / Night mode."""
    try:
        if mw:
            if hasattr(mw, "themeManager") and hasattr(mw.themeManager, "night_mode"):
                return bool(mw.themeManager.night_mode)
            if hasattr(mw, "pm") and hasattr(mw.pm, "night_mode"):
                return bool(mw.pm.night_mode())
            if hasattr(mw, "palette"):
                return mw.palette().window().color().lightness() < 128
    except Exception:
        pass
    try:
        from aqt import qApp
        if qApp:
            return qApp.palette().window().color().lightness() < 128
    except Exception:
        pass
    return False


def get_font_family_css(font_family: str) -> str:
    if not font_family or font_family in ["System Default", "system", "default", ""]:
        return 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif'
    return f'"{font_family}", system-ui, -apple-system, sans-serif'


def get_font_size_css(font_size) -> str:
    try:
        size = int(font_size)
    except (ValueError, TypeError):
        size = 16

    q_size = round(size * 1.375)
    meta_size = max(10, round(size * 0.6875))
    chip_size = max(11, round(size * 0.8125))
    cat_hdr = chip_size
    score_size = max(12, round(size * 0.875))
    cue_size = max(9, round(size * 0.625))

    pad_y = max(3, round(size * 0.25))
    pad_x = max(8, round(size * 0.6875))

    return f"""
/* Font Size: {size}px */
:root, html, body, .card {{
  font-size: {size}px !important;
}}
.question {{
  font-size: {q_size}px !important;
}}
.meta {{
  font-size: {meta_size}px !important;
}}
.chip, .dz .chip, .drop-zone .chip, .cat-drop-area .chip {{
  font-size: {chip_size}px !important;
  padding: {pad_y}px {pad_x}px !important;
}}
.cat-header {{
  font-size: {cat_hdr}px !important;
}}
.score {{
  font-size: {score_size}px !important;
}}
.dz-empty-cue {{
  font-size: {cue_size}px !important;
}}
"""


def generate_dynamic_css(config: dict) -> str:
    """Generates card styling with automatic Anki dark mode and customizable midcenter alignment."""
    center_mid = config.get("center_image_midcenter", False)
    max_w = config.get("max_card_width_px", 920)
    max_h = config.get("max_image_height_vh", 68)
    theme_mode = config.get("theme_mode", "auto")
    font_family = config.get("font_family", "")
    font_size = config.get("font_size", 16)

    max_w_str = f"{max_w}px" if max_w < 9000 else "100%"
    max_h_str = f"{max_h}vh" if max_h < 100 else "none"

    custom_css = BASE_CSS

    font_css = get_font_family_css(font_family)
    custom_css += f"""
:root, html, body, .card {{
  --font: {font_css} !important;
  font-family: {font_css} !important;
}}
"""
    custom_css += get_font_size_css(font_size)

    # Sizing and alignment overrides
    custom_css += f"""
.ddi-wrap {{
  max-width: {max_w_str} !important;
}}
.img-box, .img-arena, .img-box img {{
  max-height: {max_h_str} !important;
}}
"""

    if center_mid:
        custom_css += """
/* Midcenter mode: Visually centered on screen with stable top anchor to prevent vertical jump */
html, body {
  min-height: 100% !important;
  margin: 0 !important;
  padding: 0 !important;
  display: block !important;
  overflow-y: auto !important;
}

.card {
  min-height: 100vh !important;
  height: auto !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: flex-start !important;
  padding-top: max(24px, calc(48vh - 330px)) !important;
  padding-bottom: 48px !important;
  margin: 0 !important;
  box-sizing: border-box !important;
}

.ddi-wrap {
  margin: 0 auto !important;
}
"""

    if theme_mode == "light":
        custom_css += """
:root, html, body, .card {
  --bg: #ffffff !important;
  --fg: #1c1c1c !important;
  --muted: #8e8e93 !important;
  --border: #e2e8f0 !important;
  --surf: #f8fafc !important;
  --chip-placed-bg: #ffffff !important;
  --chip-placed-fg: #0f172a !important;
  --chip-placed-border: #94a3b8 !important;
  --chip-ok-bg: #ffffff !important;
  --chip-ok-fg: #0f172a !important;
  --chip-ok-border: #94a3b8 !important;
  --chip-err-bg: #ffffff !important;
  --chip-err-fg: #0f172a !important;
  --chip-err-border: #94a3b8 !important;
  --chip-miss-bg: #ffffff !important;
  --chip-miss-fg: #15803d !important;
  --chip-miss-border: #94a3b8 !important;
  --chip-wrong-strike: #64748b !important;
  --chip-correct-fg: #15803d !important;
  --dz-empty-border: rgba(148, 163, 184, 0.75) !important;
  --dz-empty-bg: rgba(255, 255, 255, 0.6) !important;
}
"""
    elif theme_mode == "dark":
        custom_css += """
:root, html, body, .card {
  --bg: #18181b !important;
  --fg: #f4f4f5 !important;
  --muted: #a1a1aa !important;
  --border: #27272a !important;
  --surf: #27272a !important;
  --chip-placed-bg: #22242a !important;
  --chip-placed-fg: #f1f5f9 !important;
  --chip-placed-border: #3f3f46 !important;
  --chip-ok-bg: #22242a !important;
  --chip-ok-fg: #f1f5f9 !important;
  --chip-ok-border: #3f3f46 !important;
  --chip-err-bg: #22242a !important;
  --chip-err-fg: #f1f5f9 !important;
  --chip-err-border: #3f3f46 !important;
  --chip-miss-bg: #22242a !important;
  --chip-miss-fg: #4ade80 !important;
  --chip-miss-border: #52525b !important;
  --chip-wrong-strike: #94a3b8 !important;
  --chip-correct-fg: #4ade80 !important;
  --dz-empty-border: rgba(113, 113, 122, 0.7) !important;
  --dz-empty-bg: rgba(0, 0, 0, 0.4) !important;
}
"""

    if config.get("use_colored_feedback", False):
        custom_css += """
/* Calm colored feedback mode */
.c-ok {
  background: #f0fdf4 !important;
  background-color: #f0fdf4 !important;
  color: #166534 !important;
  border: 1.5px solid #86efac !important;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04) !important;
}
.c-err {
  background: #fef2f2 !important;
  background-color: #fef2f2 !important;
  color: #991b1b !important;
  border: 1.5px solid #fca5a5 !important;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04) !important;
}
.c-miss {
  background: #f0fdf4 !important;
  background-color: #f0fdf4 !important;
  color: #166534 !important;
  border: 1.5px dashed #86efac !important;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04) !important;
}
.chip-correct {
  color: #166534 !important;
}
html.night_mode .c-ok, html.nightMode .c-ok, body.night_mode .c-ok, .card.night_mode .c-ok {
  background: #14291f !important;
  background-color: #14291f !important;
  color: #86efac !important;
  border: 1.5px solid #166534 !important;
  box-shadow: none !important;
}
html.night_mode .c-err, html.nightMode .c-err, body.night_mode .c-err, .card.night_mode .c-err {
  background: #2b171a !important;
  background-color: #2b171a !important;
  color: #fca5a5 !important;
  border: 1.5px solid #7f1d1d !important;
  box-shadow: none !important;
}
html.night_mode .c-miss, html.nightMode .c-miss, body.night_mode .c-miss, .card.night_mode .c-miss {
  background: #14291f !important;
  background-color: #14291f !important;
  color: #86efac !important;
  border: 1.5px dashed #166534 !important;
  box-shadow: none !important;
}
html.night_mode .chip-correct, html.nightMode .chip-correct, body.night_mode .chip-correct, .card.night_mode .chip-correct {
  color: #86efac !important;
}
.dz-ok, .dz-err {
  border-color: transparent !important;
  background: transparent !important;
}
"""
    return custom_css


def generate_dynamic_category_css(config: dict) -> str:
    """Generates Category card styling with theme and customizable midcenter alignment."""
    center_mid = config.get("cat_center_card", False) or config.get("center_image_midcenter", False)
    theme_mode = config.get("theme_mode", "auto")
    font_family = config.get("font_family", "system")
    font_size = config.get("font_size", "medium")

    custom_css = CAT_BASE_CSS

    font_css = get_font_family_css(font_family)
    custom_css += f"""
:root, html, body, .card {{
  --font: {font_css} !important;
  font-family: {font_css} !important;
}}
"""
    custom_css += get_font_size_css(font_size)

    if center_mid:
        custom_css += """
/* Category Midcenter mode: Visually centered on screen with stable top anchor to prevent vertical jump */
html, body {
  min-height: 100% !important;
  margin: 0 !important;
  padding: 0 !important;
  display: block !important;
  overflow-y: auto !important;
}

.card {
  min-height: 100vh !important;
  height: auto !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: flex-start !important;
  padding-top: max(24px, calc(48vh - 330px)) !important;
  padding-bottom: 48px !important;
  margin: 0 !important;
  box-sizing: border-box !important;
}

.cat-wrap, .ddi-wrap {
  margin: 0 auto !important;
}
"""

    if theme_mode == "light":
        custom_css += """
:root, html, body, .card {
  --bg: #ffffff !important;
  --fg: #1c1c1c !important;
  --muted: #8e8e93 !important;
  --border: #e2e8f0 !important;
  --surf: #f8fafc !important;
  --chip-placed-bg: #ffffff !important;
  --chip-placed-fg: #0f172a !important;
  --chip-placed-border: #94a3b8 !important;
  --chip-ok-bg: #ffffff !important;
  --chip-ok-fg: #0f172a !important;
  --chip-ok-border: #94a3b8 !important;
  --chip-err-bg: #ffffff !important;
  --chip-err-fg: #0f172a !important;
  --chip-err-border: #94a3b8 !important;
  --chip-miss-bg: #ffffff !important;
  --chip-miss-fg: #15803d !important;
  --chip-miss-border: #94a3b8 !important;
  --chip-wrong-strike: #64748b !important;
  --chip-correct-fg: #15803d !important;
}
"""
    elif theme_mode == "dark":
        custom_css += """
:root, html, body, .card {
  --bg: #18181b !important;
  --fg: #f4f4f5 !important;
  --muted: #a1a1aa !important;
  --border: #27272a !important;
  --surf: #27272a !important;
  --chip-placed-bg: #22242a !important;
  --chip-placed-fg: #f1f5f9 !important;
  --chip-placed-border: #3f3f46 !important;
  --chip-ok-bg: #22242a !important;
  --chip-ok-fg: #f1f5f9 !important;
  --chip-ok-border: #3f3f46 !important;
  --chip-err-bg: #22242a !important;
  --chip-err-fg: #f1f5f9 !important;
  --chip-err-border: #3f3f46 !important;
  --chip-miss-bg: #22242a !important;
  --chip-miss-fg: #4ade80 !important;
  --chip-miss-border: #52525b !important;
  --chip-wrong-strike: #94a3b8 !important;
  --chip-correct-fg: #4ade80 !important;
}
"""

    if config.get("use_colored_feedback", False):
        custom_css += """
/* Calm colored feedback mode */
.c-ok {
  background: #f0fdf4 !important;
  background-color: #f0fdf4 !important;
  color: #166534 !important;
  border: 1.5px solid #86efac !important;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04) !important;
}
.c-err {
  background: #fef2f2 !important;
  background-color: #fef2f2 !important;
  color: #991b1b !important;
  border: 1.5px solid #fca5a5 !important;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04) !important;
}
.c-miss {
  background: #f0fdf4 !important;
  background-color: #f0fdf4 !important;
  color: #166534 !important;
  border: 1.5px dashed #86efac !important;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04) !important;
}
.chip-correct {
  color: #166534 !important;
}
html.night_mode .c-ok, html.nightMode .c-ok, body.night_mode .c-ok, .card.night_mode .c-ok {
  background: #14291f !important;
  background-color: #14291f !important;
  color: #86efac !important;
  border: 1.5px solid #166534 !important;
  box-shadow: none !important;
}
html.night_mode .c-err, html.nightMode .c-err, body.night_mode .c-err, .card.night_mode .c-err {
  background: #2b171a !important;
  background-color: #2b171a !important;
  color: #fca5a5 !important;
  border: 1.5px solid #7f1d1d !important;
  box-shadow: none !important;
}
html.night_mode .c-miss, html.nightMode .c-miss, body.night_mode .c-miss, .card.night_mode .c-miss {
  background: #14291f !important;
  background-color: #14291f !important;
  color: #86efac !important;
  border: 1.5px dashed #166534 !important;
  box-shadow: none !important;
}
html.night_mode .chip-correct, html.nightMode .chip-correct, body.night_mode .chip-correct, .card.night_mode .chip-correct {
  color: #86efac !important;
}
"""
    return custom_css


def generate_card_templates(config: dict) -> Tuple[str, str]:
    """Generates front and back HTML templates reflecting gameplay options."""
    auto_shuffle = config.get("auto_shuffle_pool", True)
    hide_res = config.get("hide_resultat", not config.get("show_score_badge", True))
    show_score = not hide_res
    show_missed = config.get("show_missed_answer_on_back", True)
    enable_tap = config.get("enable_click_to_place", True)
    use_colored = config.get("use_colored_feedback", False)
    show_symbols = config.get("show_symbols", False)

    front = FRONT_TEMPLATE
    back = BACK_TEMPLATE

    if use_colored:
        back = back.replace('<div class="ddi-wrap', '<div class="ddi-wrap colored-feedback')

    if show_symbols:
        back = back.replace('chip.textContent=userVal;', "chip.textContent='✓ ' + userVal;")
        back = back.replace('<span class="chip-wrong">', '<span class="chip-wrong">✗ ')
        back = back.replace('<span class="chip-correct">', '<span class="chip-correct">✓ ')

    if not auto_shuffle:
        front = front.replace("shuffle(LABELS).forEach(", "LABELS.forEach(")

    if not enable_tap:
        front = front.replace("var selectedChip=null;", "var selectedChip=null; var _tapDisabled=true;")

    if not show_score:
        back = back.replace('<div class="section-label">Resultat</div>', '<div class="section-label" style="display:none">Resultat</div>')
        back = back.replace('<div id="scoreBox"></div>', '<div id="scoreBox" style="display:none"></div>')

    if not show_missed:
        back = back.replace("chip.className='chip c-miss';", "chip.className='chip c-err';")

    return front, back


def generate_category_card_templates(config: dict) -> Tuple[str, str]:
    """Generates front and back HTML templates for category sorting reflecting gameplay options."""
    hide_res = config.get("hide_resultat", not config.get("show_score_badge", True))
    show_score = not hide_res
    use_colored = config.get("use_colored_feedback", False)
    show_symbols = config.get("cat_show_symbols", False) or config.get("show_symbols", False)
    show_missed = config.get("cat_show_missed", config.get("show_missed_answer_on_back", True))
    front = CAT_FRONT_TEMPLATE
    back = CAT_BACK_TEMPLATE
    if use_colored:
        back = back.replace('<div class="cat-wrap', '<div class="cat-wrap colored-feedback')
    if show_symbols:
        back = back.replace('chip.textContent = item;', "chip.textContent = '✓ ' + item;")
        back = back.replace('<span class="chip-wrong">', '<span class="chip-wrong">✗ ')
        back = back.replace('<span class="chip-correct">', '<span class="chip-correct">✓ ')
    if not show_score:
        back = back.replace('<div class="section-label">Resultat</div>', '<div class="section-label" style="display:none">Resultat</div>')
        back = back.replace('<div id="catScoreBox"></div>', '<div id="catScoreBox" style="display:none"></div>')
    if not show_missed:
        back = back.replace("missChip.className = 'chip c-miss';", "missChip.className = 'chip c-err';")
    return front, back


def apply_config_to_note_type(config: dict):
    """Updates the CSS and templates in the Anki Note Type models according to user settings."""
    if not mw or not mw.col:
        return
    models = mw.col.models
    model = models.by_name(NOTE_TYPE_NAME)
    if model:
        front_html, back_html = generate_card_templates(config)
        model['css'] = generate_dynamic_css(config)
        for tmpl in model.get('tmpls', []):
            tmpl['qfmt'] = front_html
            tmpl['afmt'] = back_html
        try:
            models.save(model, update_cards=True)
        except TypeError:
            models.save(model)

    cat_model = models.by_name(CAT_NOTE_TYPE_NAME)
    if cat_model:
        cat_front_html, cat_back_html = generate_category_card_templates(config)
        cat_model['css'] = generate_dynamic_category_css(config)
        for tmpl in cat_model.get('tmpls', []):
            tmpl['qfmt'] = cat_front_html
            tmpl['afmt'] = cat_back_html
        try:
            models.save(cat_model, update_cards=True)
        except TypeError:
            models.save(cat_model)

    try:
        if hasattr(mw, "reviewer") and mw.reviewer and hasattr(mw.reviewer, "card") and mw.reviewer.card:
            mw.reviewer.card.load()
        if hasattr(mw, "reset"):
            mw.reset()
        if hasattr(mw, "update_undo_actions"):
            mw.update_undo_actions()
    except Exception:
        pass


def ensure_ddi_note_type(force_update: bool = False):
    """Ensure the 'Drag drop Image' note type exists and its templates/CSS are up-to-date."""
    if not mw or not mw.col:
        return None
    models = mw.col.models
    model = models.by_name(NOTE_TYPE_NAME)

    # Check for and migrate legacy note type names
    if not model:
        for leg in LEGACY_NAMES:
            legacy_model = models.by_name(leg)
            if legacy_model:
                legacy_model['name'] = NOTE_TYPE_NAME
                try:
                    models.save(legacy_model)
                except Exception:
                    pass
                model = legacy_model
                break

    config = mw.addonManager.getConfig(__name__) or {}
    css_content = generate_dynamic_css(config)
    front_html, back_html = generate_card_templates(config)

    if not model:
        model = models.new(NOTE_TYPE_NAME)
        for field_name in FIELDS:
            field = models.new_field(field_name)
            models.add_field(model, field)
        template = models.new_template("Card 1")
        template['qfmt'] = front_html
        template['afmt'] = back_html
        models.add_template(model, template)
        model['css'] = css_content
        try:
            models.save(model, update_cards=True)
        except TypeError:
            models.save(model)
        tooltip(f"'{NOTE_TYPE_NAME}' note type created successfully!", period=3000)
    else:
        updated = False
        existing_field_names = [f['name'] for f in model.get('flds', [])]
        
        # Rename legacy Answer field to Extra if Extra does not exist yet
        if 'Answer' in existing_field_names and 'Extra' not in existing_field_names:
            for fld in model.get('flds', []):
                if fld['name'] == 'Answer':
                    fld['name'] = 'Extra'
                    updated = True
                    break
            existing_field_names = [f['name'] for f in model.get('flds', [])]

        # Add any missing new fields (Extra, Front Audio, Back Audio, etc.)
        for f_name in FIELDS:
            if f_name not in existing_field_names:
                new_fld = models.new_field(f_name)
                models.add_field(model, new_fld)
                updated = True

        if model.get('css', '').strip() != css_content.strip():
            model['css'] = css_content
            updated = True
        for tmpl in model.get('tmpls', []):
            if tmpl.get('qfmt', '').strip() != front_html.strip():
                tmpl['qfmt'] = front_html
                updated = True
            if tmpl.get('afmt', '').strip() != back_html.strip():
                tmpl['afmt'] = back_html
                updated = True

        if updated or force_update:
            if force_update:
                model['css'] = css_content
                for tmpl in model.get('tmpls', []):
                    tmpl['qfmt'] = front_html
                    tmpl['afmt'] = back_html
            try:
                models.save(model, update_cards=True)
            except TypeError:
                models.save(model)
            if updated:
                tooltip(f"'{NOTE_TYPE_NAME}' templates and styling updated to latest version!", period=3000)
    return model


def ensure_dragdrop_category_note_type(force_update: bool = False):
    """Ensure the 'DragDrop' Category Sorting note type exists and its templates/CSS are up-to-date."""
    if not mw or not mw.col:
        return None
    models = mw.col.models
    model = models.by_name(CAT_NOTE_TYPE_NAME)

    if not model:
        for leg in CAT_LEGACY_NAMES:
            legacy_model = models.by_name(leg)
            if legacy_model:
                legacy_model['name'] = CAT_NOTE_TYPE_NAME
                try:
                    models.save(legacy_model)
                except Exception:
                    pass
                model = legacy_model
                break

    config = mw.addonManager.getConfig(__name__) or {}
    cat_css = generate_dynamic_category_css(config)
    cat_front_html, cat_back_html = generate_category_card_templates(config)

    if not model:
        model = models.new(CAT_NOTE_TYPE_NAME)
        for field_name in CAT_FIELDS:
            field = models.new_field(field_name)
            models.add_field(model, field)
        template = models.new_template("Card 1")
        template['qfmt'] = cat_front_html
        template['afmt'] = cat_back_html
        models.add_template(model, template)
        model['css'] = cat_css
        try:
            models.save(model, update_cards=True)
        except TypeError:
            models.save(model)
    else:
        updated = False
        existing_field_names = [f['name'] for f in model.get('flds', [])]
        for f_name in CAT_FIELDS:
            if f_name not in existing_field_names:
                new_fld = models.new_field(f_name)
                models.add_field(model, new_fld)
                updated = True

        if model.get('css', '').strip() != cat_css.strip():
            model['css'] = cat_css
            updated = True
        for tmpl in model.get('tmpls', []):
            if tmpl.get('qfmt', '').strip() != cat_front_html.strip():
                tmpl['qfmt'] = cat_front_html
                updated = True
            if tmpl.get('afmt', '').strip() != cat_back_html.strip():
                tmpl['afmt'] = cat_back_html
                updated = True

        if updated or force_update:
            if force_update:
                model['css'] = cat_css
                for tmpl in model.get('tmpls', []):
                    tmpl['qfmt'] = cat_front_html
                    tmpl['afmt'] = cat_back_html
            try:
                models.save(model, update_cards=True)
            except TypeError:
                models.save(model)
    return model


def ensure_all_note_types(force_update: bool = False):
    """Ensures both Image Labeling and Category Sorting note types exist silently."""
    ensure_ddi_note_type(force_update)
    ensure_dragdrop_category_note_type(force_update)


def set_editor_note_type(editor: Editor, model_name: str):
    """Transparently switches the note type in the current Anki editor window."""
    try:
        if not mw or not mw.col or not editor or not editor.note:
            return
        models = mw.col.models
        target_model = models.by_name(model_name)
        if not target_model:
            if model_name == NOTE_TYPE_NAME:
                target_model = ensure_ddi_note_type()
            elif model_name == CAT_NOTE_TYPE_NAME:
                target_model = ensure_dragdrop_category_note_type()

        if not target_model:
            return

        note = editor.note
        if note.model().get("name") != model_name:
            if hasattr(editor, "set_model") and callable(editor.set_model):
                editor.set_model(target_model)
            elif hasattr(editor, "setNote") and callable(editor.setNote):
                new_note = mw.col.new_note(target_model)
                for f in ["Title", "Question", "Layout", "Extra", "Front Audio", "Back Audio"]:
                    if f in note and f in new_note:
                        new_note[f] = note[f]
                editor.setNote(new_note)
            else:
                note.mid = target_model['id']
                editor.loadNote()
    except Exception:
        pass


class DdiGuideDialog(QDialog):
    """
    Native Anki User Guide Dialog for Drag Drop.
    Matches the clean, compact native layout with clear sections,
    horizontal separators, native button styling, and bottom version credit.
    """
    def __init__(self, parent=None):
        super().__init__(parent or mw)
        self.setWindowTitle("Drag Drop — Guide")
        self.setFixedSize(460, 480)
        self.close_parent_on_close = False
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 14)
        layout.setSpacing(10)

        def make_divider():
            line = QFrame()
            line.setFrameShape(QFrame.Shape.HLine if hasattr(QFrame, 'Shape') else QFrame.HLine)
            line.setFrameShadow(QFrame.Shadow.Sunken if hasattr(QFrame, 'Shadow') else QFrame.Sunken)
            line.setFixedHeight(1)
            line.setStyleSheet("background-color: palette(mid); border: none;")
            return line

        # Header Title and Subtitle
        lbl_title = QLabel("Drag Drop")
        lbl_title.setStyleSheet("font-size: 16px; font-weight: bold; color: palette(text);")
        layout.addWidget(lbl_title)

        lbl_subtitle = QLabel("Create interactive flashcards by labeling images or sorting items into categories.")
        lbl_subtitle.setWordWrap(True)
        lbl_subtitle.setStyleSheet("font-size: 11.5px; color: #7f8c8d; line-height: 1.35;")
        layout.addWidget(lbl_subtitle)

        # Top Horizontal Divider Line
        layout.addWidget(make_divider())

        # Section 1: What it does
        sec1_title = QLabel("<b>What it does</b>")
        sec1_title.setStyleSheet("font-size: 12px; color: palette(text);")
        layout.addWidget(sec1_title)

        sec1_body = QLabel(
            "• Turn diagrams and lists into interactive cards<br>"
            "• Drag labels to the correct place (or click to place them)<br>"
            "• See your score and feedback when you flip the card<br>"
            "• Works in light and dark mode"
        )
        sec1_body.setWordWrap(True)
        sec1_body.setTextFormat(Qt.TextFormat.RichText if hasattr(Qt, 'TextFormat') else Qt.RichText)
        sec1_body.setStyleSheet("font-size: 11.5px; line-height: 1.45; color: palette(text); padding-left: 4px;")
        layout.addWidget(sec1_body)

        # Section 2: How to use
        sec2_title = QLabel("<b>How to use</b>")
        sec2_title.setStyleSheet("font-size: 12px; color: palette(text); margin-top: 2px;")
        layout.addWidget(sec2_title)

        sec2_body = QLabel(
            "• Click <b>Add</b> and choose <b>Drag Drop (Image)</b> or <b>Drag Drop (Category)</b><br>"
            "• For image cards: paste your picture, then click the toolbar button to place drop zones<br>"
            "• For category cards: add your categories and items<br>"
            "• During review: drag items into place, then press <b>Space</b> to check your answers"
        )
        sec2_body.setWordWrap(True)
        sec2_body.setTextFormat(Qt.TextFormat.RichText if hasattr(Qt, 'TextFormat') else Qt.RichText)
        sec2_body.setStyleSheet("font-size: 11.5px; line-height: 1.45; color: palette(text); padding-left: 4px;")
        layout.addWidget(sec2_body)

        # Section 3: Settings
        sec3_title = QLabel("<b>Settings (Tools → Drag Drop Settings)</b>")
        sec3_title.setStyleSheet("font-size: 12px; color: palette(text); margin-top: 2px;")
        layout.addWidget(sec3_title)

        sec3_body = QLabel(
            "• Open <b>Tools → Drag Drop Settings</b> to change theme, layout, animations, and feedback style"
        )
        sec3_body.setWordWrap(True)
        sec3_body.setTextFormat(Qt.TextFormat.RichText if hasattr(Qt, 'TextFormat') else Qt.RichText)
        sec3_body.setStyleSheet("font-size: 11.5px; line-height: 1.45; color: palette(text); padding-left: 4px;")
        layout.addWidget(sec3_body)

        layout.addStretch()

        # Divider Line Above Buttons
        layout.addWidget(make_divider())

        # Action Buttons Row
        btn_bar = QHBoxLayout()
        btn_bar.setContentsMargins(0, 2, 0, 2)
        btn_bar.setSpacing(10)

        btn_settings = QPushButton("Open Settings")
        btn_settings.setFixedHeight(28)
        btn_settings.setCursor(Qt.CursorShape.PointingHandCursor if hasattr(Qt, 'CursorShape') else Qt.PointingHandCursor)
        btn_settings.clicked.connect(self.open_settings)
        btn_bar.addWidget(btn_settings)

        btn_bar.addStretch()

        btn_got_it = QPushButton("Got it ✔")
        btn_got_it.setDefault(True)
        btn_got_it.setFixedHeight(28)
        btn_got_it.setMinimumWidth(85)
        btn_got_it.setCursor(Qt.CursorShape.PointingHandCursor if hasattr(Qt, 'CursorShape') else Qt.PointingHandCursor)
        btn_got_it.setStyleSheet("""
            QPushButton {
                background-color: #1d80e2;
                color: #ffffff;
                font-weight: 500;
                border: 1px solid #166bc2;
                border-radius: 4px;
                padding: 4px 14px;
            }
            QPushButton:hover {
                background-color: #166bc2;
            }
            QPushButton:pressed {
                background-color: #0f549c;
            }
        """)
        btn_got_it.clicked.connect(self.on_got_it)
        btn_bar.addWidget(btn_got_it)

        layout.addLayout(btn_bar)

        # Divider Line Below Buttons
        layout.addWidget(make_divider())

        # Footer Line with Version Only (Centered)
        lbl_version = QLabel("v1.3.0")
        lbl_version.setAlignment(Qt.AlignmentFlag.AlignCenter if hasattr(Qt, 'AlignmentFlag') else Qt.AlignCenter)
        lbl_version.setStyleSheet("font-size: 11px; color: #7f8c8d; padding-top: 1px; font-family: monospace;")
        layout.addWidget(lbl_version)

    def on_got_it(self):
        self.close_parent_on_close = True
        if self.parent() and isinstance(self.parent(), QDialog):
            self.parent().accept()
        self.accept()

    def open_settings(self):
        self.close_parent_on_close = False
        parent_dlg = self.parent()
        if parent_dlg and isinstance(parent_dlg, QDialog):
            self.accept()
        else:
            self.accept()
            open_ddi_settings_dialog()


class DdiSettingsDialog(QDialog):
    """
    Native Anki / Qt Settings Dialog for Drag Drop.
    Uses standard Qt QTabWidget, QGroupBox, QCheckBox, QComboBox and QDialogButtonBox,
    automatically styled by Anki's native palette in both light and dark mode.
    """
    def __init__(self, parent=None):
        super().__init__(parent or mw)
        self.setWindowTitle("Drag Drop")
        self.resize(500, 340)
        self.config = mw.addonManager.getConfig(__name__) or {}
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        # Tab Widget
        self.tabs = QTabWidget()

        # -------------------------------------------------------------
        # TAB 1: GENERAL
        # -------------------------------------------------------------
        tab_gen = QWidget()
        l_gen = QVBoxLayout(tab_gen)
        l_gen.setContentsMargins(10, 10, 10, 10)
        l_gen.setSpacing(10)

        grp_display = QGroupBox("Display Settings")
        form_gen = QFormLayout(grp_display)
        form_gen.setSpacing(8)

        self.cmb_theme_mode = QComboBox()
        self.cmb_theme_mode.addItems([
            "Auto (System / Anki)",
            "Light Mode",
            "Dark Mode"
        ])
        t_mode = self.config.get("theme_mode", "auto")
        if t_mode == "light": self.cmb_theme_mode.setCurrentIndex(1)
        elif t_mode == "dark": self.cmb_theme_mode.setCurrentIndex(2)
        else: self.cmb_theme_mode.setCurrentIndex(0)
        form_gen.addRow("Theme:", self.cmb_theme_mode)

        self.cmb_default_layout = QComboBox()
        self.cmb_default_layout.addItems([
            "Horizontal (Side-by-Side)",
            "Vertical (Stacked)"
        ])
        d_lay = self.config.get("default_layout", "horizontal")
        self.cmb_default_layout.setCurrentIndex(1 if d_lay == "vertical" else 0)
        form_gen.addRow("Default Layout:", self.cmb_default_layout)

        self.cmb_font = QFontComboBox()
        f_val = self.config.get("font_family", "")
        if f_val and f_val not in ["System Default", ""]:
            self.cmb_font.setCurrentFont(QFont(f_val))
        form_gen.addRow("Font:", self.cmb_font)

        self.cmb_size = QComboBox()
        self.cmb_size.addItems(["12", "14", "16", "18", "20", "22", "24"])
        s_val = str(self.config.get("font_size", 16))
        idx_size = self.cmb_size.findText(s_val)
        if idx_size >= 0:
            self.cmb_size.setCurrentIndex(idx_size)
        else:
            self.cmb_size.setCurrentIndex(2)  # Default 16
        form_gen.addRow("Font Size:", self.cmb_size)

        l_gen.addWidget(grp_display)
        l_gen.addStretch()
        self.tabs.addTab(tab_gen, "General")

        # -------------------------------------------------------------
        # TAB 2: IMAGE LABELING
        # -------------------------------------------------------------
        tab_img = QWidget()
        l_img = QVBoxLayout(tab_img)
        l_img.setContentsMargins(10, 10, 10, 10)
        l_img.setSpacing(8)

        grp_img_opts = QGroupBox("Review Options")
        chk_grid = QGridLayout(grp_img_opts)
        chk_grid.setHorizontalSpacing(14)
        chk_grid.setVerticalSpacing(6)

        self.chk_midcenter = QCheckBox("Center card on screen")
        self.chk_midcenter.setChecked(self.config.get("center_image_midcenter", False))
        chk_grid.addWidget(self.chk_midcenter, 0, 0)

        self.chk_shuffle = QCheckBox("Auto-shuffle labels")
        self.chk_shuffle.setChecked(self.config.get("auto_shuffle_pool", True))
        chk_grid.addWidget(self.chk_shuffle, 0, 1)

        self.chk_score = QCheckBox("Show Resultat / score badge")
        self.chk_score.setChecked(not self.config.get("hide_resultat", not self.config.get("show_score_badge", True)))
        self.chk_score.stateChanged.connect(self._sync_score_from_image)
        chk_grid.addWidget(self.chk_score, 1, 0)

        self.chk_tap = QCheckBox("Enable click-to-place")
        self.chk_tap.setChecked(self.config.get("enable_click_to_place", True))
        chk_grid.addWidget(self.chk_tap, 1, 1)

        self.chk_symbols = QCheckBox("Show ✓ / ✗ symbols")
        self.chk_symbols.setChecked(self.config.get("show_symbols", False))
        chk_grid.addWidget(self.chk_symbols, 2, 0)

        self.chk_colored = QCheckBox("Use colored feedback")
        self.chk_colored.setChecked(self.config.get("use_colored_feedback", False))
        chk_grid.addWidget(self.chk_colored, 2, 1)

        l_img.addWidget(grp_img_opts)

        # Dimensions sub-form
        form_img_dim = QFormLayout()
        form_img_dim.setSpacing(6)

        self.cmb_max_width = QComboBox()
        self.cmb_max_width.addItems([
            "Compact (800px)",
            "Standard (920px)",
            "Wide (1050px)",
            "Full Width (100%)"
        ])
        curr_w = self.config.get("max_card_width_px", 920)
        idx_w = 1
        if curr_w <= 800: idx_w = 0
        elif curr_w == 920: idx_w = 1
        elif curr_w == 1050: idx_w = 2
        elif curr_w >= 1200: idx_w = 3
        self.cmb_max_width.setCurrentIndex(idx_w)
        form_img_dim.addRow("Max width:", self.cmb_max_width)

        self.cmb_max_height = QComboBox()
        self.cmb_max_height.addItems([
            "Small (55% screen)",
            "Standard (68% screen)",
            "Large (80% screen)",
            "Natural (unconstrained)"
        ])
        curr_h = self.config.get("max_image_height_vh", 68)
        idx_h = 1
        if curr_h <= 55: idx_h = 0
        elif curr_h == 68: idx_h = 1
        elif curr_h == 78 or curr_h == 80 or curr_h == 88: idx_h = 2
        elif curr_h >= 100: idx_h = 3
        self.cmb_max_height.setCurrentIndex(idx_h)
        form_img_dim.addRow("Max height:", self.cmb_max_height)

        l_img.addLayout(form_img_dim)
        l_img.addStretch()
        self.tabs.addTab(tab_img, "Image Labeling")

        # -------------------------------------------------------------
        # TAB 3: CATEGORY SORTING
        # -------------------------------------------------------------
        tab_cat = QWidget()
        l_cat = QVBoxLayout(tab_cat)
        l_cat.setContentsMargins(10, 10, 10, 10)
        l_cat.setSpacing(8)

        grp_cat = QGroupBox("Category Options")
        cat_grid = QGridLayout(grp_cat)
        cat_grid.setHorizontalSpacing(14)
        cat_grid.setVerticalSpacing(6)

        self.chk_cat_center = QCheckBox("Center card on screen")
        self.chk_cat_center.setChecked(self.config.get("cat_center_card", False))
        cat_grid.addWidget(self.chk_cat_center, 0, 0)

        self.chk_cat_anim = QCheckBox("Smooth animations")
        self.chk_cat_anim.setChecked(self.config.get("cat_smooth_animations", True))
        cat_grid.addWidget(self.chk_cat_anim, 0, 1)

        self.chk_cat_symbols = QCheckBox("Show ✓ / ✗ symbols")
        self.chk_cat_symbols.setChecked(self.config.get("cat_show_symbols", False))
        cat_grid.addWidget(self.chk_cat_symbols, 1, 0)

        self.chk_cat_equal_col = QCheckBox("Equal height columns")
        self.chk_cat_equal_col.setChecked(self.config.get("cat_equal_height_columns", True))
        cat_grid.addWidget(self.chk_cat_equal_col, 1, 1)

        self.chk_cat_highlight = QCheckBox("Highlight drop zones")
        self.chk_cat_highlight.setChecked(self.config.get("cat_highlight_drop_zones", True))
        cat_grid.addWidget(self.chk_cat_highlight, 2, 0)

        self.chk_cat_reorder = QCheckBox("Allow reordering items")
        self.chk_cat_reorder.setChecked(self.config.get("cat_allow_reordering", True))
        cat_grid.addWidget(self.chk_cat_reorder, 2, 1)

        self.chk_cat_score = QCheckBox("Auto-evaluate score")
        self.chk_cat_score.setChecked(self.config.get("cat_auto_evaluate_score", True))
        cat_grid.addWidget(self.chk_cat_score, 3, 0)

        self.chk_cat_hide_resultat = QCheckBox("Hide result / score box (Resultat)")
        self.chk_cat_hide_resultat.setChecked(self.config.get("hide_resultat", not self.config.get("show_score_badge", True)))
        self.chk_cat_hide_resultat.stateChanged.connect(self._sync_hide_resultat_from_cat)
        cat_grid.addWidget(self.chk_cat_hide_resultat, 3, 1)

        l_cat.addWidget(grp_cat)
        l_cat.addStretch()
        self.tabs.addTab(tab_cat, "Category Sorting")

        # -------------------------------------------------------------
        # TAB 4: SUPPORT
        # -------------------------------------------------------------
        tab_sup = QWidget()
        l_sup = QVBoxLayout(tab_sup)
        l_sup.setContentsMargins(10, 10, 10, 10)
        l_sup.setSpacing(8)

        grp_sup = QGroupBox("Add-on Information & Maintenance")
        l_grp_sup = QVBoxLayout(grp_sup)
        l_grp_sup.setSpacing(8)

        btn_guide = QPushButton("Open User Guide...")
        btn_guide.clicked.connect(self.open_guide)
        l_grp_sup.addWidget(btn_guide)

        btn_report = QPushButton("Report an Issue (GitHub)...")
        btn_report.clicked.connect(self.report_issue)
        l_grp_sup.addWidget(btn_report)

        btn_defaults = QPushButton("Restore Defaults")
        btn_defaults.clicked.connect(self.restore_defaults)
        l_grp_sup.addWidget(btn_defaults)

        l_sup.addWidget(grp_sup)
        l_sup.addStretch()
        self.tabs.addTab(tab_sup, "Support")

        layout.addWidget(self.tabs, stretch=1)

        # -------------------------------------------------------------
        # BOTTOM ACTION BAR (Native Anki standard Save & Cancel)
        # -------------------------------------------------------------
        btn_box = QHBoxLayout()
        btn_box.setSpacing(6)
        btn_box.addStretch()

        btn_cancel = QPushButton("Cancel")
        btn_cancel.clicked.connect(self.reject)
        btn_box.addWidget(btn_cancel)

        self.btn_save = QPushButton("Save")
        self.btn_save.setDefault(True)
        self.btn_save.clicked.connect(self.save_settings)
        btn_box.addWidget(self.btn_save)

        layout.addLayout(btn_box)

    def _sync_score_from_image(self, state):
        self.chk_cat_hide_resultat.blockSignals(True)
        self.chk_cat_hide_resultat.setChecked(not self.chk_score.isChecked())
        self.chk_cat_hide_resultat.blockSignals(False)

    def _sync_hide_resultat_from_cat(self, state):
        self.chk_score.blockSignals(True)
        self.chk_score.setChecked(not self.chk_cat_hide_resultat.isChecked())
        self.chk_score.blockSignals(False)

    def open_guide(self):
        dlg = DdiGuideDialog(self)
        dlg.exec()
        if getattr(dlg, "close_parent_on_close", False):
            self.accept()

    def report_issue(self):
        url = QUrl("https://github.com/Doummar/Drag_drop/issues")
        QDesktopServices.openUrl(url)

    def restore_defaults(self):
        self.cmb_theme_mode.setCurrentIndex(0)
        self.cmb_default_layout.setCurrentIndex(0)
        self.cmb_font.setCurrentFont(QFont())
        idx_16 = self.cmb_size.findText("16")
        if idx_16 >= 0:
            self.cmb_size.setCurrentIndex(idx_16)
        self.chk_midcenter.setChecked(False)
        self.cmb_max_width.setCurrentIndex(1)
        self.cmb_max_height.setCurrentIndex(1)
        self.chk_shuffle.setChecked(True)
        self.chk_score.setChecked(True)
        self.chk_cat_hide_resultat.setChecked(False)
        self.chk_tap.setChecked(True)
        self.chk_colored.setChecked(False)
        self.chk_cat_center.setChecked(False)
        self.chk_cat_symbols.setChecked(False)
        self.chk_cat_anim.setChecked(True)
        self.chk_cat_highlight.setChecked(True)
        self.chk_cat_equal_col.setChecked(True)
        self.chk_cat_score.setChecked(True)
        self.chk_cat_reorder.setChecked(True)
        tooltip("Default settings restored. Click 'Save' to apply.", period=2500)

    def save_settings(self):
        w_map = [800, 920, 1050, 1200, 9999]
        h_map = [55, 68, 78, 88, 100]
        t_modes = ["auto", "light", "dark"]
        d_layouts = ["horizontal", "vertical"]

        self.config["theme_mode"] = t_modes[self.cmb_theme_mode.currentIndex()]
        self.config["default_layout"] = d_layouts[self.cmb_default_layout.currentIndex()]
        
        font_fam = self.cmb_font.currentFont().family()
        self.config["font_family"] = font_fam
        try:
            self.config["font_size"] = int(self.cmb_size.currentText())
        except (ValueError, TypeError):
            self.config["font_size"] = 16

        self.config["center_image_midcenter"] = self.chk_midcenter.isChecked()
        self.config["max_card_width_px"] = w_map[self.cmb_max_width.currentIndex()]
        self.config["max_image_height_vh"] = h_map[self.cmb_max_height.currentIndex()]
        self.config["auto_shuffle_pool"] = self.chk_shuffle.isChecked()
        
        is_hidden_resultat = self.chk_cat_hide_resultat.isChecked()
        self.config["hide_resultat"] = is_hidden_resultat
        self.config["show_score_badge"] = not is_hidden_resultat
        
        self.config["enable_click_to_place"] = self.chk_tap.isChecked()
        self.config["show_symbols"] = self.chk_symbols.isChecked()
        self.config["use_colored_feedback"] = self.chk_colored.isChecked()

        self.config["cat_center_card"] = self.chk_cat_center.isChecked()
        self.config["cat_show_symbols"] = self.chk_cat_symbols.isChecked()
        self.config["cat_smooth_animations"] = self.chk_cat_anim.isChecked()
        self.config["cat_highlight_drop_zones"] = self.chk_cat_highlight.isChecked()
        self.config["cat_equal_height_columns"] = self.chk_cat_equal_col.isChecked()
        self.config["cat_auto_evaluate_score"] = self.chk_cat_score.isChecked()
        self.config["cat_allow_reordering"] = self.chk_cat_reorder.isChecked()

        mw.addonManager.writeConfig(__name__, self.config)
        apply_config_to_note_type(self.config)
        tooltip("Drag Drop: Settings saved!", period=3000)
        self.accept()


def open_ddi_settings_dialog():
    """Opens the Drag Drop settings window."""
    dlg = DdiSettingsDialog(mw)
    dlg.exec()


class DdiImageCanvas(QWidget):
    """
    Interactive image canvas that displays the note's picture,
    draws dashed drop-zone bounding boxes, handles click-to-place and dragging,
    and supports image pasting (Ctrl+V / Cmd+V) and file drag-and-drop.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pixmap: Optional[QPixmap] = None
        self.zones: List[Dict[str, any]] = []
        self.selected_index: int = -1
        self.dragged_index: int = -1
        self.drag_offset_x: float = 0.0
        self.drag_offset_y: float = 0.0
        self.hover_coords: Tuple[float, float] = (0.0, 0.0)
        self.on_zones_changed = None
        self.on_coords_hover = None
        self.is_drag_over: bool = False
        
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus if hasattr(Qt, 'FocusPolicy') else Qt.StrongFocus)
        self.setMinimumSize(400, 300)
        self.setAcceptDrops(True)

    def set_image(self, pixmap: QPixmap):
        self.pixmap = pixmap
        self.update()

    def set_zones(self, zones: List[Dict[str, any]]):
        self.zones = zones
        self.update()

    def select_zone(self, index: int):
        self.selected_index = index
        self.update()

    def get_image_render_rect(self) -> QRect:
        if not self.pixmap or self.pixmap.isNull():
            return self.rect()
        scaled = self.pixmap.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatio if hasattr(Qt, 'AspectRatioMode') else Qt.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation if hasattr(Qt, 'TransformationMode') else Qt.SmoothTransformation
        )
        x = (self.width() - scaled.width()) // 2
        y = (self.height() - scaled.height()) // 2
        return QRect(x, y, scaled.width(), scaled.height())

    def pos_to_percent(self, pos: QPoint) -> Optional[Tuple[float, float]]:
        img_rect = self.get_image_render_rect()
        if img_rect.width() <= 0 or img_rect.height() <= 0:
            return None
        if not img_rect.contains(pos):
            return None
        pct_x = max(0.0, min(100.0, ((pos.x() - img_rect.x()) / img_rect.width()) * 100.0))
        pct_y = max(0.0, min(100.0, ((pos.y() - img_rect.y()) / img_rect.height()) * 100.0))
        return (round(pct_x, 1), round(pct_y, 1))

    def percent_to_pos(self, pct_x: float, pct_y: float) -> QPoint:
        img_rect = self.get_image_render_rect()
        px = img_rect.x() + int((pct_x / 100.0) * img_rect.width())
        py = img_rect.y() + int((pct_y / 100.0) * img_rect.height())
        return QPoint(px, py)

    def dragEnterEvent(self, event):
        md = event.mimeData()
        if md.hasUrls() or md.hasImage():
            self.is_drag_over = True
            event.acceptProposedAction()
            self.update()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        md = event.mimeData()
        if md.hasUrls() or md.hasImage():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.is_drag_over = False
        self.update()
        event.accept()

    def dropEvent(self, event):
        self.is_drag_over = False
        self.update()
        md = event.mimeData()
        p = self.parent()
        if md.hasUrls():
            urls = md.urls()
            if urls:
                fpath = urls[0].toLocalFile()
                if fpath and os.path.exists(fpath):
                    if p and hasattr(p, "import_image_file"):
                        p.import_image_file(fpath)
            event.acceptProposedAction()
        elif md.hasImage():
            img = md.imageData()
            if img and p and hasattr(p, "import_image_object"):
                p.import_image_object(img)
            event.acceptProposedAction()

    def keyPressEvent(self, event):
        # Support Ctrl+V / Cmd+V paste on the canvas
        is_paste = False
        if hasattr(QKeySequence, 'StandardKey') and event.matches(QKeySequence.StandardKey.Paste):
            is_paste = True
        elif hasattr(QKeySequence, 'Paste') and event.matches(QKeySequence.Paste):
            is_paste = True
        elif event.key() == (Qt.Key.Key_V if hasattr(Qt, 'Key') else Qt.Key_V):
            mods = event.modifiers()
            ctrl_or_cmd = (Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.MetaModifier) if hasattr(Qt, 'KeyboardModifier') else (Qt.ControlModifier | Qt.MetaModifier)
            if mods & ctrl_or_cmd:
                is_paste = True
        
        if is_paste:
            p = self.parent()
            if p and hasattr(p, "paste_image_from_clipboard"):
                p.paste_image_from_clipboard()
                event.accept()
                return
        super().keyPressEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing if hasattr(QPainter, 'RenderHint') else QPainter.Antialiasing)

        dark = is_anki_dark_mode()
        bg_canvas = QColor("#1e1e24") if dark else QColor("#f1f5f9")
        painter.fillRect(self.rect(), bg_canvas)

        img_rect = self.get_image_render_rect()
        if self.pixmap and not self.pixmap.isNull():
            painter.drawPixmap(img_rect, self.pixmap)
        else:
            # Draw Clean Native Anki Empty State Box
            card_rect = self.rect().adjusted(24, 24, -24, -24)
            pen = QPen(QColor("#3b82f6" if self.is_drag_over else ("#475569" if dark else "#cbd5e1")))
            pen.setStyle(Qt.PenStyle.DashLine if hasattr(Qt, 'PenStyle') else Qt.DashLine)
            pen.setWidth(2)
            painter.setPen(pen)
            painter.setBrush(QBrush(QColor("#1e293b" if dark else "#f8fafc")))
            painter.drawRoundedRect(card_rect, 12, 12)

            painter.setPen(QColor("#f8fafc") if dark else QColor("#0f172a"))
            f_title = QFont("-apple-system", 11)
            f_title.setBold(True)
            painter.setFont(f_title)
            r_title = QRect(card_rect.left(), card_rect.center().y() - 32, card_rect.width(), 26)
            painter.drawText(r_title, Qt.AlignmentFlag.AlignCenter if hasattr(Qt, 'AlignmentFlag') else Qt.AlignCenter, "No diagram image loaded in Note")

            painter.setPen(QColor("#94a3b8") if dark else QColor("#64748b"))
            f_sub = QFont("-apple-system", 9)
            painter.setFont(f_sub)
            r_sub = QRect(card_rect.left(), card_rect.center().y() - 4, card_rect.width(), 24)
            painter.drawText(r_sub, Qt.AlignmentFlag.AlignCenter if hasattr(Qt, 'AlignmentFlag') else Qt.AlignCenter, "Paste (Ctrl+V / ⌘V)  ·  Drag & drop image here  ·  or click to browse")

            # Draw visual button inside empty state
            btn_rect = QRect(card_rect.center().x() - 90, card_rect.center().y() + 28, 180, 30)
            painter.setBrush(QBrush(QColor("#2563eb")))
            painter.setPen(Qt.PenStyle.NoPen if hasattr(Qt, 'PenStyle') else Qt.NoPen)
            painter.drawRoundedRect(btn_rect, 6, 6)
            painter.setPen(QColor("#ffffff"))
            f_btn = QFont("-apple-system", 9)
            f_btn.setBold(True)
            painter.setFont(f_btn)
            painter.drawText(btn_rect, Qt.AlignmentFlag.AlignCenter if hasattr(Qt, 'AlignmentFlag') else Qt.AlignCenter, "Select Diagram Image")
            return

        # Draw drag-over overlay if dragging over loaded image
        if self.is_drag_over:
            painter.setBrush(QBrush(QColor(37, 99, 235, 120)))
            painter.setPen(QPen(QColor("#60a5fa"), 3, Qt.PenStyle.DashLine if hasattr(Qt, 'PenStyle') else Qt.DashLine))
            painter.drawRoundedRect(img_rect, 8, 8)
            painter.setPen(QColor("#ffffff"))
            f_overlay = QFont("-apple-system", 12)
            f_overlay.setBold(True)
            painter.setFont(f_overlay)
            painter.drawText(img_rect, Qt.AlignmentFlag.AlignCenter if hasattr(Qt, 'AlignmentFlag') else Qt.AlignCenter, "Drop image to replace diagram")

        # Draw Drop Zones
        font = QFont("-apple-system", 9)
        font.setBold(True)
        painter.setFont(font)
        fm = QFontMetrics(font)

        for i, zone in enumerate(self.zones):
            pt = self.percent_to_pos(zone['x'], zone['y'])
            label_text = zone['label'] or f"Zone {i+1}"
            text_w = fm.horizontalAdvance(label_text) if hasattr(fm, 'horizontalAdvance') else fm.width(label_text)
            box_w = max(90, text_w + 24)
            box_h = 32
            box_rect = QRect(pt.x() - box_w // 2, pt.y() - box_h // 2, box_w, box_h)

            is_sel = (i == self.selected_index)

            # Semi-transparent background
            bg_color = QColor(37, 99, 235, 200) if is_sel else (QColor(15, 23, 42, 190) if not dark else QColor(0, 0, 0, 180))
            painter.setBrush(QBrush(bg_color))

            # Dashed or solid border
            pen = QPen(QColor("#60a5fa") if is_sel else QColor("#ffffff"))
            pen.setWidth(2 if is_sel else 1)
            pen.setStyle(Qt.PenStyle.SolidLine if is_sel else (Qt.PenStyle.DashLine if hasattr(Qt, 'PenStyle') else Qt.DashLine))
            painter.setPen(pen)
            painter.drawRoundedRect(box_rect, 6, 6)

            # Text
            painter.setPen(QColor("#ffffff"))
            painter.drawText(box_rect, Qt.AlignmentFlag.AlignCenter if hasattr(Qt, 'AlignmentFlag') else Qt.AlignCenter, label_text)

    def mousePressEvent(self, event):
        if not self.pixmap or self.pixmap.isNull():
            p = self.parent()
            if p and hasattr(p, "browse_image_file"):
                p.browse_image_file()
            return

        pos = event.pos()
        font = QFont("-apple-system", 9)
        fm = QFontMetrics(font)

        # Check if clicked an existing zone
        clicked_idx = -1
        for i in reversed(range(len(self.zones))):
            zone = self.zones[i]
            pt = self.percent_to_pos(zone['x'], zone['y'])
            label_text = zone['label'] or f"Zone {i+1}"
            text_w = fm.horizontalAdvance(label_text) if hasattr(fm, 'horizontalAdvance') else fm.width(label_text)
            box_w = max(90, text_w + 24)
            box_h = 32
            box_rect = QRect(pt.x() - box_w // 2, pt.y() - box_h // 2, box_w, box_h)
            if box_rect.contains(pos):
                clicked_idx = i
                self.drag_offset_x = zone['x']
                self.drag_offset_y = zone['y']
                break

        if clicked_idx >= 0:
            self.selected_index = clicked_idx
            self.dragged_index = clicked_idx
            self.setCursor(Qt.CursorShape.ClosedHandCursor if hasattr(Qt, 'CursorShape') else Qt.ClosedHandCursor)
            if self.on_zones_changed:
                self.on_zones_changed(self.zones, self.selected_index)
            self.update()
        else:
            # Click on blank image area -> add new zone at position
            coords = self.pos_to_percent(pos)
            if coords:
                new_zone = {
                    'label': f"Label {len(self.zones) + 1}",
                    'x': coords[0],
                    'y': coords[1]
                }
                self.zones.append(new_zone)
                self.selected_index = len(self.zones) - 1
                if self.on_zones_changed:
                    self.on_zones_changed(self.zones, self.selected_index)
                self.update()

    def mouseMoveEvent(self, event):
        pos = event.pos()
        coords = self.pos_to_percent(pos)
        if coords and self.on_coords_hover:
            self.on_coords_hover(coords[0], coords[1])

        if self.dragged_index >= 0 and coords:
            self.zones[self.dragged_index]['x'] = coords[0]
            self.zones[self.dragged_index]['y'] = coords[1]
            if self.on_zones_changed:
                self.on_zones_changed(self.zones, self.selected_index)
            self.update()

    def mouseReleaseEvent(self, event):
        self.dragged_index = -1
        self.setCursor(Qt.CursorShape.ArrowCursor if hasattr(Qt, 'CursorShape') else Qt.ArrowCursor)


class DdiVisualEditorDialog(QDialog):
    """
    Visual Drop Zone Placement Studio launched from Anki's Note Editor.
    Supports placing drop zones, dragging/dropping images, pasting images (Ctrl+V / Cmd+V),
    and saving diagram updates directly to the note.
    """
    def __init__(self, editor: Editor, parent=None):
        super().__init__(parent or editor.parentWindow)
        self.editor = editor
        self.setWindowTitle("Drag drop Image — Visual Placement Studio")
        self.resize(1020, 700)
        self.zones: List[Dict[str, any]] = []
        self.pixmap: Optional[QPixmap] = None
        self.loaded_image_filename: Optional[str] = None
        self.setup_ui()
        self.load_note_data()

    def setup_ui(self):
        dark = is_anki_dark_mode()
        lbl_subtitle_color = "#94a3b8" if dark else "#64748b"
        lbl_coords_color = "#60a5fa" if dark else "#2563eb"
        del_btn_bg = "#451a1a" if dark else "#fee2e2"
        del_btn_border = "#7f1d1d" if dark else "#fca5a5"
        del_btn_color = "#fca5a5" if dark else "#b91c1c"
        del_btn_hover = "#7f1d1d" if dark else "#fecaca"

        self.setStyleSheet(f"""
            QDialog {{
                background-color: palette(window);
                color: palette(text);
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            }}
            QLabel {{
                color: palette(text);
            }}
            QGroupBox {{
                background-color: palette(window);
                border: 1px solid palette(mid);
                border-radius: 8px;
                margin-top: 10px;
                padding: 12px;
                color: palette(text);
                font-weight: 600;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 6px;
                color: palette(text);
            }}
            QListWidget {{
                background-color: palette(base);
                border: 1px solid palette(mid);
                border-radius: 6px;
                color: palette(text);
                padding: 4px;
            }}
            QListWidget::item:selected {{
                background-color: #2563eb;
                color: #ffffff;
                border-radius: 4px;
            }}
            QLineEdit, QTextEdit {{
                background-color: palette(base);
                border: 1px solid palette(mid);
                border-radius: 6px;
                color: palette(text);
                padding: 6px;
            }}
            QLineEdit:focus, QTextEdit:focus {{
                border: 1.5px solid #2563eb;
            }}
            QRadioButton {{
                color: palette(text);
                font-size: 12.5px;
                font-weight: 500;
                spacing: 6px;
            }}
            QRadioButton::indicator {{
                width: 15px;
                height: 15px;
                border-radius: 8px;
                border: 1.5px solid palette(mid);
                background-color: palette(base);
            }}
            QRadioButton::indicator:hover {{
                border-color: #3b82f6;
            }}
            QRadioButton::indicator:checked {{
                border: 4.5px solid #2563eb;
                background-color: palette(base);
            }}
            QPushButton {{
                background-color: palette(button);
                border: 1px solid palette(mid);
                border-radius: 6px;
                padding: 6px 12px;
                color: palette(button-text);
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: palette(midlight);
                border-color: palette(dark);
            }}
            QPushButton#saveBtn {{
                background-color: #2563eb;
                border: 1px solid #1d4ed8;
                color: #ffffff;
                font-weight: 600;
            }}
            QPushButton#saveBtn:hover {{
                background-color: #1d4ed8;
            }}
            QPushButton#delBtn {{
                background-color: {del_btn_bg};
                border: 1px solid {del_btn_border};
                color: {del_btn_color};
            }}
            QPushButton#delBtn:hover {{
                background-color: {del_btn_hover};
            }}
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(14)

        # Left Canvas Area
        left_box = QVBoxLayout()
        
        # Header toolbar
        tb_layout = QHBoxLayout()
        self.lbl_title = QLabel("<b>Click diagram</b> to add drop zone · <b>Drag</b> box to position")
        self.lbl_title.setStyleSheet(f"color: {lbl_subtitle_color}; font-size: 12px;")
        tb_layout.addWidget(self.lbl_title)
        
        tb_layout.addStretch()

        self.btn_load_image = QPushButton("Load / Replace Image")
        self.btn_load_image.clicked.connect(self.browse_image_file)
        self.btn_load_image.setToolTip("Select or replace the diagram image (or press Ctrl+V / drop file)")
        tb_layout.addWidget(self.btn_load_image)

        self.lbl_coords = QLabel("X: 0.0%  Y: 0.0%")
        self.lbl_coords.setStyleSheet(f"color: {lbl_coords_color}; font-family: monospace; font-size: 12px; font-weight: bold;")
        tb_layout.addWidget(self.lbl_coords)

        left_box.addLayout(tb_layout)

        self.canvas = DdiImageCanvas(self)
        self.canvas.on_zones_changed = self.on_canvas_zones_changed
        self.canvas.on_coords_hover = lambda x, y: self.lbl_coords.setText(f"X: {x:.1f}%  Y: {y:.1f}%")
        left_box.addWidget(self.canvas, stretch=1)

        layout.addLayout(left_box, stretch=3)

        # Right Control Sidebar
        sidebar = QVBoxLayout()
        sidebar.setSpacing(10)

        grp_zones = QGroupBox("Drop Zones List")
        gz_layout = QVBoxLayout(grp_zones)
        gz_layout.setSpacing(8)

        self.list_zones = QListWidget()
        self.list_zones.currentRowChanged.connect(self.on_list_selection_changed)
        gz_layout.addWidget(self.list_zones)

        btn_row = QHBoxLayout()
        self.btn_add_zone = QPushButton("Add Zone")
        self.btn_add_zone.clicked.connect(self.add_manual_zone)
        btn_row.addWidget(self.btn_add_zone)

        self.btn_del_zone = QPushButton("Delete")
        self.btn_del_zone.setObjectName("delBtn")
        self.btn_del_zone.clicked.connect(self.delete_selected_zone)
        btn_row.addWidget(self.btn_del_zone)

        gz_layout.addLayout(btn_row)
        sidebar.addWidget(grp_zones, stretch=2)

        # Edit selected zone properties
        grp_edit = QGroupBox("Selected Zone Label")
        ge_layout = QVBoxLayout(grp_edit)
        ge_layout.setSpacing(6)

        self.txt_label = QLineEdit()
        self.txt_label.setPlaceholderText("Enter label text (e.g. Femur)...")
        self.txt_label.textChanged.connect(self.on_label_text_edited)
        ge_layout.addWidget(self.txt_label)

        pos_row = QHBoxLayout()
        self.lbl_pos_x = QLabel("X: --")
        self.lbl_pos_y = QLabel("Y: --")
        self.lbl_pos_x.setStyleSheet(f"color: {lbl_subtitle_color}; font-family: monospace;")
        self.lbl_pos_y.setStyleSheet(f"color: {lbl_subtitle_color}; font-family: monospace;")
        pos_row.addWidget(self.lbl_pos_x)
        pos_row.addWidget(self.lbl_pos_y)
        ge_layout.addLayout(pos_row)

        sidebar.addWidget(grp_edit)

        # Layout Selector
        grp_layout = QGroupBox("Card Layout")
        gl_layout = QHBoxLayout(grp_layout)
        gl_layout.setContentsMargins(8, 6, 8, 6)
        gl_layout.setSpacing(14)

        self.radio_layout_h = QRadioButton("Horizontal (Bottom Pool)")
        self.radio_layout_v = QRadioButton("Vertical (Side Pool)")
        self.radio_layout_h.setChecked(True)

        self.layout_btn_group = QButtonGroup(self)
        self.layout_btn_group.addButton(self.radio_layout_h, 0)
        self.layout_btn_group.addButton(self.radio_layout_v, 1)

        gl_layout.addWidget(self.radio_layout_h)
        gl_layout.addWidget(self.radio_layout_v)
        gl_layout.addStretch()
        sidebar.addWidget(grp_layout)

        # Distractor Labels
        grp_dist = QGroupBox("Distractor Labels (No Zone)")
        gd_layout = QVBoxLayout(grp_dist)
        self.txt_distractors = QLineEdit()
        self.txt_distractors.setPlaceholderText("Extra decoy labels separated by |")
        gd_layout.addWidget(self.txt_distractors)
        sidebar.addWidget(grp_dist)

        # Extra / Explanation
        grp_ans = QGroupBox("Card Extra / Explanation")
        ga_layout = QVBoxLayout(grp_ans)
        self.txt_extra = QTextEdit()
        self.txt_extra.setMaximumHeight(80)
        self.txt_extra.setPlaceholderText("Optional explanation shown on back...")
        ga_layout.addWidget(self.txt_extra)
        sidebar.addWidget(grp_ans)

        sidebar.addStretch()

        # Action Buttons
        act_row = QHBoxLayout()
        self.btn_save = QPushButton("Save Zones to Note")
        self.btn_save.setObjectName("saveBtn")
        self.btn_save.clicked.connect(self.save_and_close)
        act_row.addWidget(self.btn_save)

        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.clicked.connect(self.reject)
        act_row.addWidget(self.btn_cancel)

        sidebar.addLayout(act_row)
        layout.addLayout(sidebar, stretch=1)

    def load_note_data(self):
        note = self.editor.note
        if not note:
            return

        # Layout orientation
        if "Layout" in note and note["Layout"].strip().lower() == "vertical":
            self.radio_layout_v.setChecked(True)
        else:
            self.radio_layout_h.setChecked(True)

        # 1. Parse Image
        img_html = note["Image"] if "Image" in note else ""
        img_match = re.search(r'src="([^"]+)"', img_html) or re.search(r"src='([^']+)'", img_html)
        if not img_match:
            img_match = re.search(r'src=([^s>]+)', img_html)
        if img_match and mw and mw.col:
            img_filename = img_match.group(1)
            media_dir = mw.col.media.dir()
            full_path = os.path.join(media_dir, img_filename)
            if os.path.exists(full_path):
                self.pixmap = QPixmap(full_path)
                self.canvas.set_image(self.pixmap)

        # 2. Parse Zones
        raw_zones = (note["Zones"] if "Zones" in note else "").strip()
        parsed_zones = []
        if raw_zones:
            for item in raw_zones.split('|'):
                item = item.strip()
                if not item:
                    continue
                if '=' in item:
                    lbl, coords = item.split('=', 1)
                    coords = coords.strip()
                    parts = coords.replace('%', '').split(',')
                    if len(parts) == 2:
                        try:
                            px = float(parts[0].strip())
                            py = float(parts[1].strip())
                            parsed_zones.append({'label': lbl.strip(), 'x': px, 'y': py})
                        except ValueError:
                            pass
        self.zones = parsed_zones
        self.canvas.set_zones(self.zones)
        self.refresh_list()

        # 3. Parse Distractors
        raw_labels_str = note["Labels"] if "Labels" in note else ""
        raw_labels = [s.strip() for s in raw_labels_str.split('|') if s.strip()]
        zone_labels = [z['label'] for z in self.zones]
        distractors = [l for l in raw_labels if l not in zone_labels]
        self.txt_distractors.setText(" | ".join(distractors))

        # 4. Parse Extra (or fallback legacy Answer)
        extra_val = ""
        if "Extra" in note:
            extra_val = note["Extra"]
        elif "Answer" in note:
            extra_val = note["Answer"]
        self.txt_extra.setPlainText(extra_val)

    def refresh_list(self):
        self.list_zones.blockSignals(True)
        self.list_zones.clear()
        for i, z in enumerate(self.zones):
            item = QListWidgetItem(f"{i+1}. {z['label']} ({z['x']}%, {z['y']}%)")
            self.list_zones.addItem(item)
        if 0 <= self.canvas.selected_index < len(self.zones):
            self.list_zones.setCurrentRow(self.canvas.selected_index)
            z = self.zones[self.canvas.selected_index]
            self.txt_label.setText(z['label'])
            self.lbl_pos_x.setText(f"X: {z['x']:.1f}%")
            self.lbl_pos_y.setText(f"Y: {z['y']:.1f}%")
        else:
            self.txt_label.clear()
            self.lbl_pos_x.setText("X: --")
            self.lbl_pos_y.setText("Y: --")
        self.list_zones.blockSignals(False)

    def on_canvas_zones_changed(self, zones, selected_index):
        self.zones = zones
        self.refresh_list()

    def on_list_selection_changed(self, row: int):
        self.canvas.select_zone(row)
        if 0 <= row < len(self.zones):
            z = self.zones[row]
            self.txt_label.blockSignals(True)
            self.txt_label.setText(z['label'])
            self.txt_label.blockSignals(False)
            self.lbl_pos_x.setText(f"X: {z['x']:.1f}%")
            self.lbl_pos_y.setText(f"Y: {z['y']:.1f}%")

    def on_label_text_edited(self, text: str):
        idx = self.canvas.selected_index
        if 0 <= idx < len(self.zones):
            self.zones[idx]['label'] = text.strip()
            self.canvas.update()
            item = self.list_zones.item(idx)
            if item:
                item.setText(f"{idx+1}. {text.strip()} ({self.zones[idx]['x']}%, {self.zones[idx]['y']}%)")

    def add_manual_zone(self):
        new_zone = {'label': f"Label {len(self.zones) + 1}", 'x': 50.0, 'y': 50.0}
        self.zones.append(new_zone)
        self.canvas.set_zones(self.zones)
        self.canvas.select_zone(len(self.zones) - 1)
        self.refresh_list()

    def import_image_file(self, file_path: str):
        if not os.path.exists(file_path):
            return
        if mw and mw.col:
            try:
                fname = mw.col.media.add_file(file_path)
                if fname:
                    self.loaded_image_filename = fname
                    media_dir = mw.col.media.dir()
                    full_path = os.path.join(media_dir, fname)
                    self.pixmap = QPixmap(full_path if os.path.exists(full_path) else file_path)
                    self.canvas.set_image(self.pixmap)
                    self.lbl_title.setText(f"<b>Diagram image:</b> {fname} · <b>Click</b> diagram to add drop zone")
                    tooltip(f"Diagram image loaded: {fname}", period=2500)
                    return
            except Exception:
                pass
        self.pixmap = QPixmap(file_path)
        self.canvas.set_image(self.pixmap)
        self.lbl_title.setText("<b>Diagram loaded</b> · <b>Click</b> diagram to add drop zone")

    def import_image_object(self, img_obj):
        qimg = img_obj if isinstance(img_obj, QImage) else QImage(img_obj)
        if not qimg.isNull() and mw and mw.col:
            import time
            fname = f"ddi_paste_{int(time.time() * 1000)}.png"
            media_dir = mw.col.media.dir()
            save_path = os.path.join(media_dir, fname)
            try:
                qimg.save(save_path, "PNG")
                self.loaded_image_filename = fname
                self.pixmap = QPixmap.fromImage(qimg)
                self.canvas.set_image(self.pixmap)
                self.lbl_title.setText(f"<b>Diagram pasted:</b> {fname} · <b>Click</b> diagram to add drop zone")
                tooltip(f"Diagram image pasted & saved to note: {fname}", period=2500)
            except Exception:
                pass

    def paste_image_from_clipboard(self):
        cb = QApplication.clipboard()
        md = cb.mimeData()
        if md.hasImage():
            qimg = cb.image()
            if not qimg.isNull():
                self.import_image_object(qimg)
                return True
        elif md.hasUrls():
            urls = md.urls()
            if urls:
                fpath = urls[0].toLocalFile()
                if fpath and os.path.exists(fpath):
                    self.import_image_file(fpath)
                    return True
        elif cb.pixmap() and not cb.pixmap().isNull():
            self.import_image_object(cb.pixmap().toImage())
            return True
        tooltip("No image found on clipboard to paste.", period=2000)
        return False

    def browse_image_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Diagram Image",
            "",
            "Images (*.png *.jpg *.jpeg *.webp *.gif *.svg *.bmp *.tiff);;All Files (*)"
        )
        if path:
            self.import_image_file(path)

    def keyPressEvent(self, event):
        # Allow pasting image from anywhere in dialog unless editing text
        focus_w = self.focusWidget()
        is_text_focused = isinstance(focus_w, (QLineEdit, QTextEdit))
        
        is_paste = False
        if hasattr(QKeySequence, 'StandardKey') and event.matches(QKeySequence.StandardKey.Paste):
            is_paste = True
        elif hasattr(QKeySequence, 'Paste') and event.matches(QKeySequence.Paste):
            is_paste = True
        elif event.key() == (Qt.Key.Key_V if hasattr(Qt, 'Key') else Qt.Key_V):
            mods = event.modifiers()
            ctrl_or_cmd = (Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.MetaModifier) if hasattr(Qt, 'KeyboardModifier') else (Qt.ControlModifier | Qt.MetaModifier)
            if mods & ctrl_or_cmd:
                is_paste = True

        if is_paste and not is_text_focused:
            if self.paste_image_from_clipboard():
                event.accept()
                return

        super().keyPressEvent(event)

    def delete_selected_zone(self):
        idx = self.canvas.selected_index
        if 0 <= idx < len(self.zones):
            del self.zones[idx]
            self.canvas.set_zones(self.zones)
            self.canvas.select_zone(min(idx, len(self.zones) - 1))
            self.refresh_list()

    def save_and_close(self):
        if not self.zones:
            QMessageBox.warning(self, "No Zones Placed", "Please place at least one drop zone before saving.")
            return

        note = self.editor.note
        formatted_zones = " | ".join([f"{z['label']}={z['x']},{z['y']}" for z in self.zones])
        labels_list = [z['label'] for z in self.zones]

        if 'Image' in note and self.loaded_image_filename:
            note['Image'] = f'<img src="{self.loaded_image_filename}">'

        if 'Zones' in note:
            note['Zones'] = formatted_zones

        if 'Labels' in note:
            dist_raw = [s.strip() for s in self.txt_distractors.text().split('|') if s.strip()]
            combined = list(dict.fromkeys(labels_list + dist_raw))
            note['Labels'] = " | ".join(combined)

        if 'Layout' in note:
            note['Layout'] = "vertical" if self.radio_layout_v.isChecked() else "horizontal"

        if 'Extra' in note:
            note['Extra'] = self.txt_extra.toPlainText().strip()
        elif 'Answer' in note:
            note['Answer'] = self.txt_extra.toPlainText().strip()

        self.editor.loadNote()
        tooltip(f"Saved {len(self.zones)} drop zones to note.", period=3000)
        self.accept()


class FlowLayout(QLayout):
    """
    Standard Qt FlowLayout that arranges widgets horizontally and wraps to new lines as needed.
    Prevents horizontal overflow and container stretching.
    """
    def __init__(self, parent=None, margin=0, spacing=6):
        super().__init__(parent)
        if parent is not None:
            self.setContentsMargins(margin, margin, margin, margin)
        self.setSpacing(spacing)
        self.itemList: List[QLayoutItem] = []

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item):
        self.itemList.append(item)

    def count(self):
        return len(self.itemList)

    def itemAt(self, index):
        if 0 <= index < len(self.itemList):
            return self.itemList[index]
        return None

    def takeAt(self, index):
        if 0 <= index < len(self.itemList):
            return self.itemList.pop(index)
        return None

    def expandingDirections(self):
        try:
            return Qt.Orientation(0)
        except Exception:
            try:
                return Qt.Orientations(0)
            except Exception:
                return Qt.Orientation.Horizontal & Qt.Orientation.Vertical

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        return self.doLayout(QRect(0, 0, width, 0), True)

    def setGeometry(self, rect):
        super().setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()
        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())
        margins = self.contentsMargins()
        size += QSize(margins.left() + margins.right(), margins.top() + margins.bottom())
        return size

    def doLayout(self, rect, testOnly):
        x = rect.x()
        y = rect.y()
        lineHeight = 0
        spacing = self.spacing()

        for item in self.itemList:
            wid = item.widget()
            spaceX = spacing
            spaceY = spacing
            item_w = item.sizeHint().width()
            item_h = item.sizeHint().height()
            nextX = x + item_w + spaceX
            if nextX - spaceX > rect.right() and lineHeight > 0:
                x = rect.x()
                y = y + lineHeight + spaceY
                nextX = x + item_w + spaceX
                lineHeight = 0

            if not testOnly:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = nextX
            lineHeight = max(lineHeight, item_h)

        return y + lineHeight - rect.y()


class EasyCardCreatorDialog(QDialog):
    """
    Interactive, visual card creator for Drag & Drop Category Sorting cards.
    Allows easy category creation, direct item assignment, and distractors with a fixed, stable layout.
    """
    def __init__(self, editor: Editor, parent=None):
        super().__init__(parent or editor.parentWindow)
        self.editor = editor
        self.setWindowTitle("Category Sorting — Easy Card Creator")
        self.setFixedSize(880, 620)
        
        self.categories: List[str] = []
        self.category_items: Dict[str, List[str]] = {}
        self.unassigned_items: List[str] = []
        self.distractors: List[str] = []

        self.setup_ui()
        self.load_note_data()

    def setup_ui(self):
        dark = is_anki_dark_mode()
        del_btn_bg = "#451a1a" if dark else "#fee2e2"
        del_btn_border = "#7f1d1d" if dark else "#fca5a5"
        del_btn_color = "#fca5a5" if dark else "#b91c1c"
        del_btn_hover = "#7f1d1d" if dark else "#fecaca"

        card_bg = "#21252b" if dark else "#ffffff"
        card_border = "#3e4451" if dark else "#e2e8f0"
        chip_bg = "#282c34" if dark else "#f8fafc"
        chip_border = "#4b5263" if dark else "#cbd5e1"
        dist_bg = "#351a1e" if dark else "#fff1f2"
        dist_border = "#5e242c" if dark else "#fecdd3"

        self.setStyleSheet(f"""
            QDialog {{
                background-color: palette(window);
                color: palette(text);
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            }}
            QLabel {{
                color: palette(text);
            }}
            QGroupBox {{
                background-color: palette(window);
                border: 1px solid palette(mid);
                border-radius: 8px;
                margin-top: 8px;
                padding: 10px;
                color: palette(text);
                font-weight: 600;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 6px;
                color: palette(text);
            }}
            QLineEdit, QTextEdit, QComboBox {{
                background-color: palette(base);
                border: 1px solid palette(mid);
                border-radius: 6px;
                color: palette(text);
                padding: 5px 8px;
            }}
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{
                border: 1.5px solid #2563eb;
            }}
            QRadioButton {{
                color: palette(text);
                font-size: 12.5px;
                font-weight: 500;
                spacing: 6px;
            }}
            QRadioButton::indicator {{
                width: 15px;
                height: 15px;
                border-radius: 8px;
                border: 1.5px solid palette(mid);
                background-color: palette(base);
            }}
            QRadioButton::indicator:hover {{
                border-color: #3b82f6;
            }}
            QRadioButton::indicator:checked {{
                border: 4.5px solid #2563eb;
                background-color: palette(base);
            }}
            QPushButton {{
                background-color: palette(button);
                border: 1px solid palette(mid);
                border-radius: 6px;
                padding: 5px 12px;
                color: palette(button-text);
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: palette(midlight);
                border-color: palette(dark);
            }}
            QPushButton#saveBtn {{
                background-color: #2563eb;
                border: 1px solid #1d4ed8;
                color: #ffffff;
                font-weight: 600;
                padding: 7px 18px;
            }}
            QPushButton#saveBtn:hover {{
                background-color: #1d4ed8;
            }}
            QPushButton#primaryActionBtn {{
                background-color: #2563eb;
                border: 1px solid #1d4ed8;
                color: #ffffff;
                font-weight: 600;
                padding: 5px 12px;
            }}
            QPushButton#primaryActionBtn:hover {{
                background-color: #1d4ed8;
            }}
            QPushButton#delBtn {{
                background-color: {del_btn_bg};
                border: 1px solid {del_btn_border};
                color: {del_btn_color};
                font-size: 11px;
                padding: 3px 8px;
                font-weight: 500;
            }}
            QPushButton#delBtn:hover {{
                background-color: {del_btn_hover};
            }}
            QPushButton#chipDelBtn {{
                background: transparent;
                border: none;
                color: {del_btn_color};
                font-weight: 700;
                padding: 0 2px;
                font-size: 12px;
            }}
            QPushButton#chipDelBtn:hover {{
                color: #ef4444;
            }}
            QScrollArea {{
                border: 1px solid palette(mid);
                border-radius: 8px;
                background-color: palette(base);
            }}
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 14, 16, 14)
        main_layout.setSpacing(10)

        # Header Info
        header_box = QHBoxLayout()
        header_title = QLabel("<h2>Category Sorting — Easy Card Creator</h2>")
        header_title.setTextFormat(Qt.TextFormat.RichText if hasattr(Qt, 'TextFormat') else Qt.RichText)
        header_box.addWidget(header_title)
        header_box.addStretch()
        main_layout.addLayout(header_box)

        content_grid = QHBoxLayout()
        content_grid.setSpacing(14)

        # Left Column: Card Metadata (Prompts, Orientation & Explanation)
        left_col = QVBoxLayout()
        left_col.setSpacing(10)

        grp_meta = QGroupBox("Card Prompt & Orientation")
        gm_layout = QVBoxLayout(grp_meta)
        gm_layout.setSpacing(8)

        lbl_t = QLabel("Title / Topic:")
        self.txt_title = QLineEdit()
        self.txt_title.setPlaceholderText("e.g. Biology · Animal Classification")
        gm_layout.addWidget(lbl_t)
        gm_layout.addWidget(self.txt_title)

        lbl_q = QLabel("Question / Instructions:")
        self.txt_question = QLineEdit()
        self.txt_question.setPlaceholderText("e.g. Sort each creature into its biological class:")
        gm_layout.addWidget(lbl_q)
        gm_layout.addWidget(self.txt_question)

        lbl_lay = QLabel("Layout Orientation:")
        gm_layout.addWidget(lbl_lay)

        layout_radio_box = QHBoxLayout()
        layout_radio_box.setContentsMargins(0, 0, 0, 4)
        layout_radio_box.setSpacing(14)

        self.cat_radio_h = QRadioButton("Horizontal (Columns)")
        self.cat_radio_v = QRadioButton("Vertical (Rows)")
        self.cat_radio_h.setChecked(True)

        self.cat_layout_group = QButtonGroup(self)
        self.cat_layout_group.addButton(self.cat_radio_h, 0)
        self.cat_layout_group.addButton(self.cat_radio_v, 1)

        layout_radio_box.addWidget(self.cat_radio_h)
        layout_radio_box.addWidget(self.cat_radio_v)
        layout_radio_box.addStretch()
        gm_layout.addLayout(layout_radio_box)

        left_col.addWidget(grp_meta)

        grp_extra = QGroupBox("Explanation / Notes (Shown on Back)")
        ge_layout = QVBoxLayout(grp_extra)
        self.txt_extra = QTextEdit()
        self.txt_extra.setPlaceholderText("Optional notes or explanation revealed upon answering...")
        self.txt_extra.setMinimumHeight(110)
        ge_layout.addWidget(self.txt_extra)
        left_col.addWidget(grp_extra)

        left_col.addStretch()
        content_grid.addLayout(left_col, stretch=2)

        # Right Column: Visual Interactive Category Manager
        right_col = QVBoxLayout()
        right_col.setSpacing(10)

        grp_interactive = QGroupBox("Categories & Answer Assignment")
        gi_layout = QVBoxLayout(grp_interactive)
        gi_layout.setContentsMargins(10, 10, 10, 10)
        gi_layout.setSpacing(8)

        # 1. Add Category Input Bar
        add_cat_row = QHBoxLayout()
        add_cat_row.setSpacing(6)
        self.input_new_cat = QLineEdit()
        self.input_new_cat.setPlaceholderText("Enter category name (e.g. Mammals)...")
        self.input_new_cat.returnPressed.connect(self.add_category)
        add_cat_row.addWidget(self.input_new_cat)

        btn_add_cat = QPushButton("+ Add Category")
        btn_add_cat.setObjectName("primaryActionBtn")
        btn_add_cat.clicked.connect(self.add_category)
        add_cat_row.addWidget(btn_add_cat)
        gi_layout.addLayout(add_cat_row)

        # 2. Scrollable Category Cards & Assigned Items Board (Vertical Scroll Only)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        if hasattr(Qt, 'ScrollBarPolicy'):
            self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        else:
            self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.board_container = QWidget()
        self.board_layout = QVBoxLayout(self.board_container)
        self.board_layout.setContentsMargins(6, 6, 6, 6)
        self.board_layout.setSpacing(10)
        self.scroll_area.setWidget(self.board_container)
        gi_layout.addWidget(self.scroll_area, stretch=1)

        # 3. Distractor Decoy Items (Extra wrong answers)
        grp_dist = QGroupBox("Distractor Items (Optional Decoys)")
        gdist_layout = QVBoxLayout(grp_dist)
        gdist_layout.setContentsMargins(8, 8, 8, 8)
        gdist_layout.setSpacing(6)

        add_dist_row = QHBoxLayout()
        add_dist_row.setSpacing(6)
        self.input_new_dist = QLineEdit()
        self.input_new_dist.setPlaceholderText("Add extra wrong chip (e.g. Starfish)...")
        self.input_new_dist.returnPressed.connect(self.add_distractor)
        add_dist_row.addWidget(self.input_new_dist)

        btn_add_dist = QPushButton("+ Add Decoy")
        btn_add_dist.clicked.connect(self.add_distractor)
        add_dist_row.addWidget(btn_add_dist)
        gdist_layout.addLayout(add_dist_row)

        self.dist_chips_container = QWidget()
        self.dist_flow_layout = FlowLayout(self.dist_chips_container, margin=0, spacing=5)
        gdist_layout.addWidget(self.dist_chips_container)

        gi_layout.addWidget(grp_dist)

        right_col.addWidget(grp_interactive, stretch=1)
        content_grid.addLayout(right_col, stretch=3)

        main_layout.addLayout(content_grid, stretch=1)

        # Bottom Actions Bar
        act_row = QHBoxLayout()
        act_row.addStretch()

        self.btn_save = QPushButton("Save Card to Note")
        self.btn_save.setObjectName("saveBtn")
        self.btn_save.clicked.connect(self.save_and_close)
        act_row.addWidget(self.btn_save)

        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.clicked.connect(self.reject)
        act_row.addWidget(self.btn_cancel)

        main_layout.addLayout(act_row)

    def clear_layout(self, layout):
        if not layout:
            return
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

    def render_categories(self):
        """Renders the categories, assigned answers, and unassigned answers pool."""
        self.clear_layout(self.board_layout)

        dark = is_anki_dark_mode()
        card_bg = "#1e2227" if dark else "#ffffff"
        card_border = "#3a3f4b" if dark else "#cbd5e1"
        chip_bg = "#282c34" if dark else "#f1f5f9"
        chip_border = "#4b5263" if dark else "#cbd5e1"

        if not self.categories:
            empty_lbl = QLabel("<p style='color: #888; text-align: center; margin: 30px 0;'><b>No categories yet.</b><br><span style='font-size: 12px;'>Type a category name above and click <i>+ Add Category</i>.</span></p>")
            empty_lbl.setTextFormat(Qt.TextFormat.RichText if hasattr(Qt, 'TextFormat') else Qt.RichText)
            empty_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter if hasattr(Qt, 'AlignmentFlag') else Qt.AlignCenter)
            self.board_layout.addWidget(empty_lbl)
            self.board_layout.addStretch()
            return

        # Render each Category Card
        for cat in self.categories:
            items = self.category_items.get(cat, [])

            card_frame = QFrame()
            card_frame.setStyleSheet(f"""
                QFrame {{
                    background-color: {card_bg};
                    border: 1px solid {card_border};
                    border-radius: 8px;
                    padding: 8px;
                }}
            """)
            cf_layout = QVBoxLayout(card_frame)
            cf_layout.setContentsMargins(8, 8, 8, 8)
            cf_layout.setSpacing(6)

            # Card Header (Category Name, Count & Delete Button)
            head_row = QHBoxLayout()
            head_row.setSpacing(6)

            cat_title_lbl = QLabel(f"<b>{cat}</b> <span style='color: #888; font-size: 11px;'>({len(items)} items)</span>")
            cat_title_lbl.setTextFormat(Qt.TextFormat.RichText if hasattr(Qt, 'TextFormat') else Qt.RichText)
            head_row.addWidget(cat_title_lbl)
            head_row.addStretch()

            btn_del_cat = QPushButton("✕ Delete Category")
            btn_del_cat.setObjectName("delBtn")
            btn_del_cat.clicked.connect(lambda _, c=cat: self.remove_category(c))
            head_row.addWidget(btn_del_cat)
            cf_layout.addLayout(head_row)

            # Assigned Item Chips Container (Wrapping FlowLayout)
            chips_wrap_widget = QWidget()
            flow_chips = FlowLayout(chips_wrap_widget, margin=0, spacing=4)

            if not items:
                no_items_lbl = QLabel("<span style='color: #999; font-size: 11.5px; font-style: italic;'>No answers in this category yet.</span>")
                no_items_lbl.setTextFormat(Qt.TextFormat.RichText if hasattr(Qt, 'TextFormat') else Qt.RichText)
                flow_chips.addWidget(no_items_lbl)
            else:
                for idx, item_text in enumerate(items):
                    chip = QFrame()
                    chip.setStyleSheet(f"""
                        QFrame {{
                            background-color: {chip_bg};
                            border: 1px solid {chip_border};
                            border-radius: 5px;
                            padding: 1px 5px;
                        }}
                    """)
                    ch_layout = QHBoxLayout(chip)
                    ch_layout.setContentsMargins(3, 1, 3, 1)
                    ch_layout.setSpacing(4)

                    txt_lbl = QLabel(item_text)
                    txt_lbl.setStyleSheet("font-weight: 500; font-size: 11.5px;")
                    ch_layout.addWidget(txt_lbl)

                    btn_del_item = QPushButton("✕")
                    btn_del_item.setObjectName("chipDelBtn")
                    btn_del_item.setToolTip(f"Remove '{item_text}' from {cat}")
                    btn_del_item.clicked.connect(lambda _, c=cat, i=idx: self.remove_item_from_category(c, i))
                    ch_layout.addWidget(btn_del_item)

                    flow_chips.addWidget(chip)

            cf_layout.addWidget(chips_wrap_widget)

            # Inline Quick Add Item Row
            add_item_row = QHBoxLayout()
            add_item_row.setSpacing(6)

            txt_new_item = QLineEdit()
            txt_new_item.setPlaceholderText(f"Add answer to {cat} (Press Enter)...")
            txt_new_item.setStyleSheet("font-size: 12px; padding: 3px 6px;")
            add_item_row.addWidget(txt_new_item)

            btn_add_item = QPushButton("+ Add")
            btn_add_item.setStyleSheet("font-size: 12px; padding: 3px 10px;")
            
            def make_add_handler(c=cat, inp=txt_new_item):
                def handler():
                    val = inp.text().strip()
                    if val:
                        self.add_item_to_category(c, val)
                        inp.clear()
                        inp.setFocus()
                return handler

            handler_fn = make_add_handler(cat, txt_new_item)
            txt_new_item.returnPressed.connect(handler_fn)
            btn_add_item.clicked.connect(handler_fn)
            add_item_row.addWidget(btn_add_item)

            cf_layout.addLayout(add_item_row)
            self.board_layout.addWidget(card_frame)

        # Render Unassigned Answers section if any exist
        if self.unassigned_items:
            unass_frame = QFrame()
            unass_frame.setStyleSheet(f"""
                QFrame {{
                    background-color: {'#2a251e' if dark else '#fffbeb'};
                    border: 1px dashed {'#d97706' if dark else '#f59e0b'};
                    border-radius: 8px;
                    padding: 8px;
                }}
            """)
            uf_layout = QVBoxLayout(unass_frame)
            uf_layout.setContentsMargins(8, 8, 8, 8)
            uf_layout.setSpacing(6)

            u_head = QLabel("<b>Unassigned Answers</b> <span style='color: #888; font-size: 11px;'>(Select category to assign)</span>")
            u_head.setTextFormat(Qt.TextFormat.RichText if hasattr(Qt, 'TextFormat') else Qt.RichText)
            uf_layout.addWidget(u_head)

            u_wrap_widget = QWidget()
            u_flow = FlowLayout(u_wrap_widget, margin=0, spacing=4)

            for item_text in self.unassigned_items:
                chip = QFrame()
                chip.setStyleSheet(f"""
                    QFrame {{
                        background-color: {chip_bg};
                        border: 1px solid {chip_border};
                        border-radius: 5px;
                        padding: 1px 5px;
                    }}
                """)
                ch_layout = QHBoxLayout(chip)
                ch_layout.setContentsMargins(3, 1, 3, 1)
                ch_layout.setSpacing(4)

                txt_lbl = QLabel(item_text)
                txt_lbl.setStyleSheet("font-weight: 500; font-size: 11.5px;")
                ch_layout.addWidget(txt_lbl)

                # Quick assign combobox
                combo_assign = QComboBox()
                combo_assign.addItem("Assign to...")
                for c in self.categories:
                    combo_assign.addItem(c)
                combo_assign.setStyleSheet("font-size: 11px; padding: 1px 3px;")

                def make_combo_handler(it=item_text, cb=combo_assign):
                    def handler(idx):
                        if idx > 0:
                            selected_cat = cb.itemText(idx)
                            self.assign_unassigned_item(it, selected_cat)
                    return handler

                combo_assign.currentIndexChanged.connect(make_combo_handler(item_text, combo_assign))
                ch_layout.addWidget(combo_assign)

                btn_del_u = QPushButton("✕")
                btn_del_u.setObjectName("chipDelBtn")
                btn_del_u.setToolTip(f"Delete '{item_text}'")
                btn_del_u.clicked.connect(lambda _, it=item_text: self.remove_unassigned_item(it))
                ch_layout.addWidget(btn_del_u)

                u_flow.addWidget(chip)

            uf_layout.addWidget(u_wrap_widget)
            self.board_layout.addWidget(unass_frame)

        self.board_layout.addStretch()

    def render_distractors(self):
        """Renders the distractor decoy chips using FlowLayout."""
        self.clear_layout(self.dist_flow_layout)

        dark = is_anki_dark_mode()
        dist_bg = "#351a1e" if dark else "#fff1f2"
        dist_border = "#5e242c" if dark else "#fecdd3"

        if not self.distractors:
            no_d_lbl = QLabel("<span style='color: #888; font-size: 11.5px; font-style: italic;'>No distractor decoys added.</span>")
            no_d_lbl.setTextFormat(Qt.TextFormat.RichText if hasattr(Qt, 'TextFormat') else Qt.RichText)
            self.dist_flow_layout.addWidget(no_d_lbl)
        else:
            for idx, dist_text in enumerate(self.distractors):
                chip = QFrame()
                chip.setStyleSheet(f"""
                    QFrame {{
                        background-color: {dist_bg};
                        border: 1px solid {dist_border};
                        border-radius: 5px;
                        padding: 1px 5px;
                    }}
                """)
                ch_layout = QHBoxLayout(chip)
                ch_layout.setContentsMargins(3, 1, 3, 1)
                ch_layout.setSpacing(4)

                txt_lbl = QLabel(dist_text)
                txt_lbl.setStyleSheet("font-weight: 500; font-size: 11.5px; color: #e11d48;" if not dark else "font-weight: 500; font-size: 11.5px; color: #fb7185;")
                ch_layout.addWidget(txt_lbl)

                btn_del_d = QPushButton("✕")
                btn_del_d.setObjectName("chipDelBtn")
                btn_del_d.setToolTip(f"Remove distractor '{dist_text}'")
                btn_del_d.clicked.connect(lambda _, i=idx: self.remove_distractor(i))
                ch_layout.addWidget(btn_del_d)

                self.dist_flow_layout.addWidget(chip)

    def add_category(self):
        cat_name = self.input_new_cat.text().strip()
        if not cat_name:
            return
        if cat_name in self.categories:
            QMessageBox.information(self, "Category Exists", f"'{cat_name}' is already in your categories.")
            self.input_new_cat.clear()
            return
        self.categories.append(cat_name)
        if cat_name not in self.category_items:
            self.category_items[cat_name] = []
        self.input_new_cat.clear()
        self.render_categories()

    def remove_category(self, cat_name: str):
        if cat_name in self.categories:
            self.categories.remove(cat_name)
            # Move assigned items to unassigned so user work is not lost
            remaining_items = self.category_items.pop(cat_name, [])
            for it in remaining_items:
                if it not in self.unassigned_items:
                    self.unassigned_items.append(it)
            self.render_categories()

    def add_item_to_category(self, cat_name: str, item_text: str):
        item_text = item_text.strip()
        if not item_text:
            return
        if cat_name not in self.category_items:
            self.category_items[cat_name] = []
        self.category_items[cat_name].append(item_text)
        self.render_categories()

    def remove_item_from_category(self, cat_name: str, item_idx: int):
        if cat_name in self.category_items and 0 <= item_idx < len(self.category_items[cat_name]):
            self.category_items[cat_name].pop(item_idx)
            self.render_categories()

    def assign_unassigned_item(self, item_text: str, target_cat: str):
        if item_text in self.unassigned_items:
            self.unassigned_items.remove(item_text)
        if target_cat not in self.category_items:
            self.category_items[target_cat] = []
        self.category_items[target_cat].append(item_text)
        self.render_categories()

    def remove_unassigned_item(self, item_text: str):
        if item_text in self.unassigned_items:
            self.unassigned_items.remove(item_text)
            self.render_categories()

    def add_distractor(self):
        dist_text = self.input_new_dist.text().strip()
        if not dist_text:
            return
        self.distractors.append(dist_text)
        self.input_new_dist.clear()
        self.render_distractors()

    def remove_distractor(self, idx: int):
        if 0 <= idx < len(self.distractors):
            self.distractors.pop(idx)
            self.render_distractors()

    def load_note_data(self):
        note = self.editor.note
        if not note:
            return

        if "Title" in note:
            self.txt_title.setText(note["Title"])
        if "Question" in note:
            self.txt_question.setText(note["Question"])
        if "Extra" in note:
            self.txt_extra.setPlainText(note["Extra"])
        if "Layout" in note and note["Layout"].strip().lower() == "vertical":
            self.cat_radio_v.setChecked(True)
        else:
            self.cat_radio_h.setChecked(True)

        # Parse Categories
        raw_cats = (note["Categories"] if "Categories" in note else "") if note else ""
        if raw_cats:
            self.categories = [c.strip() for c in raw_cats.split("|") if c.strip()]
        else:
            self.categories = []

        # Parse Items (Format: Item=Category | Item=Category)
        self.category_items = {c: [] for c in self.categories}
        self.unassigned_items = []

        raw_items = (note["Items"] if "Items" in note else "") if note else ""
        if raw_items:
            for pair in raw_items.split("|"):
                p = pair.strip()
                if not p:
                    continue
                eq = p.find("=")
                if eq > 0:
                    it = p[:eq].strip()
                    ct = p[eq + 1:].strip()
                    if ct not in self.categories:
                        self.categories.append(ct)
                        self.category_items[ct] = []
                    self.category_items[ct].append(it)
                else:
                    self.unassigned_items.append(p)

        # Parse Distractors
        raw_dist = (note["Distractors"] if "Distractors" in note else "") if note else ""
        if raw_dist:
            self.distractors = [d.strip() for d in raw_dist.split("|") if d.strip()]
        else:
            self.distractors = []

        self.render_categories()
        self.render_distractors()

    def save_and_close(self):
        if not self.categories:
            QMessageBox.warning(self, "Missing Categories", "Please create at least one category before saving.")
            return

        total_items = sum(len(items) for items in self.category_items.values())
        if total_items == 0:
            QMessageBox.warning(self, "Missing Answers", "Please add at least one answer to your categories.")
            return

        note = self.editor.note
        if not note:
            return

        # Format Categories: Cat1 | Cat2
        cats_str = " | ".join(self.categories)

        # Format Items: Item=Category | Item=Category
        items_pairs = []
        for cat in self.categories:
            for it in self.category_items.get(cat, []):
                items_pairs.append(f"{it}={cat}")
        for unass in self.unassigned_items:
            items_pairs.append(unass)
        items_str = " | ".join(items_pairs)

        # Format Distractors: Decoy1 | Decoy2
        dist_str = " | ".join(self.distractors)

        if "Title" in note:
            note["Title"] = self.txt_title.text().strip()
        if "Question" in note:
            note["Question"] = self.txt_question.text().strip()
        if "Categories" in note:
            note["Categories"] = cats_str
        if "Items" in note:
            note["Items"] = items_str
        if "Distractors" in note:
            note["Distractors"] = dist_str
        if "Layout" in note:
            note["Layout"] = "vertical" if self.cat_radio_v.isChecked() else "horizontal"
        if "Extra" in note:
            note["Extra"] = self.txt_extra.toPlainText().strip()

        self.editor.loadNote()
        tooltip("Saved Category Sorting card to note.", period=3000)
        self.accept()


class DdiChoiceOption(QFrame):
    """
    Clickable option card matching native Anki list and button behavior.
    Supports native light and dark mode colors with high-contrast, perfectly readable hover and focus states.
    """
    clicked = pyqtSignal()

    def __init__(self, title: str, subtitle: str, parent=None):
        super().__init__(parent)
        self.dark = is_anki_dark_mode()
        self.title_text = title
        self.subtitle_text = subtitle
        self.setCursor(Qt.CursorShape.PointingHandCursor if hasattr(Qt, 'CursorShape') else Qt.PointingHandCursor)
        self.setFixedHeight(54)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus if hasattr(Qt, 'FocusPolicy') else Qt.StrongFocus)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 6, 12, 6)
        layout.setSpacing(2)

        self.lbl_title = QLabel(title)
        self.lbl_subtitle = QLabel(subtitle)

        layout.addWidget(self.lbl_title)
        layout.addWidget(self.lbl_subtitle)

        self.is_hovered = False
        self.is_pressed = False
        self.update_style()

    def update_style(self):
        if self.dark:
            # Native Anki Dark Theme Palette
            if self.is_pressed:
                bg = "#21262d"
                border = "#388bfd"
                t_color = "#58a6ff"
                s_color = "#c9d1d9"
            elif self.is_hovered or self.hasFocus():
                bg = "#30363d"
                border = "#58a6ff"
                t_color = "#58a6ff"
                s_color = "#c9d1d9"
            else:
                bg = "#21262d"
                border = "#30363d"
                t_color = "#f0f6fc"
                s_color = "#8b949e"
        else:
            # Native Anki Light Theme Palette
            if self.is_pressed:
                bg = "#dbeafe"
                border = "#1d4ed8"
                t_color = "#1d4ed8"
                s_color = "#475569"
            elif self.is_hovered or self.hasFocus():
                bg = "#eff6ff"
                border = "#2563eb"
                t_color = "#1d4ed8"
                s_color = "#334155"
            else:
                bg = "#ffffff"
                border = "#d1d5db"
                t_color = "#111827"
                s_color = "#6b7280"

        self.setStyleSheet(f"""
            QFrame {{
                background-color: {bg};
                border: 1px solid {border};
                border-radius: 4px;
            }}
        """)
        self.lbl_title.setStyleSheet(f"font-size: 13px; font-weight: bold; color: {t_color}; background: transparent; border: none;")
        self.lbl_subtitle.setStyleSheet(f"font-size: 11px; color: {s_color}; background: transparent; border: none;")

    def enterEvent(self, event):
        self.is_hovered = True
        self.update_style()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.is_hovered = False
        self.is_pressed = False
        self.update_style()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == (Qt.MouseButton.LeftButton if hasattr(Qt, 'MouseButton') else Qt.LeftButton):
            self.is_pressed = True
            self.update_style()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.is_pressed and event.button() == (Qt.MouseButton.LeftButton if hasattr(Qt, 'MouseButton') else Qt.LeftButton):
            self.is_pressed = False
            self.update_style()
            if self.rect().contains(event.pos()):
                self.clicked.emit()
        super().mouseReleaseEvent(event)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key.Key_Return if hasattr(Qt, 'Key') else Qt.Key_Return,
                           Qt.Key.Key_Enter if hasattr(Qt, 'Key') else Qt.Key_Enter,
                           Qt.Key.Key_Space if hasattr(Qt, 'Key') else Qt.Key_Space):
            self.clicked.emit()
        else:
            super().keyPressEvent(event)

    def focusInEvent(self, event):
        self.update_style()
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self.update_style()
        super().focusOutEvent(event)


class DdiChoiceDialog(QDialog):
    """
    Native Anki choice dialog for creating Drag & Drop Cards.
    Presents two clear, compact selectable options matching standard Anki dialog styling.
    Positioned attached directly near and just below the clicked toolbar icon.
    """
    def __init__(self, editor: Editor, parent=None):
        super().__init__(parent or editor.parentWindow)
        self.editor = editor
        self.setWindowTitle("Create Drag & Drop Card")
        self.setFixedSize(360, 205)
        self.setup_ui()
        self.position_near_trigger()

    def showEvent(self, event):
        super().showEvent(event)
        self.position_near_trigger()

    def position_near_trigger(self):
        try:
            dlg_w = self.width() or 360
            dlg_h = self.height() or 205
            pos = QCursor.pos()
            
            # Position relative to editor and clicked toolbar button
            parent_window = getattr(self.editor, "parentWindow", None) if self.editor else None
            if parent_window and hasattr(parent_window, "geometry"):
                pw_geo = parent_window.geometry()
                # If mouse cursor is inside or near parent window, attach just below the click point
                if pw_geo.contains(pos) or (abs(pos.x() - pw_geo.center().x()) < pw_geo.width() and abs(pos.y() - pw_geo.top()) < 250):
                    x = pos.x() - 35
                    y = pos.y() + 10
                else:
                    # Fallback for keyboard shortcut (Ctrl+Alt+D): position attached below top toolbar
                    x = pw_geo.x() + 90
                    y = pw_geo.y() + 85
            else:
                x = pos.x() - 35
                y = pos.y() + 10

            # Screen bounds safety clamping
            screen_geo = None
            if hasattr(QGuiApplication, "screenAt"):
                screen = QGuiApplication.screenAt(pos) or QGuiApplication.primaryScreen()
                if screen:
                    screen_geo = screen.availableGeometry()
            elif hasattr(QApplication, "desktop"):
                screen_geo = QApplication.desktop().availableGeometry(pos)

            if screen_geo:
                if x + dlg_w > screen_geo.right() - 8:
                    x = screen_geo.right() - dlg_w - 8
                if x < screen_geo.left() + 8:
                    x = screen_geo.left() + 8
                if y + dlg_h > screen_geo.bottom() - 8:
                    y = max(screen_geo.top() + 8, pos.y() - dlg_h - 10)
                if y < screen_geo.top() + 8:
                    y = screen_geo.top() + 8

            self.move(int(x), int(y))
        except Exception:
            pass

    def setup_ui(self):
        dark = is_anki_dark_mode()
        btn_bg = "#383838" if dark else "#e1e1e1"
        btn_hover = "#444444" if dark else "#d5d5d5"
        btn_border = "#555555" if dark else "#adadad"

        self.setStyleSheet(f"""
            QDialog {{
                background-color: palette(window);
                color: palette(window-text);
            }}
            QPushButton.cancel-btn {{
                background-color: {btn_bg};
                border: 1px solid {btn_border};
                border-radius: 4px;
                padding: 4px 14px;
                color: palette(button-text);
                font-size: 12px;
                min-width: 70px;
            }}
            QPushButton.cancel-btn:hover {{
                background-color: {btn_hover};
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 12)
        layout.setSpacing(8)

        # Prompt / Subtitle
        lbl_sub = QLabel("Choose the type of card:")
        lbl_sub.setStyleSheet("font-size: 12px; color: palette(window-text);")
        layout.addWidget(lbl_sub)

        # Options Container
        cards_vbox = QVBoxLayout()
        cards_vbox.setSpacing(6)

        # 1. Option 1: Image Labeling
        self.opt_image = DdiChoiceOption(
            title="Image Labeling",
            subtitle="Place labels on a diagram",
            parent=self
        )
        self.opt_image.clicked.connect(self.select_image_labeling)
        cards_vbox.addWidget(self.opt_image)

        # 2. Option 2: Category Sorting
        self.opt_cat = DdiChoiceOption(
            title="Category Sorting",
            subtitle="Sort items into groups",
            parent=self
        )
        self.opt_cat.clicked.connect(self.select_category_sorting)
        cards_vbox.addWidget(self.opt_cat)

        layout.addLayout(cards_vbox)

        layout.addSpacing(4)

        # Bottom Bar with Cancel Button
        bottom_bar = QHBoxLayout()
        bottom_bar.addStretch()

        btn_cancel = QPushButton("Cancel")
        btn_cancel.setProperty("class", "cancel-btn")
        btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor if hasattr(Qt, 'CursorShape') else Qt.PointingHandCursor)
        btn_cancel.setAutoDefault(False)
        btn_cancel.setDefault(False)
        btn_cancel.clicked.connect(self.reject)
        bottom_bar.addWidget(btn_cancel)

        layout.addLayout(bottom_bar)

        # Focus initial option
        self.opt_image.setFocus()

    def select_image_labeling(self):
        self.accept()
        set_editor_note_type(self.editor, NOTE_TYPE_NAME)
        dlg = DdiVisualEditorDialog(self.editor, parent=self.editor.parentWindow)
        dlg.exec()

    def select_category_sorting(self):
        self.accept()
        set_editor_note_type(self.editor, CAT_NOTE_TYPE_NAME)
        dlg = EasyCardCreatorDialog(self.editor, parent=self.editor.parentWindow)
        dlg.exec()


PLACE_ZONES_ICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <rect width="18" height="18" x="3" y="3" rx="2" stroke="#94a3b8"/>
  <circle cx="8.5" cy="8.5" r="1.5" fill="#94a3b8" stroke="none"/>
  <path d="m21 15-5-5L5 21" stroke="#94a3b8"/>
  <rect width="8" height="5" x="11" y="6" rx="1" stroke="#3b82f6" stroke-width="1.8" stroke-dasharray="2 1" fill="#3b82f6" fill-opacity="0.2"/>
</svg>"""

MODE_IMAGE_ICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="#3b82f6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <rect width="18" height="18" x="3" y="3" rx="2.5" stroke="#3b82f6"/>
  <circle cx="8.5" cy="8.5" r="1.5" fill="#3b82f6" stroke="none"/>
  <path d="m21 15-5-5L5 21" stroke="#3b82f6"/>
  <rect width="7" height="4" x="12" y="6" rx="1" stroke="#3b82f6" stroke-width="1.6" stroke-dasharray="2 1" fill="#3b82f6" fill-opacity="0.25"/>
</svg>"""

MODE_CATEGORY_ICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="#3b82f6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <rect x="3" y="3.5" width="8" height="17" rx="2" stroke="#3b82f6" stroke-width="1.8"/>
  <rect x="13" y="3.5" width="8" height="17" rx="2" stroke="#3b82f6" stroke-width="1.8"/>
  <line x1="5.5" y1="7.5" x2="8.5" y2="7.5" stroke="#3b82f6" stroke-width="1.6" stroke-linecap="round"/>
  <line x1="5.5" y1="11.5" x2="8.5" y2="11.5" stroke="#3b82f6" stroke-width="1.6" stroke-linecap="round"/>
  <line x1="5.5" y1="15.5" x2="8.5" y2="15.5" stroke="#3b82f6" stroke-width="1.6" stroke-linecap="round"/>
  <line x1="15.5" y1="7.5" x2="18.5" y2="7.5" stroke="#3b82f6" stroke-width="1.6" stroke-linecap="round"/>
  <line x1="15.5" y1="11.5" x2="18.5" y2="11.5" stroke="#3b82f6" stroke-width="1.6" stroke-linecap="round"/>
</svg>"""


def get_place_zones_icon_path() -> Optional[str]:
    """Ensures place_zones.svg icon exists in the addon icons directory and returns its absolute path."""
    try:
        addon_dir = os.path.dirname(os.path.abspath(__file__))
        icons_dir = os.path.join(addon_dir, "icons")
        os.makedirs(icons_dir, exist_ok=True)
        icon_path = os.path.join(icons_dir, "place_zones.svg")
        if not os.path.exists(icon_path):
            with open(icon_path, "w", encoding="utf-8") as f:
                f.write(PLACE_ZONES_ICON_SVG)
        return icon_path
    except Exception:
        return None


def get_mode_image_icon_path() -> Optional[str]:
    """Ensures mode_image.svg icon exists and returns its path."""
    try:
        addon_dir = os.path.dirname(os.path.abspath(__file__))
        icons_dir = os.path.join(addon_dir, "icons")
        os.makedirs(icons_dir, exist_ok=True)
        icon_path = os.path.join(icons_dir, "mode_image.svg")
        if not os.path.exists(icon_path):
            with open(icon_path, "w", encoding="utf-8") as f:
                f.write(MODE_IMAGE_ICON_SVG)
        return icon_path
    except Exception:
        return None


def get_mode_category_icon_path() -> Optional[str]:
    """Ensures mode_category.svg icon exists and returns its path."""
    try:
        addon_dir = os.path.dirname(os.path.abspath(__file__))
        icons_dir = os.path.join(addon_dir, "icons")
        os.makedirs(icons_dir, exist_ok=True)
        icon_path = os.path.join(icons_dir, "mode_category.svg")
        if not os.path.exists(icon_path):
            with open(icon_path, "w", encoding="utf-8") as f:
                f.write(MODE_CATEGORY_ICON_SVG)
        return icon_path
    except Exception:
        return None


def open_drag_drop_card_creator(editor: Editor):
    """Opens the Drag & Drop card creator choice dialog or appropriate tool."""
    ensure_all_note_types()
    dlg = DdiChoiceDialog(editor, parent=editor.parentWindow)
    dlg.position_near_trigger()
    dlg.exec()


def on_setup_editor_buttons(buttons: List[str], editor: Editor) -> List[str]:
    """Adds a single unified drag & drop card button to Anki's Note Editor toolbar."""
    icon_path = get_place_zones_icon_path()
    btn = editor.addButton(
        icon=icon_path,
        cmd="ddi_create_card",
        func=lambda ed=editor: open_drag_drop_card_creator(ed),
        tip="Create Drag & Drop Card (Ctrl+Alt+D)",
        keys="Ctrl+Alt+D"
    )
    buttons.append(btn)
    return buttons


def add_menu_action():
    """Adds 'Drag Drop' item to Anki's Tools menu."""
    action = QAction("Drag Drop", mw)
    action.triggered.connect(open_ddi_settings_dialog)
    mw.form.menuTools.addAction(action)


def on_webview_will_set_content(web_content, context):
    """Dynamically injects CSS rules into web views, e.g., hiding Resultat box during review."""
    try:
        config = mw.addonManager.getConfig(__name__) or {}
        hide_res = config.get("hide_resultat", not config.get("show_score_badge", True))
        if hide_res:
            web_content.head += """
<style id="ddi-hide-resultat-style">
  #scoreBox,
  #catScoreBox,
  .score,
  .section-label,
  #result,
  .resultat,
  div:has(> #scoreBox),
  div:has(> #catScoreBox),
  div:has(> #result) {
    display: none !important;
  }
</style>
"""
    except Exception:
        pass


# Initialize hooks & actions
gui_hooks.profile_did_open.append(ensure_all_note_types)
gui_hooks.editor_did_init_buttons.append(on_setup_editor_buttons)
try:
    gui_hooks.webview_will_set_content.append(on_webview_will_set_content)
except Exception:
    pass
addHook("profileLoaded", add_menu_action)

try:
    if mw and mw.col:
        ensure_all_note_types(force_update=False)
except Exception:
    pass

try:
    mw.addonManager.setConfigAction(__name__, open_ddi_settings_dialog)
except Exception:
    pass
