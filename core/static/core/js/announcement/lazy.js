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

function setup(feed, initialLimit, perPage) {
    // temporary buffer of cards
    let loadIn = new Map()
    // initialLimit is a multiple of perPage
    let nextPage = initialLimit / perPage + 1
    let loadedLast = false
    let loading = false
    let cardsElem = document.getElementById(`cards-${feed}`)
    let pk = ["all", "my"].includes(feed) ? feed : cardsElem.dataset.pk;

    console.log("lazy: feed", feed);
    console.log('lazy: k', pk);

    // loads the buffer into the webpage
    function loadBuffer(){
        // guarantee that only one instance is running (don't want announcements to be added in a different order)
        if(!loading){
            loading = true;
            // add the next card if we haven't loaded the last card yet
            while(!loadedLast && loadIn.has(nextPage + 1)){
                cardsElem.insertAdjacentHTML('beforeend', loadIn.get(nextPage + 1));
                const nexts = cardsElem.getElementsByClassName('has-next');
                for (let i = nexts.length - 2; i >= 0; i--) {
                    nexts[i].remove();
                }
                if(nexts[nexts.length - 1].classList.contains("no-more")) loadedLast = true;
                nextPage += 1;
            }
            loading = false;
        }
    }

    function insert(cards) {
        cardsElem.insertAdjacentHTML('beforeend', cards)
        const nexts = cardsElem.getElementsByClassName('has-next')
        for (let i = nexts.length - 2; i >= 0; i--)
            nexts[i].remove()
        loadedLast = nexts[nexts.length - 1].classList.contains("no-more")
    }

    // adds the card to the buffer
    async function loadNextPage() {
        if (loadedLast) {
            // no more to load
            return
        }
        console.debug(`lazy: [${feed} / ${pk}]: loading next page (${nextPage})`)
        const cards = await loadPage(nextPage, pk)
        insert(cards)
        console.debug(`lazy: [${feed} / ${pk}]: ${nextPage} ${loadedLast ? "yes last" : "no last"}`)
        nextPage ++
    }

    let locked = false

    // called when we want to add more cards - asynchronously called, updates page at the start
    return async () => {
        if (!locked) {
            // NOTE: not the best, but should be good enough
            locked = true
            await loadNextPage()
            locked = false
        }
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
