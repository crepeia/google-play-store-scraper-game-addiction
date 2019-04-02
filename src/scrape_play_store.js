// Please refer to documentation at: https://github.com/facundoolano/google-play-scraper#list

var gplay = require('google-play-scraper'); 

// Define app id
// const appid = 'com.ea.game.pvz2_row'; // Plant vs. Zombies
const appid = 'com.king.candycrushsaga'; // Candy Crush Saga

// Return list of applications of a given category
gplay.list({
    category: gplay.category.GAME_ACTION,
    collection: gplay.collection.TOP_FREE,
    num: 120,
    lang: 'pt',
    country: 'br',
  })
  .then(console.log, console.log);

// Returns app general information 
gplay.app({appId: appid , 
           lang:'pt', 
           country:'br'})
//    .then(console.log, console.log);


// Return categories available on Google Play
//gplay.categories().then(console.log);

// Return app review
gplay.reviews({
    appId: appid,
    lang: 'pt',
    page: 0,
    sort: gplay.sort.HELPFULNESS,
    page: 0,
})
//.then(console.log, console.log);
