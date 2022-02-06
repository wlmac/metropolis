/**
 * @author      : Ken Shibata (kenxshibata@gmail.com)
 * @description : lazy loading of annoucements
 */

let loadIn = new Map();
let pagesLoaded = 0;
let loadedLast = false;
let loading = false;
let cardsElem;

function loadBuffer(){
    if(!loading){
        loading = true;
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

async function loadPage(page, feed) {
    const response = await fetch(
        `/announcements/cards?page=${page}&feed=${feed}`,
    );
    return response.text();
}

async function insertPage(page, feed) {
    console.log(`loading page ${page} for feed ${feed}`);
    const cards = await loadPage(page, feed);
    loadIn.set(page, cards);
    loadBuffer();
}

function setup(feedSlug) {
    cardsElem = document.getElementById(`cards-${feedSlug}`);
    return async (page) => {
        if (!loadedLast) {
            await insertPage(page, feedSlug);
        }
    }
}

export { setup };
