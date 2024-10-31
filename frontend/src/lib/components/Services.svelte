<script>
    // Add any functionality for dynamic data here if needed, such as fetching services from an API.
</script>

<style>
    .services-container {
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

    .services-list {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 1.5rem;
        margin-top: 2rem;
    }

    .service-card {
        background-color: #fff;
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        max-width: 280px;
        text-align: left;
        transition: transform 0.2s ease-in-out;
    }

    .service-card:hover {
        transform: translateY(-5px);
    }

    .service-icon {
        font-size: 3rem;
        color: #4A90E2;
        margin-bottom: 1rem;
    }

    .service-title {
        font-size: 1.25rem;
        font-weight: 600;
        margin-top: 0.5rem;
        color: #333;
    }

    .service-description {
        font-size: 0.9rem;
        color: #777;
        margin-top: 0.5rem;
    }
</style>

<div class="services-container">
    <h1 class="header-title">Our Services</h1>
    <p class="description">
        At TopicNet, we offer a range of services designed to help you turn your data into meaningful insights. Explore
        our offerings below.
    </p>

    <div class="services-list">
        <div class="service-card">
            <div class="service-icon">📄</div>
            <h3 class="service-title">Document Analysis</h3>
            <p class="service-description">
                We process and analyze unstructured documents, turning complex text data into structured insights for
                easy understanding and action.
            </p>
        </div>
        <div class="service-card">
            <div class="service-icon">🧠</div>
            <h3 class="service-title">Mindmap Generation</h3>
            <p class="service-description">
                Our advanced tools automatically generate mindmaps from your documents, making it easy to visualize
                relationships and concepts.
            </p>
        </div>
        <div class="service-card">
            <div class="service-icon">📊</div>
            <h3 class="service-title">Data Visualization</h3>
            <p class="service-description">
                We offer a variety of customizable visualization tools to present your data in a clear, interactive way,
                suitable for analysis and presentations.
            </p>
        </div>
        <div class="service-card">
            <div class="service-icon">🔒</div>
            <h3 class="service-title">Secure Storage</h3>
            <p class="service-description">
                With top-notch security measures, we ensure your data is safely stored, encrypted, and easily accessible
                only to you.
            </p>
        </div>
    </div>
</div>
