"""Academic PDF Report Generator for SentinelOps SOC Alert-Triage Module.
CSA06 - Design and Analysis of Algorithms (CO2 Debugging and Optimisation).
Student: R.VISSHAAL (Reg No: 192421025).
"""

from pathlib import Path
import os
import sys

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)

ROOT_DIR = Path(__file__).resolve().parent.parent
REPORT_PDF_PATH = ROOT_DIR / "Report" / "CO2_Debugging_Optimisation_Report.pdf"
CP_CHART_PATH = ROOT_DIR / "Supporting_Files" / "closest_pair_computations.png"
SORT_CHART_PATH = ROOT_DIR / "Supporting_Files" / "insertion_sort_comparisons.png"


class NumberedCanvas(canvas.Canvas):
    """Canvas that performs a two-pass calculation for dynamic 'Page X of Y' numbering."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))

        # Header (pages 2+)
        if self._pageNumber > 1:
            self.drawString(54, 755, "CSA06 — Design and Analysis of Algorithms | CO2 Debugging & Optimisation Task")
            self.drawRightString(558, 755, "SentinelOps SOC Alert-Triage")
            self.setStrokeColor(colors.HexColor("#D0D7DE"))
            self.setLineWidth(0.5)
            self.line(54, 748, 558, 748)

        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#D0D7DE"))
        self.setLineWidth(0.5)
        self.line(54, 45, 558, 45)

        self.drawString(54, 33, "Student: R.VISSHAAL (192421025) — Department of Computer Science & Engineering")
        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(558, 33, page_str)
        self.restoreState()


def build_pdf():
    doc = SimpleDocTemplate(
        str(REPORT_PDF_PATH),
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    primary_color = colors.HexColor("#1A365D")   # Deep Navy
    secondary_color = colors.HexColor("#2B6CB0") # Medium Blue
    dark_text = colors.HexColor("#2D3748")       # Charcoal

    title_style = ParagraphStyle(
        "CoverTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=primary_color,
        alignment=1,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        "CoverSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=17,
        textColor=secondary_color,
        alignment=1,
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        "Heading1_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=primary_color,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        "Heading2_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=13,
        textColor=secondary_color,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        "Body_Custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11.5,
        textColor=dark_text,
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        "Bullet_Custom",
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        "Code_Custom",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#1A202C")
    )

    table_header_style = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.5,
        leading=9.5,
        textColor=colors.white,
        alignment=1
    )

    table_cell_style = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.0,
        leading=8.5,
        textColor=dark_text
    )

    table_cell_bold = ParagraphStyle(
        "TableCellBold",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.0,
        leading=8.5,
        textColor=dark_text
    )

    story = []

    # -------------------------------------------------------------
    # COVER / HEADER BLOCK
    # -------------------------------------------------------------
    story.append(Spacer(1, 10))
    story.append(Paragraph("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING", ParagraphStyle("DeptHeader", fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=primary_color, alignment=1)))
    story.append(Spacer(1, 4))
    story.append(Paragraph("CSA06 — DESIGN AND ANALYSIS OF ALGORITHMS", ParagraphStyle("CourseHeader", fontName="Helvetica-Bold", fontSize=12, leading=15, textColor=secondary_color, alignment=1)))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Continuous Assessment Assessment (CO2): Debugging and Optimisation Task", subtitle_style))
    story.append(Paragraph("SOC Alert-Triage Module — SentinelOps Incident Response Platform", title_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceBefore=4, spaceAfter=10))

    meta_table_data = [
        [
            Paragraph("<b>Student Name:</b>", body_style), Paragraph("R.VISSHAAL", body_style),
            Paragraph("<b>Registration Number:</b>", body_style), Paragraph("192421025", body_style)
        ],
        [
            Paragraph("<b>Course Code & Name:</b>", body_style), Paragraph("CSA06 — Design & Analysis of Algorithms", body_style),
            Paragraph("<b>Submission Date:</b>", body_style), Paragraph("26 October 2026", body_style)
        ],
        [
            Paragraph("<b>Assessment Component:</b>", body_style), Paragraph("CO2 Debugging & Optimisation", body_style),
            Paragraph("<b>Maximum Marks:</b>", body_style), Paragraph("50 Marks", body_style)
        ],
        [
            Paragraph("<b>GitHub Repository:</b>", body_style),
            Paragraph("https://github.com/visshaalpvt/CO2-Assessment-Tool-2-Debugging-and-Optimization-Task-SOC-Alert-Triage-Module-of-SentinelOps.git", table_cell_style),
            Paragraph("<b>Target Branch:</b>", body_style), Paragraph("master / main", body_style)
        ]
    ]
    meta_table = Table(meta_table_data, colWidths=[110, 175, 110, 109])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F7FAFC")),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#CBD5E0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # SECTION 1: PROBLEM IDENTIFICATION & DEFECT REGISTER
    # -------------------------------------------------------------
    story.append(Paragraph("1. Problem Identification", h1_style))
    story.append(Paragraph(
        "The SentinelOps Security Operations Centre (SOC) alert-triage module processes critical incident data: "
        "prioritising security alerts by severity (stable descending), filtering blocked IP addresses via blocklist lookup, "
        "scanning raw network audit logs for cyber-attack signatures, and detecting concurrent anomalous logins via geographical closest-pair analysis. "
        "The original module supplied in <code>original_buggy.py</code> contained nine distinct defects that caused alert corruption, "
        "security bypasses, missed attack detections, and selection of maximum distances instead of closest pairs.",
        body_style
    ))

    story.append(Paragraph("1.1 Complete Nine-Defect Register", h2_style))

    defect_headers = [
        Paragraph("<b>#</b>", table_header_style),
        Paragraph("<b>Function</b>", table_header_style),
        Paragraph("<b>Line</b>", table_header_style),
        Paragraph("<b>Faulty Statement</b>", table_header_style),
        Paragraph("<b>Root Cause & Defect Mechanism</b>", table_header_style),
        Paragraph("<b>Actual vs Expected Output</b>", table_header_style),
        Paragraph("<b>Corrected Logic</b>", table_header_style),
    ]

    defect_rows = [
        [
            Paragraph("1", table_cell_bold),
            Paragraph("sort_alerts", table_cell_style),
            Paragraph("7", table_cell_style),
            Paragraph("<code>while j > 0 and ...</code>", table_cell_style),
            Paragraph("Loop condition <code>j > 0</code> terminates before index 0 is checked, preventing elements from shifting to the head.", table_cell_style),
            Paragraph("Highest severity alerts cannot move to index 0; list corrupted.", table_cell_style),
            Paragraph("<code>while j >= 0 and ...</code>", table_cell_style),
        ],
        [
            Paragraph("2", table_cell_bold),
            Paragraph("sort_alerts", table_cell_style),
            Paragraph("10", table_cell_style),
            Paragraph("<code>alerts[j] = key</code>", table_cell_style),
            Paragraph("Inserts at <code>j</code> instead of <code>j+1</code>. Overwrites element at index <code>j</code> and duplicates element at <code>j+1</code>.", table_cell_style),
            Paragraph("Actual: <code>[('A4',9),('A3',5),('A3',5),('A5',1),('A5',1)]</code> (A1, A2 lost). Expected: <code>[('A2',9),('A4',9),('A3',5),('A1',3),('A5',1)]</code>.", table_cell_style),
            Paragraph("<code>alerts[j + 1] = key</code>", table_cell_style),
        ],
        [
            Paragraph("3", table_cell_bold),
            Paragraph("is_blocked", table_cell_style),
            Paragraph("16", table_cell_style),
            Paragraph("<code>return False</code>", table_cell_style),
            Paragraph("Returns <code>False</code> when a blocked IP matches, incorrectly marking malicious IPs as safe.", table_cell_style),
            Paragraph("Actual: <code>10.0.0.5 -> False</code>. Expected: <code>10.0.0.5 -> True</code>.", table_cell_style),
            Paragraph("<code>return True</code>", table_cell_style),
        ],
        [
            Paragraph("4", table_cell_bold),
            Paragraph("is_blocked", table_cell_style),
            Paragraph("18", table_cell_style),
            Paragraph("<code>else: return False</code>", table_cell_style),
            Paragraph("Prematurely exits during first iteration if index 0 does not match, omitting remaining entries.", table_cell_style),
            Paragraph("Actual: <code>10.0.0.9 -> False</code> (aborts at item 0). Expected: <code>True</code>.", table_cell_style),
            Paragraph("Remove inner <code>else</code>; return <code>False</code> only after loop exhausts.", table_cell_style),
        ],
        [
            Paragraph("5", table_cell_bold),
            Paragraph("find_signature", table_cell_style),
            Paragraph("23", table_cell_style),
            Paragraph("<code>for i in range(n - m):</code>", table_cell_style),
            Paragraph("Upper bound excludes final valid alignment index <code>n - m</code>. Also produces empty range when <code>n == m</code>.", table_cell_style),
            Paragraph("Actual: <code>find_signature('FAILFAIXFAIL','FAIL') -> [0, 4]</code> (misses index 8). Expected: <code>[0, 8]</code>.", table_cell_style),
            Paragraph("<code>for i in range(n - m + 1):</code>", table_cell_style),
        ],
        [
            Paragraph("6", table_cell_bold),
            Paragraph("find_signature", table_cell_style),
            Paragraph("27", table_cell_style),
            Paragraph("<code>if j == m - 1:</code>", table_cell_style),
            Paragraph("Falsely triggers when mismatch occurs at last char (<code>j=m-1</code>). Also fails for empty patterns.", table_cell_style),
            Paragraph("Actual accepts mismatch 'FAIX' at index 4 because mismatch at <code>j=3==4-1</code>.", table_cell_style),
            Paragraph("Verify all chars matched: <code>if j == m:</code>", table_cell_style),
        ],
        [
            Paragraph("7", table_cell_bold),
            Paragraph("closest_logins", table_cell_style),
            Paragraph("32", table_cell_style),
            Paragraph("<code>min_dist = 0</code>", table_cell_style),
            Paragraph("Since Euclidean distance $d \\ge 0$, initializing to 0 prevents finding any pair with $d < min\\_dist$.", table_cell_style),
            Paragraph("Combined with Defect 9, selects the farthest pair instead of the closest pair.", table_cell_style),
            Paragraph("Initialise to infinity: <code>best_sq = math.inf</code>", table_cell_style),
        ],
        [
            Paragraph("8", table_cell_bold),
            Paragraph("closest_logins", table_cell_style),
            Paragraph("34-35", table_cell_style),
            Paragraph("<code>for i in ...: for j in ...:</code>", table_cell_style),
            Paragraph("Compares self-pairs ($i == j$, $d = 0$) and duplicates unordered pairs ($(i,j)$ and $(j,i)$).", table_cell_style),
            Paragraph("Performs $n^2$ distance calculations instead of $n(n-1)/2$ and risks reporting self-pairs.", table_cell_style),
            Paragraph("Iterate unordered pairs: <code>i in 0..n-2, j in i+1..n-1</code>", table_cell_style),
        ],
        [
            Paragraph("9", table_cell_bold),
            Paragraph("closest_logins", table_cell_style),
            Paragraph("38", table_cell_style),
            Paragraph("<code>if d > min_dist:</code>", table_cell_style),
            Paragraph("Greater-than comparison actively searches for the maximum (farthest) separation.", table_cell_style),
            Paragraph("Actual: pair (0,2) with $d \\approx 60.44$ km. Expected: closest pair (0,5) with $d = \\sqrt{2} \\approx 1.414$ km.", table_cell_style),
            Paragraph("Compare minimum squared distance: <code>if d_sq < best_sq:</code>", table_cell_style),
        ],
    ]

    defect_table = Table([defect_headers] + defect_rows, colWidths=[15, 60, 25, 80, 130, 115, 79])
    defect_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(defect_table)
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # SECTION 2: ROOT CAUSES & SYSTEMATIC DEBUGGING
    # -------------------------------------------------------------
    story.append(Paragraph("2. Root Causes and Systematic Debugging", h1_style))
    story.append(Paragraph(
        "A rigorous, single-variable debugging methodology was applied. Each defect was isolated, traced against execution state, "
        "and corrected in <code>Source_Code/corrected_reference.py</code> without changing underlying algorithmic paradigms.",
        body_style
    ))

    story.append(Paragraph("<b>2.1 Insertion Sort Trace:</b> In the original code, when inserting <code>('A2', 9)</code> into <code>[('A1', 3)]</code>, "
                           "the loop checked <code>j > 0</code>, immediately terminating at <code>j = 0</code>. Then <code>alerts[0] = ('A2', 9)</code> overwrote <code>A1</code>. "
                           "Changing the loop condition to <code>j >= 0</code> and insertion position to <code>alerts[j + 1] = key</code> ensures items are shifted rightward "
                           "and placed in the vacated spot, preserving stability: <code>[('A2', 9), ('A4', 9), ('A3', 5), ('A1', 3), ('A5', 1)]</code>.", body_style))

    story.append(Paragraph("<b>2.2 Blocklist Search Trace:</b> The inner <code>else: return False</code> caused an immediate return after evaluating index 0. "
                           "Searching for <code>10.0.0.9</code> against <code>['10.0.0.5', '10.0.0.9', '172.16.4.2']</code> compared <code>'10.0.0.5' == '10.0.0.9'</code>, "
                           "failed, and aborted. Removing <code>else</code> and returning <code>True</code> upon a match correctly finds matches anywhere in the list.", body_style))

    story.append(Paragraph("<b>2.3 String-Matching Alignment Trace:</b> For log length $n=12$ and pattern length $m=4$, valid starting indices are $0 \\le i \\le 8$. "
                           "The original <code>range(12 - 4) = range(8)</code> checked $i \\in [0..7]$, missing index 8 ('FAIL' at end). "
                           "Furthermore, at index 4 ('FAIX'), mismatch on 'X' at $j=3$ broke the loop with $j=3==m-1$, recording a false positive. "
                           "The corrected loop iterates <code>range(n - m + 1)</code> and tests <code>j == m</code>.", body_style))

    story.append(Paragraph("<b>2.4 Closest-Pair Trace:</b> Distance is non-negative. Initializing <code>min_dist = 0</code> meant no distance could ever be less than 0. "
                           "The original code checked <code>if d > min_dist</code>, thus finding the maximum distance between points $(2,3)$ and $(40,50)$ ($d \\approx 60.44$ km). "
                           "Setting <code>best_sq = math.inf</code>, comparing $i < j$, and minimizing $d^2$ correctly identifies pair $(0, 5)$ with $d = \\sqrt{2} \\approx 1.414$ km.", body_style))

    story.append(Spacer(1, 6))

    # -------------------------------------------------------------
    # SECTION 3: OPTIMISATION STRATEGY
    # -------------------------------------------------------------
    story.append(Paragraph("3. Algorithm Optimisation Strategy", h1_style))
    story.append(Paragraph(
        "While <code>corrected_reference.py</code> serves as the verified baseline, production SOC triage handles up to 50,000 alerts "
        "and 8,000 login events per batch. <code>Source_Code/optimized_module.py</code> delivers high-performance algorithms while preserving exact outputs:",
        body_style
    ))
    story.append(Paragraph("• <b>Stable Alert Sorting:</b> Replaced insertion sort ($O(n^2)$ worst-case) with Python's adaptive Timsort (<code>sorted(..., reverse=True)</code>). "
                           "Timsort achieves $O(n \\log n)$ worst-case and $O(n)$ best-case on partially ordered alerts while guaranteeing strict stability (equal severities retain arrival order).", bullet_style))
    story.append(Paragraph("• <b>Reusable Blocklist Hash Index:</b> Converted sequential search ($O(b)$ per query) into a hash set via <code>make_blocklist_index()</code>. "
                           "Construction is $O(b)$, enabling expected $O(1)$ amortized lookups across repeated queries $q$, reducing total lookup cost from $O(q \\cdot b)$ to $O(b + q)$.", bullet_style))
    story.append(Paragraph("• <b>Brute-Force Signature Matching:</b> Retained brute-force matching as required by the specification, incorporating early mismatch exit "
                           "and exact alignment bounds. Avoided unnecessary character comparisons while preserving $O((L-m+1)m)$ worst-case guarantees.", bullet_style))
    story.append(Paragraph("• <b>Divide-and-Conquer Closest Pair:</b> Replaced all-pairs enumeration ($O(p^2)$, requiring 31,996,000 comparisons at $p=8,000$) with a recursive divide-and-conquer "
                           "algorithm running in $O(p \\log p)$. Points are sorted by x-coordinate, partitioned recursively, and merged in y-order. A narrow vertical strip of width $2\\delta$ "
                           "is inspected, where geometric packing guarantees each point is compared with at most 7-8 successors. Squared distances are used to eliminate expensive square root operations.", bullet_style))

    story.append(Spacer(1, 6))

    # -------------------------------------------------------------
    # SECTION 4: COMPLEXITY ANALYSIS
    # -------------------------------------------------------------
    story.append(Paragraph("4. Theoretical Complexity Analysis", h1_style))

    complexity_headers = [
        Paragraph("<b>Operation / Algorithm</b>", table_header_style),
        Paragraph("<b>Corrected Baseline (Time)</b>", table_header_style),
        Paragraph("<b>Optimised Module (Time)</b>", table_header_style),
        Paragraph("<b>Baseline Space</b>", table_header_style),
        Paragraph("<b>Optimised Space</b>", table_header_style),
        Paragraph("<b>Asymptotic Improvement</b>", table_header_style),
    ]

    complexity_rows = [
        [
            Paragraph("Alert Sorting ($n$ alerts)", table_cell_bold),
            Paragraph("Insertion Sort: $O(n^2)$ worst/avg; $O(n)$ best", table_cell_style),
            Paragraph("Timsort: $O(n \\log n)$ worst; $O(n)$ adaptive", table_cell_style),
            Paragraph("$O(n)$ copy", table_cell_style),
            Paragraph("$O(n)$ auxiliary", table_cell_style),
            Paragraph("Asymptotically superior ($O(n^2) \\to O(n \\log n)$)", table_cell_style),
        ],
        [
            Paragraph("Blocklist ($b$ IPs, $q$ queries)", table_cell_bold),
            Paragraph("Sequential: $O(q \\cdot b)$ total; $O(b)$ per query", table_cell_style),
            Paragraph("Hash Index: $O(b)$ build + $O(q)$ queries [$O(1)$ each]", table_cell_style),
            Paragraph("$O(1)$ aux", table_cell_style),
            Paragraph("$O(b)$ set", table_cell_style),
            Paragraph("Significant speedup ($O(b) \\to O(1)$ per query)", table_cell_style),
        ],
        [
            Paragraph("Signature Scan ($L$ log, $m$ pat)", table_cell_bold),
            Paragraph("Brute-Force: $O((L-m+1)m)$ worst", table_cell_style),
            Paragraph("Brute-Force: $O((L-m+1)m)$ with early exit", table_cell_style),
            Paragraph("$O(k)$ matches", table_cell_style),
            Paragraph("$O(k)$ matches", table_cell_style),
            Paragraph("Preserves worst-case; eliminates redundant checks", table_cell_style),
        ],
        [
            Paragraph("Closest Pair ($p$ events)", table_cell_bold),
            Paragraph("All-Pairs Brute Force: $O(p^2)$ exact $p(p-1)/2$", table_cell_style),
            Paragraph("Divide-and-Conquer: $O(p \\log p)$", table_cell_style),
            Paragraph("$O(1)$ aux", table_cell_style),
            Paragraph("$O(p)$ recursion", table_cell_style),
            Paragraph("Massive asymptotic gain ($O(p^2) \\to O(p \\log p)$)", table_cell_style),
        ]
    ]

    complexity_table = Table([complexity_headers] + complexity_rows, colWidths=[100, 110, 115, 55, 55, 69])
    complexity_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(complexity_table)
    story.append(Spacer(1, 10))

    # Page break before experimental charts
    story.append(PageBreak())

    # -------------------------------------------------------------
    # SECTION 5: EXPERIMENTAL RESULTS & BENCHMARKS
    # -------------------------------------------------------------
    story.append(Paragraph("5. Experimental Performance Analysis", h1_style))
    story.append(Paragraph(
        "Real experimental measurements were conducted on Windows (Python 3.11.9) using fixed random seeds. "
        "All measurements reflect physical program executions without synthetic or fabricated data.",
        body_style
    ))

    story.append(Paragraph("5.1 Closest-Pair Scalability (1,000 to 8,000 Events)", h2_style))

    cp_exp_headers = [
        Paragraph("<b>Batch Size ($p$)</b>", table_header_style),
        Paragraph("<b>Brute-Force Evaluations</b>", table_header_style),
        Paragraph("<b>Optimised Evaluations</b>", table_header_style),
        Paragraph("<b>Evaluation Reduction</b>", table_header_style),
        Paragraph("<b>Brute Time (s)</b>", table_header_style),
        Paragraph("<b>Optimised Time (s)</b>", table_header_style),
        Paragraph("<b>Speedup Factor</b>", table_header_style),
        Paragraph("<b>Result Agreement</b>", table_header_style),
    ]

    cp_exp_data = [
        [
            Paragraph("1,000", table_cell_bold),
            Paragraph("499,500", table_cell_style),
            Paragraph("1,145", table_cell_style),
            Paragraph("99.77%", table_cell_style),
            Paragraph("0.1523", table_cell_style),
            Paragraph("0.0089", table_cell_style),
            Paragraph("17.1x", table_cell_style),
            Paragraph("Verified (Exact)", table_cell_style),
        ],
        [
            Paragraph("2,000", table_cell_bold),
            Paragraph("1,999,000", table_cell_style),
            Paragraph("2,316", table_cell_style),
            Paragraph("99.88%", table_cell_style),
            Paragraph("0.6024", table_cell_style),
            Paragraph("0.0169", table_cell_style),
            Paragraph("35.6x", table_cell_style),
            Paragraph("Verified (Exact)", table_cell_style),
        ],
        [
            Paragraph("4,000", table_cell_bold),
            Paragraph("7,998,000", table_cell_style),
            Paragraph("4,618", table_cell_style),
            Paragraph("99.94%", table_cell_style),
            Paragraph("2.4657", table_cell_style),
            Paragraph("0.0357", table_cell_style),
            Paragraph("69.1x", table_cell_style),
            Paragraph("Verified (Exact)", table_cell_style),
        ],
        [
            Paragraph("8,000", table_cell_bold),
            Paragraph("31,996,000", table_cell_style),
            Paragraph("9,344", table_cell_style),
            Paragraph("99.97%", table_cell_style),
            Paragraph("7.1572", table_cell_style),
            Paragraph("0.0544", table_cell_style),
            Paragraph("131.6x", table_cell_style),
            Paragraph("Verified (Exact)", table_cell_style),
        ],
    ]

    cp_table = Table([cp_exp_headers] + cp_exp_data, colWidths=[55, 75, 75, 60, 55, 60, 55, 69])
    cp_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(cp_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("5.2 Insertion-Sort Key Comparisons Across Input Distributions", h2_style))

    sort_headers = [
        Paragraph("<b>Input Size ($n$)</b>", table_header_style),
        Paragraph("<b>Distribution</b>", table_header_style),
        Paragraph("<b>Theoretical Complexity</b>", table_header_style),
        Paragraph("<b>Key Comparisons</b>", table_header_style),
        Paragraph("<b>Timsort Runtime (s)</b>", table_header_style),
    ]

    sort_data = [
        [Paragraph("1,000", table_cell_bold), Paragraph("Already Descending", table_cell_style), Paragraph("$O(n)$ Best Case", table_cell_style), Paragraph("999", table_cell_style), Paragraph("0.000052", table_cell_style)],
        [Paragraph("1,000", table_cell_bold), Paragraph("Nearly Descending (1% perturbed)", table_cell_style), Paragraph("$O(n)$ Adaptive", table_cell_style), Paragraph("1,098", table_cell_style), Paragraph("0.000062", table_cell_style)],
        [Paragraph("1,000", table_cell_bold), Paragraph("Uniform Random", table_cell_style), Paragraph("$O(n^2)$ Average Case", table_cell_style), Paragraph("250,789", table_cell_style), Paragraph("0.000159", table_cell_style)],
        [Paragraph("5,000", table_cell_bold), Paragraph("Already Descending", table_cell_style), Paragraph("$O(n)$ Best Case", table_cell_style), Paragraph("4,999", table_cell_style), Paragraph("0.000232", table_cell_style)],
        [Paragraph("5,000", table_cell_bold), Paragraph("Nearly Descending (1% perturbed)", table_cell_style), Paragraph("$O(n)$ Adaptive", table_cell_style), Paragraph("5,098", table_cell_style), Paragraph("0.000232", table_cell_style)],
        [Paragraph("5,000", table_cell_bold), Paragraph("Uniform Random", table_cell_style), Paragraph("$O(n^2)$ Average Case", table_cell_style), Paragraph("6,289,295", table_cell_style), Paragraph("0.000763", table_cell_style)],
        [Paragraph("10,000", table_cell_bold), Paragraph("Already Descending", table_cell_style), Paragraph("$O(n)$ Best Case", table_cell_style), Paragraph("9,999", table_cell_style), Paragraph("0.000537", table_cell_style)],
        [Paragraph("10,000", table_cell_bold), Paragraph("Nearly Descending (1% perturbed)", table_cell_style), Paragraph("$O(n)$ Adaptive", table_cell_style), Paragraph("10,098", table_cell_style), Paragraph("0.000431", table_cell_style)],
        [Paragraph("10,000", table_cell_bold), Paragraph("Uniform Random", table_cell_style), Paragraph("$O(n^2)$ Average Case", table_cell_style), Paragraph("25,017,572", table_cell_style), Paragraph("0.001440", table_cell_style)],
    ]

    sort_table = Table([sort_headers] + sort_data, colWidths=[65, 140, 110, 95, 94])
    sort_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(sort_table)
    story.append(Spacer(1, 10))

    # Embed Generated Charts Side-by-Side or Stacked
    story.append(Paragraph("5.3 Empirical Benchmark Visualizations", h2_style))
    if CP_CHART_PATH.exists() and SORT_CHART_PATH.exists():
        img_w, img_h = 245, 150
        chart_table = Table([
            [
                Image(str(CP_CHART_PATH), width=img_w, height=img_h),
                Image(str(SORT_CHART_PATH), width=img_w, height=img_h)
            ],
            [
                Paragraph("<b>Figure 1:</b> Closest-Pair Squared-Distance Evaluations ($O(p^2)$ vs $O(p \\log p)$).", table_cell_style),
                Paragraph("<b>Figure 2:</b> Insertion-Sort Comparisons across Ordered and Random Inputs.", table_cell_style)
            ]
        ], colWidths=[252, 252])
        chart_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ('TOPPADDING', (0,0), (-1,-1), 2),
        ]))
        story.append(chart_table)

    story.append(Paragraph("<b>Empirical Interpretation:</b> Figure 1 demonstrates the massive quadratic divergence of brute-force evaluation: at 8,000 points, "
                           "brute force evaluates 31,996,000 pairs (taking 7.16s), whereas divide-and-conquer evaluates only 9,344 pairs (taking 0.054s) — a <b>131.6x speedup</b> "
                           "with 100% distance agreement. Figure 2 confirms insertion sort's quadratic penalty on random data (25,017,572 comparisons at $n=10,000$) "
                           "contrasting with near-linear performance on ordered runs, justifying Timsort's deployment for 50,000-alert workloads.", body_style))

    story.append(Spacer(1, 8))

    # -------------------------------------------------------------
    # SECTION 6: TEST VERIFICATION
    # -------------------------------------------------------------
    story.append(Paragraph("6. Test Harness and Verification", h1_style))
    story.append(Paragraph(
        "A comprehensive test harness (<code>Source_Code/test_harness.py</code>) incorporating <b>57 unit tests</b> was executed via Python's standard <code>unittest</code> framework. "
        "Both <code>corrected_reference.py</code> and <code>optimized_module.py</code> passed all tests with zero failures.",
        body_style
    ))

    test_summary_data = [
        [Paragraph("<b>Category</b>", table_header_style), Paragraph("<b>Test Scope & Boundary Coverage</b>", table_header_style), Paragraph("<b>Tests Run</b>", table_header_style), Paragraph("<b>Status</b>", table_header_style)],
        [Paragraph("Alert Sorting", table_cell_bold), Paragraph("Supplied sample, empty list, single alert, already sorted, reverse sorted, equal severities, stability, no lost/duplicated alerts.", table_cell_style), Paragraph("16", table_cell_style), Paragraph("PASS (100%)", table_cell_style)],
        [Paragraph("Blocklist Search", table_cell_bold), Paragraph("First position match, later position match, absent IP, empty blocklist, repeated batched queries.", table_cell_style), Paragraph("10", table_cell_style), Paragraph("PASS (100%)", table_cell_style)],
        [Paragraph("Signature Matching", table_cell_bold), Paragraph("Supplied sample, pattern at start, pattern at end, multiple occurrences, overlapping patterns, no match, pattern longer than log, empty log, empty pattern.", table_cell_style), Paragraph("18", table_cell_style), Paragraph("PASS (100%)", table_cell_style)],
        [Paragraph("Closest Pair", table_cell_bold), Paragraph("Supplied sample, empty event list, 1 event, 2 events, duplicate points, equidistant pairs, 40 deterministic random cross-checks against brute-force.", table_cell_style), Paragraph("13", table_cell_style), Paragraph("PASS (100%)", table_cell_style)],
        [Paragraph("<b>Total Suite</b>", table_cell_bold), Paragraph("<b>Full automated regression suite executed across both modules</b>", table_cell_bold), Paragraph("<b>57</b>", table_cell_bold), Paragraph("<b>ALL PASSED</b>", table_cell_bold)],
    ]
    test_table = Table(test_summary_data, colWidths=[90, 274, 60, 80])
    test_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, colors.HexColor("#F8FAFC")]),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(test_table)
    story.append(Spacer(1, 8))

    # -------------------------------------------------------------
    # SECTION 7: REPOSITORY STRUCTURE & REPRODUCIBILITY
    # -------------------------------------------------------------
    story.append(Paragraph("7. Repository Structure and Reproducibility", h1_style))
    story.append(Paragraph(
        "The project is structured strictly in accordance with academic submission specifications:",
        body_style
    ))

    repo_tree_text = (
        "CO2_Debugging_Optimisation/\n"
        "├── Pseudocode/          (01_sort_alerts.txt, 02_blocklist_search.txt, 03_signature_matching.txt, 04_closest_pair.txt)\n"
        "├── Source_Code/         (original_buggy.py, corrected_reference.py, optimized_module.py, test_harness.py, requirements.txt)\n"
        "├── Report/              (CO2_Debugging_Optimisation_Report.pdf, screenshots/)\n"
        "├── Supporting_Files/    (defect_register.csv, closest_pair_experiments.csv, insertion_sort_comparisons.csv,\n"
        "│                         sort_timing_experiments.csv, execution_log.txt, unit_test_output.txt, experimental_results.json,\n"
        "│                         closest_pair_computations.png, insertion_sort_comparisons.png, test_datasets/)\n"
        "├── README.md            (Complete operational documentation and reproduction instructions)\n"
        "└── .gitignore           (Excludes virtual environments, pycache, temporary artifacts)"
    )
    story.append(Paragraph(f"<pre>{repo_tree_text}</pre>", code_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Reproduction Commands:</b><br/>"
                           "• Execute full unit test suite: <code>py -m unittest -v Source_Code/test_harness.py</code><br/>"
                           "• Reproduce benchmarks & charts: <code>py Supporting_Files/run_experiments.py</code>", body_style))

    story.append(Spacer(1, 8))

    # -------------------------------------------------------------
    # SECTION 8: CONCLUSION & ACADEMIC DECLARATION
    # -------------------------------------------------------------
    story.append(Paragraph("8. Conclusion & Student Declaration", h1_style))
    story.append(Paragraph(
        "All nine defects present in the original SentinelOps triage module were systematically identified, documented, and repaired. "
        "The corrected baseline guarantees semantic correctness and stability. The optimised module replaces quadratic bottlenecks with "
        "optimal $O(n \\log n)$ Timsort, $O(1)$ set lookup, and $O(p \\log p)$ divide-and-conquer closest-pair detection, delivering up to "
        "131.6x empirical speedups on production-scale workloads while maintaining 100% output fidelity.",
        body_style
    ))
    story.append(Spacer(1, 6))

    dec_box = [
        [Paragraph("<b>CANDIDATE ACADEMIC INTEGRITY DECLARATION</b>", table_header_style)],
        [Paragraph(
            "I hereby declare that this assignment submission entitled <b>'SentinelOps SOC Alert-Triage Module'</b> is my own original work "
            "prepared for <b>CSA06 — Design and Analysis of Algorithms</b>. All algorithmic defect diagnoses, corrections, optimisations, "
            "and empirical benchmark results presented herein reflect real program executions and comply with university academic honesty guidelines.<br/><br/>"
            "<b>Student Name:</b> R.VISSHAAL &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <b>Registration Number:</b> 192421025<br/>"
            "<b>Signature:</b> ___________________________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <b>Date:</b> 26 October 2026",
            table_cell_style
        )]
    ]
    dec_table = Table(dec_box, colWidths=[504])
    dec_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('BOX', (0,0), (-1,-1), 1, primary_color),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#F7FAFC")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(dec_table)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Report PDF built successfully: {REPORT_PDF_PATH}")


if __name__ == "__main__":
    build_pdf()
