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
       
        loginError.textContent = "Wrong login, minimum lenght 3";
        loginError.className =  "visible"
        input.className ="form-control error"
        return 1
    } else {
        loginError.textContent = "";
        loginError.className =  "invisible"
        input.className ="form-control"
        return 0
    }
};
function validateName(input) {
    const value = input.value
    const nameError = document.getElementById("nameError");
    if (!value || value.length < 3) {
        nameError.textContent = "Wrong name, minimum lenght 3";
        nameError.className =  "visible"
        input.className ="form-control error"
        return 1
    } else {
        nameError.textContent = "";
        nameError.className =  "invisible"
        input.className ="form-control"
        return 0
    }
};

function validateSurname(input) {
    const value = input.value
    const surnameError = document.getElementById("surnameError");
    if (!value || value.length < 3) {
        surnameError.textContent = "Wrong surname, minimum lenght 3";
        surnameError.className =  "visible"
        input.className ="form-control error"
        return 1
    } else {
        surnameError.textContent = "";
        surnameError.className =  "invisible"
        input.className ="form-control"
        return 0
    }
};

function validatePhone(input) {
    const value = input.value
    const phoneError = document.getElementById("phoneError");
    const regex = /[+][0-9]{2}[0-9]?[0-9]{9}/
    const formatedPhone = value.replace(/[ \-\/]/g, '')
   
    if (!value || !formatedPhone.match(regex) ) {
        phoneError.textContent = "wrong phone number, proper format: +48(X?) XXX XXX XXX";
        phoneError.className =  "visible"
        input.className ="form-control error"
        return 1
    } else {
        phoneError.textContent = "";
        phoneError.className =  "invisible"
        input.className ="form-control"
        return 0
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
        return 1
    } else {
        passwordError.innerHTML = "";
        passwordError.className =  "invisible"
        input.className ="form-control"
        return 0
    }
};

function validatePassword2(input) {
    const value2 = input.value
    const value = document.getElementById("rEmail").value;
    const password2Error = document.getElementById("password2Error");

    if (value != value2) {
        password2Error.innerHTML = "Password and veryfy password are not match";
        password2Error.className =  "visible"
        input.className ="form-control error"
        return 1
    } else {
        password2Error.innerHTML = "";
        password2Error.className =  "invisible"
        input.className ="form-control"
        return 0
    }
};

function validateNameLength(input) {
    const value = input.value
    const nameError = document.getElementById("nameError");
    if (!value || value.length < 3) {
        nameError.textContent = "To short, minimum lenght 3";
        nameError.className =  "visible"
        input.className ="form-control error"
        return 1
    } else {
        nameError.textContent = "";
        nameError.className =  "invisible"
        input.className ="form-control"
        return 0
    }
};

function validateActivityName(input) {
    //dorobic sprawdzanie czy juz taka istnieje
    const value = input.value
    const nameError = document.getElementById("nameError");
    if (!value || value.length < 3) {
        nameError.textContent = "To short, minimum lenght 3";
        nameError.className =  "visible"
        input.className ="form-control error"
        return 1
    } else {
        nameError.textContent = "";
        nameError.className =  "invisible"
        input.className ="form-control"
        return 0
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
    window.location.href = '/auth/login-page';
};

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
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

                logout();

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

        const validEmail = validateEmail(data.email);
        const validLogin = validateLogin(data.login);
        const valideName = validateName(data.name);
        const validSurname = validateSurname(data.surname);
        const validPhone = validateSurname(data.phone);
        const validPassword = validateSurname(data.password); 
        const validPassword2 = validateSurname(data.password2); 
        
        if (validPassword2 == 0 || validEmail == 0 || validLogin == 0 || valideName == 0 || validSurname == 0 || validPhone == 0 || validPassword == 0) {
            return
        };

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

//add new category
const categoriesForm = document.getElementById('categoriesForm');
if (categoriesForm) {
    categoriesForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const form = event.target
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        const level = Number(data.level)
        const payload = {
            name: data.category,
            description: data.description,
            level: level,
            active: 'True',
            picture: 'string'
        };
        
        try {   
            const token = getCookie('access_token');
            if (!token) {
                throw new Error('Authentication token not found');
            }
            
            const response = await fetch('/categories', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });
             document.cookie = `access_token=${data.access_token}; path=/`

            if (response.ok) {
                //const data = await response.text();
            } else {
                const errorData = response.text()
                const errorMessage = JSON.stringify(errorData.detail)
                alert(errorMessage);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        };
    });
}


//add new type
const typesForm = document.getElementById('typesForm');
if (typesForm) {
    typesForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const form = event.target
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        const payload = {
            name: data.type,
            description: data.description,
            active: 'True'
        };

        try {   
            const token = getCookie('access_token');
            if (!token) {
                throw new Error('Authentication token not found');
            }
            
            const response = await fetch('/types', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });
             document.cookie = `access_token=${data.access_token}; path=/`

            if (response.ok) {
                //const data = await response.text();
            } else {
                const errorData = response.text()
                const errorMessage = JSON.stringify(errorData.detail)
                alert(errorMessage);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        };
    });
}

//add new activity
const activitiesForm = document.getElementById('activitiesForm');
if (activitiesForm) {
    activitiesForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const form = event.target
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        let type_id = document.getElementById('Types input list');
        let selectedOption = type_id.options[type_id.selectedIndex];
        type_id = selectedOption.value;
        let category_id = document.getElementById('Categories input list');
        selectedOption = category_id.options[category_id.selectedIndex];
        category_id = selectedOption.value;

        const payload = {
            name: data.activity,
            description: data.description,
            active: 'True',
            progress: 0,
            priority: data.priorities,
            category_id: category_id,
            type_id: type_id
        };
            alert( JSON.stringify(payload))
        try {   
            const token = getCookie('access_token');
            if (!token) {
                throw new Error('Authentication token not found');
            }
            
            const response = await fetch('/activities/activity', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });
             document.cookie = `access_token=${data.access_token}; path=/`

            if (response.ok) {
                //const data = await response.text();
            } else {
                const errorData = response.text()
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

const goLoginBtn = document.getElementById('goLoginBtn');
if (goLoginBtn) {
    goLoginBtn.addEventListener('click', async function (event) {
        event.preventDefault();
    
        window.location.href = '/auth/login-page';
    });
};

const goAddActivityBtn = document.getElementById('addActivityBtn');
if (goAddActivityBtn) {
    goAddActivityBtn.addEventListener('click', async function (event) {
        event.preventDefault();

        const token = getCookie('access_token');
        if (!token) {
            throw new Error('Authentication token not found');
        }

       
        document.cookie = `access_token=${token}; path=/`
        
        window.location.href = '/activities/add-page';
    });
};

const goAddACategoryBtn = document.getElementById('addCategoryBtn');
if (goAddACategoryBtn) {
    goAddACategoryBtn.addEventListener('click', async function (event) {
        event.preventDefault();
    
        window.location.href = '/categories/add-page';
    });
};

const goAddTypeBtn = document.getElementById('addTypeBtn');
if (goAddTypeBtn) {
    goAddTypeBtn.addEventListener('click', async function (event) {
        event.preventDefault();
    
        window.location.href = '/types/add-page';
    });
};

const goToActivitiesBtn = document.getElementById('goToActivitiesBtn');
if (goToActivitiesBtn) {
    goToActivitiesBtn.addEventListener('click', async function (event) {
        event.preventDefault();

        const token = getCookie('access_token');
        if (!token) {
            throw new Error('Authentication token not found');
        }

       
        document.cookie = `access_token=${token}; path=/`
        
        window.location.href = '/activities/activity-page';
    });
};


