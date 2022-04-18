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
    console.log("gkisdsdn")
    
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
        console.log("chakin")
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
})