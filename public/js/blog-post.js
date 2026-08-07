async function loadPost() {
    const article = document.getElementById("article");
    const params = new URLSearchParams(window.location.search);
    const id = params.get("id");

    try {
        const response = await fetch("data/blog-posts.json", { cache: "no-store" });
        if (!response.ok) throw new Error("Unable to load this post.");

        const posts = await response.json();
        const post = posts.find(item => item.id === id);

        if (!post) throw new Error("Blog post not found.");

        const formattedDate = new Date(post.date + "T12:00:00").toLocaleDateString(
            "en-US",
            { year: "numeric", month: "long", day: "numeric" }
        );

        document.title = `${post.title} | Ada Forge Books`;

        article.innerHTML = `
            <p class="eyebrow">${post.category}</p>
            <p class="date">${formattedDate}</p>
            <h1>${post.title}</h1>
            ${post.image ? `<img class="article-image" src="${post.image}" alt="">` : ""}
            <div class="article-body">
                ${post.body.map(paragraph => `<p>${paragraph}</p>`).join("")}
            </div>

            <div class="actions article-actions">
                ${post.bookLink ? `<a class="button primary" href="${post.bookLink}">${post.bookLinkText || "Learn More"}</a>` : ""}
                <button id="share-facebook" class="share-button">Share on Facebook</button>
                <a class="button" href="blog.html">← Back to Blog</a>
            </div>
        `;

        document.getElementById("share-facebook").addEventListener("click", () => {
            window.open(
                "https://www.facebook.com/sharer/sharer.php?u=" + encodeURIComponent(window.location.href),
                "facebook-share",
                "width=700,height=600,resizable=yes,scrollbars=yes"
            );
        });

    } catch (error) {
        article.innerHTML = `<p class="error">${error.message}</p><p><a href="blog.html">Return to Blog</a></p>`;
    }
}

loadPost();

 
