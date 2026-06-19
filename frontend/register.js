document.getElementById('registrationForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    // 1. Target form input elements dynamically using their correct field names
    // Note: If your HTML elements use different IDs, change these selector names to match.
    const fullNameElement = document.querySelector('input[placeholder="Adnan Ahmad Rana"]') || document.getElementById('name');
    const majorElement = document.querySelector('input[placeholder="Computer Science"]') || document.getElementById('major');
    const emailElement = document.querySelector('input[type="email"]') || document.getElementById('email');
    const passwordElement = document.querySelector('input[type="password"]') || document.getElementById('password');

    // 2. Safely capture input values
    const fullName = fullNameElement ? fullNameElement.value : '';
    const major = majorElement ? majorElement.value : '';
    const email = emailElement ? emailElement.value : '';
    const password = passwordElement ? passwordElement.value : '';

    // 3. Assemble the request object payload
    // CRITICAL FIX: We map 'fullName' to the key 'username' so Pydantic validation passes!
    const payload = {
        username: fullName,
        email: email,
        password: password,
        major: major,
        year: 1,           // Default numeric values for schema compatibility
        subjects: [],      // Default array value
        bio: ""            // Default text string field
    };

    try {
        // 4. Send request string to the modern backend auth endpoint
        const response = await fetch('/api/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (response.ok || response.status === 201) {
            alert('Registration complete! Account created successfully.');
            // Route user smoothly to the sign-in index or login portal layout
            window.location.href = '/';
        } else {
            // Handle structured Pydantic array validation feedback elegantly
            if (Array.isArray(data.detail)) {
                const errorText = data.detail.map(err => `${err.loc[1] || err.loc[0]}: ${err.msg}`).join('\n');
                alert(`Validation Failed:\n${errorText}`);
            } else {
                alert(`Error: ${data.detail || 'Could not verify registry parameters.'}`);
            }
        }
    } catch (error) {
        console.error('Submission synchronization exception intercepted:', error);
        alert('Network anomaly encountered connecting to backend API engine.');
    }
});
