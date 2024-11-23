document.body.addEventListener('htmx:afterRequest', function(event) {
    if (event.detail.xhr.status === 200) {
        try {
            const data = JSON.parse(event.detail.xhr.responseText);
            if (data.redirect_url) {
                window.location.href = data.redirect_url;
            }
        } catch (e) {
            console.error('Ошибка обработки JSON-ответа:', e);
        }
    }
});