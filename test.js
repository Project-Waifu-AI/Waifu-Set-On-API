const fetch = require('node-fetch');

const loginData = {
  emailORname: 'dimas.ngadinegaran@gmail.com',
  password: 'Dimas230205',
  // Other fields from the LoginWSO model
};

fetch('http://waifu-set-on.wso:8000/api/auth/wso/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(loginData),
  credentials: 'include',
})
  .then(response => {
    if (response.ok) {
      if (response.redirected) {
        // Handle the redirect manually or follow it on the server
        console.log('Redirect URL:', response.url);
        // ... perform additional logic based on the redirect URL
      } else {
        return response.json();
      }
    } else {
      return response.json().then(error => {
        throw new Error(error.detail || 'An error occurred');
      });
    }
  })
  .then(data => {
    console.log(data);
  })
  .catch(error => {
    console.error(error.message);
  });
