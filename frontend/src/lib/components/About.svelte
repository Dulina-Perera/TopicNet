<script>
    
</script>

<style>
    .about-container {
        max-width: 900px;
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

    .team-section {
        margin-top: 2rem;
    }

    .team-header {
        font-size: 2rem;
        font-weight: 500;
        color: #333;
        margin-bottom: 1.5rem;
    }

    .team-members {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 1.5rem;
    }

    .team-member {
        background-color: #fff;
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        max-width: 200px;
        text-align: center;
    }

    .team-member img {
        width: 100%;
        height: auto;
        border-radius: 50%;
    }

    .member-name {
        font-size: 1.125rem;
        font-weight: 600;
        margin-top: 0.5rem;
        color: #333;
    }

    .member-role {
        font-size: 0.9rem;
        color: #777;
    }

    .mission-section {
        background: linear-gradient(to bottom, #f0f0f5, #fff);
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    }
</style>

<div class="about-container">
    <h1 class="header-title">About Us</h1>
    <p class="description">
        At TopicNet, we are dedicated to transforming unstructured data into structured insights that drive decisions.
        Our mission is to empower individuals and businesses to visualize, explore, and understand complex information
        effortlessly.
    </p>

    <div class="mission-section">
        <h2 class="team-header">Our Mission</h2>
        <p>
            We believe in the power of knowledge and visualization. Our goal is to create tools that make information
            accessible, interactive, and useful, enabling our users to make data-driven decisions and discover
            new perspectives on their information.
        </p>
    </div>

    <div class="team-section">
        <h2 class="team-header">Meet Our Team</h2>
        <div class="team-members">
            <div class="team-member">
                <img src="/profile.png" alt="Team Member">
                <h3 class="member-name">Dulina Perera</h3>
            </div>
            <div class="team-member">
                <img src="/profile.png" alt="Team Member">
                <h3 class="member-name">Tithira Perera</h3>
            </div>
            <div class="team-member">
                <img src="/profile.png" alt="Team Member">
                <h3 class="member-name">Thiwanka Pathirana</h3>
            </div>
            <!-- Add more team members as needed -->
        </div>
    </div>
</div>
