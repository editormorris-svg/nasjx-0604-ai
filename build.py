#!/usr/bin/env python3
"""Generate language-specific static pages for nasjx.0604.ai."""
import re
from pathlib import Path

LANGS = {
    'en': {
        'html_lang': 'en',
        'title': 'Welcome to NAS Jiaxing',
        'description': 'Welcome to NAS Jiaxing — a learning community powered by safe, private AI.',
        'zyk_link': 'ZYK Website →',
    },
    'zh-cn': {
        'html_lang': 'zh-Hans',
        'title': '欢迎来到嘉兴诺安达学校',
        'description': '欢迎来到嘉兴诺安达学校——一个由安全、私密且合规的 AI 提供支持的学习社区。',
        'zyk_link': 'ZYK 官网 →',
    },
    'zh-hk': {
        'html_lang': 'zh-Hant',
        'title': '歡迎來到嘉興諾安達學校',
        'description': '歡迎來到嘉興諾安達學校——一個由安全、私密且合規的 AI 提供支援的學習社群。',
        'zyk_link': 'ZYK 官網 →',
    },
}

SOURCE = Path(__file__).parent / 'source.html'


def switcher(active: str) -> str:
    items = [
        ('en', 'English', 'EN'),
        ('zh-cn', 'Simplified Chinese', '简'),
        ('zh-hk', 'Traditional Chinese', '繁'),
    ]
    links = '\n          '.join(
        f'<a href="/{code}/" class="{"active" if code == active else ""}" aria-label="{label}">{text}</a>'
        for code, label, text in items
    )
    return (
        f'<div class="lang-switch" aria-label="Language switcher">\n          {links}\n        </div>'
    )


def alternates() -> str:
    base = 'https://nasjx.0604.ai'
    lines = [f'<link rel="alternate" hreflang="{code}" href="{base}/{code}/" />' for code in LANGS]
    lines.append(f'<link rel="alternate" hreflang="x-default" href="{base}/en/" />')
    return '\n  ' + '\n  '.join(lines)


def build_lang_page(lang: str, section: str) -> str:
    info = LANGS[lang]
    html = SOURCE.read_text(encoding='utf-8')

    # Replace CSS to style both buttons and anchor links in language switcher.
    html = html.replace('.lang-switch button {', '.lang-switch button,\n    .lang-switch a {')
    html = html.replace('.lang-switch button.active {', '.lang-switch button.active,\n    .lang-switch a.active {')

    # Update html lang, title, description.
    html = re.sub(r'<html lang="[^"]*">', f'<html lang="{info["html_lang"]}">', html, count=1)
    html = re.sub(r'<title>.*?</title>', f'<title>{info["title"]}</title>', html, count=1, flags=re.S)
    html = re.sub(
        r'(<meta name="description" content=")([^"]*)(" />)',
        rf'\g<1>{info["description"]}\3',
        html,
        count=1,
    )

    # Insert hreflang alternate links after the description meta tag.
    html = re.sub(
        r'(<meta name="description" content="[^"]*" />)',
        rf'\1\n  {alternates()}',
        html,
        count=1,
    )

    # Replace nav link to ZYK website.
    html = re.sub(
        r'(<a href="https://0604\.ai" class="nav-link"[^>]*>).*?(</a>)',
        rf'\g<1>{info["zyk_link"]}\2',
        html,
        count=1,
        flags=re.S,
    )

    # Replace language switcher with anchored version.
    html = re.sub(
        r'<div class="lang-switch" aria-label="Language switcher">.*?</div>',
        switcher(lang),
        html,
        count=1,
        flags=re.S,
    )

    # Normalize the section to be active and split it out.
    section = section.replace('class="lang-content"', 'class="lang-content active"', 1)

    # Replace everything inside <main> with just this language's section.
    html = re.sub(r'(<main>).*?(</main>)', rf'\1\n{section}\n</main>', html, count=1, flags=re.S)

    # Remove the language-switching script block; pages are now static per language.
    html = re.sub(r'<script>\s*\(function\s*\(\)\s*\{.*?\}\)\(\);\s*</script>', '', html, count=1, flags=re.S)

    return html


def build_redirect_page() -> str:
    return '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Welcome to NAS Jiaxing</title>
  <meta name="description" content="Welcome to NAS Jiaxing — a learning community powered by safe, private AI." />
  <link rel="alternate" hreflang="en" href="https://nasjx.0604.ai/en/" />
  <link rel="alternate" hreflang="zh-Hans" href="https://nasjx.0604.ai/zh-cn/" />
  <link rel="alternate" hreflang="zh-Hant" href="https://nasjx.0604.ai/zh-hk/" />
  <link rel="alternate" hreflang="x-default" href="https://nasjx.0604.ai/en/" />
  <script>
    (function () {
      var lang = navigator.language || navigator.userLanguage || 'en';
      if (lang.startsWith('zh')) {
        if (lang === 'zh-HK' || lang === 'zh-TW' || lang === 'zh-Hant') {
          window.location.replace('/zh-hk/');
        } else {
          window.location.replace('/zh-cn/');
        }
      } else {
        window.location.replace('/en/');
      }
    })();
  </script>
  <style>
    body { font-family: Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif; color: #1A1A2E; background: #F6F8FA; display: flex; align-items: center; justify-content: center; min-height: 100vh; margin: 0; text-align: center; }
    .box { background: #fff; padding: 2rem; border-radius: 1rem; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    h1 { font-size: 1.25rem; margin-bottom: 1rem; color: #0A2540; }
    a { color: #2D8A6E; text-decoration: none; font-weight: 600; }
    a:hover { text-decoration: underline; }
    ul { list-style: none; padding: 0; margin: 1rem 0 0; display: flex; gap: 1rem; justify-content: center; }
  </style>
</head>
<body>
  <div class="box">
    <h1>Welcome to NAS Jiaxing</h1>
    <p>Choose a language / 选择语言 / 選擇語言</p>
    <ul>
      <li><a href="/en/">English</a></li>
      <li><a href="/zh-cn/">简体中文</a></li>
      <li><a href="/zh-hk/">繁體中文</a></li>
    </ul>
  </div>
</body>
</html>
'''


def main() -> None:
    if not SOURCE.exists():
        raise SystemExit(f"Missing source file: {SOURCE}")

    source_text = SOURCE.read_text(encoding='utf-8')
    main_match = re.search(r'<main>(.*?)</main>', source_text, re.S)
    if not main_match:
        raise SystemExit("Could not find <main> content in source.html")

    main_content = main_match.group(1)
    # Split by language section comments.
    parts = re.split(r'<!--\s*(English|Simplified Chinese|Traditional Chinese)\s*-->\s*', main_content)
    # parts: ['', 'English', '<section...>', 'Simplified Chinese', ...]
    sections = {}
    for i in range(1, len(parts), 2):
        label = parts[i]
        section = parts[i + 1].strip()
        key = {'English': 'en', 'Simplified Chinese': 'zh-cn', 'Traditional Chinese': 'zh-hk'}[label]
        sections[key] = section

    root = Path(__file__).parent
    for lang, section in sections.items():
        page = build_lang_page(lang, section)
        out_dir = root / lang
        out_dir.mkdir(exist_ok=True)
        (out_dir / 'index.html').write_text(page, encoding='utf-8')
        print(f"Generated {lang}/index.html")

    (root / 'index.html').write_text(build_redirect_page(), encoding='utf-8')
    print("Generated root index.html (language redirect)")


if __name__ == '__main__':
    main()
