function count_click(tweet_id)
{
    target =  (event.target) ? event.target : ((event.currentTarget) ? event.currentTarget : event.srcElement);
    alert(target);
}

function get_tweet(tweet_id)
{
    var jqxhr = $.ajax({
        url:"{% url tweets.views.get_tweet %}"+tweet_id,
        data:{},
        type:'GET',
        dataType:'json'}).done(function(data) {
        if (data['status'] = 200)
        {
            $("#tweet-"+tweet_id).children(".details")[0].innerHTML = data['html'];
        } 
    }
    )
}

function vote_links(tweet_id,status)
{
    up_html = "<a href=\"{% url tweets.views.upvote %}"+tweet_id+"\" onclick=\"upvote_tweet('"+tweet_id+"');return false;\"><i class=\"icon-chevron-up icon-2x\"></i></a>"
    down_html = "<a href=\"{% url tweets.views.downvote %}"+tweet_id+"\" onclick=\"downvote_tweet('"+tweet_id+"');return false;\"><i class=\"icon-chevron-down icon-2x\"></i></a>"
    if (status == 'upvoted')
    {
        up_html = "<a href=\"{% url tweets.views.undo_upvote %}"+tweet_id+"\" onclick=\"undo_upvote_tweet('"+tweet_id+"');return false;\"><i class=\"icon-chevron-up icon-2x green\"></i></a>"
    }
    else if (status == 'downvoted')
    {
        down_html = "<a href=\"{% url tweets.views.undo_upvote %}"+tweet_id+"\" onclick=\"undo_downvote_tweet('"+tweet_id+"');return false;\"><i class=\"icon-chevron-down icon-2x red\"></i></a>"
    }
    return up_html+down_html
}

function upvote_tweet(tweet_id,up)
{

    var jqxhr = $.ajax({
        url:"{% url tweets.views.upvote %}"+tweet_id,
        data:{},
        type:'GET',
        dataType:'json'})
        .done(function(data) {
        if (data['status'] = 200)
        {
            $("#tweet-votes-"+tweet_id).html(vote_links(tweet_id,'upvoted'));
        }
    }
    )
}

function undo_upvote_tweet(tweet_id)
{
    var jqxhr = $.ajax({
        url:"{% url tweets.views.undo_upvote %}"+tweet_id,
        data:{},
        type:'GET',
        dataType:'json'})
    .done(function(data) {
        if (data['status'] = 200)
        {
            $("#tweet-votes-"+tweet_id).html(vote_links(tweet_id,'neutral'));
        }
    }
    )
}

function downvote_tweet(tweet_id,up)
{

    var jqxhr = $.ajax({
        url:"{% url tweets.views.downvote %}"+tweet_id,
        data:{},
        type:'GET',
        dataType:'json'})
        .done(function(data) {
        if (data['status'] = 200)
        {
            $("#tweet-votes-"+tweet_id).html(vote_links(tweet_id,'downvoted'));
        }
    }
    )
}

function undo_downvote_tweet(tweet_id)
{
    var jqxhr = $.ajax({
        url:"{% url tweets.views.undo_downvote %}"+tweet_id,
        data:{},
        type:'GET',
        dataType:'json'})
    .done(function(data) {
        if (data['status'] = 200)
        {
            $("#tweet-votes-"+tweet_id).html(vote_links(tweet_id,'neutral'));
        }
    }
    )
}

{%if request.user.is_staff %}
function add_to_category(tweet_id,category)
{
    var jqxhr = $.ajax({
        url:"{% url tweets.views.add_to_category %}"+tweet_id+"/"+category,
        data:{},
        type:'GET',
        dataType:'json'})
    .done(function(data) {
        if (data['status'] = 200)
        {
            $("#tweet-"+tweet_id+"-"+category).html("<a href=\"{% url tweets.views.remove_from_category %}"+tweet_id+"/"+category+"\" onclick=\"remove_from_category('"+tweet_id+"','"+category+"');return false;\"><span class=\"label label-success\">"+category+"</span></a>");
        }
    }
    )
}

function remove_from_category(tweet_id,category)
{
    var jqxhr = $.ajax({
        url:"{% url tweets.views.remove_from_category %}"+tweet_id+"/"+category,
        data:{},
        type:'GET',
        dataType:'json'})
    .done(function(data) {
        if (data['status'] = 200)
        {
            $("#tweet-"+tweet_id+"-"+category).html("<a href=\"{% url tweets.views.add_to_category %}"+tweet_id+"/"+category+"\" onclick=\"add_to_category('"+tweet_id+"','"+category+"');return false;\"><span class=\"label\">"+category+"</span></a>");
        }
    }
    )
}
{%endif%}

{%if not request.session.info_box_dismissed %}
function dismiss_info_box()
{
    var jqxhr = $.ajax({
        url:"{% url tweets.views.dismiss_info_box %}",
        data:{},
        type:'GET',
        dataType:'json'})
    .done(function(data) {
    }
    );
    $('.alert').alert('close');
}
{%endif%}

var alreadyloading = false;
var current_page = 1;
 
$(window).scroll(function() {
    if ($('body').height() <= ($(window).height() + $(window).scrollTop())) {
        if (alreadyloading == false) {
            alreadyloading = true;
            $('#tweets-loading').html("<p>Please wait, loading more Tweets...</p>")
            var jqxhr = $.ajax({
               url:load_tweets_url+"?page="+(current_page+1),
                data:{},
                type:'GET',
                dataType:'json'})
            .done(function(data) {
                if (data['status'] == 200)
                {
                    $('#tweets').children().last().after(data['tweets_html']);
                    $('#tweets-loading').html("")
                }
                else
                {
                    $('#tweets-loading').html("<p>Loading failed.</p>")
                }
                alreadyloading = false;
                current_page++;
            });

        }
    }
});

