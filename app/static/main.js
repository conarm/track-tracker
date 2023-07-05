$(document).ready(function() {
    $("button").on("click", function() {
        var clicked_obj = $(this);
        var id = clicked_obj.attr('id');

        $.ajax({
            url: '/like',
            type: 'POST',
            data: JSON.stringify({rating_id: id}),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(response) {
                console.log(response);
                $('#likes').text("Likes: " + response.likes);
            },
            error: function(error){
                console.log(error);
            }
        });
    });
});