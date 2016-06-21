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
    return { allRecipes:[] };
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
          <div className="recipeThumb">
            <div className="info-overlay">
            {recipe.save} Saved | {recipe.tried} Tried
            </div>
            <img src={"/get_recipe_img/"+recipe.id}/>
          </div>
          
          <div className="recipeInfo">
            <h4>{recipe.name}</h4>
            <img className="rUserImg" src={"/user_photo/"+recipe.user.username}/>
            <a href={"/profile/"+recipe.user.id}>{recipe.user.username}</a>
          </div>
        </div>
      );
    });

    return (
      <div className="recipeBox">
        <h4>Hot Recipes</h4>
        { allRecipes }
      </div>
    );
  }
});

var CategoryBox = React.createClass({
  initCategory: function(){

    this.setState({
      allCates: [
        {title:"Vegetable", icon:"category-icon vegetable"},
        {title:"Meat", icon:"category-icon steak"},
        {title:"SeaFood", icon:"category-icon shrimp"},
        {title:"Soup", icon:"category-icon soup"},
        {title:"Egg", icon:"category-icon egg"},
        {title:"Bakery", icon:"category-icon doughnut"}]
    });
  },
  getInitialState: function(){
    return { allCates:[] };
  },
  componentDidMount: function(){
    this.initCategory();
  },
  render: function(){
    var allCates = this.state.allCates.map(function(cat, i){
      return(
        <li key={i}>
          <a href="/">
          <div className={cat.icon}></div>{cat.title}
          </a>
        </li>
      );
    });
    return (
      <div className="categoryBox">
        <ul>{allCates}</ul>
      </div>
    );
  }
});

var categoryInstance = ReactDOM.render(
  <CategoryBox/>,
  document.getElementById('categoryArea')
);

var recipeAreaInstance = ReactDOM.render(
  <RecipeBox/>,
  document.getElementById('recipeArea')
);