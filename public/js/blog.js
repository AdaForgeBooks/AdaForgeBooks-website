async function loadPosts() {
    const grid = document.getElementById("post-grid");

    try {
        const response = await fetch("data/blog-posts.json", { cache: "no-store" });
        if (!response.ok) throw new Error("Unable to load blog posts.");

        const posts = await response.json();

        posts.sort((a, b) => new Date(b.date) - new Date(a.date));

        grid.innerHTML = "";

        posts.forEach(post => {
            const article = document.createElement("article");
            article.className = "post-card";

            const formattedDate = new Date(post.date + "T12:00:00").toLocaleDateString(
                "en-US",
                { year: "numeric", month: "long", day: "numeric" }
            );

            article.innerHTML = `
                ${post.image ? `<img class="post-image" src="${post.image}" alt="">` : ""}
                <div class="post-card-body">
                    <p class="category">${post.category}</p>
                    <p class="date">${formattedDate}</p>
                    <h3>${post.title}</h3>
                    <p>${post.excerpt}</p>
                    <div class="actions">
                        <a class="read-more" href="blog-post.html?id=${encodeURIComponent(post.id)}">Read Full Post →</a>
                        <button class="share-button" data-id="${post.id}">Share on Facebook</button>
                    </div>
                </div>
            `;

            grid.appendChild(article);
        });

        document.querySelectorAll(".share-button").forEach(button => {
            button.addEventListener("click", () => {
                const postUrl = new URL(
                    `blog-post.html?id=${encodeURIComponent(button.dataset.id)}`,
                    window.location.href
                ).href;

                window.open(
                    "https://www.facebook.com/sharer/sharer.php?u=" + encodeURIComponent(postUrl),
                    "facebook-share",
                    "width=700,height=600,resizable=yes,scrollbars=yes"
                );
            });
        });

    } catch (error) {
        grid.innerHTML = `<p class="error">${error.message}</p>`;
    }
}

loadPosts();
