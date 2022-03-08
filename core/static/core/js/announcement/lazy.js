/**
 * @author      : Ken Shibata (kenxshibata@gmail.com)
 * @description : lazy loading of annoucements
 */

async function loadPage(page, feed) {
    const response = await fetch(
        `/announcements/cards?page=${page}&feed=${feed}`,
    );
    return response.text();
}

function setup(feedSlug, initialLimit, perPage) {
    let page = 2

    // temporary buffer of cards
    let loadIn = new Map()
    let pagesLoaded = initialLimit
    let loadedLast = false
    let loading = false
    let cardsElem = document.getElementById(`cards-${feedSlug}`)
    let pk = ["all", "my"].includes(feedSlug) ? feedSlug : cardsElem.dataset.pk;

    console.log("feedSlug", feedSlug);
    console.log('pk', pk);

    // loads the buffer into the webpage
    function loadBuffer(){
        // guarantee that only one instance is running (don't want announcements to be added in a different order)
        if(!loading){
            loading = true;
            // add the next card if we haven't loaded the last card yet
            while(!loadedLast && loadIn.has(pagesLoaded + 1)){
                cardsElem.insertAdjacentHTML('beforeend', loadIn.get(pagesLoaded + 1));
                const nexts = cardsElem.getElementsByClassName('has-next');
                for (let i = nexts.length - 2; i >= 0; i--) {
                    nexts[i].remove();
                }
                if(nexts[nexts.length - 1].classList.contains("no-more")) loadedLast = true;
                pagesLoaded += 1;
            }
            loading = false;
        }
    }

    // adds the card to the buffer
    async function insertPage(page, feed, pk) {
        console.debug(`loading page ${page} for feed ${feed} or ${pk}`)
        const cards = await loadPage(page, pk)
        loadIn.set(page, cards)
        loadBuffer()
    }


    // called when we want to add more cards - asynchronously called, updates page at the start
    return async () => {
        let start = page
        page += perPage
        for(let i = start; i < start + perPage; i++)
            if (!loadedLast)
                await insertPage(i, feedSlug, pk)
    }
}

function mapSetup(ks, initialLimit, perPage) {
    const m = new Map();
    for (let i in ks) {
        const k = ks[i];
        m.set(k, setup(k, initialLimit, perPage));
    }
    return m;
}

function loadCheck(margin) {
    return window.innerHeight + window.scrollY >= document.body.offsetHeight - margin
}

export { loadCheck, mapSetup };
