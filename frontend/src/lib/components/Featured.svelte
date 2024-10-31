<script>
    // Add dynamic functionality here if needed, such as fetching featured items from an API.
</script>

<style>
    .featured-container {
        max-width: 1000px;
        margin: 0 auto;
        padding: 2rem;
        padding-top: 100px;
        text-align: center;
        color: #333;
    }

    .header-title {
        font-size: 2.5rem;
        font-weight: 600;
        color: #333;
    }

    .description {
        font-size: 1.125rem;
        margin-top: 1rem;
        color: #555;
    }

    .featured-list {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 1.5rem;
        margin-top: 2rem;
    }

    .featured-card {
        background-color: #fff;
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        max-width: 300px;
        text-align: left;
        transition: transform 0.2s ease-in-out;
    }

    .featured-card:hover {
        transform: translateY(-5px);
    }

    .featured-image {
        width: 100%;
        height: auto;
        border-radius: 6px;
    }

    .featured-title {
        font-size: 1.25rem;
        font-weight: 600;
        margin-top: 1rem;
        color: #333;
    }

    .featured-description {
        font-size: 0.9rem;
        color: #777;
        margin-top: 0.5rem;
    }

    .featured-link {
        font-size: 0.9rem;
        color: #4A90E2;
        font-weight: 500;
        margin-top: 0.75rem;
        display: inline-block;
        text-decoration: none;
    }

    .featured-link:hover {
        text-decoration: underline;
    }
</style>

<div class="featured-container">
    <h1 class="header-title">Featured Highlights</h1>
    <p class="description">
        Discover some of our most innovative projects and case studies that showcase the capabilities of TopicNet.
    </p>

    <div class="featured-list">
        <div class="featured-card">
            <img src="parse.svg" alt="Project Image" class="featured-image">
            <h3 class="featured-title">AI-Powered Document Parsing</h3>
            <p class="featured-description">
                Leveraging advanced AI, we transformed complex documents into interactive insights for leading
                enterprises.
            </p>
            <a href="/case-study/ai-document-parsing" class="featured-link">Read More</a>
        </div>

        <div class="featured-card">
            <img src="/image.png" alt="Project Image" class="featured-image">
            <h3 class="featured-title">Real-Time Visualization Dashboard</h3>
            <p class="featured-description">
                Developed a real-time, interactive dashboard for financial data, enhancing decision-making for clients.
            </p>
            <a href="/case-study/real-time-dashboard" class="featured-link">Read More</a>
        </div>

        <div class="featured-card">
            <img src="/security.png" alt="Project Image" class="featured-image">
            <h3 class="featured-title">Secure Data Management Solution</h3>
            <p class="featured-description">
                Implemented a secure data solution that ensures data privacy and compliance for healthcare providers.
            </p>
            <a href="/case-study/secure-data-management" class="featured-link">Read More</a>
        </div>
        
        <!-- Add more featured items as needed -->
    </div>
</div>
