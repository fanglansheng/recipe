var WorkBox = React.createClass({
  componentDidMount: function(){
    console.log(this.props);
  },
  render: function() {
    // console.log(this.props);
    return (
      <div className="workBox">
          <span>User: {this.props.work.user.username}</span>
          <a href={"/delete_work/"+this.props.work.id}>Delete</a>
          <p>{this.props.work.bio}</p>
          <img className="workImg" src={"/get_work_img/"+this.props.work.id}/>
      </div>
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


// each post in post list
var PostList = React.createClass({
  
  render: function(){
    var allPosts = this.props.allWork.map(function(post){
      return(
        <WorkBox key={post.id} work={post}/>
      );
    });
    return (
      <div className="postList">
      { allPosts }
      </div>
    );
  }
});

var PostBox = React.createClass({
  loadPostsFromServer: function(){
    //ajax;
    var itself = this;
    $.get("/get_all_works")
    .done(function(data) {
      itself.setState({
        maxCount: data['maxCount'],
        allWork: data.works
      });
    });
  },
  // executes exactly once during the lifecycle of the component 
  // and sets up the initial state of the component.
  getInitialState: function(){
    return {maxCount:[], allWork:[]};
  },
  componentDidMount: function(){
    this.loadPostsFromServer();
    // setInterval()
  },
  render: function(){
    return(
      <div className="postBox">
        <PostList maxCount={this.state.maxCount} allWork={this.state.allWork}/>
      </div>
    );
  }
});
ReactDOM.render(
  <PostBox/>,
  document.getElementById('content1')
);