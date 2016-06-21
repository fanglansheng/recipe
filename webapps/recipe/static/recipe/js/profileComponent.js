var PerfileRecipeBox = React.createClass({
  loadRecipeFromServer: function(){
    //ajax;
    var itself = this;
    $.get("/get_all_recipes")
    .done(function(data) {
      itself.setState({
        allRecipes: data.recipes
      });
    });
  },

  getInitialState: function(){
    return {allRecipes:[]};
  },

  componentDidMount: function(){
    this.loadRecipeFromServer();
    // setInterval(this.updateWorkList, 5000);
  },

  render: function(){
    var itself = this;
    var allRecipes = this.state.allRecipes.map(function(recipe, i){
      
      return(
        <div key={i} className="recipeItem">
          <img src={"/get_recipe_img/"+recipe.id}/>
          <img src={"/user_photo/"+recipe.user.username}/>
          <div>{recipe.user.username}</div>
          <div> {recipe.save.length} saved</div>
          <div> {recipe.name} </div>
        </div>
      );
    });

    return (
      <div className="recipeBox"> 
        { allRecipes }
      </div>
    );
  }
});

var PerfileSavesBox = React.createClass({
  loadSavesFromServer: function(){
    var itself = this;
    $.get("/get_all_recipes")
    .done(function(data) {
      itself.setState({
        allSaves: data.recipes
      });
    });
  },

  getInitialState: function(){
    return {allSaves:[]};
  },

  componentDidMount: function(){
    this.loadSavesFromServer();
  },

  render: function(){
    var itself = this;
    var allSaves = this.state.allSaves.map(function(recipe, i){
      return(
        <div key={i} className="recipeItem">
          <img src={"/get_recipe_img/"+recipe.id}/>
          <img src={"/user_photo/"+recipe.user.username}/>
          <div>{recipe.user.username}</div>
          <div> {recipe.save.length} saved</div>
          <div> {recipe.name} </div>
        </div>
      );
    });

    return (
      <div className="recipeBox"> 
        { allSaves }
      </div>
    );
  }
});

var ProfileWorkBox = React.createClass({
  loadWorksFromServer: function(){
    var itself = this;
    $.get("/get_all_works")
    .done(function(data) {
      itself.setState({
        maxCount: data.maxCount,
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
    this.loadWorksFromServer();
  },

  render: function(){
    var itself = this;
    var allPosts = this.state.allWork.map(function(post, i){
      var workBox = post.deleted ? null : (
        <div key={i} className="recipeItem">
          <img src={"/get_work_img/"+post.id}/>
          <div>{post.user.username}</div>
          <div> {post.likes.length} saved</div>
          <div> {post.name} </div>
        </div>
      );
      return( <div key={i}> { workBox } </div> );
    });

    return (
      <div className="postList">
        { allPosts }
      </div>
    );
  }
});

var ProfileContentBox = React.createClass({
  loadProfile: function(){
    var itself = this;
    console.log(userid);
    $.get("/get_user_profile/"+userid)
    .done(function(data) {
      console.log(data);
      itself.setState({
        profile: data.profile,
        fanss: data.fans,
        userRecipes: data.user_recipes,
        userWorks: data.user_works,
        userSaves: data.profile.saves
      });
    });
  },

  getInitialState: function(){
    return { profile:null,
             fans: 0,
             userRecipes:[],
             userWorks:[],
             userSaves:[]};
  },

  componentDidMount: function(){
    this.loadProfile();
  },

  render: function(){
    var profile = this.state.profile;
    console.log(profile);
    var profileBox = this.state.profile == null ? null : (
      <div className="profileContentBox">
        <div className="profileTop">
          <img src={"/user_photo/"+profile.user.username}/>
          <p>{profile.user.username}</p>
          <p>{profile.bio}</p>
          <p>Fans: {this.state.fans}</p>
          <p>Following: {profile.following.length}</p>
        </div>

        <div>
          <h2>Recipes</h2>
          <PerfileRecipeBox/>
        </div>
        <div>
          <h2>Works</h2>
          <ProfileWorkBox/>
        </div>
        <div>
          <h2>Saves</h2>
          <PerfileSavesBox/>
        </div>

      </div>
    );

    return(
      <div> {profileBox} </div>
    );
  }

});

var profileInstance = ReactDOM.render(
  <ProfileContentBox/>,
  document.getElementById('profileArea')
);