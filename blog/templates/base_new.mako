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



        <div id="main">

            <div class="innerwrap">

                <div id="c1">


%for entry in entries:
                    <!-- post -->
                    <div class="" id="post-${entry.id}">

                        <div class="post-title">
                            <h1>
                                <a href="/${entry.date.year}/${entry.date.month}/${entry.id}" rel="bookmark">${entry.title}</a>
                            </h1>
                            <%
                                import datetime, urllib
                            %>
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
                            ##${content.replace('literal-block', 'literal-block prettyprint') | n,trim}
                            ${entry.shortcontent | n,trim}
                        </div>

                        <div class="post-pages"></div>
                        <div class="post-foot">
                            <a href="http://learnmongo.com/posts/mongo-seattle-2011/#disqus_thread" class="comments-link" title="Comment on Mongo Seattle 2011" data-disqus-identifier="1143 http://learnmongo.com/?p=1143">0 Comments and 0 Reactions</a>				<div class="post-meta">
                                <div class="post-tags"></div>
                            </div>
                        </div>
                    </div>
                    <div class="sep"></div>

%endfor

                </div>








                <!-- column right -->
                <div id="c2">

                    <div id="sidebar">

                        <ul id="widgets">

                            <li class="widget">
                            <h2>Search LearnMongo</h2>
                            <form method="get" id="searchform" action="">
                                <input type="text" onfocus="if (this.value == &#39;Search&#39;) {this.value = &#39;&#39;;}" onblur="if (this.value == &#39;&#39;) {this.value = &#39;Search&#39;;}" value="Search" name="s">
                            </form>
                            </li>




                            <li class="widget"><h2>Follow Me on Twitter!</h2>			<div class="textwidget"><p><a href="https://twitter.com/vincentwv" class="twitter-follow-button" data-show-count="false">Follow @vincentwv</a><br>
                                </p>
                            </div>
                            </li>

                            <li class="widget">
                            <h2>Speaking</h2>	
                            <div id="gtalkwidget">
                                <!--<a href=""><img style="width:75%;" src="/static/image/mongoLA_badge_blank.png"></a>
                                <br>-->
                                <iframe src="http://www.google.com/talk/service/badge/Show?tk=z01q6amlqb5ighq076lqoblqmum5r1tt1m4rdjh9rak3a33u8mdbopdh6kppfsssk347q8c48hu9eho2dk5g9dq7ocn8nk85ldh169rbseel0apl617759qacbcjpq9m52fifp7fe2on6c07ojopmc38kke2dnsfbfmth5agq7102v8tijfubjdei42gpq8k5c8&amp;w=200&amp;h=60" frameborder="0" allowtransparency="true" width="200" height="60"></iframe>
                            </div>
                            </li>


                            <li class="widget"><h2>Categories</h2>	
                            <ul>
                                %for category in categories:
                                <li class="cat-item"><a href="" title="">${category.name}</a>
                                (${category.postcount})
                                </li>
                                %endfor
                            </ul>
                            </li>		



                            <li class="widget">	
                            <h2>Recent Posts</h2>	
                            <ul>
                                %for post in recent_posts:
                                <li><a href="" title="${post.title}">${post.title}</a></li>
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
            <div class="innerwrap">
                <div class="Nav">
                    <strong class="on">1</strong> <a href="">2</a>  <a href="">3</a>  <a href="">4</a> <a href="">Next »</a> ... <a href="">Last »</a></div> 	</div>
        </div>

        <div id="footer">

            <div class="innerwrap">

                <div id="footer-info">

                </div>

            </div>

        </div>


</body></html>
