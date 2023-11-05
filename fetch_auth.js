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

// test fetch
ulang_tahun = new Date('2023-11-04');

const email = 'godim.ngadinegaran@gmail.com';
const password = '230205';
const konfirmasi_password = '230205';
const token = '36967';
const pesan = 'hai siapa namamu';
const access_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxZGQwMDkwZS0xZDdmLTQ0NTQtYmEyMi0xNzlmYWQzNTJkNzciLCJsZXZlbCI6InVzZXIiLCJleHAiOjE2OTkxNzk0Njd9.8IvicnHa84SeAiWhvKCz05ySA4WDzuBygoiN65qPoeM';
loginFetch(email, password)
    .then(data => {
        console.log('pesan:', data);
    })
    .catch(error => {
        console.error(error);
    });
