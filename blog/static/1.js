$(document).ready(function(){
   $(window).bind('scroll', loadOnScroll);
});

// Scroll globals
var pageNum = 1; // The latest page loaded
var hasNextPage = true; // Indicates whether to expect another page after this one
var next = 0;
var items = [];
var options = {
  year: 'numeric',
  month: 'long',
  day: 'numeric',
  timezone: 'UTC',
};
// loadOnScroll handler
var loadOnScroll = function() {
   // If the current scroll position is past out cutoff point...
    if (  $(document).height()- $(window).height()-$(window).scrollTop()<30) {
        // temporarily unhook the scroll event watcher so we don't call a bunch of times in a row
        $(window).unbind();
        // execute the load function below that will visit the JSON feed and stuff data into the HTML
        loadItems();
    }
};

var loadItems = function() {
var search = window.location.search.substr(1),
	keys = {};
      
search.split('&').forEach(function(item) {
	item = item.split('=');
	keys[item[0]] = item[1];
});
      

    // If the next page doesn't exist, just quit now
    if (hasNextPage === false) {
        return false
    }

    // Update the page number
    pageNum = pageNum + 1;
    // Configure the url we're about to hit
    if(next === null){
         $(window).bind('scroll', loadOnScroll);
        return
    }
    $.ajax({
        url: 'https://skeletpingvina.xyz/apiusers/?format=json',
        data: (keys['category']!==undefined) ? {offset: pageNum*10-1,category:keys['category']} : {offset:pageNum*10-1},
        dataType: 'json',
        success: function(data) {
            // Update global next page variable
            hasNextPage = true;//.hasNext;
            // Loop through all items
            next = data['next']
            for (var i in data['results']) {
if($(".post-title > a").eq(0).text() == data['results'][i]['title']){
	break;
}
let categorys = '';
		for (var j in data['results'][i]['category']){
categorys += `<a href="/?category=${data['results'][i]['category'][j]['pk']}" rel="tag" style="margin-left: 5px;">#${data['results'][i]['category'][j]['title']}</a>`;
}
                var date = new Date(data['results'][i]['published_date']).toLocaleString("ru", options);
                $("#articles").append(`
                <article>
        <a class="post-thumbnail" href="/${data['results'][i]['slug']}" style="background-image: url('${data['results'][i]['image']} ');">
        </a>
      <div class="post-content">
        <h2 class="post-title"><a href="/${data['results'][i]['slug']}">${data['results'][i]['title']}</a></h2>
        <p>${data['results'][i]['short_text']}</p>
        <span class="post-date">${date}</span>
${categorys}
      </div>
    </article>
                `)
            }
if(data['results'].length){
        $(window).scrollTop($(window).height()-50)

}
        },
        error: function(data) {
            // When I get a 400 back, fail safely
            hasNextPage = false
        },
        complete: function(data, textStatus){
            // Turn the scroll monitor back on
            $(window).bind('scroll', loadOnScroll);
        }
    });
};
