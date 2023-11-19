const url_action_bw = 'http://localhost:8000/BecomeWaifu'

const bahasa = ['bahasa indonesia', 'English', '日本語', 'basa jawa', '한국어', 'русский язык']

async function BWMeimeiHimari(bahasa, file, access_token) {
    const url = `${url_action_bw}/change-voice/speaker_id=14?bahasa=${bahasa}`;
    try {
        const response = await fetch(url, {
            method: 'POST',
            body: file,
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'access-token': access_token
            }
        });

        if (response.status === 200) {
            const data = await response.json();
            return data;
        } else if (response.status === 400){
            return 'LOG AUDIO ANDA TELAH MENCAPAI BATAS HAPUS LOG-AUDIO ANDA DAN MULAI RUBAH SUARA ANDA LAGI :)'
        }
    } catch (error) {
        return 'An error occurred while preparing the answer for your please repeat request'
    }
}

async function BWKusukabeTsumugi(bahasa, file, access_token) {
    const url = `${url_action_bw}/change-voice/speaker_id=8?bahasa=${bahasa}`;
    try {
        const response = await fetch(url, {
            method: 'POST',
            body: file,
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'access-token': access_token
            }
        });

        if (response.status === 200) {
            const data = await response.json();
            return data;
        } else if (response.status === 400){
            return 'LOG AUDIO ANDA TELAH MENCAPAI BATAS HAPUS LOG-AUDIO ANDA DAN MULAI RUBAH SUARA ANDA LAGI :)'
        }
    } catch (error) {
        return 'An error occurred while preparing the answer for your please repeat request'
    }
}

async function BWNurse_T(bahasa, file, access_token) {
    const url = `${url_action_bw}/change-voice/speaker_id=47?bahasa=${bahasa}`;
    try {
        const response = await fetch(url, {
            method: 'POST',
            body: file,
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'access-token': access_token
            }
        });

        if (response.status === 200) {
            const data = await response.json();
            return data;
        } else if (response.status === 400){
            return 'LOG AUDIO ANDA TELAH MENCAPAI BATAS HAPUS LOG-AUDIO ANDA DAN MULAI RUBAH SUARA ANDA LAGI :)'
        }
    } catch (error) {
        return 'An error occurred while preparing the answer for your please repeat request'
    }
}

async function BWNo7(bahasa, file, access_token) {
    const url = `${url_action_bw}/change-voice/speaker_id=29?bahasa=${bahasa}`;
    try {
        const response = await fetch(url, {
            method: 'POST',
            body: file,
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'access-token': access_token
            }
        });

        if (response.status === 200) {
            const data = await response.json();
            return data;
        } else if (response.status === 400){
            return 'LOG AUDIO ANDA TELAH MENCAPAI BATAS HAPUS LOG-AUDIO ANDA DAN MULAI RUBAH SUARA ANDA LAGI :)'
        }
    } catch (error) {
        return 'An error occurred while preparing the answer for your please repeat request'
    }
}

async function BWSayo(bahasa, file, access_token) {
    const url = `${url_action_bw}/change-voice/speaker_id=46?bahasa=${bahasa}`;
    try {
        const response = await fetch(url, {
            method: 'POST',
            body: file,
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'access-token': access_token
            }
        });

        if (response.status === 200) {
            const data = await response.json();
            return data;
        } else if (response.status === 400){
            return 'LOG AUDIO ANDA TELAH MENCAPAI BATAS HAPUS LOG-AUDIO ANDA DAN MULAI RUBAH SUARA ANDA LAGI :)'
        }
    } catch (error) {
        return 'An error occurred while preparing the answer for your please repeat request'
    }
}