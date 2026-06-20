import os

from pathlib import Path
from urllib.parse import quote, urlparse
import time

import flet as ft


BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"

PROFILE_NAME = "Timoteus N Matheus"
PROFILE_ROLE = "Electrical Engineering Student | UNAM"
PROFILE_EMAIL = "timoteusmatheus8@gmail.com"
PROFILE_GITHUB = "https://github.com/timoteusmatheus8-ux"
UNAM_LOGO_SRC = "unam-logo.png"
PROFILE_PHOTO_SRC = "profile-photo-new.jpeg"
ABOUT_PHOTO_SRC = "about-photo.jpg"
APP_PORT = 8553

# Color palette: high-contrast, web-friendly dark theme tuned for readability
# Background / surfaces
BG = "#071028"      # deep navy background
SURFACE = "#0b1a2b"       # primary surface
SURFACE_2 = "#0f2738"     # secondary surface
SURFACE_3 = "#122a3a"     # tertiary surface

# Text / accents
INK = "#f8fafc"           # primary text (very light)
STEEL = "#cbd5e1"         # secondary text / muted bright
MUTED = "#94a3b8"         # muted text
LINE = "#1f2a37"          # divider / line color

# Theme accents
PRIMARY = "#38bdf8"       # bright sky-blue accent (used for buttons/links)
ACCENT = "#f59e0b"        # warm amber accent for highlights
GREEN = "#34d399"         # success / positive
BLUE = PRIMARY
CYAN = "#06b6d4"          # teal accent
VIOLET = "#7c3aed"        # violet accent

# Backwards-compatible aliases for previous UNAM-specific names
UNAM_RED = PRIMARY
UNAM_GOLD = ACCENT
UNAM_BLACK = "#071028"
UNAM_WHITE = INK




# Certificate files and helpers removed — MATLAB certificate documents were
# removed from the codebase as requested.


def main(page: ft.Page):
    page.title = "UNAM Electrical Engineering Portfolio | Timoteus N Matheus"
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = ft.Theme(color_scheme_seed=UNAM_RED)
    page.bgcolor = BG
    page.padding = 0
    page.spacing = 0
    page.window_min_width = 980
    page.window_min_height = 720

    active_key = "home"

    def show_message(message: str):
        page.snack_bar = ft.SnackBar(ft.Text(message), open=True)
        page.update()

    async def open_email(_):
        await page.launch_url(f"mailto:{PROFILE_EMAIL}")

    async def open_github(_):
        await page.launch_url(PROFILE_GITHUB)

    async def play_reflection_video(_):
        await page.launch_url(
            asset_url("reflection-video.mp4"),
            web_popup_window_name="_blank",
        )

    def asset_url(path: str):
        clean_path = quote(path.replace("\\", "/"), safe="/")
        page_url = getattr(page, "url", None)
        if page_url:
            parsed_url = urlparse(page_url)
            if parsed_url.scheme and parsed_url.netloc:
                scheme = {"ws": "http", "wss": "https"}.get(parsed_url.scheme, parsed_url.scheme)
                return f"{scheme}://{parsed_url.netloc}/{clean_path}"
        return clean_path

    def logo_mark(width=138, height=86):
        # Return an empty placeholder instead of loading an external UNAM logo image.
        return ft.Container(
            width=width,
            height=height,
        )

    def image_slot(image_src: str, title: str, subtitle: str, width=238, height=278, icon=ft.Icons.PERSON, border_color=CYAN):
        # Only attempt to load an image when a non-empty path is provided and the file exists.
        photo_exists = bool(image_src) and (ASSETS_DIR / image_src).exists()
        if photo_exists:
            photo_content = ft.Image(
                src=(ASSETS_DIR / image_src).read_bytes(),
                width=width,
                height=height,
                fit=ft.BoxFit.COVER,
            )
        else:
            # Render an empty placeholder (no icons or text) so nothing appears in the image slot.
            photo_content = ft.Container()
        return ft.Container(
            width=width,
            height=height,
            alignment=ft.Alignment(0, 0),
            border_radius=8,
            border=ft.Border.all(1, ft.Colors.with_opacity(0.55, border_color)),
            bgcolor="#0c1420",
            content=photo_content,
        )

    def profile_photo_slot(width=238, height=278):
        # Circular profile photo slot: show image if present, otherwise an empty circular placeholder.
        photo_exists = bool(PROFILE_PHOTO_SRC) and (ASSETS_DIR / PROFILE_PHOTO_SRC).exists()
        radius = int(min(width, height) / 2)
        if photo_exists:
            photo_bytes = (ASSETS_DIR / PROFILE_PHOTO_SRC).read_bytes()
            photo = ft.Image(src=photo_bytes, width=width, height=height, fit=ft.BoxFit.COVER)
        else:
            photo = ft.Container()
        return ft.Container(
            width=width,
            height=height,
            alignment=ft.Alignment(0, 0),
            border_radius=radius,
            border=ft.Border.all(1, ft.Colors.with_opacity(0.55, CYAN)),
            bgcolor="#0c1420",
            content=photo,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        )

    def about_photo_slot(width=300, height=340):
        return image_slot(
            ABOUT_PHOTO_SRC,
            "About Photo",
            "Ready for upload",
            width=width,
            height=height,
            icon=ft.Icons.ENGINEERING,
            border_color=UNAM_GOLD,
        )

    def title_block(title: str, subtitle: str):
        return ft.Column(
            [
                ft.Text(title, size=34, weight=ft.FontWeight.W_800, color=INK),
                ft.Text(subtitle, size=17, color=MUTED),
                ft.Container(
                    height=4,
                    width=170,
                    border_radius=8,
                    gradient=ft.LinearGradient(
                        colors=[CYAN, UNAM_RED, UNAM_GOLD],
                        begin=ft.Alignment(-1, 0),
                        end=ft.Alignment(1, 0),
                    ),
                ),
            ],
            spacing=8,
        )

    def card(content, padding=18, bgcolor=SURFACE_2):
        return ft.Card(
            elevation=0,
            bgcolor=ft.Colors.TRANSPARENT,
            content=ft.Container(
                content=content,
                padding=padding,
                bgcolor=bgcolor,
                border_radius=8,
                border=ft.Border.all(1, LINE),
            ),
        )

    def status_chip(text: str, color: str):
        return ft.Container(
            content=ft.Text(text, size=13, color=color, weight=ft.FontWeight.W_700),
            padding=ft.Padding(left=10, top=6, right=10, bottom=6),
            border_radius=8,
            bgcolor=ft.Colors.with_opacity(0.14, color),
            border=ft.Border.all(1, ft.Colors.with_opacity(0.34, color)),
        )

    def contact_button(label: str, icon: str, click_handler):
        return ft.FilledButton(
            label,
            icon=icon,
            on_click=click_handler,
            style=ft.ButtonStyle(
                bgcolor=UNAM_RED,
                color=UNAM_WHITE,
                shape=ft.RoundedRectangleBorder(radius=8),
                padding=ft.Padding(left=16, top=14, right=16, bottom=14),
            ),
        )

    def page_shell(controls):
        return ft.Column(
            controls,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=18,
        )

    def unam_student_banner():
        # Banner removed: return an empty container so pages render without the
        # top UNAM banner section that previously displayed the name and roles.
        return ft.Container()

    electrical_focus = [
        ("Circuit Design", "analog and digital circuits", ft.Icons.ELECTRIC_BOLT, UNAM_RED),
        ("Signals & Systems", "signal analysis and processing", ft.Icons.SHOW_CHART, UNAM_GOLD),
        ("Electronics", "semiconductors and embedded systems", ft.Icons.DEVICE_HUB, GREEN),
        ("Power Systems", "generation, transmission, distribution", ft.Icons.POWER, BLUE),
    ]

    formula_cards = [
        ("Ohm's Law", "V = I * R", "Relationship between voltage, current and resistance."),
        ("Power", "P = V * I", "Electrical power computed from voltage and current."),
        ("Capacitance", "Q = C * V", "Charge stored in a capacitor for a given voltage."),
        ("Impedance (AC)", "Z = R + jX", "Combined resistance and reactance in AC circuits."),
    ]



    home_page = page_shell(
        [
            ft.Container(
                padding=ft.Padding(left=26, top=6, right=26, bottom=26),
                border_radius=8,
                border=ft.Border.all(1, LINE),
                gradient=ft.LinearGradient(
                    colors=["#0b111c", "#121827", "#1e1217"],
                    begin=ft.Alignment(-1, -1),
                    end=ft.Alignment(1, 1),
                ),
                content=ft.ResponsiveRow(
                    [
                        ft.Container(
                            col={"sm": 12, "md": 7},
                            content=ft.Column(
                                [
                                    ft.Row(
                                        [
                                                    status_chip("UNAM Electrical Engineering", CYAN),
                                                    status_chip("Programming I Portfolio", UNAM_GOLD),
                                        ],
                                        spacing=8,
                                        wrap=True,
                                    ),
                                    ft.Text(
                                        "Welcome to my webportfolio",
                                        size=44,
                                        weight=ft.FontWeight.W_900,
                                        color=INK,
                                    ),
                                    ft.Text(PROFILE_NAME, size=28, weight=ft.FontWeight.W_800, color=CYAN),
                                    ft.Text(PROFILE_ROLE, size=19, color=UNAM_GOLD, weight=ft.FontWeight.W_700),
                                    ft.Text(
                                        "",
                                        size=18,
                                        color=STEEL,
                                    ),
                                    ft.Row(
                                        [
                                            contact_button("Email Me", ft.Icons.EMAIL, open_email),
                                            ft.OutlinedButton(
                                                "GitHub",
                                                icon=ft.Icons.CODE,
                                                on_click=open_github,
                                                style=ft.ButtonStyle(
                                                    color=CYAN,
                                                    shape=ft.RoundedRectangleBorder(radius=8),
                                                ),
                                            ),
                                            ft.OutlinedButton(
                                                "About Me",
                                                icon=ft.Icons.PERSON,
                                                on_click=lambda _: show_page("about"),
                                                style=ft.ButtonStyle(
                                                    color=INK,
                                                    shape=ft.RoundedRectangleBorder(radius=8),
                                                ),
                                            ),
                                        ],
                                        spacing=12,
                                        wrap=True,
                                    ),
                                ],
                                spacing=14,
                            ),
                        ),
                        ft.Container(
                            col={"sm": 12, "md": 5},
                            content=ft.Column(
                                [
                                    profile_photo_slot(),
                                    card(
                                        ft.Column(
                                            [
                                                ft.Row(
                                                    [
                                                        ft.Icon(ft.Icons.SETTINGS, color=CYAN, size=36),
                                                        ft.Text("Engineering Focus Board", size=22, weight=ft.FontWeight.W_900, color=INK),
                                                    ],
                                                    spacing=10,
                                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                                ),
                                                ft.Text(
                                                    "Loads, energy, materials, motion, data, and documentation - presented through a clean Python interface with UNAM identity.",
                                                    color=STEEL,
                                                    size=16,
                                                ),
                                                ft.ResponsiveRow(
                                                    [
                                                        ft.Container(
                                                            col={"sm": 6, "md": 6},
                                                            content=ft.Container(
                                                                padding=12,
                                                                border_radius=8,
                                                                bgcolor=ft.Colors.with_opacity(0.12, color),
                                                                border=ft.Border.all(1, ft.Colors.with_opacity(0.30, color)),
                                                                content=ft.Column(
                                                                    [
                                                                        ft.Icon(icon, color=color, size=30),
                                                                        ft.Text(title, color=INK, weight=ft.FontWeight.W_800, size=15),
                                                                        ft.Text(detail, color=MUTED, size=12),
                                                                    ],
                                                                    spacing=5,
                                                                ),
                                                            ),
                                                        )
                                                        for title, detail, icon, color in electrical_focus
                                                    ],
                                                    spacing=10,
                                                    run_spacing=10,
                                                ),
                                            ],
                                            spacing=14,
                                        ),
                                        bgcolor="#101a2a",
                                    ),
                                ],
                                spacing=14,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                        ),
                    ],
                    spacing=20,
                    run_spacing=18,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ),
            ft.ResponsiveRow(
                [
                    ft.Container(
                        col={"sm": 12, "md": 6},
                        content=card(
                            ft.Column(
                                [
                                    ft.Icon(ft.Icons.PICTURE_AS_PDF, color=UNAM_RED, size=42),
                                    ft.Text("MATLAB Certificates", size=22, weight=ft.FontWeight.W_800, color=INK),
                                    ft.Text("Uploaded PDFs open from the certificate cards.", color=STEEL, size=16),
                                    ft.OutlinedButton("Open Certificates", icon=ft.Icons.SCHOOL, on_click=lambda _: show_page("matlab")),
                                ],
                                spacing=10,
                            )
                        ),
                    ),
                    ft.Container(
                        col={"sm": 12, "md": 6},
                        content=card(
                            ft.Column(
                                [
                                    ft.Icon(ft.Icons.CODE, color=UNAM_GOLD, size=42),
                                    ft.Text("GitHub", size=22, weight=ft.FontWeight.W_800, color=INK),
                                    ft.Text(PROFILE_GITHUB, color=STEEL, size=15),
                                    ft.OutlinedButton("Open GitHub", icon=ft.Icons.OPEN_IN_NEW, on_click=open_github),
                                ],
                                spacing=10,
                            )
                        ),
                    ),
                ],
                spacing=14,
                run_spacing=14,
            ),
        ]
    )

    about_page = page_shell(
        [
            unam_student_banner(),
            title_block("About Me", "A separate introduction to who I am and how I think."),
            card(
                ft.ResponsiveRow(
                    [
                        ft.Container(
                            col={"sm": 12, "md": 4},
                            content=ft.Column(
                                [about_photo_slot()],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                        ),
                        ft.Container(
                            col={"sm": 12, "md": 8},
                            content=ft.Column(
                                [
                                    ft.Text(PROFILE_NAME, size=28, weight=ft.FontWeight.W_900, color=INK),
                                    ft.Text(PROFILE_ROLE, size=18, color=UNAM_GOLD),
                                    ft.Text(
                                        "I am a second-year Electrical Engineering student at the University of Namibia with a strong interest in computer programming. I enjoy using code to make engineering work clearer: circuit calculations can be checked, signals can be visualised, and project progress can be documented in a way that is easy for other people to understand. Electrical engineering teaches me to think about circuits, signals, power, systems, and safety limits, while programming helps me turn those ideas into practical tools.",
                                        size=18,
                                        color=STEEL,
                                    ),
                                    ft.Text(
                                        "For this Computer Programming I portfolio, I am showing both sides of my learning: the engineering side, where formulas and systems matter, and the software side, where structure, navigation, evidence, and user experience matter. My goal is to become the kind of engineer who can solve technical problems and also build useful digital tools around them.",
                                        size=17,
                                        color=MUTED,
                                    ),
                                    ft.Row(
                                        [
                                            contact_button("Email", ft.Icons.EMAIL, open_email),
                                            ft.OutlinedButton("GitHub", icon=ft.Icons.CODE, on_click=open_github),
                                        ],
                                        spacing=12,
                                        wrap=True,
                                    ),
                                ],
                                spacing=14,
                            ),
                        ),
                    ],
                    spacing=14,
                    run_spacing=16,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor=SURFACE_3,
            ),
            title_block("Electrical Toolkit", "Engineering ideas I can connect to code."),
            ft.ResponsiveRow(
                [
                    ft.Container(
                        col={"sm": 12, "md": 6, "lg": 3},
                        content=card(
                            ft.Column(
                                [
                                    ft.Text(name, color=INK, size=20, weight=ft.FontWeight.W_800),
                                    ft.Container(
                                        content=ft.Text(formula, color=UNAM_GOLD, size=17, weight=ft.FontWeight.W_800),
                                        padding=10,
                                        bgcolor=UNAM_BLACK,
                                        border_radius=8,
                                        border=ft.Border.all(1, LINE),
                                    ),
                                    ft.Text(desc, color=MUTED, size=14),
                                ],
                                spacing=10,
                            )
                        ),
                    )
                    for name, formula, desc in formula_cards
                ],
                spacing=14,
                run_spacing=14,
            ),
        ]
    )



    # Get list of PDF certificates from the certificates folder
    certificates_dir = ASSETS_DIR / "certificates"
    pdf_files = sorted([f for f in certificates_dir.glob("*.pdf")])
    
    matlab_content = [
        title_block(
            "MATLAB Achievement Hub",
            f"{len(pdf_files)} certificate(s) completed" if pdf_files else "No MATLAB PDF certificates are present.",
        ),
    ]
    
    # Helper function to create open_pdf handler for each certificate
    def make_open_pdf_handler(pdf_path: str):
        async def open_pdf(_):
            # Build an absolute URL to the static asset so the browser
            # requests the PDF file directly instead of reloading the
            # app route. Open in a new browser tab (web_only_window_name)
            # and prefer opening inside the browser view.
            absolute_url = f"http://127.0.0.1:{APP_PORT}/{pdf_path}"
            await ft.UrlLauncher().launch_url(
                absolute_url,
                mode=ft.LaunchMode.IN_APP_BROWSER_VIEW,
                web_only_window_name="_blank",
            )
        return open_pdf
    
    # Add cards for each PDF certificate
    if pdf_files:
        for pdf_file in pdf_files:
            pdf_name = pdf_file.stem  # filename without .pdf extension
            rel_path = pdf_file.relative_to(BASE_DIR).as_posix()
            
            matlab_content.append(
                card(
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.DESCRIPTION, size=32, color=UNAM_GOLD),
                            ft.Column(
                                [
                                    ft.Text(pdf_name, size=18, weight=ft.FontWeight.W_700, color=INK),
                                    ft.Text(pdf_file.name, size=13, color=MUTED),
                                ],
                                spacing=4,
                                expand=True,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.OPEN_IN_NEW,
                                icon_color=PRIMARY,
                                tooltip="Open PDF",
                                url=asset_url(rel_path),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=12,
                    ),
                    padding=16,
                )
            )
    
    matlab_page = page_shell(matlab_content)

    blog_page = page_shell(
        [
            title_block(
                "Technical Blog: My contributions on OreGuide project",
                "Timoteus N Matheus- 225053055",
            ),
            card(
                ft.Column(
                    [
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Icon(
                                        ft.Icons.PLAY_CIRCLE_FILL,
                                        size=80,
                                        color=PRIMARY,
                                    ),
                                    ft.Text(
                                        "Watch Reflection Video",
                                        size=20,
                                        weight=ft.FontWeight.W_800,
                                        color=INK,
                                    ),
                                    ft.Text(
                                        "Click to open and play the reflection video in a new tab.",
                                        size=14,
                                        color=MUTED,
                                        text_align=ft.TextAlign.CENTER,
                                    ),
                                    ft.ElevatedButton(
                                        "Play Video",
                                        icon=ft.Icons.OPEN_IN_NEW,
                                        on_click=play_reflection_video,
                                        style=ft.ButtonStyle(
                                            color=BG,
                                            bgcolor=PRIMARY,
                                            shape=ft.RoundedRectangleBorder(radius=8),
                                        ),
                                    ),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=14,
                            ),
                            padding=40,
                            alignment=ft.Alignment(0, 0),
                            bgcolor=BG,
                            border_radius=8,
                            border=ft.Border.all(1, LINE),
                        ),
                        ft.Text("Reflection video", size=16, color=STEEL),
                    ],
                    spacing=12,
                ),
                padding=16,
            ),
        ]
    )

    github_page = page_shell(
        [
            unam_student_banner(),
            title_block(
                "GitHub Evidence & Documentation",
                "",
            ),
            ft.Row(
                [
                    ft.OutlinedButton("Open GitHub", icon=ft.Icons.OPEN_IN_NEW, on_click=open_github),
                    ft.OutlinedButton("Email Timoteus", icon=ft.Icons.EMAIL, on_click=open_email),
                ],
                spacing=12,
                wrap=True,
            ),
            card(
                ft.Column(
                    [
                        ft.Text("Contact Details", size=22, weight=ft.FontWeight.W_800, color=INK),
                        ft.Text(f"Email: {PROFILE_EMAIL}", size=16, color=STEEL),
                        ft.Text(f"GitHub: {PROFILE_GITHUB}", size=16, color=STEEL),
                    ],
                    spacing=8,
                )
            ),
        ]
    )

    pages = {
        "home": home_page,
        "about": about_page,
        "matlab": matlab_page,
        "blog": blog_page,
        "github": github_page,
    }

    page_host = ft.Container(expand=True, content=home_page, bgcolor=BG)
    nav_buttons = {}

    def nav_style(is_active: bool):
        return ft.ButtonStyle(
            color=UNAM_WHITE if is_active else STEEL,
            bgcolor=ft.Colors.with_opacity(0.24, CYAN) if is_active else ft.Colors.TRANSPARENT,
            shape=ft.RoundedRectangleBorder(radius=8),
            text_style=ft.TextStyle(size=15, weight=ft.FontWeight.W_700),
            padding=ft.Padding(left=12, top=13, right=12, bottom=13),
        )

    def set_nav_styles():
        for key, button in nav_buttons.items():
            button.style = nav_style(key == active_key)

    def show_page(key: str):
        nonlocal active_key
        active_key = key
        page_host.content = pages[key]
        set_nav_styles()
        page.update()

    def make_nav(label: str, key: str, icon: str):
        button = ft.TextButton(
            label,
            icon=icon,
            style=nav_style(key == active_key),
            on_click=lambda _, page_key=key: show_page(page_key),
        )
        nav_buttons[key] = button
        return button

    nav_items = [
        ("Home", "home", ft.Icons.HOME),
        ("About Me", "about", ft.Icons.PERSON),
        ("MATLAB", "matlab", ft.Icons.SCHOOL),
        ("Blog", "blog", ft.Icons.BOOK),
        ("GitHub", "github", ft.Icons.CODE),
    ]

    # Top horizontal navigation bar (replaces left sidebar)
    top_nav = ft.Container(
        padding=ft.Padding(left=14, top=8, right=14, bottom=8),
        bgcolor=ft.Colors.TRANSPARENT,
        content=ft.Row(
            [make_nav(label, key, icon) for label, key, icon in nav_items],
            alignment=ft.MainAxisAlignment.START,
            spacing=8,
        ),
    )

    # Master frame structure holding navigation and viewport layout content
    page.add(
        ft.Column(
            [
                top_nav,
                ft.Container(
                    content=page_host,
                    expand=True,
                    padding=ft.Padding(left=24, top=12, right=24, bottom=24),
                ),
            ],
            expand=True,
            spacing=0,
        )
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8554))
    ft.run(main, port=port, assets_dir=str(ASSETS_DIR))