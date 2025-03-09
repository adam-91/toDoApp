//login
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const form = event.target
        const formData = new FormData(form);

        const payload = new URLSearchParams();
        for (const [key, value] of formData.entries()) {
            payload.append(key, value);
        }

        try {
            const response = await fetch('/auth/token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: payload.toString()
            });

            if (response.ok) {
                const data = await response.json();
                // cookie: delete old one
                logout();
                // cookie: save token 
                document.cookie = `access_token=${data.access_token}; path=/`;
                window.location.href = '/activities/activity-page';
            } else {
                const errorData = await response.json();
                console.error('Error:', errorData);
                //alert(`Error: ${errorData.detail}`);
            }
        } catch (error) {
            console.error('Error:', error);
            //alert('An error occurred. Please try again.');
        }

    });
}

//registration
const registerForm = document.getElementById('registerForm');
if (registerForm) {
    registerForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const form = event.target
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        if (data.password !== data.password2) {
            alert("Passwords don't match");
            return;
        }

        const payload = {
            login: data.login,
            email: data.email,
            name: data.name,
            second_name: data.secondname,
            surname: data.surname,
            phone: data.phone,
            password: data.password
        };

        try {   
            const response = await fetch('/auth', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                window.location.href = '/auth/login-page';
            } else {
                const errorData = await response.json();
                const errorMessage = JSON.stringify(errorData.detail)
                alert(errorMessage);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        };
    });
}

function logout() {
    const cookies = document.cookie.split(";");

    // clear cookes
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i];
        const eqPos = cookie.indexOf("=");
        const name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
        document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/";
    }

    window.location.href = '/auth/login-page';
};