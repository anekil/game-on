function deleteRating(ratingId) {
    fetch('/rating-delete', {
        method: 'POST',
        body: JSON.stringify({ ratingId: ratingId })
    }).then();
}

function recommend() {
      fetch('/recommend', {
        method: 'GET',
    }).then();
}