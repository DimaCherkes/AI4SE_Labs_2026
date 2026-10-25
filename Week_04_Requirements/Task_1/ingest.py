"""
Deterministic Ingestion Engine for Software Requirements Refinement Agentic Network.

Satisfies:
- ANS2: Non-AI deterministic ingestion node.
- OS4: Complete source document provenance and relative path tracing.
- OS8: Completeness across heterogeneous input formats (.txt and .eml).
- OS9: Identification and tagging of non-functional conversational chatter.
"""

from __future__ import annotations

import argparse
import email
from email.utils import parsedate_to_datetime
import json
from pathlib import Path
import re
from typing import Any, Dict, List, Optional, Union

# Dual compatibility: Pydantic v2 / v1 with fallback to standard dataclass
try:
    from pydantic import BaseModel, Field
except ImportError:
    # Graceful fallback if pydantic is not installed in current environment
    class BaseModel:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
        def model_dump(self) -> Dict[str, Any]:
            return self.__dict__.copy()
        def dict(self) -> Dict[str, Any]:
            return self.__dict__.copy()
    def Field(default=None, default_factory=None, description=""):
        return default_factory() if default_factory else default


# ==============================================================================
# Data Models (PROJECT.md Interface Contract)
# ==============================================================================

class ParsedMessage(BaseModel):
    """Represents a single RFC 822 message in a multi-message thread."""
    part_index: int = Field(default=1, description="1-based index within thread")
    sender: str = Field(default="", description="From header value")
    recipient: str = Field(default="", description="To header value")
    cc: Optional[str] = Field(default=None, description="Cc header value if present")
    subject: str = Field(default="", description="Subject header value")
    raw_date: str = Field(default="", description="Verbatim Date header value")
    parsed_date: Optional[str] = Field(default=None, description="Normalized ISO 8601 timestamp")
    is_summary: bool = Field(default=False, description="True if Katherine Gregory consensus summary")
    body: str = Field(default="", description="Clean text body")
    noise_snippets: List[str] = Field(default_factory=list, description="Detected non-functional chatter")

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump() if hasattr(self, "model_dump") else self.dict()

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)


class DocumentItem(BaseModel):
    """Unified document representation for LangGraph ingestion node.
    
    Adheres strictly to PROJECT.md interface contract:
      - source_path: str
      - file_type: str ('email' or 'text')
      - title: str
      - content: str
      - summary: Optional[str]
      - metadata: Dict[str, Any]
    """
    source_path: str = Field(
        default="", 
        description="Relative POSIX path from corpus_dir (e.g. 'conversations/conv_pines014_material_volume.eml')"
    )
    file_type: str = Field(
        default="text", 
        description="'email' for .eml threads, 'text' for .txt documents"
    )
    title: str = Field(
        default="", 
        description="Document title or email thread subject"
    )
    content: str = Field(
        default="", 
        description="Clean text content optimized for LLM prompts"
    )
    summary: Optional[str] = Field(
        default=None, 
        description="Consensus summary text if available"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Provenance, participants, dates, line counts, and chatter tags"
    )

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump() if hasattr(self, "model_dump") else self.dict()

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)



# ==============================================================================
# Non-Functional Chatter Detection Taxonomy
# ==============================================================================

CHATTER_PATTERNS = [
    # Coffee complaints and incidents
    r'\b(?:office sludge|coffee sludge|decent cup of coffee|need coffee|coffee maker broke|spilled coffee)\b',
    # Pets and domestic animals
    r'\b(?:goldfish|bubbles ii|golden doodle|biscuit|mittens|puppy|squirrels stealing|mouse problem|exterminator|penguins)\b',
    r'\bcat\s+(?:has started|keeps knocking|sleeping on my keyboard|sit on their keyboard|tail)\b',
    r'\bdog\s+(?:ate my library card|barks at everything)\b',
    # Food, cooking, restaurants
    r'\b(?:pies [\'\"]?n[\'\"]? thighs|anniversary dinner|heirloom tomatoes?|tomato sandwich|pesto recipe|chicken tikka|costco.*sunday|farmer[\'s]* market|chef[\'s]* table)\b',
    # Pop culture, TV, movies, books, sports
    r'\b(?:marvel movie|endgame|the west wing|netflix|crawdads sing|evelyn hugo|rise and fall of the dinosaurs|t-rex|braves game|baseball game)\b',
    # Family, recitals, personal chores, humor
    r'\b(?:soccer practice.*rain|piano recital|ballet class|recital.*chopin|running shoes|haircut|eye cream|expresso)\b',
    # Personal postscript markers
    r'^\s*(?:\(?(?:P\.S\.|BTW|By the way)\b[^\n]*\)?)\s*$'
]

CHATTER_REGEX = re.compile('|'.join(CHATTER_PATTERNS), re.IGNORECASE)


def detect_noise_snippets(text: str) -> List[str]:
    """Detects and extracts non-functional chatter lines from text."""
    hits: List[str] = []
    for line in text.splitlines():
        if CHATTER_REGEX.search(line):
            clean_l = line.strip()
            if clean_l and clean_l not in hits:
                hits.append(clean_l)
    return hits


# ==============================================================================
# RFC 822 Date Normalization with Missing Year Resilience
# ==============================================================================

def normalize_rfc822_date(raw_date: str, default_year: int = 2009) -> Optional[str]:
    """Parses RFC 822/2822 date header into ISO 8601 string.
    
    Robustly handles malformed dates missing the 4-digit year (e.g. 'Fri, 10 Apr 11:03:45 -0500').
    """
    if not raw_date or not raw_date.strip():
        return None
    date_str = raw_date.strip()
    
    # 1. Standard RFC 2822 parse
    try:
        dt = parsedate_to_datetime(date_str)
        return dt.isoformat()
    except Exception:
        pass

    # 2. Resilient fix: inject default year when month is followed directly by time
    fixed = re.sub(r'([A-Za-z]{3})\s+(\d{1,2}:\d{2}(?::\d{2})?)', rf'\1 {default_year} \2', date_str)
    try:
        dt = parsedate_to_datetime(fixed)
        return dt.isoformat()
    except Exception:
        pass

    return None


# ==============================================================================
# Parsing Logic for Email Threads (.eml)
# ==============================================================================

def _parse_eml_thread(file_path: Path, base_path: Path) -> DocumentItem:
    """Parses a multi-message RFC 822 email thread file."""
    rel_path = file_path.relative_to(base_path).as_posix()
    raw_content = file_path.read_text(encoding="utf-8", errors="replace")
    
    # Split thread on separator line '==='
    chunks = re.split(r"(?m)^===\s*$", raw_content)
    
    parsed_messages: List[ParsedMessage] = []
    participants: set[str] = set()
    summary_text: Optional[str] = None
    primary_subject: str = ""
    primary_sender: str = ""
    primary_raw_date: str = ""
    all_chatter: List[str] = []
    
    for idx, chunk in enumerate(chunks):
        chunk_str = chunk.strip()
        if not chunk_str:
            continue
            
        msg = email.message_from_string(chunk_str)
        sender = msg.get("From", "").strip()
        recipient = msg.get("To", "").strip()
        cc = msg.get("Cc", "").strip() or None
        subject = msg.get("Subject", "").strip()
        raw_date = msg.get("Date", "").strip()
        
        # Decode body
        if msg.is_multipart():
            body_parts = []
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    payload = part.get_payload(decode=True)
                    if payload is not None and isinstance(payload, bytes):
                        charset = part.get_content_charset() or "utf-8"
                        try:
                            body_parts.append(payload.decode(charset, errors="replace"))
                        except (LookupError, UnicodeDecodeError):
                            body_parts.append(payload.decode("utf-8", errors="replace"))
            body = "\n".join(body_parts).strip()
        else:
            payload = msg.get_payload(decode=True)
            if payload is not None and isinstance(payload, bytes):
                charset = msg.get_content_charset() or "utf-8"
                try:
                    body = payload.decode(charset, errors="replace").strip()
                except (LookupError, UnicodeDecodeError):
                    body = payload.decode("utf-8", errors="replace").strip()
            else:
                body = (msg.get_payload() or "").strip()
                
        # Normalize date
        iso_date = normalize_rfc822_date(raw_date, default_year=2009)
        
        if sender:
            participants.add(sender)
        if not primary_sender and sender:
            primary_sender = sender
        if not primary_subject and subject:
            primary_subject = subject
        if not primary_raw_date and raw_date:
            primary_raw_date = raw_date
            
        # Detect Katherine Gregory consensus summary
        is_summary = "SUMMARY:" in subject.upper() or (
            "katherine.gregory" in sender.lower() and "summariz" in body[:120].lower()
        )
        if is_summary and not summary_text:
            summary_text = body
            
        # Chatter detection
        chatter = detect_noise_snippets(body)
        if chatter:
            all_chatter.extend(chatter)
            
        parsed_messages.append(
            ParsedMessage(
                part_index=idx + 1,
                sender=sender,
                recipient=recipient,
                cc=cc,
                subject=subject,
                raw_date=raw_date,
                parsed_date=iso_date,
                is_summary=is_summary,
                body=body,
                noise_snippets=chatter
            )
        )
        
    # Build clean structured content for downstream LLM prompts
    title = primary_subject or file_path.stem.replace("_", " ").title()
    content_lines = [
        f"# EMAIL THREAD: {title}",
        f"Source File: {rel_path}",
        f"Participants: {', '.join(sorted(participants))}",
        f"Initial Date: {primary_raw_date}\n"
    ]
    
    if summary_text:
        content_lines.append("=== CONSENSUS SUMMARY (Katherine Gregory) ===")
        content_lines.append(summary_text)
        content_lines.append("\n=== DETAILED DISCUSSION THREAD ===")
        
    for m in parsed_messages:
        content_lines.append(f"--- [Message {m.part_index}] From: {m.sender} | Date: {m.raw_date} ---")
        content_lines.append(f"Subject: {m.subject}")
        content_lines.append(m.body)
        content_lines.append("")
        
    content = "\n".join(content_lines).strip()
    
    metadata: Dict[str, Any] = {
        "sender": primary_sender,
        "date": primary_raw_date,
        "parsed_date": normalize_rfc822_date(primary_raw_date, default_year=2009),
        "participants": sorted(list(participants)),
        "doc_subtype": "email_thread",
        "message_count": len(parsed_messages),
        "messages": [m.to_dict() for m in parsed_messages],
        "has_consensus_summary": summary_text is not None,
        "chatter_detected": sorted(list(set(all_chatter))),
        "raw_byte_size": file_path.stat().st_size,
        "line_count": len(raw_content.splitlines())
    }
    
    return DocumentItem(
        source_path=rel_path,
        file_type="email",
        title=title,
        content=content,
        summary=summary_text,
        metadata=metadata
    )


# ==============================================================================
# Parsing Logic for Plain Text Files (.txt)
# ==============================================================================

def _parse_text_document(file_path: Path, base_path: Path) -> DocumentItem:
    """Parses a structured plain text document (.txt)."""
    rel_path = file_path.relative_to(base_path).as_posix()
    raw_content = file_path.read_text(encoding="utf-8", errors="replace")
    lines = raw_content.splitlines()
    
    # Extract title from header banner
    title = file_path.stem.replace("_", " ").title()
    for l in lines[:10]:
        clean_l = l.strip(" =#-*\t")
        if clean_l and len(clean_l) > 4 and not clean_l.startswith("==="):
            title = clean_l
            break
            
    # Subtype detection
    stem = file_path.stem.lower()
    if "srs" in stem:
        subtype = "srs_draft"
        sender = "Lori Ayre, Lucien Kress (Galecia Group)"
    elif "reference" in stem:
        subtype = "reference_doc"
        sender = "PINES IT Department"
    elif "interview" in stem:
        subtype = "interview"
        sender = "Interviewer / Interviewee"
    elif "minutes" in stem or "subcommittee" in stem:
        subtype = "meeting_minutes"
        sender = "Katherine Gregory (Chair) / Working Group"
    elif "survey" in stem:
        subtype = "survey_results"
        sender = "Katherine Gregory (Compiler)"
    else:
        subtype = "text_document"
        sender = "Author"
        
    # Extract participants from header if available
    participants: List[str] = []
    for line in lines[:30]:
        if any(hdr in line for hdr in ("ATTENDEES:", "Interviewer:", "Interviewee:", "Prepared by:")):
            participants.append(line.strip())
            
    # Check for chatter in text files (usually none, but robust to check)
    chatter = detect_noise_snippets(raw_content)
    
    metadata: Dict[str, Any] = {
        "sender": sender,
        "date": "2009",
        "parsed_date": "2009-01-01T00:00:00",
        "participants": participants,
        "doc_subtype": subtype,
        "message_count": 1,
        "messages": [],
        "has_consensus_summary": False,
        "chatter_detected": chatter,
        "raw_byte_size": file_path.stat().st_size,
        "line_count": len(lines)
    }
    
    return DocumentItem(
        source_path=rel_path,
        file_type="text",
        title=title,
        content=raw_content.strip(),
        summary=None,
        metadata=metadata
    )


# ==============================================================================
# Public API Function
# ==============================================================================

def ingest_corpus(corpus_dir: Union[str, Path]) -> List[DocumentItem]:
    """Recursively parses all .txt and .eml files in corpus_dir.
    
    Args:
        corpus_dir: String or Path representing corpus directory path.
        
    Returns:
        Deterministic list of DocumentItem objects sorted by relative source_path.
        
    Raises:
        FileNotFoundError: If corpus_dir does not exist.
        NotADirectoryError: If corpus_dir is not a directory.
    """
    base_path = Path(corpus_dir).resolve()
    if not base_path.exists():
        raise FileNotFoundError(f"Corpus directory does not exist: {corpus_dir}")
    if not base_path.is_dir():
        raise NotADirectoryError(f"Corpus path is not a directory: {corpus_dir}")
        
    discovered_files: List[Path] = []
    for path in base_path.rglob("*"):
        if path.is_file() and path.suffix.lower() in (".txt", ".eml"):
            # Exclude files in hidden directories (e.g. .git, .venv) or hidden files
            rel_parts = path.relative_to(base_path).parts
            if not any(part.startswith(".") for part in rel_parts):
                discovered_files.append(path)
                
    # Deterministic alphabetical sort by relative POSIX path
    discovered_files.sort(key=lambda p: p.relative_to(base_path).as_posix())
    
    documents: List[DocumentItem] = []
    for file_path in discovered_files:
        if file_path.suffix.lower() == ".eml":
            doc = _parse_eml_thread(file_path, base_path)
        else:
            doc = _parse_text_document(file_path, base_path)
        documents.append(doc)
        
    return documents


# ==============================================================================
# CLI Entry Point
# ==============================================================================

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Deterministic Ingestion Engine for Requirements Corpus"
    )
    parser.add_argument(
        "--corpus-dir", 
        type=str, 
        default="data/corpus",
        help="Path to corpus directory"
    )
    parser.add_argument(
        "--dump-json", 
        type=str, 
        default=None,
        help="Optional path to output parsed documents as JSON"
    )
    parser.add_argument(
        "--quiet", 
        action="store_true",
        help="Suppress console progress output"
    )
    
    args = parser.parse_args()
    
    try:
        items = ingest_corpus(args.corpus_dir)
    except Exception as e:
        print(f"Error ingesting corpus: {e}")
        raise SystemExit(1)
        
    if not args.quiet:
        print(f"Successfully ingested {len(items)} documents from '{args.corpus_dir}':")
        emails = [i for i in items if i.file_type == "email"]
        texts = [i for i in items if i.file_type == "text"]
        summaries = [i for i in items if i.summary is not None]
        chatter = [i for i in items if len(i.metadata.get("chatter_detected", [])) > 0]
        
        print(f"  - Emails: {len(emails)} threads")
        print(f"  - Text Documents: {len(texts)}")
        print(f"  - With Consensus Summary: {len(summaries)}")
        print(f"  - With Personal Chatter: {len(chatter)}")
        print("-" * 60)
        for idx, item in enumerate(items):
            summ_tag = "[SUMMARY]" if item.summary else "         "
            print(f"  {idx+1:2d}. {summ_tag} {item.source_path:<48} ({item.file_type})")
            
    if args.dump_json:
        out_path = Path(args.dump_json)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        dump_data = [item.to_dict() for item in items]
        out_path.write_text(json.dumps(dump_data, indent=2), encoding="utf-8")
        if not args.quiet:
            print(f"\nDumped {len(dump_data)} document items to {out_path}")


if __name__ == "__main__":
    main()
