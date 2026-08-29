from pathlib import Path
import json
import html

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
DATA = PUBLIC / "data" / "blog-posts.json"
BLOG_DIR = PUBLIC / "blog"

SITE = "https://adaforgebooks.net"
DEFAULT_IMAGE = f"{SITE}/images/homepage/ada-forge-logo.png"

with DATA.open(encoding="utf-8") as f:
    posts = json.load(f)

BLOG_DIR.mkdir(parents=True, exist_ok=True)

for post in posts:
    slug = post["id"]
    page_dir = BLOG_DIR / slug
    page_dir.mkdir(parents=True, exist_ok=True)

    title = post["title"]
    excerpt = post["excerpt"]
    category = post.get("category", "News")
    date = post["date"]

    image = post.get("image", "").strip()

    if image:
        if image.startswith("http://") or image.startswith("https://"):
            og_image = image
        else:
            og_image = SITE + "/" + image.lstrip("/")
    else:
        og_image = DEFAULT_IMAGE

    canonical = f"{SITE}/blog/{slug}/"

    paragraphs = "\n".join(
        f"<p>{html.escape(paragraph)}</p>"
        for paragraph in post.get("body", [])
    )

    book_button = ""
    if post.get("bookLink"):
        text = html.escape(post.get("bookLinkText") or "Learn More")
        link = html.escape(post["bookLink"], quote=True)
        book_button = f'<a class="button primary" href="{link}">{text}</a>'

    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>{html.escape(title)} | Ada Forge Books</title>

    <meta name="description" content="{html.escape(excerpt, quote=True)}">

    <link rel="canonical" href="{canonical}">

    <meta property="og:type" content="article">
    <meta property="og:title" content="{html.escape(title, quote=True)}">
    <meta property="og:description" content="{html.escape(excerpt, quote=True)}">
    <meta property="og:image" content="{html.escape(og_image, quote=True)}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:site_name" content="Ada Forge Books">

    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{html.escape(title, quote=True)}">
    <meta name="twitter:description" content="{html.escape(excerpt, quote=True)}">
    <meta name="twitter:image" content="{html.escape(og_image, quote=True)}">

    <link rel="stylesheet" href="/css/blog.css">
    <link rel="stylesheet" href="/css/footer.css">
</head>

<body>

<header class="site-header">
    <a class="brand" href="/">
        <img src="/images/blog/ada-forge-logo.png" alt="Ada Forge Books">
        <span>Ada Forge Books</span>
    </a>

    <nav>
        <a href="/">Home</a>
        <a href="/books/">Books</a>
        <a href="/about/">About</a>
        <a href="/blog.html">Blog</a>

        <a class="buy-now"
           href="https://www.amazon.com/stores/Todd-Thorne/author/B0FC8KB4LV"
           target="_blank"
           rel="noopener noreferrer">
            Amazon Store
        </a>
    </nav>
</header>

<main>
<section class="article-shell">
    <article class="full-post">

        <p class="eyebrow">{html.escape(category)}</p>

        <p class="date">
            <time datetime="{html.escape(date)}">{html.escape(date)}</time>
        </p>

        <h1>{html.escape(title)}</h1>

        {"<img class='article-image' src='" + html.escape(post['image'], quote=True) + "' alt='" + html.escape(title, quote=True) + "'>" if post.get("image") else ""}

        <div class="article-body">
            {paragraphs}
        </div>

        <div class="actions article-actions">
            {book_button}

            <button
                class="share-button"
                onclick="window.open(
                    'https://www.facebook.com/sharer/sharer.php?u=' +
                    encodeURIComponent('{canonical}'),
                    'facebook-share',
                    'width=700,height=600,resizable=yes,scrollbars=yes'
                )">
                Share on Facebook
            </button>

            <a class="button" href="/blog.html">← Back to Blog</a>
        </div>

    </article>
</section>
</main>

<footer class="site-footer">
    <div class="footer-brand">
        <strong>Ada Forge Books</strong>
        <span>Stories by Todd Thorne</span>
    </div>

    <nav class="footer-navigation" aria-label="Footer navigation">
        <a href="/">Home</a>
        <a href="/books/">Books</a>
        <a href="/about/">About</a>
        <a href="/blog.html">Blog</a>

        <a href="https://www.goodreads.com/author/show/71901585.Todd_Thorne"
           target="_blank"
           rel="noopener noreferrer">
            Goodreads
        </a>

        <a href="https://www.amazon.com/stores/Todd-Thorne/author/B0FC8KB4LV"
           target="_blank"
           rel="noopener noreferrer">
            Amazon Store
        </a>
    </nav>

    <p class="footer-copyright">
        © 2026 Todd Thorne · Ada Forge Books
    </p>
</footer>

</body>
</html>
'''

    output = page_dir / "index.html"
    output.write_text(page, encoding="utf-8")

    print("GENERATED:", output)

print()
print(f"Generated {len(posts)} blog pages.")
