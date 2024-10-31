<script>
    let name = '';
    let email = '';
    let message = '';

    const handleSubmit = (event) => {
        event.preventDefault();
        // Here, you can add functionality to handle form submission, such as sending the data to your backend.
        alert('Thank you for reaching out! We will get back to you soon.');
        
        // Reset form fields
        name = '';
        email = '';
        message = '';
    };
</script>

<style>
    .contact-container {
        max-width: 800px;
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

    .form-container {
        margin-top: 2rem;
        background-color: #fff;
        padding: 2rem;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        max-width: 600px;
        margin: auto;
    }

    .form-field {
        width: 100%;
        margin-bottom: 1.5rem;
    }

    .form-label {
        display: block;
        font-weight: 500;
        margin-bottom: 0.5rem;
        color: #333;
    }

    .form-input, .form-textarea {
        width: 100%;
        padding: 0.75rem;
        font-size: 1rem;
        border: 1px solid #ccc;
        border-radius: 4px;
    }

    .form-textarea {
        resize: vertical;
        height: 120px;
    }

    .submit-button {
        background-color: #4A90E2;
        color: #fff;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.2s ease-in-out;
    }

    .submit-button:hover {
        background-color: #357ABD;
    }

    .contact-info {
        margin-top: 2rem;
        font-size: 1rem;
        color: #555;
    }
</style>

<div class="contact-container">
    <h1 class="header-title">Contact Me</h1>
    <p class="description">
        Feel free to reach out with any questions, collaboration ideas, or just to say hello! Fill out the form below or
        use the contact information provided.
    </p>

    <div class="form-container">
        <form on:submit={handleSubmit}>
            <div class="form-field">
                <label class="form-label" for="name">Name</label>
                <input class="form-input" type="text" id="name" bind:value={name} required>
            </div>

            <div class="form-field">
                <label class="form-label" for="email">Email</label>
                <input class="form-input" type="email" id="email" bind:value={email} required>
            </div>

            <div class="form-field">
                <label class="form-label" for="message">Message</label>
                <textarea class="form-textarea" id="message" bind:value={message} required></textarea>
            </div>

            <button type="submit" class="submit-button">Send Message</button>
        </form>
    </div>

    <div class="contact-info">
        <p>Email: contact@topicnet.com</p>
        <p>Phone: +1 (123) 456-7890</p>
        <p>Address: 1234 Elm Street, Anytown, ST 12345</p>
    </div>
</div>
