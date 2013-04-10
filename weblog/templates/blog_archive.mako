<%inherit file="blog_base.mako" />

<%block name="meta_head">
<title>${title}</title>
</%block>


<%block name="_body">

<div>

<article>
	<header>
		<h1 class="entry-title">${title}</h1>
	</header>

	<div id="blog-archives">
	%for year, posts in post_by_year:
		<h2>${year}</h2>
		%for post in posts:
		<article>
			<h1><a href="/post/${post.url}">${post.title}</a></h1>

			<time>
				<span class="month">${month_name(post.date.month)}</span>
				<span class="day">${post.date.strftime("%d")}</span>
				<span class="year">${post.date.year}</span>
			</time>

			<footer>
  				<span>taged in 
  				%for i in range(len(post.tags)):
  					<% tag = post.tags[i] %>
  					%if i == 0:
  					<a class="category" href="/tag/${tag.name}">${tag.name}</a>
  					%else:
  					,&nbsp;
  					<a class="category" href="/tag/${tag.name}">${tag.name}</a>
  					%endif
  				%endfor
  				</span>
			</footer>

		</article>
		%endfor
	%endfor
	</div>

</article>

</div>

</%block>
