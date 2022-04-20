// Add wishlist
// $(document).on('click',".add-wishlist", function){
//     var _pid=$(this).attr('data-product');
//    // Ajax
//     $.ajax({
//          url:"/add-wishlist",
//          data:{
//               ticket:_tid
//          },
//          dataType: 'json',
//          success:function(res){
//                console.log(res);
//           }
//      });
//     7/ EndAjax
// });
// End


// $('.add-sishlist').on('click',".add-wishlist", function){
//     var _pid=$(this).attr('data-ticket');
//     //ajax
//     $.ajax({
//         url:"/add_wishlist",
//         data:{
//             ticket:_tid
//         },
//         dataType: 'json',
//         sucess:function(res){
//             console.log(res);
//         }
//     })
// }

$(document).ready(function(){
    
    $(".add-wishlist").on('click',function(){
        alertify.success("Added to wishlist");
        var tid = $(this).attr('data-ticket');
        console.log("ticket_id"+tid);
        $.ajax({
            url:"/add_wishlist",
            data:{
                ticket:tid
            },
            success:function(res){

                console.log("passed")
                
            }
        })
    })

    $(".remove-wishlist").on('click',function(){
        var tid = $(this).attr('pid');
        console.log("ticket_id"+tid);
        var ems = this
        $.ajax({
            url:"/removewishlist",
            data:{
                ticket:tid
            },
            success:function(res){

                console.log("passed")
                ems.parentNode.parentNode.parentNode.remove()
            }
        })
    })

    
});
$('.like-form').submit(function(e){
    e.preventDefault()
    
    const post_id = $(this).attr('id')
    
    const likeText = $(`.like-btn${post_id}`).text()
    const trim = $.trim(likeText)

    const url = $(this).attr('action')
    
    let res;
    const likes = $(`.like-count${post_id}`).text()
    console.log('akdin'+likes)
    const trimCount = parseInt(likes)
    
    $.ajax({
        type: 'POST',
        url: url,
        data: {
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
            'post_id':post_id,
        },
        success: function(response) {
            if(trim === 'Unlike') {
                $(`.like-btn${post_id}`).text('Like')
                res = trimCount - 1
            } else {
                $(`.like-btn${post_id}`).text('Unlike')
                res = trimCount + 1
            }

            $(`.like-count${post_id}`).text(res)
            // if(response.bool==true){
            //     console.log("rishavasdfafds")
            // }
        },
        error: function(response) {
            console.log('error', response)
        }
    })

})