// each post in post list
// bind(this, arg1, arg2, ...): we're simply passing more arguments to deleteWork
var PostList = React.createClass({
  deleteWork: function(workid){
    var itself = this;
    $.post("/delete_work/"+workid)
    .done(function(data) {
      if(data.type == "error"){
        // show work again and show some error msgs
        errMsg = "";
        $.each(data.errors,function(i,el){
          errMsg +=el[0].message;
          console.log(i+errMsg);
        });
      }
      else{
        // success, hide this work
        var workList = itself.state.allWork;
        workList.forEach(function(w){
          if(w.id == workid){
            w.deleted = true;
          }
        });

        itself.setState({
          allWork: workList
        });
      }
    });
  },

  loadPostsFromServer: function(){
    //ajax;
    var itself = this;
    $.get("/get_all_works")
    .done(function(data) {
      itself.setState({
        maxCount: data.maxCount,
        allWork: data.works
      });
    });
  },

  updateWorkList: function(){
    console.log(this.state.maxCount);
    var itself = this;
    $.get("/get_work_changes/"+this.state.maxCount)
    .done(function(data) {

      // get new work and deleted works
      var addedWorks = [];
      var deletedWorks = {};
      data.works.forEach(function(c){
        if(c.deleted == true){
          deletedWorks[c.id]=c;
        }
        else{
          addedWorks.push(c);
        }
      });

      // change status in old work list and add new works at front of list
      var workList = itself.state.allWork;
      workList.forEach(function(w){
        if(deletedWorks[w.id] != undefined){
          w.deleted = true;
        }
      });

      itself.setState({
        maxCount: data.maxCount,
        allWork: addedWorks.concat(itself.state.allWork)
      });
    })
    .fail(function(data){
      console.log("Fail:get_work_changes");
      console.log(data);
    }); 
  },

  // executes exactly once during the lifecycle of the component 
  // and sets up the initial state of the component.
  getInitialState: function(){
    return {maxCount:[], allWork:[]};
  },

  componentDidMount: function(){
    this.loadPostsFromServer();
    setInterval(this.updateWorkList, 5000);
  },

  render: function(){
    var itself = this;
    var allPosts = this.state.allWork.map(function(post, i){
      var workBox = post.deleted ? null : (
        <WorkBox work={post} onDelete={itself.deleteWork.bind(itself, post.id)}/>
      );
      return(
        <div key={i} > { workBox } </div>
      );
    });

    return (
      <div> 
        <WorkForm updateList={this.updateWorkList}/>
        <div className="postList">
        { allPosts }
        </div>
      </div>
    );
  }
});

var WorkBox = React.createClass({
  render: function() {
    return (
      <div className="workBox">
        <span>User: {this.props.work.user.username}</span>
        <DeleteWorkBtn clickHandler={this.props.onDelete}/>
        <p>{this.props.work.bio}</p>
        <img className="workImg" src={"/get_work_img/"+this.props.work.id}/>
      </div>
    );
  }
});

var DeleteWorkBtn = React.createClass({
  render: function(){
    return (
      <button className="delWorkBtn" onClick={this.props.clickHandler}>
        Delete
      </button>
    );
  }
});

// var CommentForm = React.createClass({
//     render: function() {
//         return (
//             <div className="postBox">
//             </div>
//         );
//     }
// });

// var CommentList = React.createClass({
//     render: function() {
//         return (
//             <div className="postBox">
//             </div>
//         );
//     }
// });

// var PostItem = React.createClass({
//   render: function() {
//     return (
//       <div className="postBox">
//         <h1>Works</h1>
//         <WrokBox/>
//         <CommentForm/>
//         <CommentList/>
//       </div>
//     );
//   }
// });

var WorkForm = React.createClass({
  addWork: function(e){
    e.preventDefault();
    // use FormData to add img file to request body.
    var formData = new FormData();
    // client side validation:
    console.log(this.refs.workfile.files);

    if(this.refs.workfile.files.length == 0){
        console.log("no files");
        return;
    }

    // append data to request data
    formData.append("img", this.refs.workfile.files[0]);
    formData.append("bio", this.state.workbio);
    formData.append("csrfmiddlewaretoken", $('input[name=csrfmiddlewaretoken]').val());

    var self = this;
    // make ajax request
    $.ajax({ 
        type: 'POST', 
        url: '/post_work', 
        data: formData,
        processData: false,  // tell jQuery not to process the data
        contentType: false   // tell jQuery not to set contentType
    })
    .done(function(data) {
        if(data.type == "error"){
            errMsg = "";
            $.each(data.errors,function(i,el){
                errMsg +=el[0].message;
                console.log(errMsg);
            });
        }
        else{
            self.props.updateList();
        }
    });
  },

  changeHandler: function(event){
    this.setState({
      workbio: event.target.value
    });
  },

  getInitialState: function(){
    return { workbio: "What did you cook?" };
  },

  render: function(){
    return (
      <form enctype="multipart/form-data" method="post" id="workform">
        <textarea className="workformText" value={this.state.workbio} 
          onChange={this.changeHandler}></textarea>
        <input ref="workfile" name="img" type="file"/>
        <input id="submit-work" type="submit" value="Share" onClick={this.addWork}/>
        <DjangoCSRFToken/>
      </form>
    );
  }
});


var DjangoCSRFToken = React.createClass({
  render: function() {
    var csrfToken = getCookie('csrftoken');//Django.csrf_token();
    return (
      <input type="hidden" name="csrfmiddlewaretoken" value={csrfToken}/>
    );
  }
});

// module.exports = DjangoCSRFToken: DjangoCSRFToken;

var postListInstance = ReactDOM.render(
  <PostList/>,
  document.getElementById('content1')
);


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

$(document).ready(function () {

    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  });

});