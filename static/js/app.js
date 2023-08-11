
$(document).ready(function () {
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