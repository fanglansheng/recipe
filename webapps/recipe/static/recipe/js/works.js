function addWork(){
    // use FormData to add img file to request body.
    var postForm = $("#workform");
    var formData = new FormData();
    // client side validation:
    if($('input[type=file]')[0].files.length == 0){
        console.log("no files");
        return;
    }

    // append data to request data
    formData.append("img", $('input[type=file]')[0].files[0]);
    formData.append("bio", $('#workform-text').val());
    formData.append("csrfmiddlewaretoken", $('input[name=csrfmiddlewaretoken]').val());

    // make ajax request
    $.ajax({ 
        type: postForm.attr('method'), 
        url: postForm.attr('action'), 
        data: formData,
        processData: false,  // tell jQuery not to process the data
        contentType: false   // tell jQuery not to set contentType
    })
    .done(function(data) {
        if(data.type == "error"){
            errMsg = "";
            $.each(data.errors,function(i,el){
                console.log(i);
                errMsg +=el[0].message;
                console.log(errMsg);
                // $(".registerError").html(function(0, "sdff"));
                // function(0, el[0].message)
            });
            // $('[data-toggle="tooltip"]').tooltip();  
            // $("#post-text-area").addClass("post-warning");
        }
        else{
          // $('[data-toggle="tooltip"]').tooltip('disable');
          // $("#post-text-area").removeClass("post-warning");
            updateWorkList();
        }
    });
}

function populateWorkList() {
    $.get("/get_all_works")
    .done(function(data) {
        var workList = $("#works-list");
        // store wrok data from json to workList element
        workList.data('maxCount', data['maxCount']);
        // empty the current workList content to create new wroks.
        // workList.html('');
        // create new wrok
        for (var i = 0; i < data.works.length; i++) {
            // parse json string data to object that can used easily
            var work = JSON.parse(data.works[i]);
            var new_item = $("<p>").append(work['fields'].bio);
            var item_id = work.pk;
            var new_img = $('<img>').attr('src', "/get_work_img/"+item_id);
            workList.append(new_item);
            workList.append(new_img);
            // $('#'+post.postId+' .comment-post').data("postId",post.postId);
        }

    });
}

function updateWorkList(){
    var workList = $("#works-list");
    var maxEntry = workList.data("maxCount");

    $.get("/get_work_changes/"+maxEntry)
    .done(function(data) {
        workList.data('maxCount', data['maxCount']);
        for (var i = 0; i < data.works.length; i++) {
            var work = JSON.parse(data.works[i]);
            var new_item = $("<p>").append(work['fields'].bio);
            var new_item = $("<p>").append(work['fields'].bio);
            var item_id = work.pk;
            var new_img = $('<img>').attr('src', "/get_work_img/"+item_id);
            workList.prepend(new_img);
            workList.prepend(new_item);
            // $('#'+post.postId+' .comment-post').data("postId",post.postId);
        }
    }); 
}


$(document).ready(function () {
    // Add event-handlers
    $("#submit-work").click(function(ev){
        ev.preventDefault();
        addWork();
    });
    // add event-handler to dynamic created items
    // $("#posts-list").on("keypress",".comment-post", 
    //   function (e) { if (e.which == 13) addComment(); } );

    // Set up post list with initial DB items and DOM data
    populateWorkList();
    // populateComments();

    // Periodically refresh to-do list
    window.setInterval(updateWorkList, 5000);
    // window.setInterval(updateComments, 5000);

    // CSRF set-up copied from Django docs
    function getCookie(name) {  
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
    });

});