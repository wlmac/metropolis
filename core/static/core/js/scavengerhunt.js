function setCookie(cname, cvalue, exdays) {
    const d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    let expires = 'expires='+ d.toUTCString();
    document.cookie = cname + '=' + cvalue + ';' + expires + ';path=/sacmas2021/scavenger/';
}

function getCookie(cname) {
    let name = cname + '=';
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return '';
}

function isJSON(str) {
    try {
        JSON.parse(str);
        return true;
    } catch(err) {
        return false;
    }
}

function updateCookie(cname, value) {
    let cookie = getCookie(cname);
    if (cookie == '') {
        cookie = '[]';
    }
    if(isJSON(cookie)) {
        cookie = JSON.parse(cookie);
    } else {
        cookie = [cookie];
    }
    if (!cookie.includes(value)) {
        cookie.push(value);
    }
    cookie = JSON.stringify(cookie);
    setCookie(cname, cookie, 7);
  }

function addQR(url) {
    var code = url.slice(1, -1).split('/').pop().split('-').slice(2).join('-');
    if(code === undefined) {
        return;
    }
    updateCookie('codes', code);
}

function setMsg(dict) {
    let cookie = getCookie('codes');
    if (cookie == '') {
        cookie = '[]';
    }
    if(isJSON(cookie)) {
        cookie = JSON.parse(cookie);
    } else {
        cookie = [cookie];
    }
    let count = 0;
    let codes = JSON.parse(dict.replaceAll('&#x27;', '"'));
    $('#message').empty();
    for (let key in codes) {
        if (cookie.includes(codes[key][0])) {
            $('#message').append(`<span>${codes[key][1]}</span> `);
            count++;
        }
    }
    if (count == 1) {
        count = `${count} QR code.`
    } else if (count == 15) {
        count = 'all the QR codes.'
    } else {
        count = `${count} QR codes.`
    }
    $('#found').text(`You have found ${count}`);
}