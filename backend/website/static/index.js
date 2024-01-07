function deleteRating(ratingId) {
    fetch('/rating-delete', {
        method: 'POST',
        body: JSON.stringify({ ratingId: ratingId })
    }).then(() => window.location = window.location.href);
}

function recommend() {
      fetch('/recommend', {
        method: 'GET',
    }).then();
}