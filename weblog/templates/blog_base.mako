<!DOCTYPE html>
<html>
    <head>
	<meta charset=utf-8>
	<meta name="description" content="Vincent-W's weblog.">
    <meta name="author" content="Vincent W">

  <link href="/static/screen.css" media="screen, projection" rel="stylesheet" type="text/css">


 <!--Fonts from Google"s Web font directory at http://google.com/webfonts -->
<link href="http://fonts.googleapis.com/css?family=PT+Serif:regular,italic,bold,bolditalic" rel="stylesheet" type="text/css">
<link href="http://fonts.googleapis.com/css?family=PT+Sans:regular,italic,bold,bolditalic" rel="stylesheet" type="text/css">


<style type="text/css">

</style>


	<%block name="meta_head">
	</%block>


    </head>


  <body>




<!-- header -->
 <%block name="header">
<header role="">
<div id="header-content"><hgroup>
  <h1><a href="/">VINCENT W</a></h1>
  
</hgroup>


<%block name="nav">
  	<nav role="navigation">
  	<div id="nav-content">

<form action="http://google.com/search" method="get">
  <fieldset role="search">
    <input type="hidden" name="q" value="site:www.loglogvincent.com">
    <input class="search" type="text" name="q" results="0" placeholder="Search">
  </fieldset>
</form>
<ul class="main-navigation">
  <li><a href="/">Blog</a></li>
  <li><a href="/about">About</a></li>
  <li><a href="/rss">RSS</a></li>
</ul>

</div>
</nav>
 </%block>

  </div>
  </header>
  </%block>
<!-- end header -->












	<div id="main">
	<div id="content">


		
	    <%block name="_body">

	    <%doc><div class="blog-index">
	    <article>
		<p>hello</p>
	    </article>
	    </div>
	    </%doc>

	    </%block>
	    


	    <aside class="sidebar">
	    <section>
		  <h1>Recent Posts</h1>
		  <ul id="recent_posts">
		    
		    %for post in recent_posts:
		      <li class="post">
		        <a href="/post/${post.url}">${post.content_title}</a>
		      </li>
		    %endfor

		  </ul>
		</section>
	    </aside>

	    </div>
	</div>






<footer style="text-align:center;">
<%block name="footer">

<p>© Copyright 2012 by Vincent w. 
Contact me via <a href="mailto:vincent.syshan@gmail.com">mail</a>, <a href="http://weibo.com/2119986460">weibo</a>, <a href="https://github.com/vincentwv">github</a>. </p>
 </%block>


</footer>

    </body>
</html>

