const url_autentikasi = 'http://localhost:8000/wso-auth'

async function loginFetch(emailORname, password) {
    const url = `${url_autentikasi}/login`;
    const requestBody = {
        emailORname: emailORname,
        password: password
    };

    try {
        const response = await fetch(url, {
            method: 'POST',
            body: JSON.stringify(requestBody),
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.status === 200) {
            const data = await response.json();

            return data;
        } else {
            throw new Error('Request failed with status ' + response.status);
        }
    } catch (error) {
        throw new Error('Error:', error);
    }
}

async function regisFetch(email) {
    const url = `${url_autentikasi}/register/${email}`;
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.status === 200) {
            const data = await response.json();
            
            return data;
        } else {
            throw new Error('Request failed with status ' + response.status);
        }
    } catch (error) {
        throw new Error('Error: ' + error);
    }
}

async function simpanUserFetch(email, password, konfirmasiPassword, token) {
    const url = `${url_autentikasi}/simpan-user`;
    const requestBody = {
        email: email,
        password: password,
        konfirmasi_password: konfirmasiPassword,
        token: token
    };

    try {
        const response = await fetch(url, {
            method: 'POST',
            body: JSON.stringify(requestBody),
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.status === 201) {
            const data = await response.json();

            return data;
        } else {
            throw new Error('Request failed with status ' + response.status);
        }
    } catch (error) {
        throw new Error('Error:', error);
    }
}

module.exports = {loginFetch, regisFetch, simpanUserFetch};