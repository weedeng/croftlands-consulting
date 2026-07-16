from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, ListFlowable, ListItem, KeepTogether
)

OUTPUT = r"C:\Users\graem\Website buildout\CrossLLM_Chat_Index_v1_Spec.pdf"

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'TitleX', parent=styles['Title'],
    fontName='Helvetica-Bold', fontSize=22, leading=26,
    textColor=colors.HexColor('#1a365d'), spaceAfter=6, alignment=TA_LEFT,
)
subtitle_style = ParagraphStyle(
    'Subtitle', parent=styles['Normal'],
    fontSize=11, leading=14, textColor=colors.HexColor('#555555'),
    spaceAfter=18,
)
h1 = ParagraphStyle(
    'H1', parent=styles['Heading1'],
    fontName='Helvetica-Bold', fontSize=15, leading=19,
    textColor=colors.HexColor('#1a365d'),
    spaceBefore=14, spaceAfter=8,
)
h2 = ParagraphStyle(
    'H2', parent=styles['Heading2'],
    fontName='Helvetica-Bold', fontSize=12, leading=16,
    textColor=colors.HexColor('#2c5282'),
    spaceBefore=10, spaceAfter=5,
)
body = ParagraphStyle(
    'Body', parent=styles['BodyText'],
    fontName='Helvetica', fontSize=10, leading=14,
    spaceAfter=6, alignment=TA_LEFT,
)
bullet = ParagraphStyle(
    'Bullet', parent=body, leftIndent=14, bulletIndent=2, spaceAfter=3,
)
small = ParagraphStyle(
    'Small', parent=body, fontSize=9, leading=12,
    textColor=colors.HexColor('#666666'),
)

def P(t, s=body): return Paragraph(t, s)

def bullets(items):
    return ListFlowable(
        [ListItem(P(i, bullet), leftIndent=10) for i in items],
        bulletType='bullet', start='•', leftIndent=14,
        bulletFontName='Helvetica', bulletFontSize=10,
    )

doc = SimpleDocTemplate(
    OUTPUT, pagesize=A4,
    leftMargin=2.0*cm, rightMargin=2.0*cm,
    topMargin=1.8*cm, bottomMargin=1.8*cm,
    title="Cross-LLM Chat Index - v1 Spec",
    author="Croftlands Consulting",
)

story = []

# --- Cover header ---
story.append(P("Cross-LLM Chat Index", title_style))
story.append(P("v1 Product Specification &mdash; Option B (Pure Browser Extension)", subtitle_style))

# --- Executive summary ---
story.append(P("Executive Summary", h1))
story.append(P(
    "A privacy-first productivity tool that indexes the user&rsquo;s conversations across "
    "Claude, ChatGPT, Grok, and Gemini into a single, searchable place. Users continue "
    "using each AI tool the way they do today; the extension passively captures their "
    "conversations and provides fast search, summaries, and one-click deep-links back to "
    "the original thread."
))
story.append(P(
    "Architecture choice for v1 is <b>Option B: a pure Chrome/Edge browser extension</b> "
    "with a full-page in-browser UI. No native desktop app, no backend, all data stored "
    "locally in the browser. This dissolves the &lsquo;web session must be active&rsquo; "
    "sync problem because the extension is alive whenever the browser is."
))

# --- Why Option B ---
story.append(P("Why Option B (vs. desktop app or hybrid)", h1))
data = [
    ['Dimension', 'Option B (Extension)', 'Desktop App + Ext.'],
    ['Build scope', 'One artifact', 'Two artifacts'],
    ['Auto-sync', 'Passive (always-on)', 'Requires launch-tab dance'],
    ['Install friction', 'One click (Web Store)', 'Installer + extension'],
    ['Updates', 'Automatic via Web Store', 'Manual / auto-updater'],
    ['Storage ceiling', 'IndexedDB (tens of K)', 'Unlimited (SQLite)'],
    ['Price ceiling', 'Lower expectation', 'Higher expectation'],
    ['OS packaging', 'None', 'Mac + Windows builds'],
]
t = Table(data, colWidths=[5.0*cm, 5.5*cm, 5.5*cm])
t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a365d')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 9),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#cccccc')),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f5f7fa')]),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
]))
story.append(t)
story.append(Spacer(1, 6))
story.append(P(
    "Trade-off accepted: lower per-unit price and a hard ceiling on local storage. "
    "Revisit a native wrapper (Option C) only if users hit storage limits or demand "
    "a &lsquo;real app&rsquo; feel.", small
))

# --- v1 plan ---
story.append(P("v1 Concrete Plan", h1))

story.append(P("Platform &amp; runtime", h2))
story.append(bullets([
    "Chrome + Edge extension, Manifest V3.",
    "Firefox added post-v1 if asked for.",
    "Local-only storage. No backend, no cloud sync in v1.",
]))

story.append(P("User interface", h2))
story.append(bullets([
    "Full-page tab launched from the extension icon (<code>chrome-extension://&hellip;/app.html</code>).",
    "Looks and behaves like a standalone app inside a browser tab.",
    "Left rail: provider filter (Claude / ChatGPT / Grok / Gemini), date range, tags, starred.",
    "Main pane: conversation cards &mdash; title, provider badge, date, snippet/summary, tags.",
    "Detail view: full conversation rendered with markdown / code blocks / tables, plus a prominent <b>&lsquo;Open in [Provider]&rsquo;</b> button.",
]))

story.append(P("Storage", h2))
story.append(bullets([
    "IndexedDB for the conversation index. Comfortable for tens of thousands of conversations.",
    "Bulk export to JSON file as a manual backup.",
    "Bulk import to restore on a new machine or browser profile.",
]))

story.append(P("Capture (the workhorse)", h2))
story.append(bullets([
    "Content scripts on <b>claude.ai</b>, <b>chatgpt.com</b>, <b>grok.com</b>, <b>gemini.google.com</b>.",
    "Watch for new or updated conversations as the user chats; write to IndexedDB.",
    "Capture: title, full message history, conversation URL, timestamps, model used.",
    "Gemini and Grok are fully covered (web-only).",
    "Claude and ChatGPT desktop apps are covered <i>indirectly</i>: both sync to their web backends, so the extension catches those conversations next time the web app is active.",
]))

story.append(P("Backfill &amp; safety net", h2))
story.append(bullets([
    "Drag-and-drop import of each provider&rsquo;s official export .zip file (ChatGPT, Claude, Gemini via Google Takeout, Grok via X export).",
    "Parser per provider, intelligent dedupe by conversation ID on re-import.",
    "&lsquo;Add manually&rsquo;: paste a URL + title + note as an escape hatch for anything automation misses.",
]))

story.append(P("Search", h2))
story.append(bullets([
    "v1: keyword full-text search over titles, messages, tags, notes.",
    "Filters: provider, date range, tag, starred.",
    "v1.x: optional local semantic search via a small in-browser embedding model (lazy-loaded; ~100&ndash;200&nbsp;MB).",
]))

story.append(P("Summaries", h2))
story.append(bullets([
    "Auto-generate a 1&ndash;2 sentence summary per conversation on first index.",
    "Default: local model running in the extension (free, private, slower).",
    "Pro option: user supplies a cheap API key (Haiku / GPT-4o-mini / Gemini Flash) for higher quality.",
]))

story.append(P("Deep-linking back to the source", h2))
story.append(bullets([
    "ChatGPT: <code>chatgpt.com/c/&lt;id&gt;</code>",
    "Claude: <code>claude.ai/chat/&lt;id&gt;</code>",
    "Gemini: <code>gemini.google.com/app/&lt;id&gt;</code>",
    "Grok: <code>grok.com/chat/&lt;id&gt;</code>",
    "&lsquo;Open in [Provider]&rsquo; focuses an existing tab if open, else opens a new one.",
]))

story.append(P("Organisation", h2))
story.append(bullets([
    "User-defined tags (e.g. <code>#client-acme</code>, <code>#tax-research</code>).",
    "Star / pin important conversations.",
    "Smart folders &mdash; saved searches that auto-update.",
]))

story.append(P("Sync status panel", h2))
story.append(bullets([
    "Per-provider: last successful capture, # of conversations indexed.",
    "Gentle nudge if a provider hasn&rsquo;t synced in N days: &lsquo;Haven&rsquo;t seen Claude conversations in a while &mdash; open claude.ai to sync.&rsquo;",
    "Turns the constraint into a normal background-sync UX, not a mysterious gap.",
]))

story.append(PageBreak())

# --- Out of scope ---
story.append(P("Explicitly Out of Scope for v1", h1))
story.append(bullets([
    "No prompt engine &mdash; users keep using Claude / ChatGPT / Grok / Gemini directly.",
    "No editing of original conversations.",
    "No multi-device real-time sync (v2).",
    "No team or sharing features.",
    "No automatic model failover or routing.",
    "No iOS or Android client (v2: read-only viewer + Share Sheet target).",
    "No native desktop wrapper (revisit only if storage or pricing forces it).",
]))

# --- Capture matrix ---
story.append(P("Provider Capture Matrix", h1))
data = [
    ['Provider', 'How user accesses it', 'v1 capture path'],
    ['ChatGPT', 'Web + desktop app + iPhone', 'Web extension; desktop syncs via web; iPhone via export or Share'],
    ['Claude', 'Web + desktop app + iPhone', 'Web extension; desktop syncs via web; iPhone via export or Share'],
    ['Gemini', 'Web only (no desktop app)', 'Web extension (full coverage)'],
    ['Grok', 'Web only (grok.com / x.com)', 'Web extension (full coverage)'],
]
t = Table(data, colWidths=[2.8*cm, 5.5*cm, 8.0*cm])
t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a365d')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 9),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#cccccc')),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f5f7fa')]),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
]))
story.append(t)
story.append(Spacer(1, 8))
story.append(P(
    "<b>Expectation to document explicitly in onboarding:</b> the extension captures "
    "ChatGPT and Claude <i>desktop app</i> conversations only when the user&rsquo;s web "
    "session is active in the same browser. In practice this means keeping a pinned tab "
    "open, or visiting the web version occasionally. The Sync Status panel surfaces this "
    "naturally.", small
))

# --- Risks ---
story.append(P("Risks &amp; Sticking Points", h1))
risks = [
    ("ToS grey area for the extension.",
     "Reading the user&rsquo;s own conversations from their own logged-in session is generally tolerated. "
     "Ship clear language: &lsquo;The extension reads only your own conversations from your own browser, never sends them to us.&rsquo; "
     "Local-only storage strengthens this position."),
    ("DOM breakage on provider redesigns.",
     "Every web UI redesign at Claude / ChatGPT / Gemini / Grok can break content-script selectors. "
     "Budget ~2&ndash;4 hours/month of maintenance. Manageable but ongoing."),
    ("iPhone coverage gap.",
     "v1 captures iOS conversations only after they sync to the provider&rsquo;s web backend (usually seconds), and only when the user next has the web app active. "
     "Mobile-first capture (Share Sheet target, native viewer) is a v2 item. State this clearly on the landing page."),
    ("IndexedDB storage limits and purging.",
     "Browsers can evict IndexedDB under storage pressure. Mitigate with the <code>navigator.storage.persist()</code> API and regular export-to-file backups."),
    ("Provider export lag.",
     "ChatGPT exports can take hours to arrive. Acceptable for backfill, unacceptable as the only ingestion path. Extension is the live path."),
    ("Search quality on long technical threads.",
     "Keyword FTS handles most queries; code-heavy or mixed-language threads sometimes need semantic search. Plan local embeddings as a v1.x add-on."),
    ("Competition window is open but narrow.",
     "Nothing dominant in the multi-LLM cross-provider search niche today. A 6&ndash;12 month window before someone bigger ships something similar."),
]
for title_, detail in risks:
    story.append(P(f"<b>{title_}</b>", body))
    story.append(P(detail, body))

# --- Pricing ---
story.append(P("Pricing &amp; Positioning", h1))
story.append(bullets([
    "<b>Free tier:</b> manual .zip imports, keyword search, deep-link.",
    "<b>Pro (one-time $19.99&ndash;$29 or $4&ndash;5/month):</b> auto-capture, semantic search, summaries, smart folders.",
    "<b>Distribution:</b> Chrome Web Store + a marketing site selling license keys via Stripe. Keeps the customer relationship.",
    "<b>Positioning line:</b> &lsquo;All your AI conversations, searchable in seconds. Stays on your machine.&rsquo;",
    "<b>Audience to seed:</b> Hacker News, productivity Twitter, finance / consulting / dev subreddits, LinkedIn AI groups.",
]))

# --- Build order ---
story.append(P("v1 Build Order", h1))
order = [
    "Extension scaffolding (MV3, build pipeline, packaging script).",
    "IndexedDB schema + data-access layer.",
    "Importer for ChatGPT export .zip (best-documented format).",
    "Full-page UI shell + browse/search list view.",
    "FTS5-equivalent keyword search over IndexedDB.",
    "Detail view + &lsquo;Open in Provider&rsquo; deep-link.",
    "Content script for ChatGPT &mdash; prove the live-capture pattern end-to-end.",
    "Extend content scripts to Claude, Gemini, Grok.",
    "Importers for the other three providers&rsquo; export formats.",
    "Sync status panel + storage persistence prompt.",
    "Tags, stars, smart folders.",
    "Local-model summaries.",
    "Polish, license-key flow, Chrome Web Store submission.",
]
story.append(ListFlowable(
    [ListItem(P(s, body), leftIndent=10) for s in order],
    bulletType='1', leftIndent=18,
))
story.append(Spacer(1, 4))
story.append(P(
    "Rough effort: 6&ndash;10 weeks of focused evening/weekend work for a competent solo "
    "developer; longer if new to MV3 extensions.", small
))

# --- Open decisions ---
story.append(P("Open Decisions Before Build Starts", h1))
story.append(bullets([
    "<b>Pricing model:</b> one-time vs. subscription.",
    "<b>Licence delivery:</b> Chrome Web Store payments vs. external Stripe + licence key.",
    "<b>Summary engine default:</b> local model from day one, or require API key for Pro only.",
    "<b>Brand &amp; name:</b> Croftlands sub-brand vs. standalone product brand.",
    "<b>Beta cohort:</b> private list of 20&ndash;50 multi-LLM users before public launch.",
]))

doc.build(story)
print(f"Wrote: {OUTPUT}")
