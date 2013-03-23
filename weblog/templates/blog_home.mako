<%inherit file="blog_base.mako" />

<%block name="meta_head">
<title>Blog | Vincent W's Thoughts and Writings</title>
</%block>


<%block name="_body">

<div class="blog-index">

%for post in posts:

<article>

    <header>
    <h1 class="entry-title"><a href="/post/${post.url}">${post.content_title}</a></h1>
    <p class="meta">
        <time>${post.date.strftime('%b %d, %Y')}</time>
        |
        <a href="http://www.loglogvincent.com/post/${post.url}#disqus_thread">0 Comments</a>
    </p>
    </header>

    <div class="entry-content">
    ${post.summary}
    </div>

    <footer>
    <a rel="full-article" href="/post/${post.url}">Read on →</a>
    </footer>

</article>


%endfor




<div class="pagination">
    
    %if page_num > 0:
      <a class="prev" href="/page/${page_num-1}">← Older</a>
    %endif
    
    <a href="/blog/archives">Blog Archives</a>
    
    %if max_page_num > page_num:
    <a class="next" href="/">Newer →</a>
    %endif
  </div>
    


</div>



##disqus comments count:
    <script type="text/javascript">
    /* * * CONFIGURATION VARIABLES: EDIT BEFORE PASTING INTO YOUR WEBPAGE * * */
    var disqus_shortname = 'loglogvincent'; // required: replace example with your forum shortname

    /* * * DON'T EDIT BELOW THIS LINE * * */
    (function () {
        var s = document.createElement('script'); s.async = true;
        s.type = 'text/javascript';
        s.src = '//' + disqus_shortname + '.disqus.com/count.js';
        (document.getElementsByTagName('HEAD')[0] || document.getElementsByTagName('BODY')[0]).appendChild(s);
    }());
    </script>
    

</%block>

