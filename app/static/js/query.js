$(function() {
    $('span.btn.btn-clear').click(function(){
        $('span.btn').removeClass('active')
        $(this).addClass('active')
    });
    $('span.btn').click(function(){
        $(this).toggleClass('active');
        if ($('span.btn.active').length > 5) {
            alert('最多只能选择5个标签！')
            $(this).removeClass('active')
        };
        let stars, careers, sexes, positions, tags, experiences;
        stars = careers = sexes = positions = tags = experiences = new Array();
    });
})