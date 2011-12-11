<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"><head profile="http://gmpg.org/xfn/11"><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title> 
            <%block name="title">Blog | Vincent's Notes</%block>
        </title>

        <link rel="stylesheet" href="/static/css/style.css" type="text/css" media="all">
        <link rel="stylesheet" href="/static/css/tweet_stream.css" type="text/css" media="all">
        <link href="/static/js/google-code-prettify/prettify.css" type="text/css" rel="stylesheet" />
        <script type="text/javascript" src="/static/js/google-code-prettify/prettify.js" ></script>

        <%block name="css">
        </%block>

    </head>
    <body onload="prettyPrint()" >

        <%block name="header">
        <div id="header">
            <div class="innerwrap">
                <div id="menu">
                    <ul>
                        <li><a href="" title="">About</a></li>
                        <li><a href="" title="">GitHub</a></li>
                        <li><a href="" class="subscribe">Subscribe</a></li>
                    </ul>
                </div>

                <h1>
                    <a href="/">
                        <span class="vincent">Vincent</span>
                        <span class="blog">blog</span>
                    </a>
                </h1>
                <!--<h4>Resources for Learning and Mastering MongoDB</h4>-->
            </div>
        </div>
        </%block>


        <%block name="columnleft">

        <div id="main">

            <div class="innerwrap">

                <div id="c1">

                    <%block name="contentleft">
<%
    import datetime, urllib
%>


                    %for entry in recent_posts:
                    <!-- post -->
                    <div class="" id="post-${entry.id}">

                        <div class="post-title">
                            <h1>
                                <a href="/${entry.date.year}/${entry.date.month}/${entry.id}" rel="bookmark">${entry.title}</a>
                            </h1>

                            <span class="post-date">
                                ${datetime.datetime.fromtimestamp(entry.timestamp).strftime("%b %d %Y %H:%M:%S")}
                            </span>
                            <span class="post-categories">
                                in <a href="?category=${urllib.quote(entry.category.name)}" title="">${entry.category.name}</a>
                            </span>
                            <span class="post-categories">
                                taged as 
                                %for i in range(len(entry.tags)):
                                <% tag=entry.tags[i] %>
                                <a href="?tag=${urllib.quote(tag.name)}">${tag.name}</a>
                                %if i != len(entry.tags)-1:
                                ,
                                %endif    
                                %endfor
                            </div>


                            <div class="post-text">
                                <%
                                    from docutils.core import publish_parts
                                    content = publish_parts(entry.content, writer_name='html')['html_body']
                                %>
                                ${content.replace('literal-block', 'literal-block prettyprint') | n,trim}
                            </div>

                            <div class="post-pages" style="display:none"></div>
                            <div class="post-foot">
                                <a href="" class="comments-link" title="" style="display:none" >0 Comments and 0 Reactions</a>				<div class="post-meta">
                                    <div class="post-tags"></div>
                                </div>
                            </div>
                        </div>
                        <div class="sep"><hr></div>

                        %endfor
                        </%block>

                    </div>


                    </%block>





                    <!-- column right -->
                    <div id="c2">

                        <div id="sidebar">

                            <ul id="widgets">

                                <li class="widget">
                                <h2>Search</h2>
                                <!--<form method="get" id="searchform" action="">
                                    <input type="text" onfocus="if (this.value == &#39;Search&#39;) {this.value = &#39;&#39;;}" onblur="if (this.value == &#39;&#39;) {this.value = &#39;Search&#39;;}" value="Search" name="s">
                                </form> -->
                                <!-- GOOGLE CSE -->
                                <div id="cse" style="width: 100%;">Loading</div>
<script src="http://www.google.com/jsapi" type="text/javascript"></script>
<script type="text/javascript"> 
  google.load('search', '1', {language : 'en', style : google.loader.themes.SHINY});
  google.setOnLoadCallback(function() {
    var customSearchControl = new google.search.CustomSearchControl(
      '013068152288002893796:ets6c-unptc');

    customSearchControl.setResultSetSize(google.search.Search.FILTERED_CSE_RESULTSET);
    customSearchControl.draw('cse');
  }, true);
</script>



                                </li>




                                <li class="widget"><h2>Follow Me on SNS</h2>		
                                <div class="textwidget">
                                    <p>
                                    <a href="https://twitter.com/vincentwv" class="twitter-follow-button" data-show-count="false">twitter @vincentwv</a><br>
                                    <a href="http://t.qq.com/Test_Vincent" class="twitter-follow-button" data-show-count="false">qq @vincent</a><br>
                                    <a href="http://weibo.com/vincentwv" class="twitter-follow-button" data-show-count="false">sina @vincent_wv</a><br>
                                    <a href="http://www.douban.com/people/Riefu/" class="twitter-follow-button" data-show-count="false">douban @vincentwv</a><br>
                                    </p>
                                </div>
                                </li>

                                <li class="widget">
                                <h2>Chatting with Me</h2>	
                                <div id="gtalkwidget">
                                    <!--<a href=""><img style="width:75%;" src="/static/image/mongoLA_badge_blank.png"></a>
                                    <br>-->
                                    <iframe src="http://www.google.com/talk/service/badge/Show?tk=z01q6amlq5u5r7751132h9m7pamj8neni062rh47h4otv4qhj58f9d3jhbo3kiruiib05f52268drrtc2qt9h80em5mc1ccc7dcj1nhtp3btigi03r09u4sltfh0sptq9argl75nc2dgibc0sh7blkds2lrdqc34d0lls6os4son5e16r5e782159r0beegemjo&amp;w=200&amp;h=60" frameborder="0" allowtransparency="true" width="200" height="60"></iframe>
                                </div>
                                </li>


                                <li class="widget"><h2>Categories</h2>	
                                <ul>
                                    %for category in categories:
                                    <%
                                        import urllib, copy
                                        q_c = copy.copy(current_query)
                                        q_c['category'] = category.name
                                    %>
                                    <li class="cat-item"><a href="?${urllib.urlencode(q_c)}" title="${category.name}">${category.name}</a>
                                    (${category.postcount})
                                    </li>
                                    %endfor
                                </ul>
                                </li>		



                                <li class="widget">	
                                <h2>Recent Posts</h2>	
                                <ul>
                                    %for post in recent_posts[:6]:
                                    <li><a href="/${post.date.year}/${post.date.month}/${post.id}" title="${post.title}">${post.title}</a></li>
                                    %endfor
                                </ul>
                                </li>


                                <li class="widget"><h2>Archives</h2>		<ul>
                                    %for arch in archives:
                                    <li><a href="" title="${arch[0]}">${arch[0]}</a>&nbsp;(${arch[1]})</li>
                                    %endfor
                                </ul>
                                </li>


                                <!-- tweet widget
                                <li class="widget">
                                <h2> <a class="tgt-twitter-follow" href="" title="Follow learnmongo On Twitter" target="_blank" rel="nofollow"><img src="./Vincent's Notes_files/follow_me-a.png"></a> </h2> </li>

                                <li class="tgt_tweet"> <a href="" title="Follow LearnMongo On Twitter" target="_blank" rel="nofollow"><img class="alignleft" src="./Vincent's Notes_files/learnmongo_normal.png" alt="avatar"></a>
                                <div class="tgt_tweet_dat">
                                    @shift8creative yea some slides and code will be ready in a day or two!<span class="tgt_twitter_meta">5 days ago via <a href="" rel="nofollow">Twitter for iPhone</a></span>
                                </div>
                                </li>

                                <li class="tgt_tweet">
                                <a href="" title="Follow LearnMongo On Twitter" target="_blank" rel="nofollow"><img class="alignleft" src="./Vincent's Notes_files/learnmongo_normal.png" alt="avatar"></a>
                                <div class="tgt_tweet_dat">
                                    Thanks for coming to the session, sorry  the technical issues threw me off a bit. Exciting to hear about the roadmap at #mongoseattle now!<span class="tgt_twitter_meta">5 days ago via <a href="" rel="nofollow">Twitter for iPhone</a></span>
                                </div>
                                </li>

                                -->
                            </ul>

                        </div>
                    </div><!-- /c2 -->

                </div><!-- /innerwrap -->

            </div>

            <div class="navigation">
                <div class="innerwrap" id="innerwarp-bottom">
                    <div class="Nav">
                        <% count = recent_posts.count() %>
                        %for i in range(0, count/10 + 1):
                        %if i+1 == p:
                        <strong class="on">${i+1}</strong>
                        %else:
                        <%
                            import copy, urllib
                            c_q = copy.copy(current_query)
                            c_q['p'] = i+1
                        %>
                        <a href="?${urllib.urlencode(c_q)}">${i+1}</a>
                        %endif
                        %endfor
                </div>
            </div>
            </div>

            <div id="footer">

                <div class="innerwrap">

                    <div id="footer-info">

                    </div>

                </div>

            </div>


    </body></html>
