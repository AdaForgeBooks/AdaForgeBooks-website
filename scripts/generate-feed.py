from pathlib import Path
import json
import html
from datetime import datetime, timezone
from email.utils import format_datetime

posts = json.loads(Path("public/data/blog-posts.json").read_text(encoding="utf-8"))

site = "https://adaforgebooks.net"
blog = site + "/blog.html"
feed = site + "/feed.xml"

items = []

for post in posts:
    title = html.escape(post.get("title", "Ada Forge Books"))
    description = html.escape(post.get("excerpt", ""))
    post_id = post.get("id", "")
    link = site + "/blog-post.html?id=" + post_id

    try:
        dt = datetime.strptime(post.get("date", ""), "%Y-%m-%d").replace(tzinfo=timezone.utc)
        pubdate = format_datetime(dt)
    except ValueError:
        pubdate = format_datetime(datetime.now(timezone.utc))

    content = "".join(
        "<p>" + html.escape(paragraph) + "</p>"
        for paragraph in post.get("body", [])
    )

    items.append(f"""
    <item>
        <title>{title}</title>
        <link>{html.escape(link)}</link>
        <guid isPermaLink="true">{html.escape(link)}</guid>
        <pubDate>{pubdate}</pubDate>
        <description>{description}</description>
        <content:encoded><![CDATA[{content}]]></content:encoded>
    </item>""")

rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
     xmlns:content="http://purl.org/rss/1.0/modules/content/">
<channel>
<title>Ada Forge Books | Todd Thorne</title>
<link>{blog}</link>
<description>News, books, writing updates and behind-the-scenes stories from author Todd Thorne and Ada Forge Books.</description>
<language>en-us</language>
<lastBuildDate>{format_datetime(datetime.now(timezone.utc))}</lastBuildDate>
<atom:link xmlns:atom="http://www.w3.org/2005/Atom" href="{feed}" rel="self" type="application/rss+xml" />
{"".join(items)}
</channel>
</rss>
"""

Path("public/feed.xml").write_text(rss, encoding="utf-8")

print("RSS feed updated.")
print("Posts:", len(posts))
