
$(document).ready(function () {

    $('.like-btn').click(function (e) {
        e.preventDefault();
        
        const self = $(this);
        let liked = self.data('liked');
        const csfrToken = self.data('csrftoken');
        const likeCountElement = self.siblings('.like-count');

        console.log(liked);
        $.ajax({
            type: 'POST',
            url: self.attr('href'), 
            data: {
                csrfmiddlewaretoken: csfrToken
            },
            success: function(response) {
                liked = !liked;
                self.data('liked', liked);

                likeCountElement.text(response.like_count);
                if (liked) {
                    self.children('i').removeClass('bi-hand-thumbs-up').addClass('bi-hand-thumbs-up-fill');
                } else {
                    self.children('i').removeClass('bi-hand-thumbs-up-fill').addClass('bi-hand-thumbs-up');
                }
            }
        });

    });


    jdenticon();
    $('.spinner-border').hide();
    var infinite = new Waypoint.Infinite({
        element: $('.infinite-container')[0],
        handler: function (direction) {
            console.log(diretion);

        },
        offset: 'bottom-in-view',

        onBeforePageLoad: function () {
            $('.spinner-border').show();
        },
        onAfterPageLoad: function () {
            jdenticon();
            $('.spinner-border').hide();
        }
    });
});