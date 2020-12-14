$(document).ready(function(){
    console.log('working from the base ...')

    $('#post_success_message').delay(5000).fadeOut();
});



$('#model-btn').click(function (){
    console.log('button works ...')
    $('.ui.modal').modal('show')
})

let display = false

$(".comment_btn").click(function () {
    console.log('comment button works ...')
    if (display===false) {
        $(this).next(".comment-box").show("slow");
        display=true
    } else {
        $(this).next(".comment-box").hide("slow");
        display=false
    }
});