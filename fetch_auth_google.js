const url_auth_google = 'https://blabalala/google-auth'

async function autentikasi_google() {
    const url = `${url_auth_google}/autentikasi`;
    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            }
        });

        if (response.status === 200 || response.status === 201) {
            const data = await response.json();

            return data;
        } else {
            throw new Error('Request failed with status ' + response.status);
        }
    } catch (error) {
        throw new Error('Error: ' + error);
    }
}