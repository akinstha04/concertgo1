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
});
$('.increment-btn').click(function(e) {
    console.log("ckickec");
    var inc_value = $(this).closest('.certified').find('.qty-input').val();
    // var ids = document.getElementById("ticketprice").textContent
    // var t = parseInt(ids)
    // console.log("asdf"+ids)
    var value = parseInt(inc_value,10);
    value = isNaN(value) ? 0 : value;
    if(value<20)
        value++;
        $(this).closest('.certified').find('.qty-input').val(value);

    // $.ajax({
    //     type: 'GET',
    //     url: '/increaseticket',
    //     data: {
    //         'increase':value,
    //     },
    //     success: function(response) {
    //         aa = t * response.bool
    //         document.getElementById("subtotal").innerText = "$"+aa
    //         document.getElementById("t_amount").innerText = "$"+aa
    //         document.cookie = "amount=" + aa + ";" + "path=/;";
    //     }
    // })
});
$('.decrement-btn').click(function(e) {
    console.log("ckickec");
    var inc_value = $(this).closest('.certified').find('.qty-input').val();
    // var ids = document.getElementById("ticketprice").textContent
    // var t = parseInt(ids)
    // console.log("asdf"+ids)
    var value = parseInt(inc_value,10);
    value = isNaN(value) ? 0 : value;
    if(value>1)
        value--;
    $(this).closest('.certified').find('.qty-input').val(value);

    // $.ajax({
    //     type: 'GET',
    //     url: '/decreaseticket',
    //     data: {
    //         'increase':value,
    //     },
    //     success: function(response) {
    //         aa = t * response.bool
    //         document.getElementById("subtotal").innerText = "$"+aa
    //     },
    // })
});

$('.follow-form').submit(function(e){
    e.preventDefault()
    
    const profile_id = $(this).attr('id')
    
    const followText = $(`.follow-btn${post_id}`).text()
    const trim = $.trim(followText)

    const url = $(this).attr('action')
    
    let res;
    const followers = $(`.follower-count${post_id}`).text()
    console.log('akdin'+followers)
    const trimCount = parseInt(likes)
    
    $.ajax({
        type: 'POST',
        url: url,
        data: {
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
            'post_id':post_id,
        },
        success: function(response) {
            if(trim === 'Unfollow') {
                $(`.follow-btn${profile_id}`).text('Follow')
                res = trimCount - 1
            } else {
                $(`.follow-btn${profile_id}`).text('Unfollow')
                res = trimCount + 1
            }

            $(`.follow-count${profile_id}`).text(res)
            // if(response.bool==true){
            //     console.log("rishavasdfafds")
            // }
        },
        error: function(response) {
            console.log('error', response)
        }
    })
});