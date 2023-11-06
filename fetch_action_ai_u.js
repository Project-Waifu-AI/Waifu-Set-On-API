const url_action_aiu = 'http://localhost:8000/AsistenWaifu'

async function pesanMeimeiHimari(pesan, access_token) {
    const url = `${url_action_aiu}/pesan-meimei-himari?pesan=${pesan}`;
    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'access-token': access_token
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

async function pesanNurseT(pesan, access_token) {
    const url = `${url_action_aiu}/pesan-nurse-T?pesan=${pesan}`;
    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'access-token': access_token
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

async function pesanKusukabeTsumugi(pesan, access_token) {
    const url = `${url_action_aiu}/pesan-kusukabe-tsumugi?pesan=${pesan}`;
    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'access-token': access_token
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

async function pesanNo7(pesan, access_token) {
    const url = `${url_action_aiu}/pesan-no.7?pesan=${pesan}`;
    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'access-token': access_token
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

async function pesanSayo(pesan, access_token) {
    const url = `${url_action_aiu}/pesan-SAYO?pesan=${pesan}`;
    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'access-token': access_token
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

async function deleteObrolan(access_token){
    const url = `${url_action_aiu}/delete-obrolan`;
    try {
        const response = await fetch(url, {
            method: 'DELETE',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'access-token': access_token
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
module.exports = {pesanKusukabeTsumugi,pesanMeimeiHimari,pesanNo7,pesanNurseT,pesanSayo, deleteObrolan};