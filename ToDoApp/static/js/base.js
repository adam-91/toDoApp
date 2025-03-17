function validateEmail(input) {
    const value = input.value
    const emailError = document.getElementById("emailError");
    const regex = /[a-zA-Z0-9._%+\-]+@+[a-z0-9.\-]+\.[a-z]{2,}/
    if (!value || !value.match(regex) ) {
        emailError.textContent = "Wrong email adress";
        emailError.className =  "visible"
        input.className ="form-control error"
        return 1
    } else {
        emailError.textContent = "";
        emailError.className =  "invisible"
        input.className ="form-control"
        return 0
    }
};

function validateLogin(input) {
    const value = input.value
    const loginError = document.getElementById("loginError");
    if (!value || value.length < 3) {
        console.log(value.length)
        loginError.textContent = "Wrong login, minimum lenght 3";
        loginError.className =  "visible"
        input.className ="form-control error"
    } else {
        loginError.textContent = "";
        loginError.className =  "invisible"
        input.className ="form-control"
    }
};
function validateName(input) {
    const value = input.value
    const nameError = document.getElementById("nameError");
    if (!value ||value.length < 3) {
        nameError.textContent = "Wrong name, minimum lenght 3";
        nameError.className =  "visible"
        input.className ="form-control error"
    } else {
        nameError.textContent = "";
        nameError.className =  "invisible"
        input.className ="form-control"
    }
};

function validateSurname(input) {
    const value = input.value
    const surnameError = document.getElementById("surnameError");
    if (!value || value.length < 3) {
        surnameError.textContent = "Wrong surname, minimum lenght 3";
        surnameError.className =  "visible"
        input.className ="form-control error"
    } else {
        surnameError.textContent = "";
        surnameError.className =  "invisible"
        input.className ="form-control"
    }
};

function validatePhone(input) {
    const value = input.value
    const phoneError = document.getElementById("phoneError");
    const regex = /[+][0-9]{2}[0-9]?[0-9]{9}/
    const formatedPhone = value.replace(/[ \-\/]/g, '')
    console.log('phone: ', formatedPhone, value)
    if (!value || !formatedPhone.match(regex) ) {
        phoneError.textContent = "wrong phone number, proper format: +48(X?) XXX XXX XXX";
        phoneError.className =  "visible"
        input.className ="form-control error"
    } else {
        phoneError.textContent = "";
        phoneError.className =  "invisible"
        input.className ="form-control"
    }
};

function validatePassword(input) {
    const value = input.value
    const passwordError = document.getElementById("passwordError");
    const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*<>?])([A-Za-z\d@#$%^&*<>?]){8,}$/
    if (!value || !value.match(regex) ) {
        passwordError.innerHTML = "Wrong password, should be: at least 8 characters long,<br/>Contains at least one lowercase letter<br/>Contains at least one uppercase letter<br/>Contains at least one number<br/>Contains at least one special character (!, @, #, $, %, ^, &, *, <, >, ?)";
        passwordError.className =  "visible"
        input.className ="form-control error"
    } else {
        passwordError.innerHTML = "";
        passwordError.className =  "invisible"
        input.className ="form-control"
    }
};

function logout() {
    const cookies = document.cookie.split(";");

    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i];
        const eqPos = cookie.indexOf("=");
        const name = eqPos > -1 ? cookie.substring(0, eqPos) : cookie;
        document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/";
    }

    // Redirect to the login page
    window.location.href = '/auth/login-page';
};

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
        let isValid = true;
        const email = document.getElementById("email").value;

        const emailError = document.getElementById("emailError");
        const regex = /[a-zA-Z0-9._%+\-]+@+[a-z0-9.\-]+\.[a-z]{2,}/
        if (!email || !email.match(regex) ) {
          emailError.textContent = "Wrong email adress";
          emailError.className =  "visible"
          email.className ="form-control error"
          isValid = false;
        } else {
            console.log('ok')
          emailError.textContent = "";
          emailError.className="invisible"
        }

        const form = event.target
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        if (data.password !== data.password2) {
            alert("Passwords don't match");
            return;
        }

        if (!isValid) {
            return
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

const goRregisterBtn = document.getElementById('goRegisterBtn');
if (goRregisterBtn) {
    goRregisterBtn.addEventListener('click', async function (event) {
        event.preventDefault();
    
        window.location.href = '/auth/register-page';
    });
};

const goLoginBtn= document.getElementById('goLoginBtn');
if (goLoginBtn) {
    goLoginBtn.addEventListener('click', async function (event) {
        event.preventDefault();
    
        window.location.href = '/auth/login-page';
    });
};


