

// each post in post list
// bind(this, arg1, arg2, ..\.): we're simply passing 
// more arguments to deleteWork
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

  likeHandler: function(workid){
    $.get("/like_work/"+workid)
    .done(function(data) {
      if(data.type=="success"){
        itself.state.allWork.forEach(function(c,i,input){
          if(c.id == workid){
            input[i]=data.work;
            itself.setState({ allWork: input });
          }
        });
      }
      else if(data.type=="errors"){

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
        <WorkBox work={post}
                 onDelete={itself.deleteWork.bind(itself, post.id)}/>
      );
      return( <div key={i}> { workBox } </div> );
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
  onShowComment: function(){
    var isShow = this.state.showCmt;
    this.setState({showCmt:!isShow});
  },

  onLike : function(){
    var isLiked = this.state.liked;
    this.setState({liked:!isLiked});
  },

  getInitialState: function(){
    return {liked:false, showCmt:false};
  },

  render: function() {
    var work = this.props.work;
    var commentBox = this.state.showCmt ? 
      <CommentList isShow={this.state.showCmt} workid={work.id}/>:null;
    return (
      <div className="workBox">
        <div className="workItem">
          <div className="workUserBox">
            <img className="uImgCircleSmall"
              src={"/user_photo/"+work.user.username}/>
            <a href={"/profile/"+work.user.id}>{work.user.username}</a>
            <button className="delWorkBtn" onClick={this.props.onDelete}></button>
          </div>

          <div>
            <p className="bio">{work.bio}</p>
            <img className="workImg" src={"/get_work_img/"+work.id}/>
          </div>

          <div>
            <button className="likeBtn" onClick={this.props.onLike}>
              <i className="material-icons">thumb_up</i>
            </button>
            <button className="btn" onClick={this.onShowComment}>
              <i className="material-icons">comment</i>
            </button>
          </div>
        </div>
        {commentBox}
      </div>
    );
  }
});


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

    this.setState({"workbio":""});
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
    return { workbio: "" };
  },

  render: function(){
    return (
      <form enctype="multipart/form-data" method="post" id="workform">
        <textarea className="workformText" value={this.state.workbio} 
          onChange={this.changeHandler} placeholder="What did you cook?"></textarea>
        <input ref="workfile" name="img" type="file"/>
        <input id="submit-work" type="submit" value="Share" onClick={this.addWork}/>
        <DjangoCSRFToken/>
      </form>
    );
  }
});


var CommentList = React.createClass({
  loadCommentsFromServer: function(){
    if(!this.props.isShow) return;
    var itself = this;
    $.get("/get_comments_by_work/"+this.props.workid)
    .done(function(data) {
      itself.setState({ user:data.user, allComments: data.comments });
    });
  },

  deleteHandler: function(commentid){
    // delete this comment at front end
    var commentList = this.state.allComments;
    commentList.forEach(function(c,i,input){
      if(c.id == commentid){
        input.slice(i,1);
      }
    });

    this.setState({allComments: commentList});

    var itself = this;
    $.post("/delete_work_comment/"+commentid)
    .done(function(data) {
      if(data.type == "error"){
        errMsg = "";
        $.each(data.errors,function(i,el){
          errMsg +=el[0].message;
          console.log(i+errMsg);
        });
      }
    });
  },

  getInitialState: function(){
    return { user:'', allComments:[]};
  },

  componentDidMount: function(){
    this.loadCommentsFromServer();
    setInterval(this.loadCommentsFromServer, 5000);
  },

  render: function(){
    // each comment item
    var self = this;
    var allComments = this.state.allComments.map(function(c, i){
      var deleteBtn = c.user.username != self.state.user ? null : (
          <button className="delWorkBtn"
            onClick={self.deleteHandler.bind(self,c.id)}>
          </button>
        );

      return(
        <div key={i} className="commentItem">
          {deleteBtn}
          <p>
            <a href={"/profile/"+c.user.username}>{c.user.username}: </a>
            {c.content}
          </p>
        </div>
      );
    });

    return (
      <div className="commentBox">
        <CommentForm workid={this.props.workid}
          updateHandler={this.loadCommentsFromServer}/>
        <div className="commentList">
          { allComments }
        </div>
      </div>
    );
  }
});


var CommentForm = React.createClass({
  addComment : function(e){
    e.preventDefault();
    // use FormData to add img file to request body.
    var formData = new FormData();

    // client side validation:
    if(this.state.comment == ''){
        console.log("no inputs");
        return;
    }

    var csrf = this.refs.csrfToken.refs.csrf.value;
    // append data to request data
    formData.append("content", this.state.comment);
    formData.append("csrfmiddlewaretoken", csrf);

    this.setState({"comment":""});
    var self = this;
    $.ajax({ 
        type: 'POST', 
        url: '/post_comment/'+this.props.workid, 
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
          self.props.updateHandler();
        }
    });
  },

  changeHandler: function(event){
    this.setState({
      comment: event.target.value
    });
  },

  getInitialState: function(){
    return { comment: "" };
  },

  render: function() {
    return (
      <form className="commentForm" enctype="multipart/form-data" method="post">
        <textarea
          value={this.state.comment} 
          onChange={this.changeHandler}>
        </textarea>
        <input className="material-icons" type="submit"
          value="send" onClick={this.addComment}/>
        <DjangoCSRFToken ref="csrfToken"/>
      </form>
    );
}
});

var DjangoCSRFToken = React.createClass({
  render: function() {
    var csrfToken = getCookie('csrftoken');
    return (
      <input ref="csrf" type="hidden"
        name="csrfmiddlewaretoken" value={csrfToken}/>
    );
  }
});

// module.exports = DjangoCSRFToken: DjangoCSRFToken;

var postListInstance = ReactDOM.render(
  <PostList/>,
  document.getElementById('workArea')
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