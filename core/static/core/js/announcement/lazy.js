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

function setup(feedSlug, initial_cards) {
    let page = 1

    // temporary buffer of cards
    let loadIn = new Map();
    let pagesLoaded = initial_cards;
    let loadedLast = false;
    let loading = false;
    let cardsElem = document.getElementById(`cards-${feedSlug}`);

    // loads the buffer into the webpage
    function loadBuffer(){
        // guarantee that only one thread is running (don't want announcements to be added in a different order)
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
    async function insertPage(page, feed) {
        console.log(`loading page ${page} for feed ${feed}`);
        const cards = await loadPage(page, feed);
        loadIn.set(page, cards);
        loadBuffer();
    }

    // called when we want to add more cards - asynchronously called, updates page at the start
    return async (pageLen) => {
        let start = page
        page += pageLen
        for(let i = start; i < start + pageLen; i++){
            if (!loadedLast) {
                await insertPage(i, feedSlug);
            }
        }
    }
}

export { setup };
