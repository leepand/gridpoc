//实现单选


$(function () {
$('.navChange ').on('click', 'li', function() {
    $('.navChange li.active').removeClass('active');
    $(this).addClass('active');
});
    
});


 


/*$('#navChange li').click(function (e) {
        
        $('#navChange li').removeClass('active');

        var $parent = $(this);
        if (!$parent.hasClass('active')) {
            $parent.addClass('active');
        }
       
    });*/
