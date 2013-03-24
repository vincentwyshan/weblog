<%inherit file="blog_base.mako" />

<%block name="meta_head">
<title>${post.content_title}</title>

<script type="text/javascript" src="http://w.sharethis.com/button/buttons.js"></script>
</%block>



<%block name="_body">

<div>
<article class="hentry">

<div class="tags">
    %for i in range(len(post.tags)):
        <% import urllib %>
        <% tag = post.tags[i] %>
        %if i > 0:
            ,&nbsp;
        %endif
        <a href="/tag/${urllib.quote(tag.name)}">${tag.name}</a>
    %endfor
</div>

<header>
    <h1 class="entry-title"><a rel="full-article" href="">${post.content_title}</a></h1>
    <p class="meta">
        <time>${post.date.strftime('%b %d, %Y')}</time>
    </P>
</header>

<div class="entry-content">
    ${post.html_content|n}
</div>

<footer>
    <p class="meta">
        <span class="byline author vcard">
            Posted by Vincent W
        </span>
        <time>${post.date.strftime('%b %d, %Y')}</time>
        <span class="categories">
            %for i in range(len(post.tags)):
                <% import urllib %>
                <% tag = post.tags[i] %>
                %if i > 0:
                    ,
                %endif
                <a class="category" href="/tag/${urllib.quote(tag.name)}">${tag.name}</a>
            %endfor
        </span>
    </p>


    <div class="sharing" style="text-align:right;">
        <span class='st_googleplus_large' displayText='Google +'></span>
        <span class='st_reddit_large' displayText='Reddit'></span>
        <span class='st_facebook_large' displayText='Facebook'></span>
        <span class='st_twitter_large' displayText='Tweet'></span>
        <span class='st_sina_large' displayText='Sina'></span>
        <script type="text/javascript">stLight.options({publisher: "b2657899-882a-4e2b-ad5c-acdc57c3b096", doNotHash: false, doNotCopy: false, hashAddressBar: false});</script>
    </div>

    <p class="meta">
        %if prev_post:
        <a class="basic-alignment left" href="/post/${prev_post.url}" title="${prev_post.content_title}">« ${prev_post.content_title}</a>
        %endif
       
        %if next_post:
        <a class="basic-alignment right" href="/post/${next_post.url}" title="${next_post.content_title}">${next_post.content_title} »</a>
        %endif
    </p>

</footer>



<hr id="post-end">

## disqus
    <div id="disqus_thread"></div>
    <script type="text/javascript">
        /* * * CONFIGURATION VARIABLES: EDIT BEFORE PASTING INTO YOUR WEBPAGE * * */
        var disqus_shortname = 'loglogvincent'; // required: replace example with your forum shortname

        /* * * DON'T EDIT BELOW THIS LINE * * */
        (function() {
            var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
            dsq.src = '//' + disqus_shortname + '.disqus.com/embed.js';
            (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
        })();
    </script>
    <noscript>Please enable JavaScript to view the <a href="http://disqus.com/?ref_noscript">comments powered by Disqus.</a></noscript>
    <a href="http://disqus.com" class="dsq-brlink">comments powered by <span class="logo-disqus">Disqus</span></a>
    


      <div id="disqus_thread"></div>
    <script type="text/javascript">
        /* * * CONFIGURATION VARIABLES: EDIT BEFORE PASTING INTO YOUR WEBPAGE * * */
        var disqus_shortname = 'vincentwsblog'; // required: replace example with your forum shortname

        /* * * DON'T EDIT BELOW THIS LINE * * */
        (function() {
            var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
            dsq.src = 'http://' + disqus_shortname + '.disqus.com/embed.js';
            (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
        })();
    </script>
    <noscript>Please enable JavaScript to view the <a href="http://disqus.com/?ref_noscript">comments powered by Disqus.</a></noscript>
    <a href="http://disqus.com" class="dsq-brlink">comments powered by <span class="logo-disqus">Disqus</span></a>


</article>
</div>
    

</%block>
