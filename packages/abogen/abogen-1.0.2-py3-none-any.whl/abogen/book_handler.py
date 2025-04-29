import re
import html
import ebooklib
import base64
import fitz  # PyMuPDF for PDF support
from ebooklib import epub
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import (
    QDialog,
    QTreeWidget,
    QTreeWidgetItem,
    QDialogButtonBox,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QTreeWidgetItemIterator,
    QSplitter,
    QWidget,
    QPushButton,
    QCheckBox,
    QMenu,
    QLabel,
)
from PyQt5.QtCore import Qt
from utils import clean_text, calculate_text_length
import os


class HandlerDialog(QDialog):
    # Class variables to remember checkbox states between dialog instances
    _save_chapters_separately = False
    _merge_chapters_at_end = True

    def __init__(self, book_path, file_type=None, checked_chapters=None, parent=None):
        super().__init__(parent)

        # Determine file type if not explicitly provided
        self.file_type = file_type or (
            "pdf" if book_path.lower().endswith(".pdf") else "epub"
        )
        self.book_path = book_path

        # Extract book name from file path
        book_name = os.path.splitext(os.path.basename(book_path))[0]

        # Set window title based on file type and book name
        self.setWindowTitle(
            f'Select {"Chapters" if self.file_type == "epub" else "Pages"} - {book_name}'
        )
        self.resize(1200, 900)
        self._block_signals = False  # Flag to prevent recursive signals
        # Configure window: remove help button and allow resizing
        self.setWindowFlags(
            Qt.Window | Qt.WindowCloseButtonHint | Qt.WindowMaximizeButtonHint
        )
        self.setWindowModality(Qt.NonModal)
        # Initialize save chapters flags from class variables
        self.save_chapters_separately = HandlerDialog._save_chapters_separately
        self.merge_chapters_at_end = HandlerDialog._merge_chapters_at_end

        # Load the book based on file type
        self.book = epub.read_epub(book_path) if self.file_type == "epub" else None
        self.pdf_doc = fitz.open(book_path) if self.file_type == "pdf" else None

        # Extract book metadata
        self.book_metadata = self._extract_book_metadata()

        # Initialize UI elements that are used in other methods
        self.save_chapters_checkbox = None
        self.merge_chapters_checkbox = None

        # Build treeview
        self.treeWidget = QTreeWidget(self)
        self.treeWidget.setHeaderHidden(True)
        self.treeWidget.setSelectionMode(QTreeWidget.SingleSelection)
        self.treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeWidget.customContextMenuRequested.connect(self.on_tree_context_menu)

        # Initialize checked_chapters set
        self.checked_chapters = set(checked_chapters) if checked_chapters else set()

        # For storing content and lengths
        self.content_texts = {}
        self.content_lengths = {}

        # Pre-process content based on file type
        self._preprocess_content()

        # Add "Information" item at the beginning of the tree
        info_item = QTreeWidgetItem(self.treeWidget, ["Information"])
        info_item.setData(0, Qt.UserRole, "info:bookinfo")
        info_item.setFlags(info_item.flags() & ~Qt.ItemIsUserCheckable)
        font = info_item.font(0)
        font.setBold(True)
        info_item.setFont(0, font)

        # Build tree based on file type
        self._build_tree()

        # Hide expand/collapse decoration if there are no parent items
        has_parents = False
        for i in range(self.treeWidget.topLevelItemCount()):
            if self.treeWidget.topLevelItem(i).childCount() > 0:
                has_parents = True
                break
        self.treeWidget.setRootIsDecorated(has_parents)

        # Setup UI (creates save_chapters_checkbox and other UI elements)
        self._setup_ui()

        # Run auto-check after UI is setup
        if not self._are_provided_checks_relevant():
            self._run_auto_check()

        # Connect signals
        self.treeWidget.currentItemChanged.connect(self.update_preview)
        self.treeWidget.itemChanged.connect(self.handle_item_check)
        self.treeWidget.itemChanged.connect(lambda _: self._update_checkbox_states())
        self.treeWidget.itemDoubleClicked.connect(self.handle_item_double_click)

        # Select first item and expand all
        self.treeWidget.expandAll()
        if self.treeWidget.topLevelItemCount() > 0:
            self.treeWidget.setCurrentItem(self.treeWidget.topLevelItem(0))

        # Update checkbox states
        self._update_checkbox_states()

    def _preprocess_content(self):
        """Pre-process content from the document"""
        if self.file_type == "epub":
            # Always process EPUB content using the anchor-based approach
            self._process_epub_content()
        else:
            self._preprocess_pdf_content()

    def _process_epub_content(self, split_anchors=True):
        """
        Process EPUB content by globally ordering TOC entries and slicing content between them.
        Ensures all content between defined TOC start points is captured.
        """
        # split_anchors parameter kept for compatibility but always treated as True
        book = self.book

        # 1. Cache all document HTML and determine spine order
        self.doc_content = {}
        # Correctly get hrefs from spine items
        spine_docs = []
        for spine_item_tuple in book.spine:
            item_id = spine_item_tuple[0]
            item = book.get_item_with_id(item_id)
            if item:
                spine_docs.append(item.get_name())  # Use get_name() for href
            else:
                print(f"Warning: Spine item with id '{item_id}' not found in book items.")

        doc_order = {href: i for i, href in enumerate(spine_docs)}

        for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            href = item.get_name()
            if href in doc_order:  # Only process docs in spine
                try:
                    html_content = item.get_content().decode('utf-8', errors='ignore')
                    self.doc_content[href] = html_content
                except Exception:
                    self.doc_content[href] = ""  # Handle decoding errors

        # 2. Get all TOC entries with hrefs and determine their positions
        toc_entries_with_pos = []

        def find_position(doc_href, fragment_id):
            if doc_href not in self.doc_content:
                return -1
            html_content = self.doc_content[doc_href]
            if not fragment_id:  # No fragment, position is 0
                return 0

            # Find position of fragment identifier (id= or name=)
            id_match_str = f'id="{fragment_id}"'
            name_match_str = f'name="{fragment_id}"'

            id_pos = html_content.find(id_match_str)
            name_pos = html_content.find(name_match_str)

            pos = -1
            if id_pos != -1 and name_pos != -1:
                pos = min(id_pos, name_pos)
            elif id_pos != -1:
                pos = id_pos
            elif name_pos != -1:
                pos = name_pos
            else:
                return -1  # Anchor not found by simple string search

            # Backtrack to the start of the tag '<'
            tag_start_pos = html_content.rfind('<', 0, pos)
            return tag_start_pos if tag_start_pos != -1 else 0  # Default to 0 if '<' not found

        def collect_toc_entries(entries):
            collected = []
            for entry in entries:
                href, title = None, "Unknown"
                children = []
                entry_obj = None  # Store the original entry object

                if isinstance(entry, ebooklib.epub.Link):
                    href, title = entry.href, entry.title or entry.href
                    entry_obj = entry
                elif isinstance(entry, tuple) and len(entry) >= 1:
                    section_or_link = entry[0]
                    entry_obj = section_or_link
                    if isinstance(section_or_link, ebooklib.epub.Section):
                        title = section_or_link.title
                        href = getattr(section_or_link, "href", None)
                    elif isinstance(section_or_link, ebooklib.epub.Link):
                        href, title = section_or_link.href, section_or_link.title or section_or_link.href

                    if len(entry) > 1 and isinstance(entry[1], list):
                        children = entry[1]

                if href:
                    base_href, fragment = href.split('#', 1) if '#' in href else (href, None)
                    if base_href in doc_order:  # Only consider entries pointing to spine documents
                        position = find_position(base_href, fragment)
                        if position != -1:  # Only add if position is valid
                            collected.append({
                                "href": href,  # Use the original href from TOC as the key
                                "title": title,
                                "doc_href": base_href,
                                "position": position,
                                "doc_order": doc_order[base_href]
                            })

                if children:
                    collected.extend(collect_toc_entries(children))
            return collected

        all_toc_entries = collect_toc_entries(self.book.toc)

        # Handle case where book has no TOC or empty TOC
        if not all_toc_entries:
            # Create a synthetic TOC entry for the first spine document
            if spine_docs:
                # Process all content as a single chapter
                all_content_html = ""
                for doc_href in spine_docs:
                    all_content_html += self.doc_content.get(doc_href, "")

                if all_content_html:
                    soup = BeautifulSoup(all_content_html, 'html.parser')
                    text = clean_text(soup.get_text()).strip()
                    
                    # Use the first spine document as the identifier
                    first_doc = spine_docs[0]
                    self.content_texts[first_doc] = text
                    self.content_lengths[first_doc] = len(text)
                    
                    # Create a synthetic TOC entry for tree building
                    self.book.toc = [(epub.Link(first_doc, "Main Content", first_doc),)]
            return

        # 3. Sort TOC entries globally
        all_toc_entries.sort(key=lambda x: (x["doc_order"], x["position"]))

        # 4. Slice content between sorted entries
        self.content_texts = {}
        self.content_lengths = {}
        num_entries = len(all_toc_entries)

        for i in range(num_entries):
            current_entry = all_toc_entries[i]
            current_href = current_entry["href"]
            current_doc = current_entry["doc_href"]
            current_pos = current_entry["position"]
            current_doc_html = self.doc_content.get(current_doc, "")

            start_slice_pos = current_pos
            slice_html = ""

            # Find the start of the next TOC entry
            next_entry = all_toc_entries[i + 1] if (i + 1) < num_entries else None

            if next_entry:
                next_doc = next_entry["doc_href"]
                next_pos = next_entry["position"]

                if current_doc == next_doc:
                    # Next entry is in the same document
                    slice_html = current_doc_html[start_slice_pos:next_pos]
                else:
                    # Next entry is in a different document
                    # Take content from current position to end of current document
                    slice_html = current_doc_html[start_slice_pos:]
                    # Include content from intermediate documents in the spine
                    current_doc_index = current_entry["doc_order"]
                    next_doc_index = next_entry["doc_order"]
                    for doc_idx in range(current_doc_index + 1, next_doc_index):
                        intermediate_doc_href = spine_docs[doc_idx]
                        slice_html += self.doc_content.get(intermediate_doc_href, "")
                    # Add content from the beginning of the next document up to the next entry's position
                    next_doc_html = self.doc_content.get(next_doc, "")
                    slice_html += next_doc_html[:next_pos]
            else:
                # This is the last TOC entry
                # Take content from current position to end of current document
                slice_html = current_doc_html[start_slice_pos:]
                # Include content from all remaining documents in the spine
                current_doc_index = current_entry["doc_order"]
                for doc_idx in range(current_doc_index + 1, len(spine_docs)):
                    intermediate_doc_href = spine_docs[doc_idx]
                    slice_html += self.doc_content.get(intermediate_doc_href, "")

            # 5. Extract text and store
            slice_soup = BeautifulSoup(slice_html, 'html.parser')
            
            # Remove sup and sub tags from the HTML before extracting text
            for tag in slice_soup.find_all(['sup', 'sub']):
                tag.decompose()
                
            text = clean_text(slice_soup.get_text()).strip()
            self.content_texts[current_href] = text  # Store using the original TOC href
            self.content_lengths[current_href] = len(text)

        # 6. Handle content BEFORE the first TOC entry
        if all_toc_entries:
            first_entry = all_toc_entries[0]
            first_doc_href = first_entry["doc_href"]
            first_pos = first_entry["position"]
            first_doc_order = first_entry["doc_order"]
            prefix_html = ""
            # Include content from documents before the first entry's document
            for doc_idx in range(first_doc_order):
                intermediate_doc_href = spine_docs[doc_idx]
                prefix_html += self.doc_content.get(intermediate_doc_href, "")
            # Include content from the start of the first entry's document up to its position
            first_doc_html = self.doc_content.get(first_doc_href, "")
            prefix_html += first_doc_html[:first_pos]

            if prefix_html.strip():
                prefix_soup = BeautifulSoup(prefix_html, 'html.parser')
                # Remove sup and sub tags
                for tag in prefix_soup.find_all(['sup', 'sub']):
                    tag.decompose()
                prefix_text = clean_text(prefix_soup.get_text()).strip()
                
                if prefix_text:
                    # Create a new chapter for content before the first TOC entry
                    # Use a synthetic href to avoid collision with real TOC entries
                    prefix_chapter_href = "prefix_content_chapter"
                    self.content_texts[prefix_chapter_href] = prefix_text
                    self.content_lengths[prefix_chapter_href] = len(prefix_text)
                    
                    # Add a new entry to the TOC for the prefix content
                    prefix_link = epub.Link(prefix_chapter_href, "Introduction", prefix_chapter_href)
                    # Insert at beginning of TOC
                    if isinstance(self.book.toc, list):
                        self.book.toc.insert(0, (prefix_link,))
                    else:
                        self.book.toc = [(prefix_link,)] + (self.book.toc or [])

    def _preprocess_pdf_content(self):
        """Pre-process all page contents from PDF document"""
        for page_num in range(len(self.pdf_doc)):
            text = clean_text(self.pdf_doc[page_num].get_text())
            # Remove bracketed numbers (citations, footnotes)
            text = re.sub(r"\[\s*\d+\s*\]", "", text)

            # Remove standalone page numbers (numbers alone on a line)
            text = re.sub(r"^\s*\d+\s*$", "", text, flags=re.MULTILINE)

            # Remove page numbers at the end of paragraphs
            # This pattern looks for digits surrounded by whitespace at the end of paragraphs
            text = re.sub(r"\s+\d+\s*$", "", text, flags=re.MULTILINE)

            # Also remove page numbers followed by a hyphen or dash at paragraph end
            # (common in headers/footers like "- 42 -")
            text = re.sub(r"\s+[-–—]\s*\d+\s*[-–—]?\s*$", "", text, flags=re.MULTILINE)

            page_id = f"page_{page_num+1}"
            self.content_texts[page_id] = text
            self.content_lengths[page_id] = calculate_text_length(text)

    def _build_tree(self):
        """Build tree based on file type"""
        if self.file_type == "epub":
            self._build_epub_tree()
        else:
            self._build_pdf_tree()

    def _build_epub_tree(self):
        """Build the tree for EPUB files from TOC"""
        self.treeWidget.clear()
        info_item = QTreeWidgetItem(self.treeWidget, ["Information"])
        info_item.setData(0, Qt.UserRole, "info:bookinfo")
        info_item.setFlags(info_item.flags() & ~Qt.ItemIsUserCheckable)
        font = info_item.font(0)
        font.setBold(True)
        info_item.setFont(0, font)

        # Regular tree building
        def build_tree(toc_entries, parent_item):
            for entry in toc_entries:
                href, title, children = None, "Unknown", []
                if isinstance(entry, ebooklib.epub.Link):
                    href, title = entry.href, entry.title or entry.href
                elif isinstance(entry, tuple) and len(entry) >= 1:
                    section_or_link = entry[0]
                    if isinstance(section_or_link, ebooklib.epub.Section):
                        title = section_or_link.title
                        href = getattr(section_or_link, "href", None)
                    elif isinstance(section_or_link, ebooklib.epub.Link):
                        href, title = (
                            section_or_link.href,
                            section_or_link.title or section_or_link.href,
                        )
                    if len(entry) > 1 and isinstance(entry[1], list):
                        children = entry[1]
                else:
                    continue

                # Create tree item
                item = QTreeWidgetItem(parent_item, [title])
                item.setData(0, Qt.UserRole, href)

                # Make item checkable if it has content
                has_content = href and href in self.content_texts and self.content_texts[href].strip()
                if has_content or children:
                    item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                    is_checked = href and href in self.checked_chapters
                    item.setCheckState(0, Qt.Checked if is_checked else Qt.Unchecked)
                else:
                    item.setFlags(item.flags() & ~Qt.ItemIsUserCheckable)

                # Process children
                if children:
                    build_tree(children, item)

        build_tree(self.book.toc, self.treeWidget)

    def _build_pdf_tree(self):
        """Build the tree for PDF files combining outline/bookmarks with pages"""
        # Get outline and store if this PDF has bookmarks
        outline = self.pdf_doc.get_toc()
        self.has_pdf_bookmarks = bool(outline)

        if not outline:
            # No bookmarks/outline available, create a simple page list
            self._build_pdf_pages_tree()
            return

        # Process the outline to determine page ranges
        bookmark_pages = []
        page_to_bookmark = {}
        next_page_boundaries = {}
        # Track added pages to prevent duplicates
        added_pages = set()

        # Extract page numbers from outline recursively
        def extract_page_numbers(entries):
            for entry in entries:
                if (
                    len(entry) >= 3
                ):  # Valid outline entry has at least level, title, page
                    _, title, page = entry[:3]
                    # Convert page reference to actual page number (0-based)
                    page_num = (
                        page - 1
                        if isinstance(page, int)
                        else self.pdf_doc.resolve_link(page)[0]
                    )
                    bookmark_pages.append((page_num, title))

                    # Process children recursively
                    if len(entry) > 3 and isinstance(entry[3], list):
                        extract_page_numbers(entry[3])

        extract_page_numbers(outline)
        bookmark_pages.sort()

        # Determine page ranges for each bookmark
        for i, (page_num, title) in enumerate(bookmark_pages):
            if i < len(bookmark_pages) - 1:
                next_page_boundaries[page_num] = bookmark_pages[i + 1][0]
            page_to_bookmark[page_num] = title

        # Helper function to build the tree structure recursively
        def build_outline_tree(entries, parent_item):
            for entry in entries:
                if (
                    len(entry) >= 3
                ):  # Valid outline entry has at least level, title, page
                    entry_level, title, page = entry[:3]
                    # Get actual page number (0-based)
                    page_num = (
                        page - 1
                        if isinstance(page, int)
                        else self.pdf_doc.resolve_link(page)[0]
                    )
                    page_id = f"page_{page_num+1}"

                    # Create bookmark item
                    bookmark_item = QTreeWidgetItem(parent_item, [title])
                    bookmark_item.setData(0, Qt.UserRole, page_id)
                    bookmark_item.setFlags(
                        bookmark_item.flags() | Qt.ItemIsUserCheckable
                    )
                    bookmark_item.setCheckState(
                        0,
                        (
                            Qt.Checked
                            if page_id in self.checked_chapters
                            else Qt.Unchecked
                        ),
                    )

                    # Mark this page as added
                    added_pages.add(page_num)

                    # Add child pages that belong to this bookmark
                    next_page = next_page_boundaries.get(page_num, len(self.pdf_doc))
                    for sub_page_num in range(
                        page_num + 1, next_page
                    ):  # Skip the bookmark page itself
                        # Skip if this page is a bookmark itself or already added as a child elsewhere
                        if (
                            sub_page_num in page_to_bookmark
                            or sub_page_num in added_pages
                        ):
                            continue

                        page_id = f"page_{sub_page_num+1}"
                        page_title = f"Page {sub_page_num+1}"

                        # Try to get a better title from the first line of content
                        page_text = self.content_texts.get(page_id, "").strip()
                        if page_text:
                            first_line = page_text.split("\n", 1)[0].strip()
                            if first_line and len(first_line) < 100:
                                page_title += f" - {first_line}"

                        page_item = QTreeWidgetItem(bookmark_item, [page_title])
                        page_item.setData(0, Qt.UserRole, page_id)
                        page_item.setFlags(page_item.flags() | Qt.ItemIsUserCheckable)
                        page_item.setCheckState(
                            0,
                            (
                                Qt.Checked
                                if page_id in self.checked_chapters
                                else Qt.Unchecked
                            ),
                        )

                        # Mark this page as added
                        added_pages.add(sub_page_num)

                    # Process child bookmarks if any
                    if len(entry) > 3 and isinstance(entry[3], list):
                        build_outline_tree(entry[3], bookmark_item)

        # Start building the tree from the outline
        build_outline_tree(outline, self.treeWidget)

        # Add pages not covered by bookmarks
        covered_pages = set(
            added_pages
        )  # Use our tracked pages to find uncategorized ones

        # Add remaining pages as top-level items under "Other Pages"
        uncategorized_pages = [
            i for i in range(len(self.pdf_doc)) if i not in covered_pages
        ]
        if uncategorized_pages:
            self._add_other_pages(uncategorized_pages)

    def _build_pdf_pages_tree(self):
        """Build a simple page list for PDFs without bookmarks"""
        pages_item = QTreeWidgetItem(self.treeWidget, ["Pages"])
        pages_item.setFlags(pages_item.flags() & ~Qt.ItemIsUserCheckable)
        font = pages_item.font(0)
        font.setBold(True)
        pages_item.setFont(0, font)

        for page_num in range(len(self.pdf_doc)):
            page_id = f"page_{page_num+1}"
            page_title = f"Page {page_num+1}"

            # Try to get a better title from the first line of content
            page_text = self.content_texts.get(page_id, "").strip()
            if page_text:
                first_line = page_text.split("\n", 1)[0].strip()
                if first_line and len(first_line) < 100:
                    page_title += f" - {first_line}"

            page_item = QTreeWidgetItem(pages_item, [page_title])
            page_item.setData(0, Qt.UserRole, page_id)
            page_item.setFlags(page_item.flags() | Qt.ItemIsUserCheckable)
            page_item.setCheckState(
                0, Qt.Checked if page_id in self.checked_chapters else Qt.Unchecked
            )

    def _add_other_pages(self, uncategorized_pages):
        """Add uncategorized pages to the tree"""
        other_pages = QTreeWidgetItem(self.treeWidget, ["Other Pages"])
        other_pages.setFlags(other_pages.flags() & ~Qt.ItemIsUserCheckable)
        font = other_pages.font(0)
        font.setBold(True)
        other_pages.setFont(0, font)

        for page_num in uncategorized_pages:
            page_id = f"page_{page_num+1}"
            page_title = f"Page {page_num+1}"

            # Try to get better title from first line
            page_text = self.content_texts.get(page_id, "").strip()
            if page_text:
                first_line = page_text.split("\n", 1)[0].strip()
                if first_line and len(first_line) < 100:
                    page_title += f" - {first_line}"

            page_item = QTreeWidgetItem(other_pages, [page_title])
            page_item.setData(0, Qt.UserRole, page_id)
            page_item.setFlags(page_item.flags() | Qt.ItemIsUserCheckable)
            page_item.setCheckState(
                0, Qt.Checked if page_id in self.checked_chapters else Qt.Unchecked
            )

    def _are_provided_checks_relevant(self):
        """Check if provided checks are relevant to this book"""
        if not self.checked_chapters:
            return False

        # Collect all identifiers present in tree
        all_identifiers = set()
        iterator = QTreeWidgetItemIterator(self.treeWidget)
        while iterator.value():
            item = iterator.value()
            if item.flags() & Qt.ItemIsUserCheckable:
                identifier = item.data(0, Qt.UserRole)
                if identifier:
                    all_identifiers.add(identifier)
            iterator += 1

        # Check for any intersection with provided chapters
        return bool(self.checked_chapters.intersection(all_identifiers))

    def _setup_ui(self):
        """Set up the user interface"""
        # Add preview panel
        self.previewEdit = QTextEdit(self)
        self.previewEdit.setReadOnly(True)
        self.previewEdit.setMinimumWidth(300)
        self.previewEdit.setStyleSheet("QTextEdit { border: none; }")

        # Create informative text label below preview
        self.previewInfoLabel = QLabel("*Note: You can modify the content later using the \"Edit\" button in the input box or by accessing the temporary files directory through settings.", self)
        self.previewInfoLabel.setWordWrap(True)
        self.previewInfoLabel.setStyleSheet("QLabel { color: #666; font-style: italic; }")

        # Right panel layout (preview and info label)
        previewLayout = QVBoxLayout()
        previewLayout.setContentsMargins(0, 0, 0, 0)
        previewLayout.addWidget(self.previewEdit, 1)
        previewLayout.addWidget(self.previewInfoLabel, 0)
        
        rightWidget = QWidget()
        rightWidget.setLayout(previewLayout)

        # Dialog buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        # Selection buttons
        item_type = "chapters" if self.file_type == "epub" else "pages"

        # Auto-select button
        self.auto_select_btn = QPushButton(f"Auto-select {item_type}", self)
        self.auto_select_btn.clicked.connect(self.auto_select_chapters)
        self.auto_select_btn.setToolTip(f"Automatically select main {item_type}")

        # Selection buttons layout
        buttons_layout = QVBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(10)

        # Row 1: Auto-select
        auto_select_layout = QHBoxLayout()
        auto_select_layout.addWidget(self.auto_select_btn)
        buttons_layout.addLayout(auto_select_layout)

        # Row 2: Select/Deselect All
        select_layout = QHBoxLayout()
        self.select_all_btn = QPushButton("Select all", self)
        self.select_all_btn.clicked.connect(self.select_all_chapters)
        self.deselect_all_btn = QPushButton("Clear all", self)
        self.deselect_all_btn.clicked.connect(self.deselect_all_chapters)
        select_layout.addWidget(self.select_all_btn)
        select_layout.addWidget(self.deselect_all_btn)
        buttons_layout.addLayout(select_layout)

        # Row 3: Parent selection
        parent_layout = QHBoxLayout()
        self.select_parents_btn = QPushButton("Select parents", self)
        self.select_parents_btn.clicked.connect(self.select_parent_chapters)
        self.deselect_parents_btn = QPushButton("Unselect parents", self)
        self.deselect_parents_btn.clicked.connect(self.deselect_parent_chapters)
        parent_layout.addWidget(self.select_parents_btn)
        parent_layout.addWidget(self.deselect_parents_btn)
        buttons_layout.addLayout(parent_layout)

        # Row 4: Expand/Collapse
        expand_layout = QHBoxLayout()
        self.expand_all_btn = QPushButton("Expand All", self)
        self.expand_all_btn.clicked.connect(self.treeWidget.expandAll)
        self.collapse_all_btn = QPushButton("Collapse All", self)
        self.collapse_all_btn.clicked.connect(self.treeWidget.collapseAll)
        expand_layout.addWidget(self.expand_all_btn)
        expand_layout.addWidget(self.collapse_all_btn)
        buttons_layout.addLayout(expand_layout)

        # Left panel layout
        leftLayout = QVBoxLayout()
        leftLayout.setContentsMargins(0, 0, 5, 0)
        leftLayout.addLayout(buttons_layout)
        leftLayout.addWidget(self.treeWidget)

        # Save options checkboxes
        checkbox_text = (
            "Save each chapter separately"
            if self.file_type == "epub"
            else "Save each page separately"
        )
        self.save_chapters_checkbox = QCheckBox(checkbox_text, self)
        self.save_chapters_checkbox.setChecked(self.save_chapters_separately)
        self.save_chapters_checkbox.stateChanged.connect(self.on_save_chapters_changed)
        leftLayout.addWidget(self.save_chapters_checkbox)

        self.merge_chapters_checkbox = QCheckBox(
            "Create a merged version at the end", self
        )
        self.merge_chapters_checkbox.setChecked(self.merge_chapters_at_end)
        self.merge_chapters_checkbox.stateChanged.connect(
            self.on_merge_chapters_changed
        )
        leftLayout.addWidget(self.merge_chapters_checkbox)

        leftLayout.addWidget(buttons)

        # Create left panel widget
        leftWidget = QWidget()
        leftWidget.setLayout(leftLayout)

        # Create splitter for left panel and preview
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(leftWidget)
        self.splitter.addWidget(rightWidget)  # Now using rightWidget that includes preview and label
        self.splitter.setSizes([280, 420])

        # Set main layout
        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(self.splitter)
        self.setLayout(mainLayout)

    def _update_checkbox_states(self):
        """Update checkboxes enabled states based on document type and selection"""
        # Make sure checkboxes exist before trying to modify them
        if (
            not hasattr(self, "save_chapters_checkbox")
            or not self.save_chapters_checkbox
        ):
            return

        # For PDFs without bookmarks, always disable separate chapters option
        if (
            self.file_type == "pdf"
            and hasattr(self, "has_pdf_bookmarks")
            and not self.has_pdf_bookmarks
        ):
            self.save_chapters_checkbox.setEnabled(False)
            self.merge_chapters_checkbox.setEnabled(False)
            return

        # Count checked items differently based on file type
        checked_count = 0

        if self.file_type == "epub":
            # For EPUB: Count all checked items
            iterator = QTreeWidgetItemIterator(self.treeWidget)
            while iterator.value():
                item = iterator.value()
                if (
                    item.flags() & Qt.ItemIsUserCheckable
                    and item.checkState(0) == Qt.Checked
                ):
                    checked_count += 1
                    if checked_count >= 2:
                        break
                iterator += 1

        else:  # PDF
            # For PDF: Count distinct parent groups
            # We need content from at least 2 different parents to enable "save separately"
            parent_groups = set()

            iterator = QTreeWidgetItemIterator(self.treeWidget)
            while iterator.value():
                item = iterator.value()
                if (
                    item.flags() & Qt.ItemIsUserCheckable
                    and item.checkState(0) == Qt.Checked
                ):
                    # Get the parent (or the item itself if it's a top-level item)
                    parent = item.parent()
                    if parent and parent != self.treeWidget.invisibleRootItem():
                        # Use memory address as a unique identifier since QTreeWidgetItem is not hashable
                        parent_groups.add(id(parent))
                    else:
                        # Top-level items count as their own parent group
                        parent_groups.add(id(item))
                iterator += 1

            checked_count = len(parent_groups)

        # Enable save separately only if enough distinct groups are checked
        min_groups_required = 2
        self.save_chapters_checkbox.setEnabled(checked_count >= min_groups_required)

        # Enable merge only if save separately is enabled and checked
        self.merge_chapters_checkbox.setEnabled(
            self.save_chapters_checkbox.isEnabled()
            and self.save_chapters_checkbox.isChecked()
        )

    def select_all_chapters(self):
        """Select all chapters/pages"""
        self._block_signals = True
        iterator = QTreeWidgetItemIterator(self.treeWidget)
        while iterator.value():
            item = iterator.value()
            if item.flags() & Qt.ItemIsUserCheckable:
                item.setCheckState(0, Qt.Checked)
            iterator += 1
        self._block_signals = False
        self._update_checked_set_from_tree()

    def deselect_all_chapters(self):
        """Deselect all chapters/pages"""
        self._block_signals = True
        iterator = QTreeWidgetItemIterator(self.treeWidget)
        while iterator.value():
            item = iterator.value()
            if item.flags() & Qt.ItemIsUserCheckable:
                item.setCheckState(0, Qt.Unchecked)
            iterator += 1
        self._block_signals = False
        self._update_checked_set_from_tree()

    def select_parent_chapters(self):
        """Select only parent chapters/sections"""
        self._block_signals = True
        iterator = QTreeWidgetItemIterator(self.treeWidget)
        while iterator.value():
            item = iterator.value()
            if item.flags() & Qt.ItemIsUserCheckable and item.childCount() > 0:
                item.setCheckState(0, Qt.Checked)
            iterator += 1
        self._block_signals = False
        self._update_checked_set_from_tree()

    def deselect_parent_chapters(self):
        """Deselect only parent chapters/sections"""
        self._block_signals = True
        iterator = QTreeWidgetItemIterator(self.treeWidget)
        while iterator.value():
            item = iterator.value()
            if item.flags() & Qt.ItemIsUserCheckable and item.childCount() > 0:
                item.setCheckState(0, Qt.Unchecked)
            iterator += 1
        self._block_signals = False
        self._update_checked_set_from_tree()

    def auto_select_chapters(self):
        """Auto-select chapters/pages"""
        self._run_auto_check()

    def _run_auto_check(self):
        """Run automatic content selection based on file type"""
        self._block_signals = True

        if self.file_type == "epub":
            self._run_epub_auto_check()
        else:  # PDF
            self._run_pdf_auto_check()

        self._block_signals = False
        self._update_checked_set_from_tree()

    def _run_epub_auto_check(self):
        """Auto-check logic for EPUB files"""
        iterator = QTreeWidgetItemIterator(self.treeWidget)
        while iterator.value():
            item = iterator.value()
            if not (item.flags() & Qt.ItemIsUserCheckable):
                iterator += 1
                continue

            href = item.data(0, Qt.UserRole)
            lookup_href = href.split("#")[0] if href else None

            # Check based on length (> 1000 chars) and parent status
            if (
                lookup_href and self.content_lengths.get(lookup_href, 0) > 1000
            ) or item.childCount() > 0:
                item.setCheckState(0, Qt.Checked)
                # Check children of parents
                if item.childCount() > 0:
                    for i in range(item.childCount()):
                        child = item.child(i)
                        if child.flags() & Qt.ItemIsUserCheckable:
                            child.setCheckState(0, Qt.Checked)
            iterator += 1

    def _run_pdf_auto_check(self):
        """Auto-check logic for PDF files"""
        # If there are no bookmarks, just check all pages
        if hasattr(self, "has_pdf_bookmarks") and not self.has_pdf_bookmarks:
            iterator = QTreeWidgetItemIterator(self.treeWidget)
            while iterator.value():
                item = iterator.value()
                if item.flags() & Qt.ItemIsUserCheckable:
                    item.setCheckState(0, Qt.Checked)
                iterator += 1
            return

        # For PDFs with bookmarks, select all bookmark items and non-empty pages
        iterator = QTreeWidgetItemIterator(self.treeWidget)
        while iterator.value():
            item = iterator.value()
            if not (item.flags() & Qt.ItemIsUserCheckable):
                iterator += 1
                continue

            identifier = item.data(0, Qt.UserRole)

            # Always select bookmark items or non-empty pages
            if not identifier:
                iterator += 1
                continue

            if (
                not identifier.startswith("page_")
                or self.content_lengths.get(identifier, 0) > 0
            ):
                item.setCheckState(0, Qt.Checked)

            iterator += 1

    def _update_checked_set_from_tree(self):
        """Update the internal set of checked items"""
        self.checked_chapters.clear()
        iterator = QTreeWidgetItemIterator(self.treeWidget)
        while iterator.value():
            item = iterator.value()
            if item.checkState(0) == Qt.Checked:
                identifier = item.data(0, Qt.UserRole)
                if identifier:
                    self.checked_chapters.add(identifier)
            iterator += 1
        # Only update checkbox states if they exist
        if hasattr(self, "save_chapters_checkbox") and self.save_chapters_checkbox:
            self._update_checkbox_states()

    def handle_item_check(self, item):
        """Handle item check/uncheck by updating children"""
        if self._block_signals:
            return

        self._block_signals = True

        # Update children recursively
        if item.flags() & Qt.ItemIsUserCheckable:
            for i in range(item.childCount()):
                child = item.child(i)
                if child.flags() & Qt.ItemIsUserCheckable:
                    child.setCheckState(0, item.checkState(0))

        self._block_signals = False
        self._update_checked_set_from_tree()

    def handle_item_double_click(self, item, column=0):
        """Toggle check state when a non-parent item is double-clicked on the text, not the checkbox"""
        # Only toggle items that are checkable and don't have children
        if item.flags() & Qt.ItemIsUserCheckable and item.childCount() == 0:
            # Get the rectangle of the checkbox
            rect = self.treeWidget.visualItemRect(item)
            checkbox_width = 20  # Approximate width of the checkbox

            # Get current mouse position
            mouse_pos = self.treeWidget.mapFromGlobal(self.treeWidget.cursor().pos())

            # Only toggle if click position is not on the checkbox
            if mouse_pos.x() > rect.x() + checkbox_width:
                # Toggle the check state
                new_state = (
                    Qt.Unchecked if item.checkState(0) == Qt.Checked else Qt.Checked
                )
                item.setCheckState(0, new_state)

    def update_preview(self, current):
        """Update the preview panel with selected item content"""
        if not current:
            self.previewEdit.clear()
            return

        identifier = current.data(0, Qt.UserRole)

        # Special case for the Information item
        if identifier == "info:bookinfo":
            self._display_book_info()
            return

        # Get content based on file type
        text = None
        if self.file_type == "epub":
            # For EPUB, always use the exact href from the TOC
            text = self.content_texts.get(identifier)
        else:  # PDF
            text = self.content_texts.get(identifier)

        # Display content or placeholder text - never remove titles
        if text is None:
            title = current.text(0)
            # Add title to preview even if no content
            self.previewEdit.setPlainText(f"{title}\n\n(No content available for this item)")
        elif not text.strip():
            title = current.text(0)
            self.previewEdit.setPlainText(f"{title}\n\n(This item is empty)")
        else:
            self.previewEdit.setPlainText(text)

    def _display_book_info(self):
        """Display book metadata and cover image in the preview panel"""
        self.previewEdit.clear()
        html_content = "<html><body style='font-family: Arial, sans-serif;'>"

        # Add cover image if available
        if self.book_metadata["cover_image"]:
            try:
                image_data = base64.b64encode(self.book_metadata["cover_image"]).decode(
                    "utf-8"
                )

                # Determine image type
                image_type = "jpeg"
                if self.book_metadata["cover_image"].startswith(b"\x89PNG"):
                    image_type = "png"
                elif self.book_metadata["cover_image"].startswith(b"GIF"):
                    image_type = "gif"

                html_content += (
                    f"<div style='text-align: center; margin-bottom: 20px;'>"
                )
                html_content += (
                    f"<img src='data:image/{image_type};base64,{image_data}' "
                )
                html_content += f"width='300' style='object-fit: contain;' /></div>"
            except Exception as e:
                html_content += f"<p>Error displaying cover image: {str(e)}</p>"

        # Add title, authors, publisher
        if self.book_metadata["title"]:
            html_content += (
                f"<h2 style='text-align: center;'>{self.book_metadata['title']}</h2>"
            )

        if self.book_metadata["authors"]:
            authors_text = ", ".join(self.book_metadata["authors"])
            html_content += f"<p style='text-align: center; font-style: italic;'>By {authors_text}</p>"

        if self.book_metadata["publisher"]:
            html_content += f"<p style='text-align: center;'>Published by {self.book_metadata['publisher']}</p>"

        html_content += "<hr/>"

        # Add description
        if self.book_metadata["description"]:
            desc = re.sub(r"<[^>]+>", "", self.book_metadata["description"])
            html_content += f"<h3>Description:</h3><p>{desc}</p>"

        # Add file type and page count for PDFs
        if self.file_type == "pdf":
            page_count = len(self.pdf_doc) if self.pdf_doc else 0
            html_content += f"<p>File type: PDF<br>Page count: {page_count}</p>"

        html_content += "</body></html>"
        self.previewEdit.setHtml(html_content)

    def _extract_book_metadata(self):
        """Extract book metadata"""
        metadata = {
            "title": None,
            "authors": [],
            "description": None,
            "cover_image": None,
            "publisher": None,
        }

        if self.file_type == "epub":
            # Extract EPUB metadata
            title_items = self.book.get_metadata("DC", "title")
            if title_items:
                metadata["title"] = title_items[0][0]

            author_items = self.book.get_metadata("DC", "creator")
            if author_items:
                metadata["authors"] = [author[0] for author in author_items]

            desc_items = self.book.get_metadata("DC", "description")
            if desc_items:
                metadata["description"] = desc_items[0][0]

            publisher_items = self.book.get_metadata("DC", "publisher")
            if publisher_items:
                metadata["publisher"] = publisher_items[0][0]

            # Try to find cover image
            for item in self.book.get_items_of_type(ebooklib.ITEM_COVER):
                metadata["cover_image"] = item.get_content()
                break

            if not metadata["cover_image"]:
                for item in self.book.get_items_of_type(ebooklib.ITEM_IMAGE):
                    if "cover" in item.get_name().lower():
                        metadata["cover_image"] = item.get_content()
                        break
        else:  # PDF
            # Extract PDF metadata
            pdf_info = self.pdf_doc.metadata
            if pdf_info:
                metadata["title"] = pdf_info.get("title", None)

                author = pdf_info.get("author", None)
                if author:
                    metadata["authors"] = [author]

                metadata["description"] = pdf_info.get("subject", None)

                keywords = pdf_info.get("keywords", None)
                if keywords:
                    if metadata["description"]:
                        metadata["description"] += f"\n\nKeywords: {keywords}"
                    else:
                        metadata["description"] = f"Keywords: {keywords}"

                metadata["publisher"] = pdf_info.get("creator", None)

            # Try to get cover image from first page
            if len(self.pdf_doc) > 0:
                try:
                    pix = self.pdf_doc[0].get_pixmap(matrix=fitz.Matrix(2, 2))
                    metadata["cover_image"] = pix.tobytes("png")
                except Exception:
                    pass

        return metadata

    def get_selected_text(self):
        """Get selected text and checked identifiers based on file type"""
        if self.file_type == "epub":
            return self._get_epub_selected_text()
        else:  # PDF
            return self._get_pdf_selected_text()

    def _get_epub_selected_text(self):
        """Get selected text from EPUB content"""
        all_checked_hrefs = set()
        chapter_titles = []

        # Collect all checked hrefs in tree order to preserve chapter sequence
        ordered_checked_items = []
        iterator = QTreeWidgetItemIterator(self.treeWidget)
        while iterator.value():
            item = iterator.value()
            if item.checkState(0) == Qt.Checked:
                href = item.data(0, Qt.UserRole)
                if href and href != "info:bookinfo":
                    all_checked_hrefs.add(href)
                    ordered_checked_items.append((item, href))
            iterator += 1

        # Process checked items in order
        for item, href in ordered_checked_items:
            # Always use the exact href (including fragment) from the TOC
            text = self.content_texts.get(href)
            if text and text.strip():
                title = item.text(0)
                title = re.sub(r"^\s*-\s*", "", title).strip()
                marker = f"<<CHAPTER_MARKER:{title}>>"
                chapter_titles.append((title, marker + "\n" + text))

        return "\n\n".join([t[1] for t in chapter_titles]), all_checked_hrefs

    def _get_pdf_selected_text(self):
        """Get selected text from PDF content"""
        all_checked_identifiers = set()
        included_text_ids = set()
        section_titles = []
        all_content = []

        # Check if PDF has no bookmarks
        pdf_has_no_bookmarks = (
            hasattr(self, "has_pdf_bookmarks") and not self.has_pdf_bookmarks
        )

        # Collect all checked identifiers
        iterator = QTreeWidgetItemIterator(self.treeWidget)
        while iterator.value():
            item = iterator.value()
            if item.checkState(0) == Qt.Checked:
                identifier = item.data(0, Qt.UserRole)
                if identifier:
                    all_checked_identifiers.add(identifier)
            iterator += 1

        # For PDFs without bookmarks, collect all content without chapter markers
        if pdf_has_no_bookmarks:
            sorted_page_ids = sorted(
                [id for id in all_checked_identifiers if id.startswith("page_")],
                key=lambda x: int(x.split("_")[1]) if x.split("_")[1].isdigit() else 0,
            )
            for page_id in sorted_page_ids:
                if page_id not in included_text_ids:
                    text = self.content_texts.get(page_id, "")
                    if text:
                        all_content.append(text)
                        included_text_ids.add(page_id)
            return "\n\n".join(all_content), all_checked_identifiers

        # For PDFs with bookmarks, process content with parent-child relationships
        # If only child pages are selected (not parent), use parent's name as chapter marker at first selected child
        iterator = QTreeWidgetItemIterator(self.treeWidget)
        while iterator.value():
            item = iterator.value()
            if item.childCount() > 0:
                parent_checked = item.checkState(0) == Qt.Checked
                parent_id = item.data(0, Qt.UserRole)
                parent_title = item.text(0)
                # Gather checked children
                checked_children = []
                for i in range(item.childCount()):
                    child = item.child(i)
                    child_id = child.data(0, Qt.UserRole)
                    if (
                        child.checkState(0) == Qt.Checked
                        and child_id
                        and child_id not in included_text_ids
                    ):
                        checked_children.append((child, child_id))
                # If parent is checked, use old logic (parent marker, all content)
                if parent_checked and parent_id and parent_id not in included_text_ids:
                    combined_text = self.content_texts.get(parent_id, "")
                    for child, child_id in checked_children:
                        child_text = self.content_texts.get(child_id, "")
                        if child_text:
                            combined_text += "\n\n" + child_text
                        included_text_ids.add(child_id)
                    if combined_text.strip():
                        title = re.sub(r"^\s*-\s*", "", parent_title).strip()
                        marker = f"<<CHAPTER_MARKER:{title}>>"
                        section_titles.append((title, marker + "\n" + combined_text))
                        included_text_ids.add(parent_id)
                # If only children are checked, use parent's name as marker at first child
                elif not parent_checked and checked_children:
                    title = re.sub(r"^\s*-\s*", "", parent_title).strip()
                    marker = f"<<CHAPTER_MARKER:{title}>>"
                    for idx, (child, child_id) in enumerate(checked_children):
                        text = self.content_texts.get(child_id, "")
                        if text:
                            if idx == 0:
                                section_titles.append((title, marker + "\n" + text))
                            else:
                                section_titles.append((title, text))
                        included_text_ids.add(child_id)
            elif item.flags() & Qt.ItemIsUserCheckable:
                identifier = item.data(0, Qt.UserRole)
                if (
                    identifier
                    and identifier not in included_text_ids
                    and item.checkState(0) == Qt.Checked
                ):
                    text = self.content_texts.get(identifier, "")
                    if text:
                        title = item.text(0)
                        title = re.sub(r"^\s*-\s*", "", title).strip()
                        marker = f"<<CHAPTER_MARKER:{title}>>"
                        section_titles.append((title, marker + "\n" + text))
                        included_text_ids.add(identifier)
            iterator += 1

        return "\n\n".join([t[1] for t in section_titles]), all_checked_identifiers

    def on_save_chapters_changed(self, state):
        """Update the save_chapters_separately flag"""
        self.save_chapters_separately = bool(state)
        self.merge_chapters_checkbox.setEnabled(self.save_chapters_separately)
        HandlerDialog._save_chapters_separately = self.save_chapters_separately

    def on_merge_chapters_changed(self, state):
        """Update the merge_chapters_at_end flag"""
        self.merge_chapters_at_end = bool(state)
        HandlerDialog._merge_chapters_at_end = self.merge_chapters_at_end

    def get_save_chapters_separately(self):
        """Return whether to save chapters separately"""
        return (
            self.save_chapters_separately
            if self.save_chapters_checkbox.isEnabled()
            else False
        )

    def get_merge_chapters_at_end(self):
        """Return whether to merge chapters at the end"""
        return self.merge_chapters_at_end

    def on_tree_context_menu(self, pos):
        """Handle context menu on tree items"""
        item = self.treeWidget.itemAt(pos)
        if (
            not item
            or item.childCount() == 0
            or not (item.flags() & Qt.ItemIsUserCheckable)
        ):
            return

        menu = QMenu(self)
        checked = item.checkState(0) == Qt.Checked
        text = "Unselect only this" if checked else "Select only this"
        action = menu.addAction(text)

        def do_toggle():
            self.treeWidget.blockSignals(True)
            new_state = Qt.Unchecked if checked else Qt.Checked
            item.setCheckState(0, new_state)
            self.treeWidget.blockSignals(False)
            self._update_checked_set_from_tree()

        action.triggered.connect(do_toggle)
        menu.exec_(self.treeWidget.mapToGlobal(pos))

    def closeEvent(self, event):
        """Clean up resources when the dialog is closed"""
        if self.pdf_doc is not None:
            self.pdf_doc.close()
        event.accept()
