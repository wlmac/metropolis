/**
 * @author      : Ken Shibata (kenxshibata@gmail.com)
 * @description : lazy loading of annoucements
 */

async function loadPage(page, feed) {
    const response = await fetch(
        `/announcements/cards?page=${page}&feed=${feed}`,
    );
    const cards = response.text();
    return cards;
}

async function insertPage(cardsElem, page, feed) {
    console.log(`loading page ${page} for feed ${feed}`);
    const cards = await loadPage(page, feed);
    cardsElem.insertAdjacentHTML('beforeend', cards);
    const nexts = cardsElem.getElementsByClassName('has-next');
    for (let i = nexts.length - 2; i >= 0; i--) {
        nexts[i].remove();
    }
    if (nexts[nexts.length-1].classList.contains('no-more')) {
        return false;
    }
    return true;
}

function setup(feedSlug) {
    let page = 1;
    let hasNext = true;
    const cardsElem = document.getElementById(`cards-${feedSlug}`);
    return async () => {
        if (hasNext) {
            hasNext = await insertPage(cardsElem, page, feedSlug);
            page += 1;
        }
    }
}

export { setup };
