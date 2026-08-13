import * as params from '@params';

let fuse;
let resList = document.getElementById('searchResults');
let sInput = document.getElementById('searchInput');
let first, last, current_elem = null
let resultsAvailable = false;

function escapeHtml(value) {
    return String(value ?? '').replace(/[&<>"']/g, function (ch) {
        return ({
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#39;'
        })[ch];
    });
}

function renderResult(item) {
    const title = escapeHtml(item.title);
    const permalink = escapeHtml(item.permalink);
    const summary = escapeHtml(item.summary);
    const date = escapeHtml(item.date);
    const tags = Array.isArray(item.tags) ? item.tags : [];
    const tagHtml = tags
        .filter(Boolean)
        .map((tag) => `<span class="search-tag">${escapeHtml(tag)}</span>`)
        .join('');

    let html = `<li class="post-entry"><header class="entry-header">${title}</header>`;
    if (summary) {
        html += `<div class="entry-content">${summary}</div>`;
    }
    if (date || tagHtml) {
        html += `<footer class="entry-footer">`;
        if (date) {
            html += `<time>${date}</time>`;
        }
        if (date && tagHtml) {
            html += `<span class="search-meta-sep">·</span>`;
        }
        if (tagHtml) {
            html += `<span class="search-tags">${tagHtml}</span>`;
        }
        html += `</footer>`;
    }
    // Keep the overlay link last so PaperMod keyboard nav still works.
    html += `<a href="${permalink}" aria-label="${title}"></a></li>`;
    return html;
}

window.onload = function () {
    let xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                let data = JSON.parse(xhr.responseText);
                if (data) {
                    let options = {
                        distance: 100,
                        threshold: 0.4,
                        ignoreLocation: true,
                        keys: [
                            'title',
                            'permalink',
                            'summary',
                            'content'
                        ]
                    };
                    if (params.fuseOpts) {
                        options = {
                            isCaseSensitive: params.fuseOpts.iscasesensitive ?? false,
                            includeScore: params.fuseOpts.includescore ?? false,
                            includeMatches: params.fuseOpts.includematches ?? false,
                            minMatchCharLength: params.fuseOpts.minmatchcharlength ?? 1,
                            shouldSort: params.fuseOpts.shouldsort ?? true,
                            findAllMatches: params.fuseOpts.findallmatches ?? false,
                            keys: params.fuseOpts.keys ?? ['title', 'permalink', 'summary', 'content'],
                            location: params.fuseOpts.location ?? 0,
                            threshold: params.fuseOpts.threshold ?? 0.4,
                            distance: params.fuseOpts.distance ?? 100,
                            ignoreLocation: params.fuseOpts.ignorelocation ?? true
                        }
                    }
                    fuse = new Fuse(data, options);
                }
            } else {
                console.log(xhr.responseText);
            }
        }
    };
    xhr.open('GET', "../index.json");
    xhr.send();
}

function activeToggle(ae) {
    document.querySelectorAll('.focus').forEach(function (element) {
        element.classList.remove("focus")
    });
    if (ae) {
        ae.focus()
        document.activeElement = current_elem = ae;
        ae.parentElement.classList.add("focus")
    } else {
        document.activeElement.parentElement.classList.add("focus")
    }
}

function reset() {
    resultsAvailable = false;
    resList.innerHTML = sInput.value = '';
    sInput.focus();
}

sInput.onkeyup = function (e) {
    if (fuse) {
        let results;
        if (params.fuseOpts) {
            results = fuse.search(this.value.trim(), {limit: params.fuseOpts.limit});
        } else {
            results = fuse.search(this.value.trim());
        }
        if (results.length !== 0) {
            let resultSet = '';

            for (let item in results) {
                resultSet += renderResult(results[item].item);
            }

            resList.innerHTML = resultSet;
            resultsAvailable = true;
            first = resList.firstChild;
            last = resList.lastChild;
        } else {
            resultsAvailable = false;
            resList.innerHTML = '';
        }
    }
}

sInput.addEventListener('search', function (e) {
    if (!this.value) reset()
})

document.onkeydown = function (e) {
    let key = e.key;
    let ae = document.activeElement;

    let inbox = document.getElementById("searchbox").contains(ae)

    if (ae === sInput) {
        let elements = document.getElementsByClassName('focus');
        while (elements.length > 0) {
            elements[0].classList.remove('focus');
        }
    } else if (current_elem) ae = current_elem;

    if (key === "Escape") {
        reset()
    } else if (!resultsAvailable || !inbox) {
        return
    } else if (key === "ArrowDown") {
        e.preventDefault();
        if (ae == sInput) {
            activeToggle(resList.firstChild.lastChild);
        } else if (ae.parentElement != last) {
            activeToggle(ae.parentElement.nextSibling.lastChild);
        }
    } else if (key === "ArrowUp") {
        e.preventDefault();
        if (ae.parentElement == first) {
            activeToggle(sInput);
        } else if (ae != sInput) {
            activeToggle(ae.parentElement.previousSibling.lastChild);
        }
    } else if (key === "ArrowRight") {
        ae.click();
    }
}
