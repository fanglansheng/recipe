var RecipeBox = React.createClass({
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
          <img src={"/user_photo/"+recipe.user.id}/>
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

var recipeAreaInstance = ReactDOM.render(
  <RecipeBox/>,
  document.getElementById('recipeArea')
);