let deferredPrompt;
let installPopupClass = '.install-popup'

function displayInstallPrompt(event) {
    event.preventDefault();
    deferredPrompt = event;
    if (Cookies.get('hide_install_prompt') != '1') {
        $(installPopupClass).show();
    }
}

window.addEventListener('beforeinstallprompt', displayInstallPrompt);

window.addEventListener('load', (event) => {
    document.getElementById('install-popup-button').addEventListener('click', async (e) => {
        $(installPopupClass).hide();
        deferredPrompt.prompt();
        const { outcome } = await deferredPrompt.userChoice;
        deferredPrompt = null;
    });
});

window.addEventListener('appinstalled', () => {
    $(installPopupClass).hide();
    deferredPrompt = null;
    window.removeEventListener('beforeinstallprompt', displayInstallPrompt);
});
function dismissInstallPrompt() {
    //Cookies.set('hide_install_prompt', '1', {expires: 7});
    Cookies.set('hide_install_prompt', '1', {expires: 1});
    $(installPopupClass).hide();
}
