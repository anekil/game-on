function deleteRating(ratingId) {
    fetch('/rating-delete', {
        method: 'POST',
        body: JSON.stringify({ ratingId: ratingId })
    }).then((_res) => {
        window.location.href = "/";
    });
}