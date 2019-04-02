// Please refer to documentation at: https://github.com/facundoolano/google-play-scraper#list

var gplay = require('google-play-scraper'); 

// Define app id
const appid = 'com.ea.game.pvz2_row';

// Returns app general information 
gplay.app({appId: appid , 
           lang:'pt', 
           country:'br'})
//    .then(console.log, console.log);


// Return categories available on Google Play
gplay.categories().then(console.log);

// Return app review
gplay.reviews({
    appId: appid,
    lang: 'pt',
    page: 0,
    sort: gplay.sort.RATING,
    page: 0,
})
//.then(console.log, console.log);
